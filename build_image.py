#!/usr/bin/env python3
"""Build the VELMARA travel poster: a lantern-lit harbour town on a tideless
glass sea. Draws entry.png (1024x1024) with PIL. Deterministic, no network.
Run: python3 build_image.py
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
HORIZON = 560
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

CREAM = (255, 243, 214)
GOLD = (255, 196, 110)
AMBER = (255, 170, 80)
DEEP = (16, 22, 48)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0 - 1))
        draw.line([(x0, y), (x1, y)], fill=lerp(top, bottom, t))


def main():
    img = Image.new("RGB", (W, H), DEEP)
    d = ImageDraw.Draw(img)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)

    # --- sky: deep indigo -> violet -> warm amber at the horizon ---
    vgrad(d, (0, 0, W, HORIZON), (13, 18, 46), (64, 38, 84))
    vgrad(d, (0, 380, W, HORIZON), (64, 38, 84), (214, 128, 66))
    # sun glow + disc, low over the sea, left of centre
    sx, sy, sr = 380, 438, 74
    for r, a in ((260, 26), (200, 38), (150, 55), (110, 80)):
        od.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 190, 100, a))
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 226, 160))
    d.ellipse([sx - sr + 10, sy - sr + 10, sx + sr - 10, sy + sr - 10],
              fill=(255, 240, 200))
    # faint early stars high up
    import random
    rng = random.Random(20261121)
    for _ in range(70):
        x = rng.randint(20, W - 20)
        y = rng.randint(20, 300)
        r = rng.choice((1, 1, 2))
        a = rng.randint(60, 170)
        od.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 240, a))
    # a few birds
    for bx, by, s in ((700, 180, 16), (760, 210, 12), (650, 240, 10), (830, 150, 13)):
        d.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340, fill=(20, 24, 52), width=3)
        d.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340, fill=(20, 24, 52), width=3)

    # --- sea: dark teal-indigo with warm reflection streaks ---
    vgrad(d, (0, HORIZON, W, H), (38, 44, 84), (12, 18, 40))
    # sun road: shimmering gold dashes under the sun
    for i in range(46):
        y = HORIZON + 12 + i * 9
        spread = 26 + (y - HORIZON) * 0.55
        wdt = rng.randint(18, 70)
        cx = sx + rng.randint(-int(spread), int(spread))
        a = max(30, 190 - i * 3)
        od.line([(cx - wdt, y), (cx + wdt, y)], fill=(255, 196, 110, a), width=3)
    # faint cool streaks elsewhere
    for _ in range(60):
        y = rng.randint(HORIZON + 20, H - 30)
        x = rng.randint(0, W - 120)
        ln = rng.randint(20, 90)
        od.line([(x, y), (x + ln, y)], fill=(140, 170, 220, rng.randint(14, 42)), width=2)

    # --- town silhouette along the shore ---
    shore = (10, 16, 40)
    # back row of roofs
    x = -10
    while x < W + 10:
        bw = rng.randint(46, 110)
        bh = rng.randint(46, 120)
        d.rectangle([x, HORIZON - bh, x + bw, HORIZON + 2], fill=shore)
        # pitched roof
        d.polygon([(x - 4, HORIZON - bh), (x + bw // 2, HORIZON - bh - rng.randint(16, 34)),
                   (x + bw + 4, HORIZON - bh)], fill=shore)
        # chimney
        if rng.random() < 0.5:
            cx0 = x + rng.randint(8, max(9, bw - 18))
            d.rectangle([cx0, HORIZON - bh - 26, cx0 + 10, HORIZON - bh], fill=shore)
        x += bw + rng.randint(2, 14)
    # lit windows in the town
    for _ in range(90):
        wx = rng.randint(10, W - 16)
        wy = rng.randint(HORIZON - 110, HORIZON - 12)
        ww, wh = 5, 7
        warm = rng.random() < 0.75
        col = (255, 196, 110) if warm else (255, 226, 160)
        d.rectangle([wx, wy, wx + ww, wy + wh], fill=col)
        od.rectangle([wx - 3, wy - 3, wx + ww + 3, wy + wh + 3],
                     fill=(255, 190, 100, 40))

    # --- the landmark: the Lantern Tower, centre-right ---
    tx = 660
    base_y = HORIZON + 2
    top_y = 268
    # glow halo behind the lantern room
    for r, a in ((150, 30), (110, 55), (75, 90)):
        od.ellipse([tx - r, top_y - r + 40, tx + r, top_y + r + 40],
                   fill=(255, 200, 110, a))
    # tapered tower body
    d.polygon([(tx - 34, base_y), (tx - 20, top_y + 60), (tx + 20, top_y + 60),
               (tx + 34, base_y)], fill=(12, 14, 36))
    # tower bands
    for by in (top_y + 110, top_y + 170, top_y + 230):
        d.line([(tx - 27, by), (tx + 27, by)], fill=(40, 34, 66), width=4)
    # small tower windows, lit
    for wy in (top_y + 92, top_y + 148, top_y + 204, top_y + 258):
        d.rectangle([tx - 5, wy, tx + 5, wy + 12], fill=(255, 196, 110))
    # lantern room + dome
    d.rectangle([tx - 26, top_y + 18, tx + 26, top_y + 62], fill=(20, 18, 44))
    d.rectangle([tx - 18, top_y + 26, tx + 18, top_y + 54], fill=(255, 214, 130))
    d.line([(tx - 18, top_y + 40), (tx + 18, top_y + 40)], fill=(200, 140, 60), width=2)
    d.polygon([(tx - 30, top_y + 18), (tx, top_y - 8), (tx + 30, top_y + 18)],
              fill=(16, 16, 40))
    d.ellipse([tx - 4, top_y - 16, tx + 4, top_y - 8], fill=(255, 214, 130))
    # light beams fanning out
    od.polygon([(tx - 14, top_y + 40), (tx - 190, top_y - 30), (tx - 190, top_y + 96)],
               fill=(255, 210, 120, 72))
    od.polygon([(tx + 14, top_y + 40), (tx + 200, top_y - 10), (tx + 200, top_y + 116)],
               fill=(255, 210, 120, 72))
    # tower light reflected on the sea
    for i in range(26):
        y = HORIZON + 14 + i * 12
        wdt = 10 + i * 2
        a = max(30, 175 - i * 6)
        od.line([(tx - wdt, y), (tx + wdt, y)], fill=(255, 200, 110, a), width=4)

    # --- boats with lanterns on the glass sea ---
    for bx, by, s in ((220, 700, 1.0), (880, 780, 0.8), (480, 850, 0.65)):
        bw = int(74 * s)
        bh = int(16 * s)
        d.polygon([(bx - bw // 2, by), (bx + bw // 2, by), (bx + bw // 3, by + bh),
                   (bx - bw // 3, by + bh)], fill=(10, 12, 30))
        d.line([(bx, by), (bx, by - int(52 * s))], fill=(10, 12, 30), width=3)
        d.polygon([(bx + 3, by - int(50 * s)), (bx + 3, by - 6),
                   (bx + int(34 * s), by - 6)], fill=(232, 222, 200))
        # boat lantern
        lx, ly = bx + int(8 * s), by - int(58 * s)
        od.ellipse([lx - 14, ly - 14, lx + 14, ly + 14], fill=(255, 200, 110, 90))
        d.ellipse([lx - 4, ly - 5, lx + 4, ly + 5], fill=(255, 220, 140))
        # reflection
        for i in range(8):
            y = by + bh + 6 + i * 7
            od.line([(bx - bw // 3, y), (bx + bw // 3, y)],
                    fill=(255, 200, 110, max(20, 90 - i * 10)), width=2)

    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)

    # --- poster frame ---
    d.rectangle([26, 26, W - 27, H - 27], outline=CREAM, width=4)
    d.rectangle([36, 36, W - 37, H - 37], outline=(255, 243, 214), width=1)

    # --- the place name, large, in the sky ---
    name = "VELMARA"
    font = ImageFont.truetype(SERIF_BOLD, 128)
    # letter-spaced, centred
    widths = [d.textlength(ch, font=font) for ch in name]
    gap = 14
    total = sum(widths) + gap * (len(name) - 1)
    cx, cy = W // 2, 128
    x = cx - total // 2
    # soft shadow for legibility
    for ch, wd in zip(name, widths):
        d.text((x + 3, cy + 4), ch, font=font, fill=(10, 12, 34))
        x += wd + gap
    x = cx - total // 2
    for ch, wd in zip(name, widths):
        d.text((x, cy), ch, font=font, fill=CREAM)
        x += wd + gap
    # thin rules flanking the name
    rule_y = cy + 118
    d.line([(cx - total // 2 - 150, rule_y), (cx - total // 2 - 24, rule_y)],
           fill=CREAM, width=3)
    d.line([(cx + total // 2 + 24, rule_y), (cx + total // 2 + 150, rule_y)],
           fill=CREAM, width=3)
    d.ellipse([cx - 5, rule_y - 5, cx + 5, rule_y + 5], fill=GOLD)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
