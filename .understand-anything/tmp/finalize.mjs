import { readFileSync, writeFileSync, readdirSync, unlinkSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { createHash } from 'crypto';

const root = 'D:/Sistema Escolta';
const uaDir = join(root, '.understand-anything');

// Generate fingerprint
const graph = readFileSync(join(uaDir, 'knowledge-graph.json'));
const hash = createHash('sha256').update(graph).digest('hex').slice(0, 16);

const metadata = {
  schemaVersion: 1,
  generatedAt: new Date().toISOString(),
  graphHash: hash,
  totalNodes: 359,
  totalEdges: 605,
  layers: 8,
  tourSteps: 14,
  filesAnalyzed: 150,
  language: 'pt'
};

writeFileSync(join(uaDir, 'metadata.json'), JSON.stringify(metadata, null, 2));
console.log('Metadata written:', JSON.stringify(metadata, null, 2));

// Clean up intermediate files
const intermediateDir = join(uaDir, 'intermediate');
const tmpDir = join(uaDir, 'tmp');

try {
  for (const f of readdirSync(intermediateDir)) {
    unlinkSync(join(intermediateDir, f));
  }
  console.log('Cleaned intermediate/');
} catch (e) { console.log('No intermediate to clean'); }

// Clean tmp but keep this script
try {
  for (const f of readdirSync(tmpDir)) {
    if (f === 'finalize.mjs' || f === 'fix-tour-dangling.mjs') continue; // skip self
    unlinkSync(join(tmpDir, f));
  }
  console.log('Cleaned tmp/');
} catch (e) { console.log('No tmp to clean'); }
