"""Generates the toolbox grid: one same-size tile per skill, in the style of skillicons.dev.

Tiles come from skillicons.dev's artwork where it exists, otherwise from Simple Icons brand logos,
otherwise from a small drawn glyph. The skill list mirrors mohameddddt.github.io (lib/skills.ts),
groups in the site's order and skills by how many projects use them.
Needs network access to fetch the logos.

Usage: python scripts/generate_toolbox.py [output_dir]   # defaults to ./assets
"""
import math
import os
import random
import re
import sys
import urllib.request

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
SKILLICONS = "https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/"
SIMPLE_ICONS = "https://cdn.jsdelivr.net/npm/simple-icons@16/icons/"

THEMES = {
    "dark": dict(tile="#242938", ink="#e8ecf4", label="#c9d1dc", cyan="#22d3ee", violet="#a78bfa", lime="#a3e635",
                 amber="#fbbf24", rose="#fb7185", green="#4ade80"),
    "light": dict(tile="#F4F2ED", ink="#141821", label="#3d4454", cyan="#0891b2", violet="#7c3aed", lime="#4d7c0f",
                  amber="#d97706", rose="#e11d48", green="#16a34a"),
}

# (label, source): "si:Name" = skillicons file, "simple:slug" = Simple Icons, "g:name" = drawn glyph
SKILLS = [
    # Languages
    ("Python", "si:Python"), ("Dart", "si:Dart"), ("TypeScript", "si:TypeScript"), ("JavaScript", "si:JavaScript"),
    ("SQL", "g:sql"), ("Kotlin", "si:Kotlin"), ("Java", "si:Java"),
    # Machine learning
    ("scikit-learn", "si:ScikitLearn|SciKitLearn"), ("NumPy", "simple:numpy"), ("Jupyter", "simple:jupyter"), ("PyTorch", "si:PyTorch"),
    ("pandas", "simple:pandas"), ("Matplotlib", "g:plot"), ("XGBoost", "g:tree"), ("Transformers", "simple:huggingface"),
    ("Ensembles", "g:ensemble"), ("LightGBM", "g:leaftree"), ("WavLM", "g:wave"), ("MedCPT", "g:medical"),
    ("MobileNetV3", "g:mobilenet"), ("TF Lite", "si:TensorFlow"), ("librosa", "g:spectrogram"), ("SciPy", "simple:scipy"),
    # LLMs & retrieval
    ("Gemini API", "simple:googlegemini"), ("RAG", "g:rag"), ("Embeddings", "g:embeddings"), ("pgvector", "g:pgvector"),
    # Optimization
    ("Integer prog.", "g:lattice"), ("PuLP", "g:lp"), ("Branch & Bound", "g:bnb"), ("Genetic algos", "g:dna"),
    ("Sim. annealing", "g:anneal"), ("ALNS", "g:alns"), ("Dynamic prog.", "g:dp"),
    # Backend & APIs
    ("FastAPI", "si:FastAPI"), ("JWT", "simple:jsonwebtokens"), ("Flask", "si:Flask"), ("Node.js", "si:NodeJS"),
    ("Express", "si:ExpressJS"), ("SQLAlchemy", "simple:sqlalchemy"), ("Gunicorn", "simple:gunicorn"), ("Celery", "simple:celery"),
    # Web & desktop
    ("React", "si:React"), ("Vite", "si:Vite"), ("Next.js", "si:NextJS"), ("Tailwind CSS", "si:TailwindCSS"),
    ("TanStack Query", "simple:reactquery"), ("MapLibre", "simple:maplibre"), ("Electron", "si:Electron"),
    # Mobile
    ("Flutter", "si:Flutter"), ("SQLite", "si:SQLite"), ("BLoC", "g:bloc"), ("Firebase FCM", "si:Firebase"),
    ("Compose", "simple:jetpackcompose"), ("Material 3", "simple:materialdesign"), ("Coil", "g:image"),
    ("DataStore", "g:keyvalue"), ("Provider", "g:provider"), ("GetIt", "g:locator"), ("Hive", "g:hive"),
    # Data & cloud
    ("PostgreSQL", "si:PostgreSQL"), ("Supabase", "si:Supabase"), ("Render", "simple:render"), ("Vercel", "si:Vercel"),
    ("PostGIS", "g:map"), ("Redis", "si:Redis"), ("Kaggle", "simple:kaggle"),
    # Media
    ("FFmpeg", "simple:ffmpeg"), ("yt-dlp", "g:download"), ("ExoPlayer", "g:play"), ("WebTorrent", "g:magnet"),
    ("Invidious", "simple:invidious"), ("Chromaprint", "g:fingerprint"),
    # Quality & DevOps
    ("GitHub Actions", "si:GithubActions"), ("Docker", "si:Docker"), ("pytest", "simple:pytest"), ("Sentry", "si:Sentry"),
    ("Playwright", "g:browsertest"), ("PyInstaller", "g:package"),
    # Domains
    ("Computer vision", "si:OpenCV"), ("NLP", "g:chat"), ("Audio", "g:speaker"), ("Geospatial", "g:globe"),
    ("Sports analytics", "g:ball"), ("Security", "g:shield"),
    # Also from coursework and everyday use
    ("C", "si:C"), ("C++", "si:CPP"), ("Bash", "si:Bash"), ("Linux", "si:Linux"), ("Git", "si:Git"),
]

# Simple Icons colours that vanish on a tile, per theme
COLOR_OVERRIDES = {"numpy": {"dark": "#4dabcf"}, "huggingface": {"light": "#ff9d00"},
                   "materialdesign": {"dark": "#d0bcff"}, "scipy": {"light": "#0054a6"}}

_cache = {}


def fetch(url):
    if url not in _cache:
        req = urllib.request.Request(url, headers={"User-Agent": "profile-toolbox"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                _cache[url] = r.read().decode("utf-8")
        except Exception:
            _cache[url] = None
    return _cache[url]


def luminance(hex_):
    def ch(c):
        c = int(c, 16) / 255
        return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    h = hex_.lstrip("#")
    r, g, b = (ch(h[i:i + 2]) for i in (0, 2, 4))
    return .2126 * r + .7152 * g + .0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + .05) / (lb + .05)


def scope_ids(svg, prefix):
    """Prefix every id so icons can share one document."""
    ids = set(re.findall(r'id="([^"]+)"', svg))
    for i in ids:
        svg = svg.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f"url(#{i})", f"url(#{prefix}{i})")
        svg = svg.replace(f'href="#{i}"', f'href="#{prefix}{i}"')
    return svg


def skillicon(names, mode, prefix):
    # "A|B": the repo spells some names differently per theme (ScikitLearn-Dark, SciKitLearn-Light)
    svg = next((s for n in names.split("|") for s in (fetch(f"{SKILLICONS}{n}-{mode.title()}.svg"),
                                                       fetch(f"{SKILLICONS}{n}.svg")) if s), None)
    if not svg:
        name = names
        raise SystemExit(f"skillicons: no artwork for {name}")
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", svg.strip(), flags=re.S)
    return scope_ids(inner, prefix)


def simple_icon(slug, mode, t):
    svg = fetch(f"{SIMPLE_ICONS}{slug}.svg")
    if not svg:
        raise SystemExit(f"Simple Icons: no icon {slug}")
    d = re.search(r'<path d="([^"]+)"', svg).group(1)
    color = COLOR_OVERRIDES.get(slug, {}).get(mode) or "#" + BRAND_HEX[slug]
    if contrast(color, t["tile"]) < 2.2:
        color = t["ink"]
    return (f'<rect width="256" height="256" rx="60" fill="{t["tile"]}"/>'
            f'<path transform="translate(60 60) scale(5.667)" d="{d}" fill="{color}"/>')


BRAND_HEX = {}


def load_brand_colors():
    import json
    data = json.loads(fetch("https://cdn.jsdelivr.net/npm/simple-icons@16/data/simple-icons.json"))
    for icon in data if isinstance(data, list) else data["icons"]:
        if "slug" in icon:
            BRAND_HEX[icon["slug"]] = icon["hex"]


# ---------------------------------------------------------------- drawn glyphs, on a 256 tile
def S(c, w=14, fill="none", cap="round"):
    return f'fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="round"'


def glyph(name, t):
    a, b, c, d, e, ink = t["cyan"], t["violet"], t["lime"], t["amber"], t["rose"], t["ink"]
    rnd = random.Random(name)
    if name == "sql":
        return (f'<ellipse cx="128" cy="74" rx="62" ry="22" {S(a)}/>'
                f'<path d="M66 74V182A62 22 0 0 0 190 182V74M66 128A62 22 0 0 0 190 128" {S(a)}/>')
    if name == "plot":
        return (f'<path d="M62 58V194H200" {S(ink, 12)} stroke-opacity=".5"/>'
                f'<path d="M78 170C102 70 130 196 150 120S184 70 196 76" {S(a)}/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="{d}"/>' for x, y in [(96, 150), (128, 168), (160, 104), (188, 132)]))
    if name in ("tree", "leaftree", "bnb"):
        if name == "tree":
            nodes = {0: (128, 62), 1: (82, 126), 2: (174, 126), 3: (58, 192), 4: (106, 192), 5: (150, 192), 6: (198, 192)}
            edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
            col = a
        elif name == "leaftree":
            nodes = {0: (96, 58), 1: (60, 114), 2: (144, 114), 3: (112, 164), 4: (190, 164), 5: (84, 206), 6: (140, 206)}
            edges = [(0, 1), (0, 2), (2, 3), (2, 4), (3, 5), (3, 6)]
            col = c
        else:
            nodes = {0: (128, 62), 1: (80, 126), 2: (176, 126), 3: (56, 192), 4: (104, 192)}
            edges = [(0, 1), (0, 2), (1, 3), (1, 4)]
            col = b
        out = "".join(f'<path d="M{nodes[i][0]} {nodes[i][1]}L{nodes[j][0]} {nodes[j][1]}" {S(ink, 9)} stroke-opacity=".45"/>' for i, j in edges)
        out += "".join(f'<circle cx="{x}" cy="{y}" r="17" fill="{col}"/>' for x, y in nodes.values())
        if name == "bnb":  # a pruned branch
            out += (f'<path d="M176 143L196 178" {S(ink, 9)} stroke-opacity=".45" stroke-dasharray="2 14"/>'
                    f'<path d="M184 178L212 206M212 178L184 206" {S(e, 12)}/>')
        return out
    if name == "ensemble":
        return (f'<path d="M70 76L128 180M128 76V180M186 76L128 180" {S(ink, 9)} stroke-opacity=".45"/>'
                f'<circle cx="70" cy="76" r="22" fill="{a}"/><circle cx="128" cy="76" r="22" fill="{b}"/>'
                f'<circle cx="186" cy="76" r="22" fill="{c}"/><circle cx="128" cy="184" r="28" fill="{d}"/>')
    if name == "wave":
        hs = [30, 62, 96, 70, 124, 84, 52, 104, 66, 36]
        return "".join(f'<path d="M{58 + i * 15.5:.1f} {128 - h / 2}V{128 + h / 2}" {S(b if i % 2 else a, 10)}/>' for i, h in enumerate(hs))
    if name == "medical":
        return (f'<path d="M128 70V186M70 128H186" {S(e, 36)}/>'
                f'<circle cx="190" cy="66" r="12" fill="{a}"/><circle cx="66" cy="190" r="12" fill="{b}"/>'
                f'<circle cx="196" cy="190" r="9" fill="{a}" fill-opacity=".6"/>')
    if name == "mobilenet":
        out = f'<rect x="80" y="44" width="96" height="168" rx="20" {S(ink, 11)}/>'
        for i in range(3):
            for j in range(3):
                out += f'<rect x="{98 + i * 22}" y="{88 + j * 22}" width="16" height="16" rx="4" fill="{d}" fill-opacity="{.35 + .65 * rnd.random():.2f}"/>'
        return out + f'<path d="M116 186H140" {S(ink, 9)} stroke-opacity=".5"/>'
    if name == "spectrogram":
        out = ""
        for i in range(9):
            for j in range(7):
                v = rnd.random() * (1 - j / 9)
                out += f'<rect x="{52 + i * 17}" y="{68 + j * 17}" width="14" height="14" rx="3" fill="{b if v < .45 else e}" fill-opacity="{.2 + .8 * v:.2f}"/>'
        return out
    if name == "rag":
        return (f'<rect x="56" y="48" width="104" height="136" rx="14" {S(ink, 11)}/>'
                f'<path d="M80 86H136M80 112H136M80 138H112" {S(ink, 9)} stroke-opacity=".5"/>'
                f'<circle cx="166" cy="162" r="32" {S(a, fill=t["tile"])}/><path d="M190 186L212 208" {S(a, 16)}/>')
    if name == "embeddings":
        o = (66, 194)
        out = ""
        for (x, y), col in [((196, 92), a), ((186, 170), b), ((112, 60), c)]:
            out += f'<path d="M{o[0]} {o[1]}L{x} {y}" {S(col, 11)}/><circle cx="{x}" cy="{y}" r="15" fill="{col}"/>'
        return out + f'<circle cx="{o[0]}" cy="{o[1]}" r="12" fill="{ink}"/>'
    if name == "pgvector":
        return (f'<ellipse cx="106" cy="88" rx="48" ry="17" {S(b, 12)}/>'
                f'<path d="M58 88V172A48 17 0 0 0 154 172V88M58 130A48 17 0 0 0 154 130" {S(b, 12)}/>'
                f'<path d="M150 150L196 84" {S(a, 12)}/><circle cx="198" cy="80" r="15" fill="{a}"/>')
    if name == "lattice":
        out = f'<path d="M68 188L68 108L148 68L188 108L188 188Z" fill="{a}" fill-opacity=".14" stroke="{a}" stroke-width="9" stroke-linejoin="round"/>'
        for i in range(4):
            for j in range(4):
                x, y = 68 + i * 40, 68 + j * 40
                out += f'<circle cx="{x}" cy="{y}" r="9" fill="{ink}" fill-opacity=".45"/>'
        return out + f'<circle cx="148" cy="108" r="17" fill="{d}"/>'
    if name == "lp":
        return (f'<path d="M62 192V93L132 134L93 192Z" fill="{c}" fill-opacity=".2"/>'
                f'<path d="M50 85L206 180M84 206L190 48" {S(c, 11)}/>'
                f'<path d="M62 52V192H204" {S(ink, 10)} stroke-opacity=".45"/><circle cx="132" cy="134" r="17" fill="{d}"/>')
    if name == "dna":
        p1, p2, rungs = [], [], ""
        for k in range(29):
            x = 52 + k * 152 / 28
            s = math.sin(k / 28 * 2 * math.pi * 1.5)
            p1.append(f"{x:.1f} {128 - 54 * s:.1f}")
            p2.append(f"{x:.1f} {128 + 54 * s:.1f}")
            if k % 3 == 1:
                rungs += f'<path d="M{x:.1f} {128 - 54 * s:.1f}V{128 + 54 * s:.1f}" {S(ink, 7)} stroke-opacity=".35"/>'
        return rungs + f'<path d="M{"L".join(p1)}" {S(e, 13)}/><path d="M{"L".join(p2)}" {S(a, 13)}/>'
    if name == "anneal":
        pts = []
        for k in range(41):
            x = 48 + k * 4
            y = 92 + k * 1.6 + 30 * math.sin(k / 3.2) * (1 - k / 60)
            pts.append(f"{x:.1f} {y:.1f}")
        return (f'<path d="M{"L".join(pts)}" {S(d, 12)}/>'
                f'<circle cx="108" cy="78" r="17" fill="{e}"/><path d="M128 66Q150 40 170 70" {S(ink, 8)} stroke-opacity=".5" stroke-dasharray="1 14"/>')
    if name == "alns":
        pts = [(128 + 70 * math.cos(k / 8 * 2 * math.pi), 128 + 70 * math.sin(k / 8 * 2 * math.pi)) for k in range(8)]
        out = ""
        for k in range(8):
            (x1, y1), (x2, y2) = pts[k], pts[(k + 1) % 8]
            if k in (1, 2):
                continue
            out += f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" {S(a, 10)}/>'
        (x1, y1), (x3, y3) = pts[1], pts[3]
        out += f'<path d="M{x1:.1f} {y1:.1f}Q128 150 {x3:.1f} {y3:.1f}" {S(d, 10)} stroke-dasharray="2 16"/>'
        return out + "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{d if k == 2 else ink}"/>' for k, (x, y) in enumerate(pts))
    if name == "dp":
        out = ""
        for i in range(4):
            for j in range(4):
                filled = i + j <= 3
                out += (f'<rect x="{54 + i * 38}" y="{54 + j * 38}" width="32" height="32" rx="7" '
                        f'fill="{b if filled else ink}" fill-opacity="{.3 + .2 * (i + j) if filled else .1}"/>')
        return out + f'<path d="M70 70L190 190" {S(d, 11)}/><path d="M164 192H192V164" {S(d, 11)}/>'
    if name == "bloc":
        return (f'<path d="M128 46L200 88L128 130L56 88Z" fill="{a}"/>'
                f'<path d="M56 88L128 130V212L56 170Z" fill="{a}" fill-opacity=".55"/>'
                f'<path d="M200 88L128 130V212L200 170Z" fill="{b}" fill-opacity=".75"/>')
    if name == "image":
        return (f'<rect x="54" y="66" width="148" height="124" rx="18" {S(e, 12)}/>'
                f'<path d="M58 172L104 126L140 160L162 140L198 176" {S(e, 12)}/><circle cx="160" cy="104" r="14" fill="{d}"/>')
    if name == "keyvalue":
        out = ""
        for k, col in enumerate([a, b, c]):
            y = 70 + k * 46
            out += (f'<rect x="56" y="{y}" width="36" height="32" rx="8" fill="{col}"/>'
                    f'<path d="M112 {y + 16}H{200 - k * 22}" {S(ink, 12)} stroke-opacity=".55"/>')
        return out
    if name == "provider":
        return (f'<path d="M128 98V128M88 128H168M88 128V156M168 128V156" {S(ink, 10)} stroke-opacity=".5"/>'
                f'<rect x="92" y="52" width="72" height="46" rx="12" fill="{a}"/>'
                f'<rect x="52" y="156" width="72" height="46" rx="12" fill="{b}"/><rect x="132" y="156" width="72" height="46" rx="12" fill="{b}"/>')
    if name == "locator":
        return (f'<circle cx="128" cy="128" r="64" {S(c, 12)}/><circle cx="128" cy="128" r="30" {S(c, 12)}/>'
                f'<path d="M128 44V74M128 182V212M44 128H74M182 128H212" {S(ink, 11)}/><circle cx="128" cy="128" r="9" fill="{d}"/>')
    if name == "hive":
        def hexa(cx, cy, r=34):
            return "M" + "L".join(f"{cx + r * math.cos(math.pi / 3 * k + math.pi / 6):.1f} {cy + r * math.sin(math.pi / 3 * k + math.pi / 6):.1f}" for k in range(6)) + "Z"
        return (f'<path d="{hexa(98, 96)}" fill="{d}"/><path d="{hexa(158, 96)}" fill="{d}" fill-opacity=".6"/>'
                f'<path d="{hexa(128, 148)}" fill="{d}" fill-opacity=".85"/>')
    if name == "map":
        return (f'<path d="M48 84L96 64L160 88L208 68V172L160 192L96 168L48 188Z" fill-opacity=".12" {S(a, 10, fill=a)}/>'
                f'<path d="M96 64V168M160 88V192" {S(a, 8)} stroke-opacity=".5"/>'
                f'<path d="M128 156C128 156 96 120 96 100A32 32 0 0 1 160 100C160 120 128 156 128 156Z" fill="{e}"/><circle cx="128" cy="100" r="11" fill="{t["tile"]}"/>')
    if name == "download":
        return f'<path d="M128 52V150M88 112L128 152L168 112" {S(e, 18)}/><path d="M60 168V196H196V168" {S(ink, 14)}/>'
    if name == "play":
        return (f'<rect x="48" y="66" width="160" height="124" rx="22" {S(a, 12)}/>'
                f'<path d="M110 100L156 128L110 156Z" fill="{a}" stroke="{a}" stroke-width="8" stroke-linejoin="round"/>')
    if name == "magnet":
        return (f'<path d="M78 70V132A50 50 0 0 0 178 132V70" {S(e, 32, cap="butt")}/>'
                f'<path d="M78 56V84M178 56V84" stroke="{ink}" stroke-width="32"/>')
    if name == "fingerprint":
        out = ""
        for k, r in enumerate([20, 40, 60, 80]):
            out += f'<path d="M{128 - r} {150}A{r} {r} 0 0 1 {128 + r} {150}" {S(b if k % 2 else a, 11)}/>'
            out += f'<path d="M{128 - r} {150}V{150 + 26 - k * 6}" {S(b if k % 2 else a, 11)}/>'
        return out + f'<path d="M128 150V198" {S(a, 11)}/>'
    if name == "browsertest":
        return (f'<rect x="44" y="58" width="168" height="140" rx="20" {S(ink, 11)}/><path d="M44 96H212" {S(ink, 11)}/>'
                + "".join(f'<circle cx="{70 + k * 22}" cy="77" r="6" fill="{ink}"/>' for k in range(3))
                + f'<path d="M92 148L118 172L166 124" {S(t["green"], 16)}/>')
    if name == "package":
        return (f'<path d="M128 46L204 86V170L128 210L52 170V86Z" fill="#3776ab"/>'
                f'<path d="M52 86L128 126L204 86L128 46Z" fill="#ffd43b"/><path d="M128 126V210" stroke="#1e4f7a" stroke-width="8"/>')
    if name == "chat":
        return (f'<path d="M60 64H196A14 14 0 0 1 210 78V158A14 14 0 0 1 196 172H118L80 204V172H60A14 14 0 0 1 46 158V78A14 14 0 0 1 60 64Z" {S(b, 12)}/>'
                f'<path d="M80 102H176M80 134H148" {S(ink, 11)} stroke-opacity=".6"/>')
    if name == "speaker":
        return (f'<path d="M56 104H88L132 66V190L88 152H56Z" fill="{a}"/>'
                f'<path d="M158 100A40 40 0 0 1 158 156M178 76A72 72 0 0 1 178 180" {S(a, 12)}/>')
    if name == "globe":
        return (f'<circle cx="128" cy="128" r="76" {S(c, 12)}/><ellipse cx="128" cy="128" rx="34" ry="76" {S(c, 10)}/>'
                f'<path d="M52 128H204M64 90H192M64 166H192" {S(c, 9)} stroke-opacity=".7"/>')
    if name == "ball":
        pent = "M" + "L".join(f"{128 + 28 * math.cos(-math.pi / 2 + k * 2 * math.pi / 5):.1f} {128 + 28 * math.sin(-math.pi / 2 + k * 2 * math.pi / 5):.1f}" for k in range(5)) + "Z"
        spokes = "".join(f"M{128 + 28 * math.cos(-math.pi / 2 + k * 2 * math.pi / 5):.1f} {128 + 28 * math.sin(-math.pi / 2 + k * 2 * math.pi / 5):.1f}"
                         f"L{128 + 76 * math.cos(-math.pi / 2 + k * 2 * math.pi / 5):.1f} {128 + 76 * math.sin(-math.pi / 2 + k * 2 * math.pi / 5):.1f}" for k in range(5))
        return (f'<circle cx="128" cy="128" r="76" fill-opacity=".08" {S(ink, 11, fill=ink)}/>'
                f'<path d="{spokes}" {S(ink, 9)}/><path d="{pent}" fill="{c}"/>')
    if name == "shield":
        return (f'<path d="M128 44L200 72V124C200 168 168 198 128 214C88 198 56 168 56 124V72Z" fill-opacity=".14" {S(e, 12, fill=e)}/>'
                f'<path d="M98 128L120 150L162 106" {S(e, 15)}/>')
    raise SystemExit(f"no glyph {name}")


def tile(source, mode, prefix):
    t = THEMES[mode]
    kind, ref = source.split(":", 1)
    if kind == "si":
        return skillicon(ref, mode, prefix)
    if kind == "simple":
        return simple_icon(ref, mode, t)
    return f'<rect width="256" height="256" rx="60" fill="{t["tile"]}"/>' + glyph(ref, t)


def grid(mode):
    t = THEMES[mode]
    W, COLS, TILE = 880, 9, 72
    cell = W / COLS
    ROW = TILE + 44
    out = ""
    for k, (label, source) in enumerate(SKILLS):
        col, row = k % COLS, k // COLS
        x, y = col * cell + (cell - TILE) / 2, row * ROW
        out += (f'<svg x="{x:.1f}" y="{y}" width="{TILE}" height="{TILE}" viewBox="0 0 256 256">'
                f'{tile(source, mode, f"i{k}-")}</svg>'
                f'<text x="{col * cell + cell / 2:.1f}" y="{y + TILE + 20}" text-anchor="middle" font-family="{SANS}" '
                f'font-size="12.5" fill="{t["label"]}">{label.replace("&", "&amp;")}</text>')
    rows = math.ceil(len(SKILLS) / COLS)
    H = rows * ROW - 14
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="{len(SKILLS)} skills">\n{out}\n</svg>\n')


load_brand_colors()
for mode in ("dark", "light"):
    svg = grid(mode)  # build first so a failed fetch never truncates the existing file
    with open(os.path.join(OUT, f"toolbox-{mode}.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
print(f"ok · {len(SKILLS)} tiles")
