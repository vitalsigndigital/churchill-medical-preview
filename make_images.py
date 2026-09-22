#!/usr/bin/env python3
"""
Generates the raster assets that the SVG logo cannot cover:
  assets/img/apple-touch-icon.png   180x180  (iOS home screen)
  assets/img/og-default.png        1200x630  (link previews)

The caduceus is re-drawn here from the same path geometry as
assets/img/caduceus.svg, supersampled 4x, so the raster mark and the vector
mark are the same shape. Run after any change to caduceus.svg.

Run:  python make_images.py
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "assets", "img")
BRAND = (15, 76, 155)
NAVY = (8, 38, 76)
SS = 4  # supersample factor

# --- geometry, mirrored from caduceus.svg (viewBox 0 0 120 205) -------------
WING_PATHS = [
    [(57, 29), (43, 21), (26, 14), (7, 10), (18, 19), (30, 26), (44, 33)],
    [(57, 35), (44, 29), (28, 24), (11, 22), (22, 29), (34, 35), (47, 39)],
    [(57, 41), (45, 37), (32, 34), (18, 33), (28, 40), (39, 43), (49, 46)],
    [(57, 47), (47, 45), (36, 44), (26, 44), (34, 49), (42, 51), (50, 53)],
]
STAFF = [(56.6, 26), (63.4, 26), (63.4, 171), (60, 195), (56.6, 171)]
KNOB = (60, 18, 9)
HEADS = [(30, 60, 8.8, 6.1, 25), (90, 60, 8.8, 6.1, -25)]
SNAKES = [
    [(35, 63), (52, 71), (84, 86), (84, 106), (84, 126), (36, 126), (36, 146), (36, 166), (84, 166), (84, 179)],
    [(85, 63), (68, 71), (36, 86), (36, 106), (36, 126), (84, 126), (84, 146), (84, 166), (36, 166), (36, 179)],
]
SNAKE_W = 7.4


def bez(p0, p1, p2, p3, n=60):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((
            u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0],
            u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1],
        ))
    return out


def wing_outline(pts):
    """Two chained cubics forming a closed feather."""
    a = bez(pts[0], pts[1], pts[2], pts[3])
    b = bez(pts[3], pts[4], pts[5], pts[6])
    return a + b


def spine(pts):
    """Chained cubics: p0 + (c1,c2,p)* """
    out = []
    cur = pts[0]
    for i in range(1, len(pts) - 2, 3):
        out += bez(cur, pts[i], pts[i+1], pts[i+2], 70)
        cur = pts[i+2]
    return out


def rot_ellipse(cx, cy, rx, ry, deg, n=48):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x*ca - y*sa, cy + x*sa + y*ca))
    return pts


def draw_caduceus(size, colour):
    """Return an RGBA image of the mark, `size` px tall, transparent ground."""
    vb_w, vb_h = 120, 205
    scale = (size * SS) / vb_h
    W, H = int(vb_w * scale), int(vb_h * scale)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    sc = lambda p: (p[0] * scale, p[1] * scale)

    for pts in WING_PATHS:
        for mirror in (False, True):
            q = [(120 - x, y) for x, y in pts] if mirror else pts
            d.polygon([sc(p) for p in wing_outline(q)], fill=colour)

    cx, cy, r = KNOB
    d.ellipse([(cx-r)*scale, (cy-r)*scale, (cx+r)*scale, (cy+r)*scale], fill=colour)
    d.polygon([sc(p) for p in STAFF], fill=colour)

    for cx, cy, rx, ry, deg in HEADS:
        d.polygon([sc(p) for p in rot_ellipse(cx, cy, rx, ry, deg)], fill=colour)

    # Stroke the serpents as a dense run of discs — gives true round caps/joins.
    rad = (SNAKE_W / 2) * scale
    for s in SNAKES:
        for x, y in spine(s):
            px, py = x * scale, y * scale
            d.ellipse([px-rad, py-rad, px+rad, py+rad], fill=colour)

    return im.resize((W // SS, H // SS), Image.LANCZOS)


def font(names, size):
    for n in names:
        p = os.path.join(r"C:\Windows\Fonts", n)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def rounded_icon():
    """180x180 iOS touch icon: brand square, white mark."""
    S = 180
    im = Image.new("RGBA", (S*SS, S*SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S*SS-1, S*SS-1], radius=int(S*SS*0.22), fill=BRAND + (255,))
    im = im.resize((S, S), Image.LANCZOS)
    mark = draw_caduceus(122, (255, 255, 255, 255))
    im.alpha_composite(mark, ((S - mark.width)//2, (S - mark.height)//2))
    out = os.path.join(IMG, "apple-touch-icon.png")
    im.convert("RGB").save(out, "PNG", optimize=True)
    return out, im.size


def og_card():
    """1200x630 link-preview card, built on the same hero frame as the site."""
    W, H = 1200, 630
    hero = Image.open(os.path.join(IMG, "hero-consultation-1920.webp")).convert("RGB")
    # cover-fit
    r = max(W / hero.width, H / hero.height)
    hero = hero.resize((int(hero.width*r), int(hero.height*r)), Image.LANCZOS)
    left = (hero.width - W)//2
    top = int((hero.height - H) * 0.32)
    im = hero.crop((left, top, left + W, top + H)).convert("RGBA")

    # Match the site hero scrim: solid navy on the left, smoothstepped to the
    # right so there is no visible knee where the falloff begins.
    scrim = Image.new("RGBA", (W, H))
    sd = ImageDraw.Draw(scrim)
    for x in range(W):
        t = max(0.0, min(1.0, (x / W - 0.30) / 0.70))
        s = t * t * (3 - 2 * t)                    # smoothstep
        sd.line([(x, 0), (x, H)], fill=NAVY + (int(255 - 118 * s),))
    im.alpha_composite(scrim)
    # A second, gentler vertical wash keeps the lower-right corner from
    # competing with the phone number.
    wash = Image.new("RGBA", (W, H))
    wd = ImageDraw.Draw(wash)
    for y in range(H):
        t = max(0.0, min(1.0, (y / H - 0.45) / 0.55))
        wd.line([(0, y), (W, y)], fill=NAVY + (int(70 * t * t),))
    im.alpha_composite(wash)

    d = ImageDraw.Draw(im)
    f_name = font(["georgiab.ttf", "georgia.ttf", "segoeuib.ttf", "arialbd.ttf"], 62)
    f_sub = font(["segoeui.ttf", "arial.ttf"], 30)
    f_meta = font(["segoeuib.ttf", "arialbd.ttf"], 27)

    x0, y0 = 72, 150
    mark = draw_caduceus(96, (255, 255, 255, 255))
    im.alpha_composite(mark, (x0, y0 - 18))

    d.text((x0 + 86, y0 + 6), "Churchill", font=f_name, fill=(255, 255, 255))
    d.text((x0 + 88, y0 + 78), "MEDICAL CLINIC", font=f_meta, fill=(187, 214, 247))

    d.text((x0, 322), "Walk-in clinic in Churchill Meadows,", font=f_sub, fill=(226, 236, 249))
    d.text((x0, 362), "Mississauga — no appointment needed", font=f_sub, fill=(226, 236, 249))

    d.line([(x0, 428), (x0 + 96, 428)], fill=(90, 145, 215), width=3)

    d.text((x0, 458), "(905) 607-6495", font=f_meta, fill=(255, 255, 255))
    d.text((x0, 498), "3050 Artesian Drive, Unit 6  ·  Covered by OHIP",
           font=font(["segoeui.ttf", "arial.ttf"], 25), fill=(170, 199, 233))

    # JPEG, not PNG: this is a photograph, and a 375 KB link preview is a
    # needless download on every share.
    out = os.path.join(IMG, "og-default.jpg")
    im.convert("RGB").save(out, "JPEG", quality=86, optimize=True, progressive=True)
    return out, (W, H)


if __name__ == "__main__":
    for path, size in (rounded_icon(), og_card()):
        print("%-46s %s  %.0f KB" % (os.path.basename(path), size, os.path.getsize(path)/1024))
