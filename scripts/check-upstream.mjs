// Checks if the upstream sources in upstream.json changed since we copied them.
// Uses the public GitHub API. Set GITHUB_TOKEN to avoid the rate limit (60 requests per hour).
import { readFileSync } from 'node:fs';

const upstream = JSON.parse(readFileSync(new URL('../upstream.json', import.meta.url), 'utf8'));
const headers = process.env.GITHUB_TOKEN ? { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` } : {};

const latestCommit = async ({ repo, path }) => {
  const url = `https://api.github.com/repos/${repo}/commits?path=${encodeURIComponent(path)}&per_page=1`;
  const response = await fetch(url, { headers });
  if (!response.ok) {
    throw new Error(`${repo}/${path}: GitHub API returned ${response.status}`);
  }
  const [latest] = await response.json();
  if (!latest) {
    throw new Error(`${repo}/${path}: path not found (moved or deleted upstream?)`);
  }
  return latest.sha;
};

const sources = Object.entries(upstream).flatMap(([plugin, list]) => list.map((source) => ({ plugin, ...source })));
const results = await Promise.all(
  sources.map(async (source) => ({
    ...source,
    latest: await latestCommit(source).catch((error) => error),
  })),
);

let changed = 0;
for (const { plugin, repo, path, commit, latest } of results) {
  if (latest instanceof Error) {
    changed++;
    console.log(`ERROR    ${plugin}: ${latest.message}`);
  } else if (latest === commit) {
    console.log(`ok       ${plugin}: ${repo}/${path}`);
  } else {
    changed++;
    console.log(`CHANGED  ${plugin}: ${repo}/${path}`);
    console.log(`         https://github.com/${repo}/compare/${commit}...${latest}`);
    console.log(`         new commit: ${latest}`);
  }
}
console.log(changed ? `\n${changed} source(s) need a look.` : '\nAll sources are up to date.');
process.exit(changed ? 1 : 0);
