"""Wrap Platane/snk output in a 404.0 FM card so it matches the rest of the profile.

Usage (in CI, after snk):  python3 scripts/frame_snake.py dist/snake-raw.svg dist/snake.svg
"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
snk = open(src).read()
vb = re.search(r'viewBox="([^"]+)"', snk).group(1)
_, _, vw, vh = (float(v) for v in vb.split())
inner = snk[snk.index(">", snk.index("<svg")) + 1: snk.rindex("</svg>")]

SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace'
BG, PANEL, LINE, TXT, MUTED = "#1c1430", "#241a3b", "#2f2450", "#f2ecff", "#9a8bb4"
AMBER, PINK, RED = "#ffd43b", "#ff8fab", "#ff4d6d"
DOTS = ["#2f2450", "#4a2f6b", "#7a3f8f", "#b06cff", "#ff8fab"]

PX, PY, PW = 24, 66, 952
SW = PW - 40
SH = round(SW * vh / vw)
PH = SH + 32
FY = PY + PH + 30
H = FY + 24

legend = "".join(
    f'<rect x="{84 + i * 18}" y="{FY - 11}" width="12" height="12" rx="3" fill="{c}"/>' for i, c in enumerate(DOTS)
)
out = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{H}" viewBox="0 0 1000 {H}" role="img" aria-label="Signal history: the station snake (a yellow snake) eats Fang Foo Fong's GitHub contribution graph, one commit at a time.">
<style>
.fx-h{{font:700 15px {MONO};fill:{TXT};letter-spacing:3px}}
.fx-m{{font:500 13px {MONO};fill:{MUTED}}}
.fx-on{{font:700 11px {MONO};fill:{RED};letter-spacing:1.5px}}
.fx-blink{{animation:fx-blink 1.2s steps(2) infinite}}
@keyframes fx-blink{{50%{{opacity:.25}}}}
</style>
<rect width="1000" height="{H}" rx="18" fill="{BG}"/>
<text x="32" y="44" class="fx-h">SIGNAL HISTORY</text>
<circle class="fx-blink" cx="222" cy="39" r="4" fill="{RED}"/><text x="232" y="43" class="fx-on">LIVE FEED</text>
<text x="968" y="44" class="fx-m" text-anchor="end">the station snake eats one commit at a time</text>
<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="14" fill="#130d1f" stroke="{LINE}" stroke-width="1.5"/>
<svg x="{PX + 20}" y="{PY + 16}" width="{SW}" height="{SH}" viewBox="{vb}">{inner}</svg>
<text x="32" y="{FY}" class="fx-m">less</text>{legend}<text x="{84 + 5 * 18 + 6}" y="{FY}" class="fx-m">more</text>
<text x="968" y="{FY}" class="fx-m" text-anchor="end">fed daily at 07:00 ICT · please do not tap the glass</text>
</svg>'''
open(dst, "w").write(out)
