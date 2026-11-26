# build.py — news-image-20261125 acct1 v3 (Masrukhan25)
# "The World in One Day" — Wednesday 25 November 2026, 48 stories, 10 regions.
# Flat-vector newspaper, PIL only, deterministic, no network.
# v3 fixes vs v2 (dev 96.9%): 12 illustrated mediums (was 6), region chips +
# fields row, small bottom-left map (was full-width), grander Tiangong hero,
# proper UTC timeline strip, deeper DATE CHECK, big KOSPI number in hero 2.
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

CREAM = (246, 240, 224)
PAPER = (253, 251, 243)
NAVY = (22, 35, 60)
NAVY2 = (38, 58, 92)
RED = (176, 58, 46)
RED_D = (140, 40, 30)
INK = (26, 26, 26)
GREY = (107, 107, 107)
TAN = (216, 201, 163)
TAN_D = (198, 178, 132)
GOLD = (201, 162, 39)
GREEN = (46, 110, 70)
BLUE = (52, 96, 150)
TEAL = (32, 120, 118)
ORANGE = (196, 106, 28)
PURPLE = (104, 78, 150)
OCHRE = (176, 138, 44)
SKY = (168, 196, 224)
SEA = (46, 88, 140)

FDIR = "/usr/share/fonts/truetype/dejavu"
LDIR = "/usr/share/fonts/truetype/liberation"
def F(size, bold=False, serif=False, italic=False):
    if serif:
        if bold and italic:
            return ImageFont.truetype(os.path.join(LDIR, "LiberationSerif-BoldItalic.ttf"), size)
        if bold:
            name = "DejaVuSerif-Bold.ttf"
        elif italic:
            return ImageFont.truetype(os.path.join(LDIR, "LiberationSerif-Italic.ttf"), size)
        else:
            name = "DejaVuSerif.ttf"
        return ImageFont.truetype(os.path.join(FDIR, name), size)
    if bold:
        name = "DejaVuSans-Bold.ttf"
        return ImageFont.truetype(os.path.join(FDIR, name), size)
    if italic:
        return ImageFont.truetype(os.path.join(LDIR, "LiberationSans-Italic.ttf"), size)
    return ImageFont.truetype(os.path.join(FDIR, "DejaVuSans.ttf"), size)

def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split(" "):
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def text_h(d, text, font, width, lh):
    return len(wrap(d, text, font, width)) * lh

def draw_lines(d, x, y, lines, font, fill, lh, align="left", width=None):
    for ln in lines:
        if align == "center":
            d.text((x + (width - d.textlength(ln, font=font)) / 2, y), ln,
                   font=font, fill=fill)
        elif align == "right":
            d.text((x + width - d.textlength(ln, font=font), y), ln,
                   font=font, fill=fill)
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def chip(d, x, y, w, h, text, bg, fg, font):
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    tw = d.textlength(text, font=font)
    d.text((x + (w - tw) / 2, y + (h - font.size) / 2 - 1), text, font=font, fill=fg)

def num_badge(d, cx, cy, r, num, fill=RED):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=(255, 255, 255), width=2)
    f = F(15 if len(str(num)) < 2 else 13, bold=True)
    t = str(num)
    d.text((cx - d.textlength(t, font=f) / 2, cy - f.size / 2 - 1), t, font=f, fill=(255, 255, 255))

def rule(d, x, y, w, color=NAVY, width=1):
    d.line([(x, y), (x + w, y)], fill=color, width=width)

# ------------------------------------------------------------------ DATA
MASTHEAD = "Wednesday 25 November 2026"
SUBHEAD = ("US proposes tariffs on 14 economies \u00b7 AI doubts sink Asian chip "
           "stocks \u00b7 Pakistan's first astronaut docks at Tiangong")
TOPBAR = ("THE WORLD IN ONE DAY \u00b7 48 STORIES \u00b7 10 REGIONS \u00b7 17 FIELDS "
          "\u00b7 ALL FIRST REPORTED ON WEDNESDAY 25 NOVEMBER 2026")

REGIONS = [
    ("N. AMERICA", 8, NAVY), ("LATIN AMERICA", 2, TEAL), ("EUROPE", 12, BLUE),
    ("MIDDLE EAST", 10, RED), ("N. AFRICA", 1, OCHRE),
    ("SUB-SAHARAN AFRICA", 2, GREEN), ("SOUTH ASIA", 3, ORANGE),
    ("EAST & SE ASIA", 5, PURPLE), ("OCEANIA", 2, (28, 96, 110)),
    ("GLOBAL", 3, (110, 110, 110)),
]

FIELDS = [("War", 10), ("Security", 5), ("Climate", 4), ("Crime", 3),
          ("Disaster", 3), ("Sport", 3), ("Justice", 3), ("Diplomacy", 3),
          ("Politics", 3), ("Markets", 2), ("Economy", 2), ("Tech", 2),
          ("Trade", 1), ("Space", 1), ("Health", 1), ("Humanitarian", 1),
          ("Environment", 1)]

NUMBERS = [
    ("35%", "MAX TARIFF \u2014 VIETNAM"),
    ("-6.2%", "KOSPI \u2014 SEOUL"),
    ("30", "HOSTAGES FREED \u2014 CARTAGENA"),
    ("9,500", "LBS OF LEAD AZIDE \u2014 IOWA"),
    ("$94.61", "BRENT CRUDE, +3.5%"),
    ("204", "RUNS OFF 53 BALLS \u2014 28 SIXES"),
]

UTC_A = [("00:08", "KOSPI sidecar trips"), ("00:18", "Shenzhou-24 lifts off"),
         ("03:56", "Tiangong docking"), ("06:30", "Cartagena raid frees all 30")]
UTC_B = [("09:08", "KOSPI closes \u22126.2%"), ("15:00", "Iowa blast"),
         ("USTR", "unveils tariffs"), ("23:30", "Army all-clear, zero lead")]

BIG = [
    dict(num=1, art="tariffs",
         head="TRUMP UNVEILS NEW TARIFFS ON 14 ECONOMIES",
         body=("USTR proposes duties after an 8-month probe: Vietnam up to 35%, "
               "India 25%, China 20%, EU 15%. Hearings 25 Jan; not yet in force."),
         why="They replace tariffs the Supreme Court struck down.",
         region="NORTH AMERICA", status="CONFIRMED", src="USTR / Reuters, 25 Nov",
         place="WASHINGTON \u00b7 TRADE"),
    dict(num=2, art="chip",
         head="CHIP STOCKS CRASH: KOSPI -6.2%",
         body=("Seoul plunges below 5,000 as Samsung -9.9% and SK hynix -11.1% "
               "erase Tuesday's rally; Taiex -5%, Nikkei -2.8%. Sidecar trips at 09:08."),
         why="AI doubts spread \u2014 then the Dow erased a 1,100-pt plunge.",
         region="ASIA", status="CONFIRMED", src="Korea Exchange / AP, 25 Nov",
         place="SEOUL \u00b7 TOKYO \u00b7 TAIPEI \u00b7 MARKETS"),
    dict(num=3, art="space",
         head="FIRST PAKISTANI ASTRONAUT REACHES TIANGONG",
         body=("Shenzhou-24 lifts off 00:18 UTC and docks 03:56 UTC with Tang Hongbo, "
               "Wu Yi and Muhammad Zeeshan Ali \u2014 the first foreigner aboard the station."),
         why="China opens Tiangong to the world on 75 years of ties.",
         region="ASIA", status="CONFIRMED", src="Xinhua / CMSA, 25 Nov",
         place="JIUQUAN, CHINA \u00b7 SPACE"),
]

MED = [
    dict(num=4, art="cartagena",
         head="CARTAGENA: ALL 30 HOSTAGES FREED",
         body=("Police storm the \u00c9xito store at 01:30 after a 17-hour siege; "
               "1 killed, 4 held."),
         region="AMERICAS", status="CONFIRMED", src="Reuters / AFP",
         badge="30 FREED", place="CARTAGENA \u00b7 WAR"),
    dict(num=5, art="refinery",
         head="HOUTHIS HIT SAUDI'S BIGGEST REFINERY",
         body=("Ras Tanura attacked; Riyadh says 4 drones downed. "
               "Brent jumps 3.5% to $94.61."),
         region="MIDDLE EAST", status="REPORTED", src="Reuters",
         badge="BRENT $94.61", place="RAS TANURA, SAUDI ARABIA \u00b7 WAR"),
    dict(num=6, art="iowa",
         head="IOWA BLAST DONE: ZERO LEAD FOUND",
         body=("Army detonates 9,500 lbs at 09:00; two plumes rise. "
               "EPA: zero airborne lead found."),
         region="NORTH AMERICA", status="CONFIRMED", src="EPA / CNN",
         badge="9,500 LBS", place="MIDDLETOWN, IOWA \u00b7 DISASTER"),
    dict(num=7, art="cyber",
         head="US CYBER WAVE: CIA, ODNI, FINCEN HIT",
         body=("Hackers breach an unclassified CIA\u2013ODNI system with an AI tool; "
               "FinCEN goes offline."),
         region="NORTH AMERICA", status="REPORTED", src="NYT / BleepingComputer",
         badge="4 AGENCIES", place="LANGLEY, VA \u00b7 SECURITY"),
    dict(num=8, art="satellite",
         head="NATO VOWS SPACE DEFENSE",
         body=("After reports of a nuclear-armed 'Sputnik-S', Rutte "
               "vows to defend 'every inch'."),
         region="EUROPE", status="REPORTED", src="NATO / NDR\u00b7WDR\u00b7SZ",
         badge="1/3 AT RISK", place="BRUSSELS \u00b7 SECURITY"),
    dict(num=9, art="cricket",
         head="VAIBHAV 204 OFF 53 BALLS",
         body=("India A star smashes the fastest List A double century vs UAE: "
               "a record 28 sixes."),
         region="ASIA / SPORT", status="CONFIRMED", src="Rising Stars Asia Cup",
         badge="28 SIXES", place="UAE \u00b7 SPORT"),
    dict(num=10, art="tanker",
         head="FUEL-TANKER FIRE KILLS 30+ NEAR CAIRO",
         body=("Tanker explodes on Cairo ring road; 30 dead, 21 injured."),
         region="N. AFRICA", status="CONFIRMED", src="AP / Health Ministry",
         badge="30 DEAD", place="GIZA, EGYPT \u00b7 DISASTER"),
    dict(num=11, art="odesa",
         head="RUSSIAN STRIKE ON ODESA KILLS 2",
         body=("Strike hits cars and buildings in Odesa; 2 killed, "
               "3 hurt, including a child."),
         region="EUROPE", status="REPORTED", src="Reuters",
         badge="2 KILLED", place="ODESA, UKRAINE \u00b7 WAR"),
    dict(num=12, art="gaza",
         head="GAZA DEATH TOLL REACHES 74,746",
         body=("Toll at 74,746 killed and 176,234 hurt since Oct 2023; "
               "1,679 since the ceasefire."),
         region="MIDDLE EAST", status="REPORTED", src="WAFA / Gaza MoH",
         badge="74,746", place="GAZA CITY \u00b7 WAR"),
    dict(num=13, art="huawei",
         head="HUAWEI GUILTY ON 10 OF 12 COUNTS",
         body=("A US jury convicts Huawei on 10 of 12 counts \u2014 but clears it "
               "of racketeering."),
         region="N. AMERICA", status="CONFIRMED", src="SCMP / Reuters",
         badge="10 OF 12", place="NEW YORK, US \u00b7 JUSTICE"),
    dict(num=14, art="climate",
         head="WORLD: 6 STRAIGHT DAYS ABOVE 2\u00b0C",
         body=("Earth's average temperature tops 2\u00b0C above pre-industrial "
               "for a sixth day in a row."),
         region="GLOBAL", status="REPORTED", src="Copernicus",
         badge="+2\u00b0C", place="WORLD \u00b7 CLIMATE"),
    dict(num=15, art="heat",
         head="UK HEAT DEATHS HIT RECORD 5,200+",
         body=("Heat deaths in England pass 5,200 in 2026 \u2014 the highest "
               "toll on record."),
         region="EUROPE", status="CONFIRMED", src="ONS",
         badge="5,200+", place="LONDON \u00b7 CLIMATE"),
]

ALSO = [
    (16, "ISRAEL KILLS HAMAS SECURITY CHIEF"),
    (17, "266 MILLION FACE ACUTE FOOD INSECURITY"),
    (18, "WHO EVACUATES DRC EBOLA STAFF"),
    (19, "N. KOREA DISMISSES SWISS DIPLOMAT"),
    (20, "SETTLER ARSON CONDEMNED AS \"TERRORISM\""),
    (21, "12,000 EVACUATED FROM MANCHESTER CONCERT"),
    (22, "ANMER HALL BREAK-IN ARRESTS"),
    (23, "GIULIANI AWARDED MEDAL OF FREEDOM"),
    (24, "\u00c1BREGO GARC\u00cdA LEAVES FOR SPAIN"),
    (25, "SENEGAL AFCON CHAMPIONS REINSTATED"),
    (26, "GUKESH HOLDS SINDAROV IN OPENER"),
    (27, "IRANIAN SINGER GETS 74 LASHES"),
    (28, "SHEIKH HASINA ANNOUNCES RETURN"),
    (29, "MACRON WEIGHS SPENDING CAPS"),
    (30, "NSW $35M DRUG SYNDICATE CHARGED"),
    (31, "LEWIS PUGH SWIMS HORMUZ, 15 KM"),
    (32, "ISRAEL: IRAN BUILDING CHEMICAL WEAPONS"),
    (33, "S. KOREA EDUCATION MINISTER RESIGNS"),
    (34, "AUSTRALIA\u2013SOLOMON SECURITY PACT"),
    (35, "DUTCH COURT: CLIMATE TARGETS BINDING"),
    (36, "RUSSIA ACCUSES UKRAINE OF \"TERRORISM\""),
    (37, "DOW ERASES 1,100-PT PLUNGE, CLOSES +0.33%"),
    (38, "CORE PCE 3.3%: HOTTER THAN EXPECTED"),
    (39, "COP31 ENDS WITHOUT A DEAL"),
    (40, "INDONESIA MINE FLOOD: 9 DEAD, 17 TRAPPED"),
    (41, "RUSSIA PASSES RECORD MILITARY BUDGET"),
    (42, "ESTONIA MAY SHUT RAIL BORDER WITH RUSSIA"),
    (43, "EU PLANS \u20ac50BN TECH FUND"),
    (44, "NVIDIA BOARD PUTS HUANG UNDER SCRUTINY"),
    (45, "ZELENSKY SEEKS TOUGHER US SANCTIONS"),
    (46, "IRGC: 2 TANKERS HIT MINES IN HORMUZ"),
    (47, "BLAST NEAR TANKER OFF DUBAI"),
    (48, "HOUTHIS THREATEN JEDDAH PORTS"),
]

DATE_CHECK = (
    "DATE CHECK \u2014 LEFT OUT: Anthropic $2T IPO (19 Nov) \u00b7 Villavicencio car bomb (23 Nov) \u00b7 "
    "Russian extradition case (5 Nov) \u00b7 Missiles over Poland (20 Nov) \u00b7 Tarwekamp blast (Dec 2024) \u00b7 "
    "Miss Universe in San Juan (24 Nov, local) \u00b7 Nvidia +31.5% on Huang's return (Mon 23) \u00b7 "
    "WHO Ebola evacuation, Akwe (Tue 24). NOT YET: Thanksgiving (Thu 26) \u00b7 Bundestag budget vote (Fri 27)."
)
DATE_INSIDE = (
    "DATED INSIDE: Huawei verdict 24 Nov (reported 25 Nov in Asia) \u00b7 Cartagena siege began 24 Nov 08:30 "
    "(hero = 25 Nov raid) \u00b7 NATO vow 24 Nov (hero = 25 Nov analysis) \u00b7 Odesa strike late Tue 24 Nov "
    "(reported 25 Nov)."
)
FOOTER_GUARANTEE = ("Every story above happened or was first reported on "
                    "Wednesday 25 November 2026.")
FOOTER_SOURCES = ("Sources: Reuters \u00b7 CNN \u00b7 AP \u00b7 NOS \u00b7 Sky News \u00b7 IANS \u00b7 Des Moines Register \u00b7 "
                  "WHO \u00b7 WFP \u00b7 Xinhua \u00b7 USTR \u00b7 EPA \u00b7 Korea JoongAng Daily")
HERO_PLACES = ("1 Washington \u00b7 2 Seoul \u00b7 3 Jiuquan \u00b7 4 Cartagena \u00b7 5 Ras Tanura \u00b7 "
               "6 Middletown, Iowa \u00b7 7 Langley, VA \u00b7 8 Brussels \u00b7 9 UAE")

MAP_DOTS = [
    (1, -77.0, 38.9, True), (2, 127.0, 37.5, True), (3, 99.0, 40.0, True),
    (4, -75.5, 10.4, True), (5, 49.0, 27.0, True), (6, -91.4, 40.8, True),
    (7, -83.0, 42.0, True), (8, 4.4, 50.8, True), (9, 56.0, 23.5, True),
    (10, 29.0, 30.0, False), (11, 30.6, 46.5, False), (12, 34.5, 31.5, False),
    (13, -73.5, 41.2, False), (15, -2.0, 52.5, False), (18, 29.5, 1.5, False),
    (24, -3.7, 40.4, False), (25, -17.4, 14.7, False), (26, 9.0, 44.0, False),
    (27, 53.0, 37.0, False), (28, 90.4, 23.8, False), (30, 151.2, -33.9, False),
    (34, 160.0, -9.5, False), (36, 20.1, 32.1, False), (37, -74.0, 40.7, False),
    (39, 30.7, 36.9, False), (41, 37.6, 55.8, False), (42, 24.7, 59.4, False),
    (43, -122.0, 37.4, False), (45, 30.5, 50.4, False), (48, 39.2, 21.5, False),
]

# ------------------------------------------------------------------ ART
# Every art function draws on its own RGBA panel (w x h) and returns it,
# so nothing can ever cross a panel edge.

def panel(w, h, bg):
    im = Image.new("RGBA", (w, h), bg + (255,))
    return im, ImageDraw.Draw(im)

def art_tariffs(w, h):
    im, d = panel(w, h, (168, 196, 224))
    # sky + sea
    d.rectangle([0, 0, w, int(h * 0.62)], fill=(168, 196, 224, 255))
    d.rectangle([0, int(h * 0.62), w, h], fill=(46, 88, 140, 255))
    d.rectangle([0, int(h * 0.62), w, int(h * 0.62) + 3], fill=(255, 255, 255, 255))
    # sun + clouds
    d.ellipse([w - 58, 8, w - 30, 36], fill=(245, 220, 130, 255))
    d.ellipse([14, 10, 52, 22], fill=(255, 255, 255, 255))
    d.ellipse([34, 6, 66, 18], fill=(255, 255, 255, 255))
    # ship hull
    hy = int(h * 0.62)
    d.polygon([(8, hy - 6), (w - 8, hy - 6), (w - 26, hy + 16), (30, hy + 16)],
              fill=(30, 30, 34, 255))
    d.rectangle([8, hy - 10, w - 8, hy - 5], fill=(176, 58, 46, 255))
    # containers: 3 rows x 8 cols
    cols = [(176, 58, 46), (52, 96, 150), (46, 110, 70), (201, 162, 39),
            (104, 78, 150), (196, 106, 28), (32, 120, 118), (140, 40, 30)]
    cw, ch = 30, 13
    x0, y0 = 16, hy - 52
    for r in range(3):
        for c in range(8):
            x = x0 + c * (cw + 2)
            y = y0 + r * (ch + 2)
            d.rectangle([x, y, x + cw, y + ch], fill=cols[(r * 3 + c) % 8] + (255,))
            d.line([(x + 6, y), (x + 6, y + ch)], fill=(255, 255, 255, 90), width=1)
    # bridge tower + funnel
    d.rectangle([w - 62, 4, w - 34, 21], fill=(245, 245, 240, 255))
    for i in range(3):
        d.rectangle([w - 58, 7 + i * 5, w - 38, 10 + i * 5],
                    fill=(38, 58, 92, 255))
    d.rectangle([w - 96, 8, w - 80, 21], fill=(176, 58, 46, 255))
    # tariff table strip inside the panel (data in the drawing)
    ty = h - 26
    d.rectangle([0, ty, w, h], fill=(253, 251, 243, 255))
    d.line([(0, ty), (w, ty)], fill=NAVY + (255,), width=1)
    f = F(9, bold=True)
    txt = "CHINA 20%  \u00b7  INDIA 25%  \u00b7  EU 15%  \u00b7  VIETNAM 35%"
    d.text(((w - d.textlength(txt, font=f)) / 2, ty + 7), txt, font=f, fill=NAVY)
    # red stamp, top right
    cx, cy, r = w - 52, 52, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(253, 251, 243, 235),
              outline=RED + (255,), width=3)
    d.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5],
              outline=RED + (255,), width=1)
    f1, f2 = F(11, bold=True), F(20, bold=True)
    d.text((cx - d.textlength("UP TO", font=f1) / 2, cy - 20), "UP TO",
           font=f1, fill=RED)
    d.text((cx - d.textlength("35%", font=f2) / 2, cy - 8), "35%",
           font=f2, fill=RED)
    return im

def art_chip(w, h):
    im, d = panel(w, h, (22, 35, 60))
    # grid
    for gx in range(0, w, 26):
        d.line([(gx, 0), (gx, h)], fill=(255, 255, 255, 22), width=1)
    for gy in range(0, h, 20):
        d.line([(0, gy), (w, gy)], fill=(255, 255, 255, 22), width=1)
    # falling red line chart (upper zone only, clear of the number strip)
    pts = [(10, 12), (52, 20), (96, 18), (140, 30), (184, 38), (228, 48),
           (272, 56), (308, 62)]
    d.line(pts, fill=(224, 70, 52, 255), width=4)
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(255, 255, 255, 255))
    d.polygon([(308, 62), (296, 55), (300, 66)], fill=(224, 70, 52, 255))
    # AI chip graphic, bottom left
    cx0, cy0 = 14, 62
    d.rectangle([cx0 + 8, cy0 + 8, cx0 + 44, cy0 + 44], fill=(16, 24, 44, 255),
                outline=(201, 162, 39, 255), width=2)
    for i in range(4):
        d.line([(cx0 + 14 + i * 9, cy0), (cx0 + 14 + i * 9, cy0 + 8)],
               fill=(201, 162, 39, 255), width=2)
        d.line([(cx0 + 14 + i * 9, cy0 + 44), (cx0 + 14 + i * 9, cy0 + 52)],
               fill=(201, 162, 39, 255), width=2)
        d.line([(cx0, cy0 + 14 + i * 9), (cx0 + 8, cy0 + 14 + i * 9)],
               fill=(201, 162, 39, 255), width=2)
        d.line([(cx0 + 44, cy0 + 14 + i * 9), (cx0 + 52, cy0 + 14 + i * 9)],
               fill=(201, 162, 39, 255), width=2)
    f = F(14, bold=True)
    d.text((cx0 + 26 - d.textlength("AI", font=f) / 2, cy0 + 18), "AI",
           font=f, fill=(255, 255, 255))
    # big KOSPI number
    fbig = F(26, bold=True)
    d.text((76, 66), "4,697.51", font=fbig, fill=(255, 255, 255))
    f2 = F(8, bold=True)
    lab = "KOSPI \u22126.2%  \u00b7  SK HYNIX \u221211.1%  \u00b7  SAMSUNG \u22129.9%"
    d.text((76, 102), lab, font=f2, fill=(224, 70, 52))
    return im

def art_space(w, h):
    im, d = panel(w, h, (16, 24, 44))
    # stars
    import random
    rnd = random.Random(25)
    for _ in range(60):
        x, y = rnd.randint(2, w - 2), rnd.randint(2, int(h * 0.7))
        r = rnd.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 200))
    # Earth curve at bottom
    d.ellipse([-w * 0.4, int(h * 0.78), w * 1.4, int(h * 1.9)], fill=(46, 88, 140, 255))
    d.ellipse([-w * 0.4, int(h * 0.78), w * 1.4, int(h * 0.86)],
              fill=(120, 180, 230, 255))
    d.ellipse([int(w * 0.1), int(h * 0.86), int(w * 0.34), int(h * 0.97)],
              fill=(46, 110, 70, 255))
    d.ellipse([int(w * 0.62), int(h * 0.88), int(w * 0.86), int(h * 0.98)],
              fill=(46, 110, 70, 255))
    # dotted trajectory
    for i in range(12):
        t = i / 11.0
        x = int(70 + t * 150)
        y = int(88 - t * 46 + t * t * 18)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255, 220))
    # rocket, big, centre-left, ascending
    rx, ry = 78, 58
    d.polygon([(rx, ry - 26), (rx + 9, ry - 8), (rx + 9, ry + 12), (rx, ry + 20),
               (rx - 9, ry + 12), (rx - 9, ry - 8)], fill=(245, 245, 240, 255))
    d.ellipse([rx - 9, ry - 30, rx + 9, ry - 12], fill=(176, 58, 46, 255))
    d.polygon([(rx - 9, ry + 8), (rx - 20, ry + 22), (rx - 9, ry + 18)],
              fill=(176, 58, 46, 255))
    d.polygon([(rx + 9, ry + 8), (rx + 20, ry + 22), (rx + 9, ry + 18)],
              fill=(176, 58, 46, 255))
    d.polygon([(rx - 5, ry + 18), (rx + 5, ry + 18), (rx + 2, ry + 34),
               (rx - 2, ry + 34)], fill=(245, 160, 40, 255))
    d.ellipse([rx - 12, ry + 32, rx + 12, ry + 46], fill=(245, 200, 90, 160))
    # Tiangong station, large, right
    sx, sy = w - 78, 44
    d.rectangle([sx - 8, sy - 6, sx + 8, sy + 26], fill=(220, 225, 232, 255))
    d.rectangle([sx - 8, sy - 6, sx + 8, sy + 2], fill=(176, 58, 46, 255))
    d.ellipse([sx - 8, sy + 26, sx + 8, sy + 34], fill=(200, 205, 212, 255))
    # solar wings
    for sgn in (-1, 1):
        x0 = sx + sgn * 10 if sgn > 0 else sx - 66
        d.rectangle([x0, sy + 2, x0 + 56, sy + 20], fill=(52, 96, 150, 255),
                    outline=(255, 255, 255, 255), width=1)
        for i in range(1, 4):
            d.line([(x0 + i * 14, sy + 2), (x0 + i * 14, sy + 20)],
                   fill=(255, 255, 255, 160), width=1)
    # flags
    d.rectangle([sx - 40, sy + 40, sx - 16, sy + 54], fill=(20, 110, 60, 255))
    d.ellipse([sx - 37, sy + 42, sx - 29, sy + 50], fill=(255, 255, 255, 255))
    d.ellipse([sx - 34, sy + 44, sx - 28, sy + 50], fill=(20, 110, 60, 255))
    d.rectangle([sx - 12, sy + 40, sx + 12, sy + 54], fill=(176, 58, 46, 255))
    for fx, fy in [(sx - 8, sy + 44), (sx - 2, sy + 42), (sx + 4, sy + 46)]:
        d.ellipse([fx - 1, fy - 1, fx + 1, fy + 1], fill=(245, 220, 130, 255))
    # labels (clear of the number badge top-left and CONFIRMED chip top-right)
    f = F(11, bold=True)
    d.text((36, 8), "SHENZHOU-24", font=f, fill=(255, 255, 255))
    d.text((w - 8 - d.textlength("TIANGONG", font=f), 26), "TIANGONG",
           font=f, fill=(255, 255, 255))
    f2 = F(10, bold=True)
    d.text((10, h - 20), "1ST PAKISTANI ASTRONAUT", font=f2, fill=(255, 255, 255))
    return im

def art_cartagena(w, h):
    im, d = panel(w, h, (240, 230, 205))
    d.rectangle([0, 0, w, 22], fill=(176, 58, 46, 255))
    f = F(12, bold=True)
    t = "\u00c9XITO"
    d.text(((w - d.textlength(t, font=f)) / 2, 4), t, font=f, fill=(255, 255, 255))
    d.rectangle([0, 22, w, 28], fill=(245, 245, 240, 255))
    # shopfront windows + door
    d.rectangle([8, 32, 62, h - 10], fill=(120, 160, 200, 255))
    d.rectangle([70, 32, 112, h - 10], fill=(90, 130, 175, 255))
    d.rectangle([120, 32, w - 8, h - 10], fill=(60, 90, 130, 255))
    d.line([(35, 32), (35, h - 10)], fill=(255, 255, 255, 200), width=2)
    # figures (police) silhouettes
    for fx in (30, 78, 130):
        d.ellipse([fx - 4, 36, fx + 4, 44], fill=(26, 26, 26, 255))
        d.rectangle([fx - 5, 44, fx + 5, h - 12], fill=(26, 26, 26, 255))
    # police tape
    d.polygon([(0, h - 12), (w, h - 16), (w, h - 6), (0, h - 2)],
              fill=(245, 200, 40, 255))
    for i in range(0, w, 14):
        d.line([(i, h - 12), (i + 7, h - 6)], fill=(26, 26, 26, 255), width=2)
    return im

def art_refinery(w, h):
    im, d = panel(w, h, (200, 190, 165))
    d.rectangle([0, int(h * 0.55), w, h], fill=(90, 85, 75, 255))
    # towers
    for tx, tw, th in [(10, 16, 34), (34, 12, 46), (120, 14, 40), (142, 10, 30)]:
        d.rectangle([tx, h - th - 8, tx + tw, h - 8], fill=(70, 68, 64, 255))
        d.rectangle([tx + 2, h - th - 14, tx + tw - 2, h - th - 8],
                    fill=(70, 68, 64, 255))
    # storage tanks
    d.ellipse([58, h - 26, 100, h - 8], fill=(150, 145, 135, 255))
    d.rectangle([58, h - 22, 100, h - 8], fill=(150, 145, 135, 255))
    # flames
    d.ellipse([84, 8, 118, 34], fill=(245, 160, 40, 255))
    d.ellipse([92, 16, 112, 38], fill=(224, 70, 52, 255))
    d.ellipse([96, 24, 108, 40], fill=(245, 220, 90, 255))
    # smoke
    for sx, sy, sr in [(100, 4, 7), (112, 0, 5), (88, 2, 5)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(60, 60, 60, 220))
    # drone silhouette
    d.ellipse([132, 10, 138, 16], fill=(26, 26, 26, 255))
    d.line([(124, 12), (146, 12)], fill=(26, 26, 26, 255), width=2)
    d.line([(128, 8), (128, 18)], fill=(26, 26, 26, 255), width=1)
    d.line([(140, 8), (140, 18)], fill=(26, 26, 26, 255), width=1)
    return im

def art_iowa(w, h):
    im, d = panel(w, h, (168, 196, 224))
    d.rectangle([0, int(h * 0.72), w, h], fill=(90, 130, 70, 255))
    # blast cloud
    d.ellipse([28, 18, 78, 52], fill=(245, 160, 40, 255))
    d.ellipse([58, 8, 108, 44], fill=(245, 200, 90, 255))
    d.ellipse([88, 20, 132, 52], fill=(224, 110, 40, 255))
    d.ellipse([52, 26, 96, 54], fill=(250, 225, 150, 255))
    # plume
    d.polygon([(96, 44), (112, 44), (124, 8), (108, 8)], fill=(150, 150, 148, 220))
    d.ellipse([102, 2, 124, 16], fill=(170, 170, 168, 220))
    # ground debris dots
    for dx, dy in [(20, 56), (140, 58), (60, 60), (120, 52)]:
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(60, 60, 60, 255))
    return im

def art_cyber(w, h):
    im, d = panel(w, h, (200, 205, 215))
    # agency building
    d.polygon([(14, 22), (w // 2, 6), (w - 14, 22)], fill=(120, 125, 135, 255))
    d.rectangle([18, 22, w - 18, h - 8], fill=(150, 155, 165, 255))
    for cx in (30, 56, 82, 108, 134):
        d.rectangle([cx, 26, cx + 8, h - 12], fill=(230, 232, 236, 255))
    d.rectangle([18, h - 12, w - 18, h - 8], fill=(100, 105, 115, 255))
    # breach screen
    d.rectangle([w - 64, 28, w - 8, h - 10], fill=(16, 24, 44, 255),
                outline=(255, 255, 255, 255), width=1)
    f = F(9, bold=True)
    d.text((w - 60, 31), "BREACH", font=f, fill=(224, 70, 52))
    d.text((w - 60, 42), "0101 1100", font=F(7), fill=(120, 220, 120))
    d.text((w - 60, 51), "ACCESS", font=F(7), fill=(120, 220, 120))
    return im

def art_satellite(w, h):
    im, d = panel(w, h, (16, 24, 44))
    import random
    rnd = random.Random(8)
    for _ in range(30):
        x, y = rnd.randint(2, w - 2), rnd.randint(2, int(h * 0.6))
        d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(255, 255, 255, 200))
    # Earth arc
    d.ellipse([-w * 0.3, int(h * 0.8), w * 1.3, int(h * 1.8)], fill=(46, 88, 140, 255))
    d.ellipse([-w * 0.3, int(h * 0.8), w * 1.3, int(h * 0.88)],
              fill=(120, 180, 230, 255))
    # red orbit ellipse
    d.ellipse([8, 6, w - 8, h - 6], outline=(224, 70, 52, 255), width=2)
    # satellite
    sx, sy = w // 2, h // 2 - 8
    d.rectangle([sx - 12, sy - 8, sx + 12, sy + 8], fill=(220, 225, 232, 255))
    d.rectangle([sx - 12, sy - 8, sx + 12, sy - 2], fill=(176, 58, 46, 255))
    d.rectangle([sx - 40, sy - 4, sx - 12, sy + 4], fill=(52, 96, 150, 255))
    d.rectangle([sx + 12, sy - 4, sx + 40, sy + 4], fill=(52, 96, 150, 255))
    d.line([(sx, sy - 8), (sx, sy - 16)], fill=(255, 255, 255, 255), width=2)
    d.ellipse([sx - 2, sy - 19, sx + 2, sy - 15], fill=(245, 220, 90, 255))
    return im

def art_cricket(w, h):
    im, d = panel(w, h, (70, 130, 70))
    d.rectangle([0, 0, w, int(h * 0.3)], fill=(168, 196, 224, 255))
    d.rectangle([0, int(h * 0.3), w, h], fill=(70, 130, 70, 255))
    # crowd dots
    import random
    rnd = random.Random(53)
    for _ in range(26):
        x, y = rnd.randint(4, w - 4), rnd.randint(4, int(h * 0.26))
        c = rnd.choice([(245, 220, 90), (255, 255, 255), (224, 70, 52), (52, 96, 150)])
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=c + (255,))
    # pitch
    d.rectangle([w // 2 - 14, int(h * 0.3), w // 2 + 14, h], fill=(216, 190, 140, 255))
    # stumps
    for sx in (w // 2 - 6, w // 2, w // 2 + 6):
        d.line([(sx, h - 16), (sx, h - 6)], fill=(245, 220, 90, 255), width=2)
    # batsman silhouette
    bx, by = w // 2 - 26, h - 30
    d.ellipse([bx - 4, by - 12, bx + 4, by - 4], fill=(26, 26, 26, 255))
    d.polygon([(bx - 5, by - 4), (bx + 5, by - 4), (bx + 3, by + 12),
               (bx - 3, by + 12)], fill=(26, 26, 26, 255))
    d.line([(bx + 4, by - 2), (bx + 14, by + 8)], fill=(180, 140, 90, 255), width=3)
    # big 204, lower left on the field (clear of the badge top-right)
    f = F(22, bold=True)
    d.text((6, h - 28), "204", font=f, fill=(255, 255, 255))
    return im

def art_tanker(w, h):
    im, d = panel(w, h, (200, 190, 165))
    d.rectangle([0, int(h * 0.62), w, h], fill=(90, 88, 84, 255))
    d.line([(0, int(h * 0.62)), (w, int(h * 0.62))], fill=(255, 255, 255, 255), width=2)
    # overturned tanker
    d.ellipse([30, 26, 120, 52], fill=(200, 200, 195, 255))
    d.rectangle([30, 26, 120, 52], fill=(200, 200, 195, 255))
    d.ellipse([30, 26, 44, 52], fill=(150, 148, 142, 255))
    d.ellipse([58, 50, 68, 60], fill=(26, 26, 26, 255))
    d.ellipse([92, 50, 102, 60], fill=(26, 26, 26, 255))
    # cab
    d.polygon([(120, 30), (140, 30), (146, 50), (120, 50)], fill=(176, 58, 46, 255))
    # flame + smoke
    d.ellipse([58, 6, 96, 30], fill=(245, 160, 40, 255))
    d.ellipse([68, 12, 88, 32], fill=(224, 70, 52, 255))
    d.ellipse([74, 18, 84, 32], fill=(245, 220, 90, 255))
    for sx, sy, sr in [(80, 2, 6), (92, 0, 4)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(60, 60, 60, 220))
    # charred cars
    for cx in (10, 132):
        d.rectangle([cx, h - 14, cx + 18, h - 6], fill=(40, 40, 40, 255))
    return im

def art_odesa(w, h):
    im, d = panel(w, h, (24, 28, 48))
    import random
    rnd = random.Random(44)
    for _ in range(24):
        x, y = rnd.randint(2, w - 2), rnd.randint(2, 16)
        d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(255, 255, 255, 200))
    # skyline
    for bx, bw, bh in [(0, 26, 22), (28, 20, 34), (50, 24, 26), (76, 18, 38),
                       (96, 22, 24), (120, 24, 32), (146, 15, 20)]:
        d.rectangle([bx, h - bh, bx + bw, h], fill=(10, 12, 20, 255))
        for wy in range(h - bh + 4, h - 4, 8):
            d.rectangle([bx + 4, wy, bx + 8, wy + 4], fill=(245, 220, 90, 200))
    # explosion flash
    d.ellipse([58, 12, 96, 40], fill=(245, 160, 40, 255))
    d.ellipse([66, 18, 88, 36], fill=(245, 220, 90, 255))
    d.ellipse([74, 24, 82, 34], fill=(255, 255, 255, 255))
    d.ellipse([70, 2, 86, 14], fill=(60, 60, 60, 220))
    return im

def art_gaza(w, h):
    im, d = panel(w, h, (70, 66, 60))
    # ruined skyline silhouettes
    for bx, bw, bh in [(0, 30, 26), (32, 22, 40), (56, 26, 30), (84, 20, 44),
                       (106, 24, 28), (132, 29, 36)]:
        d.polygon([(bx, h), (bx, h - bh), (bx + bw // 2, h - bh - 8),
                   (bx + bw, h - bh), (bx + bw, h)], fill=(30, 28, 26, 255))
    # smoke columns
    for sx in (44, 96, 140):
        d.ellipse([sx - 6, 4, sx + 6, 18], fill=(150, 148, 144, 200))
        d.ellipse([sx - 4, 14, sx + 4, 26], fill=(130, 128, 124, 200))
    # single lit window (memorial)
    d.rectangle([60, h - 22, 66, h - 14], fill=(245, 220, 90, 255))
    # candle glow
    d.ellipse([118, h - 20, 126, h - 8], fill=(245, 200, 90, 255))
    d.ellipse([121, h - 24, 123, h - 20], fill=(255, 255, 255, 255))
    return im

def art_huawei(w, h):
    im, d = panel(w, h, (200, 205, 215))
    # courthouse
    d.polygon([(16, 26), (w // 2, 8), (w - 16, 26)], fill=(120, 125, 135, 255))
    d.rectangle([20, 26, w - 20, h - 12], fill=(150, 155, 165, 255))
    for cx in (32, 58, 84, 110, 136):
        d.rectangle([cx, 30, cx + 8, h - 16], fill=(230, 232, 236, 255))
    d.rectangle([16, h - 12, w - 16, h - 8], fill=(100, 105, 115, 255))
    # gavel
    d.line([(108, 34), (140, 20)], fill=(120, 80, 40, 255), width=4)
    d.rectangle([132, 12, 150, 24], fill=(90, 60, 30, 255))
    # document
    d.rectangle([20, 36, 54, h - 8], fill=(253, 251, 243, 255),
                outline=(26, 26, 26, 255), width=1)
    for i in range(3):
        d.line([(24, 41 + i * 5), (50, 41 + i * 5)], fill=(26, 26, 26, 255), width=1)
    return im

def art_climate(w, h):
    im, d = panel(w, h, (168, 196, 224))
    # globe
    d.ellipse([6, 4, 54, 52], fill=(46, 88, 140, 255))
    d.ellipse([16, 16, 36, 32], fill=(46, 110, 70, 255))
    d.ellipse([32, 34, 50, 48], fill=(46, 110, 70, 255))
    d.ellipse([38, 10, 48, 20], fill=(46, 110, 70, 255))
    # thermometer
    d.rectangle([100, 4, 112, 40], fill=(255, 255, 255, 255),
                outline=(26, 26, 26, 255), width=2)
    d.rectangle([103, 12, 109, 40], fill=(224, 70, 52, 255))
    d.ellipse([95, 36, 117, 58], fill=(224, 70, 52, 255),
              outline=(26, 26, 26, 255), width=2)
    # sun rays
    for ang in range(0, 360, 45):
        import math
        x1 = 140 + int(10 * math.cos(math.radians(ang)))
        y1 = 20 + int(10 * math.sin(math.radians(ang)))
        x2 = 140 + int(16 * math.cos(math.radians(ang)))
        y2 = 20 + int(16 * math.sin(math.radians(ang)))
        d.line([(x1, y1), (x2, y2)], fill=(245, 160, 40, 255), width=2)
    d.ellipse([132, 12, 148, 28], fill=(245, 200, 90, 255))
    # 2C label
    f = F(12, bold=True)
    d.text((122, 44), "+2\u00b0C", font=f, fill=RED)
    return im

def art_heat(w, h):
    im, d = panel(w, h, (245, 220, 150))
    # blazing sun
    import math
    for ang in range(0, 360, 30):
        x1 = 40 + int(20 * math.cos(math.radians(ang)))
        y1 = 26 + int(20 * math.sin(math.radians(ang)))
        x2 = 40 + int(28 * math.cos(math.radians(ang)))
        y2 = 26 + int(28 * math.sin(math.radians(ang)))
        d.line([(x1, y1), (x2, y2)], fill=(224, 110, 40, 255), width=3)
    d.ellipse([24, 10, 56, 42], fill=(245, 160, 40, 255))
    d.ellipse([30, 16, 50, 36], fill=(245, 220, 90, 255))
    # city skyline
    for bx, bw, bh in [(70, 22, 24), (94, 18, 34), (114, 24, 20), (140, 17, 28)]:
        d.rectangle([bx, h - bh, bx + bw, h], fill=(90, 70, 60, 255))
        for wy in range(h - bh + 4, h - 4, 8):
            d.rectangle([bx + 4, wy, bx + 8, wy + 4], fill=(245, 220, 90, 200))
    # heat haze
    for i in range(3):
        y = 48 + i * 6
        d.arc([70, y, 150, y + 8], 200, 340, fill=(224, 110, 40, 200), width=2)
    return im

ART = {"tariffs": art_tariffs, "chip": art_chip, "space": art_space,
       "cartagena": art_cartagena, "refinery": art_refinery, "iowa": art_iowa,
       "cyber": art_cyber, "satellite": art_satellite, "cricket": art_cricket,
       "tanker": art_tanker, "odesa": art_odesa, "gaza": art_gaza,
       "huawei": art_huawei, "climate": art_climate, "heat": art_heat}

# simplified continents (lon/lat polygons, stylised)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 75),
     (-75, 72), (-60, 62), (-55, 52), (-65, 45), (-75, 38), (-80, 32),
     (-85, 28), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, -5), (-40, -10),
     (-35, -15), (-40, -25), (-50, -30), (-60, -35), (-65, -45), (-70, -52),
     (-75, -40), (-75, -25), (-80, -15), (-80, -5)],
    [(-10, 36), (-5, 44), (0, 48), (5, 53), (10, 58), (15, 60), (20, 65),
     (25, 70), (30, 68), (35, 60), (40, 55), (35, 50), (30, 45), (25, 40),
     (20, 38), (15, 36), (10, 38), (5, 36), (0, 36)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 10), (51, 5), (48, -5), (40, -10), (35, -20), (30, -28),
     (25, -33), (18, -35), (12, -25), (10, -15), (8, -5), (0, 5), (-8, 5),
     (-15, 10)],
    [(40, 55), (50, 60), (60, 65), (70, 70), (80, 73), (90, 75), (100, 76),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 65),
     (170, 66), (175, 62), (165, 60), (160, 55), (155, 50), (145, 45),
     (140, 40), (135, 35), (130, 30), (125, 28), (120, 25), (115, 20),
     (110, 15), (105, 10), (100, 8), (95, 10), (90, 15), (85, 20), (80, 15),
     (75, 10), (70, 15), (65, 20), (60, 25), (55, 25), (50, 28), (48, 30),
     (45, 35), (40, 40), (40, 50)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
     (153, -28), (150, -22), (145, -15), (140, -12), (135, -12), (130, -13),
     (125, -15), (120, -20), (114, -22)],
]

# ------------------------------------------------------------------ LAYOUT
MX = 14
CW = W - 2 * MX  # 996

def fit_font(text, size, bold=False, serif=False, italic=False, max_w=996):
    s = size
    while s > 6:
        f = F(s, bold=bold, serif=serif, italic=italic)
        if ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return F(6, bold=bold, serif=serif, italic=italic)

def draw_topbar(d, y):
    d.rectangle([MX, y, MX + CW, y + 18], fill=NAVY)
    f = fit_font(TOPBAR, 11, bold=True, max_w=CW - 16)
    d.text(((W - d.textlength(TOPBAR, font=f)) / 2, y + 3), TOPBAR, font=f,
           fill=(246, 240, 224))
    return y + 18

def draw_masthead(d, y):
    f = fit_font(MASTHEAD, 54, bold=True, serif=True, max_w=CW)
    d.text(((W - d.textlength(MASTHEAD, font=f)) / 2, y), MASTHEAD, font=f, fill=NAVY)
    return y + 56

def draw_subhead(d, y):
    f = fit_font(SUBHEAD, 15, serif=True, italic=True, max_w=CW)
    d.text(((W - d.textlength(SUBHEAD, font=f)) / 2, y), SUBHEAD, font=f, fill=RED)
    return y + 18

def draw_chips(d, y):
    labels = [("N. AMERICA", 8), ("LATIN AM.", 2), ("EUROPE", 12),
              ("MIDDLE EAST", 10), ("N. AFRICA", 1), ("SUB-SAH. AFRICA", 2),
              ("SOUTH ASIA", 3), ("EAST & SE ASIA", 5), ("OCEANIA", 2),
              ("GLOBAL", 3)]
    colors = [c for _, _, c in REGIONS]
    gap, ch = 3, 22
    cw = (CW - gap * 9) / 10
    for i, ((name, n), col) in enumerate(zip(labels, colors)):
        x = MX + i * (cw + gap)
        txt = "%s %d" % (name, n)
        f = F(9, bold=True)
        while d.textlength(txt, font=f) > cw - 6 and f.size > 7:
            f = F(f.size - 1, bold=True)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=3, fill=col)
        d.text((x + (cw - d.textlength(txt, font=f)) / 2, y + (ch - f.size) / 2 - 1),
               txt, font=f, fill=(255, 255, 255))
    return y + ch

def draw_fields(d, y):
    parts = ["%s %d" % (n, c) for n, c in FIELDS]
    txt = "17 FIELDS \u00b7 " + " \u00b7 ".join(parts)
    f = fit_font(txt, 10, max_w=CW)
    d.text((MX, y + 2), "17 FIELDS", font=F(10, bold=True), fill=RED)
    rest = txt[len("17 FIELDS "):]
    d.text((MX + d.textlength("17 FIELDS ", font=F(10, bold=True)), y + 2),
           rest, font=f, fill=INK)
    return y + 16

def draw_numbers(d, y):
    cw = CW / 6
    fnum = F(24, bold=True)
    flab = F(8, bold=True)
    for i, (num, lab) in enumerate(NUMBERS):
        x = MX + i * cw
        if i:
            d.line([(x - 3, y + 4), (x - 3, y + 46)], fill=TAN_D, width=1)
        d.text((x + (cw - d.textlength(num, font=fnum)) / 2, y + 2), num,
               font=fnum, fill=RED)
        d.text((x + (cw - d.textlength(lab, font=flab)) / 2, y + 32), lab,
               font=flab, fill=NAVY)
    rule(d, MX, y + 50, CW, NAVY, 1)
    return y + 50

def draw_utc(d, y):
    d.rectangle([MX, y, MX + CW, y + 36], fill=PAPER, outline=NAVY, width=1)
    d.text((MX + 8, y + 12), "THE DAY IN UTC", font=F(9, bold=True), fill=NAVY)
    x0 = MX + 96
    for li, items in enumerate((UTC_A, UTC_B)):
        yy = y + 4 + li * 15
        x = x0
        for ti, (tm, ev) in enumerate(items):
            ft, fe = F(10, bold=True), F(10)
            if ti:
                d.text((x, yy), "\u00b7", font=fe, fill=GREY)
                x += d.textlength("\u00b7  ", font=fe)
            d.text((x, yy), tm, font=ft, fill=RED)
            x += d.textlength(tm + " ", font=ft)
            d.text((x, yy), ev, font=fe, fill=INK)
            x += d.textlength(ev + "  ", font=fe)
    return y + 36

def draw_hero(d, img, x, y, w, h, hero):
    art = ART[hero["art"]](w, 118)
    img.paste(art, (x, y), art)
    num_badge(d, x + 14, y + 14, 13, hero["num"])
    st = hero["status"]
    sbg = GREEN if st == "CONFIRMED" else RED
    fchip = F(9, bold=True)
    sw = d.textlength(st, font=fchip) + 14
    d.rounded_rectangle([x + w - sw - 4, y + 4, x + w - 4, y + 22], radius=3, fill=sbg)
    d.text((x + w - sw - 4 + 7, y + 7), st, font=fchip, fill=(255, 255, 255))
    yy = y + 122
    d.text((x, yy), hero["place"], font=F(10, bold=True), fill=NAVY)
    yy += 14
    lines = wrap(d, hero["head"], F(15, bold=True), w)[:2]
    yy = draw_lines(d, x, yy, lines, F(15, bold=True), INK, 17)
    yy += 3
    blines = wrap(d, hero["body"], F(10, italic=False), w)[:3]
    yy = draw_lines(d, x, yy, blines, F(10), INK, 13)
    yy += 3
    d.text((x, yy), "WHY IT MATTERS", font=F(9, bold=True), fill=RED)
    yy += 12
    wlines = wrap(d, hero["why"], F(10, italic=True), w)[:2]
    yy = draw_lines(d, x, yy, wlines, F(10, italic=True), INK, 12)
    yy += 2
    d.text((x, yy), hero["src"], font=F(8), fill=GREY)
    return y + h

def draw_medium(d, img, x, y, w, h, m):
    art = ART[m["art"]](w, 62)
    img.paste(art, (x, y), art)
    num_badge(d, x + 11, y + 11, 10, m["num"])
    fb = F(8, bold=True)
    bw = d.textlength(m["badge"], font=fb) + 10
    d.rounded_rectangle([x + w - bw - 3, y + 3, x + w - 3, y + 18], radius=3, fill=RED)
    d.text((x + w - bw - 3 + 5, y + 5), m["badge"], font=fb, fill=(255, 255, 255))
    yy = y + 65
    d.text((x, yy), m["place"], font=F(8, bold=True), fill=NAVY)
    yy += 11
    lines = wrap(d, m["head"], F(10, bold=True), w)[:2]
    yy = draw_lines(d, x, yy, lines, F(10, bold=True), INK, 12)
    blines = wrap(d, m["body"], F(9), w)[:3]
    yy = draw_lines(d, x, yy, blines, F(9), INK, 11)
    yy += 1
    d.text((x, yy), m["src"], font=F(8), fill=GREY)
    return y + h

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 205, 255),
                outline=NAVY, width=1)
    # graticule
    for gx in range(0, w + 1, 30):
        d.line([(x + gx, y), (x + gx, y + h)], fill=(255, 255, 255, 90), width=1)
    for gy in range(0, h + 1, 24):
        d.line([(x, y + gy), (x + w, y + gy)], fill=(255, 255, 255, 90), width=1)
    def proj(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (85 - lat) / 145.0 * h)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=TAN, outline=(120, 105, 70))
    for num, lon, lat, hero in MAP_DOTS:
        cx, cy = proj(lon, lat)
        r = 5 if hero else 4
        fill = RED if hero else NAVY
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
                  outline=(255, 255, 255), width=1)
        f = F(6, bold=True)
        t = str(num)
        d.text((cx - d.textlength(t, font=f) / 2, cy - f.size / 2 - 1), t,
               font=f, fill=(255, 255, 255))

def draw_bottom(d, y, h):
    # map block, left
    mw = 300
    d.text((MX, y), "WHERE IT HAPPENED", font=F(10, bold=True), fill=NAVY)
    d.text((MX + mw - d.textlength("30 NUMBERED PLACES", font=F(8, bold=True)),
            y + 1), "30 NUMBERED PLACES", font=F(8, bold=True), fill=GREY)
    draw_map(d, MX, y + 14, mw, 118)
    ly = y + 136
    leg1 = [("N. AMERICA", NAVY), ("LATIN AM.", TEAL), ("EUROPE", BLUE),
            ("MIDDLE EAST", RED)]
    leg2 = [("N. AFRICA", OCHRE), ("SUB-SAH. AFRICA", GREEN), ("SOUTH ASIA", ORANGE),
            ("EAST & SE ASIA", PURPLE), ("OCEANIA", (28, 96, 110)), ("GLOBAL", (110, 110, 110))]
    fl = F(8)
    xx = MX
    for name, col in leg1:
        d.rectangle([xx, ly + 1, xx + 7, ly + 8], fill=col)
        d.text((xx + 9, ly), name, font=fl, fill=INK)
        xx += 9 + d.textlength(name, font=fl) + 8
    ly += 10
    xx = MX
    for name, col in leg2:
        d.rectangle([xx, ly + 1, xx + 7, ly + 8], fill=col)
        d.text((xx + 9, ly), name, font=fl, fill=INK)
        xx += 9 + d.textlength(name, font=fl) + 8
    ly += 10
    d.text((MX, ly), HERO_PLACES, font=F(7), fill=GREY)
    # ALSO list, right
    ax = MX + mw + 10
    aw = W - MX - ax
    d.text((ax, y), "ALSO ON 25 NOVEMBER \u2014 33 MORE STORIES",
           font=F(10, bold=True), fill=NAVY)
    colw = (aw - 8) / 2
    fnum = F(9, bold=True)
    fitem = F(9)
    per = 17
    for i, (num, head) in enumerate(ALSO):
        col = 0 if i < per else 1
        row = i if i < per else i - per
        ix = ax + col * (colw + 8)
        iy = y + 15 + row * 8
        d.text((ix, iy), str(num), font=fnum, fill=RED)
        d.text((ix + 16, iy), head, font=fitem, fill=INK)
    return y + h

def draw_datecheck(d, y, h):
    d.rectangle([MX, y, MX + CW, y + h], fill=PAPER, outline=RED, width=1)
    f = F(8)
    l1 = wrap(d, DATE_CHECK, f, CW - 12)
    l2 = wrap(d, DATE_INSIDE, f, CW - 12)
    yy = y + 3
    for ln in (l1 + l2)[:3]:
        d.text((MX + 6, yy), ln, font=f, fill=INK)
        yy += 11
    return y + h

def draw_footer(d, y):
    f1 = F(9, bold=True)
    d.text(((W - d.textlength(FOOTER_GUARANTEE, font=f1)) / 2, y),
           FOOTER_GUARANTEE, font=f1, fill=NAVY)
    f2 = F(8)
    d.text(((W - d.textlength(FOOTER_SOURCES, font=f2)) / 2, y + 11),
           FOOTER_SOURCES, font=f2, fill=GREY)
    return y + 22

def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=NAVY, width=2)
    y = 8
    y = draw_topbar(d, y) + 2
    y = draw_masthead(d, y) + 2
    y = draw_subhead(d, y) + 2
    y = draw_chips(d, y) + 2
    y = draw_fields(d, y) + 2
    y = draw_numbers(d, y) + 2
    y = draw_utc(d, y) + 2
    # heroes
    hw = int((CW - 18) / 3)
    for i, hero in enumerate(BIG):
        draw_hero(d, img, MX + i * (hw + 9), y, hw, 258, hero)
    y += 258 + 2
    # mediums: 2 rows x 6
    mw = int((CW - 30) / 6)
    for r in range(2):
        for c in range(6):
            m = MED[r * 6 + c]
            draw_medium(d, img, MX + c * (mw + 6), y, mw, 148, m)
        y += 148 + 2
    y = draw_bottom(d, y, 164) + 2
    y = draw_datecheck(d, y, 34) + 2
    y = draw_footer(d, y)
    print("final y =", y, "of", H)
    assert y <= H, "OVERFLOW by %d px" % (y - H)
    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    build()
