#!/usr/bin/env python3
"""Compose the front page for Friday 20 November 2026.

Draws a one-page newspaper, "The Daily Signal", that sums up the day's
world news in a single 1024x1024 image: a masthead carrying the date, a
hero panel for the Shenzhen trilateral summit, three panels for the
Anthropic market debut, the World Court's Rohingya ruling and the
Hormuz escalation, and a footer ticker with five shorter items.

Everything is drawn with PIL shapes and type -- no photographs and no
outside assets -- and the finished page is written to entry.png beside
this script.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Canvas and palette: warm paper, near-black ink, one red, one deep blue.
SIZE = 1024
MARGIN = 40
WIDTH = SIZE - 2 * MARGIN

PAPER = (250, 246, 236)
INK = (22, 21, 24)
SOFT = (52, 50, 48)
RED = (178, 32, 38)
BLUE = (26, 54, 112)
WHITE = (248, 246, 240)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = FONT_DIR / "DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
SERIF_ITALIC = Path(
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
)


def font(path, size):
    return ImageFont.truetype(str(path), size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap measured with the real font metrics."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if current and draw.textlength(trial, font=fnt) > max_width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def fit(draw, text, path, max_width, start, minimum=20):
    """Largest size, from start down, at which text fits on one line."""
    size = start
    while size > minimum and draw.textlength(text, font=font(path, size)) > max_width:
        size -= 1
    return font(path, size)


def centered(draw, y, text, fnt, fill=INK):
    """Draw text centred on the page; return the bottom of its glyphs."""
    draw.text((SIZE // 2, y), text, font=fnt, fill=fill, anchor="ma")
    return draw.textbbox((SIZE // 2, y), text, font=fnt, anchor="ma")[3]


def tracked(draw, x, y, text, fnt, fill, tracking=3):
    """Draw letter-spaced text (for kickers); return its right edge."""
    cursor = x
    for ch in text:
        draw.text((cursor, y), ch, font=fnt, fill=fill)
        cursor += draw.textlength(ch, font=fnt) + tracking
    return cursor - tracking


def star(draw, cx, cy, radius, fill):
    points = []
    for i in range(10):
        r = radius if i % 2 == 0 else radius * 0.42
        angle = -math.pi / 2 + i * math.pi / 5
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)


# --- the three flags of the summit table --------------------------------

def flag_united_states(draw, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        fill = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=fill)
    canton_w, canton_h = w * 0.45, stripe * 4
    draw.rectangle([x, y, x + canton_w, y + canton_h], fill=(60, 59, 110))
    for row in range(4):
        for col in range(5):
            cx = x + (col + 0.5) * canton_w / 5
            cy = y + (row + 0.5) * canton_h / 4
            draw.ellipse([cx - 2.2, cy - 2.2, cx + 2.2, cy + 2.2], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.18, y + h * 0.28, h * 0.17, (255, 222, 0))
    for dx, dy in ((0.35, 0.12), (0.39, 0.30), (0.35, 0.47), (0.28, 0.58)):
        star(draw, x + w * dx, y + h * dy, h * 0.06, (255, 222, 0))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def flag_russia(draw, x, y, w, h):
    band = h / 3
    for i, fill in enumerate(((255, 255, 255), (0, 57, 166), (213, 43, 30))):
        draw.rectangle([x, y + i * band, x + w, y + (i + 1) * band], fill=fill)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def summit_graphic(draw, top):
    """Three flags on poles above a summit table, with name labels."""
    flag_w, flag_h = 126, 64
    centers = (212, 512, 812)
    flags = (flag_united_states, flag_china, flag_russia)
    labels = ("UNITED STATES", "CHINA", "RUSSIA")
    table_y = top + flag_h + 22
    for cx, draw_flag in zip(centers, flags):
        draw.line([cx, top - 4, cx, table_y], fill=INK, width=4)
        draw_flag(draw, cx - flag_w // 2, top, flag_w, flag_h)
        draw.ellipse(
            [cx - 11, table_y - 26, cx + 11, table_y - 4], fill=INK
        )
    draw.rectangle([110, table_y, SIZE - 110, table_y + 13], fill=BLUE)
    label_font = font(SANS_BOLD, 21)
    for cx, label in zip(centers, labels):
        draw.text((cx, table_y + 20), label, font=label_font, fill=INK, anchor="ma")
    return table_y + 45


# --- page sections --------------------------------------------------------

def masthead(draw):
    y = 38
    draw.line([MARGIN, y, SIZE - MARGIN, y], fill=INK, width=3)
    title_font = fit(draw, "THE DAILY SIGNAL", SERIF_BOLD, 900, 98)
    y = centered(draw, y + 10, "THE DAILY SIGNAL", title_font) + 8
    draw.line([MARGIN, y, SIZE - MARGIN, y], fill=INK, width=2)
    y = centered(draw, y + 8, "FRIDAY · 20 NOVEMBER 2026", font(SANS_BOLD, 38), fill=RED)
    draw.rectangle([MARGIN, y + 10, SIZE - MARGIN, y + 17], fill=INK)
    return y + 26


def hero(draw, y):
    tracked(draw, MARGIN, y, "SHENZHEN · FIRST TRILATERAL SUMMIT",
            font(SANS_BOLD, 26), RED)
    y += 34
    head_font = font(SANS_BOLD, 48)
    headline = "TRUMP, XI AND PUTIN HOLD FIRST TRILATERAL SUMMIT IN SHENZHEN"
    for line in wrap(draw, headline, head_font, WIDTH):
        draw.text((MARGIN, y), line, font=head_font, fill=INK)
        y += 55
    standfirst = ("Three leaders meet face to face and issue "
                  "a four-point peace declaration.")
    stand_font = fit(draw, standfirst, SERIF_ITALIC, WIDTH, 28)
    draw.text((MARGIN, y + 4), standfirst, font=stand_font, fill=SOFT)
    y += 33
    return summit_graphic(draw, y + 4)


def panel(draw, y, kicker, headline, standfirst):
    tracked(draw, MARGIN, y, kicker, font(SANS_BOLD, 21), BLUE)
    y += 26
    head_font = fit(draw, headline, SANS_BOLD, WIDTH, 34, 24)
    draw.text((MARGIN, y), headline, font=head_font, fill=INK)
    y += 33
    stand_font = fit(draw, standfirst, SERIF_ITALIC, WIDTH, 24)
    draw.text((MARGIN, y), standfirst, font=stand_font, fill=SOFT)
    return y + 31


def rule(draw, y):
    draw.line([MARGIN, y, SIZE - MARGIN, y], fill=INK, width=2)
    return y + 9


def footer(draw):
    lines = [
        "UK PLEDGES 1,000+ DRONES FOR UKRAINE IN A £260M PACKAGE",
        "UKRAINE HITS KERCH BRIDGE AGAIN · CYCLONE XAVIER IN THE PACIFIC",
        "EUROPEAN ALLIES IN BERLIN READY FOR TALKS WITH RUSSIA",
        "COP31 ROW: FOSSIL FUELS DROP FROM THE DRAFT DEAL",
    ]
    top = SIZE - 142
    draw.rectangle([26, top, SIZE - 26, SIZE - 26], fill=INK)
    y = top + 10
    for line in lines:
        fnt = fit(draw, line, SANS_BOLD, 920, 22)
        centered(draw, y, line, fnt, fill=WHITE)
        y += 26
    return SIZE - 26


def compose():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([16, 16, SIZE - 16, SIZE - 16], outline=INK, width=3)
    draw.rectangle([24, 24, SIZE - 24, SIZE - 24], outline=INK, width=1)

    y = masthead(draw)
    y = hero(draw, y)
    y = rule(draw, y + 2)
    y = panel(draw, y, "NEW YORK · MARKETS",
              "ANTHROPIC SOARS IN RECORD STOCK-MARKET DEBUT",
              "The first pure AI company to list jumps on day one, "
              "even as Wall Street slides.")
    y = rule(draw, y)
    y = panel(draw, y, "THE HAGUE · WORLD COURT",
              "ICJ RULES MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA",
              "The first such finding against a state, over the 2017 "
              "campaign; refugees cheer.")
    y = rule(draw, y)
    y = panel(draw, y, "STRAIT OF HORMUZ",
              "IRAN ESCALATES TANKER ATTACKS IN THE STRAIT OF HORMUZ",
              "A Houthi missile hits Riyadh's tallest tower.")
    footer(draw)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out)
    print(f"wrote {out} ({out.stat().st_size} bytes); panels ended at y={y}")


if __name__ == "__main__":
    compose()
