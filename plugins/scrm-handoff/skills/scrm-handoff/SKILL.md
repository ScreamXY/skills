---
name: scrm-handoff
description: Use when the user wants to continue the current work in a fresh agent session, e.g. "write a handoff", "compact this for the next session". Writes a handoff document to the OS temp directory.
argument-hint: '[what the next session will focus on]'
disable-model-invocation: true
---

# Handoff

Write a handoff document that summarizes the current conversation, so a fresh agent can continue the work.

## Language

English is the user's second language. Use short sentences and common words. Avoid idioms and slang. Technical terms are fine.

## Rules

- Save the document in the OS temp directory (for example `$TMPDIR` or `/tmp`), not in the workspace. Tell the user the full path.
- If the user passed arguments, they describe what the next session will focus on. Tailor the document to that.
- Include a "Suggested skills" section: which skills the next agent should load.
- Don't copy content that already lives in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL.
- Redact sensitive information: API keys, passwords, tokens, personal data.
