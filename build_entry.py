#!/usr/bin/env python3
"""Compose the 19 Nov 2026 front-page news image (1024x1024, deterministic).

Reads the generated base photo (Shenzhen skyline at dusk), crops it to the
hero band, then lays out a broadsheet front page: a date masthead, the hero
photo with the Shenzhen trilateral headline overlaid, and below it a white
grid of six more stories from Thursday 19 November 2026 plus an "also
today" footer line. Writes entry.png in the workdir. If the PNG would
exceed 1 MiB, JPEG bytes are written instead (same filename; told apart by
first bytes).
"""
import io
import os

from PIL import Image, ImageDraw, ImageFont

WORKDIR = os.path.dirname(os.path.abspath(__file__))
BASE_PHOTO = os.path.join(
    WORKDIR, "assets",
    "media-generation-shenzhen-skyline-dusk-0-9cd8c4d1-d6a1-4bd1-9a80-d32b478db670.webp",
)
OUT_PATH = os.path.join(WORKDIR, "entry.png")

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

INK = (8, 10, 14)          # near-black for bands and text
PAPER = (255, 255, 255)    # white newsprint
AMBER = (245, 166, 0)      # amber accent
WHITE = (255, 255, 255)
GREY = (70, 74, 80)        # body grey on white
LINE = (205, 208, 212)     # hairline rules
MARGIN = 48
CONTENT_W = W - 2 * MARGIN  # 928

MASTHEAD_H = 92
HERO_TOP = MASTHEAD_H + 4
HERO_H = 488               # hero photo band: y 96..584


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a max pixel width; returns list of lines."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    base = Image.open(BASE_PHOTO).convert("RGB")
    # Hero crop: keep the skyline band (tall central tower) and resize to
    # the 1024 x HERO_H hero area.
    target_ratio = W / HERO_H
    crop_w = int(base.height * target_ratio)
    crop_x = (base.width - crop_w) // 2
    crop = base.crop((crop_x, 0, crop_x + crop_w, base.height))
    hero = crop.resize((W, HERO_H), Image.LANCZOS)

    img = Image.new("RGB", (W, H), PAPER)
    img.paste(hero, (0, HERO_TOP))
    draw = ImageDraw.Draw(img, "RGBA")

    # ---- Top masthead band ----
    draw.rectangle([0, 0, W, MASTHEAD_H], fill=INK + (255,))
    date_font = font(BOLD, 38)
    date_text = "THURSDAY, 19 NOVEMBER 2026"
    dw = draw.textlength(date_text, font=date_font)
    draw.text(((W - dw) / 2, 26), date_text, font=date_font, fill=WHITE)
    draw.rectangle([MARGIN, MASTHEAD_H, W - MARGIN, MASTHEAD_H + 4],
                   fill=AMBER + (255,))

    # ---- Gradient over the lower hero so the headline reads ----
    # A power curve darkens fast enough that the amber kicker already sits
    # on a dimmed photo, while the skyline stays visible above it.
    grad_top = HERO_TOP + 120
    grad_bottom = HERO_TOP + HERO_H
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(grad_top, grad_bottom):
        t = (y - grad_top) / (grad_bottom - grad_top)
        a = int(255 * (t ** 0.6))
        od.line([(0, y), (W, y)], fill=INK + (a,))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    # ---- Kicker + headline + standfirst, over the hero ----
    # All three sit inside the hero band (which ends at HERO_TOP + HERO_H),
    # so the pale standfirst never spills onto the white grid below.
    y = HERO_TOP + 292
    kicker_font = font(BOLD, 26)
    draw.text((MARGIN, y), "FIRST-EVER TRILATERAL \u00b7 APEC, SHENZHEN",
              font=kicker_font, fill=AMBER)
    y += 40
    hl_font = font(BOLD, 58)
    for line in ("TRUMP, XI AND PUTIN", "MEET IN SHENZHEN"):
        draw.text((MARGIN, y), line, font=hl_font, fill=WHITE)
        y += 64
    y += 2
    sub_font = font(REG, 23)
    sub = "Nuclear arms top the agenda; Ukraine and Iran loom over the talks."
    draw.text((MARGIN, y), sub, font=sub_font, fill=(232, 234, 237))

    # ---- Six-story grid on white newsprint ----
    grid_top = HERO_TOP + HERO_H + 18
    col_w = (CONTENT_W - 32) // 2
    row_h = 116
    row_gap = 10
    stories = [
        ("UKRAINE", (198, 40, 40), "Kerch Bridge hit again",
         "Overnight strike halts traffic; rail span reported hit days "
         "after a road section fell."),
        ("THE HAGUE", (30, 90, 180), "ICJ rules on Rohingya",
         "World court gives its judgment today in The Gambia's genocide "
         "case against Myanmar."),
        ("BANGLADESH", (200, 110, 0), "Troops out in Bangladesh",
         "Forces deploy nationwide ahead of a Hasina supporters' shutdown; "
         "blasts hit 28 districts."),
        ("CLIMATE", (30, 130, 70), "COP31 talks press on",
         "Antalya summit pushes climate finance and a new global "
         "stocktake as deadlines near."),
        ("TRADE", (0, 120, 120), "EU\u2013Indonesia pact cleared",
         "Duties to fall on 90% of goods; Indonesia's 50% car tariff "
         "phased out in five years."),
        ("CULTURE", (110, 70, 160), "GTA VI launches today",
         "Rockstar's first new Grand Theft Auto in 13 years arrives with "
         "12m pre-orders."),
    ]
    tag_font = font(BOLD, 19)
    title_font = font(BOLD, 24)
    sum_font = font(REG, 19)
    for i, (tag, colour, title, summary) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 32)
        cy = grid_top + row * (row_h + row_gap)
        # Hairline above each card except the first row.
        if row > 0:
            draw.line([(x, cy - 6), (x + col_w, cy - 6)], fill=LINE, width=1)
        draw.text((x, cy), tag, font=tag_font, fill=colour)
        ty = cy + 26
        draw.text((x, ty), title, font=title_font, fill=INK)
        sy = ty + 32
        for line in wrap(draw, summary, sum_font, col_w)[:2]:
            draw.text((x, sy), line, font=sum_font, fill=GREY)
            sy += 25

    # ---- Also-today footer line ----
    fy = grid_top + 3 * row_h + 2 * row_gap + 8
    draw.line([(MARGIN, fy - 8), (W - MARGIN, fy - 8)], fill=LINE, width=1)
    foot_font = font(REG, 20)
    foot = ("ALSO TODAY: Van Gogh sells for a record $190.4m \u00b7 IAEA "
            "warns on North Korea")
    draw.text((MARGIN, fy), foot, font=foot_font, fill=GREY)

    img = img.convert("RGB")

    # ---- Save: PNG if it fits in 1 MiB, else JPEG bytes in the same name ----
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    if buf.tell() <= 1048576:
        data = buf.getvalue()
    else:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=88)
        data = buf.getvalue()
    with open(OUT_PATH, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
