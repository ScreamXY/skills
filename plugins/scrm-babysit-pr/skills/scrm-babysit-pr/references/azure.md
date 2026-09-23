# Azure DevOps commands (az CLI)

Needs the `azure-devops` extension: `az extension add --name azure-devops`.

From the PR URL `https://dev.azure.com/<organization>/<project>/_git/<repo>/pullrequest/<id>`:

- `<org>` = `https://dev.azure.com/<organization>`
- `<project>`, `<repo>`, `<id>` as in the URL (decode `%20` to a space, and quote the value)

Several calls send a JSON body. Write it to a temp file and pass it with `--in-file <file>`.

## Read

- Overview: `az repos pr show --id <id> --org <org> -o json`
- Policies (builds, reviewers, comment rules): `az repos pr policy list --id <id> --org <org> -o table`
- Threads:

  ```bash
  az devops invoke --area git --resource pullRequestThreads \
    --route-parameters project=<project> repositoryId=<repo> pullRequestId=<id> \
    --org <org> --api-version 7.1 -o json
  ```

## Check out the branch

`az repos pr checkout --id <id>`

## Reply to a thread

The watcher prints comment ids as `<thread-id>.<comment-id>`.

Body: `{"content": "<text>", "parentCommentId": 1, "commentType": 1}`

```bash
az devops invoke --area git --resource pullRequestThreadComments \
  --route-parameters project=<project> repositoryId=<repo> pullRequestId=<id> threadId=<thread-id> \
  --http-method POST --in-file <body-file> --org <org> --api-version 7.1
```

## Set the thread status

Body: `{"status": "fixed"}`. Values: `active`, `fixed`, `wontFix`, `closed`, `byDesign`, `pending`.

```bash
az devops invoke --area git --resource pullRequestThreads \
  --route-parameters project=<project> repositoryId=<repo> pullRequestId=<id> threadId=<thread-id> \
  --http-method PATCH --in-file <body-file> --org <org> --api-version 7.1
```

## New top-level comment

Body: `{"comments": [{"content": "<text>", "commentType": 1}], "status": "active"}`. POST it to `pullRequestThreads` (same command as "Set the thread status", without `threadId`, with `--http-method POST`).

## Failed builds

- Build id per build policy:

  ```bash
  az repos pr policy list --id <id> --org <org> \
    --query "[?configuration.type.displayName=='Build'].{name:configuration.settings.displayName, status:status, build:context.buildId, evaluation:evaluationId}" -o table
  ```

- Failed tasks and their log ids:

  ```bash
  az devops invoke --area build --resource timeline \
    --route-parameters project=<project> buildId=<build-id> \
    --org <org> --api-version 7.1 --query "records[?result=='failed'].{name:name, log:log.id}" -o table
  ```

- Log lines (JSON, one line per entry):

  ```bash
  az devops invoke --area build --resource logs \
    --route-parameters project=<project> buildId=<build-id> logId=<log-id> \
    --org <org> --api-version 7.1 --query "value[-100:]"
  ```

- Re-queue a build policy: `az repos pr policy queue --id <id> --evaluation-id <evaluation-id> --org <org>`

## Draft PRs and bots

- Draft PRs often don't start build policies. Queue them with the command above.
- Trigger a CodeRabbit review: post a top-level comment with the text `@coderabbitai review`.
- Mark as ready: `az repos pr update --id <id> --draft false --org <org>`. Only when the user asks for it.
