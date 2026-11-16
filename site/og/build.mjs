import { Resvg } from '@resvg/resvg-js';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { execSync } from 'child_process';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
const here = dirname(fileURLToPath(import.meta.url));
const out = join(here, '..', '..', 'docs', 'assets');
mkdirSync(out, { recursive: true });
execSync(`python3 ${join(here, 'gen_svg.py')}`, { stdio: 'inherit' });
const font = { fontFiles: [join(here, 'fonts/Inter-400.ttf'), join(here, 'fonts/Inter-800.ttf')], loadSystemFonts: false, defaultFontFamily: 'Inter' };
const render = (svg, w) => new Resvg(svg, { font, fitTo: { mode: 'width', value: w } }).render().asPng();
writeFileSync(join(out, 'og.png'), render(readFileSync(join(here, 'og.svg'), 'utf8'), 1200));
const eye = '<path d="M14 50 Q50 14 86 50 Q50 86 14 50Z" fill="#f5f5f7"/><circle cx="50" cy="50" r="20" fill="#ffd60a"/><circle cx="50" cy="50" r="9" fill="#050507"/><circle cx="44" cy="44" r="3.5" fill="#fff"/>';
const fav = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="#050507"/>${eye}</svg>`;
writeFileSync(join(out, 'favicon.svg'), fav);
// padded variant for app icons: eye scaled to ~76% inside full square
const padded = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="#050507"/><g transform="translate(50 50) scale(.8) translate(-50 -50)">${eye}</g></svg>`;
for (const [n, w, s] of [['icon-192.png', 192, padded], ['icon-512.png', 512, padded], ['apple-touch-icon.png', 180, padded], ['favicon-32.png', 32, fav]])
  writeFileSync(join(out, n), render(s, w));
console.log('ok');
