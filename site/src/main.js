// kwy404 · portfolio. Ilhas interativas com Voodoo.js; visual com Monsoon; icones glyphfox.
import { termIsland } from './term.js'
import { searchIsland } from './search.js'

const doc = document.documentElement
doc.classList.remove('no-js')
window.__kwy = 1
const I = JSON.parse(document.getElementById('i18n')?.textContent || '{}')
const BASE = doc.dataset.base || '/'
const LANGS = ['en', 'pt', 'es', 'ja']

// ---------- idioma: na pagina raiz, manda para o idioma do aparelho na primeira visita
;(() => {
  if (doc.dataset.root !== '1') return
  let saved = null
  try { saved = localStorage.getItem('kwy:lang') } catch (e) {}
  if (saved) return
  const want = (navigator.languages || [navigator.language || 'en']).map((l) => String(l).toLowerCase().slice(0, 2)).find((l) => LANGS.includes(l))
  if (want && want !== 'en') location.replace(BASE + want + '/' + location.hash)
})()
document.addEventListener('click', (e) => {
  const a = e.target.closest && e.target.closest('a[data-lang]')
  if (a) try { localStorage.setItem('kwy:lang', a.dataset.lang) } catch (err) {}
})

// ---------- ilhas do Voodoo.js (o runtime liga sozinho quando a pagina termina de carregar)
const V = window.V
if (V && V.config) {
  V.config.globals.nav = () => ({
    open: false, lang: false,
    toggle() { this.open = !this.open; document.body.style.overflow = this.open ? 'hidden' : '' },
    go() { this.open = false; document.body.style.overflow = '' },
  })
  V.config.globals.term = () => termIsland(I)
  V.config.globals.search = () => searchIsland(I)
  V.config.globals.mail = () => ({
    done: false,
    async copy() {
      try { await navigator.clipboard.writeText('thekaway404@gmail.com'); this.done = true; setTimeout(() => (this.done = false), 1800) } catch (e) { location.href = 'mailto:thekaway404@gmail.com' }
    },
  })
}

// ---------- imagens: esqueleto some quando carregam (ou quando falham)
for (const im of document.querySelectorAll('img.sk')) {
  const done = () => im.classList.remove('sk'), fail = () => { im.classList.remove('sk'); im.classList.add('err') }
  if (im.complete) { im.naturalWidth ? done() : fail() } else { im.addEventListener('load', done, { once: true }); im.addEventListener('error', fail, { once: true }) }
}

// ---------- topo fica solido ao rolar
const nav = document.querySelector('.nav')
const onScroll = () => nav && nav.classList.toggle('solid', scrollY > 8)
addEventListener('scroll', onScroll, { passive: true }); onScroll()

// ---------- comprimento de cada traco dos icones (para a animacao de desenhar)
for (const p of document.querySelectorAll('.gi path, .gi circle, .gi rect, .gi line, .gi polyline, .gi ellipse')) {
  try { p.style.setProperty('--len', Math.ceil(p.getTotalLength() + 1)) } catch (e) {}
}

// ---------- aparece ao rolar (no celular os icones animam aqui, sem hover)
const touch = matchMedia('(hover: none)').matches
const io = 'IntersectionObserver' in window ? new IntersectionObserver((list) => {
  for (const en of list) if (en.isIntersecting) { en.target.classList.add('seen'); io.unobserve(en.target) }
}, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 }) : null
for (const el of document.querySelectorAll('.rv, .anim, .proj')) {
  if (!io) { el.classList.add('seen'); continue }
  if (!touch && el.classList.contains('anim') && !el.classList.contains('rv')) continue
  io.observe(el)
}

// ---------- luz que segue o mouse nos cartoes
if (!touch) document.addEventListener('pointermove', (e) => {
  const c = e.target.closest && e.target.closest('.spot'); if (!c) return
  const r = c.getBoundingClientRect()
  c.style.setProperty('--mx', e.clientX - r.left + 'px'); c.style.setProperty('--my', e.clientY - r.top + 'px')
}, { passive: true })

// ---------- contadores sobem quando aparecem
for (const b of document.querySelectorAll('[data-count]')) {
  const to = Number(b.dataset.count), suf = b.dataset.suffix || ''
  const run = () => { const t0 = performance.now(); const step = (t) => { const k = Math.min(1, (t - t0) / 1400); b.textContent = Math.round(to * (1 - Math.pow(1 - k, 3))) + suf; if (k < 1) requestAnimationFrame(step) }; requestAnimationFrame(step) }
  if (io) { const o = new IntersectionObserver(([en]) => { if (en.isIntersecting) { run(); o.disconnect() } }); o.observe(b) } else b.textContent = to + suf
}

// ---------- olho da pagina 404 segue o cursor
const lost = document.querySelector('.lost .pupil')
if (lost) addEventListener('pointermove', (e) => {
  const r = lost.ownerSVGElement.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2
  const a = Math.atan2(e.clientY - cy, e.clientX - cx), d = Math.min(14, Math.hypot(e.clientX - cx, e.clientY - cy) / 20)
  lost.setAttribute('transform', `translate(${Math.cos(a) * d} ${Math.sin(a) * d})`)
}, { passive: true })

// ---------- mensagem para quem abre o console
try {
  console.log('%c\n  kwy404\n', 'font:800 28px Inter,system-ui;background:linear-gradient(90deg,#8b7dff,#ff6ad5,#ffb547);-webkit-background-clip:text;color:transparent')
  console.log('%c' + (I.console || 'Reading the source? Say hi: thekaway404@gmail.com'), 'font:500 13px ui-monospace,monospace;color:#a1a1aa')
  console.log('%cBuilt with Voodoo.js, Monsoon and glyphfox. Press / for a terminal.', 'font:500 12px ui-monospace,monospace;color:#22d3ee')
} catch (e) {}

// ---------- easter eggs: carregam depois, em outro pedaco do JS
const loadEggs = () => import('./eggs.js').then((m) => m.eggs(I, BASE)).catch(() => {})
if ('requestIdleCallback' in window) requestIdleCallback(loadEggs, { timeout: 2500 }); else setTimeout(loadEggs, 1200)
