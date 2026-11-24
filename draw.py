#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page, 1024x1024 PNG.

Deterministic: fixed fonts, fixed layout, no timestamps, no randomness,
no network. Run twice -> byte-identical output.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/liberation/"

INK = (17, 17, 17)
PAPER = (255, 255, 255)
NAVY = (18, 52, 86)
RED = (178, 34, 34)
GREY = (90, 90, 90)
LIGHT = (238, 238, 236)
MIDLINE = (200, 200, 198)
TEAL = (14, 116, 110)
GOLD = (176, 124, 0)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_TITLE = font("LiberationSerif-Bold.ttf", 44)
F_DATE = font("LiberationSans-Bold.ttf", 17)
F_SUB = font("LiberationSans-Regular.ttf", 13)
F_TICK = font("LiberationSans-Bold.ttf", 13)
F_LEAD_H = font("LiberationSerif-Bold.ttf", 30)
F_LEAD_B = font("LiberationSans-Regular.ttf", 15)
F_SRC = font("LiberationSans-Italic.ttf", 11)
F_KICK = font("LiberationSans-Bold.ttf", 11)
F_CARD_H = font("LiberationSans-Bold.ttf", 15)
F_CARD_B = font("LiberationSans-Regular.ttf", 12)
F_BRIEF_H = font("LiberationSans-Bold.ttf", 13)
F_BRIEF = font("LiberationSans-Regular.ttf", 11)
F_FOOT = font("LiberationSans-Regular.ttf", 10)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, max_lines=None, lh=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    if lh is None:
        lh = fnt.size + 3
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


# ---------------------------------------------------------------- icons
def icon_ship(d, x, y, s, col):
    # simple corvette silhouette on waves
    d.polygon([(x, y + 0.55 * s), (x + 0.95 * s, y + 0.55 * s),
               (x + 0.82 * s, y + 0.78 * s), (x + 0.12 * s, y + 0.78 * s)], fill=col)
    d.rectangle([x + 0.30 * s, y + 0.30 * s, x + 0.62 * s, y + 0.55 * s], fill=col)
    d.line([x + 0.45 * s, y + 0.30 * s, x + 0.45 * s, y + 0.08 * s], fill=col, width=3)
    d.polygon([(x + 0.45 * s, y + 0.08 * s), (x + 0.62 * s, y + 0.18 * s),
               (x + 0.45 * s, y + 0.18 * s)], fill=RED)
    for i, wy in enumerate([0.86, 0.93]):
        d.line([x, y + wy * s, x + s, y + wy * s], fill=NAVY, width=3)


def icon_chip(d, x, y, s, col):
    d.rectangle([x + 0.22 * s, y + 0.22 * s, x + 0.78 * s, y + 0.78 * s],
                outline=col, width=4)
    d.rectangle([x + 0.40 * s, y + 0.40 * s, x + 0.60 * s, y + 0.60 * s], fill=col)
    for i in range(3):
        px = x + (0.32 + i * 0.18) * s
        d.line([px, y, px, y + 0.22 * s], fill=col, width=3)
        d.line([px, y + 0.78 * s, px, y + s], fill=col, width=3)
        d.line([x, y + (0.32 + i * 0.18) * s, x + 0.22 * s, y + (0.32 + i * 0.18) * s],
               fill=col, width=3)
        d.line([x + 0.78 * s, y + (0.32 + i * 0.18) * s, x + s,
                y + (0.32 + i * 0.18) * s], fill=col, width=3)


def icon_trophy(d, x, y, s, col):
    d.polygon([(x + 0.30 * s, y + 0.10 * s), (x + 0.70 * s, y + 0.10 * s),
               (x + 0.62 * s, y + 0.55 * s), (x + 0.38 * s, y + 0.55 * s)], fill=col)
    d.arc([x + 0.05 * s, y + 0.10 * s, x + 0.35 * s, y + 0.45 * s], 90, 270, fill=col, width=4)
    d.arc([x + 0.65 * s, y + 0.10 * s, x + 0.95 * s, y + 0.45 * s], -90, 90, fill=col, width=4)
    d.rectangle([x + 0.44 * s, y + 0.55 * s, x + 0.56 * s, y + 0.72 * s], fill=col)
    d.rectangle([x + 0.32 * s, y + 0.72 * s, x + 0.68 * s, y + 0.82 * s], fill=col)


def icon_flame(d, x, y, s, col):
    d.polygon([(x + 0.50 * s, y + 0.05 * s), (x + 0.78 * s, y + 0.45 * s),
               (x + 0.88 * s, y + 0.70 * s), (x + 0.68 * s, y + 0.92 * s),
               (x + 0.32 * s, y + 0.92 * s), (x + 0.12 * s, y + 0.70 * s),
               (x + 0.22 * s, y + 0.45 * s)], fill=col)
    d.polygon([(x + 0.50 * s, y + 0.45 * s), (x + 0.65 * s, y + 0.65 * s),
               (x + 0.58 * s, y + 0.85 * s), (x + 0.42 * s, y + 0.85 * s),
               (x + 0.35 * s, y + 0.65 * s)], fill=(255, 255, 255))


def icon_scales(d, x, y, s, col):
    d.line([x + 0.50 * s, y + 0.08 * s, x + 0.50 * s, y + 0.85 * s], fill=col, width=4)
    d.line([x + 0.15 * s, y + 0.22 * s, x + 0.85 * s, y + 0.22 * s], fill=col, width=4)
    d.line([x + 0.15 * s, y + 0.22 * s, x + 0.08 * s, y + 0.60 * s], fill=col, width=3)
    d.line([x + 0.15 * s, y + 0.22 * s, x + 0.22 * s, y + 0.60 * s], fill=col, width=3)
    d.line([x + 0.85 * s, y + 0.22 * s, x + 0.78 * s, y + 0.60 * s], fill=col, width=3)
    d.line([x + 0.85 * s, y + 0.22 * s, x + 0.92 * s, y + 0.60 * s], fill=col, width=3)
    d.arc([x + 0.02 * s, y + 0.52 * s, x + 0.28 * s, y + 0.72 * s], 0, 180, fill=col, width=4)
    d.arc([x + 0.72 * s, y + 0.52 * s, x + 0.98 * s, y + 0.72 * s], 0, 180, fill=col, width=4)
    d.rectangle([x + 0.38 * s, y + 0.85 * s, x + 0.62 * s, y + 0.92 * s], fill=col)


def icon_globe(d, x, y, s, col):
    d.ellipse([x + 0.05 * s, y + 0.05 * s, x + 0.95 * s, y + 0.95 * s], outline=col, width=4)
    d.ellipse([x + 0.30 * s, y + 0.05 * s, x + 0.70 * s, y + 0.95 * s], outline=col, width=3)
    d.line([x + 0.05 * s, y + 0.50 * s, x + 0.95 * s, y + 0.50 * s], fill=col, width=3)
    d.arc([x + 0.05 * s, y + 0.25 * s, x + 0.95 * s, y + 0.75 * s], 200, 340, fill=col, width=3)
    d.arc([x + 0.05 * s, y + 0.25 * s, x + 0.95 * s, y + 0.75 * s], 20, 160, fill=col, width=3)


def icon_mail(d, x, y, s, col):
    d.rectangle([x + 0.08 * s, y + 0.22 * s, x + 0.92 * s, y + 0.82 * s],
                outline=col, width=4)
    d.line([x + 0.08 * s, y + 0.22 * s, x + 0.50 * s, y + 0.58 * s], fill=col, width=3)
    d.line([x + 0.92 * s, y + 0.22 * s, x + 0.50 * s, y + 0.58 * s], fill=col, width=3)
    d.text((x + 0.38 * s, y + 0.60 * s), "!", font=font("LiberationSans-Bold.ttf", int(s * 0.30)), fill=RED)


# ---------------------------------------------------------------- data
LEAD = {
    "kicker": "LEAD  •  MEDITERRANEAN  •  UKRAINE WAR SPREADS",
    "headline": "Ukraine sinks Russian warship off Libya",
    "body": ("Seven Ukrainian sea drones sink the corvette Merkury at Benghazi, "
             "Zelenskyy says — the cargo ship MV Angara is hit and a Ka-27 helicopter "
             "destroyed, 2,400 km from the front line."),
    "source": "Reuters / AP / CNN — 23 Nov",
}

CARDS = [
    {"kicker": "TECH  •  UNITED STATES", "icon": icon_chip, "col": TEAL,
     "headline": "Huang back at Nvidia; shares soar 31%",
     "body": ("Board reinstates Jensen Huang as CEO 11 days after he quit; the stock "
              "adds $952bn in a day, its best since 2003."),
     "source": "CNN / Reuters — 23 Nov"},
    {"kicker": "SPORT  •  FIFA", "icon": icon_trophy, "col": GOLD,
     "headline": "Women's World Cups: USA 2031, UK 2035",
     "body": ("FIFA names the US, Mexico, Costa Rica and Jamaica for 2031 and England, "
              "Scotland, Wales and N. Ireland for 2035 — first 48-team editions."),
     "source": "FIFA / AP — 23 Nov"},
    {"kicker": "ASIA  •  INDONESIA", "icon": icon_flame, "col": RED,
     "headline": "Cikande factory fire: 24 dead, 30 missing",
     "body": ("Toll confirmed after the weekend blaze at a candy plant in Banten; "
              "rescuers search the unstable wreckage for the missing."),
     "source": "Reuters — 23 Nov"},
    {"kicker": "EUROPE  •  DENMARK", "icon": icon_scales, "col": NAVY,
     "headline": "Top court backs 'ghetto law' evictions",
     "body": ("Supreme Court rules ending 91 leases in Helsingør was not ethnic "
              "discrimination, backing Denmark's hard line on immigration."),
     "source": "Reuters — 23 Nov"},
    {"kicker": "MIDDLE EAST  •  GAZA", "icon": icon_globe, "col": TEAL,
     "headline": "Gaza a 'toxic wasteland', report finds",
     "body": ("Oxfam/CEOBS: contamination indicators across over 99% of the Strip; "
              "78% of land hit; 61m tonnes of debris to clear."),
     "source": "Oxfam — 23 Nov"},
    {"kicker": "EUROPE  •  GERMANY & DENMARK", "icon": icon_mail, "col": NAVY,
     "headline": "Hoax bomb threats hit 450 schools",
     "body": ("'Death awaits you' emails sent to schools in Germany and Denmark; "
              "police say there is no concrete danger."),
     "source": "Reuters — 23 Nov"},
]

# (region, text, source)
BRIEFS = [
    ("EUROPE", "Dymer toll rises to 11 after Russian drone hits Kyiv flats", "Geopolitiki"),
    ("EUROPE", "Kushner sets condition for Trump Ukraine security guarantees", "Geopolitiki"),
    ("EUROPE", "Polish military says Russian drone briefly entered airspace", "Roundups"),
    ("EUROPE", "Ukrainian drones hit refineries in Perm, Rostov, Tatarstan", "Geopolitiki"),
    ("EUROPE", "Merz: Europe is prepared to negotiate with Russia", "Roundups"),
    ("EUROPE", "Brussels unveils 22nd package of sanctions on Russia", "Roundups"),
    ("MIDDLE EAST", "Iran vows \u201cevery means\u201d to counter US Hormuz blockade", "Reuters"),
    ("MIDDLE EAST", "Two tankers struck in Strait of Hormuz, UK body says", "UKMTO"),
    ("MIDDLE EAST", "Houthis claim drone strike on Saudi Rabigh refinery", "Reuters"),
    ("MIDDLE EAST", "Israeli strike on Gaza City kills at least three", "Roundups"),
    ("MIDDLE EAST", "Netanyahu\u2013Eisenkot talks end with no government deal", "AFP"),
    ("AFRICA", "UN, US condemn Khartoum drone strikes; four killed", "Addis Standard"),
    ("AFRICA", "Fighting in Ituri traps DR Congo Ebola responders", "PANA"),
    ("AFRICA", "35 Fulani killed in revenge attacks in Nigeria", "AFP"),
    ("SOUTH ASIA", "Lahore tops world pollution ranking; AQI passes 500", "Times of India"),
    ("SOUTH ASIA", "Magnitude 4.0 quake hits Pakistan near Afghan border", "Times of India"),
    ("SOUTH ASIA", "India top court grants bail to Godhra convict", "Times of India"),
    ("SOUTH ASIA", "Nepal PM Balendra Shah holds talks with Modi", "MEA"),
    ("SOUTH ASIA", "India declare record 720/9 in Wellington Test", "Reuters"),
    ("EAST ASIA", "S. Korea says suspected N. Korean aircraft entered airspace", "Roundups"),
    ("EAST ASIA", "S. Korea minister quits over AI exam cheating scandal", "Reuters"),
    ("EAST ASIA", "Chinese official gets death sentence for leaking secrets", "Times of India"),
    ("EAST ASIA", "Supermoon meets the Pleiades in tonight's sky", "CNET"),
    ("OCEANIA", "Albanese blames \u201cdifficult geopolitics\u201d for COP31 failure", "AFP"),
    ("OCEANIA", "NZ retail sales rise 2.2% in third quarter", "FinScans"),
    ("NORTH AMERICA", "Appeals court gives Trump path to erase conviction", "AP"),
    ("NORTH AMERICA", "O'Hare ground stop over staffing as travel peaks", "NBC Chicago"),
    ("NORTH AMERICA", "Delta glitch delays about 2,000 flights", "AP"),
    ("LATIN AMERICA", "Bolsonaro \u201cstable\u201d in intensive care in Brazil", "AFP"),
]

TICKER = ("MARKETS — MONDAY CLOSE:  NVDA +31.5%  •  NASDAQ +6.5%  •  S&P 500 +4.7%  •  "
          "DOW +1,448  •  GOLD ~$3,577/oz  •  BRENT ~$90/bbl")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # margin

    # ---- masthead
    d.rectangle([0, 0, W, 86], fill=NAVY)
    d.text((mx, 10), "THE WORLD TODAY", font=F_TITLE, fill=(255, 255, 255))
    d.text((W - mx - d.textlength("36 STORIES · 8 REGIONS", font=F_DATE), 26),
           "36 STORIES · 8 REGIONS", font=F_DATE, fill=(255, 214, 90))
    d.rectangle([0, 86, W, 88], fill=RED)
    d.text((mx, 96), "TUESDAY 24 NOVEMBER 2026", font=F_DATE, fill=RED)
    sub = "The day's world news in one picture — every figure attributed to its source"
    d.text((W - mx - d.textlength(sub, font=F_SUB), 97), sub, font=F_SUB, fill=GREY)

    # ---- ticker
    d.rectangle([0, 122, W, 146], fill=LIGHT)
    d.text((mx, 129), TICKER, font=F_TICK, fill=INK)

    # ---- lead panel
    ly = 156
    d.rectangle([mx, ly, W - mx, ly + 132], outline=NAVY, width=2)
    d.rectangle([mx, ly, W - mx, ly + 132], fill=(245, 247, 250))
    d.rectangle([mx, ly, W - mx, ly + 132], outline=NAVY, width=2)
    icon_ship(d, mx + 16, ly + 30, 76, NAVY)
    lx = mx + 118
    d.text((lx, ly + 10), LEAD["kicker"], font=F_KICK, fill=RED)
    y = draw_wrapped(d, lx, ly + 30, LEAD["headline"], F_LEAD_H, W - mx - lx - 14, INK,
                     max_lines=1, lh=34)
    y = draw_wrapped(d, lx, y + 4, LEAD["body"], F_LEAD_B, W - mx - lx - 14, INK,
                     max_lines=3, lh=19)
    d.text((lx, ly + 132 - 20), "Source: " + LEAD["source"], font=F_SRC, fill=GREY)

    # ---- six cards: 3 cols x 2 rows
    cy = 300
    cw = (W - 2 * mx - 2 * 12) // 3
    chh = 140
    for i, c in enumerate(CARDS):
        col = i % 3
        row = i // 3
        x0 = mx + col * (cw + 12)
        y0 = cy + row * (chh + 12)
        d.rectangle([x0, y0, x0 + cw, y0 + chh], outline=MIDLINE, width=1)
        d.rectangle([x0, y0, x0 + cw, y0 + 4], fill=c["col"])
        c["icon"](d, x0 + 10, y0 + 14, 34, c["col"])
        tx = x0 + 52
        d.text((tx, y0 + 10), c["kicker"], font=F_KICK, fill=RED)
        y = draw_wrapped(d, tx, y0 + 28, c["headline"], F_CARD_H, cw - 62, INK,
                         max_lines=2, lh=18)
        y = draw_wrapped(d, x0 + 10, y0 + 64, c["body"], F_CARD_B, cw - 20, INK,
                         max_lines=3, lh=15)
        d.text((x0 + 10, y0 + chh - 18), "Source: " + c["source"], font=F_SRC, fill=GREY)

    # ---- briefs
    by = cy + 2 * chh + 12 + 8
    d.text((mx, by), "THE DAY IN BRIEF — 29 MORE STORIES", font=F_BRIEF_H, fill=NAVY)
    d.line([mx, by + 20, W - mx, by + 20], fill=RED, width=2)
    by += 28
    col_w = (W - 2 * mx - 24) // 2
    rows = (len(BRIEFS) + 1) // 2
    row_h = 23
    for i, (region, text, src) in enumerate(BRIEFS):
        col = i // rows
        row = i % rows
        x0 = mx + col * (col_w + 24)
        y0 = by + row * row_h
        tag = region + " — "
        full = tag + text
        lines = wrap(d, full, F_BRIEF, col_w - 8)
        lines = lines[:2]
        # bold region tag on first line
        d.text((x0, y0), tag, font=font("LiberationSans-Bold.ttf", 11), fill=RED)
        tx = d.textlength(tag, font=font("LiberationSans-Bold.ttf", 11))
        first = lines[0][len(tag):] if lines and lines[0].startswith(tag) else (lines[0] if lines else "")
        d.text((x0 + tx, y0), first, font=F_BRIEF, fill=INK)
        if len(lines) > 1:
            d.text((x0, y0 + 11), lines[1], font=F_BRIEF, fill=INK)

    # ---- footer
    fy = H - 26
    d.line([mx, fy - 6, W - mx, fy - 6], fill=MIDLINE, width=1)
    foot = ("Sources: Reuters, AP, CNN, AFP, FIFA, Oxfam, UKMTO, Addis Standard, PANA, Times of India, "
            "CNET, Geopolitiki — 23–24 Nov 2026. Front page drawn 24 Nov 2026.")
    d.text((mx, fy), foot, font=F_FOOT, fill=GREY)

    img.save("entry.png", format="PNG", optimize=False)


if __name__ == "__main__":
    main()
