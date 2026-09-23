---
name: scrm-wait-what
description: Use when the user did not understand your last message, e.g. "wait, what?", "I don't get it", "say that again, simpler". Explains the last message again, with the missing context,, in Simplified Technical English and the project's own words.
disable-model-invocation: true
---

# Wait, what?

## Language

English is the user's second language. Use short sentences and common words. Avoid idioms and slang. Technical terms are fine.

## Explain it again

The user did not understand your last message. Explain it again:

1. Start with a little context: where are we, and what problem are we solving?
2. Then give the point again in ASD-STE100 Simplified Technical English: short sentences, one idea per sentence, common words, active voice.
3. Use the project's own terms from `CONTEXT.md`. If the repo has a `CONTEXT-MAP.md`, follow it to the right `CONTEXT.md`. If neither exists, use the words from the code and from the user.

Keep it short. Don't just repeat the old message with small changes.
