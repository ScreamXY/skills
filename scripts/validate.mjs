// Checks that every plugin follows the repo rules in AGENTS.md. Exits with 1 on any error.
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const root = new URL('..', import.meta.url).pathname;
const LANGUAGE_SECTION =
  "## Language\n\nEnglish is the user's second language. Use short sentences and common words. Avoid idioms and slang. Technical terms are fine.";
const errors = [];

const readJson = (path) => JSON.parse(readFileSync(join(root, path), 'utf8'));
const check = (condition, message) => {
  if (!condition) {
    errors.push(message);
  }
};

const frontmatter = (text) => {
  const match = text.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) {
    return null;
  }
  const fields = {};
  for (const line of match[1].split('\n')) {
    const field = line.match(/^([\w-]+):\s*(.*)$/);
    if (field) {
      fields[field[1]] = field[2].replace(/^(['"])(.*)\1$/, '$2');
    }
  }
  return fields;
};

const claudeMarket = readJson('.claude-plugin/marketplace.json');
const codexMarket = readJson('.agents/plugins/marketplace.json');
const upstream = readJson('upstream.json');
const readme = readFileSync(join(root, 'README.md'), 'utf8');
const plugins = readdirSync(join(root, 'plugins')).filter((name) => !name.startsWith('.'));

for (const name of plugins) {
  const base = `plugins/${name}`;
  const skillDir = `${base}/skills/${name}`;
  check(/^scrm-[a-z0-9-]+$/.test(name), `${name}: name must be "scrm-" plus kebab-case`);

  const manifests = ['.claude-plugin', '.codex-plugin'].map((dir) => `${base}/${dir}/plugin.json`);
  const missing = manifests.filter((path) => !existsSync(join(root, path)));
  check(missing.length === 0, `${name}: missing ${missing.join(', ')}`);
  if (missing.length === 0) {
    const [claude, codex] = manifests.map(readJson);
    check(claude.name === name && codex.name === name, `${name}: plugin.json names must match the folder`);
    check(claude.version === codex.version, `${name}: versions differ (${claude.version} vs ${codex.version})`);
    check(claude.description === codex.description, `${name}: plugin.json descriptions differ`);
    check(codex.skills === './skills/', `${name}: .codex-plugin/plugin.json needs "skills": "./skills/"`);
  }

  const skillPath = join(root, skillDir, 'SKILL.md');
  if (!existsSync(skillPath)) {
    errors.push(`${name}: missing ${skillDir}/SKILL.md`);
    continue;
  }
  const skill = readFileSync(skillPath, 'utf8');
  const fields = frontmatter(skill) ?? {};
  check(fields.name === name, `${name}: SKILL.md name must be "${name}"`);
  check(fields.description?.startsWith('Use when'), `${name}: SKILL.md description must start with "Use when"`);
  check((fields.description ?? '').length <= 1024, `${name}: SKILL.md description is longer than 1024 characters`);
  check(skill.includes(LANGUAGE_SECTION), `${name}: SKILL.md needs the exact Language section from AGENTS.md`);
  check(skill.match(/^## .*/m)?.[0] === '## Language', `${name}: "## Language" must be the first "##" section`);
  check(skill.split('\n').length < 500, `${name}: SKILL.md has 500 lines or more`);
  for (const [, link] of skill.matchAll(/\]\(((?!https?:)[^)#]+)\)/g)) {
    check(existsSync(join(dirname(skillPath), link)), `${name}: broken link ${link}`);
  }

  const openaiPath = join(root, skillDir, 'agents/openai.yaml');
  if (existsSync(openaiPath)) {
    const implicit = readFileSync(openaiPath, 'utf8').match(/allow_implicit_invocation:\s*(true|false)/)?.[1];
    const manualOnly = fields['disable-model-invocation'] === 'true';
    check(implicit === String(!manualOnly), `${name}: allow_implicit_invocation must be ${!manualOnly}`);
  } else {
    errors.push(`${name}: missing ${skillDir}/agents/openai.yaml`);
  }

  const claudeEntry = claudeMarket.plugins.find((p) => p.name === name);
  const codexEntry = codexMarket.plugins.find((p) => p.name === name);
  check(claudeEntry?.source === `./${base}`, `${name}: missing or wrong in .claude-plugin/marketplace.json`);
  check(codexEntry?.source?.path === `./${base}`, `${name}: missing or wrong in .agents/plugins/marketplace.json`);
  check(name in upstream, `${name}: missing in upstream.json (use [] for a skill without a source)`);
  check(readme.includes(`\`${name}\``), `${name}: missing in the README skills table`);
}

for (const entry of [...claudeMarket.plugins, ...codexMarket.plugins]) {
  check(plugins.includes(entry.name), `marketplace lists unknown plugin ${entry.name}`);
}
for (const name of Object.keys(upstream)) {
  check(plugins.includes(name), `upstream.json lists unknown plugin ${name}`);
}

if (errors.length) {
  console.error(errors.map((error) => `x ${error}`).join('\n'));
  process.exit(1);
}
console.log(`ok: ${plugins.length} plugins are valid`);
