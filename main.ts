// news-image-20261119 — entry program (Node 22, standard library only).
//
// The entry is one image, entry.png, sitting beside this file. The whole
// job of this program is to put an exact copy of that image at
// /output/entry.png, which is what the grader reads. A plain byte copy is
// deterministic by construction: run it twice and the two outputs are the
// same file, byte for byte.
//
// For a local check, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(scriptDir, 'entry.png');
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const outputImage = join(outputDir, 'entry.png');

if (!existsSync(sourceImage)) {
  throw new Error(`entry.png is missing next to main.ts: ${sourceImage}`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourceImage, outputImage);

// A copy is only worth anything if it is exact, so read both files back
// and compare them byte for byte before the program exits. The check also
// guards against a truncated write: a copy that stopped halfway would
// differ in length and fail here instead of silently passing.
const sourceBytes = readFileSync(sourceImage);
const outputBytes = readFileSync(outputImage);
if (outputBytes.length !== sourceBytes.length) {
  throw new Error(
    `entry.png copy is incomplete: wrote ${outputBytes.length} bytes, expected ${sourceBytes.length}`,
  );
}
if (!sourceBytes.equals(outputBytes)) {
  throw new Error('entry.png copy differs from the source byte for byte');
}
