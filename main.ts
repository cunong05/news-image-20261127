#!/usr/bin/env node
/**
 * news-image-20261127 — entry program (program/v1).
 *
 * Copies the pre-rendered poster `entry.png` into the make.fun output
 * directory. The poster itself was rendered offline from verified news
 * reporting on the morning of 27 November 2026 (see README.md).
 *
 * Deterministic: the output bytes are exactly the input bytes, every run.
 * No network access, no randomness, no timestamps.
 */
import { mkdirSync, readFileSync, writeFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outPath = join(outDir, "entry.png");

function fail(message) {
  console.error(`news-image-20261127: ${message}`);
  process.exit(1);
}

const png = readFileSync(sourcePath);
if (png.length > MAX_BYTES) {
  fail(`entry.png is ${png.length} bytes, over the 1 MiB limit`);
}
if (!png.subarray(0, 8).equals(PNG_SIGNATURE)) {
  fail("entry.png does not start with the PNG signature");
}

// IHDR chunk: bytes 16-19 = width, 20-23 = height (big-endian uint32).
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(`entry.png is ${width}x${height}, expected 1024x1024`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(outPath, png);

const written = statSync(outPath).size;
if (written !== png.length) {
  fail(`wrote ${written} bytes, expected ${png.length}`);
}
// Read the copy back and confirm it is byte-identical to the source,
// so a partial or corrupted write can never pass silently.
const roundTrip = readFileSync(outPath);
if (!roundTrip.equals(png)) {
  fail("output bytes differ from entry.png");
}
console.log(`news-image-20261127: wrote ${outPath} (${written} bytes)`);
