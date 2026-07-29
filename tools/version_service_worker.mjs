import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const toolsDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.dirname(toolsDir);
const buildDir = path.join(repoRoot, 'frontend', 'build');
const workerPath = path.join(buildDir, 'service-worker.js');
const manifestPath = path.join(buildDir, 'asset-manifest.json');
const indexPath = path.join(buildDir, 'index.html');
const token = '__DHARMASEARCH_BUILD_VERSION__';

const [worker, manifest, index] = await Promise.all([
  readFile(workerPath, 'utf8'),
  readFile(manifestPath),
  readFile(indexPath),
]);

if (!worker.includes(token)) {
  throw new Error(`Service worker version token missing from ${workerPath}`);
}

const revision = process.env.DHARMASEARCH_BUILD_REV || '';
const version = createHash('sha256')
  .update(worker.replaceAll(token, ''))
  .update(manifest)
  .update(index)
  .update(revision)
  .digest('hex')
  .slice(0, 16);

await writeFile(workerPath, worker.replaceAll(token, version));
console.log(`Versioned service worker: ${version}`);
