// News-image entry for 23 November 2026 (Node 22, standard library only).
// The image is the entry.png beside this file; the program copies it to
// the output directory the grader gives it, deterministically.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

// The image itself is committed in this repository as entry.png (1024x1024,
// 23 November 2026 world news, drawn locally with Pillow from verified
// headlines). Copying it, byte for byte, is the whole program: no network,
// no randomness, so two runs write identical bytes.

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

// Resolve the committed image next to this file and fail loudly if it
// is missing, so a bad bundle is caught instead of silently producing
// an empty output directory.
function sourceImagePath(): string {
  const src = new URL('./entry.png', import.meta.url);
  if (!existsSync(src)) {
    throw new Error('entry.png is missing from the repository root');
  }
  return src.pathname;
}

function copyEntry(): void {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, 'entry.png');
  copyFileSync(sourceImagePath(), dest);
  // Confirm the copy landed, so a silent write failure is caught here.
  if (!existsSync(dest)) {
    throw new Error('entry.png was not written to the output directory');
  }
}

copyEntry();
