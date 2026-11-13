"""Build single-screen report figures from the captured screens.

Requires Pillow and the PNGs from scripts/capture.sh.
Outputs to report/figures/:
  screen-<name>.png          one framed screen per file
  norman-<principle>.png     one screen per principle, numbered markers
The hand-drawn process figures come from scripts/build_sketches.sh.
Run:  python3 scripts/build_figures.py
"""
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PNG = ROOT / "figma" / "png"
OUT = ROOT / "report" / "figures"
ARIAL_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SCALE = 2  # screenshots are @2x

SCREENS = ["01-today", "02-plan", "03-step", "04-focus", "04b-focus-paused", "05-rest",
           "06-calm", "06b-calm-muted", "07-settings", "07b-settings-applied", "08-progress", "00-today-dashboard"]

# Boxes in 430 x 932 CSS px, measured from the DOM in headless Chrome after fonts load.
NORMAN = {
    "visibility": ("01-today", (37, 99, 235), [(20, 356, 390, 230), (327, 64, 83, 36)]),
    "feedback": ("04-focus", (22, 163, 74), [(107, 255, 216, 216), (20, 510, 390, 52)]),
    "constraints": ("03-step", (220, 38, 38), [(20, 114, 326, 27), (20, 235, 390, 261), (20, 677, 390, 44)]),
    "consistency": ("07b-settings-applied", (217, 119, 6), [(37, 544, 356, 48), (37, 667, 356, 48), (0, 846, 430, 86), (328, 64, 82, 36)]),
    "affordance": ("06-calm", (147, 51, 234), [(20, 460, 390, 52), (343, 547, 50, 30), (20, 755, 390, 69)]),
}


def framed(img):
    """Plain thin grey border, no rounded corners."""
    out = img.copy()
    ImageDraw.Draw(out).rectangle([0, 0, out.width - 1, out.height - 1], outline=(150, 150, 150), width=3)
    return out


def pad(img, p=16):
    out = Image.new("RGB", (img.width + 2 * p, img.height + 2 * p), (255, 255, 255))
    out.paste(img, (p, p))
    return out


def screen(name):
    return framed(Image.open(PNG / f"{name}.png").convert("RGB"))


def annotate(name, colour, boxes):
    img = screen(name)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(ARIAL_B, 30)
    for i, (x, y, w, h) in enumerate(boxes, 1):
        x, y, w, h = (v * SCALE for v in (x, y, w, h))
        d.rounded_rectangle([x - 6, y - 6, x + w + 6, y + h + 6], 22, outline=colour, width=7)
        r = 26
        bx, by = min(x + w - 4, img.width - r - 6), max(y - 4, r + 6)
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=colour)
        d.text((bx, by), str(i), fill=(255, 255, 255), font=font, anchor="mm")
    return img


FLOWS = {
    "flow-planning": [("01-today", "Today"), ("03-step", "Step"), ("04-focus", "Focus"), ("04b-focus-paused", "Paused"), ("05-rest", "Rest")],
    "flow-overload": [("01-today", "Any screen"), ("06-calm", "Calm"), ("06b-calm-muted", "Quiet mode"), ("08-progress", "Progress")],
    "flow-personalise": [("02-plan", "Plan"), ("07-settings", "Settings"), ("07b-settings-applied", "Settings applied")],
}
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"


def flow(items, w=330, gap=80, label_h=50, p=10):
    """Screens of one journey in order with plain arrows: a basic report diagram."""
    shots = []
    for n, _ in items:
        img = Image.open(PNG / f"{n}.png").convert("RGB").resize((w, round(1864 * w / 860)), Image.LANCZOS)
        ImageDraw.Draw(img).rectangle([0, 0, img.width - 1, img.height - 1], outline=(150, 150, 150), width=2)
        shots.append(img)
    h = shots[0].height
    W = 2 * p + len(shots) * w + (len(shots) - 1) * gap
    canvas = Image.new("RGB", (W, 2 * p + h + label_h), (255, 255, 255))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(ARIAL, 24)
    for i, (shot, (_, label)) in enumerate(zip(shots, items)):
        x = p + i * (w + gap)
        canvas.paste(shot, (x, p))
        d.text((x + w / 2, p + h + label_h / 2 + 2), label, fill=(0, 0, 0), font=font, anchor="mm")
        if i < len(shots) - 1:
            y, x1, x2 = p + h / 2, x + w + 12, x + w + gap - 12
            d.line([(x1, y), (x2, y)], fill=(0, 0, 0), width=3)
            d.line([(x2 - 12, y - 9), (x2, y), (x2 - 12, y + 9)], fill=(0, 0, 0), width=3)
    return canvas


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for old in list(OUT.glob("fig-*.png")):
        old.unlink()
    shutil.rmtree(OUT / "_src", ignore_errors=True)
    for n in SCREENS:
        pad(screen(n)).save(OUT / f"screen-{n}.png", dpi=(200, 200))
    for key, (n, colour, boxes) in NORMAN.items():
        pad(annotate(n, colour, boxes)).save(OUT / f"norman-{key}.png", dpi=(200, 200))
    for key, items in FLOWS.items():
        flow(items).save(OUT / f"{key}.png", dpi=(200, 200))
    print("figures written to", OUT)
