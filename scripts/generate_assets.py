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


def eo_bench():
    teal, lime, am, rose = "#2dd4bf", "#a3e635", "#fbbf24", "#fb7185"
    rnd = random.Random(21)
    # a strip of Sentinel-2-like tiles: forest, crop, water, urban, ...
    land = ["#1f5f3a", "#3f7a2c", "#8a7a3a", "#1d4e6e", "#6b6f78", "#2f6f4f", "#9a8452", "#25587a"]
    tiles = ""
    for r in range(5):
        for c in range(6):
            x, y = 36 + c * 46, 70 + r * 46
            tiles += f'<rect x="{x}" y="{y}" width="42" height="42" rx="5" fill="{land[rnd.randrange(len(land))]}"/>'
            for _ in range(3):
                tiles += (f'<rect x="{x + rnd.random() * 30:.1f}" y="{y + rnd.random() * 30:.1f}" width="{4 + rnd.random() * 10:.1f}" '
                          f'height="{3 + rnd.random() * 8:.1f}" rx="2" fill="#ffffff" fill-opacity="{.05 + rnd.random() * .12:.2f}"/>')
    # a haze band sweeping the tiles, standing in for the EuroSAT-C corruptions
    tiles += (f'<rect x="36" y="70" width="272" height="226" fill="#ffffff" fill-opacity=".08">'
              f'<animate attributeName="width" values="0;272;0" dur="7s" repeatCount="indefinite"/></rect>'
              f'<text x="36" y="320" class="mono" font-size="12" fill="#ffffff" fill-opacity=".6">haze · noise · band shift · blur</text>')
    # leaderboard with 95% CIs
    rows = [("ViT-S/16", 69.56, 68.86, 70.19, teal), ("ConvNeXt-T", 66.48, 65.65, 67.23, lime),
            ("EfficientNet-B0", 53.63, 52.81, 54.35, am), ("ResNet-50", 44.92, 43.86, 45.96, rose)]
    lb = '<text x="340" y="82" class="mono" font-size="12" fill="#ffffff" fill-opacity=".55">EuroSAT-C · mCA [95% CI]</text>'
    x0, x1, lo_v, hi_v = 340, 604, 40, 75

    def sx(val):
        return x0 + (val - lo_v) / (hi_v - lo_v) * (x1 - x0)

    for k, (name, m, lo, hi, col) in enumerate(rows):
        y = 112 + k * 50
        lb += (f'<text x="{x0}" y="{y}" class="mono" font-size="12.5" fill="#ffffff" fill-opacity="{1 if k == 0 else .7}">{name}</text>'
               f'<text x="{x1}" y="{y}" text-anchor="end" class="mono" font-size="12.5" fill="{col}">{m:.2f}</text>'
               f'<rect x="{x0}" y="{y + 10}" width="{x1 - x0}" height="6" rx="3" fill="#ffffff" fill-opacity=".06"/>'
               f'<rect x="{x0}" y="{y + 10}" width="{sx(m) - x0:.1f}" height="6" rx="3" fill="{col}" fill-opacity=".85"/>'
               f'<path d="M{sx(lo):.1f} {y + 20}v8M{sx(lo):.1f} {y + 24}H{sx(hi):.1f}M{sx(hi):.1f} {y + 20}v8" fill="none" stroke="{col}" stroke-width="2"/>')
    lb += '<text x="340" y="320" class="mono" font-size="12" fill="#ffffff" fill-opacity=".6">5 benchmarks · hidden splits</text>'
    cover("eo-bench", "eo-bench · leaderboard", "#06171a", "#0b2226", teal, tiles + lb, "hidden split")


def savepoint():
    ember = "#fb923c"
    star = "M10 0 L13 7 L20 7.6 L14.6 12.2 L16.4 19.4 L10 15.4 L3.6 19.4 L5.4 12.2 L0 7.6 L7 7Z"
    covers = [("#7c2d12", "#fb923c", 5), ("#312e81", "#a78bfa", 4.5), ("#164e63", "#22d3ee", 4),
              ("#3f6212", "#a3e635", 3.5), ("#831843", "#fb7185", 5), ("#78350f", "#fbbf24", 4)]
    shelf = (f'<defs><linearGradient id="half"><stop offset=".5" stop-color="{ember}"/>'
             f'<stop offset=".5" stop-color="#ffffff" stop-opacity=".15"/></linearGradient></defs>')
    for k, (c1, c2, stars) in enumerate(covers):
        x, y = 36 + (k % 3) * 92, 68 + (k // 3) * 136
        shelf += (f'<defs><linearGradient id="cv{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c2}"/>'
                  f'<stop offset="1" stop-color="{c1}"/></linearGradient></defs>'
                  f'<rect x="{x}" y="{y}" width="80" height="106" rx="7" fill="url(#cv{k})"/>'
                  f'<path d="M{x} {y + 78} L{x + 26} {y + 56} L{x + 44} {y + 70} L{x + 62} {y + 50} L{x + 80} {y + 66} '
                  f'V{y + 99} a7 7 0 0 1 -7 7 H{x + 7} a7 7 0 0 1 -7 -7Z" fill="#000000" fill-opacity=".28"/>')
        for i in range(5):
            fill, op = (ember, 1) if i + 1 <= stars else (("url(#half)", 1) if i + .5 == stars else ("#ffffff", .15))
            shelf += f'<path transform="translate({x + 4 + i * 15} {y + 116}) scale(.6)" d="{star}" fill="{fill}" fill-opacity="{op}"/>'
    # yearly goal ring
    cx, cy0, r = 420, 140, 52
    circ = 2 * math.pi * r
    ring = (f'<circle cx="{cx}" cy="{cy0}" r="{r}" fill="none" stroke="#ffffff" stroke-opacity=".08" stroke-width="10"/>'
            f'<circle cx="{cx}" cy="{cy0}" r="{r}" fill="none" stroke="{ember}" stroke-width="10" stroke-linecap="round" '
            f'stroke-dasharray="{circ * .68:.1f} {circ:.1f}" transform="rotate(-90 {cx} {cy0})">'
            f'<animate attributeName="stroke-dasharray" values="0 {circ:.1f};{circ * .68:.1f} {circ:.1f}" dur="2.4s"/></circle>'
            f'<text x="{cx}" y="{cy0 + 4}" text-anchor="middle" class="sans" font-size="26" font-weight="800" fill="#ffffff">34</text>'
            f'<text x="{cx}" y="{cy0 + 22}" text-anchor="middle" class="mono" font-size="11" fill="#ffffff" fill-opacity=".55">of 50</text>')
    # play-session timer
    timer = (f'<rect x="496" y="96" width="118" height="88" rx="10" fill="#ffffff" fill-opacity=".05" stroke="{ember}" stroke-opacity=".35"/>'
             f'<circle cx="512" cy="116" r="4" fill="{ember}"><animate attributeName="fill-opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>'
             f'<text x="522" y="120" class="mono" font-size="11" fill="#ffffff" fill-opacity=".6">playing</text>'
             f'<text x="508" y="152" class="mono" font-size="20" font-weight="700" fill="#ffffff">01:42</text>'
             f'<text x="508" y="172" class="mono" font-size="11" fill="#ffffff" fill-opacity=".45">session</text>')
    # activity heatmap
    rnd = random.Random(14)
    heat = '<text x="368" y="232" class="mono" font-size="11" fill="#ffffff" fill-opacity=".55">activity · 2026</text>'
    for c in range(18):
        for rr in range(5):
            val = rnd.random()
            op = .07 if val < .35 else (.3 if val < .6 else (.6 if val < .85 else 1))
            heat += f'<rect x="{368 + c * 13.6:.1f}" y="{244 + rr * 13}" width="10.5" height="10" rx="2.5" fill="{ember}" fill-opacity="{op}"/>'
    cover("savepoint", "Savepoint · game diary", "#150d14", "#22131c", ember, shelf + ring + timer + heat, "IGDB · Xbox")


def lumen():
    coral, paper = "#ff7a59", "#f4efe6"
    serif = "Georgia, 'Times New Roman', serif"
    rnd = random.Random(8)
    hues = [("#ffb199", "#c2593f"), ("#a7c4b5", "#3e6b5a"), ("#9fbfd9", "#335d80"), ("#f1cf8f", "#a7742a"),
            ("#e8a7b6", "#93465a"), ("#c9c3b6", "#5a554c")]
    grid = (f'<text x="36" y="96" font-family="{serif}" font-size="34" font-style="italic" fill="{paper}">October</text>'
            f'<text x="182" y="96" class="mono" font-size="11" fill="{paper}" fill-opacity=".5">142 photos · 6 videos</text>')
    # masonry of photos, each a little landscape
    cols = [(36, [84, 64, 70]), (142, [60, 92, 66]), (248, [78, 72, 70]), (354, [66, 84, 74]), (460, [90, 60, 70])]
    k = 0
    for x, hs in cols:
        y = 112
        for h in hs:
            if y + h > 292:
                break
            top, bot = hues[k % len(hues)]
            k += 1
            grid += (f'<defs><linearGradient id="p{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
                     f'<stop offset="1" stop-color="{bot}"/></linearGradient></defs>'
                     f'<rect x="{x}" y="{y}" width="98" height="{h}" rx="8" fill="url(#p{k})"/>'
                     f'<path d="M{x} {y + h * .72:.0f} Q{x + 30} {y + h * .45:.0f} {x + 52} {y + h * .64:.0f} T{x + 98} {y + h * .56:.0f} '
                     f'V{y + h - 8} a8 8 0 0 1 -8 8 H{x + 8} a8 8 0 0 1 -8 -8Z" fill="#000000" fill-opacity=".22"/>'
                     f'<circle cx="{x + 72}" cy="{y + h * .3:.0f}" r="{5 + rnd.random() * 5:.1f}" fill="#ffffff" fill-opacity=".55"/>')
            if k == 7:  # a locked hidden folder
                grid += (f'<rect x="{x}" y="{y}" width="98" height="{h}" rx="8" fill="#140f0d" fill-opacity=".72"/>'
                         f'<rect x="{x + 41}" y="{y + h / 2 - 2:.0f}" width="16" height="13" rx="3" fill="none" stroke="{paper}" stroke-width="1.8"/>'
                         f'<path d="M{x + 44} {y + h / 2 - 2:.0f} v-4 a5 5 0 0 1 10 0 v4" fill="none" stroke="{paper}" stroke-width="1.8"/>')
            if k == 2:  # a favourite
                grid += f'<path transform="translate({x + 8} {y + 8}) scale(.7)" d="M10 17 L2.5 9.5 A4.5 4.5 0 0 1 10 3.5 A4.5 4.5 0 0 1 17.5 9.5Z" fill="{coral}"/>'
            y += h + 8
    # floating frosted dock
    dock = (f'<rect x="150" y="304" width="300" height="40" rx="20" fill="#2a211e" fill-opacity=".9" stroke="{paper}" stroke-opacity=".14"/>'
            f'<rect x="162" y="312" width="76" height="24" rx="12" fill="{coral}"/>'
            f'<text x="200" y="328" text-anchor="middle" class="sans" font-size="12" font-weight="700" fill="#1a1210">Photos</text>'
            f'<text x="282" y="328" text-anchor="middle" class="sans" font-size="12" fill="{paper}" fill-opacity=".7">Albums</text>'
            f'<text x="348" y="328" text-anchor="middle" class="sans" font-size="12" fill="{paper}" fill-opacity=".7">Search</text>'
            f'<text x="412" y="328" text-anchor="middle" class="sans" font-size="12" fill="{paper}" fill-opacity=".7">Bin</text>')
    side = ""
    for i, (name, col) in enumerate([("Coral", coral), ("Sage", "#8fb39e"), ("Ocean", "#7fa6c9"), ("Amber", "#e3b45f")]):
        side += f'<circle cx="{486 + i * 38}" cy="324" r="7" fill="{col}" stroke="{paper}" stroke-opacity="{.8 if i == 0 else 0}" stroke-width="2"/>'
    cover("lumen", "Lumen · gallery", "#1b1513", "#261d1a", coral, grid + dock + side, "Compose")


def mytube():
    rose, cy, lime = "#fb7185", "#22d3ee", "#a3e635"
    player = f"""
<rect x="36" y="66" width="352" height="198" rx="12" fill="#07080d" stroke="#ffffff" stroke-opacity=".08"/>
<defs><linearGradient id="vid" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{rose}" stop-opacity=".35"/><stop offset="1" stop-color="{cy}" stop-opacity=".12"/></linearGradient></defs>
<rect x="36" y="66" width="352" height="198" rx="12" fill="url(#vid)"/>
<circle cx="150" cy="150" r="46" fill="#ffffff" fill-opacity=".06"/><circle cx="270" cy="180" r="64" fill="#ffffff" fill-opacity=".05"/>
<rect x="52" y="236" width="320" height="4" rx="2" fill="#ffffff" fill-opacity=".18"/>
<rect x="52" y="236" width="200" height="4" rx="2" fill="#ffffff" fill-opacity=".35"/>
<rect x="52" y="236" width="128" height="4" rx="2" fill="{rose}"><animate attributeName="width" values="40;300;40" dur="12s" repeatCount="indefinite"/></rect>
<path d="M54 252 l8 5 l-8 5Z" fill="#ffffff" fill-opacity=".8"/>
<text x="74" y="261" class="mono" font-size="11" fill="#ffffff" fill-opacity=".6">6:12 / 14:03</text>
<rect x="290" y="78" width="86" height="22" rx="11" fill="#000000" fill-opacity=".45"/>
<text x="333" y="93" text-anchor="middle" class="mono" font-size="11" fill="#ffffff" fill-opacity=".75">1080p · 1.25×</text>
<text x="36" y="292" class="mono" font-size="11" fill="#ffffff" fill-opacity=".45">k play · j/l 10 s · f full screen · m mute</text>"""
    dl = '<text x="412" y="82" class="mono" font-size="12" fill="#ffffff" fill-opacity=".55">downloads → Videos\\yt</text>'
    items = [("Lecture 07 · Optimisation", "720p", 1.0, lime), ("Live set · 2 h", "MP3", .62, rose),
             ("Playlist · 18 videos", "480p", .28, cy), ("Talk · WSL2 tips", "1080p", 0, "#94a3b8")]
    for k, (name, fmt, p, col) in enumerate(items):
        y = 106 + k * 52
        dl += (f'<rect x="412" y="{y - 12}" width="200" height="42" rx="8" fill="#ffffff" fill-opacity=".04" stroke="#ffffff" stroke-opacity=".07"/>'
               f'<text x="424" y="{y + 4}" class="sans" font-size="12.5" fill="#ffffff" fill-opacity=".85">{esc(name)}</text>'
               f'<text x="600" y="{y + 4}" text-anchor="end" class="mono" font-size="11" fill="{col}">{fmt}</text>'
               f'<rect x="424" y="{y + 14}" width="176" height="4" rx="2" fill="#ffffff" fill-opacity=".08"/>')
        if p:
            dl += f'<rect x="424" y="{y + 14}" width="{176 * p:.0f}" height="4" rx="2" fill="{col}"/>'
    dl += '<text x="412" y="320" class="mono" font-size="11" fill="#ffffff" fill-opacity=".45">127.0.0.1 only · 1.3 MB Rust exe</text>'
    cover("mytube", "localhost:8080 · My Tube", "#120b10", "#1d1119", rose, player + dl, "0 MB idle")


def feather_pdf():
    teal, paper = "#2dd4bf", "#f5f5f4"
    # a reader window: contents sidebar on the left, a page with highlighted matches on the right
    win = (f'<rect x="36" y="64" width="360" height="262" rx="12" fill="#0b1211" stroke="#ffffff" stroke-opacity=".08"/>'
           f'<rect x="36" y="64" width="360" height="30" rx="12" fill="#ffffff" fill-opacity=".04"/>'
           f'<rect x="250" y="72" width="128" height="15" rx="7.5" fill="#ffffff" fill-opacity=".06" stroke="{teal}" stroke-opacity=".5"/>'
           f'<text x="260" y="83" class="mono" font-size="9.5" fill="{teal}">match · 3 of 12</text>'
           f'<text x="50" y="84" class="mono" font-size="10" fill="#ffffff" fill-opacity=".55">p. 214 / 541 · 110%</text>')
    toc = ["Contents", "1  Reading", "2  Finding", "3  Copying", "4  Light"]
    for k, item in enumerate(toc):
        win += (f'<rect x="44" y="{106 + k * 26}" width="92" height="20" rx="5" fill="{teal}" fill-opacity="{.16 if k == 2 else 0}"/>'
                f'<text x="52" y="{120 + k * 26}" class="sans" font-size="11" fill="#ffffff" fill-opacity="{.85 if k in (0, 2) else .5}">{item}</text>')
    win += f'<rect x="148" y="104" width="236" height="210" rx="4" fill="{paper}"/>'
    rnd = random.Random(3)
    for r in range(13):
        y = 120 + r * 14.5
        w = 200 if r % 5 != 4 else 120
        win += f'<rect x="162" y="{y:.1f}" width="{w}" height="5" rx="2.5" fill="#1c1917" fill-opacity=".28"/>'
        if r in (2, 7, 10):
            x = 170 + rnd.random() * 110
            win += (f'<rect x="{x:.0f}" y="{y - 3:.1f}" width="34" height="11" rx="2" fill="{"#fb923c" if r == 7 else "#facc15"}" fill-opacity=".85">'
                    f'<animate attributeName="fill-opacity" values=".85;.35;.85" dur="2.6s" begin="{r * .2:.1f}s" repeatCount="indefinite"/></rect>')
    # memory with a 541-page textbook, from the README
    mem = '<text x="420" y="84" class="mono" font-size="12" fill="#ffffff" fill-opacity=".55">memory · 541-page book</text>'
    for k, (label, mb, col, prefix) in enumerate([("after opening", 16, teal, "≈ "), ("page cache budget", 32, "#5eead4", ""),
                                                   ("while reading", 70, "#99f6e4", "&lt; ")]):
        y = 108 + k * 58
        w = 182 * mb / 70
        mem += (f'<text x="420" y="{y}" class="sans" font-size="12.5" fill="#ffffff" fill-opacity=".85">{label}</text>'
                f'<text x="602" y="{y}" text-anchor="end" class="mono" font-size="11" fill="{col}">{prefix}{mb} MB</text>'
                f'<rect x="420" y="{y + 10}" width="182" height="8" rx="4" fill="#ffffff" fill-opacity=".07"/>'
                f'<rect x="420" y="{y + 10}" width="{w:.0f}" height="8" rx="4" fill="{col}">'
                f'<animate attributeName="width" values="0;{w:.0f}" dur="1.6s"/></rect>')
    mem += ('<text x="420" y="300" class="mono" font-size="11" fill="#ffffff" fill-opacity=".45">only visible pages rendered</text>'
            '<text x="420" y="318" class="mono" font-size="11" fill="#ffffff" fill-opacity=".45">0.8 MB exe · Win32 + GDI</text>')
    cover("feather-pdf", "Feather PDF · reader", "#0a1312", "#10201d", teal, win + mem, "16 MB")


def almanac():
    paper, ink, red, gold = "#f3ece0", "#211d18", "#c2553b", "#c79a2c"
    serif = "Georgia, 'Times New Roman', serif"
    # the Today page as a paper card
    day = (f'<rect x="36" y="64" width="268" height="262" rx="18" fill="{paper}"/>'
           f'<text x="56" y="94" class="mono" font-size="10" letter-spacing="2" fill="{red}">QUIET HOURS</text>'
           f'<text x="56" y="132" font-family="{serif}" font-size="36" font-weight="700" fill="{ink}">Monday</text>'
           f'<text x="56" y="152" class="sans" font-size="11.5" fill="{ink}" fill-opacity=".55">9 November · week 46</text>'
           f'<text x="56" y="214" font-family="{serif}" font-size="54" font-weight="700" fill="{ink}">09:41</text>'
           f'<text x="226" y="214" font-family="{serif}" font-size="20" fill="{gold}">30</text>')
    for k, (label, p, col) in enumerate([("DAY", .4, red), ("WEEK", .08, "#6b8f71"), ("YEAR", .85, gold)]):
        x = 56 + k * 80
        day += (f'<text x="{x}" y="244" class="mono" font-size="8.5" letter-spacing="1" fill="{ink}" fill-opacity=".55">{label}</text>'
                f'<rect x="{x}" y="252" width="68" height="4" rx="2" fill="{ink}" fill-opacity=".1"/>'
                f'<rect x="{x}" y="252" width="{68 * p:.0f}" height="4" rx="2" fill="{col}"/>')
    for k, (name, col, done) in enumerate([("Read", red, True), ("Walk", "#6b8f71", False), ("Water", gold, True)]):
        x = 56 + k * 80
        day += (f'<rect x="{x}" y="276" width="70" height="26" rx="13" fill="{col if done else "none"}" stroke="{col}" stroke-opacity=".7"/>'
                f'<text x="{x + 35}" y="293" text-anchor="middle" class="sans" font-size="11" font-weight="600" fill="{paper if done else ink}">{name}</text>')
    # a month grid with marked days
    cal = (f'<text x="330" y="88" font-family="{serif}" font-size="22" font-weight="700" fill="{paper}">November</text>'
           f'<text x="604" y="88" text-anchor="end" class="mono" font-size="11" fill="{paper}" fill-opacity=".5">2026</text>')
    start = 6  # 1 November 2026 is a Sunday
    for i in range(30):
        cell = start + i
        x, y = 342 + (cell % 7) * 38, 116 + (cell // 7) * 34
        if i + 1 == 9:
            cal += (f'<rect x="{x - 15}" y="{y - 16}" width="30" height="30" rx="8" fill="{paper}"/>'
                    f'<text x="{x}" y="{y + 4}" text-anchor="middle" class="sans" font-size="12" font-weight="700" fill="{ink}">9</text>')
        else:
            cal += f'<text x="{x}" y="{y + 4}" text-anchor="middle" class="sans" font-size="12" fill="{paper}" fill-opacity="{.85 if (cell % 7) < 5 else .5}">{i + 1}</text>'
        if i + 1 in (11, 17, 24):
            cal += f'<circle cx="{x}" cy="{y + 12}" r="2.4" fill="{gold if i + 1 == 24 else red}"/>'
    # an alarm that rings
    cal += (f'<rect x="330" y="296" width="276" height="30" rx="15" fill="{paper}" fill-opacity=".08" stroke="{paper}" stroke-opacity=".15"/>'
            f'<g transform="translate(350 311)"><path d="M-6 3V-1A6 6 0 0 1 6 -1V3L8 5H-8Z M-2 7H2" fill="none" stroke="{gold}" stroke-width="1.8" stroke-linejoin="round">'
            f'<animateTransform attributeName="transform" type="rotate" values="0;14;-14;10;-10;0;0" dur="2.4s" repeatCount="indefinite"/></path></g>'
            f'<text x="366" y="315" class="mono" font-size="11" fill="{paper}" fill-opacity=".8">07:00 · weekdays · snooze 10 min</text>')
    cover("almanac", "Almanac · day planner", "#161310", "#221d17", gold, day + cal, "Compose")


def somatrack():
    lime, cy, am, rose = "#a3e635", "#22d3ee", "#fbbf24", "#fb7185"

    def hi(t, c):
        return f'<tspan fill="{c}" fill-opacity="1" font-weight="700">{t}</tspan>'

    text = (f'<rect x="36" y="62" width="568" height="72" rx="10" fill="#ffffff" fill-opacity=".04" stroke="#ffffff" stroke-opacity=".08"/>'
            f'<text x="52" y="92" class="sans" font-size="15" fill="#ffffff" fill-opacity=".75">"I study {hi("7 hours", am)} a day, mostly {hi("on my bed", rose)} with the</text>'
            f'<text x="52" y="116" class="sans" font-size="15" fill="#ffffff" fill-opacity=".75">{hi("laptop on my knees", rose)}, and take a break {hi("every 2 hours", cy)}."</text>')
    chips = ""
    x = 36
    for lab, col in [("hours=7", am), ("surface=bed", rose), ("screen=lap", rose), ("breaks=120min", cy)]:
        w = len(lab) * 7.4 + 20
        chips += (f'<rect x="{x:.0f}" y="146" width="{w:.0f}" height="24" rx="12" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".5"/>'
                  f'<text x="{x + w / 2:.0f}" y="162" text-anchor="middle" class="mono" font-size="11.5" fill="{col}">{lab}</text>')
        x += w + 8
    risks = [("back pain", .74), ("neck strain", .66), ("eye strain", .58), ("headache", .41),
             ("wrist pain", .33), ("finger numb.", .18), ("overall", .61)]
    bars = ""
    for k, (name, p) in enumerate(risks):
        col = rose if p >= .6 else (am if p >= .4 else lime)
        y = 196 + k * 20
        bars += (f'<text x="36" y="{y + 8}" class="mono" font-size="11.5" fill="#ffffff" fill-opacity=".65">{name}</text>'
                 f'<rect x="140" y="{y}" width="200" height="9" rx="4.5" fill="#ffffff" fill-opacity=".07"/>'
                 f'<rect x="140" y="{y}" width="{200 * p:.0f}" height="9" rx="4.5" fill="{col}">'
                 f'<animate attributeName="width" values="0;{200 * p:.0f}" dur="1.6s"/></rect>'
                 f'<text x="352" y="{y + 8}" class="mono" font-size="11.5" fill="{col}">{p:.2f}</text>')
    rec = f'<rect x="404" y="188" width="200" height="146" rx="10" fill="#0a120f" stroke="{lime}" stroke-opacity=".35"/>' \
          f'<text x="420" y="212" class="mono" font-size="12" fill="{lime}">what to change</text>'
    for k, (tip, d) in enumerate([("Work at a desk", "−0.21"), ("Break every 45 min", "−0.12"), ("Raise the screen", "−0.09")]):
        y = 242 + k * 26
        rec += (f'<text x="420" y="{y}" class="sans" font-size="13" fill="#ffffff" fill-opacity=".85">{tip}</text>'
                f'<text x="588" y="{y}" text-anchor="end" class="mono" font-size="12" fill="{lime}">{d}</text>')
    rec += '<text x="420" y="320" class="mono" font-size="10.5" fill="#ffffff" fill-opacity=".4">change in back-pain risk</text>'
    cover("somatrack", "habits → risk → what to change", "#0a1512", "#10201b", lime, text + chips + bars + rec, "EN · FR · AR")


def jerd():
    am, cy, lime, rose = "#fbbf24", "#22d3ee", "#a3e635", "#fb7185"
    rnd = random.Random(6)
    # barcode in a scan frame with a sweeping laser
    bc = ""
    x = 66
    while x < 266:
        w = rnd.choice([2, 2, 3, 4, 6])
        bc += f'<rect x="{x}" y="96" width="{w}" height="106" fill="#ffffff" fill-opacity=".88"/>'
        x += w + rnd.choice([2, 3, 4])
    frame = (f'<rect x="44" y="70" width="248" height="170" rx="14" fill="#0b0a07" stroke="#ffffff" stroke-opacity=".08"/>' + bc +
             f'<text x="168" y="224" text-anchor="middle" class="mono" font-size="12" fill="#ffffff" fill-opacity=".7">6 130274 019835</text>'
             f'<path d="M56 96 V82 H70 M266 82 H280 V96 M280 214 V228 H266 M70 228 H56 V214" fill="none" stroke="{am}" stroke-width="3" stroke-linecap="round"/>'
             f'<rect x="56" y="150" width="224" height="2.5" fill="{rose}">'
             f'<animate attributeName="y" values="92;206;92" dur="2.6s" repeatCount="indefinite"/></rect>')
    # stock ledger
    led = '<text x="324" y="84" class="mono" font-size="12" fill="#ffffff" fill-opacity=".55">Semolina 1 kg · movements</text>'
    moves = [("+12", "received", lime, "09:10"), ("−1", "sold", rose, "10:42"), ("−3", "sold", rose, "12:05"),
             ("−1", "count fix", am, "14:30")]
    for k, (q, why, col, t) in enumerate(moves):
        y = 112 + k * 30
        led += (f'<text x="324" y="{y}" class="mono" font-size="14" font-weight="700" fill="{col}">{q}</text>'
                f'<text x="370" y="{y}" class="sans" font-size="13" fill="#ffffff" fill-opacity=".8">{why}</text>'
                f'<text x="604" y="{y}" text-anchor="end" class="mono" font-size="11" fill="#ffffff" fill-opacity=".4">{t}</text>'
                f'<line x1="324" x2="604" y1="{y + 11}" y2="{y + 11}" stroke="#ffffff" stroke-opacity=".06"/>')
    led += (f'<text x="324" y="258" class="mono" font-size="12" fill="#ffffff" fill-opacity=".55">on hand</text>'
            f'<text x="604" y="262" text-anchor="end" class="sans" font-size="30" font-weight="800" fill="#ffffff">7</text>'
            f'<rect x="324" y="272" width="280" height="6" rx="3" fill="#ffffff" fill-opacity=".07"/>'
            f'<rect x="324" y="272" width="98" height="6" rx="3" fill="{am}"/>'
            f'<line x1="436" x2="436" y1="267" y2="283" stroke="#ffffff" stroke-opacity=".6" stroke-width="1.5"/>'
            f'<text x="436" y="298" text-anchor="middle" class="mono" font-size="10.5" fill="{am}">reorder at 8</text>')
    sync = (f'<rect x="44" y="262" width="248" height="58" rx="12" fill="#ffffff" fill-opacity=".04" stroke="{cy}" stroke-opacity=".3"/>'
            f'<g transform="translate(70 291)"><g>'
            f'<path d="M-9 -2 A9 9 0 0 1 7 -6 M9 2 A9 9 0 0 1 -7 6" fill="none" stroke="{cy}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<path d="M3 -10 L7 -6 L2 -3 M-3 10 L-7 6 L-2 3" fill="none" stroke="{cy}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="3s" repeatCount="indefinite"/></g></g>'
            f'<text x="94" y="287" class="sans" font-size="13" font-weight="700" fill="#ffffff">3 movements queued</text>'
            f'<text x="94" y="305" class="mono" font-size="11" fill="#ffffff" fill-opacity=".5">no signal · syncs when online</text>')
    cover("jerd", "Jerd · stock count", "#14110a", "#1e190d", am, frame + led + sync, "offline-first")


for mode in ("dark", "light"):
    write(f"banner-{mode}.svg", banner(mode))
    for slug, num, title, acc in [("work", "01", "Selected work", "cyan"), ("toolbox", "02", "Toolbox", "violet"),
                                  ("activity", "03", "Activity", "lime"), ("hello", "04", "Say hello.", "amber")]:
        write(f"h-{slug}-{mode}.svg", header(mode, num, title, acc))

fpl(); drone(); ser(); rag(); cadence(); streamline()
eo_bench(); savepoint(); lumen(); mytube(); somatrack(); jerd(); feather_pdf(); almanac()
print("ok")
