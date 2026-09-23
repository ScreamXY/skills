# AGENTS.md

Personal skill repo for Claude Code and Codex. One plugin per skill. The layout is in [README.md](README.md#layout).

English is the owner's second language. Keep docs, skills, and messages in simple English.

## Rules for every skill

- **Name.** `scrm-<name>` in kebab-case. The same name must be used for the plugin folder, the skill folder, `name` in both `plugin.json` files, `name` in `SKILL.md`, and both marketplace entries.
- **Language section.** Every `SKILL.md` has this section near the top. Copy it exactly. Add one skill-specific sentence if needed:

  ```markdown
  ## Language

  English is the user's second language. Use short sentences and common words. Avoid idioms and slang. Technical terms are fine.
  ```

- **Short and simple.** Keep `SKILL.md` small and plain. Use imperative sentences. Move long reference material to `references/`.
- **Works in both tools.** No tool-only features without a fallback. If a step uses a Claude Code tool (for example background runs), also say what to do in Codex.
- **Description.** Starts with `Use when`, names real trigger phrases, max 1024 characters.
- **Manual start.** `disable-model-invocation: true` in `SKILL.md` and `allow_implicit_invocation: false` in `agents/openai.yaml` belong together. Keep both in sync.
- **Version.** When you change a plugin, bump `version` in both `plugin.json` files (semver). The versions must match.
- **Sources.** For a skill based on someone else's skill: add the source to `upstream.json` and to the README table, and copy the source's `LICENSE` into the plugin folder. Never copy text from a source whose license does not allow it.

## Add a skill

1. Create `plugins/scrm-<name>/skills/scrm-<name>/SKILL.md` and `agents/openai.yaml` (copy an existing skill as a template).
2. Create `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` in `plugins/scrm-<name>/`. The Codex one also needs `"skills": "./skills/"` and an `interface` block.
3. Add the plugin to `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`.
4. Add it to `upstream.json` (`[]` if it has no source) and to the README skills table.
5. Run the checks below.

## Checks

```bash
npm run check                            # repo rules + formatting
claude plugin validate . --strict        # Claude Code marketplace
claude plugin validate plugins/<name>    # one plugin
npm run upstream                         # which sources changed
```

For bigger changes, also ask for a review with the `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` agents.
