#!/usr/bin/env python3
"""Render the 27 November 2026 world-news poster (1024x1024 PNG).

Fresh design for news-image-20261127. All copy is factual, sourced from
BBC / Reuters / CNN / Al Jazeera reporting on the morning of 27 Nov 2026.
No speculation, no hype. Deterministic: no timestamps, no randomness.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/home/hatch/workspace/makefun/news-image-20261127/entry.png"

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF_B, 46)
F_DATE = font(SANS_B, 40)
F_SUB = font(SANS, 21)
F_TAG = font(SANS_B, 19)
F_HEAD = font(SANS_B, 25)
F_BODY = font(SANS, 20)
F_STRIP = font(SANS, 19)
F_STRIP_B = font(SANS_B, 19)
F_FOOT = font(SANS, 17)

BG = (13, 22, 38)          # deep navy
HEADER_BG = (13, 22, 38)
CARD = (255, 255, 255)
INK = (18, 28, 46)
MUTED = (92, 102, 118)
ACCENT = (214, 48, 49)     # red accent
GOLD = (233, 180, 76)
STRIP_BG = (240, 242, 245)

CARDS = [
    ("KUWAIT  •  MIDDLE EAST", (178, 34, 34),
     "Drone strike kills two Italians",
     "Two Rheinmetall technicians died at a Kuwaiti air-defence station "
     "in a drone attack Italy and Kuwait blame on Iran. Tehran denies it."),
    ("EUROPE  •  BRUSSELS", (27, 84, 160),
     "EU split over budget and Ukraine loan",
     "Leaders struggle to agree a long-term budget and a $49bn loan for "
     "Ukraine as the war drags on."),
    ("GAZA  •  CEASEFIRE UNDER STRAIN", (122, 54, 148),
     "Israeli strike kills Hamas official",
     "A strike killed a Hamas official, his wife and children. Hamas weighs "
     "its response as the ceasefire frays."),
    ("BANGKOK  •  THAILAND", (196, 96, 12),
     "Blast and fire at oil refinery",
     "An explosion at Bangchak's Phra Khanong refinery injured at least nine "
     "people and forced nearby residents to evacuate."),
    ("BRITAIN  •  DEFENCE", (16, 120, 90),
     "Reservists called up over Russia threat",
     "Britain calls up military reservists for the first time since the Cold "
     "War amid the threat from Russia."),
    ("UNITED STATES  •  THANKSGIVING", (58, 90, 160),
     "Storm halts 100th Macy's parade",
     "A severe storm postponed New York's 100th Thanksgiving Day parade and "
     "left over half a million homes without power."),
]

STRIP = [
    ("CHESS", "Gukesh–Sindarov draw Game 3"),
    ("COURTS", "Depardieu to stand trial"),
    ("UK", "Net migration lowest since 1997"),
    ("MYANMAR", "Defies parts of ICJ ruling"),
    ("NORTH KOREA", "Kim vows more nukes"),
]


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=width) or [""])
    # re-wrap by pixel width
    out = []
    for line in lines:
        words, cur = line.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 168], fill=HEADER_BG)
    d.rectangle([0, 168, W, 174], fill=ACCENT)
    d.text((36, 26), "THE WORLD IN ONE DAY", font=F_TITLE, fill=(255, 255, 255))
    d.text((36, 98), "27 November 2026", font=F_DATE, fill=GOLD)
    d.text((36, 140), "Six stories that defined the day  •  Friday",
           font=F_SUB, fill=(190, 198, 210))
    # date badge, right side
    d.rounded_rectangle([856, 30, 988, 132], radius=12,
                        outline=GOLD, width=3)
    d.text((922, 44), "27", font=font(SERIF_B, 44),
           fill=(255, 255, 255), anchor="ma")
    d.text((922, 96), "NOV 2026", font=F_TAG, fill=GOLD, anchor="ma")

    # ---- cards: 2 columns x 3 rows ----
    margin, gap = 28, 16
    cw = (W - 2 * margin - gap) // 2
    ch = 208
    top = 182
    for i, (tag, color, head, body) in enumerate(CARDS):
        col, row = i % 2, i // 2
        x0 = margin + col * (cw + gap)
        y0 = top + row * (ch + gap)
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], radius=14, fill=CARD)
        d.rectangle([x0, y0, x0 + 8, y0 + ch], fill=color)
        d.text((x0 + 24, y0 + 16), tag, font=F_TAG, fill=color)
        head_lines = wrap(d, head, F_HEAD, cw - 48)
        y = y0 + 46
        for ln in head_lines[:2]:
            d.text((x0 + 24, y), ln, font=F_HEAD, fill=INK)
            y += 30
        body_lines = wrap(d, body, F_BODY, cw - 48)
        y += 6
        for ln in body_lines[:3]:
            d.text((x0 + 24, y), ln, font=F_BODY, fill=MUTED)
            y += 25

    # ---- also in the news strip (two columns) ----
    sy = top + 3 * ch + 2 * gap + 12
    d.rectangle([0, sy, W, sy + 40], fill=ACCENT)
    d.text((36, sy + 9), "ALSO IN THE NEWS", font=F_TAG, fill=(255, 255, 255))
    y = sy + 50
    for i, (tag, text) in enumerate(STRIP):
        col = i // 3
        row = i % 3
        sx = 36 if col == 0 else 540
        syy = y + row * 24
        d.text((sx, syy), tag + "  —  ", font=F_STRIP_B, fill=(255, 255, 255))
        tw = d.textlength(tag + "  —  ", font=F_STRIP_B)
        d.text((sx + tw, syy), text, font=F_STRIP, fill=(196, 204, 216))

    # ---- footer ----
    d.text((36, H - 26),
           "Sources: BBC, Reuters, CNN, Al Jazeera  •  Events as reported on 27 November 2026",
           font=F_FOOT, fill=(150, 160, 175))

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
