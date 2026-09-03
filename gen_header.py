#!/usr/bin/env python3
"""Gera light.svg e dark.svg — header animado estilo terminal para o perfil do kwy404."""
import html

# ---------- pixel art: arcade stick (24 colunas x 16 linhas) ----------
# . vazio  # corpo  o bola do manche  h haste  b botão  B botão aceso  = base
ART = """
........................
..........oo............
.........oooo...........
.........oooo...........
..........oo............
..........hh............
..........hh............
..........hh............
.######################.
.#......##..bb.bb.bb..#.
.#......##.bBBbBBbBBb.#.
.#......##.bBBbBBbBBb.#.
.#......##..bb.bb.bb..#.
.######################.
..====================..
........................
""".strip("\n").split("\n")

def pixels(theme):
    c = {
        "#": theme["body"], "o": theme["ball"], "h": theme["stick"],
        "b": theme["btn"], "B": theme["btnHot"], "=": theme["base"],
    }
    out, px = [], 15
    for y, row in enumerate(ART):
        for x, ch in enumerate(row):
            if ch == ".": continue
            delay = 0.35 + (y * 24 + x) * 0.004
            out.append(f'<rect x="{x*px}" y="{y*px}" width="{px}" height="{px}" fill="{c[ch]}" opacity="0">'
                       f'<animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="{delay:.2f}s" fill="freeze"/></rect>')
    return "\n".join(out)

THEMES = {
    "light": dict(bg="#FFFFFF", panelA="#F8FAFC", panelB="#EEF2F7", bar="#F1F5F9", line="rgba(15,23,42,0.10)",
                  muted="#94A3B8", label="#475569", key="#2563EB", val="#0F172A", dots="rgba(15,23,42,0.25)",
                  frame="#2563EB", frameSoft="rgba(37,99,235,0.35)",
                  body="#1E3A8A", ball="#DC2626", stick="#334155", btn="#60A5FA", btnHot="#22D3EE", base="#94A3B8"),
    "dark":  dict(bg="#0A101F", panelA="#0F172A", panelB="#0A101F", bar="#111A2E", line="rgba(255,255,255,0.08)",
                  muted="#475569", label="#94A3B8", key="#60A5FA", val="#F1F5F9", dots="rgba(148,163,184,0.25)",
                  frame="#3B82F6", frameSoft="rgba(96,165,250,0.35)",
                  body="#3B82F6", ball="#F87171", stick="#CBD5E1", btn="#93C5FD", btnHot="#22D3EE", base="#334155"),
}

LINES = [
    ("- Identity ", None),
    ("Subject", "Marlon Cesar Pereira"),
    ("Role", "Dev & Hardware Gaming Specialist"),
    ("Origin", "Brusque, SC - Brasil"),
    ("Business", "Hadouken Game Center / CENTER LAVACAO"),
    ("Status", "Building Voodoo.js"),
    ("- ToolChain ", None),
    ("Core.Lang", "JavaScript, TypeScript, Python"),
    ("Core.Frontend", "Voodoo.js, HTML, CSS"),
    ("Core.Backend", "Node.js"),
    ("Core.Hardware", "AMD / Intel / NVIDIA tuning"),
    ("Core.Infra", "Vercel, Git, Windows Optimization"),
    ("- Contact ", None),
    ("Grid.GitHub", "@kwy404"),
    ("Grid.Portfolio", "alexandrekohler.vercel.app"),
    ("Grid.Instagram", "@diretoria.hadouken"),
    ("Grid.Mail", "seu@email.com"),
]

def build(theme_name):
    t = THEMES[theme_name]
    parts = []
    y, begin = 100, 0.9
    total_chars = 62
    for key, val in LINES:
        if val is None:
            dots = "-" * (total_chars - len(key))
            parts.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
                         f'<text x="470" y="{y}" font-size="14" xml:space="preserve"><tspan fill="{t["label"]}">{key}</tspan><tspan fill="{t["dots"]}">{dots}</tspan></text></g>')
            y += 31
        else:
            dots = "." * max(3, total_chars - len(key) - len(val) - 2)
            parts.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
                         f'<animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
                         f'<text x="470" y="{y}" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="{t["key"]}">{html.escape(key)} </tspan>'
                         f'<tspan fill="{t["dots"]}">{dots}</tspan><tspan fill="{t["val"]}" font-weight="600"> {html.escape(val)}</tspan></text></g>')
            y += 23
        begin += 0.12
    info = "\n".join(parts)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Marlon Cesar Pereira - profile.sh --live">
<defs>
<linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t['panelA']}"/><stop offset="1" stop-color="{t['panelB']}"/></linearGradient>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#2563EB"><animate attributeName="stop-color" values="#2563EB;#22D3EE;#1E3A8A;#2563EB" dur="10s" repeatCount="indefinite"/></stop>
  <stop offset="1" stop-color="#22D3EE"><animate attributeName="stop-color" values="#22D3EE;#1E3A8A;#2563EB;#22D3EE" dur="10s" repeatCount="indefinite"/></stop>
</linearGradient>
<filter id="glow3" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>
<clipPath id="winClip"><rect x="2" y="2" width="1176" height="606" rx="18"/></clipPath>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="rgba(37,99,235,0.05)"/></pattern>
</defs>
<rect x="2" y="2" width="1176" height="606" rx="18" fill="{t['bg']}"/>
<g clip-path="url(#winClip)">
<rect x="2" y="2" width="1176" height="606" fill="url(#panelGrad)"/>
<rect x="2" y="2" width="1176" height="46" fill="{t['bar']}"/>
<line x1="2" y1="48" x2="1178" y2="48" stroke="{t['line']}"/>
<circle cx="30" cy="25" r="5.5" fill="#ff5f56"/><circle cx="50" cy="25" r="5.5" fill="#ffbd2e"/><circle cx="70" cy="25" r="5.5" fill="#27c93f"/>
<text x="590" y="29" text-anchor="middle" font-size="12" fill="{t['label']}">kwy404@hadouken ~ % ./profile.sh --live</text>

<text x="38" y="74" font-size="10" letter-spacing="3" fill="{t['muted']}">VISUAL.MAP</text>
<rect x="36" y="84" width="400" height="492" rx="10" fill="none" stroke="{t['frame']}" stroke-width="2" opacity="0.45" filter="url(#glow3)"/>
<rect x="36" y="84" width="400" height="492" rx="10" fill="{t['panelA']}" stroke="{t['frameSoft']}"/>
<rect x="37" y="85" width="398" height="490" rx="10" fill="url(#scan)"/>
<g transform="translate(56,146)" shape-rendering="crispEdges">
{pixels(t)}
</g>
<text x="236" y="430" text-anchor="middle" font-size="22" font-weight="700" fill="url(#accent)" letter-spacing="4" opacity="0">kwy404<animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="2.4s" fill="freeze"/></text>
<text x="236" y="456" text-anchor="middle" font-size="11" letter-spacing="2" fill="{t['muted']}" opacity="0">GAME CONNECTED<animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="2.7s" fill="freeze"/></text>
<rect x="120" y="486" width="232" height="6" rx="3" fill="{t['line']}"/>
<rect x="120" y="486" width="0" height="6" rx="3" fill="url(#accent)"><animate attributeName="width" from="0" to="232" dur="2.2s" begin="0.3s" fill="freeze"/></rect>
<text x="236" y="520" text-anchor="middle" font-size="10" fill="{t['muted']}" opacity="0">system loaded. fps: unlocked.<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.6s" fill="freeze"/></text>

<text x="470" y="74" font-size="10" letter-spacing="3" fill="{t['muted']}">SYSTEM.INFO</text>
{info}
<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="3.2s" fill="freeze"/>
<text x="470" y="577" font-size="14" fill="{t['label']}">&#9656; Mais sobre mim &amp; projetos abaixo no README &#8595; <tspan fill="#22D3EE">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
</g>
</g>
</svg>'''
    return svg

for name in THEMES:
    with open(f"{name}.svg", "w") as f:
        f.write(build(name))
    print("ok", name)
