---
name: scrm-babysit-pr
description: Use when the user asks to babysit, watch, or monitor a pull request on GitHub or Azure DevOps for a while, e.g. "babysit this PR for an hour", "watch PR 123 and handle the review comments", "keep an eye on CI for my PR". Waits for new review comments and CI results, fixes valid findings, and reports every change.
argument-hint: '<pr-url> [for <duration>]'
disable-model-invocation: true
---

# Babysit PR

Watch one pull request for a fixed time. React to new review comments and CI results. Report every change to the user.

## Language

English is the user's second language. Use short sentences and common words. Avoid idioms and slang. Technical terms are fine. Replies you post on the PR follow the same rule.

## Setup

1. **PR.** Take the URL from the request.
   - Only a number: GitHub `gh pr view <n> --json url -q .url`. Azure DevOps: `az repos pr show --id <n> --query repository.webUrl -o tsv`, then add `/pullrequest/<n>`.
   - Nothing: use the PR of the current branch. GitHub `gh pr view --json url -q .url`. Azure DevOps: `az repos pr list --source-branch <branch> --query "[0].[pullRequestId, repository.webUrl]" -o tsv`, then build the URL the same way.
2. **Time.** Take the duration from the request. Default: 1 hour. Say which one you use.
3. **Network (Codex).** The Codex sandbox blocks network access by default. The watcher, `gh`, `az`, and `git push` need it. Ask for it before the first call.
4. **Login.** GitHub: `gh auth status`. Azure DevOps: `az repos pr show --id <id> --org <org>` (needs the `azure-devops` extension). If it fails, stop and ask the user to log in.
5. **Commands.** Read [references/github.md](references/github.md) or [references/azure.md](references/azure.md) before the first call.
6. **Branch.** Work on the PR's source branch. If the checkout has other changes, ask before you switch.
7. **Baseline.** Run the watcher once. It saves the current state and prints a summary. `<skill-dir>` is the folder of this file. `<minutes>` is the duration in minutes (1 hour = 60).

   ```bash
   python3 <skill-dir>/scripts/pr_watch.py <pr-url> --reset --minutes <minutes>
   ```

8. **Existing work.** Handle the open threads and failed checks from the summary first (see below). If there are many, ask the user first.
9. **Draft PR.** Some bots and pipelines skip drafts. Ask if the user wants to trigger them (commands file). Never mark the PR as ready yourself.
10. Tell the user what you watch and when the watch ends.

## Watch loop

Run the watcher again. It checks right away, then every 60 seconds. It exits as soon as something changes and prints one line per change. The end time is saved, so don't pass `--reset` or `--minutes` in the loop.

- **Claude Code:** `python3 <skill-dir>/scripts/pr_watch.py <pr-url>` in the background (Bash with `run_in_background`). You get a message when it exits. Don't poll in the foreground.
- **Codex and other tools:** `python3 <skill-dir>/scripts/pr_watch.py <pr-url> --max-wait 9` in the foreground, with a 10-minute command timeout. `NO CHANGE` means: run it again.

Handle the events, then run the watcher again. Stop at `DEADLINE` or `DONE`. To change the end time, add `--minutes N` once: the watch then ends N minutes from now.

| Event                                                                                                            | Action                                                                                                                                                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `COMMENT ... [ai]`                                                                                               | Your own reply. Ignore it.                                                                                                                                                                                                                               |
| `COMMENT ...`                                                                                                    | Maybe a review finding. Handle it (next section).                                                                                                                                                                                                        |
| `THREAD <id> <old> -> open` (GitHub) or `-> active` (Azure)                                                      | A reviewer reopened a thread. Handle it as a new finding.                                                                                                                                                                                                |
| `CHECK '<name>' ... -> <result>`, any result except `success`, `approved`, `skipped`, `neutral`, `notapplicable` | A failed check. Read the log (commands file). If the PR caused it, fix and push. If it looks flaky (unrelated to the change, passes locally), re-run it, at most 2 times. Azure policies without a build (reviewers, comments, work items): report only. |
| `NEW COMMIT <sha>`                                                                                               | Someone pushed (maybe you). If it was not you, pull before you change anything.                                                                                                                                                                          |
| `MERGE ... -> conflicting`                                                                                       | Report at once. Ask before you fix the conflict.                                                                                                                                                                                                         |
| `DONE` / `DEADLINE`                                                                                              | Stop and write the summary.                                                                                                                                                                                                                              |
| `ERROR`                                                                                                          | The CLI failed 3 times in a row. Show the error and ask the user.                                                                                                                                                                                        |
| Anything else (passed checks, votes, other thread changes, draft changes)                                        | Report briefly.                                                                                                                                                                                                                                          |

## Handle a review finding

1. Read the comment and the code it points to, in its current version. The code may have changed since the comment.
2. Decide: still valid, already fixed, wrong, or no action needed (thanks, status updates, summaries). Don't reply to comments that need no action. This avoids reply loops with bots.
3. If valid: make the smallest fix. Run the project's checks for the changed code (lint, tests, types). Commit with a clear message and push.
4. Reply in the thread: what you changed (with the commit sha), or why no change is needed.
   - **Bot reviewer** (CodeRabbit, Copilot, SonarCloud, and similar): post the reply and resolve the thread. Azure DevOps: set the status to `fixed` after a code change, or `wontFix` / `byDesign` when you change nothing.
   - **Human reviewer:** show the draft reply to the user. Post it only after the user says OK. Don't resolve human threads unless the user says so.
5. End every reply you post with this line. It tells people an agent wrote it, and the watcher uses it to skip your own replies:
   `_AI-generated reply (scrm-babysit-pr)_`

## Rules

- Never merge, close, approve, or abandon the PR. Never mark a draft as ready.
- Merge conflicts: after the user agrees, merge the base branch into the PR branch. Rebase only if the user asks for it, then push with `--force-with-lease`. Never use a plain `--force`.
- Ask before big changes and changes outside the PR's scope.
- Report-only mode: if the user says "only report" or "show me first", collect the findings and report them. Don't fix or post anything.

## End

Write a short summary: what happened, what you fixed (with commits), and what is still open for the user.
