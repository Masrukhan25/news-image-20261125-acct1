#!/usr/bin/env python3
"""news-image-20261125 — acct1 v2 revision (Masrukhan25).

Rebuilds entry.png from scratch: 48 stories, 8 regions, 3 big heroes with
instantly-recognisable scenes (tariffs container ship, chip crash, Shenzhou-24),
6 medium heroes, full-width map, UTC timeline, numbers strip, ALSO list,
DATE CHECK bar. Flat vector, PIL only, deterministic, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
W = H = 1024

# ---------------------------------------------------------------- palette
CREAM = (247, 240, 220)      # paper
PAPER = (252, 247, 233)      # panel paper
NAVY = (31, 42, 68)          # ink / borders
NAVY_DK = (20, 28, 48)
RED = (176, 58, 46)          # brick red
RED_DK = (140, 40, 32)
TEAL = (36, 110, 110)
GOLD = (212, 160, 60)
SKY = (220, 233, 238)        # map sea
LAND = (217, 196, 154)       # map land
GRID = (185, 210, 220)       # map graticule
MUTED = (107, 98, 80)
GREEN = (46, 125, 70)
INK_SOFT = (60, 60, 60)

# ---------------------------------------------------------------- fonts
DJ = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = DJ + "DejaVuSerif-Bold.ttf"
SERIF = DJ + "DejaVuSerif.ttf"
SANS = DJ + "DejaVuSans.ttf"
SANS_B = DJ + "DejaVuSans-Bold.ttf"
ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def fit_font(d, text, path, size, max_w, min_size=7):
    """Largest font size (<= size) for which text fits max_w."""
    while size > min_size:
        f = F(path, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return F(path, min_size)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, f, fill, max_w, max_lines, leading):
    """Draw wrapped text; truncate last line with ellipsis if over max_lines.
    Returns y just below the last drawn line."""
    lines = wrap(d, text, f, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        # trim last line until it fits with an ellipsis
        while lines and d.textlength(lines[-1] + " ...", font=f) > max_w:
            lines[-1] = lines[-1][:-1].strip()
        lines[-1] = lines[-1] + " ..."
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def center(d, cx, y, text, f, fill):
    d.text((cx - d.textlength(text, font=f) / 2, y), text, font=f, fill=fill)


# ---------------------------------------------------------------- data
MASTHEAD = "THE WORLD IN ONE DAY"
DATE_LINE = "WEDNESDAY 25 NOVEMBER 2026  —  48 STORIES FROM 8 REGIONS"

UTC_ITEMS = [
    ("00:08", "KOSPI sidecar trips"),
    ("00:18", "Shenzhou-24 lifts off"),
    ("03:56", "Tiangong docking"),
    ("06:30", "Cartagena raid frees all 30"),
    ("15:00", "Iowa blast"),
    (None, "USTR unveils tariffs"),
    ("23:30", "Army all-clear, zero lead"),
]

NUMBERS = [
    ("35%", "MAX TARIFF — VIETNAM"),
    ("-6.2%", "KOSPI — SEOUL"),
    ("30", "HOSTAGES FREED — CARTAGENA"),
    ("9,500", "LBS OF LEAD AZIDE — IOWA"),
    ("$94.61", "BRENT CRUDE, +3.5%"),
    ("204", "RUNS OFF 53 BALLS — 28 SIXES"),
]

# Big heroes: num, headline, body, why, region, status, source, art key
BIG = [
    dict(num=1, art="tariffs",
         head="TRUMP UNVEILS NEW TARIFFS ON 14 ECONOMIES",
         body=("USTR proposes duties after an 8-month probe: Vietnam up to 35%, "
               "India 25%, China 20%, EU 15%. Hearings 25 Jan; not yet in force."),
         why="They replace tariffs the Supreme Court struck down.",
         region="NORTH AMERICA", status="CONFIRMED", src="USTR / Reuters, 25 Nov"),
    dict(num=2, art="chip",
         head="CHIP STOCKS CRASH: KOSPI -6.2%",
         body=("Seoul plunges below 5,000 as Samsung -9.9% and SK hynix -11.1% "
               "erase Tuesday's rally; Taiex -5%, Nikkei -2.8%. Sidecar trips at 09:08."),
         why="AI doubts spread — then the Dow erased a 1,100-pt plunge.",
         region="ASIA", status="CONFIRMED", src="Korea Exchange / AP, 25 Nov"),
    dict(num=3, art="space",
         head="FIRST PAKISTANI ASTRONAUT REACHES TIANGONG",
         body=("Shenzhou-24 lifts off 00:18 UTC and docks 03:56 UTC with Tang Hongbo, "
               "Wu Yi and Muhammad Zeeshan Ali — the first foreigner aboard the station."),
         why="China opens Tiangong to the world on 75 years of ties.",
         region="ASIA", status="CONFIRMED", src="Xinhua / CMSA, 25 Nov"),
]

# Medium heroes: num, headline, body, region, status, source, badge, art key
MED = [
    dict(num=4, art="cartagena",
         head="CARTAGENA: ALL 30 HOSTAGES FREED",
         body=("Police storm the Éxito store at 01:30 after a 17-hour siege; "
               "1 captor killed, 4 arrested."),
         region="AMERICAS", status="CONFIRMED", src="Reuters / AFP",
         badge="30 FREED"),
    dict(num=5, art="refinery",
         head="HOUTHIS HIT SAUDI'S BIGGEST REFINERY",
         body=("Ras Tanura attacked; Riyadh says 4 drones downed. "
               "Brent jumps 3.5% to $94.61."),
         region="MIDDLE EAST", status="REPORTED", src="Reuters",
         badge="BRENT $94.61"),
    dict(num=6, art="iowa",
         head="IOWA BLAST DONE: ZERO LEAD FOUND",
         body=("Army detonates 9,500 lbs at 09:00; two plumes rise. "
               "EPA: zero airborne lead found."),
         region="NORTH AMERICA", status="CONFIRMED", src="EPA / CNN",
         badge="9,500 LBS"),
    dict(num=7, art="cyber",
         head="US CYBER WAVE: CIA, ODNI, FINCEN HIT",
         body=("Hackers breach an unclassified CIA–ODNI system with an AI tool; "
               "FinCEN goes offline too."),
         region="NORTH AMERICA", status="REPORTED", src="NYT / BleepingComputer",
         badge="4 AGENCIES"),
    dict(num=8, art="satellite",
         head="NATO VOWS SPACE DEFENSE",
         body=("After reports of a nuclear-armed 'Sputnik-S' in December, Rutte "
               "vows to defend 'every inch'."),
         region="EUROPE", status="REPORTED", src="NATO / NDR·WDR·SZ",
         badge="1/3 AT RISK"),
    dict(num=9, art="cricket",
         head="VAIBHAV 204 OFF 53 BALLS",
         body=("India A star smashes the fastest List A double century vs UAE — "
               "a world-record 28 sixes."),
         region="ASIA / SPORT", status="CONFIRMED", src="Rising Stars Asia Cup",
         badge="28 SIXES"),
]

# ALSO list: (num, headline) — 39 items, numbered 10..48
ALSO = [
    (10, "RUSSIA ACCUSES UKRAINE OF \"TERRORISM\""),
    (11, "DOW ERASES 1,100-PT PLUNGE, CLOSES +0.33%"),
    (12, "CORE PCE 3.3%: HOTTER THAN EXPECTED"),
    (13, "HUAWEI GUILTY ON 10 OF 12 COUNTS"),
    (14, "COP31 ENDS WITHOUT A DEAL"),
    (15, "GAZA DEATH TOLL 74,746"),
    (16, "ISRAEL KILLS HAMAS SECURITY CHIEF"),
    (17, "266 MILLION FACE ACUTE FOOD INSECURITY"),
    (18, "WHO EVACUATES DRC EBOLA STAFF"),
    (19, "N. KOREA DISMISSES SWISS DIPLOMAT"),
    (20, "SETTLER ARSON CONDEMNED AS \"TERRORISM\""),
    (21, "12,000 EVACUATED FROM MANCHESTER CONCERT"),
    (22, "ANMER HALL BREAK-IN ARRESTS"),
    (23, "GIULIANI AWARDED MEDAL OF FREEDOM"),
    (24, "ÁBREGO GARCÍA LEAVES FOR SPAIN"),
    (25, "SENEGAL AFCON CHAMPIONS REINSTATED"),
    (26, "GUKESH HOLDS SINDAROV IN OPENER"),
    (27, "IRANIAN SINGER GETS 74 LASHES"),
    (28, "SHEIKH HASINA ANNOUNCES RETURN"),
    (29, "MACRON WEIGHS SPENDING CAPS"),
    (30, "NSW $35M DRUG SYNDICATE CHARGED"),
    (31, "LEWIS PUGH SWIMS HORMUZ, 15 KM"),
    (32, "ISRAEL: IRAN BUILDING CHEMICAL WEAPONS"),
    (33, "S. KOREA EDUCATION MINISTER RESIGNS"),
    (34, "AUSTRALIA–SOLOMON SECURITY PACT"),
    (35, "DUTCH COURT: CLIMATE TARGETS BINDING"),
    (36, "EGYPT FUEL-TANKER FIRE KILLS 30+"),
    (37, "INDONESIA MINE FLOOD: 9 DEAD, 17 TRAPPED"),
    (38, "UK HEAT DEATHS HIT RECORD 5,200+"),
    (39, "RUSSIA PASSES RECORD MILITARY BUDGET"),
    (40, "ESTONIA MAY SHUT RAIL BORDER WITH RUSSIA"),
    (41, "EU PLANS €50BN TECH FUND"),
    (42, "WORLD: 6 STRAIGHT DAYS ABOVE 2°C"),
    (43, "NVIDIA BOARD PUTS HUANG UNDER SCRUTINY"),
    (44, "RUSSIAN STRIKE ON ODESA KILLS 2"),
    (45, "ZELENSKY SEEKS TOUGHER US SANCTIONS"),
    (46, "IRGC: 2 TANKERS HIT MINES IN HORMUZ"),
    (47, "BLAST NEAR TANKER OFF DUBAI"),
    (48, "HOUTHIS THREATEN JEDDAH PORTS"),
]

DATE_CHECK = (
    "DATE CHECK — LEFT OUT: Anthropic $2T IPO (19 Nov) · Villavicencio car bomb (23 Nov) · "
    "Russian extradition case (5 Nov) · Missiles over Poland (20 Nov) · Tarwekamp blast (Dec 2024). "
    "DATED INSIDE: Huawei verdict 24 Nov (reported 25 Nov in Asia) · Cartagena siege began 24 Nov 08:30 "
    "(hero = the 25 Nov raid) · NATO vow 24 Nov (hero = 25 Nov analysis) · Merkury + Sparta II 21–22 Nov "
    "(ALSO = 25 Nov refinery strikes)."
)

FOOTER_GUARANTEE = ("Every story above happened or was first reported on "
                    "Wednesday 25 November 2026.")
FOOTER_SOURCES = ("Sources: Reuters · CNN · AP · NOS · Sky News · IANS · Des Moines Register · "
                  "WHO · WFP · Xinhua · USTR · EPA · Korea JoongAng Daily")

REGION_INDEX = [
    "REGION INDEX — AMERICAS 4 · NORTH AMERICA 1, 6, 7, 11, 12, 23, 24, 43 · "
    "EUROPE 8, 10, 21, 22, 26, 29, 35, 38, 39, 40, 41, 44, 45",
    "ASIA 2, 3, 9, 13, 19, 28, 33, 37 · MIDDLE EAST 5, 15, 16, 20, 27, 31, 32, 46, 47, 48 · "
    "PACIFIC 30, 34 · AFRICA 18, 25, 36 · WORLD 14, 17, 42",
]
HERO_PLACES = ("1 Washington · 2 Seoul · 3 Jiuquan · 4 Cartagena · 5 Ras Tanura · "
               "6 Middletown, Iowa · 7 Langley, VA · 8 Brussels · 9 UAE")

# Map dots: (num, lon, lat, is_hero). Positions nudged slightly where cities
# collide at this scale (stylised map); labels in REGION INDEX / HERO_PLACES.
MAP_DOTS = [
    (1, -77.0, 38.9, True), (2, 127.0, 37.5, True), (3, 99.0, 40.0, True),
    (4, -75.5, 10.4, True), (5, 49.0, 27.0, True), (6, -91.4, 40.8, True),
    (7, -83.0, 42.0, True), (8, 4.4, 50.8, True), (9, 56.0, 23.5, True),
    (10, 20.1, 32.1, False), (11, -74.0, 40.7, False), (14, 30.7, 36.9, False),
    (15, 34.5, 31.5, False), (18, 29.5, 1.5, False), (24, -3.7, 40.4, False),
    (25, -17.4, 14.7, False), (26, 9.0, 44.0, False), (27, 53.0, 37.0, False),
    (28, 90.4, 23.8, False), (30, 151.2, -33.9, False), (34, 160.0, -9.5, False),
    (36, 29.0, 30.0, False), (38, -2.0, 52.5, False), (39, 37.6, 55.8, False),
    (40, 24.7, 59.4, False), (43, -122.0, 37.4, False), (45, 30.5, 50.4, False),
    (48, 39.2, 21.5, False),
]

# Simplified continent outlines (lon, lat) — stylised flat-vector map.
CONTINENTS = [
    # North America
    [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-132, 56), (-126, 50),
     (-124, 42), (-120, 34), (-113, 29), (-108, 24), (-102, 18), (-95, 16),
     (-90, 14), (-85, 11), (-80, 8), (-79, 9), (-77, 7), (-80, 20), (-82, 28),
     (-80, 32), (-76, 35), (-73, 41), (-69, 44), (-64, 45), (-58, 47), (-54, 50),
     (-58, 55), (-63, 58), (-68, 58), (-75, 62), (-82, 64), (-90, 66), (-95, 69),
     (-105, 68), (-120, 69), (-135, 69), (-150, 70), (-162, 70), (-168, 68)],
    # Greenland
    [(-56, 60), (-48, 60), (-42, 61), (-38, 64), (-30, 68), (-22, 70),
     (-24, 76), (-32, 78), (-45, 77), (-55, 74), (-58, 70), (-58, 64)],
    # South America
    [(-79, 9), (-77, 5), (-80, -2), (-80, -6), (-76, -12), (-71, -18),
     (-70, -24), (-70, -30), (-71, -37), (-73, -44), (-70, -50), (-66, -55),
     (-68, -52), (-64, -44), (-60, -38), (-56, -34), (-51, -31), (-47, -26),
     (-41, -22), (-39, -16), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
     (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-76, 10)],
    # Africa
    [(-17, 15), (-16, 21), (-14, 27), (-9, 31), (-5, 34), (0, 36), (8, 37),
     (11, 34), (18, 32), (24, 32), (30, 31), (33, 27), (35, 22), (37, 18),
     (40, 15), (43, 11), (48, 11), (51, 12), (46, 6), (42, 1), (40, -4),
     (38, -10), (35, -17), (33, -25), (28, -32), (20, -35), (17, -31),
     (14, -26), (12, -17), (12, -9), (13, -3), (9, 4), (4, 6), (-2, 5),
     (-8, 4), (-13, 8), (-17, 12)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-1, 49),
     (2, 51), (5, 53), (8, 55), (8, 57), (6, 58), (5, 60), (9, 62), (13, 65),
     (18, 69), (24, 71), (30, 70), (36, 68), (42, 68), (48, 68), (54, 68),
     (60, 69), (66, 69), (72, 71), (78, 72), (86, 74), (94, 75), (102, 76),
     (110, 76), (118, 74), (126, 72), (134, 72), (142, 72), (150, 70),
     (158, 69), (166, 69), (174, 66), (178, 64), (172, 60), (164, 60),
     (158, 55), (152, 58), (146, 59), (141, 54), (140, 48), (138, 44),
     (134, 42), (130, 38), (127, 35), (123, 38), (121, 34), (118, 29),
     (113, 22), (108, 18), (105, 10), (103, 7), (100, 9), (97, 15), (93, 17),
     (90, 22), (87, 21), (84, 19), (80, 15), (77, 8), (74, 13), (71, 20),
     (67, 24), (63, 25), (59, 25), (56, 27), (52, 28), (49, 30), (46, 30),
     (42, 29), (39, 28), (36, 30), (33, 31), (30, 36), (27, 36), (23, 37),
     (20, 39), (17, 42), (14, 44), (11, 44), (7, 44), (3, 43), (0, 40),
     (-2, 37), (-6, 36), (-9, 37)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 54), (0, 51), (-2, 50)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (142, 44), (144, 44), (141, 42), (139, 38), (136, 35),
     (133, 34), (130, 32)],
    # Indonesia (island chain, simplified)
    [(95, 5), (98, 3), (100, 0), (103, -2), (105, -4), (107, -6), (110, -7),
     (113, -8), (116, -9), (119, -9), (122, -10), (125, -9), (128, -8),
     (131, -6), (134, -4), (137, -2), (140, -3), (141, -5), (139, -7),
     (136, -7), (133, -5), (130, -2), (127, 0), (124, 1), (121, 0), (118, 1),
     (115, 0), (112, -1), (109, -4), (106, -6), (103, -4), (100, -1),
     (97, 2), (95, 4)],
    # Borneo
    [(109, 1), (111, 3), (113, 5), (116, 6), (118, 2), (117, -2), (114, -3),
     (111, -2), (109, 0)],
    # New Guinea
    [(131, -1), (134, -2), (137, -3), (140, -4), (143, -6), (146, -7),
     (149, -9), (147, -8), (144, -6), (141, -4), (138, -3), (135, -2), (132, -1)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (140, -16), (136, -15), (135, -12), (132, -12), (130, -13), (127, -14),
     (124, -15), (122, -17), (120, -20), (117, -20), (114, -21)],
    # New Zealand
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (175, -40),
     (172, -43), (169, -46)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (45, -25),
     (43, -21), (43, -18)],
    # Iceland
    [(-22, 64), (-18, 63), (-14, 64), (-16, 66), (-20, 66), (-23, 65)],
    # Sri Lanka
    [(80, 6), (81, 8), (80, 9)],
    # Taiwan
    [(120, 22), (121, 25), (120, 25)],
    # Philippines
    [(120, 18), (122, 17), (122, 14), (121, 11), (123, 10), (124, 12), (122, 16)],
    # Cuba
    [(-85, 22), (-80, 23), (-75, 20), (-74, 20), (-77, 21), (-82, 22)],
]

# ---------------------------------------------------------------- art helpers
def layer(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def stars(d, w, h, n=26, seed=7):
    """Deterministic star field (no random module)."""
    pts = []
    x, y = seed, seed * 3 + 1
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        y = (y * 1103515245 + 12345) % 2147483648
        pts.append((x % w, y % h, 1 + (x // 997) % 2))
    for sx, sy, r in pts:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255, 220))


def flame(d, cx, base_y, w, h, col1=(255, 180, 40), col2=(230, 80, 30)):
    """Teardrop flame: outer + inner, pointing up."""
    d.polygon([(cx - w / 2, base_y), (cx - w * 0.42, base_y - h * 0.55),
               (cx - w * 0.12, base_y - h * 0.85), (cx, base_y - h),
               (cx + w * 0.15, base_y - h * 0.7), (cx + w * 0.42, base_y - h * 0.4),
               (cx + w / 2, base_y)], fill=col2 + (255,))
    d.polygon([(cx - w * 0.28, base_y), (cx - w * 0.2, base_y - h * 0.45),
               (cx, base_y - h * 0.7), (cx + w * 0.22, base_y - h * 0.35),
               (cx + w * 0.28, base_y)], fill=col1 + (255,))


def puff(d, cx, cy, r, col):
    """Round smoke/explosion puff: cluster of overlapping circles."""
    for dx, dy, rr in [(-0.7, 0.25, 0.62), (0, -0.25, 0.8), (0.65, 0.2, 0.6),
                       (-0.3, -0.55, 0.55), (0.35, -0.5, 0.5), (0, 0.35, 0.7)]:
        d.ellipse([cx + dx * r - rr * r, cy + dy * r - rr * r,
                   cx + dx * r + rr * r, cy + dy * r + rr * r], fill=col + (255,))


# ---------------------------------------------------------------- hero art
def art_tariffs(w, h):
    """Big container ship + red tariff stamp."""
    im = layer(w, h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, h * 0.62], fill=(214, 230, 236, 255))          # sky
    d.rectangle([0, h * 0.62, w, h], fill=(28, 52, 88, 255))             # sea
    for i in range(3):                                                    # waves
        y = int(h * 0.70 + i * h * 0.09)
        d.arc([10, y - 6, w - 10, y + 14], 200, 340, fill=(120, 160, 190, 255), width=2)
    d.ellipse([w * 0.04, h * 0.05, w * 0.15, h * 0.17], fill=(255, 224, 130, 255))  # sun
    # ship hull
    hx0, hx1, hy = int(w * 0.06), int(w * 0.94), int(h * 0.60)
    d.polygon([(hx0, hy - 14), (hx1, hy - 14), (hx1 - 18, hy + 22),
               (hx0 + 26, hy + 22)], fill=(150, 40, 34, 255))
    d.rectangle([hx0, hy - 16, hx1, hy - 12], fill=(31, 42, 68, 255))
    # containers: 3 rows x 5
    cont_cols = [(176, 58, 46), (36, 110, 110), (212, 160, 60),
                 (52, 96, 160), (46, 125, 70)]
    cw, ch = (hx1 - hx0 - 70) / 5, 13
    for r in range(3):
        for c in range(5):
            x0 = hx0 + 34 + c * cw
            y0 = hy - 18 - (r + 1) * ch
            d.rectangle([x0 + 1, y0 + 1, x0 + cw - 1, y0 + ch - 1],
                        fill=cont_cols[(c + r) % 5] + (255,))
            d.line([x0 + 1, y0 + ch / 2, x0 + cw - 1, y0 + ch / 2],
                   fill=(255, 255, 255, 90), width=1)
    # bridge tower + funnel
    d.rectangle([hx1 - 58, hy - 62, hx1 - 26, hy - 16], fill=(240, 240, 235, 255))
    for i in range(3):
        d.rectangle([hx1 - 54, hy - 58 + i * 12, hx1 - 30, hy - 50 + i * 12],
                    fill=(31, 42, 68, 255))
    d.rectangle([hx0 + 8, hy - 44, hx0 + 26, hy - 16], fill=(31, 42, 68, 255))
    # red stamp (drawn on own layer, rotated) — small enough to sit fully
    # inside the panel, with a light fill so it reads over the cargo
    st = layer(120, 120)
    sd = ImageDraw.Draw(st)
    cx = cy = 60
    sd.ellipse([cx - 50, cy - 50, cx + 50, cy + 50],
               fill=(252, 247, 233, 215), outline=(176, 58, 46, 255), width=5)
    sd.ellipse([cx - 41, cy - 41, cx + 41, cy + 41], outline=(176, 58, 46, 255), width=2)
    f1 = F(SANS_B, 24)
    f2 = F(SANS_B, 13)
    center(sd, cx, cy - 26, "UP TO", f2, (176, 58, 46, 255))
    center(sd, cx, cy - 8, "35%", f1, (176, 58, 46, 255))
    center(sd, cx, cy + 22, "TARIFF", f2, (176, 58, 46, 255))
    st = st.rotate(-14, resample=Image.BICUBIC, center=(cx, cy))
    im.alpha_composite(st, (w - 124, 0))
    return im


def art_chip(w, h):
    """AI chip falling over a plunging red chart."""
    im = layer(w, h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, h], fill=(238, 236, 228, 255))
    # chart grid
    for i in range(1, 5):
        y = int(h * i / 5)
        d.line([0, y, w, y], fill=(200, 200, 190, 255), width=1)
    # plunging red line with arrowhead
    pts = [(8, 14), (70, 22), (130, 34), (185, 58), (240, 88), (300, 118)]
    d.line(pts, fill=(176, 58, 46, 255), width=5, joint="curve")
    d.polygon([(300, 118), (282, 108), (286, 124)], fill=(176, 58, 46, 255))
    d.line([(8, 14), (8, 118)], fill=(120, 120, 115, 255), width=1)
    # chip (own layer, rotated)
    ch = layer(120, 120)
    cd = ImageDraw.Draw(ch)
    cd.rectangle([28, 28, 92, 92], fill=(31, 42, 68, 255),
                 outline=(212, 160, 60, 255), width=3)
    for i in range(4):  # pins
        for j in range(3):
            cd.rectangle([28 + j * 22, 18, 34 + j * 22, 28], fill=(212, 160, 60, 255))
            cd.rectangle([28 + j * 22, 92, 34 + j * 22, 102], fill=(212, 160, 60, 255))
            cd.rectangle([18, 28 + j * 22, 28, 34 + j * 22], fill=(212, 160, 60, 255))
            cd.rectangle([92, 28 + j * 22, 102, 34 + j * 22], fill=(212, 160, 60, 255))
    f = F(SANS_B, 26)
    center(cd, 60, 44, "AI", f, (255, 255, 255, 255))
    ch = ch.rotate(-16, resample=Image.BICUBIC, center=(60, 60))
    im.alpha_composite(ch, (int(w * 0.30), int(h * 0.18)))
    # big red number + small labels
    f_big = F(SANS_B, 34)
    d.text((w * 0.60, h * 0.06), "-6.2%", font=f_big, fill=(176, 58, 46, 255))
    f_s = F(SANS_B, 11)
    d.rectangle([8, h - 24, 148, h - 6], fill=(31, 42, 68, 255))
    d.text((13, h - 22), "SAMSUNG -9.9%", font=f_s, fill=(255, 255, 255, 255))
    d.rectangle([156, h - 24, 296, h - 6], fill=(31, 42, 68, 255))
    d.text((161, h - 22), "SK HYNIX -11.1%", font=f_s, fill=(255, 255, 255, 255))
    return im


def art_space(w, h):
    """Rocket + Tiangong station above Earth's curve."""
    im = layer(w, h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, h], fill=(16, 24, 48, 255))                    # night sky
    stars(d, w, int(h * 0.75), n=30)
    # Earth curve at bottom
    d.ellipse([-w * 0.25, h * 0.78, w * 1.25, h * 1.75], fill=(52, 96, 160, 255))
    d.ellipse([w * 0.08, h * 0.86, w * 0.38, h * 1.05], fill=(70, 140, 90, 255))
    d.ellipse([w * 0.55, h * 0.92, w * 0.85, h * 1.08], fill=(70, 140, 90, 255))
    d.arc([-w * 0.25, h * 0.78, w * 1.25, h * 1.75], 180, 360,
          fill=(140, 200, 240, 255), width=3)
    d.ellipse([w * 0.62, h * 0.84, w * 0.78, h * 0.90], fill=(255, 255, 255, 220))
    d.ellipse([w * 0.18, h * 0.90, w * 0.30, h * 0.95], fill=(255, 255, 255, 200))
    # Tiangong station (upper right): core + 2 solar wings
    sx, sy = int(w * 0.62), int(h * 0.30)
    d.rectangle([sx - 52, sy - 8, sx - 8, sy + 8], fill=(40, 80, 160, 255))   # left wing
    d.rectangle([sx + 8, sy - 8, sx + 52, sy + 8], fill=(40, 80, 160, 255))  # right wing
    for x in range(sx - 52, sx + 52, 11):
        d.line([x, sy - 8, x, sy + 8], fill=(140, 180, 230, 255), width=1)
    d.rectangle([sx - 10, sy - 12, sx + 34, sy + 12], fill=(200, 200, 195, 255))
    d.rectangle([sx + 34, sy - 7, sx + 52, sy + 7], fill=(170, 170, 165, 255))
    d.text((sx - 8, sy - 11), "TIANGONG", font=F(SANS_B, 8),
           fill=(31, 42, 68, 255))
    # rocket (left, ascending diagonally)
    rx, ry = int(w * 0.30), int(h * 0.42)
    rk = layer(90, 130)
    rd = ImageDraw.Draw(rk)
    rd.polygon([(45, 2), (58, 26), (58, 96), (45, 108), (32, 96), (32, 26)],
               fill=(245, 245, 240, 255), outline=(31, 42, 68, 255))
    rd.polygon([(45, 2), (58, 26), (32, 26)], fill=(176, 58, 46, 255))
    rd.rectangle([32, 58, 58, 70], fill=(176, 58, 46, 255))
    rd.ellipse([39, 32, 51, 44], fill=(140, 200, 240, 255),
               outline=(31, 42, 68, 255))
    flame(rd, 45, 128, 26, 26)
    rk = rk.rotate(24, resample=Image.BICUBIC, center=(45, 60))
    im.alpha_composite(rk, (rx - 45, ry - 60))
    # small Pakistani flag on the capsule label (kept inside the panel)
    fx, fy = int(w * 0.52), int(h * 0.52)
    d.rectangle([fx, fy, fx + 26, fy + 16], fill=(20, 90, 50, 255))
    d.ellipse([fx + 8, fy + 3, fx + 18, fy + 13], fill=(255, 255, 255, 255))
    d.ellipse([fx + 10, fy + 4, fx + 18, fy + 12], fill=(20, 90, 50, 255))
    d.text((fx + 30, fy + 2), "1ST PAKISTANI", font=F(SANS_B, 9),
           fill=(255, 255, 255, 255))
    return im


def art_cartagena(w, h):
    """Supermarket storefront + police cordon."""
    im = layer(w, h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, h], fill=(232, 222, 196, 255))
    # storefront
    d.rectangle([8, 26, w - 8, h - 26], fill=(240, 235, 220, 255),
                outline=(31, 42, 68, 255), width=2)
    # solid red fascia with the shop name (readable), awning stripes below
    d.rectangle([10, 28, w - 10, 44], fill=(176, 58, 46, 255))
    d.text((14, 30), "ÉXITO", font=F(SANS_B, 13), fill=(255, 255, 255, 255))
    for i in range(6):
        col = (176, 58, 46, 255) if i % 2 == 0 else (245, 245, 240, 255)
        x0 = 10 + i * (w - 20) / 6
        d.polygon([(x0, 46), (x0 + (w - 20) / 6, 46),
                   (x0 + (w - 20) / 6, 58), (x0, 58)], fill=col)
    # glass doors + windows
    d.rectangle([16, 64, 62, h - 30], fill=(140, 190, 210, 255),
                outline=(31, 42, 68, 255))
    d.rectangle([70, 64, 116, h - 30], fill=(160, 200, 215, 255),
                outline=(31, 42, 68, 255))
    d.line([39, 64, 39, h - 30], fill=(31, 42, 68, 255), width=2)
    d.line([93, 64, 93, h - 30], fill=(31, 42, 68, 255), width=2)
    # police car
    d.rectangle([w - 62, h - 40, w - 10, h - 24], fill=(31, 42, 68, 255))
    d.polygon([(w - 56, h - 40), (w - 48, h - 52), (w - 28, h - 52),
               (w - 18, h - 40)], fill=(31, 42, 68, 255))
    d.ellipse([w - 56, h - 26, w - 46, h - 16], fill=(20, 20, 20, 255))
    d.ellipse([w - 24, h - 26, w - 14, h - 16], fill=(20, 20, 20, 255))
    d.rectangle([w - 44, h - 56, w - 34, h - 50], fill=(200, 40, 40, 255))
    # police tape across the front
    d.rectangle([6, h - 22, w - 6, h - 12], fill=(240, 200, 40, 255))
    for x in range(8, w - 8, 14):
        d.polygon([(x, h - 22), (x + 7, h - 22), (x + 2, h - 12), (x - 5, h - 12)],
                  fill=(31, 42, 68, 255))
    return im


def art_iowa(w, h):
    """Real explosion cloud over farmland + dust plume."""
    im = layer(w, h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, h * 0.55], fill=(214, 228, 236, 255))           # sky
    d.ellipse([w * 0.78, h * 0.06, w * 0.92, h * 0.20], fill=(255, 240, 180, 255))
    # farmland
    d.rectangle([0, h * 0.55, w, h], fill=(120, 150, 80, 255))
    d.polygon([(0, h * 0.55), (w, h * 0.55), (w, h * 0.72), (0, h * 0.72)],
              fill=(150, 120, 70, 255))
    d.rectangle([0, h * 0.72, w, h], fill=(110, 140, 75, 255))
    for i in range(5):  # field rows
        y = int(h * (0.76 + i * 0.05))
        d.line([0, y, w, y], fill=(90, 115, 60, 255), width=1)
    # barn + silo (left)
    d.rectangle([8, h * 0.58, 34, h * 0.74], fill=(150, 50, 40, 255))
    d.polygon([(6, h * 0.58), (21, h * 0.50), (36, h * 0.58)], fill=(90, 30, 25, 255))
    d.ellipse([38, h * 0.52, 50, h * 0.74], fill=(180, 180, 175, 255))
    d.ellipse([38, h * 0.52, 50, h * 0.58], fill=(140, 140, 135, 255))
    # explosion: bright core + orange shell + grey smoke base
    cx, cy = int(w * 0.58), int(h * 0.34)
    puff(d, cx, cy + 6, 34, (120, 120, 115))                              # smoke
    puff(d, cx, cy, 30, (230, 120, 40))                                   # orange shell
    puff(d, cx, cy - 4, 20, (255, 190, 60))                               # yellow core
    puff(d, cx, cy - 2, 11, (255, 240, 170))                              # white-hot core
    # dust plume trailing right (southwest drift)
    d.polygon([(cx + 10, cy + 18), (w - 4, cy + 6), (w - 4, cy + 26),
               (cx + 8, cy + 30)], fill=(200, 195, 180, 255))
    d.polygon([(cx + 14, cy + 22), (w - 4, cy + 14), (w - 4, cy + 20),
               (cx + 12, cy + 26)], fill=(180, 175, 160, 255))
    return im


def art_cyber(w, h):
    """Agency building + hacked screen."""
    im = layer(w, h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, h], fill=(24, 32, 56, 255))                     # dark blue
    # agency building (left half)
    d.rectangle([6, h * 0.30, w * 0.52, h - 8], fill=(210, 205, 190, 255))
    d.polygon([(4, h * 0.30), (w * 0.27, h * 0.18), (w * 0.54, h * 0.30)],
              fill=(180, 175, 160, 255))
    for i in range(4):
        x0 = 12 + i * 22
        d.rectangle([x0, h * 0.36, x0 + 10, h - 12], fill=(160, 155, 140, 255))
    d.rectangle([w * 0.10, h * 0.42, w * 0.44, h * 0.50], fill=(31, 42, 68, 255))
    d.text((w * 0.13, h * 0.43), "CIA · ODNI", font=F(SANS_B, 8),
           fill=(255, 255, 255, 255))
    # big screen (right half)
    sx0, sy0, sx1, sy1 = int(w * 0.56), int(h * 0.14), w - 6, int(h * 0.82)
    d.rectangle([sx0, sy0, sx1, sy1], fill=(12, 20, 34, 255),
                outline=(212, 160, 60, 255), width=2)
    for i, ln in enumerate([14, 26, 20, 28, 16]):
        y = sy0 + 8 + i * 9
        d.line([sx0 + 6, y, sx0 + 6 + ln, y], fill=(80, 220, 120, 255), width=2)
    # red warning triangle + BREACH
    tx, ty = (sx0 + sx1) // 2, sy0 + 52
    d.polygon([(tx, ty - 12), (tx + 12, ty + 8), (tx - 12, ty + 8)],
              fill=(220, 50, 40, 255))
    d.text((tx - 2, ty - 8), "!", font=F(SANS_B, 12), fill=(255, 255, 255, 255))
    d.text((sx0 + 8, sy1 - 16), "BREACH", font=F(SANS_B, 11),
           fill=(220, 50, 40, 255))
    return im


def art_refinery(w, h):
    """Refinery towers burning at dusk + drone."""
    im = layer(w, h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, h * 0.55], fill=(60, 50, 70, 255))              # dusk sky
    d.rectangle([0, h * 0.45, w, h * 0.55], fill=(230, 140, 60, 255))     # horizon glow
    d.ellipse([w * 0.08, h * 0.06, w * 0.20, h * 0.18], fill=(240, 200, 120, 255))
    # ground
    d.rectangle([0, h * 0.55, w, h], fill=(40, 38, 44, 255))
    # towers
    for x0, tw, th in [(10, 16, 42), (32, 12, 56), (50, 18, 36), (72, 12, 50),
                       (92, 16, 40), (114, 12, 46)]:
        d.rectangle([x0, h - th - 22, x0 + tw, h - 22], fill=(25, 25, 30, 255))
        d.rectangle([x0 + 2, h - th - 26, x0 + tw - 2, h - th - 22],
                    fill=(25, 25, 30, 255))
        for wy in range(int(h - th - 14), int(h - 26), 8):
            d.rectangle([x0 + 3, wy, x0 + tw - 3, wy + 3], fill=(240, 200, 90, 255))
    # storage tanks
    d.ellipse([w - 34, h - 44, w - 8, h - 22], fill=(70, 68, 72, 255))
    d.rectangle([w - 34, h - 34, w - 8, h - 22], fill=(70, 68, 72, 255))
    # flames on two towers + smoke
    flame(d, 40, h - 62, 16, 22)
    flame(d, 100, h - 56, 13, 18)
    puff(d, 40, h - 78, 12, (90, 90, 95))
    puff(d, 100, h - 70, 10, (90, 90, 95))
    # drone silhouette (upper right)
    dx, dy = int(w * 0.80), int(h * 0.16)
    d.ellipse([dx - 8, dy - 3, dx + 8, dy + 3], fill=(15, 15, 18, 255))
    d.line([dx - 12, dy - 6, dx + 12, dy - 6], fill=(15, 15, 18, 255), width=2)
    d.line([dx - 12, dy + 6, dx + 12, dy + 6], fill=(15, 15, 18, 255), width=2)
    return im


def art_satellite(w, h):
    """Nuclear-armed satellite in orbit above Earth."""
    im = layer(w, h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, h], fill=(14, 20, 44, 255))
    stars(d, w, int(h * 0.70), n=22, seed=11)
    # Earth arc
    d.ellipse([-w * 0.3, h * 0.72, w * 1.3, h * 1.7], fill=(52, 96, 160, 255))
    d.ellipse([w * 0.10, h * 0.82, w * 0.34, h * 0.98], fill=(70, 140, 90, 255))
    d.arc([-w * 0.3, h * 0.72, w * 1.3, h * 1.7], 180, 360,
          fill=(140, 200, 240, 255), width=2)
    # red orbit ellipse
    d.ellipse([6, h * 0.10, w - 6, h * 0.62], outline=(200, 70, 60, 255), width=2)
    # satellite: gold body + blue panels
    sx, sy = int(w * 0.52), int(h * 0.32)
    d.rectangle([sx - 46, sy - 7, sx - 10, sy + 7], fill=(40, 80, 160, 255))
    d.rectangle([sx + 10, sy - 7, sx + 46, sy + 7], fill=(40, 80, 160, 255))
    for x in range(sx - 46, sx + 46, 9):
        d.line([x, sy - 7, x, sy + 7], fill=(140, 180, 230, 255), width=1)
    d.rectangle([sx - 10, sy - 11, sx + 10, sy + 11], fill=(212, 160, 60, 255),
                outline=(120, 80, 20, 255))
    # radiation trefoil on the body
    cx, cy, r = sx, sy, 6
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(176, 58, 46, 255))
    for a0 in (270, 30, 150):
        d.pieslice([cx - r, cy - r, cx + r, cy + r], a0, a0 + 50,
                   fill=(176, 58, 46, 255))
    d.text((sx - 26, sy + 16), "SPUTNIK-S", font=F(SANS_B, 8),
           fill=(255, 255, 255, 255))
    return im


def art_cricket(w, h):
    """Batsman + giant 204 under floodlights."""
    im = layer(w, h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, h * 0.52], fill=(46, 90, 60, 255))              # stands
    for i in range(4):                                                    # crowd rows
        y = int(h * (0.10 + i * 0.10))
        for x in range(6, w - 6, 12):
            col = [(220, 220, 210), (200, 60, 50), (240, 200, 90),
                   (80, 140, 200)][(x // 12 + i) % 4]
            d.ellipse([x, y, x + 6, y + 6], fill=col + (255,))
    # floodlights
    for fx in (14, w - 26):
        d.rectangle([fx, 6, fx + 12, 14], fill=(240, 240, 230, 255))
        d.line([fx + 6, 14, fx + 6, 30], fill=(220, 220, 210, 255), width=2)
    # pitch
    d.rectangle([0, h * 0.52, w, h], fill=(110, 160, 80, 255))
    d.rectangle([w * 0.30, h * 0.52, w * 0.70, h], fill=(214, 190, 140, 255))
    # giant 204
    f_big = F(SANS_B, 44)
    d.text((w * 0.04, h * 0.54), "204", font=f_big, fill=(255, 255, 255, 255))
    # batsman silhouette (navy) mid-swing
    bx, by = int(w * 0.68), int(h * 0.78)
    d.ellipse([bx - 7, by - 34, bx + 7, by - 20], fill=(31, 42, 68, 255))   # helmet
    d.polygon([(bx - 8, by - 22), (bx + 8, by - 22), (bx + 6, by + 2),
               (bx - 6, by + 2)], fill=(31, 42, 68, 255))                 # torso
    d.polygon([(bx - 6, by + 2), (bx + 6, by + 2), (bx + 12, by + 20),
               (bx + 4, by + 20)], fill=(31, 42, 68, 255))                # legs
    d.polygon([(bx - 6, by + 2), (bx + 6, by + 2), (bx - 2, by + 20),
               (bx - 10, by + 20)], fill=(31, 42, 68, 255))
    d.line([bx + 6, by - 16, bx + 26, by - 38], fill=(150, 100, 50, 255), width=5)  # bat
    # ball with motion lines
    d.ellipse([bx + 34, by - 44, bx + 42, by - 36], fill=(200, 40, 40, 255))
    d.line([bx + 20, by - 40, bx + 32, by - 40], fill=(255, 255, 255, 255), width=2)
    d.line([bx + 22, by - 34, bx + 32, by - 36], fill=(255, 255, 255, 255), width=2)
    return im


ART = {
    "tariffs": art_tariffs, "chip": art_chip, "space": art_space,
    "cartagena": art_cartagena, "iowa": art_iowa, "cyber": art_cyber,
    "refinery": art_refinery, "satellite": art_satellite, "cricket": art_cricket,
}

# ---------------------------------------------------------------- map
def draw_map(d, x0, y0, x1, y1):
    """Full-width world map: sea, graticule, continents, numbered dots."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    # graticule every 30 deg lon / 20 deg lat
    for lon in range(-150, 181, 30):
        x = x0 + (lon + 170) * (x1 - x0) / 360.0
        d.line([x, y0, x, y1], fill=GRID, width=1)
    for lat in range(-40, 61, 20):
        y = y0 + (75 - lat) * (y1 - y0) / 130.0
        d.line([x0, y, x1, y], fill=GRID, width=1)
    # continents
    for poly in CONTINENTS:
        pts = [(x0 + (lon + 170) * (x1 - x0) / 360.0,
                y0 + (75 - lat) * (y1 - y0) / 130.0) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=NAVY)
    # dots
    for num, lon, lat, is_hero in MAP_DOTS:
        cx = x0 + (lon + 170) * (x1 - x0) / 360.0
        cy = y0 + (75 - lat) * (y1 - y0) / 130.0
        if is_hero:
            r, col, fs = 8, RED, 8
        else:
            r, col, fs = 6, NAVY, 7
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col,
                  outline=(255, 255, 255), width=1)
        f = F(SANS_B, fs)
        t = str(num)
        d.text((cx - d.textlength(t, font=f) / 2, cy - fs / 2 - 1), t,
               font=f, fill=(255, 255, 255))


def badge(d, cx, cy, num):
    """Red number badge (circle) centred at cx, cy."""
    r = 13
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
              outline=(255, 255, 255), width=2)
    f = F(SANS_B, 13)
    t = str(num)
    d.text((cx - d.textlength(t, font=f) / 2, cy - 7), t, font=f,
           fill=(255, 255, 255))


def chip(d, x, y, text):
    """Small red data chip; returns width used."""
    f = F(SANS_B, 9)
    tw = d.textlength(text, font=f)
    w = int(tw + 12)
    d.rounded_rectangle([x, y, x + w, y + 15], radius=4, fill=RED)
    d.text((x + 6, y + 2), text, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- page assembly
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # outer double border
    d.rectangle([8, 8, W - 9, H - 9], outline=NAVY, width=3)
    d.rectangle([12, 12, W - 13, H - 13], outline=NAVY, width=1)

    # ---- masthead
    f_title = fit_font(d, MASTHEAD, SERIF_B, 46, 992)
    center(d, W // 2, 18, MASTHEAD, f_title, NAVY)
    f_date = fit_font(d, DATE_LINE, SANS_B, 16, 992)
    center(d, W // 2, 70, DATE_LINE, f_date, RED)
    d.line([16, 92, 1008, 92], fill=NAVY, width=2)
    d.line([16, 95, 1008, 95], fill=NAVY, width=1)

    # ---- UTC strip
    parts = ["THE DAY IN UTC"]
    for tm, ev in UTC_ITEMS:
        parts.append(f"{tm} {ev}" if tm else ev)
    utc_text = "  ·  ".join(parts)
    f_utc = fit_font(d, utc_text, SANS_B, 10, 992, min_size=8)
    center(d, W // 2, 100, utc_text, f_utc, NAVY)

    # ---- numbers strip
    y0, y1 = 120, 176
    d.line([16, y0, 1008, y0], fill=NAVY, width=1)
    d.line([16, y1, 1008, y1], fill=NAVY, width=1)
    for i, (big, lab) in enumerate(NUMBERS):
        cx = 16 + (i + 0.5) * 992 / 6
        if i:
            d.line([16 + i * 992 / 6, y0 + 4, 16 + i * 992 / 6, y1 - 4],
                   fill=(190, 180, 160), width=1)
        f_big = fit_font(d, big, SANS_B, 25, 150)
        center(d, cx, y0 + 4, big, f_big, RED)
        f_lab = F(SANS_B, 8)
        for j, ln in enumerate(wrap(d, lab, f_lab, 150)):
            center(d, cx, y0 + 32 + j * 10, ln, f_lab, NAVY)

    # ---- big heroes (3 columns)
    for i, hro in enumerate(BIG):
        x = 16 + i * 328
        w = 320
        y_top, y_bot = 180, 402
        d.rectangle([x, y_top, x + w, y_bot], fill=PAPER, outline=NAVY, width=2)
        # illustration layer (clipped to its own box by construction)
        art = ART[hro["art"]](w - 4, 112)
        img.paste(art, (x + 2, y_top + 2), art)
        if i == 0:  # TOP STORY ribbon
            d.rectangle([x + 2, y_top + 2, x + w - 2, y_top + 20], fill=RED)
            f_r = F(SANS_B, 10)
            center(d, x + w // 2, y_top + 5, "★  TOP STORY  ★", f_r,
                   (255, 255, 255))
        badge(d, x + 18, y_top + 36, hro["num"])
        # headline
        f_head = fit_font(d, hro["head"], SERIF_B, 13, w - 16, min_size=11)
        y = draw_wrapped(d, x + 8, y_top + 118, hro["head"], f_head, NAVY,
                         w - 16, 2, 15)
        # body
        f_body = F(SANS, 10)
        y = draw_wrapped(d, x + 8, y + 3, hro["body"], f_body, INK_SOFT,
                         w - 16, 3, 12)
        # WHY line
        why = "WHY: " + hro["why"]
        f_why = fit_font(d, why, ITALIC, 10, w - 16, min_size=8)
        d.text((x + 8, y_bot - 30), why, font=f_why, fill=RED_DK)
        # footer: region · status left, source right
        f_f = F(SANS_B, 8)
        d.text((x + 8, y_bot - 14),
               f"{hro['region']} · {hro['status']}", font=f_f, fill=RED)
        f_s = F(SANS, 8)
        sw = d.textlength(hro["src"], font=f_s)
        d.text((x + w - 8 - sw, y_bot - 14), hro["src"], font=f_s, fill=MUTED)

    # ---- medium heroes (6 columns)
    for i, hro in enumerate(MED):
        x = 18 + i * 166
        w = 158
        y_top, y_bot = 406, 594
        d.rectangle([x, y_top, x + w, y_bot], fill=PAPER, outline=NAVY, width=2)
        art = ART[hro["art"]](w - 4, 96)
        img.paste(art, (x + 2, y_top + 2), art)
        # data chip top-right of the illustration
        f_c = F(SANS_B, 9)
        cw = int(d.textlength(hro["badge"], font=f_c) + 12)
        chip(d, x + w - 4 - cw, y_top + 6, hro["badge"])
        # small number badge (r=11) top-left
        r = 11
        cx, cy = x + 14, y_top + 16
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                  outline=(255, 255, 255), width=2)
        f_n = F(SANS_B, 11)
        t = str(hro["num"])
        d.text((cx - d.textlength(t, font=f_n) / 2, cy - 6), t, font=f_n,
               fill=(255, 255, 255))
        # headline (2 lines)
        f_head = fit_font(d, hro["head"], SANS_B, 11, w - 12, min_size=10)
        draw_wrapped(d, x + 6, y_top + 102, hro["head"], f_head, NAVY,
                     w - 12, 2, 13)
        # body (3 lines)
        f_body = F(SANS, 9)
        draw_wrapped(d, x + 6, y_top + 130, hro["body"], f_body, INK_SOFT,
                     w - 12, 3, 11)
        # footer: region · status / source on two lines
        f_f = F(SANS_B, 8)
        d.text((x + 6, y_bot - 22),
               f"{hro['region']} · {hro['status']}", font=f_f, fill=RED)
        f_s = F(SANS, 8)
        d.text((x + 6, y_bot - 11), hro["src"], font=f_s, fill=MUTED)

    # ---- map (full width)
    d.text((16, 598), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=NAVY)
    f_mn = F(SANS_B, 9)
    mn = "28 NUMBERED PLACES"
    d.text((1008 - d.textlength(mn, font=f_mn), 600), mn, font=f_mn, fill=MUTED)
    d.rectangle([16, 614, 1008, 740], outline=NAVY, width=2)
    draw_map(d, 17, 615, 1007, 739)
    f_idx = F(SANS, 9)
    for j, ln in enumerate(REGION_INDEX):
        d.text((16, 744 + j * 11), ln, font=f_idx, fill=NAVY)
    d.text((16, 766), HERO_PLACES, font=f_idx, fill=MUTED)

    # ---- ALSO list (3 columns x 13 rows)
    d.text((16, 782), "ALSO ON 25 NOVEMBER", font=F(SANS_B, 12), fill=NAVY)
    f_num = F(SANS_B, 9)
    for k, (num, head) in enumerate(ALSO):
        col, row = k // 13, k % 13
        x = 16 + col * 332
        y = 800 + row * 10
        d.text((x, y), str(num), font=f_num, fill=RED)
        f_h = fit_font(d, head, SANS, 9, 320 - 22, min_size=8)
        d.text((x + 20, y), head, font=f_h, fill=NAVY)

    # ---- DATE CHECK
    d.rectangle([16, 934, 20, 962], fill=RED)
    f_dc = fit_font(d, DATE_CHECK, SANS, 9, 972, min_size=8)
    draw_wrapped(d, 26, 934, DATE_CHECK, f_dc, NAVY, 972, 2, 12)

    # ---- footer
    d.line([16, 968, 1008, 968], fill=NAVY, width=2)
    d.line([16, 971, 1008, 971], fill=NAVY, width=1)
    f_g = F(SANS_B, 9)
    center(d, W // 2, 976, FOOTER_GUARANTEE, f_g, NAVY)
    f_s2 = F(SANS, 8)
    center(d, W // 2, 990, FOOTER_SOURCES, f_s2, MUTED)

    img.save(OUT, "PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    import hashlib
    p = build()
    data = open(p, "rb").read()
    im = Image.open(p)
    print(f"saved {p}")
    print(f"size {im.size} bytes {len(data)} sha256 "
          f"{hashlib.sha256(data).hexdigest()}")
