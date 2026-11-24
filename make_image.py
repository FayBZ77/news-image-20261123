#!/usr/bin/env python3
"""Front-page summary of the world news of Monday 23 November 2026, drawn with PIL.

Stories (all reported on 23 Nov 2026, cross-checked across Reuters, AP-style wires and
day-roundups): Nvidia reinstates Jensen Huang and the market rips; Ukraine sinks a Russian
corvette in a Libyan port; Iran vows to defy the US blockade at Hormuz; COP31 ends with no
deal; a Russian strike flattens a Dymer apartment block; a Banten candy-factory fire kills 24.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 230)
INK = (18, 20, 24)
GRAY = (80, 84, 88)
RULE = (30, 30, 34)
LIGHT = (198, 190, 170)
RED = (172, 38, 44)
NAVY = (22, 52, 92)
GREEN = (16, 122, 62)
GREEN_LT = (64, 199, 120)
TEAL = (13, 106, 100)
BROWN = (146, 84, 24)
PANEL = (16, 26, 22)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SANS_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
SANS_XB = "/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_COND_B = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(f, s):
    return d.textlength(s, font=f)


def wrap(f, s, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(f, t) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(x, y, f, s, max_w, leading, color=INK):
    for line in wrap(f, s, max_w):
        d.text((x, y), line, font=f, fill=color)
        y += leading
    return y


def kicker(x, y, s, color):
    f = F(SANS_XB, 19)
    d.text((x, y), s, font=f, fill=color)
    return tw(f, s)


def headline(x, y, s, size, max_w, color=INK):
    f = F(SERIF_BLACK, size)
    return para(x, y, f, s, max_w, int(size * 1.04), color)


M = 44  # page margin

# ---------------------------------------------------------------- masthead
d.text((M, 26), "THE WORLD IN ONE PICTURE", font=F(SANS_XB, 21), fill=GRAY)
dateline = "MONDAY  •  23 NOVEMBER 2026"
f_date = F(SANS_BLACK, 25)
d.text((W - M - tw(f_date, dateline), 22), dateline, font=f_date, fill=RED)
d.line([(M, 62), (W - M, 62)], fill=RULE, width=5)
d.line([(M, 71), (W - M, 71)], fill=RULE, width=2)

# ---------------------------------------------------------------- lead story
y = 88
kicker(M, y, "THE DAY'S BIG STORY  —  MARKETS", RED)
y += 32
y = headline(M, y, "HUANG IS BACK AT NVIDIA", 64, 620)
y += 6
y = para(M, y, F(SANS, 23),
         "Eleven days after resigning in scandal, Jensen Huang returns as CEO of the "
         "chipmaker he founded — and Nvidia leaps 31% in a historic rally.", 600, 30)

# chart panel (right of the lead)
cx0, cy0, cx1, cy1 = 668, 88, W - M, 348
d.rectangle([cx0, cy0, cx1, cy1], fill=PANEL)
d.text((cx0 + 16, cy0 + 10), "NVIDIA — MONDAY", font=F(SANS_B, 17), fill=(168, 178, 170))
pts = [(cx0 + 14, cy1 - 66), (cx0 + 60, cy1 - 60), (cx0 + 104, cy1 - 84), (cx0 + 146, cy1 - 74),
       (cx0 + 188, cy1 - 110), (cx0 + 228, cy1 - 128), (cx0 + 262, cy1 - 176), (cx0 + 298, cy1 - 208)]
d.line(pts, fill=GREEN_LT, width=5, joint="curve")
for gx in range(4):
    gy = cy1 - 40 - gx * 52
    d.line([(cx0 + 12, gy), (cx1 - 12, gy)], fill=(44, 58, 50), width=1)
d.polygon([(298 + cx0 - 9, cy1 - 208 - 12), (298 + cx0 + 12, cy1 - 208 + 3), (298 + cx0 - 12, cy1 - 208 + 8)], fill=GREEN_LT)
d.text((cx0 + 16, cy1 - 40), "after the board rehires", font=F(SANS, 15), fill=(168, 178, 170))
d.text((cx0 + 16, cy1 - 22), "its founder as CEO", font=F(SANS, 15), fill=(168, 178, 170))

d.line([(M, 366), (W - M, 366)], fill=RULE, width=2)

# ---------------------------------------------------------------- middle row: two war stories
y = 384
col_w = (W - 2 * M - 28) // 2
x2 = M + col_w + 28
kicker(M, y, "WAR AT SEA", NAVY)
headline(M, y + 28, "UKRAINE SINKS RUSSIAN CORVETTE IN LIBYA", 30, col_w)
para(M, y + 122, F(SANS, 20),
     "Seven naval drones sink the Merkury in a Libyan port, Zelenskyy announces — "
     "Kyiv's war leaps a thousand miles beyond Europe's shores.", col_w, 25)
kicker(x2, y, "STRAIT OF HORMUZ", TEAL)
headline(x2, y + 28, "IRAN VOWS TO BREAK THE US BLOCKADE", 30, col_w)
para(x2, y + 122, F(SANS, 20),
     "Tehran says it will use all its tools against the naval blockade. Trump, "
     "unmoved, hints at strikes after New Year if no deal is reached.", col_w, 25)
d.line([(M + col_w + 14, y), (M + col_w + 14, y + 196)], fill=LIGHT, width=2)
d.line([(M, y + 208), (W - M, y + 208)], fill=RULE, width=2)

# ---------------------------------------------------------------- bottom row: three stories
y = 616
c3 = (W - 2 * M - 2 * 24) // 3
cols = [
    ("CLIMATE", BROWN, "COP31 ENDS WITHOUT A DEAL",
     "The UN climate summit in Turkey collapses over fossil fuels and money — "
     "what one delegate calls diplomacy's darkest moment."),
    ("UKRAINE", NAVY, "DYMER STRIKE KILLS AT LEAST 11",
     "A Russian strike flattens an apartment block in Dymer, near Kyiv. In Kryvyi "
     "Rih, a child and a young woman are also killed."),
    ("DISASTER", RED, "FACTORY FIRE KILLS 24 IN INDONESIA",
     "A blaze sweeps a candy factory in Banten. Rescuers search the ruins for "
     "dozens still missing as families wait outside."),
]
for i, (kick, color, head, body) in enumerate(cols):
    x = M + i * (c3 + 24)
    kicker(x, y, kick, color)
    headline(x, y + 27, head, 24, c3)
    para(x, y + 27 + (52 if len(head) < 24 else 78), F(SANS, 18), body, c3, 23)
    if i:
        d.line([(x - 12, y), (x - 12, y + 218)], fill=LIGHT, width=2)
d.line([(M, y + 232), (W - M, y + 232)], fill=RULE, width=2)

# ---------------------------------------------------------------- ticker
y = y + 248
d.text((M, y), "ALSO TODAY", font=F(SANS_XB, 19), fill=RED)
ticker = ("CrowdStrike buys Zscaler in a $44bn cyber deal  •  Bitcoin back above $61,000 after a "
          "two-year low  •  BepiColombo slips into orbit around Mercury  •  Kilauea's lava fountain "
          "lights up Hawaii  •  Belgium strike grounds flights  •  FBI fugitive 'El Chapo Isidro' "
          "captured in Sinaloa  •  Kenya and DR Congo restore ties")
para(M, y + 28, F(SANS_COND_B, 21), ticker, W - 2 * M, 26, GRAY)

# footer line
d.line([(M, H - 40), (W - M, H - 40)], fill=RULE, width=2)
d.text((M, H - 32), "The day's world news, summed up in one image — Monday 23 November 2026.", font=F(SANS, 16), fill=GRAY)

img.save("/home/hatch/workspace/makefun/news23/entry.png")
print("saved")
