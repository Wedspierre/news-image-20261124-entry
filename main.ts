import { copyFileSync, existsSync, readFileSync, unlinkSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const SRC = new URL("./entry.png", import.meta.url).pathname;
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const OUT = join(OUT_DIR, "entry.png");
const MAX_BYTES = 1048576;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(message) {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

if (!existsSync(SRC)) fail(`entry.png not found at ${SRC}`);
const data = readFileSync(SRC);
if (data.length === 0) fail("entry.png is empty");
if (data.length > MAX_BYTES) fail(`entry.png is ${data.length} bytes, over the 1 MiB limit`);
if (!data.subarray(0, 8).equals(PNG_MAGIC)) fail("entry.png is not a PNG (bad magic bytes)");

// IHDR: width and height are big-endian uint32 at offsets 16 and 20.
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width === 0 || height === 0 || width > 1024 || height > 1024) {
  fail(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

// The grader's sealed stage is read-only, so copyFileSync would preserve a
// read-only mode on an existing target; unlink first, then write fresh.
if (existsSync(OUT)) unlinkSync(OUT);
writeFileSync(OUT, data);

const written = readFileSync(OUT);
if (!written.equals(data)) fail("output bytes differ from entry.png after copy");
console.log(`main.ts: wrote ${OUT} (${data.length} bytes, ${width}x${height} PNG)`);
