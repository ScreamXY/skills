# GitHub commands (gh CLI)

`<url>` is the PR URL. Take `<owner>`, `<repo>`, and `<n>` from it. For text with several lines, write it to a temp file first and pass the file (`-F body=@<file>` for `gh api`, `--body-file <file>` for `gh pr comment`).

## Read

- Overview: `gh pr view <url> --json title,state,isDraft,headRefName,baseRefName`
- Checks with links: `gh pr checks <url>`
- Inline review comments: `gh api repos/<owner>/<repo>/pulls/<n>/comments --paginate`
- Conversation: `gh pr view <url> --comments`

## Check out the branch

`gh pr checkout <url>`

## Reply

The watcher prints comment ids with a prefix: `t` = inline review comment, `c` = conversation comment, `r` = review body.

- Reply in a review thread (`t<id>` comments). Use the thread id `PRRT_...` from the watcher output:

  ```bash
  gh api graphql -f query='mutation($id: ID!, $body: String!) { addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $id, body: $body}) { comment { url } } }' -f id=<thread-id> -F body=@<file>
  ```

- Answer a conversation comment or a review body: `gh pr comment <url> --body-file <file>`

## Resolve a review thread

The thread id is the `PRRT_...` value in the watcher output.

```bash
gh api graphql -f query='mutation($id: ID!) { resolveReviewThread(input: {threadId: $id}) { thread { isResolved } } }' -f id=<thread-id>
```

## Failed checks

- `gh pr checks <url>` shows a link per check. For GitHub Actions, the run id is the number after `/runs/`.
- Failed log: `gh run view <run-id> --log-failed`
- Re-run only the failed jobs: `gh run rerun <run-id> --failed`
- Checks from external services (not GitHub Actions) can't be re-run with gh. Open their link and report.

## Draft PRs and bots

- Trigger a CodeRabbit review: `gh pr comment <url> --body '@coderabbitai review'`
- Mark as ready: `gh pr ready <url>`. Only when the user asks for it.
