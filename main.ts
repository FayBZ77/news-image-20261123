// news-image-20261123: the picture of Monday 23 November 2026 is finished — entry.png, drawn by
// make_image.py — and this program's whole job is to put it where the judge looks: /output/entry.png,
// byte for byte as drawn, nothing re-encoded. Outside the grader's container MAKEFUN_OUTPUT_DIR
// stands in for /output.
import { readFileSync, writeFileSync } from 'node:fs';

const png = readFileSync(new URL('entry.png', import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
writeFileSync(`${outDir}/entry.png`, png);
