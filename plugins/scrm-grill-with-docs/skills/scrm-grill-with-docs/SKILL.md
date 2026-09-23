---
name: scrm-grill-with-docs
description: Use when the user wants a plan or design stress-tested and wants the domain language and decisions written down while you talk, e.g. "grill me and document it", "grill this and keep the glossary up to date". Interviews in rounds and keeps CONTEXT.md (glossary) and ADRs in docs/adr/ current.
disable-model-invocation: true
---

# Grill with docs

Interview the user relentlessly about the plan until you both reach a shared understanding. At the same time, build the project's domain model: the glossary in `CONTEXT.md` and the decisions in `docs/adr/`.

## Language

English is the user's second language. Use short sentences and common words. Avoid idioms and slang. Technical terms are fine. Write `CONTEXT.md` and ADRs in the same simple English.

## Grilling

Map the plan as a **design tree**: every decision branches into the decisions that depend on it.

Work the tree in **rounds**. The **frontier** is every open decision whose prerequisites are settled. Ask the whole frontier in one round. Number each question and give your recommended answer. Then wait for the user's answers.

```
❓ **Q1** - **<question title>**: <question body, can include choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <your recommended answer>
```

After each round, recompute the frontier. A question that depends on another question still open in this round belongs to a later round.

Finding facts is your job, never the user's. Look up facts from code, files, and tools yourself (use a sub-agent if your tool has them), and ask the rest of the frontier meanwhile. Decisions belong to the user: ask, then wait.

The session is done when the frontier is empty. Do not act on the plan until the user confirms that you reached a shared understanding. Writing `CONTEXT.md` and ADRs during the session is allowed: that is not acting on the plan.

## Domain model

### Files

Most repos have one context: `CONTEXT.md` at the root, ADRs in `docs/adr/`. If `CONTEXT-MAP.md` exists at the root, the repo has several contexts. The map shows where each `CONTEXT.md` lives. Decisions for the whole system go in the root `docs/adr/`. Decisions for one context go in that context's `docs/adr/`. When several contexts exist, infer which one the topic belongs to. If unclear, ask.

Create files lazily: only when you have something to write.

### During the session

- **Challenge against the glossary.** When the user uses a term that conflicts with `CONTEXT.md`, say so at once: "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy language.** When a term is vague or overloaded, propose one precise term: "You say 'account'. Do you mean the Customer or the User?"
- **Test with concrete scenarios.** Invent edge-case scenarios that force precise boundaries between concepts.
- **Cross-check with the code.** When the user says how something works, check the code. Surface contradictions: "Your code cancels whole Orders, but you said partial cancellation is possible. Which is right?"
- **Update `CONTEXT.md` right away** when a term is resolved. Don't batch. Use the format in [references/context-format.md](references/context-format.md). `CONTEXT.md` is a glossary and nothing else: no implementation details, no spec, no scratch notes.
- **Offer ADRs sparingly.** Only when all three are true: hard to reverse, surprising without context, and the result of a real trade-off. Use the format in [references/adr-format.md](references/adr-format.md).
