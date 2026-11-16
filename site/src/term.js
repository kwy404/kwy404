// Terminal escondido: abre com "/" ou "`". Comandos de verdade sobre o perfil, e algumas piadas.
const GH = 'https://github.com/kwy404'
export function termIsland(I) {
  const t = I.term || {}
  return {
    open: false, cmd: '', lines: [], hist: [], hi: -1,
    bind() {
      window.__term = this
      this.lines = [{ c: 'ok', s: t.hello || 'kwy404 terminal. Type help.' }]
    },
    show() { this.open = true; setTimeout(() => { const i = document.getElementById('term-in'); i && i.focus() }, 30) },
    close() { this.open = false },
    say(s, c) { this.lines = this.lines.concat([{ c: c || '', s }]).slice(-80); setTimeout(() => { const o = document.getElementById('term-out'); if (o) o.scrollTop = o.scrollHeight }, 10) },
    key(e) {
      if (e.key === 'Escape') return this.close()
      if (e.key === 'ArrowUp') { e.preventDefault(); if (this.hist.length) { this.hi = Math.min(this.hist.length - 1, this.hi + 1); this.cmd = this.hist[this.hist.length - 1 - this.hi] } return }
      if (e.key === 'ArrowDown') { e.preventDefault(); this.hi = Math.max(-1, this.hi - 1); this.cmd = this.hi < 0 ? '' : this.hist[this.hist.length - 1 - this.hi]; return }
      if (e.key !== 'Enter') return
      const raw = String(this.cmd || '').trim(); this.cmd = ''; this.hi = -1
      if (!raw) return
      this.hist.push(raw); this.say('~ $ ' + raw, 'in')
      const [c, ...a] = raw.split(/\s+/), arg = a.join(' ')
      const out = this.exec(c.toLowerCase(), arg)
      if (out) for (const l of [].concat(out)) this.say(l.s ?? l, l.c)
    },
    exec(c, arg) {
      const s = I.stats || {}
      switch (c) {
        case 'help': return (t.help || 'help whoami prs orgs projects stack contact lang open clear exit').split('\n')
        case 'whoami': return [t.whoami || 'Alexandre Kohler · Senior Full Stack Software Engineer · Brusque, Brazil']
        case 'prs': return [{ c: 'ok', s: `${s.prs} ${t.prs || 'merged pull requests'} · ${s.orgs} ${t.orgs || 'organizations'}` }, t.prsMore || 'open prs']
        case 'orgs': return [(I.topOrgs || []).join(' · ')]
        case 'projects': return (I.projects || []).map((p) => '• ' + p)
        case 'stack': return (I.stackLines || [])
        case 'contact': return ['thekaway404@gmail.com', 'linkedin.com/in/alexandre-silva-173687256', 'github.com/kwy404']
        case 'lang': {
          const l = (arg || '').slice(0, 2).toLowerCase()
          if (!['en', 'pt', 'es', 'ja'].includes(l)) return { c: 'er', s: 'lang en | pt | es | ja' }
          try { localStorage.setItem('kwy:lang', l) } catch (e) {}
          location.href = (document.documentElement.dataset.base || '/') + (l === 'en' ? '' : l + '/'); return '...'
        }
        case 'open': {
          const map = { github: GH, linkedin: 'https://www.linkedin.com/in/alexandre-silva-173687256/', prs: (I.contribUrl || 'contributions.html'), voodoo: 'https://kwy404.github.io/Voodoo.js/', monsoon: 'https://kwy404.github.io/monsoon/', glyphfox: 'https://kwy404.github.io/glyphfox/' }
          const u = map[(arg || '').toLowerCase()]; if (!u) return { c: 'er', s: 'open github | linkedin | prs | voodoo | monsoon | glyphfox' }
          location.href = u; return '...'
        }
        case 'sudo': return arg.startsWith('hire') ? [{ c: 'ok', s: t.hire || 'Permission granted. Opening your mail client...' }, (setTimeout(() => (location.href = 'mailto:thekaway404@gmail.com?subject=Hi%20Alexandre'), 900), '')] : { c: 'er', s: t.sudo || 'kwy404 is not in the sudoers file. This incident will be reported.' }
        case 'rm': return arg.includes('-rf') ? { c: 'er', s: t.rm || 'Nice try. Everything here has a failing test first.' } : { c: 'er', s: 'rm: missing operand' }
        case 'git': return arg.startsWith('merge') ? (window.__merge && window.__merge(), { c: 'ok', s: 'Fast-forward. 59 organizations updated.' }) : arg.startsWith('log') ? (window.__gitlog && window.__gitlog(), '') : 'git merge | git log'
        case 'matrix': case 'melt': window.__melt && window.__melt(); return 'ok'
        case 'clear': this.lines = []; return null
        case 'exit': this.close(); return null
        case 'ls': return 'contributions.html  projects/  stack.txt  secrets.txt'
        case 'cat': return arg.includes('secret') ? { c: 'ok', s: t.secret || 'Try the Konami code. ↑ ↑ ↓ ↓ ← → ← → B A' } : arg.includes('stack') ? (I.stackLines || []) : 'cat: ' + (arg || '') + ': No such file'
        default: return { c: 'er', s: `${c}: ${t.nf || 'command not found. Try help.'}` }
      }
    },
  }
}
