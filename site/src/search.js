// Busca na lista de todos os pull requests (pagina de contribuicoes). O HTML ja traz tudo; aqui so filtra.
const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
export function searchIsland(I) {
  const idx = (window.__PRS || []).map(norm)
  const orgOf = window.__PR_ORG || []
  const orgs = (window.__ORGS || []).map(norm)
  return {
    q: '',
    hit(q, i) { const n = norm(q).trim(); return !n || idx[i].includes(n) || orgs[orgOf[i]].includes(n) },
    orgHit(q, o) { const n = norm(q).trim(); if (!n) return true; if (orgs[o].includes(n)) return true; for (let i = 0; i < idx.length; i++) if (orgOf[i] === o && idx[i].includes(n)) return true; return false },
    shown(q) { let c = 0; for (let i = 0; i < idx.length; i++) if (this.hit(q, i)) c++; return c },
    label(q) { const c = this.shown(q); return (I.found || '{n} pull requests').replace('{n}', c) },
  }
}
