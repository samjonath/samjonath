"""Generates assets/header.svg: pixel-font name over a terminal prompt.

Run: python3 assets/build_header.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

NAME = "SAM JONATH"
LINES = [
    ("$", "whoami"),
    (">", "full-stack engineer // fintech // india"),
]

FONT = {
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    " ": ["..."] * 7,
}

W, PAD_X, TOP = 880, 36, 62
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

PX, GAP = 13, 2                   # pixel size and gap between pixels
cells = []                        # (x, y) of each filled pixel
col = 0
for ch in NAME:
    glyph = FONT[ch]
    for r, bits in enumerate(glyph):
        for c, b in enumerate(bits):
            if b == "#":
                cells.append((PAD_X + (col + c) * PX, TOP - 12 + r * PX))
    col += len(glyph[0]) + 1

def blocks():
    return "".join(f'<rect x="{x}" y="{y}" width="{PX - GAP}" height="{PX - GAP}" rx="1"/>' for x, y in cells)

logo_bottom = TOP - 12 + 7 * PX
line_y = [logo_bottom + 44 + i * 24 for i in range(len(LINES))]
H = line_y[-1] + 40

lines_svg = "".join(
    f'<text x="{PAD_X}" y="{y}"><tspan class="p">{escape(p)}</tspan> {escape(t)}</text>'
    for (p, t), y in zip(LINES, line_y)
)
cursor_y = line_y[-1] + 24 - 14
H += 12

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Sam Jonath, full-stack engineer, fintech">
<style>
  .bg{{fill:#0b0f14}}
  .frame{{fill:none;stroke:#30363d;stroke-width:1}}
  .name{{fill:#e6edf3}}
  .meta{{font:400 14px {MONO};fill:#8b949e}}
  .p{{fill:#7ee787}}
  .cur{{fill:#7ee787;animation:blink 1.1s infinite steps(1)}}
  .tag{{font:400 11px {MONO};fill:#484f58}}
  @keyframes blink{{0%,50%{{opacity:1}}51%,100%{{opacity:0}}}}
  @media (prefers-reduced-motion:reduce){{.cur{{animation:none}}}}
</style>
<rect class="bg" width="{W}" height="{H}" rx="8"/>
<rect class="frame" x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="8"/>
<text class="tag" x="{W - PAD_X}" y="26" text-anchor="end">~/samjonath</text>
<g class="name">{blocks()}</g>
<g class="meta">{lines_svg}</g>
<text class="meta" x="{PAD_X}" y="{line_y[-1] + 24}"><tspan class="p">$</tspan></text>
<rect class="cur" x="{PAD_X + 16}" y="{cursor_y}" width="9" height="17"/>
</svg>
'''
Path(__file__).with_name("header.svg").write_text(svg)
print("wrote header.svg", W, "x", H)
