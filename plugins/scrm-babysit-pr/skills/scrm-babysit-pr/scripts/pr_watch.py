#!/usr/bin/env python3
"""Wait until a pull request changes, print what changed, then exit.

Works with GitHub (gh CLI) and Azure DevOps (az CLI with the azure-devops extension).

First run (no state file yet): save a baseline, print a summary, exit.
Later runs: check right away, then every --interval seconds. Exit as soon as
something changes, the PR is closed, the deadline passes, or --max-wait minutes pass.
The state file lives in the OS temp directory and is updated on every poll.
"""

import argparse
import json
import subprocess
import sys
import tempfile
import time
import urllib.parse
from pathlib import Path

AI_MARKER = 'scrm-babysit-pr'
PENDING = {'queued', 'in_progress', 'waiting', 'pending', 'requested', 'expected', 'running'}
AZURE_VOTES = {10: 'approved', 5: 'approved with suggestions', 0: 'no vote', -5: 'waiting for author', -10: 'rejected'}
AZURE_STATES = {'active': 'open', 'completed': 'merged', 'abandoned': 'closed'}
MAX_FAILURES = 3

GITHUB_QUERY = """
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      state isDraft headRefOid mergeable
      comments(last: 100) { nodes { databaseId author { login } body } }
      reviews(last: 100) { nodes { databaseId author { login } state body } }
      reviewThreads(last: 100) {
        nodes {
          id isResolved path
          comments(first: 100) { nodes { databaseId author { login } body } }
        }
      }
      commits(last: 1) {
        nodes { commit { statusCheckRollup { contexts(first: 100) { nodes {
          __typename
          ... on CheckRun { name status conclusion }
          ... on StatusContext { context state }
        } } } } }
      }
    }
  }
}
"""


def run_json(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:4])} failed: {result.stderr.strip()[:300]}")
    return json.loads(result.stdout)


def parse_url(url):
    parts = urllib.parse.urlparse(url)
    path = [urllib.parse.unquote(p) for p in parts.path.split('/') if p]
    if parts.netloc == 'github.com' and len(path) >= 4 and path[2] == 'pull':
        return {'platform': 'github', 'owner': path[0], 'repo': path[1], 'number': int(path[3])}
    if parts.netloc == 'dev.azure.com' and len(path) >= 6 and path[2] == '_git' and path[4] == 'pullrequest':
        org = f'https://dev.azure.com/{path[0]}'
        return {'platform': 'azure', 'org': org, 'project': path[1], 'repo': path[3], 'number': int(path[5])}
    if parts.netloc.endswith('.visualstudio.com') and len(path) >= 5 and path[1] == '_git' and path[3] == 'pullrequest':
        org = f'https://{parts.netloc}'
        return {'platform': 'azure', 'org': org, 'project': path[0], 'repo': path[2], 'number': int(path[4])}
    sys.exit(f'Unsupported PR URL: {url}')


def comment(author, where, body):
    lines = (body or '').strip().splitlines()
    text = ' '.join((body or '').split())
    return {
        'author': author,
        'where': where,
        'text': text[:160] + ('...' if len(text) > 160 else ''),
        # Only the last line counts, so a human quote-reply of our comment is not tagged.
        'ai': bool(lines) and AI_MARKER in lines[-1],
    }


def github_snapshot(pr):
    data = run_json([
        'gh', 'api', 'graphql', '-f', f'query={GITHUB_QUERY}',
        '-f', f"owner={pr['owner']}", '-f', f"repo={pr['repo']}", '-F', f"number={pr['number']}",
    ])
    p = data['data']['repository']['pullRequest']

    def login(node):
        return (node.get('author') or {}).get('login', 'ghost')

    comments, threads, votes, checks = {}, {}, {}, {}
    for c in p['comments']['nodes']:
        comments[f"c{c['databaseId']}"] = comment(login(c), 'conversation', c['body'])
    for r in p['reviews']['nodes']:
        if r['body']:
            comments[f"r{r['databaseId']}"] = comment(login(r), f"review ({r['state'].lower()})", r['body'])
        if r['state'] in ('APPROVED', 'CHANGES_REQUESTED', 'DISMISSED'):
            votes[login(r)] = r['state'].lower().replace('_', ' ')
    for t in p['reviewThreads']['nodes']:
        threads[t['id']] = 'resolved' if t['isResolved'] else 'open'
        for c in t['comments']['nodes']:
            comments[f"t{c['databaseId']}"] = comment(login(c), f"{t['path']} (thread {t['id']})", c['body'])

    commits = p['commits']['nodes']
    rollup = (commits[0]['commit']['statusCheckRollup'] if commits else None) or {}
    for node in rollup.get('contexts', {}).get('nodes', []):
        if node['__typename'] == 'CheckRun':
            status = node['conclusion'] if node['status'] == 'COMPLETED' else node['status']
            checks[node['name']] = (status or 'unknown').lower()
        else:
            checks[node['context']] = node['state'].lower()

    return {
        'state': p['state'].lower(),
        'draft': p['isDraft'],
        'head': p['headRefOid'],
        'merge': p['mergeable'].lower(),
        'checks': checks,
        'threads': threads,
        'comments': comments,
        'votes': votes,
    }


def azure_snapshot(pr):
    base = ['--org', pr['org'], '-o', 'json']
    info = run_json(['az', 'repos', 'pr', 'show', '--id', str(pr['number'])] + base)
    project = info['repository']['project']['name']
    repo_id = info['repository']['id']
    policies = run_json(['az', 'repos', 'pr', 'policy', 'list', '--id', str(pr['number'])] + base)
    raw_threads = run_json([
        'az', 'devops', 'invoke', '--area', 'git', '--resource', 'pullRequestThreads',
        '--route-parameters', f'project={project}', f'repositoryId={repo_id}', f"pullRequestId={pr['number']}",
        '--api-version', '7.1',
    ] + base)

    checks = {}
    for policy in policies:
        config = policy.get('configuration') or {}
        name = (config.get('settings') or {}).get('displayName') or (config.get('type') or {}).get('displayName', '?')
        if name in checks:
            name = f"{name} ({policy.get('evaluationId', '?')[:8]})"
        checks[name] = policy.get('status', 'unknown').lower()

    comments, threads = {}, {}
    for t in raw_threads.get('value', []):
        texts = [c for c in t.get('comments', []) if c.get('commentType') == 'text' and not c.get('isDeleted')]
        if t.get('isDeleted') or not texts:
            continue
        path = (t.get('threadContext') or {}).get('filePath') or 'conversation'
        threads[str(t['id'])] = t.get('status') or 'unknown'
        for c in texts:
            author = (c.get('author') or {}).get('displayName', '?')
            comments[f"{t['id']}.{c['id']}"] = comment(author, f"{path} (thread {t['id']})", c.get('content'))

    votes = {r['displayName']: AZURE_VOTES.get(r.get('vote', 0), str(r.get('vote'))) for r in info.get('reviewers', [])}
    merge = info.get('mergeStatus', 'unknown')
    return {
        'state': AZURE_STATES.get(info['status'], info['status']),
        'draft': info.get('isDraft', False),
        'head': info['lastMergeSourceCommit']['commitId'],
        'merge': 'conflicting' if merge == 'conflicts' else merge.lower(),
        'checks': checks,
        'threads': threads,
        'comments': comments,
        'votes': votes,
    }


def format_comment(cid, c):
    tag = ' [ai]' if c['ai'] else ''
    return f"COMMENT {cid} by {c['author']}{tag} on {c['where']}: {c['text']}"


def diff(old, new):
    events = []
    if old['head'] != new['head']:
        events.append(f"NEW COMMIT {new['head'][:8]}")
    if old['draft'] != new['draft']:
        events.append('DRAFT -> ready for review' if not new['draft'] else 'READY -> draft')
    if old['merge'] != new['merge'] and 'conflicting' in (old['merge'], new['merge']):
        events.append(f"MERGE {old['merge']} -> {new['merge']}")
    for name, status in new['checks'].items():
        before = old['checks'].get(name, 'new')
        if before != status and status not in PENDING:
            events.append(f"CHECK '{name}' {before} -> {status}")
    for tid, status in new['threads'].items():
        before = old['threads'].get(tid)
        if before and before != status:
            events.append(f'THREAD {tid} {before} -> {status}')
    for cid, c in new['comments'].items():
        if cid not in old['comments']:
            events.append(format_comment(cid, c))
    for who, vote in new['votes'].items():
        if old['votes'].get(who) != vote:
            events.append(f'VOTE {who} -> {vote}')
    if old['state'] != new['state']:
        events.append(f"PR {old['state']} -> {new['state']}")
    return events


def print_baseline(url, snap, deadline):
    print(f'BASELINE {url}')
    print(f"state={snap['state']} draft={str(snap['draft']).lower()} head={snap['head'][:8]} merge={snap['merge']}")
    failing = [f"'{n}' {s}" for n, s in snap['checks'].items() if s not in PENDING | {'success', 'approved', 'skipped', 'neutral', 'notapplicable'}]
    pending = [n for n, s in snap['checks'].items() if s in PENDING]
    print(f"CHECKS {len(snap['checks'])} total, {len(pending)} pending, failing: {', '.join(failing) or 'none'}")
    open_threads = [tid for tid, s in snap['threads'].items() if s in ('open', 'active', 'pending')]
    print(f'OPEN THREADS {len(open_threads)}')
    for tid in open_threads:
        last = [c for c in snap['comments'].values() if f'(thread {tid})' in c['where']][-1:]
        for c in last:
            path = c['where'].split(' (thread ')[0]
            print(f"  thread {tid}: last by {c['author']}{' [ai]' if c['ai'] else ''} on {path}: {c['text']}")
    if snap['votes']:
        print('VOTES ' + ', '.join(f'{who}: {vote}' for who, vote in snap['votes'].items()))
    print(f"WATCHING until {time.strftime('%H:%M', time.localtime(deadline))}")


def poll(take, pr):
    for attempt in range(1, MAX_FAILURES + 1):
        try:
            return take(pr)
        except (RuntimeError, json.JSONDecodeError, KeyError, TypeError) as error:
            print(f'WARN poll failed ({attempt}/{MAX_FAILURES}): {error}', file=sys.stderr)
            if attempt == MAX_FAILURES:
                print(f'ERROR {error}')
                sys.exit(2)
            time.sleep(10)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('url', help='PR URL (github.com or dev.azure.com / *.visualstudio.com)')
    parser.add_argument('--minutes', type=float, help='watch window from now; sets or extends the deadline (default 60)')
    parser.add_argument('--max-wait', type=float, help='return after this many minutes without changes')
    parser.add_argument('--interval', type=int, default=60, help='seconds between polls (default 60)')
    parser.add_argument('--reset', action='store_true', help='forget the saved state and take a new baseline')
    args = parser.parse_args()

    pr = parse_url(args.url)
    take = github_snapshot if pr['platform'] == 'github' else azure_snapshot
    key = '-'.join(str(v) for k, v in pr.items() if k != 'platform').replace('https://', '').replace('/', '_')
    state_file = Path(tempfile.gettempdir()) / 'scrm-babysit-pr' / f"{pr['platform']}-{key}.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    if args.reset:
        state_file.unlink(missing_ok=True)

    def save(snap, deadline):
        state_file.write_text(json.dumps({'deadline': deadline, 'snapshot': snap}))

    if not state_file.exists():
        deadline = time.time() + (args.minutes or 60) * 60
        snap = poll(take, pr)
        save(snap, deadline)
        print_baseline(args.url, snap, deadline)
        return

    saved = json.loads(state_file.read_text())
    deadline = time.time() + args.minutes * 60 if args.minutes else saved['deadline']
    previous = saved['snapshot']
    started = time.time()
    while True:
        current = poll(take, pr)
        events = diff(previous, current)
        save(current, deadline)
        previous = current
        if events:
            print('\n'.join(events))
        if current['state'] != 'open':
            print(f"DONE the PR is {current['state']}")
            return
        if events:
            print(f"WATCHING until {time.strftime('%H:%M', time.localtime(deadline))}")
            return
        if time.time() >= deadline:
            print('DEADLINE reached')
            return
        if args.max_wait is not None and time.time() - started + args.interval >= args.max_wait * 60:
            print('NO CHANGE yet, run again')
            return
        time.sleep(args.interval)


if __name__ == '__main__':
    main()
