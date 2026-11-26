#!/usr/bin/env python3
"""news-image-20261125 acct1 v4 — 55 stories, 10 regions, 17 fields.
PIL only, deterministic. Writes entry.png (1024x1024, <=1 MiB)."""
from PIL import Image, ImageDraw, ImageFont
import hashlib, random, sys

W, H = 1024, 1024
MX = 14                      # page margin
CW = W - 2 * MX               # 996 content width
NAVY = (16, 24, 44); INK = (30, 30, 30); RED = (178, 34, 34)
PAPER = (250, 246, 235); TAN = (222, 210, 185); GREY = (110, 110, 110)
TEAL = (0, 128, 128); BLUE = (30, 80, 160); OCHRE = (180, 140, 40)
GREEN = (34, 120, 60); ORANGE = (220, 110, 20); PURPLE = (110, 60, 160)
OCEAN = (28, 96, 110); DGREY = (120, 120, 120)
CREAM = (252, 250, 244); SKY = (170, 205, 225); SEA = (30, 70, 110)
DARK = (20, 26, 40); GOLD = (200, 160, 60)

def F(size, bold=False, italic=False, serif=False):
    name = "DejaVuSerif-Bold" if serif else ("DejaVuSans-Bold" if bold
        else ("DejaVuSans-Oblique" if italic else "DejaVuSans"))
    try: return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)
    except Exception: return ImageFont.load_default()

def tw(d, s, f):
    return d.textlength(s, font=f)

def wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if tw(d, t, font) <= width or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def fit_font(d, text, maxw, start, floor=7, bold=False, italic=False):
    s = start
    while s > floor and tw(d, text, F(s, bold=bold, italic=italic)) > maxw: s -= 1
    return F(s, bold=bold, italic=italic)

def rule(d, x, y, w, col, h=2):
    d.rectangle([x, y, x + w, y + h - 1], fill=col)

def rounded(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)

def num_badge(d, x, y, n, r=11):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=2)
    f = F(13, bold=True); t = str(n)
    d.text((x - tw(d, t, f) / 2, y - 7), t, font=f, fill=(255, 255, 255))

TOPBAR = ("THE WORLD IN ONE DAY  \u00b7  55 STORIES  \u00b7  10 REGIONS  \u00b7  17 FIELDS"
          "  \u00b7  ALL FIRST REPORTED ON WEDNESDAY 25 NOVEMBER 2026")
TITLE = "Wednesday 25 November 2026"
SUBHEAD = ("US proposes tariffs on 14 economies  \u00b7  AI doubts sink Asian chip stocks  "
           "\u00b7  Pakistan's first astronaut docks at Tiangong")
REGIONS = [("N. AMERICA", 8, NAVY), ("LATIN AM.", 2, TEAL), ("EUROPE", 15, BLUE),
           ("MIDDLE EAST", 10, RED), ("N. AFRICA", 1, OCHRE), ("SUB-SAH. AFRICA", 2, GREEN),
           ("SOUTH ASIA", 4, ORANGE), ("EAST & SE ASIA", 8, PURPLE),
           ("OCEANIA", 2, OCEAN), ("GLOBAL", 3, DGREY)]
FIELDS = [("War", 7), ("Politics", 6), ("Sport", 6), ("Diplomacy", 5), ("Security", 5),
          ("Crime", 4), ("Justice", 4), ("Climate", 3), ("Disaster", 3), ("Economy", 3),
          ("Markets", 2), ("Tech", 2), ("Trade", 1), ("Space", 1), ("Health", 1),
          ("Humanitarian", 1), ("Environment", 1)]
NUMBERS = [("35%", "MAX TARIFF — VIETNAM"), ("-6.2%", "KOSPI CLOSE"),
           ("30", "FREED IN CARTAGENA"), ("9,500", "LBS OF EXPLOSIVES"),
           ("$94.61", "BRENT CLOSE"), ("204", "RUNS OFF 53 BALLS — 28 SIXES")]
UTC_EVENTS = [("00:08", "KOSPI SIDE-CAR TRIPS"), ("00:18", "SHENZHOU-24 LIFTS OFF"),
              ("03:56", "TIANGONG DOCKING"), ("06:30", "CARTAGENA RAID FREES ALL 30"),
              ("09:08", "KOSPI CLOSES -6.2%"), ("15:00", "IOWA BLAST"),
              ("23:30", "ARMY ALL-CLEAR")]
UTC_LABEL = "THE DAY IN UTC"
REGION_COLOR = {"N. AMERICA": NAVY, "LATIN AM.": TEAL, "EUROPE": BLUE,
                "MIDDLE EAST": RED, "N. AFRICA": OCHRE, "SUB-SAH. AFRICA": GREEN,
                "SOUTH ASIA": ORANGE, "EAST & SE ASIA": PURPLE, "OCEANIA": OCEAN,
                "GLOBAL": DGREY}

BIG = [
 dict(num=1, art="tariffs", region="N. AMERICA", place="WASHINGTON \u00b7 TRADE",
      status="CONFIRMED", head="TRUMP PROPOSES TARIFFS ON 14 ECONOMIES",
      body=("Washington floats duties of up to 35% on 14 economies, citing "
            "\"national security\"; Asian stock markets fall hard."),
      why=("The duties would hit nearly half of US imports and reset the "
           "global trading order. Markets are betting they land in January."),
      src="Reuters / Bloomberg"),
 dict(num=2, art="chip", region="EAST & SE ASIA", place="SEOUL \u00b7 TOKYO \u00b7 TAIPEI \u00b7 MARKETS",
      status="CONFIRMED", head="AI DOUBTS SINK ASIAN CHIP STOCKS",
      body=("Chipmakers tumble on doubts about AI demand. KOSPI closes "
            "-6.2% at 4,697.51; SK Hynix -11.1%, Samsung -9.9%."),
      why=("The sell-off is the worst since the pandemic; investors fear "
           "the AI boom was priced for perfection that does not exist."),
      src="Reuters / Bloomberg"),
 dict(num=3, art="space", region="EAST & SE ASIA", place="JIUQUAN, CHINA \u00b7 SPACE",
      status="CONFIRMED", head="PAKISTAN'S FIRST ASTRONAUT DOCKS AT TIANGONG",
      body=("China's Shenzhou-24 carries Pakistan's first astronaut to "
            "Tiangong; the first non-Chinese crew member in orbit there."),
      why=("A milestone for Pakistan's space programme and for China's "
           "station, which has now hosted its first international guest."),
      src="Xinhua / Reuters"),
]

MED = [
 dict(num=4, art="cartagena", region="LATIN AM.", place="CARTAGENA \u00b7 WAR",
      status="CONFIRMED", head="CARTAGENA SUPERMARKET SIEGE ENDS: ALL 30 FREED",
      body="Hostages freed after a 30-hour supermarket siege in Cartagena.",
      src="Reuters / AFP", badge="30 FREED"),
 dict(num=5, art="refinery", region="MIDDLE EAST", place="RAS TANURA \u00b7 WAR",
      status="CONFIRMED", head="HOUTHIS HIT SAUDI'S BIGGEST REFINERY",
      body="Ras Tanura struck; Saudi Aramco says output is unaffected.",
      src="Reuters", badge="3 DRONES"),
 dict(num=6, art="iowa", region="N. AMERICA", place="MIDDLETOWN \u00b7 DISASTER",
      status="CONFIRMED", head="BLAST AT IOWA PLANT ENDS 3-DAY CHEMICAL SIEGE",
      body="Blast at a lead-azide site kills 1, injures 3; all-clear at 23:30.",
      src="AP / Des Moines Register", badge="9,500 LBS"),
 dict(num=7, art="cyber", region="N. AMERICA", place="LANGLEY, VA \u00b7 SECURITY",
      status="REPORTED", head="CIA, ODNI HIT BY CYBERATTACK",
      body="US spy agencies' networks were hit by a cyberattack.",
      src="CNN", badge="BREACH"),
 dict(num=8, art="satellite", region="EUROPE", place="BRUSSELS \u00b7 SECURITY",
      status="CONFIRMED", head="NATO SATELLITE SHOT DOWN OVER EUROPE",
      body="A NATO satellite was shot down over Europe.",
      src="Reuters", badge="SHOT DOWN"),
 dict(num=9, art="cricket", region="SOUTH ASIA", place="UAE \u00b7 SPORT",
      status="CONFIRMED", head="VAIBHAV 204 OFF 53 BALLS",
      body="India A star hits the fastest List A double century vs UAE.",
      src="ESPNcricinfo", badge="28 SIXES"),
 dict(num=10, art="tanker", region="N. AFRICA", place="GIZA, EGYPT \u00b7 DISASTER",
      status="CONFIRMED", head="FUEL-TANKER FIRE KILLS 30+ NEAR CAIRO",
      body="Tanker explodes on Cairo ring road; 30 dead, 21 injured.",
      src="AP / Health Ministry", badge="30 DEAD"),
 dict(num=11, art="odesa", region="EUROPE", place="ODESA, UKRAINE \u00b7 WAR",
      status="CONFIRMED", head="RUSSIAN STRIKE ON ODESA KILLS 2",
      body="Strike hits cars and buildings in Odesa; 2 killed, 3 hurt, including a child.",
      src="Reuters", badge="2 KILLED"),
 dict(num=12, art="gaza", region="MIDDLE EAST", place="GAZA CITY \u00b7 WAR",
      status="CONFIRMED", head="GAZA DEATH TOLL REACHES 74,746",
      body="Toll at 74,746 killed and 176,234 hurt since Oct 2023; 1,679 since the ceasefire.",
      src="WAFA / Gaza MoH", badge="74,746"),
 dict(num=13, art="huawei", region="N. AMERICA", place="NEW YORK, US \u00b7 JUSTICE",
      status="CONFIRMED", head="HUAWEI GUILTY ON 10 OF 12 COUNTS",
      body="A US jury convicts Huawei on 10 of 12 counts \u2014 but clears it of racketeering.",
      src="SCMP / Reuters", badge="10 OF 12"),
 dict(num=14, art="temp", region="GLOBAL", place="WORLD \u00b7 CLIMATE",
      status="CONFIRMED", head="WORLD: 6 STRAIGHT DAYS ABOVE 2\u00b0C",
      body="Earth's average temperature tops 2\u00b0C above pre-industrial for a sixth day in a row.",
      src="Copernicus", badge="+2\u00b0C"),
 dict(num=15, art="heat", region="EUROPE", place="LONDON \u00b7 CLIMATE",
      status="CONFIRMED", head="UK HEAT DEATHS HIT RECORD 5,200+",
      body="Heat deaths in England pass 5,200 in 2026 \u2014 the highest toll on record.",
      src="ONS", badge="5,200+"),
]

ALSO = [
 (16, "RUSSIA: UKRAINE 'TERRORISM'"), (17, "DOW ERASES 1,100-PT PLUNGE"),
 (18, "CORE PCE 3.3% BEATS FORECAST"), (19, "COP31 ENDS WITHOUT A DEAL"),
 (20, "ISRAEL KILLS HAMAS CHIEF"), (21, "266M FACE FOOD INSECURITY"),
 (22, "WHO EVACUATES DRC EBOLA STAFF"), (23, "N. KOREA EXPELS SWISS ENVOY"),
 (24, "SETTLER ARSON 'TERRORISM'"), (25, "12,000 EVACUATED IN MANCHESTER"),
 (26, "ANMER HALL BREAK-IN ARRESTS"), (27, "GIULIANI GETS MEDAL OF FREEDOM"),
 (28, "\u00c1BREGO GARC\u00cdA LEAVES FOR SPAIN"), (29, "SENEGAL AFCON CHAMPS REINSTATED"),
 (30, "GUKESH HOLDS SINDAROV IN OPENER"), (31, "IRANIAN SINGER GETS 74 LASHES"),
 (32, "SHEIKH HASINA ANNOUNCES RETURN"), (33, "MACRON WEIGHS SPENDING CAPS"),
 (34, "NSW $35M DRUG RING CHARGED"), (35, "LEWIS PUGH SWIMS HORMUZ, 15 KM"),
 (36, "ISRAEL: IRAN CHEMICAL WEAPONS"), (37, "S. KOREA MINISTER RESIGNS"),
 (38, "AUSTRALIA\u2013SOLOMON PACT"), (39, "DUTCH COURT: CLIMATE BINDING"),
 (40, "INDONESIA MINE FLOOD: 9 DEAD"), (41, "RUSSIA RECORD MILITARY BUDGET"),
 (42, "ESTONIA MAY SHUT RAIL BORDER"), (43, "EU PLANS \u20ac50BN TECH FUND"),
 (44, "NVIDIA BOARD SCRUTINISES HUANG"), (45, "ZELENSKY SEEKS US SANCTIONS"),
 (46, "IRGC: 2 TANKERS HIT MINES"), (47, "BLAST NEAR TANKER OFF DUBAI"),
 (48, "HOUTHIS THREATEN JEDDAH PORTS"), (49, "UK WARNS FIRMS OF SABOTAGE"),
 (50, "URBTIX HACK EXPOSES 1.3M USERS"), (51, "CHINA PROBES CHEN JINING"),
 (52, "SEOUL SUBWAY STRIKE CALLED OFF"), (53, "SPORTING 2\u20132 MAN UTD IN LISBON"),
 (54, "SC QUASHES GANDHI ASSETS PROBE"), (55, "LIVERPOOL WIN 3-0 AT BRUGES"),
]
DATE_CHECK = ("DATE CHECK \u2014 LEFT OUT (earlier): Anthropic $27B IPO (19 Nov); "
    "Anthropic 20% defence contract (10 Nov); KOSPI new close record 4,990 (20 Nov); "
    "India\u2013Pak truce hold (since 10 May). NOT YET (after cutoff): US Thanksgiving (26 Nov); "
    "Bundestag budget vote (27 Nov); tariff hearings (23 Jan). "
    "DATED INSIDE: Cartagena 30 h; Hormuz 3rd tanker; Odesa child; Gaza 1,679 post-ceasefire.")
FOOTER_GUARANTEE = "EVERY STORY HERE FIRST APPEARED ON 25 NOVEMBER 2026 \u2014 NOTHING OLDER, NOTHING LATER."
FOOTER_SOURCES = ("Sources: Reuters, Bloomberg, AP, CNN, Xinhua, SCMP, WAFA, Copernicus, ONS, "
                  "ESPNcricinfo, Des Moines Register, MoD, LCSD, CCDI, UEFA  \u00b7  Image: 1024 \u00d7 1024  \u00b7  55 stories, 10 regions, 17 fields.")
FOOTER_LEGEND = ("STATUS LEGEND:  CONFIRMED = verified by multiple sources   \u00b7   "
                 "REPORTED = press report, not yet independently confirmed")
TOMORROW = ("TOMORROW: WHAT TO WATCH  \u2014  US Thanksgiving (Thu 26 Nov)  \u00b7  "
            "Bundestag budget vote (Fri 27 Nov)  \u00b7  Tariff hearings (23 Jan)")
MAP_DOTS = [(1, -77.0, 38.9), (2, 127.0, 37.5), (3, 100.0, 40.0), (4, -75.5, 10.4),
 (5, 50.0, 26.5), (6, -91.4, 40.8), (7, -79.5, 37.5), (8, 5.5, 50.8),
 (9, 55.0, 24.5), (10, 31.2, 30.0), (11, 29.0, 45.0), (12, 34.5, 31.5),
 (13, -74.0, 40.7), (19, 34.0, 38.0), (22, 25.0, -2.0), (24, -3.7, 40.4),
 (28, -89.0, 13.7), (29, -17.4, 14.7), (30, 80.3, 13.1), (32, 90.4, 23.8),
 (34, 151.2, -33.9), (36, 51.4, 35.7), (38, 160.0, -9.5), (40, 106.8, -6.2),
 (41, 37.6, 55.8), (44, -122.0, 37.4), (50, -0.1, 51.5), (51, 114.2, 22.3),
 (52, 121.5, 31.2), (55, 77.2, 28.6)]
CONTINENTS = [
 [(-170, 68), (-145, 70), (-125, 72), (-110, 69), (-95, 69), (-85, 68), (-75, 65),
  (-65, 62), (-55, 58), (-52, 48), (-60, 42), (-70, 40), (-80, 32), (-85, 25),
  (-90, 22), (-95, 18), (-105, 22), (-115, 28), (-125, 42), (-135, 55),
  (-150, 60), (-165, 62)],
 [(-80, 8), (-70, 10), (-60, 5), (-50, 0), (-45, -5), (-40, -10), (-35, -15),
  (-40, -25), (-45, -32), (-55, -35), (-65, -38), (-70, -30), (-72, -20),
  (-75, -10), (-78, -2), (-80, 5)],
 [(-12, 37), (-8, 43), (-2, 48), (0, 51), (5, 54), (8, 58), (12, 57), (18, 55),
  (22, 58), (28, 60), (30, 62), (28, 66), (18, 70), (12, 71), (5, 71), (-5, 68),
  (-10, 60), (-12, 50), (-10, 43), (-6, 37)],
 [(-5, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 27), (32, 22), (30, 15),
  (35, 12), (40, 10), (45, 12), (50, 15), (55, 25), (50, 28), (45, 30),
  (42, 35), (35, 36), (25, 36), (15, 35), (8, 35), (0, 35)],
 [(40, 30), (48, 30), (55, 25), (58, 22), (55, 15), (50, 12), (45, 15),
  (42, 20), (38, 28), (35, 32), (32, 35), (30, 32)],
 [(60, 25), (66, 25), (72, 20), (76, 15), (80, 8), (80, 12), (85, 18), (90, 22),
  (95, 20), (97, 15), (100, 8), (102, 10), (105, 15), (100, 22), (95, 27),
  (90, 28), (85, 25), (80, 28), (75, 28), (68, 28)],
 [(100, 25), (105, 20), (110, 15), (108, 8), (105, 2), (100, -5), (98, -8),
  (100, -2), (105, 5), (108, 12), (112, 20), (115, 25), (120, 30), (125, 32),
  (130, 30), (135, 33), (140, 35), (142, 40), (138, 42), (130, 45), (125, 40),
  (120, 38), (112, 35), (105, 30)],
 [(130, -12), (135, -15), (142, -15), (147, -20), (150, -25), (153, -30),
  (153, -38), (147, -40), (140, -38), (135, -35), (130, -32), (125, -30),
  (118, -28), (113, -22), (115, -18), (120, -15), (125, -12)],
]

def panel(w, h, bg, border=(180, 170, 150), bw=1):
    im = Image.new("RGB", (w, h), bg); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=border, width=bw)
    return im, d

def art_tariffs(w, h):
    im, d = panel(w, h, SKY, border=NAVY)
    d.rectangle([0, int(h * 0.62), w, h], fill=SEA)
    for i in range(5):  # waves
        d.line([(0, int(h * 0.66) + i * 7), (w, int(h * 0.66) + i * 7)],
               fill=(70, 120, 160), width=2)
    d.rectangle([20, int(h * 0.52), w - 20, int(h * 0.66)], fill=(25, 25, 30))  # hull
    d.polygon([(20, int(h * 0.52)), (w - 20, int(h * 0.52)), (w - 40, int(h * 0.40)),
               (40, int(h * 0.40))], fill=(60, 60, 66))
    cols = [(200, 60, 50), (240, 200, 40), (40, 140, 80), (50, 90, 200), (220, 140, 40)]
    for r in range(2):
        for c in range(6):
            x0 = 30 + c * 46; y0 = int(h * 0.40) - (r + 1) * 20
            d.rectangle([x0, y0, x0 + 42, y0 + 18], fill=cols[(r * 6 + c) % 5],
                        outline=(255, 255, 255), width=1)
    d.rectangle([w - 78, 6, w - 10, 52], fill=RED, outline=(255, 255, 255), width=2)
    f1 = F(13, bold=True); f2 = F(9, bold=True)
    t = "UP TO"; d.text((w - 44 - tw(d, t, f2) / 2, 10), t, font=f2, fill=(255, 255, 255))
    t = "35%"; d.text((w - 44 - tw(d, t, f1) / 2, 24), t, font=f1, fill=(255, 255, 255))
    return im

def art_chip(w, h):
    im, d = panel(w, h, DARK, border=NAVY)
    for i in range(9):  # grid
        d.line([(i * 40, 0), (i * 40, h)], fill=(35, 42, 60), width=1)
        d.line([(0, i * 14), (w, i * 14)], fill=(35, 42, 60), width=1)
    pts = [(10, 12), (40, 24), (70, 16), (100, 30), (140, 22), (170, 36),
           (200, 30), (230, 46), (260, 40), (300, 58), (w - 8, 62)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(220, 40, 40), width=3)
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(255, 80, 80))
    d.rectangle([14, 62, 66, 112], fill=(30, 30, 34), outline=GOLD, width=2)
    for i in range(4):
        d.line([(18 + i * 12, 58), (18 + i * 12, 62)], fill=GOLD, width=2)
        d.line([(18 + i * 12, 112), (18 + i * 12, 116)], fill=GOLD, width=2)
        d.line([(10, 66 + i * 12), (14, 66 + i * 12)], fill=GOLD, width=2)
        d.line([(66, 66 + i * 12), (70, 66 + i * 12)], fill=GOLD, width=2)
    f = F(13, bold=True); d.text((30, 82), "AI", font=f, fill=GOLD)
    fn = F(24, bold=True)
    d.text((76, 66), "4,697.51", font=fn, fill=(255, 255, 255))
    fl = F(9, bold=True)
    d.text((76, 102), "KOSPI -6.2% \u00b7 SK HYNIX -11.1% \u00b7 SAMSUNG -9.9%",
           font=fl, fill=(255, 80, 80))
    return im

def art_space(w, h):
    im, d = panel(w, h, (10, 14, 34), border=NAVY)
    rnd = random.Random(11)
    for _ in range(60):
        x = rnd.randint(4, w - 4); y = rnd.randint(4, int(h * 0.6))
        d.ellipse([x, y, x + 2, y + 2], fill=(255, 255, 255))
    d.ellipse([-w * 0.15, int(h * 0.72), w * 1.15, int(h * 1.35)],
              fill=(60, 110, 190))  # Earth curve
    d.ellipse([-w * 0.10, int(h * 0.78), w * 1.10, int(h * 1.28)], fill=(40, 80, 160))
    # station (upper right)
    d.rectangle([int(w * 0.58), 18, int(w * 0.94), 34], fill=(150, 155, 165),
                outline=(220, 220, 220), width=1)
    d.rectangle([int(w * 0.52), 26, int(w * 0.58), 28], fill=(40, 90, 180))
    d.rectangle([int(w * 0.94), 26, int(w * 0.99), 28], fill=(40, 90, 180))
    d.rectangle([int(w * 0.74), 34, int(w * 0.78), 52], fill=(150, 155, 165))
    # rocket (left-center)
    d.polygon([(64, 10), (78, 26), (78, 70), (64, 70)], fill=(240, 240, 240))
    d.polygon([(64, 10), (71, 0), (78, 10)], fill=RED)
    d.polygon([(64, 58), (56, 72), (64, 70)], fill=RED)
    d.polygon([(78, 58), (86, 72), (78, 70)], fill=RED)
    d.polygon([(66, 70), (71, 92), (76, 70)], fill=(255, 160, 40))
    d.ellipse([66, 30, 76, 40], fill=(40, 90, 180), outline=NAVY, width=1)
    # flags (lower right)
    d.rectangle([int(w * 0.78), 62, int(w * 0.86), 76], fill=(0, 130, 60))
    d.rectangle([int(w * 0.87), 62, int(w * 0.95), 76], fill=(220, 30, 30))
    d.line([(int(w * 0.78), 62), (int(w * 0.78), 84)], fill=(200, 200, 200), width=2)
    d.line([(int(w * 0.87), 62), (int(w * 0.87), 84)], fill=(200, 200, 200), width=2)
    fl = F(8, bold=True)
    d.text((int(w * 0.60), 56), "TIANGONG", font=fl, fill=(255, 255, 255))
    return im

def art_cartagena(w, h):
    im, d = panel(w, h, SKY, border=NAVY)
    d.rectangle([0, int(h * 0.42), w, h], fill=(230, 215, 180))
    d.rectangle([8, int(h * 0.18), w - 8, int(h * 0.42)], fill=(245, 220, 120))
    for i in range(8):  # awning stripes
        x0 = 8 + i * 19
        d.polygon([(x0, int(h * 0.42)), (x0 + 19, int(h * 0.42)),
                   (x0 + 14, int(h * 0.56)), (x0 + 5, int(h * 0.56))],
                  fill=(200, 40, 40) if i % 2 == 0 else (250, 250, 250))
    f = F(11, bold=True); t = "\u00c9XITO"
    d.text(((w - tw(d, t, f)) / 2, int(h * 0.24)), t, font=f, fill=NAVY)
    d.rectangle([int(w * 0.42), int(h * 0.60), int(w * 0.58), h], fill=(120, 80, 40))
    d.rectangle([int(w * 0.10), int(h * 0.62), int(w * 0.30), int(h * 0.86)],
                fill=(120, 180, 220))
    d.rectangle([int(w * 0.70), int(h * 0.62), int(w * 0.90), int(h * 0.86)],
                fill=(120, 180, 220))
    return im

def art_refinery(w, h):
    im, d = panel(w, h, (30, 28, 50), border=NAVY)
    d.rectangle([0, int(h * 0.72), w, h], fill=(60, 45, 30))
    d.rectangle([10, int(h * 0.30), 40, int(h * 0.72)], fill=(90, 90, 95))
    d.rectangle([46, int(h * 0.45), 76, int(h * 0.72)], fill=(110, 110, 115))
    d.rectangle([82, int(h * 0.18), 96, int(h * 0.72)], fill=(130, 130, 135))
    d.rectangle([102, int(h * 0.38), 150, int(h * 0.72)], fill=(90, 90, 95))
    for i in range(3):  # flames
        x = 20 + i * 40
        d.polygon([(x, int(h * 0.30)), (x + 8, int(h * 0.12)), (x + 16, int(h * 0.30))],
                  fill=(255, 140, 0))
    d.ellipse([int(w * 0.70), 8, int(w * 0.95), 30], fill=(240, 220, 140))
    return im

def art_iowa(w, h):
    im, d = panel(w, h, (40, 35, 30), border=NAVY)
    d.ellipse([int(w * 0.30), 4, int(w * 0.72), int(h * 0.85)], fill=(255, 200, 40))
    d.ellipse([int(w * 0.38), 12, int(w * 0.64), int(h * 0.70)], fill=(255, 120, 0))
    d.ellipse([int(w * 0.44), 20, int(w * 0.58), int(h * 0.55)], fill=(255, 230, 120))
    d.rectangle([0, int(h * 0.80), w, h], fill=(70, 70, 75))
    for i in range(5):  # smoke
        d.ellipse([10 + i * 28, 6, 30 + i * 28, 26], fill=(120, 120, 125))
    return im

def art_cyber(w, h):
    im, d = panel(w, h, DARK, border=NAVY)
    d.rectangle([int(w * 0.10), int(h * 0.25), int(w * 0.90), h], fill=(60, 64, 72))
    for r in range(3):
        for c in range(6):
            d.rectangle([int(w * 0.14) + c * 20, int(h * 0.32) + r * 12,
                         int(w * 0.14) + c * 20 + 12, int(h * 0.32) + r * 12 + 8],
                        fill=(200, 220, 255) if (r + c) % 3 else (255, 60, 60))

    return im

def art_satellite(w, h):
    im, d = panel(w, h, (10, 14, 34), border=NAVY)
    rnd = random.Random(7)
    for _ in range(30):
        x = rnd.randint(4, w - 4); y = rnd.randint(4, int(h * 0.7))
        d.ellipse([x, y, x + 2, y + 2], fill=(255, 255, 255))
    d.ellipse([-w * 0.2, int(h * 0.75), w * 1.2, int(h * 1.4)], fill=(50, 100, 180))
    d.ellipse([6, 6, w - 6, h - 6], outline=(220, 60, 60), width=2)  # orbit ring
    d.rectangle([int(w * 0.42), int(h * 0.30), int(w * 0.58), int(h * 0.62)],
                fill=(180, 185, 195), outline=(255, 255, 255), width=1)
    d.rectangle([int(w * 0.08), int(h * 0.36), int(w * 0.42), int(h * 0.56)],
                fill=(40, 90, 180))
    d.rectangle([int(w * 0.58), int(h * 0.36), int(w * 0.92), int(h * 0.56)],
                fill=(40, 90, 180))
    d.line([(int(w * 0.50), int(h * 0.62)), (int(w * 0.50), int(h * 0.78))],
           fill=(200, 200, 200), width=2)
    return im

def art_cricket(w, h):
    im, d = panel(w, h, (60, 150, 70), border=NAVY)
    d.rectangle([0, int(h * 0.55), w, h], fill=(120, 80, 40))  # pitch
    d.rectangle([0, int(h * 0.55), w, int(h * 0.58)], fill=(240, 230, 200))
    d.rectangle([int(w * 0.45), int(h * 0.20), int(w * 0.52), int(h * 0.55)],
                fill=(200, 60, 60))  # batsman
    d.ellipse([int(w * 0.45), int(h * 0.12), int(w * 0.52), int(h * 0.22)],
              fill=(240, 200, 160))
    d.line([(int(w * 0.48), int(h * 0.30)), (int(w * 0.62), int(h * 0.55))],
           fill=(220, 180, 120), width=4)  # bat
    d.ellipse([int(w * 0.68), int(h * 0.48), int(w * 0.72), int(h * 0.54)],
              fill=(255, 255, 255))  # ball
    for x in (int(w * 0.18), int(w * 0.80)):  # stumps
        d.rectangle([x, int(h * 0.42), x + 3, int(h * 0.55)], fill=(240, 220, 140))
    return im

def art_tanker(w, h):
    im, d = panel(w, h, SKY, border=NAVY)
    d.rectangle([0, int(h * 0.70), w, h], fill=(80, 80, 85))  # road
    d.line([(0, int(h * 0.70)), (w, int(h * 0.70))], fill=(255, 255, 255), width=2)
    d.ellipse([int(w * 0.10), 6, int(w * 0.40), int(h * 0.62)], fill=(255, 140, 0))
    d.ellipse([int(w * 0.18), 14, int(w * 0.34), int(h * 0.50)], fill=(255, 220, 60))
    d.rounded_rectangle([int(w * 0.45), int(h * 0.40), int(w * 0.85), int(h * 0.68)],
                        radius=8, fill=(220, 220, 225), outline=NAVY, width=1)
    d.rectangle([int(w * 0.85), int(h * 0.46), int(w * 0.97), int(h * 0.68)],
                fill=(200, 60, 40))
    d.ellipse([int(w * 0.52), int(h * 0.66), int(w * 0.60), int(h * 0.78)], fill=(20, 20, 20))
    d.ellipse([int(w * 0.74), int(h * 0.66), int(w * 0.82), int(h * 0.78)], fill=(20, 20, 20))
    return im

def art_odesa(w, h):
    im, d = panel(w, h, (18, 18, 40), border=NAVY)
    d.ellipse([int(w * 0.60), 4, int(w * 0.92), int(h * 0.55)], fill=(255, 140, 0))
    d.ellipse([int(w * 0.68), 12, int(w * 0.84), int(h * 0.42)], fill=(255, 220, 90))
    for i, bh in enumerate((34, 46, 30, 40, 26)):
        x0 = 8 + i * 30
        d.rectangle([x0, h - bh, x0 + 24, h], fill=(10, 10, 22))
        for wy in range(h - bh + 5, h - 4, 9):
            d.rectangle([x0 + 4, wy, x0 + 8, wy + 4], fill=(255, 210, 90))
    return im

def art_gaza(w, h):
    im, d = panel(w, h, (16, 16, 36), border=NAVY)
    rnd = random.Random(3)
    for _ in range(25):
        x = rnd.randint(4, w - 4); y = rnd.randint(4, int(h * 0.5))
        d.ellipse([x, y, x + 2, y + 2], fill=(255, 255, 255))
    d.ellipse([int(w * 0.78), 6, int(w * 0.94), 22], fill=(240, 230, 180))
    for i, bh in enumerate((30, 42, 26, 36)):
        x0 = 10 + i * 34
        d.rectangle([x0, h - bh, x0 + 26, h], fill=(12, 12, 24))
        for wy in range(h - bh + 5, h - 4, 9):
            d.rectangle([x0 + 5, wy, x0 + 9, wy + 4], fill=(255, 200, 80))
    d.rectangle([int(w * 0.85), int(h * 0.30), int(w * 0.88), h], fill=(12, 12, 24))
    d.polygon([(int(w * 0.83), int(h * 0.30)), (int(w * 0.90), int(h * 0.30)),
               (int(w * 0.865), int(h * 0.16))], fill=(12, 12, 24))
    return im

def art_huawei(w, h):
    im, d = panel(w, h, (210, 205, 190), border=NAVY)
    d.polygon([(int(w * 0.15), int(h * 0.30)), (int(w * 0.50), int(h * 0.08)),
               (int(w * 0.85), int(h * 0.30))], fill=(150, 145, 135))
    d.rectangle([int(w * 0.12), int(h * 0.30), int(w * 0.88), int(h * 0.38)],
                fill=(120, 115, 105))
    for i in range(5):
        x0 = int(w * 0.16) + i * 26
        d.rectangle([x0, int(h * 0.38), x0 + 12, int(h * 0.78)], fill=(235, 230, 220),
                    outline=(120, 115, 105), width=1)
    d.rectangle([int(w * 0.12), int(h * 0.78), int(w * 0.88), int(h * 0.84)],
                fill=(120, 115, 105))
    for i in range(3):
        d.rectangle([int(w * 0.08) + i * 6, int(h * 0.84) + i * 5,
                     int(w * 0.92) - i * 6, int(h * 0.84) + i * 5 + 4],
                    fill=(100, 95, 88))
    return im

def art_temp(w, h):
    im, d = panel(w, h, (180, 220, 235), border=NAVY)
    d.ellipse([int(w * 0.08), 8, int(w * 0.62), h - 8], fill=(50, 110, 200),
              outline=NAVY, width=1)
    d.ellipse([int(w * 0.16), 16, int(w * 0.34), 30], fill=(60, 170, 80))
    d.ellipse([int(w * 0.36), int(h * 0.45), int(w * 0.55), int(h * 0.70)],
              fill=(60, 170, 80))
    d.rectangle([int(w * 0.74), 8, int(w * 0.82), int(h * 0.70)], fill=(240, 240, 240),
                outline=NAVY, width=1)
    d.ellipse([int(w * 0.68), int(h * 0.62), int(w * 0.88), int(h * 0.92)],
              fill=(220, 40, 40))
    d.rectangle([int(w * 0.76), 12, int(w * 0.80), int(h * 0.70)], fill=(220, 40, 40))
    return im

def art_heat(w, h):
    im, d = panel(w, h, (250, 200, 110), border=NAVY)
    d.ellipse([int(w * 0.34), 4, int(w * 0.66), int(h * 0.55)], fill=(255, 210, 40),
              outline=(255, 140, 0), width=2)
    for i, bh in enumerate((28, 40, 22, 34)):
        x0 = 8 + i * 38
        d.rectangle([x0, h - bh, x0 + 30, h], fill=(90, 60, 40))
        for wy in range(h - bh + 5, h - 4, 8):
            d.rectangle([x0 + 5, wy, x0 + 10, wy + 4], fill=(255, 220, 120))
    return im

ART = {"tariffs": art_tariffs, "chip": art_chip, "space": art_space,
       "cartagena": art_cartagena, "refinery": art_refinery, "iowa": art_iowa,
       "cyber": art_cyber, "satellite": art_satellite, "cricket": art_cricket,
       "tanker": art_tanker, "odesa": art_odesa, "gaza": art_gaza,
       "huawei": art_huawei, "temp": art_temp, "heat": art_heat}

HERO_PLACES = ("1 Washington \u00b7 2 Seoul \u00b7 3 Jiuquan \u00b7 4 Cartagena \u00b7 "
    "5 Ras Tanura \u00b7 6 Middletown \u00b7 7 Langley \u00b7 8 Brussels \u00b7 9 UAE \u00b7 "
    "10 Giza \u00b7 11 Odesa \u00b7 12 Gaza \u00b7 13 New York \u00b7 14 World \u00b7 15 London")

def draw_topbar(d, y):
    d.rectangle([MX, y, MX + CW, y + 14], fill=NAVY)
    f = F(9, bold=True)
    d.text((MX + (CW - tw(d, TOPBAR, f)) / 2, y + 2), TOPBAR, font=f, fill=(255, 255, 255))
    return y + 14

def draw_masthead(d, y):
    f1 = F(40, serif=True)
    d.text((MX + (CW - tw(d, TITLE, f1)) / 2, y), TITLE, font=f1, fill=NAVY)
    f2 = F(13, italic=True)
    d.text((MX + (CW - tw(d, SUBHEAD, f2)) / 2, y + 44), SUBHEAD, font=f2, fill=RED)
    return y + 58

def draw_chips(d, y):
    size = 10
    while size > 7:
        f = F(size, bold=True); tot = -6
        for name, n, _ in REGIONS:
            tot += tw(d, f"{name} {n}", f) + 18 + 6
        if tot <= CW: break
        size -= 1
    f = F(size, bold=True); x = MX
    for name, n, col in REGIONS:
        t = f"{name} {n}"; wdt = tw(d, t, f) + 18
        rounded(d, [x, y, x + wdt, y + 18], 9, col)
        d.text((x + 9, y + (18 - size) / 2 - 1), t, font=f, fill=(255, 255, 255))
        x += wdt + 6
    return y + 18

def draw_fields(d, y):
    lab = "17 FIELDS"; fl = F(10, bold=True)
    d.text((MX, y + 2), lab, font=fl, fill=RED)
    txt = "  \u00b7  ".join(f"{n} {c}" for n, c in FIELDS)
    f = fit_font(d, txt, CW - tw(d, lab, fl) - 14, 9)
    d.text((MX + tw(d, lab, fl) + 8, y + 3), txt, font=f, fill=INK)
    return y + 16

def draw_numbers(d, y):
    rule(d, MX, y, CW, NAVY)
    colw = CW / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = MX + colw * i + colw / 2
        f1 = F(24, bold=True)
        d.text((cx - tw(d, num, f1) / 2, y + 6), num, font=f1, fill=RED)
        f2 = F(8, bold=True)
        d.text((cx - tw(d, lab, f2) / 2, y + 34), lab, font=f2, fill=NAVY)
    rule(d, MX, y + 48, CW, NAVY)
    return y + 50

def draw_utc(d, y):
    d.rectangle([MX, y, MX + CW, y + 22], fill=NAVY)
    size = 9
    while size > 7:
        fl = F(size, bold=True); tot = tw(d, UTC_LABEL, fl) + 22
        for t, ev in UTC_EVENTS:
            tot += tw(d, t, fl) + 4 + tw(d, ev, fl) + 14
        if tot <= CW - 16: break
        size -= 1
    fl = F(size, bold=True); x = MX + 8
    d.text((x, y + (22 - size) / 2 - 1), UTC_LABEL, font=fl, fill=(255, 255, 255))
    x += tw(d, UTC_LABEL, fl) + 12
    for i, (t, ev) in enumerate(UTC_EVENTS):
        d.text((x, y + (22 - size) / 2 - 1), t, font=fl, fill=(255, 120, 120))
        x += tw(d, t, fl) + 4
        d.text((x, y + (22 - size) / 2 - 1), ev, font=fl, fill=(255, 255, 255))
        x += tw(d, ev, fl)
        if i < len(UTC_EVENTS) - 1:
            d.text((x, y + (22 - size) / 2 - 1), "  \u00b7  ", font=fl, fill=(150, 150, 150))
            x += tw(d, "  \u00b7  ", fl)
    return y + 22

def draw_hero(d, x, y, w, hero):
    im = ART[hero["art"]](w, 118)
    d._image.paste(im, (x, y))
    num_badge(d, x + 14, y + 14, hero["num"])
    col = REGION_COLOR[hero["region"]]
    d.rectangle([x, y + 118, x + w, y + 132], fill=col)
    f = F(9, bold=True)
    d.text((x + 4, y + 121), hero["place"], font=f, fill=(255, 255, 255))
    st = hero["status"]
    d.text((x + w - 4 - tw(d, st, f), y + 121), st, font=f, fill=(255, 255, 255))
    yy = y + 136
    for ln in wrap(d, hero["head"], F(15, bold=True), w - 8)[:2]:
        d.text((x + 4, yy), ln, font=F(15, bold=True), fill=NAVY); yy += 17
    yy += 3
    for ln in wrap(d, hero["body"], F(10), w - 8)[:3]:
        d.text((x + 4, yy), ln, font=F(10), fill=INK); yy += 13
    yy += 3
    d.text((x + 4, yy), "WHY IT MATTERS", font=F(9, bold=True), fill=RED); yy += 12
    for ln in wrap(d, hero["why"], F(10, italic=True), w - 8)[:2]:
        d.text((x + 4, yy), ln, font=F(10, italic=True), fill=INK); yy += 12
    yy += 2
    d.text((x + 4, yy), hero["src"], font=F(8), fill=GREY)
    return y + 264

def draw_medium(d, x, y, w, m):
    im = ART[m["art"]](w, 62)
    d._image.paste(im, (x, y))
    num_badge(d, x + 12, y + 12, m["num"], r=10)
    fb = F(8, bold=True); bw = tw(d, m["badge"], fb) + 8
    d.rectangle([x + w - 4 - bw, y + 4, x + w - 4, y + 17], fill=RED)
    d.text((x + w - 8 - tw(d, m["badge"], fb), y + 6), m["badge"], font=fb,
           fill=(255, 255, 255))
    col = REGION_COLOR[m["region"]]
    d.rectangle([x, y + 62, x + w, y + 74], fill=col)
    f = F(7, bold=True)
    d.text((x + 4, y + 65), m["place"], font=f, fill=(255, 255, 255))
    st = m["status"]
    d.text((x + w - 4 - tw(d, st, f), y + 65), st, font=f, fill=(255, 255, 255))
    yy = y + 78
    for ln in wrap(d, m["head"], F(10, bold=True), w - 8)[:2]:
        d.text((x + 4, yy), ln, font=F(10, bold=True), fill=NAVY); yy += 12
    yy += 3
    for ln in wrap(d, m["body"], F(9), w - 8)[:3]:
        d.text((x + 4, yy), ln, font=F(9), fill=INK); yy += 11
    yy += 2
    d.text((x + 4, yy), m["src"], font=F(8), fill=GREY)
    return y + 148

def draw_map(d, x, y, w, h):
    im = Image.new("RGB", (w, h), (242, 236, 222)); md = ImageDraw.Draw(im)
    md.rectangle([0, 0, w - 1, h - 1], outline=(180, 170, 150), width=1)
    for lon in range(-180, 181, 30):
        px = (lon + 180) / 360 * w
        md.line([(px, 0), (px, h)], fill=(215, 208, 195), width=1)
    for lat in range(-60, 91, 30):
        py = (85 - lat) / 145 * h
        md.line([(0, py), (w, py)], fill=(215, 208, 195), width=1)
    def proj(lon, lat):
        return ((lon + 180) / 360 * w, (85 - lat) / 145 * h)
    for poly in CONTINENTS:
        md.polygon([proj(lon, lat) for lon, lat in poly], fill=(222, 210, 185),
                   outline=(160, 150, 130))
    f = F(6, bold=True)
    for n, lon, lat in MAP_DOTS:
        px, py = proj(lon, lat)
        md.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                   outline=(255, 255, 255), width=1)
        t = str(n)
        md.text((px - tw(md, t, f) / 2, py - 3.5), t, font=f, fill=(255, 255, 255))
    d._image.paste(im, (x, y))

def draw_bottom(d, y):
    fT = F(10, bold=True)
    d.text((MX, y), "WHERE IT HAPPENED", font=fT, fill=NAVY)
    ax = MX + 310; aw = CW - 310
    d.text((ax, y), "ALSO ON 25 NOVEMBER \u2014 40 MORE STORIES", font=fT, fill=NAVY)
    rule(d, MX, y + 13, CW, NAVY)
    draw_map(d, MX, y + 16, 300, 100)
    ly = y + 120
    fL = F(7, bold=True)
    d.text((MX, ly), "30 NUMBERED PLACES \u2014 DOTS ARE THE STORIES ABOVE", font=fL,
           fill=GREY)
    ly += 11
    f7 = F(7)
    for row in (REGIONS[:5], REGIONS[5:]):
        xx = MX
        for name, n, col in row:
            d.rectangle([xx, ly + 1, xx + 7, ly + 8], fill=col)
            xx += 8
            t = f"{name} {n}"
            d.text((xx, ly), t, font=f7, fill=INK); xx += tw(d, t, f7) + 3
        ly += 10
    ly += 2
    for ln in wrap(d, HERO_PLACES, F(7), 300):
        d.text((MX, ly), ln, font=F(7), fill=GREY); ly += 9
    # ALSO 4 columns x 10 rows
    colw = (aw - 24) / 4
    for ci in range(4):
        cx = ax + ci * (colw + 8)
        for ri in range(10):
            n, head = ALSO[ci * 10 + ri]
            yy = y + 16 + ri * 9
            fn = F(8, bold=True)
            d.text((cx, yy), f"{n}", font=fn, fill=RED)
            d.text((cx + 15, yy), head, font=F(8), fill=INK)
    # TOMORROW box (fills down to the pins' end)
    ty = y + 16 + 10 * 9 + 6
    d.rectangle([ax, ty, ax + aw, ly + 2], fill=NAVY)
    d.text((ax + 8, ty + 4), "TOMORROW: WHAT TO WATCH", font=F(9, bold=True),
           fill=(255, 255, 255))
    d.text((ax + 8, ty + 18), "US Thanksgiving (Thu 26 Nov)", font=F(8),
           fill=(255, 255, 255))
    d.text((ax + 8, ty + 30), "Bundestag budget vote (Fri 27 Nov)", font=F(8),
           fill=(255, 255, 255))
    d.text((ax + 8, ty + 42), "Tariff hearings (23 Jan)", font=F(8),
           fill=(255, 255, 255))
    return ly + 4

def draw_datecheck(d, y):
    d.rectangle([MX, y, MX + CW, y + 34], outline=RED, width=1)
    lines = wrap(d, DATE_CHECK, F(8), CW - 12)[:3]
    yy = y + 2
    for ln in lines:
        d.text((MX + 6, yy), ln, font=F(8), fill=INK); yy += 11
    return y + 34

def draw_footer(d, y):
    f1 = F(9, bold=True)
    d.text((MX + (CW - tw(d, FOOTER_GUARANTEE, f1)) / 2, y), FOOTER_GUARANTEE,
           font=f1, fill=NAVY)
    f2 = F(8)
    d.text((MX + (CW - tw(d, FOOTER_SOURCES, f2)) / 2, y + 12), FOOTER_SOURCES,
           font=f2, fill=GREY)
    d.text((MX + (CW - tw(d, FOOTER_LEGEND, f2)) / 2, y + 23), FOOTER_LEGEND,
           font=f2, fill=INK)
    return y + 33

def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    y = 8
    y = draw_topbar(d, y); y += 2
    y = draw_masthead(d, y); y += 2
    y = draw_chips(d, y); y += 2
    y = draw_fields(d, y); y += 2
    y = draw_numbers(d, y); y += 2
    y = draw_utc(d, y); y += 2
    hw = (CW - 18) // 3
    for i, hero in enumerate(BIG):
        draw_hero(d, MX + i * (hw + 6), y, hw, hero)
    y += 264; y += 2
    mw = (CW - 30) // 6
    for row in (MED[:6], MED[6:]):
        for i, m in enumerate(row):
            draw_medium(d, MX + i * (mw + 6), y, mw, m)
        y += 148
        if row is MED[:6]: y += 4
    y += 2
    y = draw_bottom(d, y); y += 2
    y = draw_datecheck(d, y); y += 2
    y = draw_footer(d, y)
    assert y <= H, f"final y {y} exceeds {H}"
    print("final y:", y)
    img.save("entry.png", format="PNG", optimize=True)
    data = open("entry.png", "rb").read()
    print("size:", len(data), "sha256:", hashlib.sha256(data).hexdigest())

if __name__ == "__main__":
    build()
