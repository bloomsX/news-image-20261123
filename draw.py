#!/usr/bin/env python3
"""Render the 23 November 2026 front page: THE WORLD TODAY.

A single 1024x1024 infographic newspaper page. All story content lives
in STORIES below (drawn from stories-23nov.md). Run:

    python3 draw.py            # writes entry.png next to this file
    python3 draw.py --out x.png

Only the Python standard library and Pillow are needed.
"""

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 24
CONTENT_W = PAGE_W - 2 * MARGIN

INK = (17, 17, 17)
RED = (185, 28, 28)
DARK_RED = (140, 20, 20)
GREY = (85, 85, 85)
LIGHT_GREY = (150, 150, 150)
RULE_GREY = (200, 200, 200)
BAND = (246, 240, 227)
MAP_BG = (245, 244, 240)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F = {
    "masthead": font(SERIF_B, 56),
    "date": font(SANS_B, 18),
    "kicker": font(SANS_B, 15),
    "dateline": font(SANS_B, 13),
    "stat_num": font(SANS_B, 30),
    "stat_lab": font(SANS, 11),
    "utc_head": font(SANS_B, 12),
    "utc": font(SANS_B, 12),
    "lead_region": font(SANS_B, 11),
    "lead_head": font(SERIF_B, 20),
    "lead_body": font(SANS, 12),
    "small_region": font(SANS_B, 10),
    "small_head": font(SERIF_B, 14),
    "small_src": font(SANS, 10),
    "section": font(SANS_B, 13),
    "also": font(SANS, 9),
    "also_num": font(SANS_B, 9),
    "bar": font(SANS_B, 11),
    "check": font(SANS, 11),
    "check_head": font(SANS_B, 11),
    "badge": font(SANS_B, 14),
    "badge_s": font(SANS_B, 11),
    "pin": font(SANS_B, 9),
}


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
# Each lead: number, scene key, place, field, headline, body, source.
LEADS = [
    (1, "summit", "ANTALYA, TÜRKIYE", "CLIMATE",
     "COP31 collapses — no deal",
     "COP31 ends without agreement in Antalya; talks break down. (BBC)",
     "BBC"),
    (2, "ballot", "WASHINGTON", "POLITICS",
     "Democrats take the House, 258–177",
     "Democrats win 258 seats and take both chambers of Congress. (BBC)",
     "BBC"),
    (3, "slide", "TOKYO", "MARKETS",
     "Nikkei −5.06% as AI sell-off spreads",
     "Japan's Nikkei dives; KOSPI halts, Taiwan swings 1,578 pts. (SimpleLife)",
     "SimpleLife"),
]

# Each small panel: number, scene key, place, field, headline, source.
SMALLS = [
    (4, "ship", "BENGHAZI, LIBYA", "WAR",
     "Frigate Merkury sinks off Benghazi", "WSJ"),
    (5, "strike", "DYMER, UKRAINE", "WAR",
     "Russian strikes kill 12 in Kyiv region", "Reuters"),
    (6, "refinery", "SAUDI ARABIA", "WAR",
     "Houthis claim Saudi refinery strikes", "Ind. Express"),
    (7, "ballot2", "ZURICH", "SPORT",
     "FIFA confirms UK as 2035 hosts", "BBC"),
    (8, "swing", "TAIPEI", "MARKETS",
     "Taiwan stocks swing 1,578 points", "SimpleLife"),
    (9, "rally", "SEOUL", "MARKETS",
     "Korea exports top $1T, a first", "SimpleLife"),
    (10, "quake", "VANUATU", "DISASTER",
     "M6.5 quake strikes Vanuatu", "USGS"),
    (11, "flags", "NEW DELHI", "POLITICS",
     "Nepal PM begins India visit", "NewsBites"),
    (12, "stage", "NEW YORK", "CULTURE",
     "ATEEZ tops Billboard 200", "Yonhap"),
    (13, "dome", "CANBERRA", "ECONOMY",
     "Jobless to top 5%, Chalmers warns", "Reuters"),
]

# ALSO list: number, region code, short text, source.
ALSO = [
    (14, "AS", "Taiwan bans short selling", "CNA"),
    (15, "AS", "KOSPI below 4,700, trading halts", "SL"),
    (16, "AS", "HK tech at 19-month low", "SL"),
    (17, "AS", "Sensex falls; Nifty −0.65%", "Rtr"),
    (18, "GL", "Brent crude $89.53", "IM"),
    (19, "AS", "India–China border talks", "NB"),
    (20, "EU", "French students plan protests", "MEye"),
    (21, "EU", "Bulgari dies aged 89", "BBC"),
    (22, "AS", "IND–NZ Test, Day 5 live", "ESPN"),
    (23, "EU", "FIDE: Sindarov takes White", "Chess"),
    (24, "EU", "Liverpool 4–0 Man Utd", "Rtr"),
    (25, "EU", "U2 album debuts at No. 4", "Var"),
    (26, "AS", "Syed Modi badminton Tue", "ESPN"),
    (27, "EU", "Vyshneve strike kills 2", "QNA"),
    (28, "EU", "Bila Tserkva strike kills 1", "QNA"),
    (29, "EU", "Dnipropetrovsk substation hit", "AFP"),
    (30, "AS", "Banten toll: 24 dead, 34 missing", "Rtr"),
    (31, "EU", "Poland: 3 objects were missiles", "BBC"),
    (32, "ME", "US hawks urge Iran strike", "FT"),
    (33, "NA", "Trump backs Huang on Nvidia", "FT"),
    (34, "AS", "Tai Po fire: one year on", "SCMP"),
    (35, "EU", "Burnham to tell MPs of EU deal", "BBC"),
    (36, "NA", "US probes alleged Nvidia spy", "Blbg"),
    (37, "ME", "Hamas seeks Gaza talks", "AA"),
    (38, "ME", "Gaza toll: 1,662 killed", "HM"),
    (39, "EU", "Kerch Bridge hit again", "NE"),
    (40, "AS", "Delhi air hazardous, AQI 324", "WC"),
    (41, "LA", "Venezuela talks extended", "LO"),
    (42, "LA", "US–Venezuela military deal", "BBC"),
    (43, "OC", "Qantas to axe 850 jobs", "CPA"),
    (44, "OC", "Albanese extends $25 script cap", "FNN"),
    (45, "OC", "RBA: tax plan fuels inflation", "FNN"),
    (46, "OC", "Lendlease rules out new shares", "FNN"),
    (47, "OC", "BHP's new boss backs nuclear", "FNN"),
    (48, "OC", "ALS −11% on Mideast hit", "FNN"),
    (49, "OC", "Olympian Henke dies, 99", "ABC"),
    (50, "OC", "PNG Chiefs sign star Young", "Cour"),
    (51, "OC", "Melbourne stabbings: charges laid", "Age"),
    (52, "OC", "Fire-ant nest found near Sydney", "Age"),
    (53, "OC", "Singapore PM flies into Sydney", "Gdn"),
    (54, "AS", "Korea Speaker begins Japan trip", "KT"),
    (55, "OC", "COP31 'a disaster for Pacific'", "ABC"),
]

STATS = [
    ("−5.06%", "Nikkei falls"),
    ("258", "Democrat House seats"),
    ("$1T", "Korea exports, first time"),
    ("12", "killed in Kyiv region"),
    ("6.5", "Vanuatu quake"),
    ("1,578", "points, Taiwan swing"),
]

UTC_ITEMS = [
    ("02:40", "Vanuatu M6.5"),
    ("03:49", "Dymer toll 12"),
    ("06:00", "Nikkei −5.06%"),
    ("06:16", "Sensex slides"),
    ("TODAY", "COP31 collapses"),
]

# Region bar: label, count, colour (widths proportional to count).
REGION_BAR = [
    ("EUROPE 13", 13, (37, 99, 235)),
    ("ASIA 16", 16, (234, 88, 12)),
    ("OCEANIA 14", 14, (16, 163, 127)),
    ("MIDEAST 4", 4, (220, 38, 38)),
    ("N AMERICA 3", 3, (101, 163, 13)),
    ("LATAM 2", 2, (124, 58, 237)),
    ("AFRICA 1", 1, (219, 190, 20)),
    ("GLOBAL 2", 2, (90, 90, 90)),
]

DATE_CHECK = ("DATE CHECK — Left out as other days' news: GTA 6 sales (20 Nov) · "
              "Nvidia Q3 (17 Nov) · BYD EU ban (20 Nov) · OpenRouter (22 Nov) · "
              "Cairn zero-day (20 Nov) · KPMG breach (18 Nov) · RS-25 test (18 Nov)")

# Map pins: story number -> (x, y) inside the map box.
PINS = {
    1: (196, 60), 2: (48, 52), 3: (306, 36), 4: (186, 74), 5: (186, 44),
    6: (206, 76), 7: (164, 36), 8: (280, 66), 9: (290, 50), 10: (316, 152),
    11: (246, 62), 12: (66, 38), 13: (296, 160),
}

# Rough continent outlines, in map-box coordinates (box is 330 x 176).
CONTINENTS = [
    # North America
    [(6, 34), (58, 18), (96, 28), (92, 56), (72, 72), (46, 78), (20, 62), (4, 46)],
    # South America
    [(74, 96), (104, 90), (116, 116), (100, 156), (86, 142), (72, 116)],
    # Europe
    [(150, 30), (180, 20), (196, 36), (186, 56), (166, 62), (150, 50)],
    # Africa
    [(156, 76), (186, 70), (202, 92), (190, 126), (170, 142), (158, 112)],
    # Asia
    [(200, 26), (262, 14), (312, 30), (306, 62), (272, 76), (240, 70),
     (216, 56), (204, 40)],
    # Australia
    [(264, 142), (306, 136), (316, 156), (290, 172), (268, 162)],
]


# ------------------------------------------------------------- illustrations
# Every scene is drawn with plain PIL shapes inside its own box
# (x, y, w, h). No external assets.

def _bars(draw, x, y, w, h, heights, colour):
    n = len(heights)
    step = w / n
    bw = step * 0.62
    for i, frac in enumerate(heights):
        bh = h * frac
        bx = x + i * step + (step - bw) / 2
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=colour)


def _polyline(draw, pts, colour, width):
    draw.line(pts, fill=colour, width=width, joint="curve")


def scene_summit(draw, x, y, w, h):
    """Climate summit: pale sky, long table, seated delegates, a clock."""
    draw.rectangle([x, y, x + w, y + h], fill=(168, 205, 225))
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=(120, 84, 52))
    draw.rectangle([x, y + h * 0.62, x + w, y + h * 0.68], fill=(94, 64, 38))
    for i, cx in enumerate([0.10, 0.26, 0.44, 0.62, 0.80]):
        px = x + w * cx
        draw.ellipse([px - 9, y + h * 0.34, px + 9, y + h * 0.34 + 18],
                     fill=(232, 190, 150))
        draw.rectangle([px - 11, y + h * 0.52, px + 11, y + h * 0.66],
                       fill=[(30, 64, 120), (185, 28, 28), (22, 120, 70),
                             (234, 130, 20), (90, 40, 110)][i])
    draw.ellipse([x + w * 0.86, y + 8, x + w * 0.86 + 26, y + 34],
                 outline=INK, width=2, fill=WHITE)
    draw.line([x + w * 0.86 + 13, y + 12, x + w * 0.86 + 13, y + 21],
              fill=INK, width=2)
    draw.line([x + w * 0.86 + 13, y + 21, x + w * 0.86 + 20, y + 21],
              fill=INK, width=2)
    draw.ellipse([x + w * 0.70, y + h * 0.44, x + w * 0.70 + 22,
                  y + h * 0.44 + 22], fill=(20, 130, 90))
    draw.ellipse([x + w * 0.70 + 6, y + h * 0.44 + 5, x + w * 0.70 + 16,
                  y + h * 0.44 + 15], fill=(120, 210, 170))


def scene_ballot(draw, x, y, w, h, box_colour=RED):
    """Ballot box with a white tick, grey skyline behind."""
    draw.rectangle([x, y, x + w, y + h], fill=(205, 214, 222))
    _bars(draw, x, y + h * 0.15, w, h * 0.85,
          [0.55, 0.8, 0.4, 0.7, 0.5, 0.9, 0.6], (160, 170, 180))
    bx, by, bw, bh = x + w * 0.30, y + h * 0.42, w * 0.42, h * 0.48
    draw.rectangle([bx, by, bx + bw, by + bh], fill=box_colour)
    draw.rectangle([bx - 6, by - 8, bx + bw + 6, by], fill=DARK_RED)
    draw.rectangle([x + w * 0.44, y + h * 0.18, x + w * 0.58, y + h * 0.40],
                   fill=WHITE, outline=GREY)
    cx, cy = bx + bw * 0.30, by + bh * 0.55
    draw.line([cx, cy, cx + bw * 0.18, cy + bh * 0.22,
               cx + bw * 0.55, cy - bh * 0.30], fill=WHITE, width=5,
              joint="curve")
    draw.ellipse([x + w * 0.78, y + h * 0.62, x + w * 0.78 + 16,
                  y + h * 0.62 + 16], fill=(232, 190, 150))
    draw.rectangle([x + w * 0.76, y + h * 0.78, x + w * 0.82, y + h],
                   fill=(30, 64, 120))


def scene_slide(draw, x, y, w, h):
    """Falling market: dark board, grey bars, red line diving down."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 30, 54))
    _bars(draw, x + 6, y + h * 0.22, w - 12, h * 0.72,
          [0.62, 0.55, 0.68, 0.5, 0.58, 0.44, 0.52, 0.36], (110, 120, 140))
    pts = [(x + 8 + i * (w - 16) / 7, y + h * (0.22 + 0.08 * i + (0.05 if i % 2 else 0)))
           for i in range(8)]
    _polyline(draw, pts, (230, 60, 60), 3)
    for px, py in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(230, 60, 60))


def scene_ship(draw, x, y, w, h):
    """Frigate on a dark sea, listing after an explosion."""
    draw.rectangle([x, y, x + w, y + h * 0.55], fill=(38, 44, 66))
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=(18, 38, 74))
    draw.polygon([(x + w * 0.12, y + h * 0.55), (x + w * 0.88, y + h * 0.50),
                  (x + w * 0.80, y + h * 0.72), (x + w * 0.20, y + h * 0.74)],
                 fill=(70, 76, 92))
    draw.rectangle([x + w * 0.30, y + h * 0.30, x + w * 0.36, y + h * 0.52],
                   fill=(90, 96, 112))
    draw.rectangle([x + w * 0.55, y + h * 0.34, x + w * 0.60, y + h * 0.50],
                   fill=(90, 96, 112))
    for fx, fy, fr in [(0.68, 0.30, 16), (0.74, 0.22, 11), (0.62, 0.24, 9)]:
        draw.ellipse([x + w * fx - fr, y + h * fy - fr,
                      x + w * fx + fr, y + h * fy + fr],
                     fill=(240, 130, 30))
    for wy in (0.80, 0.88):
        for k in range(5):
            sx = x + k * w / 5
            draw.arc([sx, y + h * wy, sx + w / 5, y + h * wy + 12],
                     180, 360, fill=(120, 180, 230), width=2)


def scene_strike(draw, x, y, w, h):
    """City block at night, one building hit, smoke rising."""
    draw.rectangle([x, y, x + w, y + h], fill=(32, 32, 44))
    for bx, bw, bh in [(0.04, 0.20, 0.62), (0.28, 0.18, 0.78),
                       (0.50, 0.22, 0.55), (0.76, 0.18, 0.70)]:
        draw.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h],
                       fill=(58, 58, 74))
    for wx in (0.09, 0.15, 0.33, 0.38, 0.55, 0.60, 0.81, 0.86):
        draw.rectangle([x + w * wx, y + h * 0.45, x + w * wx + 7, y + h * 0.45 + 9],
                       fill=(240, 200, 90))
    for sx, sy, sr in [(0.38, 0.16, 14), (0.44, 0.10, 10), (0.33, 0.10, 8)]:
        draw.ellipse([x + w * sx - sr, y + h * sy - sr,
                      x + w * sx + sr, y + h * sy + sr], fill=(200, 200, 205))
    draw.polygon([(x + w * 0.40, y + h * 0.24), (x + w * 0.46, y + h * 0.10),
                  (x + w * 0.52, y + h * 0.24)], fill=(240, 120, 30))


def scene_refinery(draw, x, y, w, h):
    """Refinery towers with orange flames against a dusk sky."""
    draw.rectangle([x, y, x + w, y + h], fill=(52, 40, 34))
    draw.rectangle([x, y + h * 0.72, x + w, y + h], fill=(30, 26, 24))
    for tx, tw, th in [(0.08, 0.10, 0.55), (0.24, 0.08, 0.68),
                       (0.40, 0.12, 0.45), (0.58, 0.08, 0.62),
                       (0.74, 0.10, 0.50)]:
        draw.rectangle([x + w * tx, y + h - h * th, x + w * (tx + tw), y + h * 0.78],
                       fill=(110, 108, 100))
        draw.polygon([(x + w * tx, y + h - h * th),
                      (x + w * (tx + tw / 2), y + h - h * th - 12),
                      (x + w * (tx + tw), y + h - h * th)], fill=(240, 120, 30))
    draw.ellipse([x + w * 0.82, y + h * 0.10, x + w * 0.82 + 20, y + h * 0.10 + 20],
                 fill=(245, 200, 90))


def scene_swing(draw, x, y, w, h):
    """Volatile market: dark board, bars, red line zig-zagging down."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 30, 54))
    _bars(draw, x + 6, y + h * 0.20, w - 12, h * 0.74,
          [0.5, 0.62, 0.45, 0.58, 0.4, 0.52, 0.34, 0.44], (110, 120, 140))
    pts = [(x + 8 + i * (w - 16) / 7,
            y + h * (0.28 + [0.0, 0.10, 0.04, 0.16, 0.08, 0.20, 0.12, 0.24][i]))
           for i in range(8)]
    _polyline(draw, pts, (230, 60, 60), 3)
    for px, py in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(230, 60, 60))


def scene_rally(draw, x, y, w, h):
    """Rising market: pale board, bars climbing, green line up."""
    draw.rectangle([x, y, x + w, y + h], fill=(222, 232, 222))
    _bars(draw, x + 6, y + h * 0.18, w - 12, h * 0.76,
          [0.30, 0.42, 0.38, 0.55, 0.50, 0.66, 0.60, 0.78], (110, 140, 170))
    pts = [(x + 8 + i * (w - 16) / 7, y + h * (0.85 - 0.09 * i))
           for i in range(8)]
    _polyline(draw, pts, (20, 140, 70), 3)
    for px, py in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(20, 140, 70))


def scene_quake(draw, x, y, w, h):
    """Cracked ground under a pale sky, a small house tilted."""
    draw.rectangle([x, y, x + w, y + h * 0.45], fill=(190, 220, 235))
    draw.polygon([(x, y + h * 0.45), (x + w, y + h * 0.45), (x + w, y + h),
                  (x, y + h)], fill=(150, 112, 70))
    draw.polygon([(x, y + h * 0.72), (x + w * 0.45, y + h * 0.55),
                  (x + w, y + h * 0.66), (x + w, y + h), (x, y + h)],
                 fill=(120, 88, 54))
    crack = [(x + w * 0.30, y + h * 0.48), (x + w * 0.38, y + h * 0.62),
             (x + w * 0.34, y + h * 0.74), (x + w * 0.44, y + h * 0.90),
             (x + w * 0.42, y + h)]
    _polyline(draw, crack, (60, 30, 20), 3)
    draw.rectangle([x + w * 0.62, y + h * 0.30, x + w * 0.80, y + h * 0.52],
                   fill=(200, 170, 130))
    draw.polygon([(x + w * 0.60, y + h * 0.32), (x + w * 0.71, y + h * 0.16),
                  (x + w * 0.82, y + h * 0.32)], fill=(140, 40, 40))


def scene_flags(draw, x, y, w, h):
    """Nepal (crimson double pennant, blue border) and India (saffron /
    white / green tricolour with navy chakra) on poles over a green field."""
    draw.rectangle([x, y, x + w, y + h * 0.55], fill=(185, 218, 238))
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=(110, 170, 100))
    # Nepal: double-pennant silhouette, crimson fill, blue border, white
    # sun/moon dots (one per pennant).
    px = x + w * 0.22
    fx0, fy0 = px, y + h * 0.14
    fw, fh = w * 0.26, h * 0.24
    nepal = [(fx0, fy0), (fx0 + fw, fy0 + fh * 0.35), (fx0, fy0 + fh * 0.45),
             (fx0 + fw, fy0 + fh * 0.85), (fx0, fy0 + fh)]
    draw.line([px, y + h * 0.12, px, y + h * 0.85], fill=INK, width=2)
    draw.polygon(nepal, fill=(220, 20, 60))
    draw.line(nepal + [nepal[0]], fill=(0, 56, 147), width=2, joint="curve")
    for dy in (0.16, 0.62):
        draw.ellipse([fx0 + fw * 0.18 - 2, fy0 + fh * dy - 2,
                      fx0 + fw * 0.18 + 2, fy0 + fh * dy + 2], fill=WHITE)
    # India: saffron / white / green bands with a navy chakra wheel.
    px = x + w * 0.60
    fx0, fy0 = px, y + h * 0.14
    draw.line([px, y + h * 0.12, px, y + h * 0.85], fill=INK, width=2)
    band = fh / 3
    draw.rectangle([fx0, fy0, fx0 + fw, fy0 + band], fill=(255, 153, 51))
    draw.rectangle([fx0, fy0 + band, fx0 + fw, fy0 + 2 * band], fill=WHITE)
    draw.rectangle([fx0, fy0 + 2 * band, fx0 + fw, fy0 + fh],
                   fill=(19, 136, 8))
    cx, cy, cr = fx0 + fw / 2, fy0 + fh / 2, fh * 0.18
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=(0, 0, 128),
                 width=1)
    draw.line([cx - cr, cy, cx + cr, cy], fill=(0, 0, 128), width=1)
    draw.line([cx, cy - cr, cx, cy + cr], fill=(0, 0, 128), width=1)


def scene_stage(draw, x, y, w, h):
    """Concert stage: dark hall, spotlight cone, pyramid roofline."""
    draw.rectangle([x, y, x + w, y + h], fill=(22, 22, 40))
    draw.polygon([(x + w * 0.5, y + h * 0.10), (x + w * 0.20, y + h * 0.95),
                  (x + w * 0.80, y + h * 0.95)], fill=(60, 60, 100))
    draw.polygon([(x + w * 0.5, y + h * 0.10), (x + w * 0.38, y + h * 0.95),
                  (x + w * 0.62, y + h * 0.95)], fill=(200, 200, 230))
    draw.ellipse([x + w * 0.44, y + h * 0.08, x + w * 0.56, y + h * 0.08 + 14],
                 fill=(255, 250, 200))
    for sx, sy in [(0.12, 0.18), (0.88, 0.14), (0.78, 0.30), (0.20, 0.34)]:
        draw.ellipse([x + w * sx - 3, y + h * sy - 3, x + w * sx + 3,
                      y + h * sy + 3], fill=(255, 220, 120))


def scene_dome(draw, x, y, w, h):
    """Parliament dome under a pale sky."""
    draw.rectangle([x, y, x + w, y + h * 0.60], fill=(198, 222, 236))
    draw.rectangle([x, y + h * 0.60, x + w, y + h], fill=(140, 170, 120))
    draw.rectangle([x + w * 0.20, y + h * 0.55, x + w * 0.80, y + h * 0.72],
                   fill=(225, 222, 210))
    draw.pieslice([x + w * 0.36, y + h * 0.18, x + w * 0.64, y + h * 0.62],
                  180, 360, fill=(235, 232, 220))
    draw.line([x + w * 0.5, y + h * 0.08, x + w * 0.5, y + h * 0.20],
              fill=INK, width=2)
    for cx in (0.28, 0.40, 0.60, 0.72):
        draw.rectangle([x + w * cx - 4, y + h * 0.58, x + w * cx + 4,
                        y + h * 0.72], fill=(120, 118, 108))


SCENES = {
    "summit": scene_summit,
    "ballot": scene_ballot,
    "slide": scene_slide,
    "ship": scene_ship,
    "strike": scene_strike,
    "refinery": scene_refinery,
    "ballot2": lambda d, x, y, w, h: scene_ballot(d, x, y, w, h, (160, 20, 60)),
    "swing": scene_swing,
    "rally": scene_rally,
    "quake": scene_quake,
    "flags": scene_flags,
    "stage": scene_stage,
    "dome": scene_dome,
}


def draw_badge(draw, cx, cy, number, big=True):
    """Red numbered circle, centred on (cx, cy)."""
    r = 13 if big else 10
    fnt = F["badge"] if big else F["badge_s"]
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    label = str(number)
    tw = draw.textlength(label, font=fnt)
    th = fnt.getbbox(label)[3]
    draw.text((cx - tw / 2, cy - th / 2 - 1), label, font=fnt, fill=WHITE)


# ------------------------------------------------------------- page sections

def render_masthead(draw):
    y = 12
    draw.text((MARGIN, y), "THE WORLD TODAY", font=F["masthead"], fill=INK)
    dateline = "MONDAY  ·  23 NOVEMBER 2026"
    dw = draw.textlength(dateline, font=F["date"])
    draw.text((PAGE_W - MARGIN - dw, y + 24), dateline, font=F["date"],
              fill=RED)
    draw.rectangle([MARGIN, 86, PAGE_W - MARGIN, 89], fill=RED)
    kicker = "55 STORIES  ·  7 REGIONS  ·  12 FIELDS  ·  EVERY STORY DATE-CHECKED TO TODAY"
    draw.text((MARGIN, 96), kicker, font=F["kicker"], fill=INK)
    page = "PAGE 1 OF 1"
    pw = draw.textlength(page, font=F["dateline"])
    draw.text((PAGE_W - MARGIN - pw, 99), page, font=F["dateline"], fill=GREY)
    draw.text((MARGIN, 118), "ALL 55 STORIES DATE-CHECKED TO MONDAY 23 NOVEMBER 2026",
              font=F["dateline"], fill=RED)
    return 140


def render_stats(draw, y):
    cell_w = CONTENT_W / len(STATS)
    for i, (num, lab) in enumerate(STATS):
        cx = MARGIN + cell_w * i
        draw.text((cx, y), num, font=F["stat_num"], fill=RED)
        draw.text((cx, y + 34), lab, font=F["stat_lab"], fill=INK)
        if i:
            draw.line([cx - 8, y + 2, cx - 8, y + 46], fill=RULE_GREY, width=1)
    return y + 52


def render_utc(draw, y):
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 26], fill=BAND)
    tx = MARGIN + 8
    draw.text((tx, y + 6), "THE DAY IN UTC", font=F["utc_head"], fill=RED)
    tx += draw.textlength("THE DAY IN UTC", font=F["utc_head"]) + 14
    parts = []
    for when, what in UTC_ITEMS:
        parts.append((when, what))
    for idx, (when, what) in enumerate(parts):
        w1 = draw.textlength(when + " ", font=F["utc_head"])
        draw.text((tx, y + 6), when, font=F["utc_head"], fill=INK)
        draw.text((tx + w1, y + 6), what, font=F["utc"], fill=INK)
        tx += w1 + draw.textlength(what, font=F["utc"]) + 8
        if idx < len(parts) - 1:
            draw.text((tx, y + 6), "·", font=F["utc"], fill=GREY)
            tx += draw.textlength("·", font=F["utc"]) + 8
    return y + 26


def render_lead(draw, x, y, w, num, scene, place, field, headline, body):
    art_h = 100
    SCENES[scene](draw, x, y, w, art_h)
    draw_badge(draw, x + 15, y + 15, num, big=True)
    ty = y + art_h + 6
    draw.text((x, ty), f"{place} · {field}", font=F["lead_region"], fill=RED)
    ty += 16
    lines = wrap(draw, headline, F["lead_head"], w)
    ty = text_block(draw, (x, ty), lines[:3], F["lead_head"], INK, 23)
    ty += 2
    blines = wrap(draw, body, F["lead_body"], w)
    text_block(draw, (x, ty), blines[:2], F["lead_body"], GREY, 15)
    return y + art_h + 6 + 16 + min(len(lines), 3) * 23 + 2 + min(len(blines), 2) * 15


def render_small(draw, x, y, w, num, scene, place, field, headline, source):
    art_h = 62
    SCENES[scene](draw, x, y, w, art_h)
    draw_badge(draw, x + 12, y + 12, num, big=False)
    ty = y + art_h + 5
    draw.text((x, ty), f"{place} · {field}", font=F["small_region"], fill=RED)
    ty += 13
    lines = wrap(draw, headline, F["small_head"], w)
    ty = text_block(draw, (x, ty), lines[:3], F["small_head"], INK, 17)
    draw.text((x, ty + 2), f"Source: {source}", font=F["small_src"], fill=GREY)
    return ty + 2 + 13


def render_map(draw, x, y, w, h):
    draw.text((x, y), "WHERE IT HAPPENED — STORIES 1–13",
              font=F["section"], fill=INK)
    my = y + 20
    mh = h - 20
    draw.rectangle([x, my, x + w, my + mh], fill=MAP_BG, outline=RULE_GREY)
    for poly in CONTINENTS:
        shifted = [(x + px, my + py) for px, py in poly]
        draw.polygon(shifted, fill=(222, 220, 210), outline=(170, 168, 158))
    for num, (px, py) in PINS.items():
        cx, cy = x + px, my + py
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
        label = str(num)
        tw = draw.textlength(label, font=F["pin"])
        th = F["pin"].getbbox(label)[3]
        draw.text((cx - tw / 2, cy - th / 2 - 1), label, font=F["pin"],
                  fill=WHITE)
    return my + mh


def render_also(draw, x, y, w, h):
    draw.text((x, y), "ALSO ON MONDAY 23 NOVEMBER — 42 MORE STORIES",
              font=F["section"], fill=INK)
    col_w = w / 3
    row_h = 13
    top = y + 20
    for i, (num, code, text, src) in enumerate(ALSO):
        col = i // 14
        row = i % 14
        cx = x + col * col_w
        cy = top + row * row_h
        head = f"{num} {code} "
        draw.text((cx, cy), head, font=F["also_num"], fill=INK)
        hx = cx + draw.textlength(head, font=F["also_num"])
        avail = col_w - (hx - cx) - 4
        line = text
        while draw.textlength(line + f" ({src})", font=F["also"]) > avail and len(line) > 12:
            line = line.rsplit(" ", 1)[0]
            if line.endswith(","):
                line = line[:-1]
        if len(line) < len(text):
            line = line.rstrip() + "…"
        draw.text((hx, cy), line, font=F["also"], fill=INK)
        sx = hx + draw.textlength(line + " ", font=F["also"])
        draw.text((sx, cy), f"({src})", font=F["also"], fill=GREY)
    return top + 14 * row_h


def render_region_bar(draw, y):
    total = sum(c for _, c, _ in REGION_BAR)
    x = MARGIN
    for label, count, colour in REGION_BAR:
        seg_w = CONTENT_W * count / total
        draw.rectangle([x, y, x + seg_w, y + 12], fill=colour)
        x += seg_w
    labels = " · ".join(l for l, _, _ in REGION_BAR)
    draw.text((MARGIN, y + 16), labels, font=F["bar"], fill=INK)
    return y + 16 + 15


def render_date_check(draw, y):
    box_h = 34
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + box_h],
                   outline=GREY, width=1)
    lines = wrap(draw, DATE_CHECK, F["check"], CONTENT_W - 16)
    text_block(draw, (MARGIN + 8, y + 4), lines[:2], F["check"], INK, 13)
    return y + box_h


def build_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), WHITE)
    draw = ImageDraw.Draw(img)

    y = render_masthead(draw)
    y = render_stats(draw, y + 2)
    y = render_utc(draw, y + 6)

    # Leads: three columns.
    lead_y = y + 10
    lead_w = (CONTENT_W - 2 * 11) // 3
    lead_bottom = lead_y
    for i, (num, scene, place, field, head, body, _src) in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + 11)
        bottom = render_lead(draw, lx, lead_y, lead_w, num, scene, place,
                             field, head, body)
        lead_bottom = max(lead_bottom, bottom)

    # Small panels: two rows of five.
    small_w = (CONTENT_W - 4 * 11) // 5
    small_top = lead_bottom + 10
    row_bottom = small_top
    for row in range(2):
        row_y = small_top + row * 152
        for col in range(5):
            item = SMALLS[row * 5 + col]
            sx = MARGIN + col * (small_w + 11)
            bottom = render_small(draw, sx, row_y, small_w, item[0], item[1],
                                  item[2], item[3], item[4], item[5])
            row_bottom = max(row_bottom, bottom)

    # Map + ALSO list.
    bottom_y = row_bottom + 8
    map_w = 330
    also_x = MARGIN + map_w + 16
    also_w = CONTENT_W - map_w - 16
    end_map = render_map(draw, MARGIN, bottom_y, map_w, 208)
    end_also = render_also(draw, also_x, bottom_y, also_w, 208)

    bar_y = max(end_map, end_also) + 8
    bar_end = render_region_bar(draw, bar_y)
    render_date_check(draw, bar_end + 4)
    return img


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render THE WORLD TODAY front page")
    parser.add_argument("--out", default=None, help="output PNG path")
    args = parser.parse_args(argv)
    here = os.path.dirname(os.path.abspath(__file__))
    out = args.out or os.path.join(here, "entry.png")
    img = build_page()
    img.save(out, "PNG")
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
