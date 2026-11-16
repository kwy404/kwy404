// Builds the resume PDFs (en, pt, es, ja) with pdfkit. No browser involved.
// Usage: bun site/resume/build.mjs   (add --nocompress to write uncompressed PDFs for checks)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import PDFDocument from 'pdfkit';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');
const OUT = path.join(ROOT, 'docs', 'resume');
const FONTS = path.join(HERE, 'fonts');
const COMPRESS = !process.argv.includes('--nocompress');

const I18N = JSON.parse(fs.readFileSync(path.join(HERE, 'i18n.json'), 'utf8'));
const MERGED = fs.readFileSync(path.join(ROOT, 'MERGED.md'), 'utf8');
const README = fs.readFileSync(path.join(ROOT, 'README.md'), 'utf8');

const PRS = 214;
const ORGS = 59;

// ---------- colors and sizes ----------
const ACCENT = '#6d5dfc';
const INK = '#16161d';
const BODY = '#2b2b33';
const GRAY = '#6b6b76';
const RULE = '#e4e2f5';

const LINKS = {
  email: 'thekaway404@gmail.com',
  github: 'https://github.com/kwy404',
  linkedin: 'https://www.linkedin.com/in/alexandre-silva-173687256/',
  portfolio: 'https://kwy404.github.io/kwy404/',
  whatsapp: 'https://wa.me/5547999500474',
  merged: 'https://github.com/kwy404/kwy404/blob/main/MERGED.md',
};

const STACK = {
  languages: 'TypeScript, JavaScript, Python, PHP, Go, Rust, Java, C#',
  backend: 'Node.js, NestJS, Fastify, Laravel, Spring Boot, APIs, microservices',
  frontend: 'React, Vue, React Native, Flutter, Swift',
  data: 'PostgreSQL, MySQL, SQLite, Redis, Elasticsearch, Kafka, RabbitMQ',
  cloud: 'Docker, AWS',
};

const HIGHLIGHTS = [
  'twbs/bootstrap#42956',
  'excalidraw/excalidraw#12178',
  'mrdoob/three.js#34673',
  'mui/material-ui#49234',
  'tailwindlabs/tailwindcss#20512',
  'puppeteer/puppeteer#15507',
  'vuejs/core#15618',
  'python-poetry/poetry#11093',
];

// ---------- per language headings and labels ----------
const T = {
  en: {
    docTitle: 'Alexandre Kohler, Senior Full Stack Software Engineer (Resume)',
    subject: 'Resume of Alexandre Kohler, Senior Full Stack Software Engineer with more than 10 years building backend systems, APIs and microservices.',
    location: 'Brusque, SC, Brazil (UTC-3). Available for remote work.',
    summary: 'Summary', skills: 'Skills', oss: 'Open source contributions', how: 'How I work',
    projects: 'Open source projects', spoken: 'Languages',
    stack: { languages: 'Languages', backend: 'Back end', frontend: 'Front end and mobile', data: 'Data and messaging', cloud: 'Cloud and infrastructure' },
    ossLead: `${PRS} merged pull requests in ${ORGS} organizations`,
    ossTop: 'Merged pull requests by organization',
    more: (n) => `and ${n} more`,
    highlights: 'Highlights',
    fullList: 'Full list of merged pull requests',
    website: 'Website', code: 'Code',
    spokenList: ['Portuguese (native)', 'English'],
    page: (a, b) => `Page ${a} of ${b}`,
  },
  pt: {
    docTitle: 'Alexandre Kohler, Senior Full Stack Software Engineer (Currículo)',
    subject: 'Currículo de Alexandre Kohler, Senior Full Stack Software Engineer com mais de 10 anos criando sistemas backend, APIs e microsserviços.',
    location: 'Brusque, SC, Brasil (UTC-3). Disponível para trabalho remoto.',
    summary: 'Resumo', skills: 'Competências', oss: 'Contribuições open source', how: 'Como eu trabalho',
    projects: 'Projetos open source', spoken: 'Idiomas',
    stack: { languages: 'Linguagens', backend: 'Back end', frontend: 'Front end e mobile', data: 'Dados e mensageria', cloud: 'Cloud e infraestrutura' },
    ossLead: `${PRS} pull requests aceitos em ${ORGS} organizações`,
    ossTop: 'Pull requests aceitos por organização',
    more: (n) => `e mais ${n}`,
    highlights: 'Destaques',
    fullList: 'Lista completa dos pull requests aceitos',
    website: 'Site', code: 'Código',
    spokenList: ['Português (nativo)', 'Inglês'],
    page: (a, b) => `Página ${a} de ${b}`,
  },
  es: {
    docTitle: 'Alexandre Kohler, Senior Full Stack Software Engineer (Currículum)',
    subject: 'Currículum de Alexandre Kohler, Senior Full Stack Software Engineer con más de 10 años creando sistemas backend, APIs y microservicios.',
    location: 'Brusque, SC, Brasil (UTC-3). Disponible para trabajo remoto.',
    summary: 'Resumen', skills: 'Habilidades', oss: 'Contribuciones open source', how: 'Cómo trabajo',
    projects: 'Proyectos open source', spoken: 'Idiomas',
    stack: { languages: 'Lenguajes', backend: 'Back end', frontend: 'Front end y móvil', data: 'Datos y mensajería', cloud: 'Cloud e infraestructura' },
    ossLead: `${PRS} pull requests aceptados en ${ORGS} organizaciones`,
    ossTop: 'Pull requests aceptados por organización',
    more: (n) => `y ${n} más`,
    highlights: 'Destacados',
    fullList: 'Lista completa de pull requests aceptados',
    website: 'Sitio web', code: 'Código',
    spokenList: ['Portugués (nativo)', 'Inglés'],
    page: (a, b) => `Página ${a} de ${b}`,
  },
  ja: {
    docTitle: 'Alexandre Kohler, Senior Full Stack Software Engineer（レジュメ）',
    subject: 'Alexandre Kohler のレジュメ。10 年以上にわたりバックエンドシステム、API、マイクロサービスを開発してきた Senior Full Stack Software Engineer。',
    location: 'ブラジル、サンタカタリーナ州ブルスケ（UTC-3）。リモート勤務が可能です。',
    summary: '概要', skills: 'スキル', oss: 'オープンソースへの貢献', how: '仕事の進め方',
    projects: 'オープンソースプロジェクト', spoken: '言語',
    stack: { languages: 'プログラミング言語', backend: 'バックエンド', frontend: 'フロントエンドとモバイル', data: 'データとメッセージング', cloud: 'クラウドとインフラ' },
    ossLead: `${ORGS} の組織で ${PRS} 件のプルリクエストがマージ`,
    ossTop: '組織別のマージ済みプルリクエスト',
    more: (n) => `ほか ${n} 組織`,
    highlights: '主なプルリクエスト',
    fullList: 'マージ済みプルリクエストの全リスト',
    website: 'Web サイト', code: 'コード',
    spokenList: ['ポルトガル語（ネイティブ）', '英語'],
    page: (a, b) => `${a} / ${b} ページ`,
  },
};

// ---------- helpers ----------
const clean = (s) =>
  String(s)
    .replaceAll('{prs}', String(PRS))
    .replaceAll('{orgs}', String(ORGS))
    .replace(/<\/?code>/g, '')
    .replace(/\s*[—–]\s*/g, ', ')
    .replace(/&nbsp;/g, ' ')
    .trim();

// Split "<b>x</b> y" into [{text, bold}]
function richParts(html) {
  const parts = [];
  const re = /<b>(.*?)<\/b>/gs;
  let last = 0, m;
  const s = clean(html);
  while ((m = re.exec(s))) {
    if (m.index > last) parts.push({ text: s.slice(last, m.index), bold: false });
    parts.push({ text: m[1], bold: true });
    last = re.lastIndex;
  }
  if (last < s.length) parts.push({ text: s.slice(last), bold: false });
  return parts.map((p) => ({ ...p, text: p.text.replace(/<[^>]+>/g, '') }));
}

// First sentence, then trimmed at a clause boundary if still long.
function shorten(desc, lang) {
  const s = clean(desc);
  const cjk = lang === 'ja';
  let first = cjk ? s.split('。')[0] + '。' : (s.match(/^.*?[.!?](?=\s|$)/s) || [s])[0];
  const max = cjk ? 110 : 165;
  if (first.length > max) {
    // Prefer a clean clause boundary: a comma that starts a new item ("a ...", "uma ...") or a colon.
    const sep = cjk ? /[、：:]/g : /(,(?=\s(?:a|an|the|um|uma|o|un|una|el|la|los|las)\s))|[:;]/g;
    let cut = -1, m;
    while ((m = sep.exec(first)) && m.index <= max) cut = m.index;
    if (cut > (cjk ? 20 : 30)) first = first.slice(0, cut) + (cjk ? '。' : '.');
  }
  return first;
}

// ---------- parse MERGED.md ----------
function parseMerged() {
  const orgs = [];
  for (const m of MERGED.matchAll(/^###\s.*?<\/a>\s*(.+?)\s*<sub>(\d+)<\/sub>/gm)) {
    orgs.push({ name: m[1].trim(), count: Number(m[2]) });
  }
  const sorted = orgs
    .map((o, i) => ({ ...o, i }))
    .sort((a, b) => b.count - a.count || a.i - b.i);
  const prs = {};
  for (const key of HIGHLIGHTS) {
    const [repo, num] = key.split('#');
    const url = `https://github.com/${repo}/pull/${num}`;
    const re = new RegExp('\\[((?:\\\\.|[^\\]])+)\\]\\(' + url.replace(/[.*+?^${}()|[\]\\/]/g, '\\$&') + '\\)');
    const m = MERGED.match(re);
    if (!m) throw new Error('PR not found in MERGED.md: ' + key);
    prs[key] = { url, title: m[1].replace(/\\(.)/g, '$1').replace(/`/g, '') };
  }
  return { orgs: sorted, prs };
}

// ---------- parse README.md project links ----------
function parseReadme() {
  const out = {};
  for (const m of README.matchAll(/<a href="(https:\/\/github\.com\/kwy404\/[^"]+)"><b>([^<]+)<\/b><\/a>(.*?)<\/td><\/tr>/g)) {
    const web = (m[3].match(/<a href="([^"]+)">Website<\/a>/) || [])[1] || null;
    out[m[2]] = { repo: m[1], website: web };
  }
  return out;
}

const MERGED_DATA = parseMerged();
const README_DATA = parseReadme();

// ---------- rendering ----------
function build(lang) {
  const L = I18N[lang];
  const t = T[lang];
  const ja = lang === 'ja';

  const doc = new PDFDocument({
    size: 'A4',
    margins: { top: 46, bottom: 50, left: 52, right: 52 },
    compress: COMPRESS,
    bufferPages: true,
    lang: L.html_lang || lang,
    displayTitle: true,
    info: {
      Title: t.docTitle,
      Author: 'Alexandre Kohler',
      Subject: t.subject,
      Keywords: 'Alexandre Kohler, kwy404, Senior Full Stack Software Engineer, Backend, APIs, Microservices, TypeScript, Node.js, NestJS, Python, Go, Rust, PHP, Laravel, Java, Spring Boot, React, Vue, PostgreSQL, Redis, Kafka, Docker, AWS, Open source',
      Creator: 'kwy404 resume builder',
    },
  });

  if (ja) {
    doc.registerFont('R', path.join(FONTS, 'NotoSansJP-Regular.ttf'));
    doc.registerFont('S', path.join(FONTS, 'NotoSansJP-Bold.ttf'));
    doc.registerFont('B', path.join(FONTS, 'NotoSansJP-Bold.ttf'));
  } else {
    doc.registerFont('R', path.join(FONTS, 'Inter-Regular.ttf'));
    doc.registerFont('S', path.join(FONTS, 'Inter-SemiBold.ttf'));
    doc.registerFont('B', path.join(FONTS, 'Inter-ExtraBold.ttf'));
  }

  const X = doc.page.margins.left;
  const W = doc.page.width - doc.page.margins.left - doc.page.margins.right;
  const bottom = () => doc.page.height - doc.page.margins.bottom;
  const GAP = ja ? 2.4 : 1.8; // line gap
  const SIZE = ja ? 8.6 : 9;

  const ensure = (h) => {
    if (doc.y + h > bottom()) {
      doc.addPage();
      doc.y = doc.page.margins.top;
    }
  };

  const heading = (label, minAfter = 46) => {
    doc.font('S').fontSize(ja ? 10 : 9.6);
    const text = ja ? label : label.toUpperCase();
    const opts = { characterSpacing: ja ? 0.4 : 1.1, lineBreak: false };
    const h = doc.heightOfString(text, opts);
    ensure(14 + h + 8 + minAfter);
    if (process.env.DEBUG) console.log(lang, label, 'page', doc.bufferedPageRange().count, 'y', Math.round(doc.y));
    doc.y += 14;
    const y = doc.y;
    doc.fillColor(ACCENT).text(text, X, y, opts);
    const tw = doc.widthOfString(text, opts);
    const ly = y + h / 2 + 0.5;
    doc.save().moveTo(X + tw + 10, ly).lineTo(X + W, ly).lineWidth(0.7).strokeColor(RULE).stroke().restore();
    doc.x = X;
    doc.y = y + h + 6;
  };

  // ----- header -----
  doc.font('B').fontSize(25).fillColor(INK).text('Alexandre Kohler', X, doc.page.margins.top, { lineBreak: false });
  let y = doc.y + (ja ? 33 : 31);
  doc.save().rect(X, y, 42, 2.6).fill(ACCENT).restore();
  y += 10;
  doc.font('S').fontSize(12).fillColor(INK).text('Senior Full Stack Software Engineer', X, y, { lineBreak: false });
  y = doc.y + 18;
  doc.font('R').fontSize(8.8).fillColor(GRAY).text(t.location, X, y, { width: W });
  y = doc.y + 3;

  const contacts = [
    { text: LINKS.email, link: 'mailto:' + LINKS.email },
    { text: 'WhatsApp +55 47 99950-0474', link: LINKS.whatsapp },
    { text: 'linkedin.com/in/alexandre-silva-173687256', link: LINKS.linkedin },
    { text: 'github.com/kwy404', link: LINKS.github },
    { text: 'kwy404.github.io/kwy404', link: LINKS.portfolio + (lang === 'en' ? '' : lang + '/') },
  ];
  // Manual flow so an item never breaks in the middle; each item gets its own link box.
  doc.font('R').fontSize(8.8);
  {
    const sep = '|';
    const sepW = doc.widthOfString(sep) + 16;
    const lh = doc.currentLineHeight() + 4;
    let cx = X, cy = y;
    contacts.forEach((c, i) => {
      const w = doc.widthOfString(c.text);
      if (i && cx + sepW + w > X + W) { cx = X; cy += lh; }
      else if (i) { doc.fillColor('#c4c1e0').text(sep, cx + 8, cy, { lineBreak: false }); cx += sepW; }
      doc.fillColor(ACCENT).text(c.text, cx, cy, { lineBreak: false });
      doc.link(cx, cy, w, doc.currentLineHeight(), c.link);
      cx += w;
    });
    doc.x = X;
    doc.y = cy + lh - 2;
  }

  // ----- summary -----
  heading(t.summary);
  const parts = richParts(L.lead);
  doc.x = X;
  parts.forEach((p, i) => {
    doc.font(p.bold ? 'S' : 'R').fontSize(SIZE + 0.4).fillColor(p.bold ? INK : BODY)
      .text(p.text, { width: W, lineGap: GAP + 0.4, continued: i < parts.length - 1 });
  });

  // ----- skills -----
  heading(t.skills);
  const labelW = ja ? 128 : 150;
  for (const k of ['languages', 'backend', 'frontend', 'data', 'cloud']) {
    doc.font('R').fontSize(SIZE);
    const h = doc.heightOfString(STACK[k], { width: W - labelW, lineGap: GAP });
    ensure(h + 3);
    const ry = doc.y;
    doc.font('S').fontSize(SIZE).fillColor(INK).text(t.stack[k], X, ry, { width: labelW - 8, lineGap: GAP });
    doc.font('R').fontSize(SIZE).fillColor(BODY).text(STACK[k], X + labelW, ry, { width: W - labelW, lineGap: GAP });
    doc.y = ry + h + 3;
  }

  // ----- open source contributions -----
  heading(t.oss, 70);
  doc.x = X;
  doc.font('S').fontSize(SIZE + 1.2).fillColor(INK).text(t.ossLead + (ja ? '。' : '.'), X, doc.y, { width: W, continued: true });
  doc.font('R').fontSize(SIZE).fillColor(ACCENT).text('  ' + t.fullList, { link: LINKS.merged, continued: false });
  doc.y += 4;

  const TOP = 14;
  const top = MERGED_DATA.orgs.slice(0, TOP);
  const rest = MERGED_DATA.orgs.length - TOP;
  const orgLine = top.map((o) => `${o.name} ${o.count}`).join(ja ? '、' : ', ') + (ja ? `、${t.more(rest)}` : `, ${t.more(rest)}`);
  doc.font('S').fontSize(SIZE).fillColor(INK).text(t.ossTop + (ja ? '：' : ': '), X, doc.y, { width: W, lineGap: GAP, continued: true });
  doc.font('R').fillColor(BODY).text(orgLine + (ja ? '。' : '.'), { lineGap: GAP });
  doc.y += 6;

  doc.font('S').fontSize(SIZE).fillColor(INK).text(t.highlights, X, doc.y, { lineGap: GAP });
  doc.y += 2;
  const hlCol = (W - 20) / 2;
  for (let i = 0; i < HIGHLIGHTS.length; i += 2) {
    const row = [HIGHLIGHTS[i], HIGHLIGHTS[i + 1]].filter(Boolean);
    const hs = row.map((key) => {
      doc.font('R').fontSize(SIZE - 0.4);
      return doc.heightOfString(key + '  ' + MERGED_DATA.prs[key].title, { width: hlCol - 8, lineGap: GAP - 0.4 });
    });
    const rh = Math.max(...hs);
    ensure(rh + 4);
    const ry = doc.y;
    row.forEach((key, j) => {
      const pr = MERGED_DATA.prs[key];
      const cx = X + j * (hlCol + 20);
      doc.save().circle(cx + 2, ry + 5.2, 1.4).fill(ACCENT).restore();
      doc.font('S').fontSize(SIZE - 0.4).fillColor(ACCENT)
        .text(key, cx + 8, ry, { width: hlCol - 8, lineGap: GAP - 0.4, link: pr.url, continued: true });
      doc.font('R').fillColor(BODY).text('  ' + pr.title, { link: pr.url, lineGap: GAP - 0.4 });
    });
    doc.y = ry + rh + 4;
  }

  // ----- how I work -----
  heading(t.how);
  const howCol = (W - 2 * 18) / 3;
  {
    const items = L.how.map((h) => ({ t: clean(h.t), d: clean(h.d) }));
    const hs = items.map((it) => {
      doc.font('S').fontSize(SIZE);
      const a = doc.heightOfString(it.t, { width: howCol, lineGap: GAP });
      doc.font('R').fontSize(SIZE - 0.4);
      return a + 2 + doc.heightOfString(it.d, { width: howCol, lineGap: GAP - 0.2 });
    });
    ensure(Math.max(...hs));
    const ry = doc.y;
    items.forEach((it, j) => {
      const cx = X + j * (howCol + 18);
      doc.font('S').fontSize(SIZE).fillColor(INK).text(it.t, cx, ry, { width: howCol, lineGap: GAP });
      doc.y += 2;
      doc.font('R').fontSize(SIZE - 0.4).fillColor(GRAY).text(it.d, cx, doc.y, { width: howCol, lineGap: GAP - 0.2 });
    });
    doc.y = ry + Math.max(...hs);
  }

  // ----- projects (two columns, row based so page breaks stay clean) -----
  heading(t.projects, 60);
  const names = Object.keys(L.projects);
  const colGap = 22;
  const colW = (W - colGap) / 2;
  const measure = (name) => {
    const p = L.projects[name];
    doc.font('S').fontSize(SIZE);
    let h = doc.heightOfString(`${name}  ${clean(p.tag)}`, { width: colW, lineGap: GAP - 0.4 });
    doc.font('R').fontSize(SIZE - 0.6);
    h += 1 + doc.heightOfString(shorten(p.desc, lang), { width: colW, lineGap: GAP - 0.4 });
    h += 1 + doc.heightOfString(t.website, { width: colW });
    return h;
  };
  const drawProject = (name, cx, ry) => {
    const p = L.projects[name];
    const links = README_DATA[name] || {};
    doc.font('S').fontSize(SIZE).fillColor(INK)
      .text(name, cx, ry, { width: colW, lineGap: GAP - 0.4, link: links.repo || null, continued: true });
    doc.font('R').fillColor(GRAY).text('  ' + clean(p.tag), { link: null, lineGap: GAP - 0.4 });
    doc.y += 1;
    doc.font('R').fontSize(SIZE - 0.6).fillColor(BODY).text(shorten(p.desc, lang), cx, doc.y, { width: colW, lineGap: GAP - 0.4 });
    doc.y += 1;
    const ly = doc.y;
    doc.font('R').fontSize(SIZE - 1.2);
    let lx = cx;
    const items = [];
    if (links.website) items.push({ text: t.website, url: links.website });
    if (links.repo) items.push({ text: links.repo.replace('https://', ''), url: links.repo });
    items.forEach((it, k) => {
      if (k) { doc.fillColor('#b9b6d6').text('|', lx, ly, { lineBreak: false }); lx += doc.widthOfString('|') + 6; }
      const iw = doc.widthOfString(it.text);
      doc.fillColor(ACCENT).text(it.text, lx, ly, { lineBreak: false });
      doc.link(lx, ly, iw, doc.currentLineHeight(), it.url);
      lx += iw + 6;
    });
  };
  for (let i = 0; i < names.length; i += 2) {
    const row = names.slice(i, i + 2);
    const rh = Math.max(...row.map(measure));
    ensure(rh + 5);
    const ry = doc.y;
    row.forEach((n, j) => drawProject(n, X + j * (colW + colGap), ry));
    doc.x = X;
    doc.y = ry + rh + 5;
  }

  // ----- languages spoken -----
  if (process.env.DEBUG) console.log(lang, 'end projects y', Math.round(doc.y), 'bottom', bottom());
  heading(t.spoken, 10);
  doc.font('R').fontSize(SIZE).fillColor(BODY).text(t.spokenList.join(ja ? '、' : ', '), X, doc.y, { width: W });

  // ----- footer on each page -----
  const range = doc.bufferedPageRange();
  for (let i = 0; i < range.count; i++) {
    doc.switchToPage(range.start + i);
    const mb = doc.page.margins.bottom;
    doc.page.margins.bottom = 0;
    const fy = doc.page.height - 32;
    doc.font('R').fontSize(7.4).fillColor(GRAY);
    doc.text('Alexandre Kohler, Senior Full Stack Software Engineer', X, fy, { lineBreak: false });
    const pt = t.page(i + 1, range.count);
    doc.text(pt, X + W - doc.widthOfString(pt), fy, { lineBreak: false });
    doc.page.margins.bottom = mb;
  }

  fs.mkdirSync(OUT, { recursive: true });
  const file = path.join(OUT, `Alexandre-Kohler-Resume-${lang}.pdf`);
  return new Promise((resolve, reject) => {
    const ws = fs.createWriteStream(file);
    ws.on('finish', () => resolve({ file, pages: range.count }));
    ws.on('error', reject);
    doc.pipe(ws);
    doc.end();
  });
}

for (const lang of ['en', 'pt', 'es', 'ja']) {
  const r = await build(lang);
  console.log(`${path.relative(ROOT, r.file)}  pages=${r.pages}  size=${fs.statSync(r.file).size}`);
}
