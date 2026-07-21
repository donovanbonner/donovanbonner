#!/usr/bin/env python3
"""Generate the profile README SVG banners (light + dark) for donovanbonner.

Design language: strict monochrome terminal aesthetic, transparent background.
Light variants use dark ink (#0d1117) on the page's white background; dark
variants swap to near-white ink (#f0f6fc). Backgrounds stay transparent so a
single <picture> theme flip is all that's needed.
"""
import os

# Resolve the assets dir whether run from the scratchpad (./donovanbonner/assets)
# or from the repo (../assets when this file lives in scripts/).
HERE = os.path.dirname(os.path.abspath(__file__))
for _c in (os.path.join(HERE, "donovanbonner", "assets"),
           os.path.join(os.path.dirname(HERE), "assets")):
    if os.path.isdir(_c):
        LIGHT = _c
        break
else:
    LIGHT = os.path.join(HERE, "assets")
    os.makedirs(LIGHT, exist_ok=True)
DARK = os.path.join(LIGHT, "dark")
os.makedirs(DARK, exist_ok=True)

# --- palette (light) -------------------------------------------------------
INK = "#0d1117"      # near-black
MUTED = "#57606a"    # gray
DARK_INK = "#f0f6fc"
DARK_MUTED = "#8b949e"

FONT = ("ui-monospace,'SF Mono','JetBrains Mono','Cascadia Code',"
        "'Fira Code',Menlo,Consolas,monospace")


def cursor(size=None):
    return (f'<tspan fill="{INK}">█'
            f'<animate attributeName="opacity" values="1;1;0;0" '
            f'keyTimes="0;0.5;0.5;1" dur="1.05s" repeatCount="indefinite"/>'
            f'</tspan>')


def wrap(viewbox, body):
    w, h = viewbox
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="{FONT}" fill="none">\n{body}\n</svg>\n')


def prompt(txt, cmd):
    """'$ cmd' — $ in ink, command in muted."""
    return f'<tspan fill="{INK}" font-weight="700">{txt} </tspan><tspan fill="{MUTED}">{cmd}</tspan>'


def line(text, y, cont=False):
    """A '> ' output line (ink) or an indented continuation line."""
    lead = f'<tspan fill="{MUTED}">&gt;&#160;</tspan>' if not cont else '<tspan>&#160;&#160;</tspan>'
    return f'  <text x="30" y="{y}" font-size="16" fill="{INK}">{lead}{text}</text>'


# --- header ----------------------------------------------------------------
def header():
    body = f'''  <rect x="1" y="1" width="818" height="186" rx="11" fill="none" stroke="{INK}" stroke-opacity="0.22" stroke-width="1.5"/>
  <circle cx="30" cy="30" r="5.5" fill="none" stroke="{INK}" stroke-opacity="0.45"/>
  <circle cx="50" cy="30" r="5.5" fill="none" stroke="{INK}" stroke-opacity="0.45"/>
  <circle cx="70" cy="30" r="5.5" fill="none" stroke="{INK}" stroke-opacity="0.45"/>
  <text x="792" y="35" text-anchor="end" font-size="13" fill="{MUTED}" letter-spacing="0.5">~/donovanbonner — zsh</text>
  <line x1="20" y1="52" x2="800" y2="52" stroke="{INK}" stroke-opacity="0.12" stroke-width="1"/>
  <text x="40" y="118" font-size="46" font-weight="700" letter-spacing="6" fill="{INK}">DONOVAN BONNER</text>
  <text x="42" y="156" font-size="16" fill="{MUTED}"><tspan fill="{INK}" font-weight="700">$ </tspan>full-stack software engineer &#183; atlanta, ga&#160;{cursor()}</text>'''
    return wrap((820, 188), body)


# --- section label ---------------------------------------------------------
def section(num, name):
    body = f'''  <rect x="4" y="13" width="10" height="10" fill="{INK}"/>
  <text x="26" y="27" font-size="15" letter-spacing="1"><tspan fill="{INK}" font-weight="700">{num}</tspan><tspan fill="{MUTED}">&#160;&#160;—&#160;&#160;{name}</tspan></text>
  <line x1="190" y1="19" x2="816" y2="19" stroke="{INK}" stroke-opacity="0.16" stroke-width="1"/>'''
    return wrap((820, 42), body)


# --- whoami card -----------------------------------------------------------
def whoami():
    lines = "\n".join([
        line("full-stack engineer — i build because i can't not.", 96),
        line("shipping swift-native consumer apps on the side,", 128),
        line("chasing that premium, it-just-feels-right polish.", 154, cont=True),
        line("deep focus over breadth: a few hard things, done right.", 190),
        line(f'production experience that reached real users.&#160;{cursor()}', 222),
    ])
    body = f'''  <rect x="1" y="1" width="818" height="252" rx="11" fill="none" stroke="{INK}" stroke-opacity="0.22" stroke-width="1.5"/>
  <text x="30" y="50" font-size="16">{prompt("$", "whoami")}</text>
{lines}'''
    return wrap((820, 254), body)


# --- the work card (clickable -> NeuroScan AI repo) ------------------------
def _b(txt, y, x=30, lead=True):
    pre = f'<tspan fill="{MUTED}">&gt;&#160;</tspan>' if lead else ''
    return f'  <text x="{x}" y="{y}" font-size="15" fill="{INK}">{pre}{txt}</text>'

def work():
    body = f'''  <rect x="1" y="1" width="818" height="316" rx="11" fill="none" stroke="{INK}" stroke-opacity="0.22" stroke-width="1.5"/>
  <text x="30" y="48" font-size="16">{prompt("$", "open neuroscan-ai")}</text>
  <text x="30" y="88" font-size="18" font-weight="700" fill="{INK}">NeuroScan AI<tspan font-weight="400" fill="{MUTED}">&#160;&#160;—&#160;&#160;full-stack MRI tumor diagnostics</tspan></text>
{_b("Cassandra, a fine-tuned EfficientNet CNN, separates three", 126)}
{_b("tumor types from healthy MRI at 93.3% test accuracy.", 151, x=46, lead=False)}
{_b("Grad-CAM heatmaps trace the gradient back to show exactly", 184)}
{_b("where the model looked — explainable, not a black box.", 209, x=46, lead=False)}
{_b("Next.js + FastAPI, with a retrieval-grounded assistant", 242)}
{_b("that explains each result in plain language.", 267, x=46, lead=False)}
  <text x="30" y="302" font-size="14" fill="{MUTED}">pytorch &#183; deep learning &#183; full-stack</text>
  <rect x="626" y="284" width="166" height="30" rx="6" fill="none" stroke="{INK}" stroke-opacity="0.55"/>
  <text x="709" y="304" text-anchor="middle" font-size="14" font-weight="700" fill="{INK}">view repo →</text>'''
    return wrap((820, 318), body)


# --- "building something new" teaser (slim banner under the work card) -----
def building():
    body = f'''  <circle cx="12" cy="21" r="4.5" fill="{INK}">
    <animate attributeName="fill-opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
  </circle>
  <text x="30" y="26" font-size="15"><tspan fill="{INK}" font-weight="700">building something new</tspan><tspan fill="{MUTED}"> in stealth — swift-native, consumer. more when it's ready.&#160;</tspan>{cursor()}</text>'''
    return wrap((820, 42), body)


# --- footer ----------------------------------------------------------------
def footer():
    body = f'''  <line x1="4" y1="16" x2="816" y2="16" stroke="{INK}" stroke-opacity="0.14" stroke-width="1"/>
  <text x="410" y="48" text-anchor="middle" font-size="13" fill="{MUTED}"><tspan fill="{INK}" font-weight="700">$ </tspan>open to good people and hard problems — reach out ↑&#160;{cursor()}</text>'''
    return wrap((820, 66), body)


ASSETS = {
    "header.svg": header(),
    "s01.svg": section("01", "whoami"),
    "whoami.svg": whoami(),
    "s02.svg": section("02", "the work"),
    "work.svg": work(),
    "building.svg": building(),
    "s03.svg": section("03", "telemetry"),
    "footer.svg": footer(),
}


def to_dark(svg):
    return svg.replace(INK, DARK_INK).replace(MUTED, DARK_MUTED)


for name, svg in ASSETS.items():
    with open(os.path.join(LIGHT, name), "w") as f:
        f.write(svg)
    with open(os.path.join(DARK, name), "w") as f:
        f.write(to_dark(svg))

print("wrote", len(ASSETS), "light +", len(ASSETS), "dark svgs")
for n in ASSETS:
    print("  ", n)
