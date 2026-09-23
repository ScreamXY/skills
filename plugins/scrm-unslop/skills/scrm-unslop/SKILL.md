---
name: scrm-unslop
description: Use when the user wants AI tells removed from a text, e.g. "unslop this", "make this sound less like AI", "clean up this draft". Rewrites the text in plain, direct English and keeps the meaning and tone.
disable-model-invocation: true
---

# Unslop

Edit text to remove AI writing patterns.

## Language

English is the user's second language. Use short sentences and common words. Avoid idioms and slang. Technical terms are fine. The rewritten text must also be easy to read for a non-native reader.

## Input

The text or file the user names. If they name nothing, use your own last message. Edit files in place. Return pasted text as a rewrite.

## Process

1. Scan for the patterns below.
2. Rewrite. Keep the meaning and the intended tone.

## Patterns to detect and fix

### Content

- **Superficial -ing phrases.** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete, or expand with real sources.
- **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete.

### Language

- **AI vocabulary.** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Replace with plain words.
- **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Say "is" or "has".
- **"Not just X, but Y."** State the point directly.
- **Rule of three.** Forcing ideas into groups of three. Use the natural number.
- **Synonym cycling.** Protagonist, main character, central figure, hero in one paragraph. Pick one word and repeat it.
- **False ranges.** "from X to Y" where X and Y are not on a meaningful scale. List the topics directly.

### Style

- **Em dash overuse.** Avoid em dashes entirely. Use periods or commas only (no parentheses, no en dashes, no hyphen-as-dash). If a thought needs separation, end the sentence or use a comma.
- **Colon overuse.** Colons are fine before a list or an example, not as mid-sentence connectors. "If you're coming from traditional automation: instead of registering event handlers, you describe conditions" becomes "Describing when the scheduler should fire works best as plain English."
- **Boldface overuse.** Don't bold every proper noun or acronym.
- **Inline-header lists.** The tell is a bold label and colon that restates the line: "**Performance:** Performance improved...". Convert those to prose. A bold lead-in that ends in a period, names the item, and adds new detail ("**Schema in TypeScript.** Tables live in one file.") is fine.
- **Title case headings.** Use sentence case.
- **Decorative emojis.** Remove them from headings and bullets.
- **Curly quotes.** Replace with straight quotes.

### Communication artifacts

- **Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!". Remove.
- **Sycophantic tone.** "Great question! You're absolutely right!". Respond directly.

### Filler

- **Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". "It is important to note that" gets deleted.
- **Excessive hedging.** "could potentially possibly be argued that it might" becomes "may".
- **Generic conclusions.** "The future looks bright." State specific plans or facts.

### Jargon

- **Abstract metaphor nouns.** Substrate, wedge, vector, locus, vantage, nexus, primitive (as noun), harness (as metaphor), surface (as in "API surface"), bedrock, scaffolding (as metaphor), modality, paradigm, gold-plating, ratchet (as metaphor), evacuate (for moving code), endgame, north star, flywheel. Pick the concrete word: "substrate" becomes "base", "wedge in" becomes "add", "vector" becomes "way", "gold-plating" becomes "more than the job needs", "evacuate" becomes "move out", "endgame" becomes "the last phase".

### Plain speech

- **Say what it does, not how it feels.** "the database stays close at hand" names a feeling. Name the mechanism or a number instead: "`.toSQL()` returns the exact string sent to the database". If you can't restate a sentence as a concrete instruction, fact, or number, cut it. If it could appear unchanged in another project's docs, it says nothing about this one. Cut it.
- **Shorten or split dense sentences.** If the reader has to backtrack, break the sentence in two or drop clauses. One idea per sentence.
- **Active voice.** Name the actor: "queries are validated" becomes "the compiler validates queries". Passive is fine only when the actor is unknown or does not matter.
- **Cut adverbs, or use a stronger verb.** "runs quickly" becomes "is fast" or the number. "significantly improves" becomes the measured delta.
- **Prefer the plain word.** "utilize" and "leverage" become "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if".
- **Mannered prose.** Metaphor or flourish where a literal phrase exists: aphorisms ("wire it or delete it"), rhetorical fragments, personified code ("the plan holds it"), figurative verbs ("rides along", "stands on"). "A dial worth turning" becomes "a parameter worth varying". The jargon section covers the metaphor nouns.
- **Over-compression.** Dropped articles, verbless fragments, symbol-speak, and abbreviations that make the reader decode instead of read. "Parser rejects bad date → exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing."
