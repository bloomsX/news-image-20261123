#!/usr/bin/env python3
"""Render the front page for Monday 23 November 2026.

v2 infographic style from news-image-20261122 (3 big illustrated lead
panels, 10 small drawn panels, big-number stats strip, numbered-pin map,
DATE CHECK box, per-story source tags) plus the UTC timeline strip the
skill requires. 55 verified stories: 3 leads + 10 small + 42 ALSO.
Every story happened, or was first reported, on 23 Nov 2026; Tier B
items carry a 23 Nov development. Items that fail the gate are named in
the DATE CHECK box and appear nowhere on the page.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (255, 255, 255)
INK = (17, 17, 17)
MUTE = (96, 96, 96)
RED = (178, 0, 0)
RULE = (198, 198, 198)
GRID = (228, 228, 228)
LAND = (236, 236, 236)
LANDLINE = (200, 200, 200)
CREAM = (250, 246, 236)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


DAY = "MONDAY  ·  23 NOVEMBER 2026"
TITLE = "THE WORLD TODAY"

# ------------------------------------------------------------------ data

# (number, place, field, headline, detail, source, scene, sky, region)
LEADS = [
    (1, "BELÉM, BRAZIL", "CLIMATE",
     "COP31 collapses — no deal",
     "COP31 ends without agreement in Belém; talks break down. (BBC)",
     "summit", (178, 216, 230), "GL"),
    (2, "WASHINGTON", "POLITICS",
     "Democrats take the House, 258–177",
     "Democrats win 258 seats and take both chambers of Congress. (BBC)",
     "ballot", (220, 228, 240), "NA"),
    (3, "TOKYO", "MARKETS",
     "Nikkei −5.06% as AI sell-off spreads",
     "Japan's Nikkei dives; KOSPI halts, Taiwan swings 1,578 pts. "
     "(SimpleLife)",
     "chart_down", (24, 28, 40), "AS"),
]

# (number, place, field, headline, source, scene, sky, region)
SMALL = [
    (4, "BENGHAZI, LIBYA", "WAR",
     "Frigate Merkury sinks off Benghazi", "WSJ",
     "sea_fire", (40, 48, 74), "AF"),
    (5, "DYMER, UKRAINE", "WAR",
     "Russian strikes kill 12 in Kyiv region", "Reuters",
     "rubble", (58, 58, 66), "EU"),
    (6, "SAUDI ARABIA", "WAR",
     "Houthis claim Saudi refinery strikes", "Ind. Express",
     "refinery", (48, 40, 52), "ME"),
    (7, "ZURICH", "SPORT",
     "FIFA confirms UK as 2035 hosts", "BBC",
     "ballot", (220, 228, 240), "EU"),
    (8, "TAIPEI", "MARKETS",
     "Taiwan stocks swing 1,578 points", "SimpleLife",
     "chart_down", (24, 28, 40), "AS"),
    (9, "SEOUL", "MARKETS",
     "Korea exports top $1T, a first", "SimpleLife",
     "chart_up", (235, 232, 210), "AS"),
    (10, "VANUATU", "DISASTER",
     "M6.5 quake strikes Vanuatu", "USGS",
     "quake", (140, 190, 220), "OC"),
    (11, "NEW DELHI", "POLITICS",
     "Nepal PM begins India visit", "NewsBites",
     "flags", (200, 216, 235), "AS"),
    (12, "NEW YORK", "CULTURE",
     "ATEEZ tops Billboard 200", "Yonhap",
     "stage", (30, 30, 46), "AS"),
    (13, "CANBERRA", "ECONOMY",
     "Jobless to top 5%, Chalmers warns", "Reuters",
     "parliament", (225, 232, 238), "OC"),
]

# (number, region, headline, source) — short headlines only
ALSO = [
    (14, "AS", "Taiwan bans short selling", "CNA"),
    (15, "AS", "KOSPI below 4,700, trading halts", "SL"),
    (16, "AS", "HK tech at 19-month low", "SL"),
    (17, "AS", "Sensex falls; Nifty −0.65%", "Rtr"),
    (18, "GL", "Brent crude $89.53", "IM"),
    (19, "AS", "India–China open border talks", "NB"),
    (20, "EU", "French students plan protests", "MEye"),
    (21, "EU", "Bulgari dies aged 89", "BBC"),
    (22, "AS", "IND–NZ Test Day 5 live", "ESPN"),
    (23, "EU", "FIDE: Sindarov takes White", "CC"),
    (24, "EU", "Pochettino's Utd thrashed 4–0", "Rtr"),
    (25, "EU", "U2 album debuts at No. 4", "Var"),
    (26, "AS", "Syed Modi badminton Tue", "ESPN"),
    (27, "EU", "Vyshneve strike kills 2 at shop", "QNA"),
    (28, "EU", "Bila Tserkva home strike kills 1", "QNA"),
    (29, "EU", "Dnipropetrovsk substation hit", "AFP"),
    (30, "AS", "Banten: 24 dead, 34 missing", "Rtr"),
    (31, "EU", "Poland: Russian missiles", "BBC"),
    (32, "ME", "US hawks urge Iran strikes", "FT"),
    (33, "NA", "Trump backs Huang on Nvidia", "FT"),
    (34, "AS", "Tai Po fire: one year on", "SCMP"),
    (35, "EU", "Burnham to tell MPs of EU deal", "BBC"),
    (36, "NA", "US probes spy tied to Nvidia", "Bbg"),
    (37, "ME", "Hamas seeks Gaza talks", "AA"),
    (38, "ME", "Gaza truce toll: 1,662 killed", "HM"),
    (39, "EU", "Kerch Bridge hit again", "NE"),
    (40, "AS", "Delhi air hazardous, AQI 324", "WC"),
    (41, "LA", "Venezuela talks extended", "LO"),
    (42, "LA", "US–Venezuela military deal", "BBC"),
    (43, "OC", "Qantas to axe 850 jobs", "CG"),
    (44, "OC", "Albanese: $25 script cap", "FNN"),
    (45, "OC", "RBA: tax may fuel inflation", "FNN"),
    (46, "OC", "Lendlease: no new shares", "FNN"),
    (47, "OC", "BHP's new boss backs nuclear", "FNN"),
    (48, "OC", "ALS drops 11% on Mideast hit", "FNN"),
    (49, "OC", "Olympian Henke dies at 99", "ABC"),
    (50, "OC", "PNG Chiefs sign star Young", "Cour"),
    (51, "OC", "Melbourne stabbings charged", "Age"),
    (52, "OC", "Fire-ant nest found in Sydney", "Age"),
    (53, "OC", "Singapore PM lands in Sydney", "Gdn"),
    (54, "AS", "Korea Speaker starts Japan trip", "KT"),
    (55, "OC", "COP31 'a disaster for Pacific'", "ABC"),
]

# (big number, label)
STATS = [
    ("−5.06%", "Nikkei falls"),
    ("258", "Democrat House seats"),
    ("$1T", "Korea exports, first time"),
    ("12", "killed in Kyiv region"),
    ("6.5", "Vanuatu quake"),
    ("1,578", "points, Taiwan swing"),
]

# UTC timeline: (time label, event)
TIMELINE = [
    ("02:40", "Vanuatu M6.5"),
    ("03:49", "Dymer toll 12"),
    ("06:00", "Nikkei −5.06%"),
    ("06:16", "Sensex slides"),
    ("TODAY", "COP31 collapses"),
]

REGION_BAR = [
    ("EUROPE", 13, (32, 56, 100)),
    ("MIDDLE EAST", 4, (178, 0, 0)),
    ("ASIA", 16, (220, 120, 0)),
    ("AFRICA", 1, (46, 125, 50)),
    ("N AMERICA", 3, (15, 76, 117)),
    ("LATAM", 2, (106, 27, 154)),
    ("OCEANIA", 14, (0, 105, 92)),
    ("GLOBAL", 2, (96, 96, 96)),
]

# Rough continent outlines, (lon, lat) points, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-95, 80), (-75, 73), (-60, 60),
     (-55, 47), (-70, 42), (-80, 32), (-80, 25), (-90, 20), (-97, 16),
     (-105, 20), (-117, 32), (-125, 48), (-150, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-50, -30),
     (-60, -40), (-70, -52), (-73, -40), (-72, -20), (-78, -5)],
    [(-17, 15), (-10, 30), (-5, 35), (10, 37), (30, 31), (43, 12),
     (51, 11), (40, -5), (35, -20), (25, -33), (18, -35), (12, -18),
     (9, 4), (-8, 5)],
    [(-10, 36), (-5, 44), (5, 48), (15, 44), (25, 40), (35, 36),
     (45, 42), (55, 50), (65, 68), (85, 75), (110, 74), (140, 72),
     (170, 66), (175, 62), (160, 55), (145, 40), (130, 33), (120, 25),
     (108, 12), (100, 8), (95, 16), (85, 20), (75, 10), (65, 25),
     (55, 27), (48, 30), (40, 36), (30, 36), (20, 40), (10, 38)],
    [(114, -22), (114, -33), (124, -33), (132, -32), (140, -38),
     (150, -37), (153, -27), (146, -19), (142, -11), (135, -12),
     (129, -14), (122, -17)],
]

# story number, lon, lat, label offset (dx, dy)
PINS = [
    (1, -48.5, -1.4, (6, -8)),    # Belém
    (2, -77.0, 38.9, (6, -8)),    # Washington
    (3, 139.7, 35.7, (6, -8)),    # Tokyo
    (4, 20.1, 32.1, (6, 2)),      # Benghazi
    (5, 30.3, 51.0, (6, -8)),     # Dymer
    (6, 46.7, 24.7, (6, -8)),     # Riyadh
    (7, 8.5, 47.4, (6, -8)),      # Zurich
    (8, 121.5, 25.0, (6, -8)),    # Taipei
    (9, 127.0, 37.5, (6, -8)),    # Seoul
    (10, 168.3, -17.7, (6, 2)),   # Port Vila
    (11, 77.2, 28.6, (6, -8)),    # New Delhi
    (12, -74.0, 40.7, (-16, -8)),  # New York (Billboard)
    (13, 149.1, -35.3, (-18, -8)),  # Canberra
]

REGION_SHORT = {
    "EU": "Europe", "ME": "Mideast", "AS": "Asia", "AF": "Africa",
    "NA": "N America", "LA": "LatAm", "OC": "Oceania", "GL": "Global",
}


def story_count():
    return len(LEADS) + len(SMALL) + len(ALSO)


def region_counts():
    counts = {}
    for lead in LEADS:
        counts[lead[7]] = counts.get(lead[7], 0) + 1
    for s in SMALL:
        counts[s[7]] = counts.get(s[7], 0) + 1
    for _n, region, _h, _s in ALSO:
        counts[region] = counts.get(region, 0) + 1
    return counts

# ------------------------------------------------------------- scenes


def _flame(d, x, y, s, cols=((255, 122, 26), (255, 180, 0), (255, 224, 80))):
    d.polygon([(x, y), (x - s * 0.55, y - s * 0.9), (x - s * 0.2, y - s * 0.5),
               (x + s * 0.15, y - s * 1.25), (x + s * 0.45, y - s * 0.55),
               (x + s * 0.6, y - s * 0.85), (x + s * 0.55, y)],
              fill=cols[0])
    d.polygon([(x - s * 0.25, y), (x - s * 0.1, y - s * 0.6),
               (x + s * 0.15, y - s * 0.8), (x + s * 0.28, y)],
              fill=cols[1])


def _smoke(d, x, y, s, col=(180, 180, 180)):
    for i, r in enumerate((s * 0.28, s * 0.36, s * 0.44)):
        d.ellipse([x - r + i * s * 0.18, y - s * (0.5 + i * 0.55) - r,
                   x + r + i * s * 0.18, y - s * (0.5 + i * 0.55) + r],
                  fill=col)


def _waves(d, x0, y0, x1, y1, col, step=16):
    for yy in range(y0, y1, 12):
        for xx in range(x0, x1, step):
            d.arc([xx, yy, xx + step, yy + 10], 180, 360, fill=col, width=2)


def _person(d, x, y, s, shirt, skin=(214, 170, 130)):
    d.ellipse([x - s * 0.32, y - s * 1.05, x + s * 0.32, y - s * 0.45],
              fill=skin)
    d.rounded_rectangle([x - s * 0.42, y - s * 0.45, x + s * 0.42, y + s * 0.55],
                        radius=int(s * 0.15), fill=shirt)


def _flagpole(d, x, y0, y1, col, w=26):
    d.line([(x, y0), (x, y1)], fill=(60, 60, 60), width=2)
    d.polygon([(x, y0), (x + w, y0 + 5), (x, y0 + 11)], fill=col)


def scene_summit(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0 + h * 0.62, x1, y0 + h * 0.72], fill=(120, 82, 50))
    d.rectangle([x0, y0 + h * 0.72, x1, y0 + h * 0.78], fill=(90, 60, 36))
    for i, shirt in enumerate(((32, 56, 100), (178, 0, 0), (46, 125, 50),
                               (220, 120, 0), (106, 27, 154))):
        cx = x0 + w * (0.12 + i * 0.19)
        _person(d, cx, y0 + h * 0.62, h * 0.16, shirt)
    gx, gy, gr = x0 + w * 0.85, y0 + h * 0.52, h * 0.14
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(32, 90, 160))
    d.ellipse([gx - gr * 0.5, gy - gr * 0.7, gx + gr * 0.3, gy + gr * 0.2],
              fill=(46, 160, 90))
    cx, cy, cr = x0 + w * 0.14, y0 + h * 0.22, h * 0.13
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255),
              outline=INK, width=2)
    d.line([(cx, cy), (cx, cy - cr * 0.6)], fill=INK, width=2)
    d.line([(cx, cy), (cx + cr * 0.5, cy)], fill=INK, width=2)


def scene_sea_fire(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0 + h * 0.6, x1, y1], fill=(16, 42, 84))
    _waves(d, x0 + 4, y0 + int(h * 0.68), x1 - 4, y1 - 4, (120, 170, 220))
    d.rectangle([x0 + w * 0.15, y0 + h * 0.45, x0 + w * 0.85, y0 + h * 0.62],
                fill=(40, 40, 44))
    for i, col in enumerate(((178, 0, 0), (220, 120, 0), (32, 56, 100))):
        d.rectangle([x0 + w * (0.2 + i * 0.2), y0 + h * 0.28,
                     x0 + w * (0.36 + i * 0.2), y0 + h * 0.45], fill=col)
    _flame(d, x0 + w * 0.3, y0 + h * 0.32, h * 0.16)
    _flame(d, x0 + w * 0.68, y0 + h * 0.32, h * 0.13)
    _smoke(d, x0 + w * 0.3, y0 + h * 0.3, h * 0.14, (120, 120, 130))


def scene_ballot(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    for i, hh in enumerate((0.5, 0.75, 0.6, 0.9, 0.65)):
        bx = x0 + w * (0.02 + i * 0.19)
        d.rectangle([bx, y0 + h * (1 - hh), bx + w * 0.15, y1],
                    fill=(170, 182, 196))
    bx0, by0 = x0 + w * 0.36, y0 + h * 0.45
    d.rectangle([bx0, by0, bx0 + w * 0.28, y1 - 2], fill=(178, 0, 0))
    d.rectangle([bx0 - w * 0.02, by0 - h * 0.06, bx0 + w * 0.30, by0],
                fill=(140, 0, 0))
    d.line([(bx0 + w * 0.08, by0 - h * 0.02), (bx0 + w * 0.2, by0 - h * 0.02)],
           fill=(255, 255, 255), width=3)
    d.rectangle([bx0 + w * 0.1, y0 + h * 0.18, bx0 + w * 0.18, by0 - h * 0.06],
                fill=(255, 255, 255), outline=INK, width=1)
    d.line([(bx0 + w * 0.06, y0 + h * 0.62), (bx0 + w * 0.12, y0 + h * 0.72),
            (bx0 + w * 0.22, y0 + h * 0.55)], fill=(255, 255, 255), width=3)
    _person(d, x0 + w * 0.82, y0 + h * 0.72, h * 0.16, (32, 56, 100))


def scene_flags(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0 + h * 0.78, x1, y1], fill=(120, 150, 110))
    _flagpole(d, x0 + w * 0.25, y0 + h * 0.18, y0 + h * 0.78, (32, 56, 100))
    d.ellipse([x0 + w * 0.25 + 12, y0 + h * 0.22, x0 + w * 0.25 + 20,
               y0 + h * 0.30], fill=(255, 255, 255))
    _flagpole(d, x0 + w * 0.6, y0 + h * 0.18, y0 + h * 0.78, (220, 220, 220))
    d.rectangle([x0 + w * 0.6, y0 + h * 0.18, x0 + w * 0.6 + 26,
                 y0 + h * 0.26], fill=(220, 220, 220))
    d.rectangle([x0 + w * 0.6, y0 + h * 0.26, x0 + w * 0.6 + 26,
                 y0 + h * 0.34], fill=(220, 40, 40))


def scene_chart(d, box, up=False, col=(255, 60, 60)):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    vals = (0.35, 0.5, 0.42, 0.62, 0.55, 0.75) if up else (0.75, 0.62, 0.7, 0.5, 0.58, 0.35)
    bw = w * 0.11
    for i, v in enumerate(vals):
        bx = x0 + w * (0.08 + i * 0.15)
        d.rectangle([bx, y1 - h * v - 4, bx + bw, y1 - 4],
                    fill=(90, 110, 150) if up else (140, 140, 150))
    pts = [(x0 + w * (0.13 + i * 0.15), y1 - h * v - 4) for i, v in enumerate(vals)]
    d.line(pts, fill=col, width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)
    d.line([(x0 + 6, y0 + 8), (x0 + 6, y1 - 4), (x1 - 6, y1 - 4)],
           fill=(200, 200, 200), width=2)


def scene_rubble(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0 + h * 0.78, x1, y1], fill=(70, 66, 60))
    # standing block
    d.rectangle([x0 + w * 0.08, y0 + h * 0.3, x0 + w * 0.42, y0 + h * 0.78],
                fill=(150, 142, 130))
    for i in range(3):
        for j in range(2):
            d.rectangle([x0 + w * (0.14 + i * 0.1), y0 + h * (0.38 + j * 0.18),
                         x0 + w * (0.2 + i * 0.1), y0 + h * (0.48 + j * 0.18)],
                        fill=(90, 84, 76))
    # collapsed block, sheared top
    d.polygon([(x0 + w * 0.5, y0 + h * 0.78), (x0 + w * 0.5, y0 + h * 0.45),
               (x0 + w * 0.68, y0 + h * 0.55), (x0 + w * 0.88, y0 + h * 0.5),
               (x0 + w * 0.92, y0 + h * 0.78)], fill=(120, 112, 100))
    # rubble triangles at the base
    for cx, s in ((0.55, 0.12), (0.72, 0.16), (0.88, 0.1)):
        d.polygon([(x0 + w * (cx - s), y0 + h * 0.78),
                   (x0 + w * cx, y0 + h * (0.78 - s * 0.8)),
                   (x0 + w * (cx + s), y0 + h * 0.78)], fill=(100, 94, 84))
    _smoke(d, x0 + w * 0.68, y0 + h * 0.5, h * 0.13, (200, 200, 200))
    _smoke(d, x0 + w * 0.25, y0 + h * 0.3, h * 0.11, (210, 210, 210))


def scene_refinery(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0 + h * 0.72, x1, y1], fill=(52, 44, 40))
    # towers
    for i, (tx, tw, th) in enumerate(((0.12, 0.14, 0.55), (0.38, 0.18, 0.68),
                                      (0.66, 0.12, 0.5))):
        d.rectangle([x0 + w * tx, y0 + h * (1 - th) - h * 0.06,
                     x0 + w * (tx + tw), y0 + h * 0.72], fill=(120, 116, 108))
        d.rectangle([x0 + w * tx, y0 + h * (1 - th) - h * 0.12,
                     x0 + w * (tx + tw), y0 + h * (1 - th) - h * 0.06],
                    fill=(150, 146, 138))
    # pipes between towers
    d.line([(x0 + w * 0.26, y0 + h * 0.55), (x0 + w * 0.38, y0 + h * 0.55)],
           fill=(90, 86, 80), width=3)
    d.line([(x0 + w * 0.56, y0 + h * 0.6), (x0 + w * 0.66, y0 + h * 0.6)],
           fill=(90, 86, 80), width=3)
    _flame(d, x0 + w * 0.47, y0 + h * 0.3, h * 0.16)
    _flame(d, x0 + w * 0.72, y0 + h * 0.42, h * 0.11)
    _smoke(d, x0 + w * 0.19, y0 + h * 0.35, h * 0.12, (170, 170, 175))


def scene_quake(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0 + h * 0.7, x1, y1], fill=(110, 96, 70))
    # cracked ground
    d.line([(x0, y0 + h * 0.7), (x0 + w * 0.3, y0 + h * 0.78),
            (x0 + w * 0.45, y0 + h * 0.72), (x0 + w * 0.7, y0 + h * 0.82),
            (x1, y0 + h * 0.74)], fill=(60, 50, 36), width=3)
    # tilted building
    d.polygon([(x0 + w * 0.14, y0 + h * 0.7), (x0 + w * 0.12, y0 + h * 0.38),
               (x0 + w * 0.34, y0 + h * 0.42), (x0 + w * 0.36, y0 + h * 0.7)],
              fill=(170, 160, 145))
    d.polygon([(x0 + w * 0.55, y0 + h * 0.7), (x0 + w * 0.57, y0 + h * 0.5),
               (x0 + w * 0.75, y0 + h * 0.48), (x0 + w * 0.73, y0 + h * 0.7)],
              fill=(150, 140, 125))
    # seismograph trace
    pts = [(x0 + w * (0.06 + i * 0.055),
            y0 + h * (0.22 + (0.06 if i % 3 else -0.05) * (1 if i % 2 else -1)))
           for i in range(16)]
    d.line(pts, fill=(178, 0, 0), width=2)


def scene_stage(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # spotlight cone
    d.polygon([(x0 + w * 0.5, y0), (x0 + w * 0.2, y1),
               (x0 + w * 0.8, y1)], fill=(60, 60, 90))
    d.polygon([(x0 + w * 0.5, y0), (x0 + w * 0.35, y1),
               (x0 + w * 0.65, y1)], fill=(90, 90, 130))
    # mic on stand
    mx = x0 + w * 0.5
    d.line([(mx, y0 + h * 0.45), (mx, y1 - 2)], fill=(200, 200, 200), width=3)
    d.ellipse([mx - h * 0.11, y0 + h * 0.22, mx + h * 0.11, y0 + h * 0.45],
              fill=(220, 220, 225), outline=(255, 255, 255), width=1)
    # stars
    for sx, sy, s in ((0.18, 0.25, 5), (0.82, 0.3, 6), (0.68, 0.14, 4)):
        cx, cy = x0 + w * sx, y0 + h * sy
        d.polygon([(cx, cy - s), (cx + s * 0.3, cy - s * 0.3),
                   (cx + s, cy), (cx + s * 0.3, cy + s * 0.3),
                   (cx, cy + s), (cx - s * 0.3, cy + s * 0.3),
                   (cx - s, cy), (cx - s * 0.3, cy - s * 0.3)],
                  fill=(255, 215, 0))


def scene_parliament(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0 + h * 0.72, x1, y1], fill=(150, 160, 130))
    # pediment + columns
    d.polygon([(x0 + w * 0.1, y0 + h * 0.42), (x0 + w * 0.5, y0 + h * 0.18),
               (x0 + w * 0.9, y0 + h * 0.42)], fill=(200, 200, 195))
    for i in range(5):
        cx = x0 + w * (0.16 + i * 0.17)
        d.rectangle([cx - w * 0.03, y0 + h * 0.44, cx + w * 0.03, y0 + h * 0.72],
                    fill=(235, 235, 230))
    d.rectangle([x0 + w * 0.08, y0 + h * 0.42, x0 + w * 0.92, y0 + h * 0.46],
                fill=(180, 180, 175))
    d.rectangle([x0 + w * 0.08, y0 + h * 0.72, x0 + w * 0.92, y0 + h * 0.76],
                fill=(180, 180, 175))
    # flag on top
    d.line([(x0 + w * 0.5, y0 + h * 0.18), (x0 + w * 0.5, y0 + h * 0.04)],
           fill=(60, 60, 60), width=2)
    d.polygon([(x0 + w * 0.5, y0 + h * 0.04), (x0 + w * 0.5 + 22, y0 + h * 0.09),
               (x0 + w * 0.5, y0 + h * 0.14)], fill=(32, 56, 100))


SCENES = {
    "summit": scene_summit,
    "sea_fire": scene_sea_fire,
    "ballot": scene_ballot,
    "flags": scene_flags,
    "chart_down": lambda d, b: scene_chart(d, b, up=False),
    "chart_up": lambda d, b: scene_chart(d, b, up=True, col=(30, 140, 60)),
    "rubble": scene_rubble,
    "refinery": scene_refinery,
    "quake": scene_quake,
    "stage": scene_stage,
    "parliament": scene_parliament,
}


# ------------------------------------------------------------- helpers

def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_also(d, num, region, head, src, max_w):
    """Fit one ALSO row into max_w: full text, else drop source, else truncate."""
    font = f(SANS, 9)
    full = f"{num} {region} {head} ({src})"
    if d.textlength(full, font=font) <= max_w:
        return full
    nosrc = f"{num} {region} {head}"
    if d.textlength(nosrc, font=font) <= max_w:
        return nosrc
    prefix = f"{num} {region} "
    avail = max_w - d.textlength(prefix + "…", font=font)
    txt = head
    while txt and d.textlength(txt, font=font) > avail:
        txt = txt[:-1].rstrip()
    return prefix + txt + "…"


def draw_map(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    def px(lon, lat):
        return x0 + (lon + 180.0) / 360.0 * w, y0 + (85.0 - lat) / 145.0 * h

    for cont in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in cont], fill=LAND,
                  outline=LANDLINE)
    for num, lon, lat, (dx, dy) in PINS:
        cx, cy = px(lon, lat)
        r = 9
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 255, 255), width=1)
        d.text((cx, cy), str(num), font=f(SANS_B, 9), fill=(255, 255, 255),
               anchor="mm")


def render(out="entry.png"):
    n = story_count()
    counts = region_counts()
    assert n == 55, n
    assert sum(counts.values()) == 55
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M = 28
    CW = W - 2 * M

    # masthead
    d.text((M, 10), TITLE, font=f(SERIF_B, 52), fill=INK)
    d.text((W - M, 22), DAY, font=f(SANS_B, 18), fill=RED, anchor="ra")
    d.rectangle([M, 88, W - M, 91], fill=RED)
    d.text((M, 96), "55 STORIES  ·  7 REGIONS  ·  12 FIELDS  ·  EVERY STORY "
           "DATE-CHECKED TO TODAY", font=f(SANS_B, 12), fill=INK)
    d.text((W - M, 96), "PAGE 1 OF 1", font=f(SANS, 11), fill=MUTE, anchor="ra")
    d.text((M, 114), "ALL 55 STORIES DATE-CHECKED TO MONDAY 23 NOVEMBER 2026",
           font=f(SANS_B, 11), fill=RED)
    d.line([(M, 132), (W - M, 132)], fill=RULE, width=1)

    # stats strip
    sy = 138
    cell = CW // 6
    for i, (num, label) in enumerate(STATS):
        x = M + i * cell
        d.text((x + cell // 2, sy + 2), num, font=f(SANS_B, 26), fill=RED,
               anchor="ma")
        lines = wrap(d, label, f(SANS, 9), cell - 10)
        for j, ln in enumerate(lines):
            d.text((x + cell // 2, sy + 30 + j * 11), ln, font=f(SANS, 9),
                   fill=MUTE, anchor="ma")
        if i:
            d.line([(x, sy + 4), (x, sy + 44)], fill=GRID, width=1)
    d.line([(M, 186), (W - M, 186)], fill=RULE, width=1)

    # UTC timeline band
    ty = 192
    d.rectangle([M, ty, W - M, ty + 26], fill=CREAM, outline=RULE)
    d.text((M + 8, ty + 7), "THE DAY IN UTC", font=f(SANS_B, 11), fill=RED)
    tx = M + 132
    for i, (t, ev) in enumerate(TIMELINE):
        seg = f"{t}  {ev}"
        if i:
            d.text((tx, ty + 7), "·", font=f(SANS_B, 11), fill=MUTE)
            tx += 14
        d.text((tx, ty + 7), t, font=f(SANS_B, 11), fill=INK)
        tx += d.textlength(t + "  ", font=f(SANS_B, 11))
        d.text((tx, ty + 7), ev, font=f(SANS, 11), fill=INK)
        tx += d.textlength(ev + "   ", font=f(SANS, 11))
    d.line([(M, ty + 32), (W - M, ty + 32)], fill=RULE, width=1)

    # big panels (leads)
    by = 224
    bw = (CW - 2 * 12) // 3
    bh = 196
    for i, (num, place, field, head, detail, scene, sky, _reg) in enumerate(LEADS):
        x = M + i * (bw + 12)
        d.rectangle([x, by, x + bw, by + 102], fill=sky)
        SCENES[scene](d, (x, by, x + bw, by + 102))
        d.ellipse([x + 8, by + 8, x + 32, by + 32], fill=RED)
        d.text((x + 20, by + 20), str(num), font=f(SANS_B, 13),
               fill=(255, 255, 255), anchor="mm")
        d.text((x, by + 110), f"{place} · {field}", font=f(SANS_B, 10), fill=RED)
        for j, ln in enumerate(wrap(d, head, f(SANS_B, 19), bw)):
            d.text((x, by + 124 + j * 22), ln, font=f(SANS_B, 19), fill=INK)
        for j, ln in enumerate(wrap(d, detail, f(SANS, 11), bw)):
            d.text((x, by + 170 + j * 14), ln, font=f(SANS, 11), fill=MUTE)
    d.line([(M, by + bh + 6), (W - M, by + bh + 6)], fill=RULE, width=1)

    # small panels, 2 rows x 5
    sy2 = by + bh + 14
    sw = (CW - 4 * 8) // 5
    sh = 132
    for row in range(2):
        for col in range(5):
            s = SMALL[row * 5 + col]
            num, place, field, head, src, scene, sky, _reg = s
            x = M + col * (sw + 8)
            y = sy2 + row * (sh + 8)
            d.rectangle([x, y, x + sw, y + 60], fill=sky)
            SCENES[scene](d, (x, y, x + sw, y + 60))
            d.ellipse([x + 5, y + 5, x + 25, y + 25], fill=RED)
            d.text((x + 15, y + 15), str(num), font=f(SANS_B, 11),
                   fill=(255, 255, 255), anchor="mm")
            d.text((x, y + 66), f"{place} · {field}", font=f(SANS_B, 9), fill=RED)
            for j, ln in enumerate(wrap(d, head, f(SANS_B, 13), sw)[:2]):
                d.text((x, y + 80 + j * 15), ln, font=f(SANS_B, 13), fill=INK)
            d.text((x, y + sh - 12), f"Source: {src}", font=f(SANS, 9), fill=MUTE)
    bottom_small = sy2 + 2 * sh + 8
    d.line([(M, bottom_small + 4), (W - M, bottom_small + 4)], fill=RULE, width=1)

    # bottom band: map left, also-list right (3 columns)
    by2 = bottom_small + 12
    d.text((M, by2), "WHERE IT HAPPENED — STORIES 1–13", font=f(SANS_B, 12), fill=INK)
    d.text((M + 356, by2), "ALSO ON MONDAY 23 NOVEMBER — 42 MORE STORIES",
           font=f(SANS_B, 12), fill=INK)
    map_box = (M, by2 + 18, M + 340, 956)
    d.rectangle(map_box, fill=(244, 246, 248), outline=GRID)
    draw_map(d, map_box)
    # region bar under the map
    rb_y = 962
    bx = M
    for name, cnt, col in REGION_BAR:
        seg = int(340 * cnt / 55)
        d.rectangle([bx, rb_y, bx + seg - 1, rb_y + 10], fill=col)
        bx += seg
    d.text((M, rb_y + 14), "EUROPE 13 · ASIA 16 · OCEANIA 14 · MIDEAST 4 · "
           "N AMERICA 3 · LATAM 2 · AFRICA 1 · GLOBAL 2",
           font=f(SANS_B, 9), fill=INK)

    # also-list, 3 columns x 14 rows
    lx = M + 356
    col_w = 198
    pitch = 14
    for i, (num, region, head, src) in enumerate(ALSO):
        col = i // 14
        row = i % 14
        x = lx + col * (col_w + 8)
        y = by2 + 20 + row * pitch
        d.text((x, y), fit_also(d, num, region, head, src, col_w),
               font=f(SANS, 9), fill=INK)

    # date-check box + credit
    d.rectangle([M, 998, W - M, 1020], fill=CREAM, outline=RULE)
    d.text((M + 8, 1004),
           "DATE CHECK — Left out as other days' news: GTA 6 sales (20 Nov) · "
           "Nvidia Q3 (17 Nov) · BYD EU ban (20 Nov) · OpenRouter (22 Nov) · "
           "Cairn zero-day (20 Nov) · KPMG breach (18 Nov) · RS-25 test (18 Nov)",
           font=f(SANS, 9), fill=INK)
    img.save(out)
    print(f"saved {out}: {n} stories, regions {counts}, "
          f"bottom_small={bottom_small}, map_top={by2}")


if __name__ == "__main__":
    render()
