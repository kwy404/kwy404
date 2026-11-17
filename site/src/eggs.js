// Easter eggs. Carregam depois da pagina pronta, num pedaco separado do JS.
export function eggs(I, BASE) {
  const E = I.eggs || {}
  const root = document.documentElement
  const toast = (s, ms = 2600) => { const d = document.createElement('div'); d.className = 'toast'; d.setAttribute('v-pre', ''); d.setAttribute('role', 'status'); d.textContent = s; document.body.appendChild(d); setTimeout(() => d.remove(), ms) }
  const typing = (e) => { const t = e.target; return t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable) }

  // 1. terminal: "/" ou "`"
  addEventListener('keydown', (e) => {
    if (typing(e) || e.metaKey || e.ctrlKey || e.altKey) return
    if (e.key === '/' || e.key === '`') { e.preventDefault(); window.__term && window.__term.show() }
  })
  for (const b of document.querySelectorAll('[data-term]')) b.addEventListener('click', () => window.__term && window.__term.show())

  // 2. codigo Konami: a pagina derrete (igual ao avatar)
  const K = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a']
  let k = 0
  const melt = () => { root.classList.toggle('melt'); toast(root.classList.contains('melt') ? (E.melt || 'Reality is melting.') : (E.unmelt || 'Back to normal. Or is it?')) }
  window.__melt = melt
  addEventListener('keydown', (e) => { if (typing(e)) return; k = (e.key.toLowerCase() === K[k].toLowerCase()) ? k + 1 : (e.key === K[0] ? 1 : 0); if (k === K.length) { k = 0; melt() } })

  // 3. digitar "merge": chuva de logos das organizacoes
  let buf = ''
  const merge = () => {
    const logos = [...document.querySelectorAll('.lg img, .org img')].map((i) => i.src).filter((v, i, a) => a.indexOf(v) === i)
    if (!logos.length) return
    const r = document.createElement('div'); r.className = 'rain'; r.setAttribute('aria-hidden', 'true')
    for (let i = 0; i < 46; i++) { const im = document.createElement('img'); im.src = logos[i % logos.length]; im.alt = ''; im.style.left = Math.random() * 100 + 'vw'; im.style.animationDuration = 2.4 + Math.random() * 2.6 + 's'; im.style.animationDelay = Math.random() * 1.2 + 's'; r.appendChild(im) }
    document.body.appendChild(r); setTimeout(() => r.remove(), 7000)
    toast(E.merge || 'git merge: 59 organizations, 0 conflicts.')
  }
  window.__merge = merge
  addEventListener('keydown', (e) => { if (typing(e) || e.key.length !== 1) return; buf = (buf + e.key.toLowerCase()).slice(-5); if (buf === 'merge') { buf = ''; merge() } })

  // 4. sete cliques na foto: abre o terceiro olho e os olhos seguem o mouse
  let clicks = 0, ct = 0
  for (const av of document.querySelectorAll('[data-avatar]')) av.addEventListener('click', (e) => {
    clicks++; clearTimeout(ct); ct = setTimeout(() => (clicks = 0), 1600)
    if (clicks >= 7) { e.preventDefault(); clicks = 0; root.classList.add('third-eye'); toast(E.eye || 'Third eye: open. They are watching you now.') }
  })
  addEventListener('pointermove', (e) => {
    if (!root.classList.contains('third-eye')) return
    for (const p of document.querySelectorAll('.art .pupil')) {
      const r = p.ownerSVGElement.getBoundingClientRect(), b = p.getBBox(), sx = r.width / 600
      const cx = r.left + (b.x + b.width / 2) * sx, cy = r.top + (b.y + b.height / 2) * sx
      const a = Math.atan2(e.clientY - cy, e.clientX - cx)
      p.setAttribute('transform', `translate(${Math.cos(a) * 5} ${Math.sin(a) * 4})`)
    }
  }, { passive: true })

  // 5. madrugada no relogio de quem visita (qualquer fuso): ceu estrelado e um aviso
  const h = new Date().getHours()
  if (h >= 0 && h < 5) { root.classList.add('night'); setTimeout(() => toast(E.night || 'It is late where you are. Go to sleep, the code will still be here tomorrow.', 5200), 1800) }

  // 6. segurar o contador de PRs: git log com os pull requests de verdade
  const gitlog = async () => {
    if (document.querySelector('.gitlog')) return
    let list = []
    try { list = await (await fetch(BASE + 'assets/prs.json', { cache: 'force-cache' })).json() } catch (e) { return }
    const w = document.createElement('div'); w.className = 'gitlog'; w.setAttribute('v-pre', ''); w.setAttribute('role', 'dialog'); w.setAttribute('aria-label', 'git log')
    const inner = document.createElement('div')
    for (const p of list) { const a = document.createElement('div'); const hsh = document.createElement('span'); hsh.className = 'h'; hsh.textContent = 'merge ' + Math.random().toString(16).slice(2, 9) + ' '; a.appendChild(hsh); a.appendChild(document.createTextNode(p[0] + '  ' + p[1])); inner.appendChild(a) }
    w.appendChild(inner); document.body.appendChild(w)
    const close = () => { w.remove(); removeEventListener('keydown', esc) }
    const esc = (e) => { if (e.key === 'Escape') close() }
    w.addEventListener('click', close); addEventListener('keydown', esc); setTimeout(close, 18500)
  }
  window.__gitlog = gitlog
  for (const s of document.querySelectorAll('[data-hold]')) {
    let t = 0
    const start = () => { t = setTimeout(gitlog, 900) }, stop = () => clearTimeout(t)
    s.addEventListener('pointerdown', start); s.addEventListener('pointerup', stop); s.addEventListener('pointerleave', stop)
    s.addEventListener('keydown', (e) => { if (e.key === 'Enter') gitlog() })
  }
}
