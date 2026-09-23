# scrm skills

My personal agent skills for **Claude Code** and **Codex**. Every skill name starts with `scrm-`, so I can tell my skills apart from skills from other sources.

English is my second language. Every skill knows this and uses short sentences and common words.

## Skills

| Skill                  | What it does                                                                                              | Based on                                                                                                                                                                                                                                                                                                                   |
| :--------------------- | :-------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scrm-show-me`         | Explains the current topic visually: pseudocode, call trees, file trees, Mermaid, diffs, or an HTML page. | [humanlayer/skills: show-me](https://github.com/humanlayer/skills/tree/main/plugins/show-me/skills/show-me)                                                                                                                                                                                                                |
| `scrm-grill-me`        | Asks you about a plan in rounds of numbered questions. Each question has a recommended answer.            | [mattpocock/skills: grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) and [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)                                                                                                                     |
| `scrm-grill-with-docs` | Like `scrm-grill-me`, and keeps the glossary (`CONTEXT.md`) and the ADRs up to date.                      | [mattpocock/skills: grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs), [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling), and [domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling) |
| `scrm-wait-what`       | Explains the last message again: more context, simpler words.                                             | [mattpocock/skills: wait-what](https://github.com/mattpocock/skills/tree/main/skills/productivity/wait-what)                                                                                                                                                                                                               |
| `scrm-handoff`         | Writes a handoff document, so a fresh agent session can continue the work.                                | [mattpocock/skills: handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff)                                                                                                                                                                                                                   |
| `scrm-unslop`          | Removes AI writing patterns from a text.                                                                  | [cursor/plugins: unslop](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop)                                                                                                                                                                                                                                 |
| `scrm-eli5`            | Explains a topic with one HTML page: big pictures, few words.                                             | [anthropics/claude-plugins-community: eli5](https://github.com/anthropics/claude-plugins-community/tree/main/eli5/skills/eli5)                                                                                                                                                                                             |
| `scrm-babysit-pr`      | Watches a GitHub or Azure DevOps PR, handles review comments, and follows CI.                             | Idea from [POLYPOINT/skills: babysit-pr](https://github.com/POLYPOINT/skills/tree/main/skills/babysit-pr). New text, because the source is proprietary.                                                                                                                                                                    |

Only `scrm-eli5` can start by itself. You start the other skills yourself: `/scrm-grill-me` in Claude Code, `$scrm-grill-me` in Codex.

## Install

Each skill is its own plugin. Install only the ones you want.

### Claude Code

```bash
claude plugin marketplace add ScreamXY/skills
claude plugin install scrm-grill-me@scrm

# all skills
for s in show-me grill-me grill-with-docs wait-what handoff unslop eli5 babysit-pr; do claude plugin install "scrm-$s@scrm"; done
```

Update: `claude plugin marketplace update scrm`, then `claude plugin update <plugin>`. In a session you can use `/plugin` instead.

### Codex

```bash
codex plugin marketplace add ScreamXY/skills
codex plugin add scrm-grill-me@scrm

# all skills
for s in show-me grill-me grill-with-docs wait-what handoff unslop eli5 babysit-pr; do codex plugin add "scrm-$s@scrm"; done
```

Update: `codex plugin marketplace upgrade scrm`.

### Other tools

The skills follow the [Agent Skills](https://agentskills.io) standard, so the [skills CLI](https://github.com/vercel-labs/skills) works too:

```bash
npx skills add ScreamXY/skills
```

## Layout

```text
.claude-plugin/marketplace.json     # Claude Code marketplace: lists all plugins
.agents/plugins/marketplace.json    # Codex marketplace: lists all plugins
plugins/
└── scrm-<name>/                    # one plugin per skill
    ├── .claude-plugin/plugin.json  # Claude Code manifest
    ├── .codex-plugin/plugin.json   # Codex manifest
    ├── LICENSE                     # only for adapted skills: the license of the source
    └── skills/scrm-<name>/
        ├── SKILL.md                # the skill
        ├── agents/openai.yaml      # Codex settings (display name, auto start)
        ├── references/             # optional: extra docs the skill loads when needed
        └── scripts/                # optional: helper scripts
upstream.json                       # source commit of each adapted skill
scripts/validate.mjs                # checks the repo rules
scripts/check-upstream.mjs          # checks if a source changed
```

## Sources and updates

`upstream.json` records, for each skill, the source path and the last source commit I copied from.

```bash
npm run upstream
```

This lists every source that changed and prints a compare link. Copy the changes you want, then put the new commit in `upstream.json` and bump the plugin version.

What I changed compared to the sources:

- All skills: the `scrm-` prefix, the simple-English rule, and a Codex manifest.
- `scrm-show-me`: fewer diff examples. HTML pages go to the OS temp directory.
- `scrm-grill-me`, `scrm-grill-with-docs`: the sources only call other skills (`grilling`, `domain-modeling`). My versions contain that text, so they work alone.
- `scrm-wait-what`: a fallback when the repo has no `CONTEXT.md`.
- `scrm-handoff`: tells you the path of the document.
- `scrm-unslop`: plain bullets instead of numbered rules. It knows which text to edit.
- `scrm-eli5`: writes an HTML file instead of a claude.ai artifact.
- `scrm-babysit-pr`: new skill and new watcher script. Works with GitHub and Azure DevOps.

## Work on the skills

See [AGENTS.md](AGENTS.md) for the rules and how to add a skill. Before you commit:

```bash
npm install
npm run check
```

## License

My own work is under the [MIT license](LICENSE). Adapted skills keep the license of their source, in `plugins/<name>/LICENSE`: MIT for the HumanLayer, Matt Pocock, and Cursor skills, and Apache 2.0 for `scrm-eli5`.
