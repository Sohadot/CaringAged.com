#!/usr/bin/env python3
"""Generate CaringAged's deterministic 1200x630 PNG social-sharing image.

Uses only Pillow and available open-source system fonts. No remote images or
privacy-sensitive photography. The asset is part of the source tree after the
branch-only generator workflow commits it.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "og" / "caringaged-share.png"
WIDTH, HEIGHT = 1200, 630

def font(paths: list[str], size: int) -> ImageFont.FreeTypeFont:
    for name in paths:
        p = Path(name)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise RuntimeError("Required open-source system font is unavailable")

def main() -> None:
    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#F7F6EF")
    draw = ImageDraw.Draw(canvas)
    pine = "#173A34"
    accent = "#C97854"
    draw.rounded_rectangle((56, 50, 1144, 582), radius=34, fill="#FEFDF8", outline="#E0E7DF", width=2)
    draw.rounded_rectangle((78, 74, 1122, 556), radius=24, fill="#F9FAF4")

    # Layered conceptual instrument: individual at the centre of care pathways.
    for radius, color in [(435, "#DFE9DF"), (355, "#E8F0E5"), (275, "#E0EADF"), (190, "#F1F4EB")]:
        cx, cy = 1030, 307
        draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), fill=color)
    cx, cy = 975, 320
    draw.ellipse((cx-131, cy-131, cx+131, cy+131), fill=pine)
    draw.ellipse((cx-102, cy-102, cx+102, cy+102), outline="#B2D0B9", width=2)
    draw.ellipse((955, 245, 996, 286), fill="#F7F6EE")
    draw.arc((907, 287, 1042, 400), 190, 350, fill="#F7F6EE", width=11)
    draw.arc((917, 337, 1032, 420), 200, 340, fill="#F7F6EE", width=9)
    for x, y in [(975, 151), (1145, 320), (975, 486), (813, 320)]:
        draw.ellipse((x-11, y-11, x+11, y+11), fill=accent, outline="#F9FAF4", width=3)

    draw.line((111, 470, 695, 470), fill="#D5E0D5", width=2)
    draw.rectangle((111, 113, 121, 123), fill=accent)

    serif = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
             "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf"]
    sans = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    sans_bold = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    draw.text((136, 102), "CARINGAGED.COM", font=font(sans_bold, 17), fill=pine)
    draw.text((108, 184), "CaringAged", font=font(serif, 79), fill=pine)
    draw.text((111, 300), "A clearer path through", font=font(serif, 37), fill=pine)
    draw.text((111, 354), "later-life care.", font=font(serif, 37), fill=pine)
    draw.text((111, 493), "INDEPENDENCE  •  DIGNITY  •  CLARITY", font=font(sans, 17), fill="#65796C")
    draw.text((809, 516), "A SOHADOT DIGITAL ASSET", font=font(sans_bold, 16), fill="#527267")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Indexed PNG is small and social-crawler friendly, with no external assets.
    canvas.quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(
        OUT, format="PNG", optimize=True
    )
    rendered = Image.open(OUT)
    assert rendered.size == (WIDTH, HEIGHT)
    assert rendered.format == "PNG"
    print(f"Rendered {OUT.relative_to(ROOT)}: {WIDTH}x{HEIGHT}, {OUT.stat().st_size} bytes")

if __name__ == "__main__":
    main()
