#!/usr/bin/env python3
"""Draw entry.png for news-image-20261123 with Pillow (build-time only).

Slate verified 2026-11-24 against multiple sources (Shadow briefing,
Principia, 10things, Off the Wire, BBC) for Monday 23 November 2026.
Every number on the image comes from those reports; no faces, no leader
likenesses, flat vector pictograms only.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.expanduser("~/workspace/bountyhawk/news-image-20261123-entry/entry.png")
W = H = 1024
BG = (247, 243, 232)
NAVY = (15, 42, 68)
INK = (20, 24, 30)
GREY = (70, 75, 85)
RED = (178, 34, 34)
TEAL = (0, 110, 110)
GOLD = (186, 132, 0)
GREEN = (34, 120, 60)
WHITE = (255, 255, 255)
GOLDLT = (255, 214, 90)
LINE = (210, 205, 190)


def font(size, bold=True):
    p = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(p, size)


def wrap(draw, text, fnt, max_w, x, y, fill, spacing=4):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- masthead ---
d.rectangle([0, 0, W, 150], fill=NAVY)
d.text((36, 18), "THE WORLD IN ONE DAY", font=font(42), fill=WHITE)
d.text((36, 74), "MONDAY  23  NOVEMBER  2026", font=font(36), fill=GOLDLT)
d.text((36, 122), "World news, summed up in one image", font=font(19, False),
       fill=(200, 215, 230))
# small globe pictogram, top right
cx, cy = 940, 75
d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], outline=GOLDLT, width=4)
d.ellipse([cx - 22, cy - 42, cx + 22, cy + 42], outline=GOLDLT, width=2)
d.line([cx - 42, cy, cx + 42, cy], fill=GOLDLT, width=2)

# --- lead panel: COP31 ends with no deal ---
lx, ly, lw, lh = 36, 168, 952, 216
d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=WHITE,
                    outline=LINE, width=2)
d.rounded_rectangle([lx, ly, lx + lw, ly + 40], radius=16, fill=GREEN)
d.rectangle([lx, ly + 26, lx + lw, ly + 40], fill=GREEN)
d.text((lx + 16, ly + 8), "LEAD  •  CLIMATE  •  COP31", font=font(19), fill=WHITE)
# globe pictogram with a crack (no deal)
gx, gy = lx + 78, ly + 122
d.ellipse([gx - 52, gy - 52, gx + 52, gy + 52], outline=GREEN, width=5)
d.ellipse([gx - 26, gy - 52, gx + 26, gy + 52], outline=GREEN, width=2)
d.line([gx - 52, gy, gx + 52, gy], fill=GREEN, width=2)
d.line([gx - 8, gy - 52, gx + 12, gy - 10, gx - 6, gy + 26, gx + 10, gy + 52],
       fill=RED, width=4)
wrap(d, "COP31 ends with no deal", font(33), 640, lx + 168, ly + 58, INK)
wrap(d, "Record-long climate talks in Antalya collapse over fossil fuels "
        "and finance — the longest UN climate conference ever.",
     font(19, False), 640, lx + 168, ly + 122, GREY)

# --- six panels ---
def card(x, y, w, h, accent, tag, headline, sub):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=WHITE,
                        outline=LINE, width=2)
    d.rounded_rectangle([x, y, x + w, y + 34], radius=14, fill=accent)
    d.rectangle([x, y + 20, x + w, y + 34], fill=accent)
    d.text((x + 14, y + 6), tag, font=font(16), fill=WHITE)
    y2 = wrap(d, headline, font(21), w - 28, x + 14, y + 44, INK)
    wrap(d, sub, font(15, False), w - 28, x + 14, y2 + 6, GREY)


stories = [
    (RED, "POLAND  •  NATO",
     "Debris at all three crash sites was Russian",
     "Polish prosecutors: wreckage came from Kh-101 cruise missiles; "
     "NATO sends early-warning aircraft."),
    (NAVY, "UKRAINE  •  LIBYA",
     "Ukraine says drones sank a Russian warship",
     "Naval drones sank the corvette Merkury at Benghazi, Libya, "
     "Zelenskyy confirmed."),
    (RED, "UKRAINE",
     "Strikes kill at least 15 around Kyiv",
     "Russian attacks hit the capital region as the war grinds on."),
    (GOLD, "INDONESIA",
     "Candy factory fire kills at least 24",
     "Blaze in Banten leaves about 30 missing; rescuers search the ruins."),
    (TEAL, "SPACE",
     "BepiColombo reaches Mercury",
     "ESA-JAXA spacecraft enters orbit after an eight-year journey."),
    (GREEN, "TRADE  •  EU",
     "EU and Indonesia sign landmark deal",
     "Trade pact sealed after years of talks; tariffs to fall."),
]
cw, ch, gap = 304, 186, 20
for i, (accent, tag, head, sub) in enumerate(stories):
    x = 36 + (i % 3) * (cw + gap)
    y = 404 + (i // 3) * (ch + gap)
    card(x, y, cw, ch, accent, tag, head, sub)

# --- bottom strip ---
by = 404 + 2 * ch + gap + 16
d.rounded_rectangle([36, by, 988, by + 96], radius=14, fill=NAVY)
d.text((56, by + 12), "ALSO ON 23 NOVEMBER", font=font(19), fill=GOLDLT)
wrap(d, "FBI probes hack of national crime database  •  NHS starts AI trial "
        "in breast cancer screening  •  Euro area inflation rises to 4.0%",
     font(18, False), 900, 56, by + 44, WHITE)
d.text((36, 994), "Events reported on Monday 23 November 2026  •  One day, one image",
       font=font(15, False), fill=(110, 110, 110))

img.save(OUT, optimize=True)
print("saved", img.size, os.path.getsize(OUT), "bytes")
