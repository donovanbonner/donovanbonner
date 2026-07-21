#!/usr/bin/env python3
"""Generate a self-contained telemetry SVG (contribution heatmap + stats).

Reads a snapshot of the GitHub contribution calendar from /tmp/cal.json and
renders a monochrome, GitHub-style heatmap that reflects REAL activity
(private contributions included, since the API was queried while authed as the
user). This removes the dependency on the flaky github-readme-stats service.
"""
import json, os

# Resolve the assets dir whether this script runs from the scratchpad
# (./donovanbonner/assets) or from the repo (../assets when placed in scripts/).
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
CAL_PATH = os.environ.get("CAL_JSON", "/tmp/cal.json")

INK = "#0d1117"
MUTED = "#57606a"
DARK_INK = "#f0f6fc"
DARK_MUTED = "#8b949e"
FONT = ("ui-monospace,'SF Mono','JetBrains Mono','Cascadia Code',"
        "'Fira Code',Menlo,Consolas,monospace")

# ---- editable snapshot facts (honest; omit unflattering-but-true metrics) ---
SINCE = 2022
LANGS = "swift · typescript · python · java · c# · c++"

_user = json.load(open(CAL_PATH))["data"]["user"]
cal = _user["contributionsCollection"]["contributionCalendar"]
TOTAL = cal["totalContributions"]
weeks = cal["weeks"]
# public repo count: from the JSON if the query included it, else env, else 7
PUBLIC_REPOS = (_user.get("repositories", {}) or {}).get("totalCount") \
    or int(os.environ.get("PUBLIC_REPOS", 7))

# geometry — generous vertical spacing so the header never crowds the grid
GX, GY = 30, 128         # grid origin
CELL, GAP = 11, 2.6
STEP = CELL + GAP
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
GRID_BOTTOM = GY + 6 * STEP + CELL      # ~220
FOOT_Y = GRID_BOTTOM + 26               # legend + languages baseline
CARD_H = FOOT_Y + 16
VIEW_H = CARD_H + 2


def bucket(c):
    if c <= 0:  return 0.08
    if c <= 2:  return 0.30
    if c <= 5:  return 0.52
    if c <= 12: return 0.74
    return 1.0


def build(ink=INK, muted=MUTED):
    cells, labels = [], []
    last_month = None
    for i, w in enumerate(weeks):
        x = GX + i * STEP
        m = int(w["contributionDays"][0]["date"][5:7])
        if m != last_month and (not labels or (x - labels[-1][0]) > 3.2 * STEP):
            labels.append((x, MONTHS[m - 1]))
            last_month = m
        for dd in w["contributionDays"]:
            y = GY + dd["weekday"] * STEP
            cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2" '
                         f'fill="{ink}" fill-opacity="{bucket(dd["contributionCount"])}"/>')
    month_y = GY - 10
    month_txt = "".join(
        f'<text x="{x:.1f}" y="{month_y}" font-size="11" fill="{muted}">{name}</text>'
        for x, name in labels)
    # legend swatches (bottom-right)
    lx = 612
    leg = [f'<text x="{lx}" y="{FOOT_Y}" font-size="11" fill="{muted}">less</text>']
    for j, op in enumerate([0.08, 0.30, 0.52, 0.74, 1.0]):
        leg.append(f'<rect x="{lx + 34 + j*15}" y="{FOOT_Y-9}" width="11" height="11" rx="2" '
                   f'fill="{ink}" fill-opacity="{op}"/>')
    leg.append(f'<text x="{lx + 34 + 5*15 + 4}" y="{FOOT_Y}" font-size="11" fill="{muted}">more</text>')

    body = f'''  <rect x="1" y="1" width="818" height="{CARD_H}" rx="11" fill="none" stroke="{ink}" stroke-opacity="0.22" stroke-width="1.5"/>
  <text x="30" y="48" font-size="15"><tspan fill="{ink}" font-weight="700">$ </tspan><tspan fill="{muted}">gh telemetry --user donovanbonner</tspan></text>
  <text x="30" y="92" font-size="24" font-weight="700" fill="{ink}">{TOTAL}<tspan font-size="14" font-weight="400" fill="{muted}">&#160;&#160;contributions in the last year</tspan></text>
  <text x="790" y="92" text-anchor="end" font-size="13" fill="{muted}">{PUBLIC_REPOS} public repos &#183; building since {SINCE}</text>
  {month_txt}
  {''.join(cells)}
  {''.join(leg)}
  <text x="30" y="{FOOT_Y}" font-size="12" fill="{muted}">languages&#160;&#160;<tspan fill="{ink}">{LANGS}</tspan></text>'''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 {VIEW_H}" '
            f'width="820" height="{VIEW_H}" font-family="{FONT}" fill="none">\n'
            f'<!-- total={TOTAL} -->\n{body}\n</svg>\n')


open(os.path.join(LIGHT, "contribs.svg"), "w").write(build(INK, MUTED))
open(os.path.join(DARK, "contribs.svg"), "w").write(build(DARK_INK, DARK_MUTED))
print(f"wrote contribs.svg (light+dark) — {TOTAL} contribs, card_h={CARD_H}, "
      f"{sum(1 for w in weeks for d in w['contributionDays'] if d['contributionCount']>0)} active days")
