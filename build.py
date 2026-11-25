# news-image-20261125 — acct1 (Masrukhan25 / @arminalyunan)
# Program draws "The World in One Day" for Wednesday 25 November 2026.
# Flat-vector PIL newspaper, 9-hero formula (24 Nov): 3 large heroes + 6 enlarged
# small heroes, world map with numbered dots + REGION INDEX, ALSO list #10-30,
# THE DAY IN NUMBERS strip, DATE CHECK bar. Deterministic, no network.
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 239, 220)
PANEL = (253, 250, 240)
NAVY = (30, 47, 77)
NAVY2 = (52, 74, 112)
BRICK = (176, 58, 46)
GOLD = (201, 149, 53)
INK = (35, 35, 32)
GREY = (112, 106, 94)
LIGHT = (233, 223, 199)
OCEAN = (206, 224, 228)
LAND = (229, 206, 161)
LANDB = (214, 186, 138)
TEAL = (46, 120, 110)
GREEN = (74, 132, 84)
SKY = (214, 231, 235)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


def serif(size, bold=True):
    return F("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf", size)


def sans(size, bold=False):
    return F("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, name, size, max_w):
    while size > 8:
        f = F(name, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return F(name, 8)


def layer(w, h):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def badge(d, cx, cy, r, num, font_size=13):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BRICK, outline=(255, 255, 255), width=2)
    f = sans(font_size, True)
    tw = d.textlength(str(num), font=f)
    d.text((cx - tw / 2, cy - font_size / 2 - 1), str(num), font=f, fill=(255, 255, 255))


def sky_ground(d, w, h, sky=SKY, ground=None, gy=None):
    d.rectangle([0, 0, w, h], fill=sky)
    if ground is not None and gy is not None:
        d.rectangle([0, gy, w, h], fill=ground)


# ---------------------------------------------------------------- illustrations
def illu_1(w, h):
    """Cartagena supermarket siege: storefront, awning, police tape."""
    img, d = layer(w, h)
    sky_ground(d, w, h, sky=(222, 232, 236), ground=(196, 190, 176), gy=int(h * 0.78))
    # building
    d.rectangle([int(w * 0.08), int(h * 0.16), int(w * 0.92), int(h * 0.78)], fill=NAVY)
    d.rectangle([int(w * 0.08), int(h * 0.16), int(w * 0.92), int(h * 0.26)], fill=(250, 246, 236))
    f = sans(15, True)
    d.text((int(w * 0.5) - d.textlength("MARKET", font=f) / 2, int(h * 0.17)), "MARKET", font=f, fill=NAVY)
    # awning stripes
    ax0, ax1, ay0, ay1 = int(w * 0.08), int(w * 0.92), int(h * 0.28), int(h * 0.40)
    n = 9
    for i in range(n):
        x0 = ax0 + (ax1 - ax0) * i // n
        x1 = ax0 + (ax1 - ax0) * (i + 1) // n
        d.rectangle([x0, ay0, x1, ay1], fill=BRICK if i % 2 == 0 else (250, 246, 236))
    # door + windows
    d.rectangle([int(w * 0.44), int(h * 0.52), int(w * 0.56), int(h * 0.78)], fill=(250, 246, 236))
    for wx in (0.16, 0.30, 0.64, 0.78):
        d.rectangle([int(w * wx), int(h * 0.48), int(w * (wx + 0.09)), int(h * 0.66)],
                    fill=(140, 190, 205))
    # police tape across the front
    ty = int(h * 0.70)
    d.rectangle([0, ty, w, ty + 12], fill=GOLD)
    for i in range(0, w, 22):
        d.polygon([(i, ty + 12), (i + 11, ty), (i + 22, ty), (i + 11, ty + 12)], fill=NAVY)
    # police car silhouette
    cx, cy = int(w * 0.70), int(h * 0.84)
    d.rounded_rectangle([cx - 52, cy - 12, cx + 52, cy + 8], radius=6, fill=NAVY)
    d.rounded_rectangle([cx - 34, cy - 24, cx + 30, cy - 10], radius=6, fill=NAVY2)
    d.rectangle([cx - 8, cy - 30, cx + 8, cy - 24], fill=BRICK)
    d.ellipse([cx - 40, cy + 2, cx - 22, cy + 14], fill=(20, 20, 20))
    d.ellipse([cx + 22, cy + 2, cx + 40, cy + 14], fill=(20, 20, 20))
    return img


def illu_2(w, h):
    """CIA + ODNI cyberattack: dark screen, code lines, warning, lock."""
    img, d = layer(w, h)
    d.rectangle([0, 0, w, h], fill=(18, 28, 48))
    # code lines (fixed pattern)
    rows = [(0.10, 0.55), (0.20, 0.75), (0.30, 0.45), (0.40, 0.65), (0.52, 0.50),
            (0.62, 0.70), (0.72, 0.42), (0.82, 0.60)]
    for i, (ry, frac) in enumerate(rows):
        y = int(h * ry)
        x1 = int(w * frac)
        col = (90, 200, 170) if i % 3 else (120, 160, 210)
        d.rectangle([int(w * 0.06), y, x1, y + 5], fill=col)
    # warning triangle
    cx, cy, s = int(w * 0.72), int(h * 0.42), 34
    d.polygon([(cx, cy - s), (cx + s, cy + s * 0.8), (cx - s, cy + s * 0.8)], fill=GOLD)
    f = sans(30, True)
    d.text((cx - d.textlength("!", font=f) / 2, cy - 16), "!", font=f, fill=NAVY)
    # lock
    lx, ly = int(w * 0.14), int(h * 0.62)
    d.rounded_rectangle([lx, ly, lx + 44, ly + 38], radius=5, fill=BRICK)
    d.arc([lx + 9, ly - 14, lx + 35, ly + 12], 180, 360, fill=(250, 246, 236), width=5)
    f2 = sans(11, True)
    d.text((int(w * 0.06), int(h * 0.88)), "CIA  ·  ODNI", font=f2, fill=(200, 210, 225))
    return img


def illu_3(w, h):
    """Iowa lead-azide detonation: blast cloud, barrels, plume arrow."""
    img, d = layer(w, h)
    sky_ground(d, w, h, sky=(238, 226, 196), ground=(120, 110, 88), gy=int(h * 0.76))
    # sun
    d.ellipse([int(w * 0.80), int(h * 0.06), int(w * 0.92), int(h * 0.18)], fill=GOLD)
    # explosion cloud: layered circles
    cx, cy = int(w * 0.42), int(h * 0.44)
    for (dx, dy, r, col) in [(-38, 6, 30, (176, 58, 46)), (30, 10, 28, (200, 90, 40)),
                             (0, -22, 34, (226, 120, 50)), (-8, 4, 26, (240, 170, 60)),
                             (18, -6, 20, (250, 210, 90))]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=col)
    # plume arrow curving up-right
    d.line([(cx + 40, cy - 30), (int(w * 0.78), int(h * 0.10))], fill=(90, 90, 80), width=3)
    d.polygon([(int(w * 0.78), int(h * 0.10)), (int(w * 0.74), int(h * 0.14)),
               (int(w * 0.80), int(h * 0.16))], fill=(90, 90, 80))
    # barrels
    for i, bx in enumerate((0.10, 0.20, 0.30)):
        x = int(w * bx)
        d.rounded_rectangle([x, int(h * 0.62), x + 26, int(h * 0.76)], radius=4, fill=NAVY2)
        d.rectangle([x, int(h * 0.66), x + 26, int(h * 0.68)], fill=GOLD)
    # warning sign
    sx, sy = int(w * 0.66), int(h * 0.60)
    d.polygon([(sx, sy), (sx + 26, sy + 24), (sx - 26, sy + 24)], fill=GOLD,
              outline=NAVY)
    f = sans(13, True)
    d.text((sx - d.textlength("!", font=f) / 2, sy + 6), "!", font=f, fill=NAVY)
    return img


def illu_4(w, h):
    """NATO space defence: satellite, stars, Earth arc."""
    img, d = layer(w, h)
    d.rectangle([0, 0, w, h], fill=(16, 26, 50))
    stars = [(0.08, 0.12), (0.22, 0.06), (0.38, 0.18), (0.55, 0.08), (0.70, 0.16),
             (0.86, 0.07), (0.93, 0.30), (0.12, 0.38), (0.30, 0.34), (0.62, 0.30)]
    for (fx, fy) in stars:
        x, y = int(w * fx), int(h * fy)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255))
    # Earth arc at bottom
    d.ellipse([int(-w * 0.25), int(h * 0.72), int(w * 1.25), int(h * 1.55)], fill=(52, 110, 170))
    d.ellipse([int(w * 0.18), int(h * 0.86), int(w * 0.42), int(h * 1.05)], fill=(74, 132, 84))
    d.ellipse([int(w * 0.62), int(h * 0.92), int(w * 0.80), int(h * 1.08)], fill=(74, 132, 84))
    # satellite
    sx, sy = int(w * 0.50), int(h * 0.38)
    d.rectangle([sx - 78, sy - 12, sx - 26, sy + 12], fill=(52, 110, 170))
    d.rectangle([sx + 26, sy - 12, sx + 78, sy + 12], fill=(52, 110, 170))
    for gx in (-78, -52, 26, 52):
        d.line([(sx + gx, sy - 12), (sx + gx, sy + 12)], fill=(200, 220, 235), width=2)
    d.rectangle([sx - 26, sy - 16, sx + 26, sy + 16], fill=GOLD)
    d.ellipse([sx - 8, sy - 6, sx + 8, sy + 6], fill=BRICK)
    d.line([(sx, sy + 16), (sx, sy + 34)], fill=(200, 220, 235), width=3)
    d.ellipse([sx - 5, sy + 32, sx + 5, sy + 42], fill=(200, 220, 235))
    return img


def illu_5(w, h):
    """Russia accuses Ukraine: cargo ship, drone, sea."""
    img, d = layer(w, h)
    sky_ground(d, w, h, sky=(222, 232, 236), ground=None, gy=None)
    # sea bands
    for i, yy in enumerate((0.55, 0.65, 0.75, 0.85)):
        d.rectangle([0, int(h * yy), w, int(h * (yy + 0.10))],
                    fill=(52, 110, 170) if i % 2 == 0 else (70, 130, 185))
    for i in range(6):
        x = int(w * (0.06 + i * 0.16))
        d.arc([x, int(h * 0.60), x + 26, int(h * 0.68)], 180, 360, fill=(255, 255, 255), width=3)
    # cargo ship
    sx, sy = int(w * 0.16), int(h * 0.52)
    d.polygon([(sx, sy), (sx + int(w * 0.52), sy), (sx + int(w * 0.46), sy + 26),
               (sx + 8, sy + 26)], fill=NAVY)
    cols = [BRICK, GOLD, (52, 110, 170), (74, 132, 84)]
    for i, c in enumerate(cols):
        x = sx + 14 + i * 34
        d.rectangle([x, sy - 34, x + 30, sy - 2], fill=c)
    d.rectangle([sx + int(w * 0.52) - 22, sy - 52, sx + int(w * 0.52) - 6, sy - 2], fill=NAVY2)
    # drone top-right
    dx, dy = int(w * 0.80), int(h * 0.22)
    d.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=(30, 30, 30))
    for (ox, oy) in ((-14, -10), (14, -10), (-14, 10), (14, 10)):
        d.line([(dx, dy), (dx + ox, dy + oy)], fill=(30, 30, 30), width=2)
        d.ellipse([dx + ox - 5, dy + oy - 3, dx + ox + 5, dy + oy + 3], fill=(120, 120, 120))
    # explosion starburst near ship bow
    ex, ey = int(w * 0.78), int(h * 0.46)
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 8, 22
        a = math.radians(ang)
        d.line([(ex, ey), (ex + int(r2 * math.cos(a)), ey + int(r2 * math.sin(a)))],
               fill=GOLD, width=4)
    d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=BRICK)
    return img


def illu_6(w, h):
    """South Korea minister resigns: ministry building, walking figure, paper."""
    img, d = layer(w, h)
    sky_ground(d, w, h, sky=(222, 232, 236), ground=(196, 190, 176), gy=int(h * 0.74))
    # ministry building with columns
    bx0, bx1 = int(w * 0.10), int(w * 0.62)
    d.rectangle([bx0, int(h * 0.30), bx1, int(h * 0.74)], fill=NAVY)
    d.polygon([(bx0 - 8, int(h * 0.30)), ((bx0 + bx1) // 2, int(h * 0.14)),
               (bx1 + 8, int(h * 0.30))], fill=BRICK)
    for i in range(4):
        x = bx0 + 14 + i * ((bx1 - bx0 - 28) // 3)
        d.rectangle([x, int(h * 0.36), x + 10, int(h * 0.74)], fill=(250, 246, 236))
    # walking figure with briefcase
    fx, fy = int(w * 0.76), int(h * 0.66)
    d.ellipse([fx - 9, fy - 26, fx + 9, fy - 8], fill=NAVY)  # head
    d.rounded_rectangle([fx - 8, fy - 8, fx + 8, fy + 18], radius=4, fill=NAVY)  # body
    d.line([(fx - 6, fy + 18), (fx - 14, fy + 34)], fill=NAVY, width=5)
    d.line([(fx + 6, fy + 18), (fx + 14, fy + 30)], fill=NAVY, width=5)
    d.rectangle([fx + 14, fy + 8, fx + 34, fy + 24], fill=BRICK)  # briefcase
    # paper sheet flying
    d.polygon([(int(w * 0.86), int(h * 0.30)), (int(w * 0.94), int(h * 0.26)),
               (int(w * 0.96), int(h * 0.42)), (int(w * 0.88), int(h * 0.46))],
              fill=(255, 255, 255), outline=GREY)
    return img


def illu_7(w, h):
    """Australia-Solomon pact: two islands, shield, flags."""
    img, d = layer(w, h)
    d.rectangle([0, 0, w, h], fill=(206, 224, 228))
    # waves
    for yy in (0.72, 0.84):
        for i in range(5):
            x = int(w * (0.02 + i * 0.20))
            d.arc([x, int(h * yy), x + 30, int(h * (yy + 0.10))], 180, 360,
                  fill=(255, 255, 255), width=3)
    # Australia-ish island (left)
    d.polygon([(int(w * 0.06), int(h * 0.55)), (int(w * 0.10), int(h * 0.42)),
               (int(w * 0.24), int(h * 0.38)), (int(w * 0.36), int(h * 0.46)),
               (int(w * 0.38), int(h * 0.60)), (int(w * 0.28), int(h * 0.68)),
               (int(w * 0.12), int(h * 0.66))], fill=LAND)
    # Solomon island (right)
    d.polygon([(int(w * 0.68), int(h * 0.50)), (int(w * 0.74), int(h * 0.40)),
               (int(w * 0.84), int(h * 0.42)), (int(w * 0.90), int(h * 0.52)),
               (int(w * 0.84), int(h * 0.60)), (int(w * 0.72), int(h * 0.60))],
              fill=GREEN)
    # shield centre
    sx, sy = int(w * 0.52), int(h * 0.42)
    d.polygon([(sx - 26, sy - 26), (sx + 26, sy - 26), (sx + 26, sy + 4),
               (sx, sy + 30), (sx - 26, sy + 4)], fill=NAVY, outline=GOLD, width=3)
    f = sans(22, True)
    d.text((sx - d.textlength("✓", font=f) / 2, sy - 20), "✓", font=f, fill=(255, 255, 255))
    # two small flags
    for fx, col in ((0.16, (30, 47, 77)), (0.74, (0, 90, 140))):
        x = int(w * fx)
        d.line([(x, int(h * 0.30)), (x, int(h * 0.52))], fill=NAVY, width=3)
        d.polygon([(x, int(h * 0.30)), (x + 30, int(h * 0.34)), (x, int(h * 0.40))],
                  fill=col)
    return img


def illu_8(w, h):
    """Vaibhav 204 off 53 balls: batsman, pitch, big 204."""
    img, d = layer(w, h)
    sky_ground(d, w, h, sky=(222, 232, 236), ground=GREEN, gy=int(h * 0.62))
    # pitch strip
    d.rectangle([int(w * 0.30), int(h * 0.62), int(w * 0.72), h], fill=(229, 206, 161))
    # stumps
    for sx in (0.34, 0.37, 0.40):
        x = int(w * sx)
        d.rectangle([x, int(h * 0.52), x + 4, int(h * 0.62)], fill=GOLD)
    # batsman silhouette mid-swing
    bx, by = int(w * 0.52), int(h * 0.50)
    d.ellipse([bx - 10, by - 30, bx + 10, by - 10], fill=NAVY)
    d.rounded_rectangle([bx - 10, by - 10, bx + 10, by + 22], radius=5, fill=NAVY)
    d.line([(bx - 8, by + 22), (bx - 18, by + 42)], fill=NAVY, width=6)
    d.line([(bx + 8, by + 22), (bx + 16, by + 40)], fill=NAVY, width=6)
    d.line([(bx + 8, by - 4), (bx + 34, by - 26)], fill=(120, 80, 40), width=7)  # bat
    # ball with motion lines
    d.ellipse([int(w * 0.80) - 8, int(h * 0.22) - 8, int(w * 0.80) + 8, int(h * 0.22) + 8],
              fill=BRICK)
    for i in range(3):
        y = int(h * (0.26 + i * 0.05))
        d.line([(int(w * 0.70), y), (int(w * 0.76), y)], fill=BRICK, width=2)
    # big 204
    f = sans(34, True)
    d.text((int(w * 0.06), int(h * 0.06)), "204", font=f, fill=BRICK)
    f2 = sans(10, True)
    d.text((int(w * 0.06), int(h * 0.06) + 38), "OFF 53 BALLS · 28 SIXES", font=f2, fill=NAVY)
    return img


def illu_9(w, h):
    """Dutch court climate targets: courthouse, gavel, scales."""
    img, d = layer(w, h)
    sky_ground(d, w, h, sky=(222, 232, 236), ground=(196, 190, 176), gy=int(h * 0.76))
    # courthouse
    bx0, bx1 = int(w * 0.12), int(w * 0.60)
    d.rectangle([bx0, int(h * 0.34), bx1, int(h * 0.76)], fill=(250, 246, 236),
                outline=NAVY, width=2)
    d.polygon([(bx0 - 8, int(h * 0.34)), ((bx0 + bx1) // 2, int(h * 0.18)),
               (bx1 + 8, int(h * 0.34))], fill=NAVY)
    for i in range(3):
        x = bx0 + 16 + i * ((bx1 - bx0 - 32) // 2)
        d.rectangle([x, int(h * 0.42), x + 12, int(h * 0.76)], fill=NAVY)
    # scales of justice (right)
    sx, sy = int(w * 0.78), int(h * 0.42)
    d.line([(sx, sy - 22), (sx, sy + 26)], fill=NAVY, width=4)
    d.line([(sx - 24, sy - 18), (sx + 24, sy - 18)], fill=NAVY, width=3)
    for sgn in (-1, 1):
        x = sx + sgn * 24
        d.line([(x, sy - 18), (x, sy + 2)], fill=NAVY, width=2)
        d.polygon([(x - 10, sy + 2), (x + 10, sy + 2), (x, sy + 14)], fill=GOLD)
    d.ellipse([sx - 5, sy - 28, sx + 5, sy - 18], fill=BRICK)
    # green check seal
    d.ellipse([int(w * 0.68), int(h * 0.70), int(w * 0.80), int(h * 0.82)], fill=GREEN)
    f = sans(14, True)
    d.text((int(w * 0.715), int(h * 0.715)), "✓", font=f, fill=(255, 255, 255))
    return img


ILLUS = [illu_1, illu_2, illu_3, illu_4, illu_5, illu_6, illu_7, illu_8, illu_9]

# ---------------------------------------------------------------- world map
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 73),
     (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35), (-80, 32), (-81, 26),
     (-84, 30), (-90, 21), (-97, 16), (-94, 17), (-90, 14), (-83, 9), (-79, 9),
     (-83, 15), (-87, 13), (-92, 15), (-97, 16), (-105, 20), (-110, 23), (-114, 28),
     (-117, 33), (-122, 37), (-124, 42), (-124, 48), (-130, 55), (-140, 60),
     (-155, 58), (-162, 55), (-168, 66)],
    # Greenland
    [(-58, 64), (-45, 60), (-40, 64), (-30, 68), (-22, 70), (-30, 74), (-45, 76),
     (-58, 74), (-60, 70), (-58, 64)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23),
     (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54), (-66, -55),
     (-65, -45), (-62, -40), (-58, -35), (-52, -32), (-48, -28), (-41, -23),
     (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-52, 4),
     (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-77, 8), (-79, 9)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50), (0, 51), (2, 51),
     (5, 53), (8, 55), (8, 57), (10, 58), (12, 56), (18, 56), (21, 55), (24, 58),
     (23, 60), (21, 65), (18, 69), (25, 71), (30, 70), (35, 68), (40, 67),
     (45, 68), (50, 69), (55, 68), (60, 69), (68, 73), (75, 73), (70, 72),
     (60, 70), (55, 68), (48, 66), (44, 65), (40, 64), (36, 64), (32, 65),
     (30, 62), (28, 60), (25, 60), (23, 58), (21, 56), (18, 55), (15, 54),
     (12, 54), (8, 54), (5, 53), (2, 51), (0, 50), (-2, 49), (-5, 48), (-2, 47),
     (-1, 44), (-2, 43), (-6, 38), (-9, 37), (-10, 36)],
    # Africa
    [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11), (-12, 8),
     (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (9, 0), (12, -5), (13, -10),
     (12, -17), (14, -22), (16, -28), (19, -34), (26, -34), (32, -29), (35, -24),
     (36, -18), (40, -15), (40, -10), (42, -4), (46, -1), (51, 2), (51, 10),
     (48, 11), (44, 11), (40, 15), (38, 18), (37, 22), (34, 27), (32, 31),
     (30, 32), (25, 32), (20, 32), (15, 32), (11, 34), (10, 37), (6, 37), (-6, 35)],
    # Asia
    [(30, 36), (36, 36), (43, 38), (48, 38), (52, 36), (56, 30), (58, 25), (61, 25),
     (66, 25), (70, 20), (72, 20), (76, 15), (77, 8), (80, 7), (80, 13), (85, 19),
     (89, 22), (91, 22), (93, 16), (97, 16), (98, 10), (100, 6), (103, 1),
     (104, 2), (106, 10), (109, 15), (110, 20), (114, 22), (118, 25), (120, 28),
     (122, 35), (126, 40), (129, 42), (132, 43), (135, 44), (138, 46), (141, 50),
     (142, 54), (140, 59), (136, 60), (132, 57), (128, 52), (124, 47), (122, 42),
     (118, 39), (114, 36), (110, 32), (106, 28), (102, 22), (98, 18), (94, 16),
     (90, 15), (86, 12), (82, 8), (80, 6), (76, 7), (72, 11), (68, 15), (64, 19),
     (60, 23), (56, 26), (52, 27), (48, 29), (44, 29), (40, 31), (36, 33),
     (32, 36), (30, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (151, -24), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
     (118, -20), (114, -21), (113, -22)],
    # UK
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-3, 50),
     (-5, 50)],
    # Madagascar
    [(43, -12), (47, -15), (50, -16), (49, -20), (47, -25), (44, -25), (43, -20),
     (43, -15)],
    # Japan — Honshu
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 35), (140, 38), (141, 41),
     (142, 43), (144, 44)],
    # Japan — Hokkaido
    [(140, 42), (142, 42), (144, 44), (141, 45), (140, 44)],
    # Sumatra
    [(95, 5), (100, 0), (104, -3), (106, -6), (101, -2), (96, 4)],
    # Java
    [(105, -6), (110, -7), (114, -8), (114, -9), (108, -8), (105, -7)],
    # Kalimantan (Borneo)
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4), (109, -2)],
    # New Guinea
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -9), (142, -8),
     (137, -5), (132, -3)],
    # New Zealand — North Island
    [(173, -35), (176, -38), (178, -38), (175, -41), (173, -40)],
    # New Zealand — South Island
    [(167, -45), (170, -43), (173, -42), (174, -41), (171, -44), (168, -46)],
    # Sri Lanka
    [(80, 6), (81, 7), (81, 9), (80, 9), (79, 7)],
    # Philippines
    [(120, 18), (122, 17), (124, 14), (123, 11), (121, 13), (120, 16)],
]

# (number, lon, lat)
DOTS = [
    (1, -75.5, 10.4), (2, -76.4, 37.0), (3, -91.3, 40.8), (4, 4.4, 50.9),
    (5, 24.0, 60.0), (5, 20.1, 32.1), (6, 127.0, 37.5), (7, 160.0, -9.4),
    (8, 54.4, 24.4), (9, 4.3, 52.1),
]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=OCEAN, outline=NAVY, width=1)

    def px(lon, lat):
        x = x0 + (lon + 180.0) / 360.0 * w
        y = y0 + (85.0 - lat) / 145.0 * h
        return x, y

    # graticule every 30 degrees
    for lon in range(-150, 181, 30):
        x = x0 + (lon + 180.0) / 360.0 * w
        d.line([(x, y0), (x, y0 + h)], fill=(255, 255, 255), width=1)
    for lat in range(-60, 86, 30):
        y = y0 + (85.0 - lat) / 145.0 * h
        d.line([(x0, y), (x0 + w, y)], fill=(255, 255, 255), width=1)
    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LANDB)
        d.line(pts + [pts[0]], fill=NAVY, width=2)
    for num, lon, lat in DOTS:
        x, y = px(lon, lat)
        bx, by = x, y
        if num == 2:
            bx, by = x + 14, y - 10
        elif num == 4:
            bx, by = x - 14, y + 10
        elif num == 9:
            bx, by = x - 14, y - 10
        if (bx, by) != (x, y):
            d.line([(x, y), (bx, by)], fill=NAVY, width=1)
        d.ellipse([x - 3.5, y - 3.5, x + 3.5, y + 3.5], fill=BRICK,
                  outline=(255, 255, 255), width=1)
        badge(d, bx, by, 9, num, font_size=10)


# ---------------------------------------------------------------- content
HEROES = [
    ("CARTAGENA SUPERMARKET SIEGE", "AMERICAS", "REPORTED",
     "30 hostages taken in an Éxito store; 10 freed, ~20 still held as captors demand $2M + safe passage.",
     "Sky News / IANS / Reuters"),
    ("CIA + ODNI CYBERATTACK", "NORTH AMERICA", "REPORTED",
     "US spy agencies hit by a cyberattack on classified systems, CNN reports — 2 agencies hit.",
     "CNN, 25 Nov"),
    ("IOWA LEAD-AZIDE DETONATION", "NORTH AMERICA", "CONFIRMED",
     "Army to blow up 9,500 lbs of ageing lead azide — the biggest such blast in nearly 50 years; plume 100+ miles.",
     "Des Moines Register / US Army"),
    ("NATO VOWS SPACE DEFENSE", "EUROPE", "REPORTED",
     "NATO vows to defend space after reports Russia may launch a nuclear-armed satellite, possibly Dec 2026.",
     "25 Nov"),
    ("RUSSIA ACCUSES UKRAINE OF “TERRORISM”", "EUROPE", "REPORTED",
     "Moscow warns of severe consequences after drone strikes on 2 Russian ships — in the Gulf of Finland and off Libya.",
     "25 Nov"),
    ("SOUTH KOREA EDUCATION MINISTER RESIGNS", "ASIA", "CONFIRMED",
     "Minister Choi Kyo-jin quits over a national exam-cheating scandal.",
     "25 Nov"),
    ("AUSTRALIA–SOLOMON ISLANDS SECURITY PACT", "PACIFIC", "CONFIRMED",
     "Canberra named Honiara’s primary security partner; no foreign military or security bases.",
     "AP, 25 Nov"),
    ("VAIBHAV 204 OFF 53 BALLS", "ASIA / SPORT", "CONFIRMED",
     "India A star smashes the fastest List A double century — 204 off 53 balls, a world-record 28 sixes.",
     "Rising Stars Asia Cup"),
    ("DUTCH COURT: CLIMATE TARGETS BINDING", "EUROPE", "CONFIRMED",
     "The Hague court keeps binding Dutch climate targets in force while the state’s appeal proceeds.",
     "NOS, 25 Nov"),
]

NUMBERS = [
    ("30", "HOSTAGES TAKEN IN CARTAGENA"),
    ("9,500", "LBS OF LEAD AZIDE, IOWA BLAST"),
    ("74,746", "GAZA DEATH TOLL"),
    ("266M", "FACE ACUTE FOOD INSECURITY"),
    ("204", "RUNS OFF 53 BALLS — 28 SIXES"),
    ("10 of 12", "COUNTS: HUAWEI GUILTY"),
]

ALSO = [
    (10, "HUAWEI GUILTY ON 10 OF 12 COUNTS"),
    (11, "COP31 ENDS WITHOUT A DEAL"),
    (12, "GAZA DEATH TOLL 74,746"),
    (13, "266 MILLION FACE ACUTE FOOD INSECURITY"),
    (14, "WHO EVACUATES DRC EBOLA STAFF"),
    (15, "NORTH KOREA THREATENS SWISS OFFICE"),
    (16, "SETTLER ARSON CONDEMNED AS “JEWISH TERRORISM”"),
    (17, "12,000 EVACUATED FROM MANCHESTER CONCERT"),
    (18, "ANMER HALL BREAK-IN ARRESTS"),
    (19, "GIULIANI AWARDED MEDAL OF FREEDOM"),
    (20, "TRUMP SET TO UNVEIL NEW TARIFFS"),
    (21, "ÁBREGO GARCÍA LEAVES FOR SPAIN"),
    (22, "SENEGAL AFCON CHAMPIONS REINSTATED"),
    (23, "GUKESH HOLDS SINDAROV IN OPENER"),
    (24, "IRANIAN SINGER GETS 74 LASHES"),
    (25, "SHEIKH HASINA ANNOUNCES RETURN"),
    (26, "MACRON WEIGHS SPENDING CAPS"),
    (27, "NSW $35M DRUG SYNDICATE CHARGED"),
    (28, "ASIAN TECH SHARES SLIDE"),
    (29, "LEWIS PUGH SWIMS HORMUZ"),
    (30, "ISRAEL: IRAN DEVELOPING CHEMICAL WEAPONS"),
]

DATE_CHECK = ("DATE CHECK — LEFT OUT: Anthropic $2T IPO (19 Nov) · Russian extradition "
              "(5 Nov) · Missiles over Poland (20 Nov) · Tarwekamp blast (Dec 2024). "
              "Huawei verdict was 24 Nov, reported 25 Nov in Asia.")


# ---------------------------------------------------------------- layout
def hero_panel(img, d, x, y, w, h, idx, illu_h, top_story=False):
    head, region, status, deck, src = HEROES[idx]
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=NAVY, width=1)
    ill = ILLUS[idx](w, illu_h)
    img.paste(ill, (x, y), ill)
    badge(d, x + 18, y + (38 if top_story else 18),
          13 if illu_h > 100 else 11, idx + 1,
          font_size=13 if illu_h > 100 else 11)
    if top_story:
        d.rectangle([x, y, x + w, y + 20], fill=BRICK)
        f = sans(11, True)
        t = "★ TOP STORY ★"
        d.text((x + w / 2 - d.textlength(t, font=f) / 2, y + 3), t, font=f,
               fill=(255, 255, 255))
    ty = y + illu_h + 6
    hf = fit(d, head, "DejaVuSans-Bold.ttf", 16 if illu_h > 100 else 12,
             w - 16)
    for ln in wrap(d, head, hf, w - 16)[:2]:
        d.text((x + 8, ty), ln, font=hf, fill=NAVY)
        ty += hf.size + 2
    df = sans(11 if illu_h > 100 else 10)
    for ln in wrap(d, deck, df, w - 16)[:3 if illu_h > 100 else 2]:
        d.text((x + 8, ty), ln, font=df, fill=INK)
        ty += 14 if illu_h > 100 else 13
    tf = sans(9, True)
    tag = region + "  ·  " + status
    d.text((x + 8, y + h - 15), tag, font=tf, fill=BRICK)
    sf = sans(9)
    sw = d.textlength(src, font=sf)
    d.text((x + w - 8 - sw, y + h - 15), src, font=sf, fill=GREY)


def build(path):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=2)
    M = 22
    y = 20
    # masthead
    tf = serif(40)
    t = "THE WORLD IN ONE DAY"
    d.text((W / 2 - d.textlength(t, font=tf) / 2, y), t, font=tf, fill=NAVY)
    y += 50
    df = sans(14, True)
    t = "WEDNESDAY 25 NOVEMBER 2026  —  30 STORIES FROM 4 REGIONS"
    d.text((W / 2 - d.textlength(t, font=df) / 2, y), t, font=df, fill=BRICK)
    y += 24
    d.line([(M, y), (W - M, y)], fill=NAVY, width=3)
    y += 4
    d.line([(M, y), (W - M, y)], fill=NAVY, width=1)
    y += 8
    # numbers strip
    lf = sans(10, True)
    d.text((M, y), "THE DAY IN NUMBERS", font=lf, fill=NAVY)
    y += 15
    strip_y = y
    cell_w = (W - 2 * M) // 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + i * cell_w
        if i:
            d.line([(cx - 4, strip_y), (cx - 4, strip_y + 46)], fill=LIGHT, width=2)
        nf = fit(d, num, "DejaVuSans-Bold.ttf", 24, cell_w - 12)
        d.text((cx + (cell_w - d.textlength(num, font=nf)) / 2, strip_y), num,
               font=nf, fill=BRICK)
        for j, ln in enumerate(wrap(d, lab, sans(9, True), cell_w - 12)):
            d.text((cx + (cell_w - d.textlength(ln, font=sans(9, True))) / 2,
                    strip_y + 27 + j * 11), ln, font=sans(9, True), fill=NAVY)
    y = strip_y + 50
    # 3 large heroes
    hw = (W - 2 * M - 20) // 3
    hh = 252
    for i in range(3):
        hero_panel(img, d, M + i * (hw + 10), y, hw, hh, i, 146, top_story=(i == 0))
    y += hh + 8
    # 6 enlarged small heroes, 2 rows x 3
    sh = 138
    for r in range(2):
        for c in range(3):
            hero_panel(img, d, M + c * (hw + 10), y, hw, sh, 3 + r * 3 + c, 70)
        y += sh + 8
    # map + ALSO row
    row_y = y
    row_h = 204
    map_w = 398
    d.rectangle([M, row_y, M + map_w, row_y + row_h], fill=PANEL, outline=NAVY, width=1)
    d.text((M + 8, row_y + 6), "WHERE IT HAPPENED", font=sans(12, True), fill=NAVY)
    draw_map(d, M + 8, row_y + 24, map_w - 16, 126)
    lf2 = sans(9, True)
    d.text((M + 8, row_y + 154), "REGION INDEX", font=lf2, fill=BRICK)
    d.text((M + 8, row_y + 166),
           "AMERICAS 1–3  ·  EUROPE 4, 5, 9  ·  ASIA 6, 8  ·  PACIFIC 7",
           font=sans(9), fill=INK)
    d.text((M + 8, row_y + 178),
           "1 Cartagena · 2 Langley · 3 Iowa · 4 Brussels · 5 Finland / Benghazi",
           font=sans(8), fill=GREY)
    d.text((M + 8, row_y + 189),
           "6 Seoul · 7 Honiara · 8 UAE · 9 The Hague",
           font=sans(8), fill=GREY)
    ax = M + map_w + 10
    aw = W - M - ax
    d.rectangle([ax, row_y, ax + aw, row_y + row_h], fill=PANEL, outline=NAVY, width=1)
    d.text((ax + 8, row_y + 6), "ALSO ON 25 NOVEMBER", font=sans(12, True), fill=NAVY)
    col_w = (aw - 16) // 2
    for i, (num, title) in enumerate(ALSO):
        col = 0 if i < 11 else 1
        row = i if i < 11 else i - 11
        tx = ax + 8 + col * col_w
        ty2 = row_y + 26 + row * 16
        nf2 = sans(10, True)
        d.text((tx, ty2), str(num), font=nf2, fill=BRICK)
        tf2 = fit(d, title, "DejaVuSans.ttf", 10, col_w - 26)
        d.text((tx + 22, ty2), title, font=tf2, fill=INK)
    y = row_y + row_h + 6
    # DATE CHECK bar
    d.rectangle([M, y, W - M, y + 30], fill=(242, 230, 200), outline=NAVY, width=1)
    d.rectangle([M, y, M + 6, y + 30], fill=BRICK)
    dcf = sans(10)
    lines = wrap(d, DATE_CHECK, dcf, W - 2 * M - 18)
    for j, ln in enumerate(lines[:2]):
        d.text((M + 14, y + 3 + j * 13), ln, font=dcf, fill=INK)
    y += 36
    # footer: double rule + guarantee
    d.line([(M, y), (W - M, y)], fill=NAVY, width=2)
    y += 3
    d.line([(M, y), (W - M, y)], fill=NAVY, width=1)
    y += 7
    ff = sans(10)
    t1 = "Every story above happened or was first reported on Wednesday 25 November 2026."
    d.text((W / 2 - d.textlength(t1, font=ff) / 2, y), t1, font=ff, fill=NAVY)
    y += 14
    t2 = "Sources: Reuters · CNN · AP · NOS · Sky News · IANS · Des Moines Register · WHO · WFP"
    d.text((W / 2 - d.textlength(t2, font=ff) / 2, y), t2, font=ff, fill=GREY)
    img.save(path, "PNG")


if __name__ == "__main__":
    build("/output/entry.png")
