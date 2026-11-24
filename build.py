#!/usr/bin/env python3
"""Build entry.png for news-image-20261124 (acct1, Masrukhan25).

Draws a broadsheet newspaper entirely in PIL flat-vector from the 31 verified
stories of Tuesday 24 November 2026. No photos, no network, no AI images.
Run:  python3 build.py   ->  writes entry.png (1024x1024, PNG, < 1 MiB)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- palette
PAPER   = (246, 238, 216)   # cream newsprint
PANEL   = (251, 246, 230)   # lighter panel
INK     = (26, 26, 26)
RULE    = (26, 26, 26)
MUTED   = (90, 84, 70)
NAVY    = (27, 58, 92)
RED     = (176, 58, 46)
GOLD    = (183, 149, 11)
GREEN   = (30, 132, 73)
SEA     = (214, 228, 238)
LAND    = (216, 201, 163)
LAND_LN = (150, 132, 96)
SKY     = (205, 222, 235)

REGION_COLOR = {
    "North America": (176, 58, 46),
    "Europe":        (36, 113, 163),
    "Middle East":   (160, 130, 10),
    "Africa":        (30, 132, 73),
    "Asia-Pacific":  (125, 60, 152),
    "Latin America": (202, 111, 30),
    "Global":        (100, 100, 100),
}
REGION_SHORT = {
    "North America": "N. AMERICA", "Europe": "EUROPE",
    "Middle East": "MIDEAST", "Africa": "AFRICA",
    "Asia-Pacific": "ASIA-PACIFIC", "Latin America": "LATIN AMERICA",
    "Global": "GLOBAL",
}

# ---------------------------------------------------------------- fonts
def font(name, size):
    cands = {
        "serif": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"],
        "serif_r": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"],
        "serif_i": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"],
        "sans": ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"],
        "sans_b": ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"],
        "mono": ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"],
        "mono_b": ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"],
    }[name]
    for p in cands:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_MAST   = font("serif", 58)
F_DATE   = font("serif", 40)
F_HERO   = font("serif", 21)
F_HERO_S = font("serif", 19)
F_GRID   = font("sans_b", 13)
F_GRID_S = font("sans", 11)
F_BODY   = font("sans", 12)
F_SMALL  = font("sans", 10)
F_SMALLB = font("sans_b", 10)
F_TINY   = font("sans", 9)
F_TINYB  = font("sans_b", 9)
F_TAG    = font("sans_b", 9)
F_NUM    = font("serif", 26)
F_MAPT   = font("sans_b", 12)
F_SECT   = font("sans_b", 13)

# ---------------------------------------------------------------- stories
# (num, region, headline, summary, source, tag, lon, lat)
STORIES = [
    (1, "Middle East", "Three tankers hit mines in Hormuz, IRGC claims",
     "IRGC claimed three tankers caught fire on naval mines under US escort; unverified.",
     "Trends MENA / TBS News", "REPORTED", 56.3, 26.6),
    (2, "Asia-Pacific", "Russian jets trigger air-raid alert on Ulleung",
     "Russian jets entered Seoul's defence zone; residents sheltered at 7:52 a.m. F-15Ks scrambled.",
     "Reuters", "CONFIRMED", 130.9, 37.5),
    (3, "Europe", "Sanofi to buy Insmed in $41 billion deal",
     "Sanofi will acquire US biotech Insmed for $41 billion in cash, its biggest pharma bet in years.",
     "Reuters", "CONFIRMED", 2.35, 48.86),
    (4, "North America", "US blacklists Megaspeed, Alibaba unit in Nvidia scandal",
     "The US Commerce Department moved to blacklist Megaspeed and Alibaba's Singapore unit Apex Enterprise Solutions, barring US firms from shipping them goods without a licence.",
     "Reuters", "CONFIRMED", -77.0, 38.9),
    (5, "Europe", "HLD plans takeover bid for care home operator Clariane",
     "Asset manager HLD Europe will launch a friendly bid at \u20ac4.60 a share, backed by a shareholder group holding about 53%.",
     "Reuters", "CONFIRMED", 2.35, 48.86),
    (6, "Europe", "Central European leaders reject new EU budget proposal",
     "The Visegrad group plus Austria rejected the \u20ac1.582 trillion EU budget plan for 2028-2034, calling it unacceptable before a summit on 26-27 November.",
     "Reuters", "CONFIRMED", 17.1, 48.1),
    (7, "Europe", "Russia warns Estonia its actions risk 'open war'",
     "Moscow summoned Estonia's charge d'affaires over plans to close the land border from 1 December; Medvedev argued a massive attack could justify a preventive nuclear strike.",
     "Reuters", "REPORTED", 24.7, 59.4),
    (8, "Europe", "EU opens antitrust probe into Coca-Cola bottler CCEP",
     "The European Commission launched an antitrust investigation into Coca-Cola Europacific Partners as Brussels debates territorial supply rules.",
     "Table.Briefings", "CONFIRMED", 4.4, 50.8),
    (9, "Europe", "EU auditors fault oversight of indirect aid",
     "The European Court of Auditors criticised the Commission for outdated information and insufficient monitoring of how aid money is used.",
     "European Court of Auditors", "CONFIRMED", 6.1, 49.6),
    (10, "Middle East", "Iran courts demand $290 billion from US",
     "Iranian courts ordered the US to pay $290 billion in damages for the war and earlier actions, a senior judiciary official said; Tehran also sued Gulf states.",
     "AFP", "REPORTED", 51.4, 35.7),
    (11, "Middle East", "Israeli strikes in Gaza kill three, incl. UNRWA worker",
     "Strikes across Gaza killed at least three people, including UNRWA worker Adel al-Helou, hit at a water well in the Jabalia refugee camp.",
     "Al Jazeera", "REPORTED", 34.5, 31.5),
    (12, "Middle East", "Houthis claim Saudi airstrike kills 17 in Hodeida",
     "The Houthis claimed a strike on a telecom building killed 17 and injured 11; the claim is not independently verified and Riyadh has not commented.",
     "AFP", "REPORTED", 42.9, 14.8),
    (13, "Africa", "Somalia, Uganda seek stronger anti-Shabaab push",
     "Presidents Mohamud and Museveni called for intensified operations and sustainable funding for the AU mission as Uganda begins a phased troop withdrawal.",
     "Shabelle Media Network", "REPORTED", 32.5, 0.0),
    (14, "Africa", "WFP warns 10m tons of wheat may miss markets",
     "The World Food Programme warned wheat from Ukraine and Russia may miss global markets, with Africa's importers first in line.",
     "WFP", "CONFIRMED", 12.5, 41.9),
    (15, "Africa", "AU maternal health roadmap launched in Ethiopia",
     "Tanzanian President Samia Suluhu Hassan launched the AU's 2026-2030 maternal health roadmap, built on Three Zeros, in Addis Ababa.",
     "Today News Africa", "CONFIRMED", 38.7, 9.0),
    (16, "Africa", "One in six pregnancies in Africa is to an adolescent girl, Africa CDC finds",
     "Africa CDC found one in six pregnancies is to an adolescent girl and only one facility in eight offers adolescent-friendly services.",
     "Africa CDC", "CONFIRMED", 38.7, 9.0),
    (17, "Africa", "Heavy fighting in Ituri traps DR Congo Ebola responders",
     "Fighting near a hospital in Ituri disrupted Ebola responders' work and forced emergency teams to take cover for more than 24 hours, the WHO said.",
     "UN News / WHO", "CONFIRMED", 30.2, 1.6),
    (18, "Africa", "Qatar condemns drone attacks on Khartoum",
     "Qatar condemned drone attacks on Khartoum, including one that hit a UN building, calling them a breach of Sudan's sovereignty and the UN Charter.",
     "Qatar MFA", "REPORTED", 32.5, 15.6),
    (19, "Asia-Pacific", "Explosion kills 6, injures 10 in Vietnam capital Hanoi",
     "At least six people were killed and 10 injured in an explosion at 8 a.m. at a food shop on Dong Da Street in a densely populated area.",
     "Reuters", "CONFIRMED", 105.9, 21.0),
    (20, "Asia-Pacific", "Magnitude 5.6 earthquake strikes Nepal near Tibet border",
     "A magnitude 5.6 quake struck near Olangchung Gola in Taplejung district and was felt across Nepal and northern India; no casualties were reported.",
     "Reuters", "CONFIRMED", 87.9, 27.9),
    (21, "Asia-Pacific", "Japan accelerates ICC funding as US sanctions threaten court",
     "Japan will pay its full 2027 contribution to the International Criminal Court by year-end, PM Sanae Takaichi said, after the court sought early payment.",
     "Reuters", "CONFIRMED", 139.7, 35.7),
    (22, "Asia-Pacific", "Australia to fine tech firms up to 5% of global revenue under internet safety bill",
     "Tech firms will face fines of up to 5% of global revenue for breaching Australia's internet safety bill, Minister Anika Wells said.",
     "Reuters", "CONFIRMED", 149.1, -35.3),
    (23, "Asia-Pacific", "Sheikh Hasina plans return to Bangladesh on 16 December",
     "Ousted PM Sheikh Hasina plans to return from more than two years of exile in India on 16 December, her spokesperson told Reuters.",
     "Reuters", "CONFIRMED", 90.4, 23.8),
    (24, "Asia-Pacific", "China names Shenzhou-24 crew with first foreign astronaut to visit Tiangong",
     "China named the crew - commander Tang Hongbo, Wu Yi and Pakistani payload specialist Zeeshan Ali - for a launch on Wednesday morning from Jiuquan.",
     "Reuters", "CONFIRMED", 100.3, 40.9),
    (25, "Asia-Pacific", "Manila court orders arrest of Atong Ang in missing sabungeros case",
     "A Manila court issued a non-bailable arrest warrant against businessman Charlie 'Atong' Ang over the disappearance of six cockfighting enthusiasts.",
     "Philippine News Agency", "REPORTED", 121.0, 14.6),
    (26, "Asia-Pacific", "Japan cuts view on consumer spending for first time since 2024",
     "Japan's government downgraded its view on consumer spending in November for the first time in more than two and a half years, citing rising prices.",
     "Reuters", "CONFIRMED", 139.7, 35.7),
    (27, "Latin America", "Car bomb rocks Villavicencio governor's office, 23 injured",
     "A car bomb outside the Meta governor's office injured 23 people and damaged nearby buildings; President De la Espriella blamed drug trafficking groups.",
     "El Tiempo", "REPORTED", -73.6, 4.1),
    (28, "Latin America", "Mexico will try 'El Chapo Isidro' at home despite US extradition request",
     "Mexico will try alleged drug lord Fausto Isidro Meza Flores in its own courts, Attorney General Godoy said, after his capture in a firefight that killed four soldiers.",
     "Reuters", "REPORTED", -99.1, 19.4),
    (29, "Latin America", "WHO chief visits Cuba as healthcare system deteriorates",
     "WHO Director-General Tedros visited Havana to assess Cuba's worsening healthcare amid US sanctions, fuel and electricity shortages.",
     "Al Jazeera", "CONFIRMED", -82.4, 23.1),
    (30, "Latin America", "Man with Alzheimer's rescued in Amazon after surviving 11 days alone",
     "An elderly man with Alzheimer's who survived 11 days alone in the Amazon rainforest is recovering after being rescued, park rangers said.",
     "AP", "REPORTED", -60.0, -3.1),
    (31, "Latin America", "Migrant caravan crosses from Guatemala into Mexico",
     "Around 300 migrants crossed from Guatemala into Mexico, hoping to reach the United States, as a new caravan walked towards the US border.",
     "Al Jazeera", "REPORTED", -92.3, 14.9),
]

NUMBERS = [
    ("$41bn", "Sanofi buys Insmed"),
    ("$290bn", "Iran courts demand from US"),
    ("5.6", "Nepal quake magnitude"),
    ("6 killed", "Hanoi explosion"),
    ("23", "injured in Villavicencio blast"),
    ("10m tons", "wheat at risk, WFP warns"),
    ("5%", "max tech fine, Australia"),
]

DATE_CHECK = [
    "Nvidia reinstates Huang (+31%) - 23 Nov, yesterday's hero",
    "COP31 talks collapse - confirmed 23 Nov",
    "Ukraine sinks corvette Merkury - 22-23 Nov",
    "SoftBank $2B Intel / typhoid drive - stale 2025 re-listings",
    "CAS Senegal AFCON ruling - not yet decided at cutoff",
]

REGION_COUNTS = [("N. AMERICA", 1), ("EUROPE", 6), ("MIDEAST", 4),
                 ("AFRICA", 6), ("ASIA-PACIFIC", 9), ("LATIN AM.", 5)]

# ---------------------------------------------------------------- text helpers
def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(d, x, y, text, fnt, max_w, fill=INK, leading=None, max_lines=None):
    lines = wrap(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or (fnt.size + 3)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def pill(d, x, y, text, bg, fg=(255, 255, 255)):
    w = int(d.textlength(text, font=F_TAG)) + 12
    h = 15
    d.rounded_rectangle([x, y, x + w, y + h], radius=7, fill=bg)
    d.text((x + 6, y + 2), text, font=F_TAG, fill=fg)
    return w

def num_badge(d, cx, cy, n, r=11, fill=RED):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=(255, 255, 255), width=1)
    t = str(n)
    tw = d.textlength(t, font=F_TINYB)
    d.text((cx - tw / 2, cy - 7), t, font=F_TINYB, fill=(255, 255, 255))

# ---------------------------------------------------------------- continents (lon, lat) rough outlines
CONTINENTS = [
    # North America
    [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58), (-130, 54),
     (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16),
     (-94, 17), (-90, 14), (-86, 12), (-83, 9), (-79, 9), (-81, 13), (-84, 16),
     (-87, 21), (-90, 21), (-91, 19), (-97, 26), (-93, 30), (-89, 30), (-84, 30),
     (-81, 25), (-80, 32), (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44),
     (-60, 47), (-55, 52), (-60, 55), (-65, 58), (-68, 58), (-75, 62), (-78, 62),
     (-85, 66), (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)],
    # Greenland
    [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-22, 70), (-20, 74),
     (-25, 78), (-35, 80), (-50, 80), (-58, 76), (-60, 72)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23),
     (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54), (-66, -55),
     (-68, -50), (-65, -45), (-62, -41), (-58, -38), (-52, -33), (-48, -28),
     (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0),
     (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-76, 10)],
    # Africa
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (30, 31), (32, 31), (34, 28), (37, 22), (39, 18),
     (43, 12), (48, 11), (51, 12), (46, 5), (41, 0), (40, -5), (39, -12),
     (36, -18), (33, -26), (28, -33), (20, -35), (17, -32), (15, -27),
     (13, -18), (12, -12), (13, -5), (9, 4), (4, 6), (-8, 5), (-13, 8)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-2, 48), (-4, 49), (0, 50),
     (3, 52), (5, 53), (8, 57), (10, 59), (5, 60), (5, 62), (12, 64),
     (18, 69), (25, 71), (30, 70), (35, 68), (40, 67), (45, 68), (55, 69),
     (65, 69), (70, 72), (75, 73), (80, 73), (90, 75), (100, 76), (110, 74),
     (120, 73), (130, 72), (140, 72), (150, 70), (160, 69), (170, 66), (178, 65),
     (178, 62), (170, 60), (162, 56), (158, 52), (150, 59), (142, 55), (140, 50),
     (135, 45), (130, 42), (127, 40), (126, 38), (122, 38), (120, 34), (122, 30),
     (120, 25), (118, 24), (110, 20), (108, 18), (105, 10), (104, 9), (100, 7),
     (98, 10), (97, 16), (94, 17), (92, 21), (89, 22), (86, 20), (83, 18),
     (80, 15), (77, 8), (76, 10), (73, 16), (70, 20), (66, 25), (61, 25),
     (57, 26), (54, 27), (52, 29), (50, 30), (48, 30), (44, 29), (40, 30),
     (36, 36), (33, 36), (30, 36), (27, 37), (23, 36), (22, 37), (19, 40),
     (16, 38), (14, 38), (12, 42), (10, 44), (8, 44), (3, 43), (0, 40),
     (-2, 37), (-6, 36), (-9, 37)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-3, 50)],
    # Japan
    [(130, 31), (132, 33), (134, 34), (137, 35), (139, 35), (140, 37), (141, 39),
     (141, 41), (142, 42), (140, 43), (138, 38), (136, 36), (133, 35), (131, 33)],
    # Australia
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (137, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -11), (140, -17),
     (136, -15), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17), (117, -20)],
    # Indonesia / SE Asia islands (simplified)
    [(95, 5), (98, 3), (100, -1), (103, -3), (105, -5), (107, -7), (110, -7),
     (112, -7), (114, -8), (116, -9), (118, -9), (120, -10), (122, -9), (124, -10),
     (126, -8), (128, -6), (130, -4), (132, -3), (134, -4), (136, -3), (138, -5),
     (140, -7), (141, -8), (138, -8), (135, -6), (132, -3), (130, 0), (128, 1),
     (126, 1), (124, 1), (122, 1), (120, 0), (118, 0), (116, 1), (114, 0),
     (112, 1), (110, 2), (108, 3), (106, 4), (104, 2), (102, 3), (100, 5), (98, 6)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (50, -20), (47, -25), (44, -25), (43, -21)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (178, -37),
     (175, -40), (173, -42), (170, -44)],
]

# ---------------------------------------------------------------- hero art (flat-vector)
def burst(d, cx, cy, r, color):
    """Starburst explosion."""
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)

def art_hormuz(d, x, y, w, h):
    """Strait of Hormuz: sea, three tankers, mine bursts, escort ship."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(58, 110, 150))
    d.rectangle([x, y + h * 0.55, x + w, y + h * 0.58], fill=(255, 255, 255))
    # distant cliffs
    d.polygon([(x, y + h * 0.55), (x + w * 0.18, y + h * 0.30), (x + w * 0.38, y + h * 0.55)],
              fill=(150, 132, 96))
    d.polygon([(x + w * 0.82, y + h * 0.55), (x + w, y + h * 0.38), (x + w, y + h * 0.55)],
              fill=(150, 132, 96))
    # escort warship (grey, left)
    sx, sy = x + w * 0.06, y + h * 0.62
    d.polygon([(sx, sy + 14), (sx + 64, sy + 14), (sx + 58, sy + 2), (sx + 6, sy + 2)], fill=(90, 96, 102))
    d.rectangle([sx + 20, sy - 6, sx + 34, sy + 2], fill=(90, 96, 102))
    d.line([sx + 27, sy - 14, sx + 27, sy - 6], fill=(90, 96, 102), width=2)
    # three tankers
    for i, tx in enumerate([0.30, 0.52, 0.74]):
        txp = x + w * tx
        d.rectangle([txp, y + h * 0.70, txp + 62, y + h * 0.82], fill=(40, 40, 40))
        d.rectangle([txp + 8, y + h * 0.62, txp + 26, y + h * 0.70], fill=(200, 60, 40))
        d.rectangle([txp + 30, y + h * 0.64, txp + 54, y + h * 0.70], fill=(230, 230, 230))
        burst(d, txp + 31, y + h * 0.52, 16 if i != 1 else 20, (245, 176, 65))
        burst(d, txp + 31, y + h * 0.52, 9, (220, 60, 30))
    # smoke
    for cx, cy, r in [(x + w * 0.34, y + h * 0.34, 9), (x + w * 0.56, y + h * 0.30, 11),
                      (x + w * 0.78, y + h * 0.34, 9)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    # mine in water
    mx, my = x + w * 0.90, y + h * 0.90
    d.ellipse([mx - 6, my - 6, mx + 6, my + 6], fill=(26, 26, 26))
    for dx, dy in [(0, -9), (0, 9), (-9, 0), (9, 0)]:
        d.line([mx, my, mx + dx, my + dy], fill=(26, 26, 26), width=2)

def art_ulleung(d, x, y, w, h):
    """Ulleung Island: island, lighthouse, jets, warning triangle."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w * 0.78, y + 10, x + w * 0.78 + 34, y + 44], fill=(250, 220, 120))
    # sea
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(58, 110, 150))
    # island
    d.polygon([(x + w * 0.08, y + h * 0.72), (x + w * 0.30, y + h * 0.34),
               (x + w * 0.52, y + h * 0.72)], fill=(70, 130, 80))
    d.polygon([(x + w * 0.30, y + h * 0.34), (x + w * 0.42, y + h * 0.52),
               (x + w * 0.52, y + h * 0.72), (x + w * 0.38, y + h * 0.72)], fill=(52, 105, 62))
    # lighthouse
    lx = x + w * 0.30
    d.rectangle([lx - 4, y + h * 0.34, lx + 4, y + h * 0.52], fill=(255, 255, 255))
    d.rectangle([lx - 4, y + h * 0.40, lx + 4, y + h * 0.46], fill=(200, 60, 40))
    d.ellipse([lx - 6, y + h * 0.30, lx + 6, y + h * 0.36], fill=(250, 220, 120))
    # warning triangle
    tx, ty = x + w * 0.66, y + h * 0.42
    d.polygon([(tx, ty - 22), (tx + 22, ty + 14), (tx - 22, ty + 14)], fill=(245, 176, 65),
              outline=(26, 26, 26))
    d.text((tx - 3, ty - 12), "!", font=font("sans_b", 20), fill=(26, 26, 26))
    # two jets (delta silhouettes)
    for jx, jy, s in [(0.55, 0.16, 1.0), (0.72, 0.08, 0.8)]:
        px, py = x + w * jx, y + h * jy
        d.polygon([(px, py), (px + 34 * s, py + 6 * s), (px, py + 12 * s)], fill=(60, 64, 70))
        d.polygon([(px + 10 * s, py + 2 * s), (px + 22 * s, py - 6 * s), (px + 24 * s, py + 2 * s)],
                  fill=(60, 64, 70))
    # radar arcs
    for r in (14, 24, 34):
        d.arc([x + w * 0.88 - r, y + h * 0.78 - r, x + w * 0.88 + r, y + h * 0.78 + r],
              start=200, end=340, fill=(255, 255, 255), width=2)

def art_sanofi(d, x, y, w, h):
    """Paris + pharma: Eiffel Tower, pill, $41bn block."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 196))
    # sky band
    d.rectangle([x, y, x + w, y + h * 0.42], fill=SKY)
    d.ellipse([x + w * 0.80, y + 8, x + w * 0.80 + 30, y + 38], fill=(250, 220, 120))
    # Paris rooftops
    for i, bx in enumerate([0.02, 0.20, 0.38, 0.56, 0.74]):
        bh = [0.42, 0.34, 0.46, 0.36, 0.44][i]
        d.rectangle([x + w * bx, y + h * (0.72 - bh), x + w * (bx + 0.16), y + h * 0.72],
                    fill=(170, 150, 120))
        d.polygon([(x + w * bx, y + h * (0.72 - bh)), (x + w * (bx + 0.08), y + h * (0.72 - bh - 0.07)),
                   (x + w * (bx + 0.16), y + h * (0.72 - bh))], fill=(120, 100, 80))
    # Eiffel Tower (right)
    ex = x + w * 0.86
    d.polygon([(ex - 16, y + h * 0.72), (ex, y + h * 0.06), (ex + 16, y + h * 0.72)], fill=(90, 84, 70))
    d.polygon([(ex - 9, y + h * 0.72), (ex, y + h * 0.30), (ex + 9, y + h * 0.72)], fill=(232, 222, 196))
    d.rectangle([ex - 20, y + h * 0.68, ex + 20, y + h * 0.72], fill=(90, 84, 70))
    # big pill (capsule) lower left
    px, py = x + w * 0.06, y + h * 0.68
    d.rounded_rectangle([px, py, px + 96, py + 24], radius=12, fill=(200, 60, 40))
    d.rounded_rectangle([px + 48, py, px + 96, py + 24], radius=12, fill=(255, 255, 255))
    d.rectangle([px + 48, py, px + 52, py + 24], fill=(200, 60, 40))
    # $41bn block
    d.rectangle([x + w * 0.44, y + h * 0.68, x + w * 0.94, y + h * 0.94], fill=NAVY)
    d.text((x + w * 0.48, y + h * 0.71), "$41 BILLION", font=font("sans_b", 19), fill=(255, 255, 255))

HERO_ART = {1: art_hormuz, 2: art_ulleung, 3: art_sanofi}

# ---------------------------------------------------------------- small grid icons
def icon_chip(d, x, y, s, c):
    d.rectangle([x + 4, y + 4, x + s - 4, y + s - 4], fill=c)
    for i in range(3):
        d.line([x + 6 + i * 8, y, x + 6 + i * 8, y + 4], fill=c, width=2)
        d.line([x + 6 + i * 8, y + s - 4, x + 6 + i * 8, y + s], fill=c, width=2)
        d.line([x, y + 6 + i * 8, x + 4, y + 6 + i * 8], fill=c, width=2)
        d.line([x + s - 4, y + 6 + i * 8, x + s, y + 6 + i * 8], fill=c, width=2)
    d.rectangle([x + 10, y + 10, x + s - 10, y + s - 10], outline=(255, 255, 255), width=2)

def icon_building(d, x, y, s, c):
    d.rectangle([x + 6, y + 6, x + s - 6, y + s - 2], fill=c)
    d.polygon([(x + 4, y + 6), (x + s / 2, y), (x + s - 4, y + 6)], fill=c)
    for r in range(2):
        for col in range(3):
            d.rectangle([x + 9 + col * 7, y + 12 + r * 9, x + 13 + col * 7, y + 16 + r * 9],
                        fill=(255, 255, 255))

def icon_eu(d, x, y, s, c):
    d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], fill=(36, 113, 163))
    import math
    for i in range(8):
        a = math.pi * 2 * i / 8 - math.pi / 2
        d.ellipse([x + s / 2 + 8 * math.cos(a) - 1.5, y + s / 2 + 8 * math.sin(a) - 1.5,
                   x + s / 2 + 8 * math.cos(a) + 1.5, y + s / 2 + 8 * math.sin(a) + 1.5],
                  fill=(250, 220, 60))

def icon_warn(d, x, y, s, c):
    d.polygon([(x + s / 2, y + 2), (x + s - 2, y + s - 2), (x + 2, y + s - 2)], fill=(245, 176, 65),
              outline=INK)
    d.text((x + s / 2 - 3, y + 8), "!", font=font("sans_b", 16), fill=INK)

def icon_bottle(d, x, y, s, c):
    d.rectangle([x + s / 2 - 4, y + 2, x + s / 2 + 4, y + 8], fill=c)
    d.polygon([(x + s / 2 - 4, y + 8), (x + s / 2 + 4, y + 8), (x + s / 2 + 7, y + s - 2),
               (x + s / 2 - 7, y + s - 2)], fill=c)
    d.rectangle([x + s / 2 - 7, y + s / 2, x + s / 2 + 7, y + s / 2 + 5], fill=(255, 255, 255))

def icon_doc(d, x, y, s, c):
    d.rectangle([x + 7, y + 3, x + s - 7, y + s - 3], fill=(255, 255, 255), outline=c, width=2)
    for i in range(3):
        d.line([x + 11, y + 9 + i * 6, x + s - 11, y + 9 + i * 6], fill=c, width=2)
    d.ellipse([x + s - 14, y + s - 12, x + s - 4, y + s - 2], fill=RED)

def icon_cash(d, x, y, s, c):
    d.rectangle([x + 2, y + 8, x + s - 2, y + s - 8], fill=(30, 132, 73))
    d.ellipse([x + s / 2 - 6, y + s / 2 - 6, x + s / 2 + 6, y + s / 2 + 6],
              outline=(255, 255, 255), width=2)
    d.text((x + s / 2 - 3, y + s / 2 - 6), "$", font=font("sans_b", 11), fill=(255, 255, 255))

def icon_blast(d, x, y, s, c):
    burst(d, x + s / 2, y + s / 2, 11, (245, 176, 65))
    burst(d, x + s / 2, y + s / 2, 6, (220, 60, 30))

def icon_megaphone(d, x, y, s, c):
    d.polygon([(x + 4, y + 12), (x + 16, y + 6), (x + 16, y + 22), (x + 4, y + 16)], fill=c)
    d.rectangle([x + 16, y + 6, x + s - 2, y + 22], fill=c)
    d.rectangle([x + 6, y + 16, x + 12, y + s - 2], fill=c)

def icon_handshake(d, x, y, s, c):
    d.polygon([(x + 3, y + 14), (x + s / 2, y + 6), (x + s - 3, y + 14), (x + s / 2, y + 22)],
              fill=c)
    d.line([x + 3, y + 14, x + s - 3, y + 14], fill=(255, 255, 255), width=2)

def icon_wheat(d, x, y, s, c):
    d.line([x + s / 2, y + s - 2, x + s / 2, y + 4], fill=c, width=2)
    for i in range(4):
        yy = y + 6 + i * 6
        d.ellipse([x + s / 2 - 7, yy, x + s / 2 - 1, yy + 5], fill=(200, 160, 60))
        d.ellipse([x + s / 2 + 1, yy, x + s / 2 + 7, yy + 5], fill=(220, 180, 80))

def icon_mother(d, x, y, s, c):
    d.ellipse([x + s / 2 - 4, y + 3, x + s / 2 + 4, y + 11], fill=c)
    d.polygon([(x + s / 2 - 8, y + s - 2), (x + s / 2 - 5, y + 12), (x + s / 2 + 5, y + 12),
               (x + s / 2 + 8, y + s - 2)], fill=c)
    d.ellipse([x + s / 2 + 4, y + 16, x + s / 2 + 10, y + 22], fill=(245, 176, 65))

GRID_ICONS = {4: icon_chip, 5: icon_building, 6: icon_eu, 7: icon_warn,
              8: icon_bottle, 9: icon_doc, 10: icon_cash, 11: icon_blast,
              12: icon_megaphone, 13: icon_handshake, 14: icon_wheat, 15: icon_mother}

# ---------------------------------------------------------------- layout
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 24                      # outer margin
CW = W - 2 * MX              # content width = 976

def rule(y, w=2):
    d.line([MX, y, MX + CW, y], fill=RULE, width=w)

# ---- masthead ----
y = 14
d.text((MX, y), "THE WORLD IN ONE DAY", font=F_MAST, fill=INK)
rule(84)
y = 92
d.text((MX, y), "TUESDAY, 24 NOVEMBER 2026", font=F_DATE, fill=RED)
sub = "31 stories  ·  6 regions  ·  Research cutoff 08:30 UTC"
d.text((MX + CW - d.textlength(sub, font=F_SMALL), y + 16), sub, font=F_SMALL, fill=MUTED)
rule(138, 3)

# ---- THE DAY IN UTC strip ----
y = 146
d.rectangle([MX, y, MX + CW, y + 30], fill=NAVY)
d.text((MX + 10, y + 7), "THE DAY IN UTC", font=F_SECT, fill=(255, 255, 255))
d.text((MX + 190, y + 8), "clock times as reported (local time shown)", font=F_TINY,
       fill=(200, 215, 230))
# axis 00-24
ax0, ax1 = MX + 430, MX + CW - 12
d.line([ax0, y + 15, ax1, y + 15], fill=(255, 255, 255), width=1)
for hh in range(0, 25, 6):
    xx = ax0 + (ax1 - ax0) * hh / 24
    d.line([xx, y + 12, xx, y + 18], fill=(255, 255, 255), width=1)
    d.text((xx - 8, y + 19), f"{hh:02d}", font=F_TINY, fill=(200, 215, 230))
# markers: Hanoi 08:00 ICT = 01:00 UTC ; Ulleung 07:52 KST (local)
for frac, label in [(1 / 24, "01:00 UTC  HANOI BLAST"), (7.87 / 24, "07:52 KST  ULLEUNG ALERT")]:
    xx = ax0 + (ax1 - ax0) * frac
    d.ellipse([xx - 4, y + 11, xx + 4, y + 19], fill=(245, 176, 65), outline=(255, 255, 255))
    d.text((xx + 7, y + 1), label, font=F_TINY, fill=(255, 255, 255))

# ---- THE DAY IN NUMBERS ----
y = 186
d.text((MX, y), "THE DAY IN NUMBERS", font=F_SECT, fill=INK)
y = 204
bw = (CW - 6 * 8) / 7
for i, (num, lab) in enumerate(NUMBERS):
    bx = MX + i * (bw + 8)
    d.rectangle([bx, y, bx + bw, y + 46], fill=PANEL, outline=RULE, width=1)
    d.rectangle([bx, y, bx + bw, y + 3], fill=RED)
    nw = d.textlength(num, font=font("sans_b", 19))
    d.text((bx + (bw - nw) / 2, y + 7), num, font=font("sans_b", 19), fill=RED)
    for j, ln in enumerate(wrap(d, lab, F_TINY, bw - 8)):
        lw = d.textlength(ln, font=F_TINY)
        d.text((bx + (bw - lw) / 2, y + 29 + j * 10), ln, font=F_TINY, fill=MUTED)
        if j >= 1:
            break

# ---- heroes ----
y = 262
d.text((MX, y), "THE THREE STORIES THAT LED THE DAY", font=F_SECT, fill=INK)
y = 280
hw = (CW - 2 * 12) / 3
hh = 208
for i, st in enumerate(STORIES[:3]):
    n, region, head, summ, src, tag, lon, lat = st
    hx = MX + i * (hw + 12)
    d.rectangle([hx, y, hx + hw, y + hh], fill=PANEL, outline=RULE, width=1)
    # art panel
    HERO_ART[n](d, hx + 1, y + 1, hw - 2, 96)
    d.line([hx, y + 97, hx + hw, y + 97], fill=RULE, width=1)
    # number badge + region
    num_badge(d, hx + 16, y + 110, n, r=11)
    d.text((hx + 32, y + 103), REGION_SHORT[region], font=F_TINYB, fill=REGION_COLOR[region])
    # headline
    ty = draw_wrapped(d, hx + 10, y + 120, head, F_HERO_S, hw - 20, leading=20, max_lines=2)
    # summary
    ty = draw_wrapped(d, hx + 10, ty + 2, summ, F_BODY, hw - 20, leading=13, max_lines=2)
    # tags row at bottom
    ty2 = y + hh - 18
    w1 = pill(d, hx + 10, ty2, tag, GREEN if tag == "CONFIRMED" else GOLD)
    d.text((hx + 10 + w1 + 6, ty2 + 2), "Source: " + src, font=F_TINY, fill=MUTED)

# ---- grid #4-15 ----
y = 500
d.text((MX, y), "MORE OF THE DAY  —  STORIES 4 TO 15", font=F_SECT, fill=INK)
y = 518
gw = (CW - 3 * 10) / 4
gh = 62
for r in range(3):
    for c in range(4):
        st = STORIES[3 + r * 4 + c]
        n, region, head, summ, src, tag, lon, lat = st
        gx = MX + c * (gw + 10)
        gy = y + r * (gh + 8)
        d.rectangle([gx, gy, gx + gw, gy + gh], fill=PANEL, outline=RULE, width=1)
        # red banner with number + region
        d.rectangle([gx, gy, gx + gw, gy + 14], fill=RED)
        d.text((gx + 5, gy + 2), f"{n}  ·  {REGION_SHORT[region]}", font=F_TAG,
               fill=(255, 255, 255))
        # icon
        GRID_ICONS[n](d, gx + 5, gy + 20, 30, REGION_COLOR[region])
        # headline (2 lines) + source
        tx = gx + 42
        draw_wrapped(d, tx, gy + 19, head, F_GRID, gw - 48, leading=14, max_lines=2)
        d.text((tx, gy + gh - 13), src, font=F_TINY, fill=MUTED)

# ---- bottom: map (left) + ALSO list (right) ----
y = 724
map_x, map_y, map_w, map_h = MX, y, 470, 218
also_x = MX + 482
also_w = CW - 482
d.text((map_x, y), "WHERE IT HAPPENED", font=F_SECT, fill=INK)
d.text((also_x, y), "ALSO ON TUESDAY 24 NOVEMBER", font=F_SECT, fill=INK)
y = 742
# map frame
d.rectangle([map_x, y, map_x + map_w, y + map_h], fill=SEA, outline=RULE, width=1)
# graticule
for glon in range(-150, 181, 30):
    gx = map_x + (glon + 180) / 360 * map_w
    d.line([gx, y, gx, y + map_h], fill=(190, 205, 218), width=1)
for glat in (-30, 0, 30, 60):
    gy = y + (75 - glat) / 130 * map_h
    d.line([map_x, gy, map_x + map_w, gy], fill=(190, 205, 218), width=1)

def project(lon, lat):
    px = map_x + (lon + 180) / 360 * map_w
    py = y + (75 - lat) / 130 * map_h
    return px, py

for poly in CONTINENTS:
    pts = [project(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=LAND, outline=LAND_LN)

# dots at true positions + numbered labels with leader lines (greedy, min 18px apart)
placed = []
OFFSETS = [(16, -14), (18, 2), (14, 12), (-2, 16), (-20, 10), (-20, -8), (0, -18), (16, -22)]
for st in STORIES:
    n, region, head, summ, src, tag, lon, lat = st
    px, py = project(lon, lat)
    col = REGION_COLOR[region]
    # shared-city second dot: nudge the dot itself a touch
    if n in (5, 16, 26):
        px += 4
        py -= 4
    d.ellipse([px - 3.5, py - 3.5, px + 3.5, py + 3.5], fill=col, outline=(255, 255, 255))
    lx, ly = None, None
    for dx, dy in OFFSETS:
        cx, cy = px + dx, py + dy
        if not (map_x + 10 <= cx <= map_x + map_w - 10 and y + 10 <= cy <= y + map_h - 10):
            continue
        if all((cx - qx) ** 2 + (cy - qy) ** 2 >= 18 ** 2 for qx, qy in placed):
            lx, ly = cx, cy
            break
    if lx is None:
        lx, ly = px + 16, py - 14
    placed.append((lx, ly))
    d.line([px, py, lx, ly], fill=INK, width=1)
    num_badge(d, lx, ly, n, r=8, fill=col)
# map legend: region counts
ly = y + map_h + 6
for i, (name, cnt) in enumerate(REGION_COUNTS):
    lx = map_x + i * 79
    col = REGION_COLOR[{"N. AMERICA": "North America", "EUROPE": "Europe",
                        "MIDEAST": "Middle East", "AFRICA": "Africa",
                        "ASIA-PACIFIC": "Asia-Pacific", "LATIN AM.": "Latin America"}[name]]
    d.ellipse([lx, ly + 2, lx + 8, ly + 10], fill=col)
    d.text((lx + 11, ly), f"{name} {cnt}", font=F_TINY, fill=INK)

# ALSO list #16-31 (16 stories, 2 columns x 8) — one-line short titles
SHORT = {16: "1 in 6 pregnancies in Africa to teens", 17: "Fighting traps Ebola teams in Ituri",
         18: "Qatar condemns Khartoum drone attacks", 19: "Hanoi blast kills 6, injures 10",
         20: "5.6 quake hits Nepal near Tibet", 21: "Japan speeds ICC funding amid sanctions",
         22: "Australia to fine tech firms up to 5%", 23: "Hasina plans return to Bangladesh",
         24: "China names Shenzhou-24 crew", 25: "Manila court orders Atong Ang arrest",
         26: "Japan cuts consumer spending view", 27: "Car bomb in Villavicencio injures 23",
         28: "Mexico to try 'El Chapo Isidro' at home", 29: "WHO chief visits Cuba amid health crisis",
         30: "Man rescued after 11 days in Amazon", 31: "Migrant caravan crosses into Mexico"}
cols = [STORIES[15:23], STORIES[23:31]]
for ci, col in enumerate(cols):
    cx = also_x + ci * (also_w / 2 + 6)
    cw2 = also_w / 2 - 6
    yy = y
    for st in col:
        n, region, head, summ, src, tag, lon, lat = st
        d.text((cx, yy), f"{n}.", font=F_TINYB, fill=RED)
        d.text((cx + 18, yy), SHORT[n], font=F_GRID_S, fill=INK)
        yy += 13
        d.text((cx + 18, yy), f"{REGION_SHORT[region]} · {src}", font=F_TINY, fill=MUTED)
        yy += 15

# ---- DATE CHECK bar ----
y = 986
d.rectangle([MX, y, MX + CW, y + 20], fill=(240, 228, 200), outline=RULE, width=1)
d.text((MX + 8, y + 4), "DATE CHECK — left out, wrong date:", font=F_TINYB, fill=RED)
dtxt = "Nvidia/Huang +31% (23 Nov) · COP31 collapse (23 Nov) · Merkury sinking (22–23 Nov) · SoftBank–Intel $2B (Aug 2025) · CAS Senegal ruling (not yet decided)"
d.text((MX + 8 + d.textlength("DATE CHECK — left out, wrong date:  ", font=F_TINYB), y + 4),
       dtxt, font=F_TINY, fill=INK)

# ---- footer ----
y = 1009
draw_wrapped(d, MX, y, "Every story above happened or was first reported on Tuesday 24 November 2026.  "
                "CONFIRMED = the event happened that day; REPORTED = first reported that day.  "
                "Sources: Reuters, AFP, AP, Al Jazeera, El Tiempo, WFP, WHO, Africa CDC.",
       F_TINY, CW, fill=MUTED, leading=11, max_lines=2)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
