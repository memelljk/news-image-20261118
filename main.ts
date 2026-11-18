// The World in One Day — Wednesday 18 November 2026.
//
// Copies the front-page image this repository holds to the output
// directory as entry.png, and checks it stays within the competition's
// size limit (at most 1 MiB). Node 22, standard library only.
//
// Run outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
const dest = join(outDir, 'entry.png');

copyFileSync(src, dest);

// Validate the file we just wrote: it must be a whole PNG within the
// competition's limits (at most 1 MiB, at most 1024 by 1024 pixels).
// The width and height live in the IHDR chunk: bytes 16-19 and 20-23,
// big-endian, right after the 8-byte signature and the IHDR length/type.
const bytes = readFileSync(dest);
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is not a PNG file');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

const size = statSync(dest).size;
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}
console.log(`wrote ${dest} (${width}x${height}, ${size} bytes)`);
