---
name: scrm-grill-me
description: Use when the user wants a plan, design, or idea stress-tested, e.g. "grill me", "poke holes in this", "challenge my plan". Interviews the user in rounds of numbered questions, each with a recommended answer, until every decision is settled.
disable-model-invocation: true
---

# Grill me

Interview the user relentlessly about the plan until you both reach a shared understanding.

## Language

English is the user's second language. Use short sentences and common words. Avoid idioms and slang. Technical terms are fine.

## Process

Map the plan as a **design tree**: every decision branches into the decisions that depend on it.

Work the tree in **rounds**. The **frontier** is every open decision whose prerequisites are settled: the questions you can ask now without guessing answers you have not heard yet. Ask the whole frontier in one round. Number each question and give your recommended answer. Then wait for the user's answers.

Format a round like this:

```
❓ **Q1** - **<question title>**: <question body, can be several paragraphs, can include choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <your recommended answer>
```

Each answer reshapes the tree. Settled decisions unblock the questions that depended on them. Recompute the frontier and ask the next round. A question that depends on another question still open in this round belongs to a later round.

Finding facts is your job, never the user's. When a question needs a fact from the environment (code, files, tools), look it up yourself. Use a sub-agent if your tool has them. Never ask the user for something you can look up. Don't block on it: only the questions that depend on the missing fact wait. Ask the rest of the frontier now. Decisions belong to the user: ask, then wait.

The session is done when the frontier is empty: every branch visited, nothing silently assumed. Do not act on the plan until the user confirms that you reached a shared understanding.
