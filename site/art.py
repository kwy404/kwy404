# -*- coding: utf-8 -*-
"""Hand-written SVG art for the portfolio: hero, 404 eye and social share image."""
import math
from html import escape

BG = "#050507"
YEL = "#ffd60a"


def _f(v):
    s = ("%.1f" % v).rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


# ---------------------------------------------------------------- hero

def _grid():
    hz = 345.0  # horizon
    out = []
    # horizontal lines, perspective spacing, waved by "gravity" toward the centre
    rows = []
    for i in range(1, 11):
        t = (i / 10.0) ** 1.8
        y = hz + t * (600 - hz)
        amp = 4 + 14 * t
        pts = []
        for k in range(0, 13):
            x = k * 50.0
            d = math.sin(k * 0.62 + i * 0.9) * amp * 0.45
            sag = amp * math.exp(-((x - 300) / 170.0) ** 2)  # pulled down in the middle
            pts.append((x, y + d + sag))
        p = "M" + " ".join("%s %s" % (_f(a), _f(b)) for a, b in pts)
        op = 0.25 + 0.6 * t
        rows.append('<path d="%s" stroke-opacity="%s"/>' % (p, _f(op)))
    out.append('<g class="grid-w" fill="none" stroke="url(#k-gridc)" stroke-width="1.4">%s</g>' % "".join(rows))
    # vertical perspective lines from vanishing point
    cols = []
    for j in range(-9, 10):
        xb = 300 + j * 70
        xm = 300 + j * 30
        cols.append('<path d="M300 %s Q%s 470 %s 600"/>' % (_f(hz - 10), _f(xm + j * 4), _f(xb)))
    out.append('<g fill="none" stroke="#ff4d6d" stroke-opacity=".32" stroke-width="1">%s</g>' % "".join(cols))
    return "".join(out)


def _stars(pts):
    s = []
    for i, (x, y, r) in enumerate(pts):
        s.append('<circle class="tw" cx="%s" cy="%s" r="%s" style="animation-delay:-%ss"/>'
                 % (x, y, r, _f((i * 0.73) % 4.0)))
    return '<g fill="#f5f5f7">%s</g>' % "".join(s)


def _float_eye(cls, lid, cx, cy, w, rot):
    h = w * 0.62
    ir = h * 0.72
    return (
        '<g class="%s"><g transform="rotate(%s %s %s)">'
        '<g class="%s">'
        '<path d="M%s %s Q%s %s %s %s Q%s %s %s %sZ" fill="#f5f5f7" stroke="%s" stroke-width="2"/>'
        '<circle cx="%s" cy="%s" r="%s" fill="%s"/>'
        '<circle cx="%s" cy="%s" r="%s" fill="#ffb547" fill-opacity=".55"/>'
        '<circle class="pupil" cx="%s" cy="%s" r="%s" fill="%s"/>'
        '<circle cx="%s" cy="%s" r="%s" fill="#fff"/>'
        '</g></g></g>'
    ) % (
        cls, rot, cx, cy, lid,
        _f(cx - w), cy, cx, _f(cy - h * 1.6), _f(cx + w), cy, cx, _f(cy + h * 1.6), _f(cx - w), cy, BG,
        cx, cy, _f(ir), YEL,
        cx, cy, _f(ir * 0.55),
        cx, cy, _f(ir * 0.45), BG,
        _f(cx - ir * 0.3), _f(cy - ir * 0.35), _f(ir * 0.14),
    )


def hero_svg():
    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" role="img" aria-labelledby="k-hero-t">')
    p.append('<title id="k-hero-t">__ART_TITLE__</title>')
    p.append(
        '<defs>'
        '<linearGradient id="k-gridc" x1="0" y1="345" x2="0" y2="600" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#ff6ad5"/><stop offset="1" stop-color="#ff3b5c"/></linearGradient>'
        '<linearGradient id="k-flow" x1="0" y1="600" x2="0" y2="290" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#8b7dff"/><stop offset=".55" stop-color="#ff6ad5"/>'
        '<stop offset="1" stop-color="#ffb547"/></linearGradient>'
        '<radialGradient id="k-moon" cx=".38" cy=".34" r=".75">'
        '<stop offset="0" stop-color="#fff3a3"/><stop offset=".45" stop-color="#ffd60a"/>'
        '<stop offset="1" stop-color="#f0a800"/></radialGradient>'
        '<radialGradient id="k-halo"><stop offset="0" stop-color="#ffd60a" stop-opacity=".28"/>'
        '<stop offset="1" stop-color="#ffd60a" stop-opacity="0"/></radialGradient>'
        '<filter id="k-glow" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="3.5" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '</defs>'
    )
    p.append('<rect width="600" height="600" fill="%s"/>' % BG)
    p.append(_grid())
    p.append(_stars([
        (42, 48, 1.6), (118, 92, 1.1), (64, 270, 1.3), (205, 36, 1.2), (388, 30, 1.5), (468, 64, 1.1),
        (556, 40, 1.7), (572, 238, 1.2), (528, 316, 1.0), (24, 176, 1.0), (160, 300, 1.1),
        (430, 300, 1.3), (250, 20, 0.9), (338, 58, 1.0),
    ]))
    # halo
    p.append('<circle cx="300" cy="190" r="165" fill="url(#k-halo)"/>')
    # merge graph (behind the moon so the trunk flows into it)
    branches = [
        "M130 600 C130 520 230 500 300 430",
        "M235 600 C235 540 290 480 300 430",
        "M385 600 C385 540 310 490 300 430",
        "M490 600 C490 515 360 495 300 430",
    ]
    trunk = "M300 430 C300 380 292 340 300 290"
    p.append('<g fill="none" stroke="url(#k-flow)" stroke-width="3.2" stroke-linecap="round" filter="url(#k-glow)">')
    for b in branches + [trunk]:
        p.append('<path class="flow" d="%s" stroke-dasharray="14 10"/>' % b)
    p.append('</g>')
    nodes = [(146, 560, "#8b7dff"), (241, 556, "#8b7dff"), (380, 556, "#ff6ad5"), (472, 548, "#8b7dff"),
             (232, 488, "#ff6ad5"), (372, 492, "#ff6ad5"), (300, 430, "#ffb547"), (298, 360, "#ffb547")]
    p.append('<g filter="url(#k-glow)">')
    for i, (x, y, c) in enumerate(nodes):
        p.append('<circle class="node" cx="%s" cy="%s" r="5" fill="%s" stroke="#f5f5f7" stroke-width="1.5" '
                 'style="animation-delay:-%ss"/>' % (x, y, c, _f(i * 0.45)))
    p.append('</g>')
    # melting smiley moon
    p.append('<g>')
    p.append('<g class="drip" fill="url(#k-moon)">'
             '<path d="M214 248 C214 290 204 312 214 322 C224 332 234 318 230 296 C228 280 236 262 240 256Z"/>'
             '<path d="M262 280 C262 320 256 352 266 362 C278 372 288 356 282 330 C280 312 286 296 290 286Z"/>'
             '<path d="M330 284 C332 304 330 318 338 326 C348 334 356 322 352 306 C350 296 354 288 358 280Z"/>'
             '<path d="M370 258 C372 290 366 302 374 310 C382 316 390 306 386 290 C384 278 388 266 390 260Z"/>'
             '<circle cx="222" cy="333" r="5"/><circle cx="275" cy="376" r="4.5"/>'
             '</g>')
    p.append('<circle cx="300" cy="190" r="110" fill="url(#k-moon)"/>')
    # face
    p.append('<ellipse cx="262" cy="190" rx="11" ry="20" fill="%s"/>' % BG)
    p.append('<ellipse cx="338" cy="190" rx="11" ry="20" fill="%s"/>' % BG)
    p.append('<path d="M240 232 Q300 284 360 232" fill="none" stroke="%s" stroke-width="8" stroke-linecap="round"/>' % BG)
    p.append('<path d="M232 226 l12 10 M368 226 l-12 10" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % BG)
    # hidden third eye
    p.append('<g class="eye3">'
             '<path d="M274 136 Q300 112 326 136 Q300 160 274 136Z" fill="#f5f5f7" stroke="%s" stroke-width="2.5"/>'
             '<circle cx="300" cy="136" r="9" fill="#ffb547"/>'
             '<circle class="pupil" cx="300" cy="136" r="4.5" fill="%s"/>'
             '</g>' % (BG, BG))
    p.append('</g>')
    # floating eyes
    p.append(_float_eye("float", "lid", 92, 196, 42, -12))
    p.append(_float_eye("float2", "lid l2", 508, 150, 34, 10))
    p.append(_float_eye("float3", "lid l3", 486, 362, 26, -6))
    # white wavy lines
    p.append('<g fill="none" stroke="#f5f5f7" stroke-width="2.2" stroke-linecap="round" stroke-opacity=".8">'
             '<g class="float2"><path d="M30 120 q15 -14 30 0 t30 0 t30 0"/></g>'
             '<g class="float3"><path d="M420 240 q12 -12 24 0 t24 0 t24 0 t24 0"/></g>'
             '<g class="float"><path d="M60 320 q10 -10 20 0 t20 0 t20 0"/></g>'
             '</g>')
    p.append('</svg>')
    return "".join(p)


# ---------------------------------------------------------------- 404 eye

def eye404_svg():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" class="eye" aria-hidden="true">'
        '<defs><radialGradient id="k-e4i" cx=".4" cy=".35" r=".7">'
        '<stop offset="0" stop-color="#fff3a3"/><stop offset=".5" stop-color="#ffd60a"/>'
        '<stop offset="1" stop-color="#ffb547"/></radialGradient>'
        '<filter id="k-e4g" x="-30%" y="-30%" width="160%" height="160%">'
        '<feGaussianBlur stdDeviation="6"/></filter></defs>'
        '<g fill="#f5f5f7">'
        '<circle cx="22" cy="28" r="1.6"/><circle cx="176" cy="22" r="1.3"/><circle cx="186" cy="120" r="1.1"/>'
        '<circle cx="14" cy="140" r="1.2"/><circle cx="150" cy="176" r="1"/><circle cx="96" cy="12" r="1"/>'
        '</g>'
        '<ellipse cx="100" cy="94" rx="80" ry="46" fill="#ff6ad5" fill-opacity=".25" filter="url(#k-e4g)"/>'
        '<g fill="#f5f5f7">'
        '<path d="M70 120 C70 145 64 158 72 164 C80 170 88 160 84 146 C82 136 86 126 90 122Z"/>'
        '<path d="M120 122 C122 140 118 150 124 155 C131 160 138 152 135 140 C133 132 136 126 138 120Z"/>'
        '<circle cx="76" cy="174" r="3.5"/>'
        '</g>'
        '<path d="M24 92 Q100 22 176 92 Q100 162 24 92Z" fill="#f5f5f7" stroke="#050507" stroke-width="3"/>'
        '<circle cx="100" cy="92" r="32" fill="url(#k-e4i)"/>'
        '<circle cx="100" cy="92" r="32" fill="none" stroke="#050507" stroke-opacity=".35" stroke-width="2"/>'
        '<circle class="pupil" cx="100" cy="92" r="14" fill="#050507"/>'
        '<circle cx="90" cy="82" r="4.5" fill="#fff"/>'
        '<path d="M30 70 q10 -9 20 0 t20 0" fill="none" stroke="#f5f5f7" stroke-width="2" stroke-linecap="round" stroke-opacity=".6"/>'
        '</svg>'
    )


# ---------------------------------------------------------------- og image

def og_svg(prs, orgs, avatar_data_uri):
    prs = int(prs)
    orgs = int(orgs)
    href = escape(avatar_data_uri, quote=True)
    grid = []
    for x in range(0, 1201, 60):
        grid.append('<path d="M%d 0V630"/>' % x)
    for y in range(0, 631, 60):
        grid.append('<path d="M0 %dH1200"/>' % y)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        'width="1200" height="630" viewBox="0 0 1200 630">'
        '<defs>'
        '<radialGradient id="k-og-v" cx="900" cy="300" r="420" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#8b7dff" stop-opacity=".38"/><stop offset="1" stop-color="#8b7dff" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="k-og-p" cx="120" cy="620" r="520" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#ff6ad5" stop-opacity=".26"/><stop offset="1" stop-color="#ff6ad5" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="k-og-n" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#8b7dff"/><stop offset=".5" stop-color="#ff6ad5"/><stop offset="1" stop-color="#ffb547"/></linearGradient>'
        '<linearGradient id="k-og-r" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#8b7dff"/><stop offset=".5" stop-color="#ff6ad5"/><stop offset="1" stop-color="#ffb547"/></linearGradient>'
        '<clipPath id="k-og-c"><circle cx="900" cy="300" r="150"/></clipPath>'
        '<filter id="k-og-g" x="-.3" y="-.3" width="1.6" height="1.6"><feGaussianBlur stdDeviation="14"/></filter>'
        '</defs>'
        '<rect width="1200" height="630" fill="#050507"/>'
        '<g stroke="#ffffff" stroke-opacity=".06" stroke-width="1">' + "".join(grid) + '</g>'
        '<rect width="1200" height="630" fill="url(#k-og-v)"/>'
        '<rect width="1200" height="630" fill="url(#k-og-p)"/>'
        '<text x="80" y="196" font-family="Inter" font-weight="800" font-size="68" fill="#f5f5f7" letter-spacing="-2">Alexandre Kohler</text>'
        '<text x="82" y="246" font-family="Inter" font-weight="400" font-size="30" fill="#a1a1aa">Senior Full Stack Software Engineer</text>'
        '<text x="78" y="390" font-family="Inter" font-weight="800">'
        '<tspan font-size="112" fill="url(#k-og-n)" letter-spacing="-4">%d</tspan>'
        '<tspan font-size="34" fill="#f5f5f7" dx="16">merged pull requests</tspan></text>'
        '<text x="82" y="446" font-family="Inter" font-weight="400" font-size="23" fill="#d4d4d8">'
        '%d organizations · Google · Microsoft · Meta · Apple</text>'
        '<text x="82" y="562" font-family="Inter" font-weight="400" font-size="22" fill="#71717a">kwy404.github.io/kwy404</text>'
        '<circle cx="900" cy="300" r="166" fill="none" stroke="url(#k-og-r)" stroke-width="14" filter="url(#k-og-g)"/>'
        '<circle cx="900" cy="300" r="150" fill="#111114"/>'
        '<image href="%s" xlink:href="%s" x="750" y="150" width="300" height="300" '
        'preserveAspectRatio="xMidYMid slice" clip-path="url(#k-og-c)"/>'
        '<circle cx="900" cy="300" r="162" fill="none" stroke="url(#k-og-r)" stroke-width="5"/>'
        # small melting smiley
        '<g transform="translate(1072 492)">'
        '<path d="M-26 8 C-26 30 -30 40 -24 44 C-18 48 -13 40 -16 30 C-17 22 -14 16 -10 14Z" fill="#ffd60a"/>'
        '<path d="M10 16 C12 28 10 34 15 37 C20 40 24 34 22 26 C21 20 23 16 25 12Z" fill="#ffd60a"/>'
        '<circle r="36" fill="#ffd60a"/>'
        '<ellipse cx="-12" cy="-6" rx="4.5" ry="8" fill="#050507"/>'
        '<ellipse cx="12" cy="-6" rx="4.5" ry="8" fill="#050507"/>'
        '<path d="M-18 10 Q0 28 18 10" fill="none" stroke="#050507" stroke-width="4" stroke-linecap="round"/>'
        '</g>'
        '<g fill="#f5f5f7"><circle cx="1110" cy="96" r="2"/><circle cx="720" cy="520" r="1.6"/>'
        '<circle cx="1150" cy="300" r="1.4"/><circle cx="700" cy="110" r="1.4"/></g>'
        '</svg>'
    ) % (prs, orgs, href, href)


if __name__ == "__main__":
    import os
    import xml.etree.ElementTree as ET
    out = "/tmp/claude-0/-root/31506e90-c78c-438a-a6c2-7e1a8f7b6397/scratchpad/art-check/"
    os.makedirs(out, exist_ok=True)
    px = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
          "YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
    for name, svg in (("hero.svg", hero_svg()), ("eye.svg", eye404_svg()), ("og.svg", og_svg(214, 59, px))):
        data = svg.encode("utf-8")
        with open(out + name, "wb") as fh:
            fh.write(data)
        ET.fromstring(data)
        print(name, len(data), "bytes, well-formed")
