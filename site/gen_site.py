#!/usr/bin/env python3
"""Static site generator for the kwy404 portfolio (GitHub Pages, served from /docs).

Reads README.md and MERGED.md for data, site/i18n.py for translations and site/art.py for the art.
Run site/build.sh, which builds the JS with Bun first and then calls this script.
"""
import glob
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, 'docs')
sys.path.insert(0, HERE)
from i18n import I18N  # noqa: E402
import art  # noqa: E402

SITE = 'https://kwy404.github.io'
BASE = '/kwy404/'
ABS = SITE + BASE
LANGS = ['en', 'pt', 'es', 'ja']
HREFLANG = {'en': 'en', 'pt': 'pt-BR', 'es': 'es', 'ja': 'ja'}
HOME = {'en': '', 'pt': 'pt/', 'es': 'es/', 'ja': 'ja/'}
CONTRIB = {'en': 'contributions/', 'pt': 'pt/contribuicoes/', 'es': 'es/contribuciones/', 'ja': 'ja/contributions/'}
TODAY = date.today().isoformat()
GH = 'https://github.com/kwy404'
LINKEDIN = 'https://www.linkedin.com/in/alexandre-silva-173687256/'
WA = 'https://wa.me/5547999500474'
PHONE = '+55 47 99950-0474'
EMAIL = 'thekaway404@gmail.com'
ZUPTE = 'https://zupte.com'
VOODOO_CDN = 'https://cdn.jsdelivr.net/npm/voodoojs@1.1.0/dist/voodoo.core.min.js'
MONSOON_CDN = 'https://cdn.jsdelivr.net/npm/monsooncss@0.2.0/dist/monsoon.min.css'
OG_IMG = ABS + 'assets/og.png'
BANNER = '/*! kwy404 portfolio · built with Voodoo.js + Monsoon + glyphfox · github.com/kwy404 */'
BUILT = [
    ('Voodoo.js', 'https://kwy404.github.io/Voodoo.js/', 'https://cdn.jsdelivr.net/gh/kwy404/Voodoo.js@main/brand/mascot/vudu-wave.svg'),
    ('Monsoon', 'https://kwy404.github.io/monsoon/', 'https://cdn.jsdelivr.net/gh/kwy404/monsoon@main/assets/mascot.svg'),
    ('glyphfox', 'https://kwy404.github.io/glyphfox/', 'https://raw.githubusercontent.com/kwy404/glyphfox/8cb57ae/docs/assets/favicon.svg'),
]

# Strings that i18n.py does not have yet (founder section, org pages, small labels).
EXTRA = {
    'en': {
        'skip': 'Skip to content', 'menu': 'Menu', 'terminal': 'Open the terminal', 'close': 'Close',
        'resume': 'Download resume (PDF)', 'resume_short': 'Resume', 'email': 'Email', 'whatsapp': 'WhatsApp', 'linkedin': 'LinkedIn', 'github': 'GitHub',
        'art': 'Surreal illustration: floating eyes and a glowing grid of merged code',
        'nav_founder': 'Zupte',
        'f_eyebrow': 'Founder', 'f_title': 'I founded and run Zupte.',
        'f_text': 'Zupte is my event ticketing platform in Brazil, for shows, parties, theater and stand-up comedy. Buyers pay with PIX or card and get their ticket by email and WhatsApp. I own the company and build the product end to end.',
        'f_points': ['Shows, parties, theater and stand-up', 'PIX or card payments', 'Tickets by email and WhatsApp'],
        'f_cta': 'Visit zupte.com',
        'org_title': "Alexandre Kohler's merged pull requests to {org}",
        'org_desc': '{n} merged pull requests by Alexandre Kohler (kwy404) to {org} open source projects: {repos}.',
        'org_sub': '{n} merged pull requests in {r} repositories.',
        'org_sub1': '{n} merged pull requests in 1 repository.',
        'one_pr': '1 merged pull request in 1 repository.',
        'org_gh': 'View {org} on GitHub', 'related': 'More organizations', 'all': 'All merged pull requests', 'home': 'Home',
        'stars': 'stars', 'pr_word': 'merged pull requests', 'langs': 'Languages',
    },
    'pt': {
        'skip': 'Pular para o conteúdo', 'menu': 'Menu', 'terminal': 'Abrir o terminal', 'close': 'Fechar',
        'resume': 'Baixar currículo (PDF)', 'resume_short': 'Currículo', 'email': 'E-mail', 'whatsapp': 'WhatsApp', 'linkedin': 'LinkedIn', 'github': 'GitHub',
        'art': 'Ilustração surreal: olhos flutuando sobre uma grade brilhante de código aceito',
        'nav_founder': 'Zupte',
        'f_eyebrow': 'Fundador', 'f_title': 'Fundei e comando a Zupte.',
        'f_text': 'A Zupte é a minha plataforma de venda de ingressos para eventos no Brasil: shows, festas, teatro e stand-up. Quem compra paga com PIX ou cartão e recebe o ingresso por e-mail e WhatsApp. Sou o dono da empresa e construo o produto de ponta a ponta.',
        'f_points': ['Shows, festas, teatro e stand-up', 'Pagamento com PIX ou cartão', 'Ingresso por e-mail e WhatsApp'],
        'f_cta': 'Conhecer a zupte.com',
        'org_title': 'Pull requests de Alexandre Kohler aceitos em {org}',
        'org_desc': '{n} pull requests de Alexandre Kohler (kwy404) aceitos em projetos open source de {org}: {repos}.',
        'org_sub': '{n} pull requests aceitos em {r} repositórios.',
        'org_sub1': '{n} pull requests aceitos em 1 repositório.',
        'one_pr': '1 pull request aceito em 1 repositório.',
        'org_gh': 'Ver {org} no GitHub', 'related': 'Mais organizações', 'all': 'Todos os pull requests aceitos', 'home': 'Início',
        'stars': 'estrelas', 'pr_word': 'pull requests aceitos', 'langs': 'Idiomas',
    },
    'es': {
        'skip': 'Saltar al contenido', 'menu': 'Menú', 'terminal': 'Abrir la terminal', 'close': 'Cerrar',
        'resume': 'Descargar CV (PDF)', 'resume_short': 'CV', 'email': 'Email', 'whatsapp': 'WhatsApp', 'linkedin': 'LinkedIn', 'github': 'GitHub',
        'art': 'Ilustración surrealista: ojos flotando sobre una cuadrícula brillante de código aceptado',
        'nav_founder': 'Zupte',
        'f_eyebrow': 'Fundador', 'f_title': 'Fundé y dirijo Zupte.',
        'f_text': 'Zupte es mi plataforma de venta de entradas para eventos en Brasil: shows, fiestas, teatro y stand-up. Quien compra paga con PIX o tarjeta y recibe su entrada por email y WhatsApp. Soy el dueño de la empresa y construyo el producto de punta a punta.',
        'f_points': ['Shows, fiestas, teatro y stand-up', 'Pago con PIX o tarjeta', 'Entradas por email y WhatsApp'],
        'f_cta': 'Visitar zupte.com',
        'org_title': 'Pull requests de Alexandre Kohler aceptados en {org}',
        'org_desc': '{n} pull requests de Alexandre Kohler (kwy404) aceptados en proyectos open source de {org}: {repos}.',
        'org_sub': '{n} pull requests aceptados en {r} repositorios.',
        'org_sub1': '{n} pull requests aceptados en 1 repositorio.',
        'one_pr': '1 pull request aceptado en 1 repositorio.',
        'org_gh': 'Ver {org} en GitHub', 'related': 'Más organizaciones', 'all': 'Todos los pull requests aceptados', 'home': 'Inicio',
        'stars': 'estrellas', 'pr_word': 'pull requests aceptados', 'langs': 'Idiomas',
    },
    'ja': {
        'skip': '本文へスキップ', 'menu': 'メニュー', 'terminal': 'ターミナルを開く', 'close': '閉じる',
        'resume': '履歴書をダウンロード (PDF)', 'resume_short': '履歴書', 'email': 'メール', 'whatsapp': 'WhatsApp', 'linkedin': 'LinkedIn', 'github': 'GitHub',
        'art': 'シュールなイラスト: マージされたコードの光るグリッドの上に浮かぶ目',
        'nav_founder': 'Zupte',
        'f_eyebrow': '創業者', 'f_title': 'Zupte を創業し、運営しています。',
        'f_text': 'Zupte はブラジルのイベントチケット販売プラットフォームです。ライブ、パーティー、演劇、スタンダップコメディに対応し、購入者は PIX またはカードで支払い、チケットはメールと WhatsApp で届きます。会社のオーナーとして、プロダクトの開発をすべて自分で手がけています。',
        'f_points': ['ライブ、パーティー、演劇、スタンダップ', 'PIX またはカードで支払い', 'チケットはメールと WhatsApp で'],
        'f_cta': 'zupte.com を見る',
        'org_title': '{org} にマージされた Alexandre Kohler のプルリクエスト',
        'org_desc': 'Alexandre Kohler (kwy404) が {org} のオープンソースプロジェクトにマージした {n} 件のプルリクエスト: {repos}。',
        'org_sub': '{r} のリポジトリで {n} 件のプルリクエストがマージされました。',
        'org_sub1': '1 つのリポジトリで {n} 件のプルリクエストがマージされました。',
        'one_pr': '1 つのリポジトリで 1 件のプルリクエストがマージされました。',
        'org_gh': 'GitHub で {org} を見る', 'related': 'ほかの組織', 'all': 'マージされたすべてのプルリクエスト', 'home': 'ホーム',
        'stars': 'スター', 'pr_word': '件のマージ済み PR', 'langs': '言語',
    },
}

esc = lambda s: html.escape(str(s), quote=True)


def slugify(name):
    s = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return s or 'org'


def md_inline(text):
    """Markdown title cell -> safe HTML (escapes, backticks to <code>)."""
    t = re.sub(r'\\([\[\]_*|`\\])', r'\1', text)
    parts = re.split(r'`([^`]+)`', t)
    out = []
    for i, p in enumerate(parts):
        out.append('<code>%s</code>' % esc(p) if i % 2 else esc(p))
    return ''.join(out)


def md_plain(text):
    return re.sub(r'\\([\[\]_*|`\\])', r'\1', text).replace('`', '')


def split_cells(line):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [c.strip() for c in re.split(r'(?<!\\)\|', line)]


LINK = re.compile(r'^\[(.*)\]\((https?://[^)\s]+)\)$')

# ---------------------------------------------------------------- data


def load_merged():
    orgs, org, repo = [], None, None
    for line in open(os.path.join(ROOT, 'MERGED.md'), encoding='utf-8'):
        line = line.rstrip('\n')
        m = re.match(r'^### <a href="([^"]+)"><img src="([^"]+)"[^>]*></a> (.+?) <sub>(\d+)</sub>', line)
        if m:
            org = {'url': m.group(1), 'logo': m.group(2), 'name': m.group(3).strip(), 'declared': int(m.group(4)), 'repos': []}
            orgs.append(org)
            repo = None
            continue
        if not org or not line.startswith('|') or line.startswith('| Repository') or line.startswith('| ---'):
            continue
        c = split_cells(line)
        if len(c) < 2:
            continue
        if c[0]:
            rm = re.match(r'^\[([^\]]+)\]\(([^)]+)\)(?:<br><sub>(.*)</sub>)?$', c[0])
            if not rm:
                raise SystemExit('bad repo cell: ' + line)
            repo = {'full': rm.group(1), 'url': rm.group(2), 'desc': (rm.group(3) or '').strip(), 'prs': []}
            org['repos'].append(repo)
        cell, note = c[1], ''
        nm = re.match(r'^(.*?)<br><sub>(.*)</sub>$', cell)
        if nm:
            cell, note = nm.group(1).strip(), re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', nm.group(2)).strip()
        lm = LINK.match(cell)
        if not lm or repo is None:
            raise SystemExit('bad PR cell: ' + line)
        repo['prs'].append({'title_md': lm.group(1), 'url': lm.group(2), 'repo': repo['full'], 'note': note})
    seen = set()
    for o in orgs:
        o['prs'] = [p for r in o['repos'] for p in r['prs']]
        o['count'] = len(o['prs'])
        s = slugify(o['name'])
        while s in seen:
            s += '-2'
        seen.add(s)
        o['slug'] = s
        if o['count'] != o['declared']:
            print('warning: %s declares %d but lists %d' % (o['name'], o['declared'], o['count']))
    return orgs


def load_readme():
    text = open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
    # highlights
    hl = []
    sec = text.split('### Highlights', 1)[1].split('## Stack', 1)[0]
    for line in sec.splitlines():
        if not line.startswith('| [') :
            continue
        c = split_cells(line)
        rm = LINK.match(c[0])
        pm = LINK.match(c[2])
        hl.append({'repo': rm.group(1), 'repo_url': rm.group(2), 'stars': c[1], 'title_md': pm.group(1), 'url': pm.group(2)})
    # stack
    stack = []
    sec = text.split('## Stack', 1)[1].split('## Open source projects', 1)[0]
    for line in sec.splitlines():
        m = re.match(r'^- \*\*(.+?):\*\* (.+)$', line.strip())
        if m:
            stack.append({'name': m.group(1), 'items': [x.strip() for x in m.group(2).split(',') if x.strip()]})
    # projects
    projects = []
    sec = text.split('## Open source projects', 1)[1].split('</table>', 1)[0]
    for row in re.findall(r'<tr>(.*?)</tr>', sec, re.S):
        repo = re.search(r'<a href="([^"]+)"><img src="([^"]+)"[^>]*alt="([^"]*)"', row)
        name = re.search(r'<b>(.+?)</b></a> · ([^<]+)<br>', row)
        parts = row.split('<br>')
        links = []
        if len(parts) >= 3:
            for href, label in re.findall(r'<a href="([^"]+)">([^<]+)</a>', parts[-1]):
                links.append({'href': href, 'label': label.strip()})
        projects.append({'repo': repo.group(1), 'logo': repo.group(2), 'alt': repo.group(3), 'name': html.unescape(name.group(1)), 'tag': name.group(2).strip(), 'links': links})
    return hl, stack, projects


ORGS = load_merged()
ALL_PRS = [p for o in ORGS for p in o['prs']]
N_PRS, N_ORGS = len(ALL_PRS), len(ORGS)
ORGS_SORTED = sorted(ORGS, key=lambda o: (-o['count'], o['name'].lower()))
HL, STACK, PROJECTS = load_readme()
ICONS = json.load(open(os.path.join(HERE, 'glyphfox-icons.json'), encoding='utf-8'))


def icon(name, cls='gi'):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (cls, ICONS[name])


def T(lang, key, **kw):
    v = I18N[lang][key] if key in I18N[lang] else EXTRA[lang][key]
    if isinstance(v, str):
        kw.setdefault('prs', N_PRS)
        kw.setdefault('orgs', N_ORGS)
        for k, x in kw.items():
            v = v.replace('{%s}' % k, str(x))
    return v


def X(lang, key, **kw):
    v = EXTRA[lang][key]
    for k, x in kw.items():
        v = v.replace('{%s}' % k, str(x))
    return v


def org_url(lang, o):
    return BASE + CONTRIB[lang] + o['slug'] + '/'


def resume(lang):
    return BASE + 'resume/Alexandre-Kohler-Resume-%s.pdf' % lang


def img(src, alt, w, h, cls='', lazy=True, extra=''):
    c = ('sk ' + cls).strip()
    return '<img class="%s" src="%s" alt="%s" width="%d" height="%d"%s decoding="async"%s>' % (
        esc(c), esc(src), esc(alt), w, h, ' loading="lazy"' if lazy else '', extra)

# ---------------------------------------------------------------- assets


def h8(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()[:8]


def minify_css(css):
    css = re.sub(r'/\*(?!!).*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};,>])\s*', r'\1', css)
    css = css.replace(';}', '}')
    return css.strip() + '\n'


def build_css():
    src = open(os.path.join(HERE, 'assets', 'site.css'), encoding='utf-8').read()
    chunks, name = {}, None
    for part in re.split(r'/\*@chunk (\w+)\*/', src):
        if name is None:
            if part.strip():
                chunks['core'] = part
            name = ''
            continue
        if name == '':
            name = part
            continue
        chunks[name] = chunks.get(name, '') + part
        name = ''
    groups = {
        'core': ['core', 'shared', 'core2', 'core3'],
        'sections': ['sections'],
        'contrib': ['contrib'],
        'eggs': ['eggs'],
    }
    out = {}
    d = os.path.join(DOCS, 'assets', 'css')
    os.makedirs(d, exist_ok=True)
    for g, names in groups.items():
        css = '/*! kwy404 portfolio · %s */\n' % g + minify_css('\n'.join(chunks[n] for n in names))
        hh = h8(css)
        fn = '%s.%s.css' % (g, hh)
        open(os.path.join(d, fn), 'w', encoding='utf-8').write(css)
        out[g] = '%sassets/css/%s?v=%s' % (BASE, fn, hh)
    return out


def find_js():
    d = os.path.join(DOCS, 'assets', 'js')
    mains = sorted(glob.glob(os.path.join(d, 'main-*.js')))
    if not mains:
        raise SystemExit('run bun build first (site/build.sh)')
    f = mains[0]
    return '%sassets/js/%s?v=%s' % (BASE, os.path.basename(f), h8(open(f, 'rb').read()))

# ---------------------------------------------------------------- page pieces


HEAD_JS = ("(function(d){d.classList.remove('no-js');try{var n=navigator,c=n.connection||{},m=window.matchMedia;"
           "if((n.hardwareConcurrency&&n.hardwareConcurrency<=4)||(n.deviceMemory&&n.deviceMemory<=2)||c.saveData||"
           "/^(slow-2g|2g|3g)$/.test(c.effectiveType||'')||(m&&m('(prefers-reduced-motion: reduce)').matches))d.classList.add('lite')}catch(e){}"
           "setTimeout(function(){if(!window.__kwy)d.classList.add('no-js')},4000)})(document.documentElement)")


def person_ld(lang):
    knows = [i for g in STACK for i in g['items']]
    return {
        '@type': 'Person', '@id': ABS + '#person', 'name': 'Alexandre Kohler', 'alternateName': 'kwy404',
        'jobTitle': 'Senior Full Stack Software Engineer', 'email': 'mailto:' + EMAIL, 'telephone': '+55 47 99950-0474',
        'url': ABS, 'image': ABS + 'assets/avatar.jpg',
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Brusque', 'addressRegion': 'SC', 'addressCountry': 'BR'},
        'sameAs': [GH, LINKEDIN, WA], 'knowsAbout': knows, 'knowsLanguage': ['pt-BR', 'en', 'es'],
        'worksFor': {'@id': ZUPTE + '/#org'},
    }


def zupte_ld():
    return {'@type': 'Organization', '@id': ZUPTE + '/#org', 'name': 'Zupte', 'url': ZUPTE,
            'description': 'Event ticketing platform in Brazil for shows, parties, theater and stand-up comedy, with PIX or card payments and tickets by email and WhatsApp.',
            'areaServed': 'BR', 'founder': {'@id': ABS + '#person'}}


def website_ld():
    return {'@type': 'WebSite', '@id': ABS + '#website', 'url': ABS, 'name': 'Alexandre Kohler (kwy404)',
            'inLanguage': [HREFLANG[l] for l in LANGS], 'publisher': {'@id': ABS + '#person'}}


def crumbs_ld(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}


def pr_list_ld(prs, name):
    return {'@type': 'ItemList', 'name': name, 'numberOfItems': len(prs), 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'url': p['url'], 'name': '%s: %s' % (p['repo'], md_plain(p['title_md']))}
        for i, p in enumerate(prs)]}


def head(lang, title, desc, path, alts, css, js, ld, root=False, noindex=False):
    I = I18N[lang]
    canon = SITE + path
    h = ['<!doctype html>',
         '<html lang="%s" class="no-js%s" data-base="%s"%s>' % (I['html_lang'], ' ja' if lang == 'ja' else '', BASE, ' data-root="1"' if root else ''),
         '<head>', '<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
         '<title>%s</title>' % esc(title),
         '<script>%s</script>' % HEAD_JS,
         '<meta name="description" content="%s">' % esc(desc),
         '<meta name="keywords" content="%s">' % esc(T(lang, 'keywords')),
         '<meta name="author" content="Alexandre Kohler">',
         '<meta name="robots" content="%s">' % ('noindex,follow' if noindex else 'index,follow,max-image-preview:large'),
         '<link rel="canonical" href="%s">' % esc(canon)]
    if alts:
        for l in LANGS:
            h.append('<link rel="alternate" hreflang="%s" href="%s">' % (HREFLANG[l], esc(SITE + alts[l])))
        h.append('<link rel="alternate" hreflang="x-default" href="%s">' % esc(SITE + alts['en']))
    h += ['<meta property="og:type" content="%s">' % ('profile' if root or path in [BASE + HOME[l] for l in LANGS] else 'website'),
          '<meta property="og:site_name" content="Alexandre Kohler (kwy404)">',
          '<meta property="og:title" content="%s">' % esc(title),
          '<meta property="og:description" content="%s">' % esc(desc),
          '<meta property="og:url" content="%s">' % esc(canon),
          '<meta property="og:image" content="%s">' % OG_IMG,
          '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
          '<meta property="og:image:alt" content="%s">' % esc(T(lang, 'title')),
          '<meta property="og:locale" content="%s">' % I['og_locale']]
    for l in LANGS:
        if l != lang:
            h.append('<meta property="og:locale:alternate" content="%s">' % I18N[l]['og_locale'])
    h += ['<meta name="twitter:card" content="summary_large_image">',
          '<meta name="twitter:title" content="%s">' % esc(title),
          '<meta name="twitter:description" content="%s">' % esc(desc),
          '<meta name="twitter:image" content="%s">' % OG_IMG,
          '<meta name="theme-color" content="#050507">', '<meta name="color-scheme" content="dark">',
          '<link rel="icon" href="%sassets/favicon.svg" type="image/svg+xml">' % BASE,
          '<link rel="icon" href="%sassets/favicon-32.png" sizes="32x32" type="image/png">' % BASE,
          '<link rel="apple-touch-icon" href="%sassets/apple-touch-icon.png">' % BASE,
          '<link rel="manifest" href="%ssite.webmanifest">' % BASE]
    if lang != 'ja':
        h += ['<link rel="preconnect" href="https://fonts.googleapis.com">',
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap">']
    h += ['<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>',
          '<link rel="stylesheet" href="__MONSOON__">']
    for c in css:
        h.append('<link rel="stylesheet" href="%s">' % c)
    h += ['<script defer src="%s"></script>' % VOODOO_CDN,
          '<script type="module" src="%s"></script>' % js]
    h.append('<script type="application/ld+json">%s</script>' % json.dumps(
        {'@context': 'https://schema.org', '@graph': ld}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
    h.append('</head>')
    return '\n'.join(h)


def lang_menu(lang, alts):
    I = I18N[lang]
    items = []
    for l in LANGS:
        cur = ' aria-current="true"' if l == lang else ''
        items.append('<a href="%s" data-lang="%s" hreflang="%s" lang="%s"%s>%s <small>%s</small></a>' % (
            esc(alts[l]), l, HREFLANG[l], I18N[l]['html_lang'], cur, esc(I18N[l]['lang_name']), l.upper()))
    return ('<div class="lang" @click.outside="lang = false">'
            '<button class="lang-b" type="button" @click="lang = !lang" :aria-expanded="lang ? \'true\' : \'false\'" aria-expanded="false" aria-haspopup="true" aria-label="%s">%s<span>%s</span></button>'
            '<div class="lang-m" v-show="lang" v-cloak @click="lang = false">%s</div></div>') % (
        esc(I['lang_label']), icon('globe', 'gi sm'), lang.upper(), ''.join(items))


def nav(lang, alts, on_home):
    I = I18N[lang]
    n = I['nav']
    home = BASE + HOME[lang]
    pre = '' if on_home else home
    links = [('#work', n['work']), ('#founder', X(lang, 'nav_founder')), ('#projects', n['projects']), ('#stack', n['stack']), ('#contact', n['contact'])]
    a = ''.join('<a href="%s%s" @click="go()">%s</a>' % (pre, h, esc(t)) for h, t in links)
    a += '<a href="%s" @click="go()">%s</a>' % (BASE + CONTRIB[lang], esc(n['all_prs']))
    return ('<a class="skip" href="#main">%s</a>\n'
            '<header class="nav" v-data="nav()" @keydown.esc="lang = false">'
            '<div class="wrap nav-in">'
            '<a class="brand" href="%s" data-avatar aria-label="Alexandre Kohler, kwy404">%s<span>kwy404</span></a>'
            '<nav class="nav-links" :class="{ open: open }" aria-label="%s">%s</nav>'
            '<div class="nav-r">%s'
            '<button class="btn sm icon" type="button" data-term aria-label="%s" title="%s">%s</button>'
            '<button class="btn sm icon menu-b" type="button" @click="toggle()" :aria-expanded="open ? \'true\' : \'false\'" aria-expanded="false" aria-label="%s">%s</button>'
            '</div></div></header>') % (
        esc(X(lang, 'skip')), home, img(BASE + 'assets/avatar.jpg', 'Alexandre Kohler', 30, 30, lazy=False),
        esc(X(lang, 'menu')), a, lang_menu(lang, alts), esc(X(lang, 'terminal')), esc(X(lang, 'terminal')), icon('terminal', 'gi sm'),
        esc(X(lang, 'menu')), icon('menu', 'gi sm'))


def sprite():
    return '<svg class="ico-sprite" aria-hidden="true" focusable="false"><defs>%s</defs></svg>' % ''.join(
        '<symbol id="i-%s" viewBox="0 0 24 24">%s</symbol>' % (n, ICONS[n]) for n in ['x', 'terminal', 'arrow-right'])


def term_island(lang):
    return ('<div v-data="term()" v-init="bind()">'
            '<div class="term" v-show="open" v-cloak role="dialog" aria-label="Terminal" @keydown.esc="close()">'
            '<div class="term-h"><i></i><i></i><i></i><span>kwy404@portfolio: ~</span>'
            '<button type="button" @click="close()" aria-label="%s"><svg class="gi sm" aria-hidden="true"><use href="#i-x"></use></svg></button></div>'
            '<div class="term-o" id="term-out" aria-live="polite"><div v-for="l in lines" :class="l.c" v-text="l.s"></div></div>'
            '<form class="term-i" @submit.prevent="run()"><b>~ $</b><input id="term-in" type="text" enterkeyhint="send" v-model="cmd" @keydown="key($event)" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" aria-label="Command"><button type="submit" class="term-go" aria-label="Run"><svg class="gi sm" aria-hidden="true"><use href="#i-arrow-right"></use></svg></button></form>'
            '</div></div>') % esc(X(lang, 'close'))


def footer(lang, alts):
    I = I18N[lang]
    built = ''.join('<a href="%s" rel="noopener">%s%s</a>' % (u, img(l, '', 22, 22), esc(n)) for n, u, l in BUILT)
    langs = ''.join('<a href="%s" data-lang="%s" hreflang="%s" lang="%s">%s</a>' % (esc(alts[l]), l, HREFLANG[l], I18N[l]['html_lang'], esc(I18N[l]['lang_name'])) for l in LANGS)
    return ('<footer v-pre><div class="wrap">'
            '<div class="foot">'
            '<div class="built"><span>%s</span>%s</div>'
            '<nav class="foot-l" aria-label="%s">%s</nav>'
            '</div>'
            '<div class="foot mt-4"><span>&copy; %s %s</span>'
            '<span class="hint">%s</span>'
            '<span class="sig">kwy404</span></div>'
            '</div></footer>') % (
        esc(I['footer_built']), built, esc(X(lang, 'langs')), langs, date.today().year, esc(I['footer_rights']),
        esc(I['footer_hint']).replace('/', '<kbd>/</kbd>', 1), )


def i18n_json(lang):
    I = I18N[lang]
    data = {
        'console': I['console'],
        'term': I['term'],
        'eggs': {k: v.replace('{orgs}', str(N_ORGS)).replace('{prs}', str(N_PRS)) for k, v in I['eggs'].items()},
        'stats': {'prs': N_PRS, 'orgs': N_ORGS},
        'topOrgs': ['%s %d' % (o['name'], o['count']) for o in ORGS_SORTED[:12]],
        'projects': ['%s: %s' % (p['name'], I['projects'].get(p['name'], {}).get('tag', p['tag'])) for p in PROJECTS],
        'stackLines': ['%s: %s' % (sg, ', '.join(g['items'])) for sg, g in zip(I['stack_groups'].values(), STACK)],
        'contribUrl': BASE + CONTRIB[lang],
        'found': I['found'],
    }
    return '<script type="application/json" id="i18n">%s</script>' % json.dumps(data, ensure_ascii=False).replace('</', '<\\/')


def page(lang, title, desc, path, alts, css, js, ld, body, root=False, noindex=False, on_home=False, extra_scripts=''):
    out = [head(lang, title, desc, path, alts, css, js, ld, root, noindex),
           '<body>',
           '<div class="bgfx" aria-hidden="true"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>',
           sprite(),
           nav(lang, alts, on_home),
           '<main id="main">', body, '</main>',
           footer(lang, alts),
           term_island(lang),
           i18n_json(lang),
           extra_scripts,
           '</body>', '</html>', '']
    return '\n'.join(out)

# ---------------------------------------------------------------- home


HOW_ICONS = [('bug', 'shake'), ('search', 'blink'), ('git-merge', 'pulse')]
STACK_ICONS = ['code', 'server', 'layers', 'database', 'cloud']


def org_card(lang, o, top=True):
    repos = ', '.join(r['full'].split('/')[-1] for r in o['repos'][:3])
    return ('<a class="card spot org" href="%s">%s<span><b>%s</b>%s</span><span class="n">%d</span></a>') % (
        org_url(lang, o), img(o['logo'], '', 34, 34), esc(o['name']),
        '<small class="org-top">%s</small>' % esc(repos) if top else '', o['count'])


def home_body(lang):
    I = I18N[lang]
    E = EXTRA[lang]
    s = []
    # hero
    s.append('<section class="hero" id="top" v-pre><div class="wrap hero-g">'
             '<div>'
             '<span class="pill"><span class="dot"><i></i></span><b>%s</b></span>'
             '<h1>%s <span class="gt">%s</span></h1>'
             '<p class="lead">%s</p>'
             '<div class="cta">'
             '<a class="btn pri" href="#contact">%s%s</a>'
             '<a class="btn" href="%s" rel="me noopener">%s%s</a>'
             '<a class="btn" href="%s" download>%s%s</a>'
             '</div>'
             '<p class="hint mt-4"><button class="btn sm" type="button" data-term>%s</button></p>'
             '<div class="stats">'
             '<div class="stat hold" data-hold tabindex="0" role="button" title="%s" aria-label="%d %s. %s"><b data-count="%d">%d</b><span>%s</span></div>'
             '<div class="stat"><b data-count="%d">%d</b><span>%s</span></div>'
             '<div class="stat"><b data-count="10" data-suffix="+">10+</b><span>%s</span></div>'
             '<div class="stat"><b data-count="%d">%d</b><span>%s</span></div>'
             '</div></div>'
             '<div class="art">%s</div>'
             '</div></section>' % (
                 esc(I['pill']), esc(I['h1_a']), esc(I['h1_b']), T(lang, 'lead'),
                 icon('mail', 'gi sm'), esc(I['cta_contact']), GH, icon('brand-github', 'gi sm'), esc(I['cta_github']),
                 resume(lang), icon('book', 'gi sm'), esc(E['resume']),
                 esc(I['cta_terminal']).replace('/', '<kbd>/</kbd>', 1),
                 esc(I['stat_hold']), N_PRS, esc(I['stat_prs']), esc(I['stat_hold']), N_PRS, N_PRS, esc(I['stat_prs']),
                 N_ORGS, N_ORGS, esc(I['stat_orgs']), esc(I['stat_years']), len(PROJECTS), len(PROJECTS), esc(I['stat_projects']),
                 art.hero_svg().replace('__ART_TITLE__', esc(E['art']))))
    # marquee
    def lg(o, hidden):
        return '<a class="lg" href="%s"%s>%s%s <small>%d</small></a>' % (
            org_url(lang, o), ' tabindex="-1"' if hidden else '', img(o['logo'], '' if hidden else o['name'], 26, 26), esc(o['name']), o['count'])
    track = ''.join(lg(o, False) for o in ORGS_SORTED)
    dup = '<span aria-hidden="true" style="display:contents">%s</span>' % ''.join(lg(o, True) for o in ORGS_SORTED)
    s.append('<section class="logos" aria-label="%s" v-pre><p>%s</p><div class="marq"><div class="marq-t">%s%s</div></div></section>' % (
        esc(I['logos_title']), esc(I['logos_title']), track, dup))
    # how
    cards = ''.join('<article class="card spot anim rv" data-fx="%s"><span class="tile">%s</span><h3>%s</h3><p>%s</p></article>' % (
        fx, icon(ic, 'gi lg'), esc(h['t']), esc(h['d'])) for (ic, fx), h in zip(HOW_ICONS, I['how']))
    s.append('<section class="s" id="how" v-pre><div class="wrap"><span class="eyebrow">%s %s</span><h2 class="rv">%s</h2><p class="sub rv">%s</p><div class="how">%s</div></div></section>' % (
        icon('sparkles', 'gi sm'), esc(I['how_eyebrow']), esc(I['how_title']), esc(I['how_sub']), cards))
    # contributions grid
    grid = ''.join(org_card(lang, o) for o in ORGS_SORTED)
    s.append('<section class="s" id="work" v-pre><div class="wrap"><span class="eyebrow">%s %s</span><h2 class="rv">%s</h2><p class="sub rv">%s</p>'
             '<div class="orgs">%s</div><p class="more"><a class="btn pri" href="%s">%s%s</a></p></div></section>' % (
                 icon('git-pull-request', 'gi sm'), esc(I['contrib_eyebrow']), esc(I['contrib_h2']), esc(T(lang, 'contrib_sub')), grid,
                 BASE + CONTRIB[lang], esc(T(lang, 'orgs_more')), icon('arrow-right', 'gi sm')))
    # highlights
    hl = ''.join('<a class="card spot" href="%s" rel="noopener"><span class="ic">%s</span><span><span class="repo">%s<span class="stars">%s %s</span></span><span class="t">%s</span></span></a>' % (
        esc(h['url']), icon('git-merge'), esc(h['repo']), icon('star', 'gi sm'), esc(h['stars']), md_inline(h['title_md'])) for h in HL)
    s.append('<section class="s" id="highlights" v-pre><div class="wrap"><span class="eyebrow">%s %s</span><h2 class="rv">%s</h2><p class="sub rv">%s</p><div class="hl">%s</div></div></section>' % (
        icon('trophy', 'gi sm'), esc(I['hl_eyebrow']), esc(I['hl_title']), esc(I['hl_sub']), hl))
    # founder
    pts = ''.join('<li>%s%s</li>' % (icon(ic), esc(t)) for ic, t in zip(['flame', 'zap', 'send'], E['f_points']))
    s.append('<section class="s" id="founder" v-pre><div class="wrap"><span class="eyebrow">%s %s</span>'
             '<div class="card spot founder rv"><div><span class="brandz">Zupte</span><h2>%s</h2><p>%s</p>'
             '<a class="btn pri" href="%s" rel="noopener">%s%s</a></div><ul>%s</ul></div></div></section>' % (
                 icon('rocket', 'gi sm'), esc(E['f_eyebrow']), esc(E['f_title']), esc(E['f_text']), ZUPTE, esc(E['f_cta']), icon('arrow-up-right', 'gi sm'), pts))
    # projects
    pc = []
    for i, p in enumerate(PROJECTS):
        tr = I['projects'].get(p['name'], {})
        links = ''.join('<a href="%s" rel="noopener">%s</a>' % (esc(l['href']), esc(I['links'].get(l['label'], l['label']))) for l in p['links'])
        links += '<a href="%s" rel="noopener">%s%s</a>' % (esc(p['repo']), icon('brand-github', 'gi sm'), esc(I['links'].get('GitHub', 'GitHub')))
        pc.append('<article class="card spot proj%s"><div class="top"><a class="logo" href="%s" rel="noopener" tabindex="-1" aria-hidden="true">%s</a>'
                  '<div><h3><a href="%s" rel="noopener">%s</a></h3><span class="tag">%s</span></div></div>'
                  '<p>%s</p><div class="links">%s</div></article>' % (
                      ' big' if i in (0, 3) else '', esc(p['repo']), img(p['logo'], '', 38, 38), esc(p['repo']), esc(p['name']),
                      esc(tr.get('tag', p['tag'])), esc(tr.get('desc', '')), links))
    s.append('<section class="s" id="projects" v-pre><div class="wrap"><span class="eyebrow">%s %s</span><h2 class="rv">%s</h2><p class="sub rv">%s</p><div class="projs">%s</div></div></section>' % (
        icon('package', 'gi sm'), esc(I['proj_eyebrow']), esc(I['proj_title']), esc(I['proj_sub']), ''.join(pc)))
    # stack
    st = ''.join('<div class="card"><h3>%s%s</h3><div class="chips">%s</div></div>' % (
        icon(ic, 'gi sm'), esc(name), ''.join('<span class="chip">%s</span>' % esc(x) for x in g['items']))
        for ic, name, g in zip(STACK_ICONS, I['stack_groups'].values(), STACK))
    s.append('<section class="s" id="stack" v-pre><div class="wrap"><span class="eyebrow">%s %s</span><h2 class="rv">%s</h2><div class="stack">%s</div></div></section>' % (
        icon('layers', 'gi sm'), esc(I['stack_eyebrow']), esc(I['stack_title']), st))
    # contact
    s.append('<section class="s" id="contact"><div class="wrap"><div class="contact">'
             '<span class="eyebrow" v-pre>%s %s</span><h2 v-pre>%s</h2><p class="sub" v-pre>%s</p>'
             '<div class="cta">'
             '<a class="btn pri" href="mailto:%s">%s%s</a>'
             '<span v-data="mail()"><button class="btn" type="button" @click="copy()">%s<span v-text="done ? \'%s\' : \'%s\'">%s</span></button></span>'
             '<a class="btn" href="%s" rel="noopener">%s%s %s</a>'
             '<a class="btn" href="%s" rel="me noopener">%s%s</a>'
             '<a class="btn" href="%s" rel="me noopener">%s%s</a>'
             '<a class="btn" href="%s" download>%s%s</a>'
             '</div></div></div></section>' % (
                 icon('send', 'gi sm'), esc(I['contact_eyebrow']), esc(I['contact_title']), esc(I['contact_sub']),
                 EMAIL, icon('mail', 'gi sm'), EMAIL,
                 icon('copy', 'gi sm'), js_str(I['copied']), js_str(I['copy_email']), esc(I['copy_email']),
                 WA, icon('smartphone', 'gi sm'), esc(E['whatsapp']), esc(PHONE),
                 LINKEDIN, icon('brand-linkedin', 'gi sm'), esc(E['linkedin']),
                 GH, icon('brand-github', 'gi sm'), esc(E['github']),
                 resume(lang), icon('book', 'gi sm'), esc(E['resume_short'])))
    return '\n'.join(s)


def js_str(s):
    return esc(s.replace('\\', '\\\\').replace("'", "\\'"))


def home_ld(lang):
    I = I18N[lang]
    url = ABS + HOME[lang]
    projects = {'@type': 'ItemList', 'name': I['proj_title'], 'numberOfItems': len(PROJECTS), 'itemListElement': []}
    for i, p in enumerate(PROJECTS):
        tr = I['projects'].get(p['name'], {})
        site = next((l['href'] for l in p['links'] if l['label'] == 'Website'), p['repo'])
        projects['itemListElement'].append({'@type': 'ListItem', 'position': i + 1, 'item': {
            '@type': 'SoftwareSourceCode', 'name': p['name'], 'description': tr.get('desc', p['tag']),
            'codeRepository': p['repo'], 'url': site, 'license': 'https://opensource.org/licenses/MIT',
            'author': {'@id': ABS + '#person'}, 'image': p['logo']}})
    return [person_ld(lang), zupte_ld(), website_ld(),
            {'@type': 'ProfilePage', '@id': url + '#page', 'url': url, 'name': T(lang, 'title'), 'description': T(lang, 'description'),
             'inLanguage': HREFLANG[lang], 'isPartOf': {'@id': ABS + '#website'}, 'mainEntity': {'@id': ABS + '#person'},
             'dateModified': TODAY, 'primaryImageOfPage': OG_IMG},
            projects]

# ---------------------------------------------------------------- contributions


def pr_row(p, idx=None):
    show = ' v-show="hit(q, %d)"' % idx if idx is not None else ''
    return ('<a class="card pr" href="%s" rel="noopener"%s>%s<span><span class="rp" v-pre>%s</span><span class="t" v-pre>%s</span>%s</span>%s</a>') % (
        esc(p['url']), show, icon('git-merge', 'gi sm'), esc(p['repo']), md_inline(p['title_md']),
        '<small class="rp" v-pre>%s</small>' % esc(p['note']) if p.get('note') else '', icon('arrow-up-right', 'gi sm x'))


def contrib_body(lang):
    I = I18N[lang]
    E = EXTRA[lang]
    groups = []
    i = 0
    for oi, o in enumerate(ORGS_SORTED):
        rows = []
        for p in o['prs']:
            rows.append(pr_row(p, i))
            i += 1
        groups.append('<section class="og" v-show="orgHit(q, %d)"><h2><a class="flex items-center gap-2" href="%s">%s<span v-pre>%s</span></a> <small>%d</small></h2><div class="prs">%s</div></section>' % (
            oi, org_url(lang, o), img(o['logo'], '', 26, 26), esc(o['name']), o['count'], ''.join(rows)))
    return ('<div class="wrap"><ol class="crumbs" v-pre><li><a href="%s">%s</a></li><li aria-current="page">%s</li></ol>'
            '<header class="page-h" v-pre><span class="eyebrow">%s %s</span><h1>%s</h1><p class="sub">%s</p></header>'
            '<div v-data="search()">'
            '<label class="search">%s<input type="search" v-model="q" placeholder="%s" aria-label="%s" autocomplete="off"><small v-text="label(q)" aria-live="polite">%s</small></label>'
            '%s'
            '<p class="empty" v-show="shown(q) === 0" v-cloak>%s</p>'
            '</div>'
            '<p class="backs" v-pre><a class="btn" href="%s">%s%s</a></p></div>') % (
        BASE + HOME[lang], esc(E['home']), esc(I['page_h1']),
        icon('git-pull-request', 'gi sm'), esc(I['contrib_eyebrow']), esc(I['page_h1']), esc(T(lang, 'page_sub')),
        icon('search', 'gi sm'), esc(I['search_placeholder']), esc(I['search_placeholder']), esc(I['found'].replace('{n}', str(N_PRS))),
        ''.join(groups), esc(I['none']), BASE + HOME[lang], icon('arrow-right', 'gi sm'), esc(I['back']))


def search_scripts():
    prs, porg = [], []
    names = [o['name'] for o in ORGS_SORTED]
    for oi, o in enumerate(ORGS_SORTED):
        for p in o['prs']:
            prs.append(('%s %s' % (p['repo'], md_plain(p['title_md']))).lower())
            porg.append(oi)
    js = 'window.__PRS=%s;window.__PR_ORG=%s;window.__ORGS=%s' % (
        json.dumps(prs, ensure_ascii=False, separators=(',', ':')), json.dumps(porg, separators=(',', ':')),
        json.dumps(names, ensure_ascii=False, separators=(',', ':')))
    return '<script>%s</script>' % js.replace('</', '<\\/')


def org_body(lang, o):
    I = I18N[lang]
    E = EXTRA[lang]
    nr = len(o['repos'])
    if o['count'] == 1:
        sub = E['one_pr']
    elif nr == 1:
        sub = X(lang, 'org_sub1', n=o['count'])
    else:
        sub = X(lang, 'org_sub', n=o['count'], r=nr)
    repos = []
    for r in o['repos']:
        repos.append('<section class="og"><div class="repo-h"><h2><a href="%s" rel="noopener">%s</a></h2>%s</div><div class="prs">%s</div></section>' % (
            esc(r['url']), esc(r['full']), '<small>%s</small>' % esc(r['desc']) if r['desc'] else '', ''.join(pr_row(p) for p in r['prs'])))
    k = ORGS_SORTED.index(o)
    rel = [ORGS_SORTED[(k + j) % N_ORGS] for j in range(1, 9)]
    return ('<div class="wrap" v-pre><ol class="crumbs"><li><a href="%s">%s</a></li><li><a href="%s">%s</a></li><li aria-current="page">%s</li></ol>'
            '<header class="page-h"><div class="org-h">%s<div><span class="eyebrow">%s %s %s</span><h1>%s</h1></div></div>'
            '<p class="sub">%s</p><p class="flex flex-wrap gap-2"><a class="btn sm" href="%s" rel="noopener">%s%s</a></p></header>'
            '%s'
            '<section class="s" style="padding-top:40px"><h2>%s</h2><div class="orgs">%s</div></section>'
            '<p class="backs"><a class="btn pri" href="%s">%s%s</a><a class="btn" href="%s">%s</a></p></div>') % (
        BASE + HOME[lang], esc(E['home']), BASE + CONTRIB[lang], esc(I['page_h1']), esc(o['name']),
        img(o['logo'], o['name'], 72, 72, lazy=False), icon('git-pull-request', 'gi sm'), o['count'], esc(E['pr_word']),
        esc(X(lang, 'org_title', org=o['name'])), esc(sub), esc(o['url']), icon('brand-github', 'gi sm'), esc(X(lang, 'org_gh', org=o['name'])),
        ''.join(repos), esc(E['related']), ''.join(org_card(lang, x) for x in rel),
        BASE + CONTRIB[lang], esc(E['all']), icon('arrow-right', 'gi sm'), BASE + HOME[lang], esc(I['back']))

# ---------------------------------------------------------------- 404


def nf_page(css, js):
    I = I18N['en']
    homes = ''.join('<a class="btn%s" href="%s" data-lang="%s" hreflang="%s" lang="%s">%s</a>' % (
        ' pri' if l == 'en' else '', BASE + HOME[l], l, HREFLANG[l], I18N[l]['html_lang'], esc(I18N[l]['nf_home'] + ' (' + I18N[l]['lang_name'] + ')')) for l in LANGS)
    body = ('<section class="lost" v-pre><div>%s<h1>%s</h1><p class="sub" style="margin:0 auto 28px">%s</p><div class="cta" style="justify-content:center">%s</div></div></section>') % (
        art.eye404_svg(), esc(I['nf_title']), esc(I['nf_text']), homes)
    alts = {l: BASE + HOME[l] for l in LANGS}
    return '\n'.join([head('en', I['nf_title'] + ' | kwy404', I['nf_text'], BASE + '404.html', None, css, js, [person_ld('en'), website_ld()], noindex=True),
                      '<body>', '<div class="bgfx" aria-hidden="true"><div class="blob b1"></div><div class="blob b2"></div></div>', sprite(),
                      nav('en', alts, False), '<main id="main">', body, '</main>', footer('en', alts), term_island('en'), i18n_json('en'),
                      '</body>', '</html>', ''])

# ---------------------------------------------------------------- write


def write(path_url, content):
    rel = path_url[len(BASE):]
    if rel.endswith('/') or rel == '':
        rel += 'index.html'
    f = os.path.join(DOCS, rel)
    os.makedirs(os.path.dirname(f), exist_ok=True)
    open(f, 'w', encoding='utf-8').write(content)
    return f


def clean():
    for l in LANGS:
        for d in [HOME[l], CONTRIB[l]]:
            if d:
                p = os.path.join(DOCS, d)
                if os.path.isdir(p):
                    shutil.rmtree(p)
    for f in ['index.html', '404.html', 'sitemap.xml', 'robots.txt', 'site.webmanifest', '.nojekyll', 'assets/prs.json', 'assets/avatar.jpg']:
        p = os.path.join(DOCS, f)
        if os.path.exists(p):
            os.remove(p)
    p = os.path.join(DOCS, 'assets', 'css')
    if os.path.isdir(p):
        shutil.rmtree(p)


def monsoon(pages):
    d = os.path.join(DOCS, 'assets', 'css')
    tmp = os.path.join(d, 'monsoon.tmp.css')
    bunx = os.environ.get('BUNX', '/root/.bun/bin/bunx')
    ok = False
    # Monsoon's purge keeps its whole component layer (.card, .btn, .hero, .stack, .toast...), whose names clash with
    # this site's own classes. Feed it only the utilities part of the official stylesheet, so the output holds just
    # the utility classes the pages use.
    src = os.path.join(HERE, '.cache', 'monsoon-utilities.css')
    try:
        full = None
        for f in glob.glob('/root/.bun/install/cache/monsooncss@0.2.0*/dist/monsoon.css'):
            full = open(f, encoding='utf-8').read()
            break
        if full is None:
            import urllib.request
            full = urllib.request.urlopen('https://cdn.jsdelivr.net/npm/monsooncss@0.2.0/dist/monsoon.css', timeout=60).read().decode('utf-8')
        k = full.index('/* monsoon:utilities */')
        os.makedirs(os.path.dirname(src), exist_ok=True)
        open(src, 'w', encoding='utf-8').write(full[k:])
    except Exception as e:  # noqa: BLE001
        print('monsoon source not found:', e)
        src = None
    try:
        r = subprocess.run(['timeout', '120', bunx, 'monsooncss@0.2.0', 'purge', '../docs/**/*.html', '-o', '../docs/assets/css/monsoon.tmp.css']
                           + (['--css', src] if src else []),
                           cwd=HERE, capture_output=True, text=True)
        ok = r.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 40
        print('monsoon purge:', (r.stderr or r.stdout).strip().splitlines()[-1:] if (r.stderr or r.stdout) else r.returncode)
    except Exception as e:  # noqa: BLE001
        print('monsoon purge failed:', e)
    if ok:
        data = open(tmp, 'rb').read()
        hh = h8(data)
        fn = 'monsoon.%s.css' % hh
        os.replace(tmp, os.path.join(d, fn))
        href = '%sassets/css/%s?v=%s' % (BASE, fn, hh)
    else:
        if os.path.exists(tmp):
            os.remove(tmp)
        href = MONSOON_CDN
        print('using Monsoon from the CDN')
    for f in pages:
        s = open(f, encoding='utf-8').read().replace('__MONSOON__', href)
        open(f, 'w', encoding='utf-8').write(s)
    return href


def main():
    os.makedirs(DOCS, exist_ok=True)
    clean()
    css = build_css()
    js = find_js()
    shutil.copy(os.path.join(HERE, 'assets', 'avatar.jpg'), os.path.join(DOCS, 'assets', 'avatar.jpg'))
    pages, sitemap = [], []
    home_css = [css['core'], css['sections'], css['eggs']]
    contrib_css = [css['core'], css['contrib'], css['eggs']]

    home_alts = {l: BASE + HOME[l] for l in LANGS}
    contrib_alts = {l: BASE + CONTRIB[l] for l in LANGS}
    for lang in LANGS:
        I = I18N[lang]
        # home
        path = BASE + HOME[lang]
        pages.append(write(path, page(lang, T(lang, 'title'), T(lang, 'description'), path, home_alts, home_css, js, home_ld(lang),
                                      home_body(lang), root=(lang == 'en'), on_home=True)))
        # all PRs
        path = BASE + CONTRIB[lang]
        title = T(lang, 'contrib_title')
        ld = [person_ld(lang), website_ld(),
              {'@type': 'CollectionPage', '@id': SITE + path + '#page', 'url': SITE + path, 'name': title, 'description': T(lang, 'contrib_description'),
               'inLanguage': HREFLANG[lang], 'isPartOf': {'@id': ABS + '#website'}, 'about': {'@id': ABS + '#person'}, 'dateModified': TODAY,
               'mainEntity': {'@id': SITE + path + '#list'}},
              crumbs_ld([(EXTRA[lang]['home'], ABS + HOME[lang]), (I['page_h1'], SITE + path)])]
        lst = pr_list_ld([p for o in ORGS_SORTED for p in o['prs']], title)
        lst['@id'] = SITE + path + '#list'
        ld.append(lst)
        pages.append(write(path, page(lang, title, T(lang, 'contrib_description'), path, contrib_alts, contrib_css, js, ld,
                                      contrib_body(lang), extra_scripts=search_scripts())))
    # org pages
    for o in ORGS_SORTED:
        alts = {l: org_url(l, o) for l in LANGS}
        repos = ', '.join(r['full'] for r in o['repos'])
        for lang in LANGS:
            I = I18N[lang]
            path = org_url(lang, o)
            title = X(lang, 'org_title', org=o['name'])
            desc = X(lang, 'org_desc', n=o['count'], org=o['name'], repos=repos)
            if len(desc) > 300:
                desc = desc[:297].rsplit(',', 1)[0] + '...'
            ld = [person_ld(lang), website_ld(),
                  {'@type': 'CollectionPage', '@id': SITE + path + '#page', 'url': SITE + path, 'name': title, 'description': desc,
                   'inLanguage': HREFLANG[lang], 'isPartOf': {'@id': ABS + '#website'}, 'author': {'@id': ABS + '#person'}, 'dateModified': TODAY,
                   'about': {'@type': 'Organization', 'name': o['name'], 'url': o['url'], 'logo': o['logo']},
                   'mainEntity': {'@id': SITE + path + '#list'}},
                  crumbs_ld([(EXTRA[lang]['home'], ABS + HOME[lang]), (I['page_h1'], ABS + CONTRIB[lang]), (o['name'], SITE + path)])]
            lst = pr_list_ld(o['prs'], title)
            lst['@id'] = SITE + path + '#list'
            ld.append(lst)
            pages.append(write(path, page(lang, title + ' | kwy404', desc, path, alts, contrib_css, js, ld, org_body(lang, o))))
    # sitemap
    groups = [home_alts, contrib_alts] + [{l: org_url(l, o) for l in LANGS} for o in ORGS_SORTED]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for gi, g in enumerate(groups):
        for l in LANGS:
            sm.append('<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority>' % (
                esc(SITE + g[l]), TODAY, 'weekly' if gi < 2 else 'monthly', '1.0' if gi == 0 else ('0.8' if gi == 1 else '0.6')))
            for l2 in LANGS:
                sm.append('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (HREFLANG[l2], esc(SITE + g[l2])))
            sm.append('<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % esc(SITE + g['en']))
            sm.append('</url>')
    sm.append('</urlset>')
    open(os.path.join(DOCS, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
    open(os.path.join(DOCS, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % ABS)
    open(os.path.join(DOCS, '.nojekyll'), 'w').write('')
    manifest = {'name': 'Alexandre Kohler (kwy404)', 'short_name': 'kwy404', 'description': T('en', 'description'),
                'start_url': BASE, 'scope': BASE, 'display': 'standalone', 'background_color': '#050507', 'theme_color': '#050507',
                'icons': [{'src': BASE + 'assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                          {'src': BASE + 'assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                          {'src': BASE + 'assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]}
    open(os.path.join(DOCS, 'site.webmanifest'), 'w').write(json.dumps(manifest, indent=2) + '\n')
    json.dump([[p['repo'], md_plain(p['title_md'])] for o in ORGS_SORTED for p in o['prs']],
              open(os.path.join(DOCS, 'assets', 'prs.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    nf = os.path.join(DOCS, '404.html')
    open(nf, 'w', encoding='utf-8').write(nf_page(contrib_css, js))
    pages.append(nf)
    href = monsoon(pages)
    print('pages: %d (orgs %d, prs %d) monsoon=%s' % (len(pages), N_ORGS, N_PRS, href))


if __name__ == '__main__':
    main()
