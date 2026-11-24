#!/usr/bin/env python3
"""Draw the front page of Monday 23 November 2026 as a single PNG.

The page is a broadsheet: a dated masthead, one dominant lead story with its own
chart panel, two war stories side by side, three shorter briefs, and a ticker of
the day's remaining headlines. Every story was reported on 23 November 2026 and
cross-checked across the day's wires and roundups before a word was drawn.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 44

PALETTE = {
    "paper": (246, 241, 230),
    "ink": (18, 20, 24),
    "muted": (80, 84, 88),
    "rule": (30, 30, 34),
    "hairline": (198, 190, 170),
    "red": (172, 38, 44),
    "navy": (22, 52, 92),
    "teal": (13, 106, 100),
    "brown": (146, 84, 24),
    "panel": (16, 26, 22),
    "panel_grid": (44, 58, 50),
    "panel_text": (168, 178, 170),
    "chart": (64, 199, 120),
}

FONT_FILES = {
    "serif": "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf",
    "black": "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf",
    "xbold": "/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf",
    "bold": "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "text": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "cond": "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf",
}

_font_cache = {}


def font(kind, size):
    key = (kind, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_FILES[kind], size)
    return _font_cache[key]


def break_lines(draw, fnt, text, width):
    """Greedy word wrap measured with the font's own advance widths."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def flow(draw, x, y, fnt, text, width, leading, fill):
    """Draw wrapped text downward from (x, y); return the y below it."""
    for line in break_lines(draw, fnt, text, width):
        draw.text((x, y), line, font=fnt, fill=fill)
    return y + leading * len(break_lines(draw, fnt, text, width))


def section_tag(draw, x, y, label, color):
    draw.text((x, y), label, font=font("xbold", 19), fill=color)


def big_headline(draw, x, y, text, size, width):
    return flow(draw, x, y, font("serif", size), text, width, round(size * 1.04), PALETTE["ink"])


def masthead(draw):
    draw.text((MARGIN, 26), "THE WORLD IN ONE PICTURE", font=font("xbold", 21), fill=PALETTE["muted"])
    date_text = "MONDAY  •  23 NOVEMBER 2026"
    date_font = font("black", 25)
    draw.text((PAGE_W - MARGIN - draw.textlength(date_text, font=date_font), 22),
              date_text, font=date_font, fill=PALETTE["red"])
    draw.line([(MARGIN, 62), (PAGE_W - MARGIN, 62)], fill=PALETTE["rule"], width=5)
    draw.line([(MARGIN, 71), (PAGE_W - MARGIN, 71)], fill=PALETTE["rule"], width=2)


def chart_panel(draw):
    x0, y0, x1, y1 = 668, 88, PAGE_W - MARGIN, 348
    draw.rectangle([x0, y0, x1, y1], fill=PALETTE["panel"])
    draw.text((x0 + 16, y0 + 10), "NVIDIA — MONDAY", font=font("bold", 17), fill=PALETTE["panel_text"])
    for step in range(4):
        gy = y1 - 40 - step * 52
        draw.line([(x0 + 12, gy), (x1 - 12, gy)], fill=PALETTE["panel_grid"], width=1)
    climb = [(x0 + 14, y1 - 66), (x0 + 60, y1 - 60), (x0 + 104, y1 - 84), (x0 + 146, y1 - 74),
             (x0 + 188, y1 - 110), (x0 + 228, y1 - 128), (x0 + 262, y1 - 176), (x0 + 298, y1 - 208)]
    draw.line(climb, fill=PALETTE["chart"], width=5, joint="curve")
    tip_x, tip_y = x0 + 298, y1 - 208
    draw.polygon([(tip_x - 9, tip_y - 12), (tip_x + 12, tip_y + 3), (tip_x - 12, tip_y + 8)], fill=PALETTE["chart"])
    draw.text((x0 + 16, y1 - 40), "after the board rehires", font=font("text", 15), fill=PALETTE["panel_text"])
    draw.text((x0 + 16, y1 - 22), "its founder as CEO", font=font("text", 15), fill=PALETTE["panel_text"])


def lead_story(draw):
    y = 88
    section_tag(draw, MARGIN, y, "THE DAY'S BIG STORY  —  MARKETS", PALETTE["red"])
    y = big_headline(draw, MARGIN, y + 32, "HUANG IS BACK AT NVIDIA", 64, 620)
    flow(draw, MARGIN, y + 6, font("text", 23),
         "Eleven days after resigning in scandal, Jensen Huang returns as CEO of the "
         "chipmaker he founded — and Nvidia leaps 31% in a historic rally.",
         600, 30, PALETTE["ink"])
    chart_panel(draw)
    draw.line([(MARGIN, 366), (PAGE_W - MARGIN, 366)], fill=PALETTE["rule"], width=2)


def war_stories(draw):
    top = 384
    col_w = (PAGE_W - 2 * MARGIN - 28) // 2
    right_x = MARGIN + col_w + 28
    section_tag(draw, MARGIN, top, "WAR AT SEA", PALETTE["navy"])
    big_headline(draw, MARGIN, top + 28, "UKRAINE SINKS RUSSIAN CORVETTE IN LIBYA", 30, col_w)
    flow(draw, MARGIN, top + 122, font("text", 20),
         "Seven naval drones sink the Merkury in a Libyan port, Zelenskyy announces — "
         "Kyiv's war leaps a thousand miles beyond Europe's shores.", col_w, 25, PALETTE["ink"])
    section_tag(draw, right_x, top, "STRAIT OF HORMUZ", PALETTE["teal"])
    big_headline(draw, right_x, top + 28, "IRAN VOWS TO BREAK THE US BLOCKADE", 30, col_w)
    flow(draw, right_x, top + 122, font("text", 20),
         "Tehran says it will use all its tools against the naval blockade. Trump, "
         "unmoved, hints at strikes after New Year if no deal is reached.", col_w, 25, PALETTE["ink"])
    draw.line([(MARGIN + col_w + 14, top), (MARGIN + col_w + 14, top + 196)], fill=PALETTE["hairline"], width=2)
    draw.line([(MARGIN, top + 208), (PAGE_W - MARGIN, top + 208)], fill=PALETTE["rule"], width=2)


BRIEFS = [
    ("CLIMATE", "brown", "COP31 ENDS WITHOUT A DEAL",
     "The UN climate summit in Turkey collapses over fossil fuels and money — "
     "what one delegate calls diplomacy's darkest moment."),
    ("UKRAINE", "navy", "DYMER STRIKE KILLS AT LEAST 11",
     "A Russian strike flattens an apartment block in Dymer, near Kyiv. In Kryvyi "
     "Rih, a child and a young woman are also killed."),
    ("DISASTER", "red", "FACTORY FIRE KILLS 24 IN INDONESIA",
     "A blaze sweeps a candy factory in Banten. Rescuers search the ruins for "
     "dozens still missing as families wait outside."),
]


def brief_stories(draw):
    top = 616
    col_w = (PAGE_W - 2 * MARGIN - 2 * 24) // 3
    for idx, (tag, color_key, head, body) in enumerate(BRIEFS):
        x = MARGIN + idx * (col_w + 24)
        section_tag(draw, x, top, tag, PALETTE[color_key])
        big_headline(draw, x, top + 27, head, 24, col_w)
        body_y = top + 27 + (52 if len(head) < 24 else 78)
        flow(draw, x, body_y, font("text", 18), body, col_w, 23, PALETTE["ink"])
        if idx:
            draw.line([(x - 12, top), (x - 12, top + 218)], fill=PALETTE["hairline"], width=2)
    draw.line([(MARGIN, top + 232), (PAGE_W - MARGIN, top + 232)], fill=PALETTE["rule"], width=2)


def ticker_and_footer(draw):
    top = 616 + 248
    draw.text((MARGIN, top), "ALSO TODAY", font=font("xbold", 19), fill=PALETTE["red"])
    items = ("CrowdStrike buys Zscaler in a $44bn cyber deal  •  Bitcoin back above $61,000 after a "
             "two-year low  •  BepiColombo slips into orbit around Mercury  •  Kilauea's lava fountain "
             "lights up Hawaii  •  Belgium strike grounds flights  •  FBI fugitive 'El Chapo Isidro' "
             "captured in Sinaloa  •  Kenya and DR Congo restore ties")
    flow(draw, MARGIN, top + 28, font("cond", 21), items, PAGE_W - 2 * MARGIN, 26, PALETTE["muted"])
    draw.line([(MARGIN, PAGE_H - 40), (PAGE_W - MARGIN, PAGE_H - 40)], fill=PALETTE["rule"], width=2)
    draw.text((MARGIN, PAGE_H - 32),
              "The day's world news, summed up in one image — Monday 23 November 2026.",
              font=font("text", 16), fill=PALETTE["muted"])


def main():
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["paper"])
    draw = ImageDraw.Draw(canvas)
    masthead(draw)
    lead_story(draw)
    war_stories(draw)
    brief_stories(draw)
    ticker_and_footer(draw)
    canvas.save("/home/hatch/workspace/makefun/news23/entry.png")
    print("saved entry.png")


if __name__ == "__main__":
    main()
