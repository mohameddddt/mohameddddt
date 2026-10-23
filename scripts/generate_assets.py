"""Generates the profile README SVG assets (banner, section headers, project covers).

Usage: python scripts/generate_assets.py [output_dir]   # defaults to ./assets
"""
import math
import os
import random
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(os.path.join(OUT, "work"), exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', 'JetBrains Mono', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(bg="#0d1117", card="#111723", ink="#e8ecf4", muted="#8b95a7", line="#232b3b",
                 cyan="#22d3ee", violet="#a78bfa", lime="#a3e635", amber="#fbbf24", rose="#fb7185",
                 chip="#161e2d"),
    "light": dict(bg="#ffffff", card="#f7f6f2", ink="#141821", muted="#5d6577", line="#e2e0d8",
                  cyan="#0891b2", violet="#7c3aed", lime="#4d7c0f", amber="#b45309", rose="#e11d48",
                  chip="#efede6"),
}


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(body.strip() + "\n")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- banner
def banner(mode):
    t = THEMES[mode]
    W, H = 1200, 400
    # small neural net on the right
    cols = [(800, 3), (910, 5), (1020, 5), (1120, 2)]
    nodes = []
    for x, n in cols:
        span = 54 * (n - 1)
        nodes.append([(x, 200 - span / 2 + i * 54) for i in range(n)])
    edges, hot = [], []
    rnd = random.Random(4)
    for a, b in zip(nodes, nodes[1:]):
        for p in a:
            for q in b:
                edges.append((p, q))
    hot_paths = [(0, 1, 2, 0), (2, 3, 1, 1), (1, 0, 4, 0), (0, 4, 3, 1)]
    for path in hot_paths:
        pts = [nodes[i][path[i]] for i in range(4)]
        hot.append(pts)
    accents = [t["cyan"], t["violet"], t["lime"], t["amber"]]

    e_svg = "\n".join(
        f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="{t["line"]}" stroke-width="1.2"/>'
        for p, q in edges)
    h_svg = ""
    for i, pts in enumerate(hot):
        d = "M" + " L".join(f"{x} {y}" for x, y in pts)
        h_svg += (f'<path d="{d}" fill="none" stroke="{accents[i]}" stroke-width="2.2" stroke-linecap="round" '
                  f'stroke-dasharray="14 400" class="flow" style="animation-delay:{i * 0.9}s"/>\n')
        h_svg += f'<path d="{d}" fill="none" stroke="{accents[i]}" stroke-width="1.2" stroke-opacity="0.35"/>\n'
    n_svg = ""
    k = 0
    for ci, col in enumerate(nodes):
        for x, y in col:
            fill = accents[k % 4] if (k * 7) % 3 == 0 else t["card"]
            stroke = accents[k % 4]
            n_svg += (f'<circle cx="{x}" cy="{y}" r="9" fill="{fill}" stroke="{stroke}" stroke-width="2" '
                      f'class="pulse" style="animation-delay:{(k % 5) * 0.6}s"/>\n')
            k += 1

    chips = ["machine learning", "computer vision", "speech & NLP", "full-stack"]
    c_svg, cx = "", 72
    for i, c in enumerate(chips):
        w = len(c) * 9.6 + 30
        c_svg += (f'<rect x="{cx}" y="320" width="{w}" height="34" rx="17" fill="{t["chip"]}" stroke="{t["line"]}"/>'
                  f'<circle cx="{cx + 16}" cy="337" r="4" fill="{accents[i]}"/>'
                  f'<text x="{cx + 27}" y="342" class="mono" font-size="16" fill="{t["ink"]}">{esc(c)}</text>\n')
        cx += w + 10

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Mohamed Sahnoune Toubal, AI engineering student at ENSIA, Algiers.">
<style>
.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
.flow{{animation:flow 3.6s linear infinite}}
@keyframes flow{{from{{stroke-dashoffset:14}}to{{stroke-dashoffset:-430}}}}
.pulse{{animation:pulse 3s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}
.blink{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.flow,.pulse,.blink{{animation:none}}}}
</style>
<defs>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t["line"]}"/></pattern>
  <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{t["card"]}"/><stop offset=".55" stop-color="{t["card"]}" stop-opacity=".2"/><stop offset="1" stop-color="{t["card"]}" stop-opacity="0"/></linearGradient>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="{t["card"]}"/>
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
  <rect width="{W}" height="{H}" fill="url(#fade)"/>
  <rect x="0" y="0" width="{W}" height="5" fill="{t["cyan"]}"/>
  <rect x="300" y="0" width="300" height="5" fill="{t["violet"]}"/>
  <rect x="600" y="0" width="300" height="5" fill="{t["lime"]}"/>
  <rect x="900" y="0" width="300" height="5" fill="{t["amber"]}"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="none" stroke="{t["line"]}"/>

<text x="72" y="78" class="mono" font-size="18" fill="{t["muted"]}"><tspan fill="{t["cyan"]}">~/mohameddddt</tspan> · ENSIA, Algiers<tspan class="blink" fill="{t["cyan"]}"> _</tspan></text>
<text x="70" y="150" class="sans" font-size="68" font-weight="800" letter-spacing="-2" fill="{t["ink"]}">Mohamed</text>
<text x="70" y="222" class="sans" font-size="68" font-weight="800" letter-spacing="-2" fill="{t["ink"]}">Sahnoune Toubal<tspan fill="{t["cyan"]}">.</tspan></text>
<text x="72" y="266" class="sans" font-size="21" fill="{t["muted"]}">AI engineering student. I train models for vision, speech</text>
<text x="72" y="294" class="sans" font-size="21" fill="{t["muted"]}">and language, and build the apps they live in.</text>
{c_svg}
{e_svg}
{h_svg}
{n_svg}
</svg>"""


# ---------------------------------------------------------------- section headers
def header(mode, num, title, accent):
    t = THEMES[mode]
    w = int(52 + len(title) * 14.6 + 66)
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40" role="img" aria-label="{esc(title)}">
<style>.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}</style>
<text x="0" y="29" class="mono" font-size="17" font-weight="600" fill="{t[accent]}">{num}</text>
<text x="32" y="29" class="mono" font-size="17" fill="{t["line"]}">/</text>
<text x="52" y="30" class="sans" font-size="27" font-weight="800" letter-spacing="-.6" fill="{t["ink"]}">{esc(title)}</text>
<rect x="{w - 52}" y="20" width="48" height="3" rx="1.5" fill="{t[accent]}"/>
</svg>"""


# ---------------------------------------------------------------- project covers (one per project, theme-neutral)
CW, CH = 640, 360
DARK = THEMES["dark"]


def cover(slug, label, bg1, bg2, accent, body, tag=""):
    tag_svg = ""
    if tag:
        w = len(tag) * 8.4 + 24
        tag_svg = (f'<rect x="{CW - 24 - w}" y="22" width="{w}" height="26" rx="13" fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".5"/>'
                   f'<text x="{CW - 24 - w / 2}" y="40" text-anchor="middle" class="mono" font-size="13" fill="{accent}">{esc(tag)}</text>')
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}" role="img" aria-label="{esc(label)}">
<style>.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient>
  <pattern id="g" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern>
  <clipPath id="c"><rect width="{CW}" height="{CH}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#c)">
<rect width="{CW}" height="{CH}" fill="url(#bg)"/>
<rect width="{CW}" height="{CH}" fill="url(#g)"/>
<text x="26" y="41" class="mono" font-size="14" fill="#ffffff" fill-opacity=".55">{esc(label)}</text>
{tag_svg}
{body}
</g>
<rect x=".5" y=".5" width="{CW - 1}" height="{CH - 1}" rx="14" fill="none" stroke="#ffffff" stroke-opacity=".08"/>
</svg>"""
    write(f"work/{slug}.svg", svg)


def fpl():
    a, amber = "#a3e635", "#fbbf24"
    # pitch (vertical half-pitch seen from above, attacking upwards)
    px, py, pw, ph = 70, 66, 500, 270
    pitch = f"""
<g fill="none" stroke="{a}" stroke-opacity=".22" stroke-width="2">
  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="4"/>
  <line x1="{px}" y1="{py + ph / 2}" x2="{px + pw}" y2="{py + ph / 2}"/>
  <circle cx="{px + pw / 2}" cy="{py + ph / 2}" r="38"/>
  <rect x="{px + pw / 2 - 90}" y="{py}" width="180" height="46"/>
  <rect x="{px + pw / 2 - 90}" y="{py + ph - 46}" width="180" height="46"/>
</g>"""
    # 3-4-3: rows from top (FWD) to bottom (GK)
    rows = [(3, 98, ["8.1", "6.4", "5.9"]), (4, 160, ["5.2", "7.6", "4.8", "5.0"]),
            (3, 228, ["4.1", "4.6", "3.9"]), (1, 298, ["3.7"])]
    players = ""
    for n, y, pts in rows:
        for i in range(n):
            x = px + pw * (i + 1) / (n + 1)
            cap = pts[i] == "8.1"
            vice = pts[i] == "7.6"
            fill = amber if cap else "#0f1d14"
            players += f'<circle cx="{x}" cy="{y}" r="15" fill="{fill}" stroke="{amber if cap else a}" stroke-width="2.5"/>'
            if cap or vice:
                players += (f'<text x="{x}" y="{y + 5}" text-anchor="middle" class="sans" font-size="14" font-weight="800" '
                            f'fill="{"#1a1405" if cap else a}">{"C" if cap else "V"}</text>')
            players += (f'<rect x="{x + 17}" y="{y - 23}" width="34" height="18" rx="9" fill="#08110b" fill-opacity=".85"/>'
                        f'<text x="{x + 34}" y="{y - 10}" text-anchor="middle" class="mono" font-size="11.5" fill="{amber if cap else "#e8ecf4"}">{pts[i]}</text>')
    cover("fpl-assistant", "fpl-assistant · GW forecast", "#0b1a12", "#13261a", a, pitch + players, "xPts 64.2")


def drone():
    c, v, am, rose = "#22d3ee", "#a78bfa", "#fbbf24", "#fb7185"
    depot = (318, 214)
    routes = [
        (c, [(206, 140), (140, 186), (164, 252), (250, 262)]),
        (v, [(290, 112), (372, 84), (470, 104), (420, 160)]),
        (am, [(470, 262), (540, 232), (548, 300), (410, 316)]),
    ]
    nofly = [(500, 138), (548, 122), (582, 160), (560, 202), (508, 192)]
    poly = " ".join(f"{x},{y}" for x, y in nofly)
    body = f"""
<defs><pattern id="h" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" stroke="{rose}" stroke-opacity=".45" stroke-width="3"/></pattern></defs>
<polygon points="{poly}" fill="url(#h)" stroke="{rose}" stroke-width="2" stroke-dasharray="6 5"/>
<text x="520" y="168" class="mono" font-size="12" fill="{rose}">no-fly</text>"""
    # the violet route detours around the zone; add a waypoint
    for col, pts in routes:
        full = [depot] + pts + [depot]
        d = "M" + " L".join(f"{x} {y}" for x, y in full)
        body += f'<path id="r{col[1:]}" d="{d}" fill="none" stroke="{col}" stroke-width="2.6" stroke-linejoin="round" stroke-opacity=".9"/>'
        for x, y in pts:
            body += f'<circle cx="{x}" cy="{y}" r="7" fill="#0b1420" stroke="{col}" stroke-width="2.5"/>'
        # drone travelling the route
        body += (f'<g><path d="M-7 0H7M0 -7V7" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round"/>'
                 f'<circle r="3.5" fill="{col}"/>'
                 f'<animateMotion dur="{7 + len(pts)}s" repeatCount="indefinite"><mpath href="#r{col[1:]}"/></animateMotion></g>')
    body += (f'<rect x="{depot[0] - 12}" y="{depot[1] - 12}" width="24" height="24" rx="4" fill="#ffffff"/>'
             f'<text x="{depot[0]}" y="{depot[1] + 36}" text-anchor="middle" class="mono" font-size="12" fill="#ffffff" fill-opacity=".7">depot</text>')
    # battery legend
    body += f"""
<g transform="translate(26 300)" class="mono" font-size="12" fill="#ffffff" fill-opacity=".7">
  <text y="0">energy ∝ distance × (mass + load)</text>
  <text y="20">B&amp;B · GA · SA · ALNS</text>
</g>"""
    cover("drone-delivery", "drp solve city.json --method alns", "#0a1220", "#111a2e", c, body, "gap 0.0%")


def ser():
    rose, v, am, cy = "#fb7185", "#a78bfa", "#fbbf24", "#22d3ee"
    rnd = random.Random(7)
    segs = [(40, 200, cy, "neutral"), (200, 390, rose, "angry"), (390, 600, am, "happy")]
    bars = ""
    x = 40
    i = 0
    while x < 600:
        env = 0.25 + 0.75 * abs(math.sin(x / 47)) * (0.6 + 0.4 * math.sin(x / 13))
        if 200 <= x < 390:
            env *= 1.25
        h = max(4, min(120, env * 110 * (0.55 + 0.45 * rnd.random())))
        col = next(s[2] for s in segs if s[0] <= x < s[1])
        bars += f'<rect x="{x}" y="{150 - h / 2}" width="4" height="{h:.1f}" rx="2" fill="{col}" fill-opacity=".9"/>'
        x += 7
        i += 1
    lbl = ""
    for s, e, col, name in segs:
        lbl += (f'<line x1="{s}" y1="78" x2="{e - 8}" y2="78" stroke="{col}" stroke-width="2"/>'
                f'<text x="{s}" y="70" class="mono" font-size="12.5" fill="{col}">{name}</text>')
    probs = [("angry", .89, rose), ("neutral", .04, cy), ("fear", .03, v), ("disgust", .02, "#94a3b8"),
             ("sad", .01, "#60a5fa"), ("happy", .01, am)]
    pb = ""
    for k, (name, p, col) in enumerate(probs):
        xx = 40 + k * 95
        pb += (f'<text x="{xx}" y="258" class="mono" font-size="12" fill="#ffffff" fill-opacity=".7">{name}</text>'
               f'<rect x="{xx}" y="268" width="82" height="8" rx="4" fill="#ffffff" fill-opacity=".08"/>'
               f'<rect x="{xx}" y="268" width="{max(3, 82 * p):.1f}" height="8" rx="4" fill="{col}"/>'
               f'<text x="{xx}" y="300" class="mono" font-size="13" fill="{col if k == 0 else "#ffffff"}" fill-opacity="{1 if k == 0 else .5}">{p:.2f}</text>')
    play = (f'<line x1="40" y1="88" x2="40" y2="212" stroke="#ffffff" stroke-width="1.5" stroke-opacity=".7">'
            f'<animate attributeName="x1" values="40;600" dur="6s" repeatCount="indefinite"/>'
            f'<animate attributeName="x2" values="40;600" dur="6s" repeatCount="indefinite"/></line>')
    cover("speech-emotion", "WavLM layers 5-9 → logistic regression", "#170e1a", "#21122a", rose, lbl + bars + play + pb, "acc 0.742")


def plag():
    am, rose = "#fbbf24", "#fb7185"
    rnd = random.Random(3)

    def doc(x0, title, marks):
        out = (f'<rect x="{x0}" y="64" width="232" height="266" rx="10" fill="#ffffff" fill-opacity=".04" stroke="#ffffff" stroke-opacity=".1"/>'
               f'<text x="{x0 + 16}" y="88" class="mono" font-size="12" fill="#ffffff" fill-opacity=".6">{title}</text>')
        ys = []
        for i in range(12):
            y = 106 + i * 18
            w = 200 - rnd.random() * 60 if i % 4 != 3 else 110
            hit = i in marks
            out += f'<rect x="{x0 + 16}" y="{y}" width="{w:.0f}" height="7" rx="3.5" fill="{am if hit else "#ffffff"}" fill-opacity="{0.9 if hit else 0.16}"/>'
            if hit:
                out += f'<rect x="{x0 + 10}" y="{y - 5}" width="{w + 12:.0f}" height="17" rx="4" fill="{am}" fill-opacity=".12"/>'
                ys.append(y + 3.5)
        return out, ys

    left, ly = doc(40, "submission.docx", [2, 3, 7, 8, 9])
    right, ry = doc(368, "source · arXiv", [1, 2, 9, 10, 11])
    links = ""
    for a_, b_ in [(ly[0], ry[0]), (ly[1], ry[1]), (ly[2], ry[2]), (ly[3], ry[3]), (ly[4], ry[4])]:
        links += f'<path d="M272 {a_} C320 {a_} 320 {b_} 368 {b_}" fill="none" stroke="{am}" stroke-opacity=".55" stroke-width="1.6"/>'
    badge = (f'<rect x="240" y="318" width="160" height="30" rx="15" fill="#120f07" stroke="{am}" stroke-opacity=".6"/>'
             f'<text x="320" y="338" text-anchor="middle" class="mono" font-size="12.5" fill="{am}">0.81 · needs review</text>')
    cover("plagiarism", "", "#15120a", "#1f190d", am, left + right + links + badge)


def rag():
    v, cy, lime = "#a78bfa", "#22d3ee", "#a3e635"
    rnd = random.Random(11)
    pts = ""
    q = (250, 190)
    near = []
    for i in range(70):
        ang = rnd.random() * 2 * math.pi
        r = 20 + rnd.random() * 120
        x, y = 250 + math.cos(ang) * r * 1.35, 195 + math.sin(ang) * r * 0.95
        if not (40 < x < 470 and 70 < y < 330):
            continue
        d = math.hypot(x - q[0], y - q[1])
        if d < 52 and len(near) < 3:
            near.append((x, y))
            continue
        pts += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#ffffff" fill-opacity=".22"/>'
    while len(near) < 3:
        near.append((q[0] + 30 * math.cos(len(near) * 2.1), q[1] + 30 * math.sin(len(near) * 2.1)))
    hl = f'<circle cx="{q[0]}" cy="{q[1]}" r="56" fill="{v}" fill-opacity=".07" stroke="{v}" stroke-opacity=".4" stroke-dasharray="4 4"/>'
    for k, (x, y) in enumerate(near):
        hl += (f'<line x1="{q[0]}" y1="{q[1]}" x2="{x:.1f}" y2="{y:.1f}" stroke="{v}" stroke-opacity=".6"/>'
               f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{cy}"/>'
               f'<text x="{q[0] + (x - q[0]) * 1.9 - 9:.1f}" y="{q[1] + (y - q[1]) * 1.9 + 4:.1f}" class="mono" font-size="11" fill="{cy}">[{k + 1}]</text>')
    hl += f'<path d="M{q[0]} {q[1] - 9} L{q[0] + 3} {q[1] - 3} L{q[0] + 9} {q[1]} L{q[0] + 3} {q[1] + 3} L{q[0]} {q[1] + 9} L{q[0] - 3} {q[1] + 3} L{q[0] - 9} {q[1]} L{q[0] - 3} {q[1] - 3}Z" fill="{v}"/>'
    hl += f'<text x="{q[0] - 34}" y="{q[1] + 76}" class="mono" font-size="11.5" fill="{v}">query · MedCPT</text>'
    card = f"""
<g transform="translate(400 92)">
  <rect width="214" height="210" rx="10" fill="#0d0b18" fill-opacity=".85" stroke="{v}" stroke-opacity=".35"/>
  <text x="16" y="28" class="mono" font-size="12" fill="{v}">answer</text>
  <rect x="16" y="44" width="176" height="7" rx="3.5" fill="#ffffff" fill-opacity=".55"/>
  <rect x="16" y="60" width="150" height="7" rx="3.5" fill="#ffffff" fill-opacity=".55"/>
  <rect x="172" y="57" width="26" height="14" rx="4" fill="{cy}" fill-opacity=".2"/><text x="185" y="68" text-anchor="middle" class="mono" font-size="10" fill="{cy}">1</text>
  <rect x="16" y="76" width="182" height="7" rx="3.5" fill="#ffffff" fill-opacity=".55"/>
  <rect x="16" y="92" width="96" height="7" rx="3.5" fill="#ffffff" fill-opacity=".55"/>
  <rect x="118" y="89" width="26" height="14" rx="4" fill="{cy}" fill-opacity=".2"/><text x="131" y="100" text-anchor="middle" class="mono" font-size="10" fill="{cy}">3</text>
  <line x1="16" x2="198" y1="122" y2="122" stroke="#ffffff" stroke-opacity=".1"/>
  <text x="16" y="146" class="mono" font-size="11" fill="#ffffff" fill-opacity=".55">sources</text>
  <text x="16" y="168" class="mono" font-size="11" fill="{cy}">[1] PMID 2134···</text>
  <text x="16" y="186" class="mono" font-size="11" fill="{cy}">[3] PMID 2580···</text>
</g>"""
    cover("medical-rag", "pgvector · top-k = 3", "#100d1d", "#1a1430", v, pts + hl + card)


def amc():
    cy, v, lime = "#22d3ee", "#a78bfa", "#a3e635"
    rnd = random.Random(5)
    cx0, cy0, s = 200, 196, 34
    axes = (f'<line x1="{cx0 - 150}" y1="{cy0}" x2="{cx0 + 150}" y2="{cy0}" stroke="#ffffff" stroke-opacity=".2"/>'
            f'<line x1="{cx0}" y1="{cy0 - 140}" x2="{cx0}" y2="{cy0 + 140}" stroke="#ffffff" stroke-opacity=".2"/>'
            f'<text x="{cx0 + 140}" y="{cy0 - 8}" class="mono" font-size="12" fill="#ffffff" fill-opacity=".5">I</text>'
            f'<text x="{cx0 + 8}" y="{cy0 - 128}" class="mono" font-size="12" fill="#ffffff" fill-opacity=".5">Q</text>')
    pts = ""
    for i in (-3, -1, 1, 3):
        for q in (-3, -1, 1, 3):
            for _ in range(16):
                x = cx0 + (i + rnd.gauss(0, .2)) * s
                y = cy0 - (q + rnd.gauss(0, .2)) * s
                pts += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.3" fill="{cy}" fill-opacity=".75"/>'
    classes = [("8PSK", .01), ("AM-DSB", .00), ("BPSK", .00), ("CPFSK", .00), ("GFSK", .00), ("PAM4", .02),
               ("QAM16", .91), ("QAM64", .05), ("QPSK", .01), ("WBFM", .00), ("AM-SSB", .00)]
    lst = ""
    for k, (name, p) in enumerate(classes):
        y = 74 + k * 24
        hit = name == "QAM16"
        lst += (f'<text x="400" y="{y + 4}" class="mono" font-size="12" fill="{lime if hit else "#ffffff"}" fill-opacity="{1 if hit else .5}">{name}</text>'
                f'<rect x="470" y="{y - 5}" width="120" height="8" rx="4" fill="#ffffff" fill-opacity=".07"/>'
                f'<rect x="470" y="{y - 5}" width="{max(2, 120 * p):.1f}" height="8" rx="4" fill="{lime if hit else cy}" fill-opacity="{1 if hit else .6}"/>')
    lst += f'<text x="400" y="352" class="mono" font-size="11" fill="#ffffff" fill-opacity=".45">SNR +18 dB · 128 I/Q samples</text>'
    cover("amc", "RadioML 2016.10A", "#071518", "#0c2025", cy, axes + pts + lst)


def cadence():
    am, rose = "#fbbf24", "#fb7185"
    rec_c = (178, 196)
    grooves = "".join(f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="#ffffff" stroke-opacity="{.05 + (r % 3) * .02}"/>' for r in range(48, 128, 6))
    record = f"""
<g transform="translate({rec_c[0]} {rec_c[1]})">
  <circle r="130" fill="#0c0708"/>
  <g>{grooves}
    <path d="M0 -122 A122 122 0 0 1 86 -86" fill="none" stroke="#ffffff" stroke-opacity=".25" stroke-width="3"/>
    <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="6s" repeatCount="indefinite"/>
  </g>
  <circle r="42" fill="{am}"/>
  <circle r="42" fill="url(#lbl)"/>
  <circle r="5" fill="#0c0708"/>
</g>
<defs><radialGradient id="lbl"><stop offset=".5" stop-color="{rose}" stop-opacity="0"/><stop offset="1" stop-color="{rose}" stop-opacity=".6"/></radialGradient></defs>"""
    rnd = random.Random(9)
    eq = ""
    for i in range(14):
        x = 352 + i * 18
        lo, hi = 20 + rnd.random() * 20, 60 + rnd.random() * 70
        dur = 0.9 + rnd.random() * 0.8
        eq += (f'<rect x="{x}" y="{226 - hi}" width="11" height="{hi}" rx="3" fill="{am if i % 3 else rose}">'
               f'<animate attributeName="height" values="{hi:.0f};{lo:.0f};{hi:.0f}" dur="{dur:.2f}s" repeatCount="indefinite"/>'
               f'<animate attributeName="y" values="{226 - hi:.0f};{226 - lo:.0f};{226 - hi:.0f}" dur="{dur:.2f}s" repeatCount="indefinite"/></rect>')
    lyr = (f'<text x="352" y="268" class="sans" font-size="16" font-weight="700" fill="#ffffff">and the night keeps <tspan fill="{am}">time</tspan></text>'
           f'<text x="352" y="292" class="sans" font-size="14" fill="#ffffff" fill-opacity=".4">with every song we play</text>'
           f'<rect x="352" y="314" width="250" height="4" rx="2" fill="#ffffff" fill-opacity=".1"/>'
           f'<rect x="352" y="314" width="150" height="4" rx="2" fill="{am}"/><circle cx="502" cy="316" r="6" fill="#ffffff"/>')
    cover("cadence", "Cadence · your music, in rhythm", "#1a0d10", "#2a1418", am, record + eq + lyr, "FLAC · 24/96")


def streamline():
    v, cy, rose = "#a78bfa", "#22d3ee", "#fb7185"
    frame = f"""
<rect x="40" y="62" width="560" height="200" rx="12" fill="#06070f" stroke="#ffffff" stroke-opacity=".08"/>
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{v}" stop-opacity=".35"/><stop offset="1" stop-color="{cy}" stop-opacity=".05"/></linearGradient></defs>
<rect x="40" y="62" width="560" height="200" rx="12" fill="url(#sky)"/>
<path d="M40 222 L150 160 L230 200 L330 130 L440 196 L520 160 L600 204 V262 H40Z" fill="#06070f" fill-opacity=".7"/>
<circle cx="320" cy="162" r="30" fill="#ffffff" fill-opacity=".12" stroke="#ffffff" stroke-opacity=".5"/>
<path d="M311 148 L336 162 L311 176Z" fill="#ffffff"/>"""
    # piece map under the player: in-order streaming fills from the left, with some pieces ahead
    rnd = random.Random(2)
    pieces = ""
    n = 56
    for i in range(n):
        x = 40 + i * 10
        if i < 24:
            col, op = v, .95
        elif i < 30 or rnd.random() < .18:
            col, op = cy, .8
        else:
            col, op = "#ffffff", .1
        pieces += f'<rect x="{x}" y="284" width="8" height="18" rx="2" fill="{col}" fill-opacity="{op}"/>'
    head = f'<rect x="276" y="278" width="2.5" height="30" rx="1" fill="#ffffff"/>'
    legend = (f'<g class="mono" font-size="12"><circle cx="46" cy="328" r="4" fill="{v}"/><text x="56" y="332" fill="#ffffff" fill-opacity=".6">played</text>'
              f'<circle cx="126" cy="328" r="4" fill="{cy}"/><text x="136" y="332" fill="#ffffff" fill-opacity=".6">buffered</text>'
              f'<text x="600" y="332" text-anchor="end" fill="#ffffff" fill-opacity=".6">12.4 MB/s · 38 peers</text></g>')
    cover("streamline", "stream://tt0000001", "#0b0c1c", "#141634", v, frame + pieces + head + legend)


for mode in ("dark", "light"):
    write(f"banner-{mode}.svg", banner(mode))
    for slug, num, title, acc in [("work", "01", "Selected work", "cyan"), ("toolbox", "02", "Toolbox", "violet"),
                                  ("activity", "03", "Activity", "lime"), ("hello", "04", "Say hello.", "amber")]:
        write(f"h-{slug}-{mode}.svg", header(mode, num, title, acc))

fpl(); drone(); ser(); plag(); rag(); amc(); cadence(); streamline()
print("ok")
