---
name: scrm-eli5
description: Use when the user types /scrm-eli5 or $scrm-eli5 <topic> or asks for a dead-simple picture explanation of how something works, e.g. "explain it like I'm five", "ELI5 this". Builds one HTML page with big pictures and few words.
---

# ELI5

Explain the topic to someone who knows nothing about it. Build one HTML page with big pictures and few words.

The topic is the text after the command. If there is none, use the current topic of the conversation.

## Language

English is the user's second language. Use short sentences and common words. Avoid idioms and slang. Technical terms are fine. Here, explain each one with a picture.

## How

- Write one self-contained HTML file (inline CSS and SVG, no external files). Save it in the OS temp directory as `eli5-<topic>.html`.
- The pictures do the explaining. Draw them large, with inline SVG. Give each picture one short caption.
- Use few words: short labels, one idea per section, no long paragraphs.
- Use an everyday comparison when it helps.
- Open the file (`open <file>` on macOS, `xdg-open <file>` on Linux) and tell the user the path.
