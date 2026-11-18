#!/usr/bin/env python3
"""Compose the news-image-20261118 front page (1024x1024) from the six
panel illustrations in assets/ plus PIL-rendered text. All text is drawn
here from real fonts; the generated illustrations contain no text.

Layout (1024 tall): masthead 0-117, hero 124-392, row2 400-652,
row3 660-875, ticker 884-1024.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ASSETS = os.path.join(REPO, "assets")

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (155, 28, 28)
NAVY = (20, 33, 61)
GOLD = (212, 175, 55)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def crop_to(img, tw, th, focus_y=0.5, focus_x=0.5):
    """Center-crop (with focus point) to the target aspect, then resize."""
    iw, ih = img.size
    target = tw / th
    cur = iw / ih
    if cur > target:  # too wide: crop width
        nw = int(ih * target)
        x0 = int((iw - nw) * focus_x)
        img = img.crop((x0, 0, x0 + nw, ih))
    else:  # too tall: crop height
        nh = int(iw / target)
        y0 = int((ih - nh) * focus_y)
        y0 = max(0, min(y0, ih - nh))
        img = img.crop((0, y0, iw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def wrap(drw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if drw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(canvas, drw, fname, x, y, w, img_h, kicker, headline, subhead,
          head_size, sub_size, focus_y=0.5, focus_x=0.5, max_head_lines=2):
    pic = crop_to(Image.open(os.path.join(ASSETS, fname)).convert("RGB"),
                  w, img_h, focus_y, focus_x)
    canvas.paste(pic, (x, y))
    drw.rectangle([x, y, x + w - 1, y + img_h - 1], outline=(0, 0, 0), width=1)
    ty = y + img_h + 8
    drw.text((x, ty), kicker, font=font(SANS_BOLD, 13), fill=RED)
    ty += 20
    hl = wrap(drw, headline, font(SERIF_BOLD, head_size), w)[:max_head_lines]
    for ln in hl:
        drw.text((x, ty), ln, font=font(SERIF_BOLD, head_size), fill=INK)
        ty += head_size + 4
    ty += 2
    for ln in wrap(drw, subhead, font(SANS, sub_size), w):
        drw.text((x, ty), ln, font=font(SANS, sub_size), fill=(40, 40, 40))
        ty += sub_size + 5
    return ty


img = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(img)

# ---- Masthead ----
draw.text((W // 2, 12), "THE WORLD IN ONE DAY",
          font=font(SERIF_BLACK, 58), fill=INK, anchor="ma")
draw.text((W // 2, 78), "WEDNESDAY, 18 NOVEMBER 2026",
          font=font(SERIF_BOLD, 26), fill=INK, anchor="ma")
draw.line([(16, 112), (W - 16, 112)], fill=INK, width=3)
draw.line([(16, 117), (W - 16, 117)], fill=INK, width=1)

# ---- Hero: EU loan ----
panel(img, draw, "media-generation-panel-eu-0-944d9c42-c269-42d7-a490-c7f2fb49dc92.webp",
      16, 124, 992, 160,
      "EUROPE — UKRAINE",
      "EU unveils €45bn loan for Ukraine",
      "Brussels presents a €45bn loan to cover two-thirds of Kyiv's €70bn gap for 2027; "
      "Kyiv repays only if Russia pays reparations. Leaders debate it on 26–27 Nov.",
      34, 16, focus_y=0.58)

# ---- Row 2: three panels ----
y2 = 400
panel(img, draw, "media-generation-panel-manila-0-c41093c5-650a-467f-9111-2c8b9ba62aa8.webp",
      16, y2, 320, 115,
      "ASIA — MANILA",
      "Trump meets Marcos in Manila",
      "Bilateral talks at Malacañang, then on to Shenzhen for APEC; the Xi–Trump–Putin "
      "summit is set for Thursday. Pax Silica was not signed.",
      22, 14, focus_x=0.5)
panel(img, draw, "media-generation-panel-cyclone-0-976a8f75-b047-4297-9fdc-cd66374ec13e.webp",
      352, y2, 320, 115,
      "WEATHER — INDIA",
      "Cyclone Akvan bears down on India",
      "Now a severe cyclonic storm, it brings heavy rain to India's east coast; landfall "
      "is forecast for Friday, with winds up to 145 km/h.",
      22, 14, focus_y=0.45)
panel(img, draw, "media-generation-panel-gta-0-e9fe4ec6-a41b-45f0-947f-7affd62a6ad0.webp",
      688, y2, 320, 115,
      "GAMES",
      "GTA VI reviews land, launch looms",
      "Reviews are reportedly out today, a day before release; New Zealand unlocks first "
      "at 11:00 UTC. Pre-orders are the biggest ever.",
      22, 14, focus_x=0.5)

# ---- Row 3: two panels ----
y3 = 660
panel(img, draw, "media-generation-panel-nvidia-0-bf2ebba0-a99d-414b-b1be-d28839e22654.webp",
      16, y3, 488, 105,
      "MARKETS",
      "Nvidia shares climb after record quarter",
      "Shares rose 3–4% after hours on $115.8bn sales, up 103%.",
      24, 14, focus_y=0.5)
panel(img, draw, "media-generation-panel-gulf-0-8fc068f9-3263-4a23-a47e-9c80c8162c27.webp",
      520, y3, 488, 105,
      "MIDDLE EAST",
      "Gulf on edge as US and Iran trade fire",
      "A third US carrier, the USS Theodore Roosevelt, is in the region as the blockade "
      "holds and Oman and Qatar mediate after Tuesday's strikes.",
      24, 14, focus_y=0.72)

# ---- Ticker ----
ty = 884
draw.rectangle([0, ty, W, H], fill=NAVY)
draw.text((16, ty + 12), "ALSO TODAY", font=font(SANS_BOLD, 15), fill=GOLD)
ticker = [
    "Trump flies to Shenzhen for APEC; Xi–Trump–Putin summit Thursday",
    "Cyclone Akvan: seas very rough, fishermen warned off, 18–20 Nov",
    "GTA VI unlocks first in New Zealand tonight; US at midnight ET",
]
yy = ty + 38
for t in ticker:
    draw.text((16, yy), "•", font=font(SANS_BOLD, 15), fill=GOLD)
    draw.text((36, yy), t, font=font(SANS, 15), fill=(235, 235, 235))
    yy += 28

img.save(os.path.join(REPO, "entry.png"), optimize=True)
print("saved entry.png", img.size)
