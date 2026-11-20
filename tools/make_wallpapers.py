#!/usr/bin/env python3
"""Draws the Aero7 wallpapers from scratch (no third-party artwork): a blue sky
gradient, soft ribbons of light, out-of-focus glints and a gentle vignette.

    python3 tools/make_wallpapers.py      # needs python3-numpy and python3-pil

Writes theme/aero7/backgrounds/{1-aero-blue,2-aero-dusk}.webp at 3840x2160 for the
Omarchy theme, and wallpapers/aero-<variant>-<WxH>.webp at 1080p / 1440p / 4K.
The drawing is resolution independent and seeded, so every size shows the same picture.
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

VARIANTS = {
    # sky stops (position 0 = top, 1 = bottom), ribbon tint, glint tint
    "blue": {
        "sky": [(0.0, "#082c5c"), (0.45, "#155c9c"), (0.78, "#3b94cf"), (1.0, "#8ccaf0")],
        "ribbon": "#d8f0ff", "glint": "#bfe6ff", "seed": 7,
    },
    "dusk": {
        "sky": [(0.0, "#071a3a"), (0.5, "#1b3f7a"), (0.8, "#3e6fae"), (1.0, "#9fb9de")],
        "ribbon": "#e6f2ff", "glint": "#ffe9c8", "seed": 11,
    },
}

SIZES = [(1920, 1080), (2560, 1440), (3840, 2160)]


def hex_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], dtype=np.float32)


def draw(w, h, v):
    rng = np.random.default_rng(v["seed"])
    # Normalised coordinates: x in [0, 16/9], y in [0, 1], independent of resolution.
    ys = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    xs = np.linspace(0, w / h, w, dtype=np.float32)[None, :]
    X = np.broadcast_to(xs, (h, w))
    Y = np.broadcast_to(ys, (h, w))

    # Sky gradient, slightly brighter towards the lower right.
    stops = v["sky"]
    pos = np.array([p for p, _ in stops], dtype=np.float32)
    cols = np.stack([hex_rgb(c) for _, c in stops])
    t = np.clip(Y * 0.85 + (X / (w / h)) * 0.15, 0, 1)
    img = np.stack([np.interp(t, pos, cols[:, k]) for k in range(3)], axis=-1).astype(np.float32)

    # Ribbons of light: flowing bands with a soft glow and a thin bright core.
    tint = hex_rgb(v["ribbon"])
    light = np.zeros((h, w), dtype=np.float32)
    for i in range(5):
        amp = rng.uniform(0.05, 0.13)
        freq = rng.uniform(1.6, 2.8)
        phase = rng.uniform(0, 2 * np.pi)
        base = 0.42 + i * 0.075 + rng.uniform(-0.02, 0.02)
        tilt = rng.uniform(-0.12, -0.04)
        centre = base + tilt * X + amp * np.sin(freq * X + phase)
        d = Y - centre
        width = rng.uniform(0.035, 0.07)
        glow = np.exp(-(d / width) ** 2) * rng.uniform(0.18, 0.32)
        core = np.exp(-(d / (width * 0.12)) ** 2) * rng.uniform(0.25, 0.45)
        fade = np.clip(1.2 - np.abs(X - (w / h) * 0.55) / (w / h) * 1.6, 0, 1)  # fade at the edges
        light += (glow + core) * fade
    img = img + light[..., None] * tint * 0.9

    # Out-of-focus glints along the ribbons.
    gl = hex_rgb(v["glint"])
    glints = np.zeros((h, w), dtype=np.float32)
    for _ in range(26):
        cx = rng.uniform(0.1, w / h - 0.1)
        cy = rng.uniform(0.35, 0.85)
        r = rng.uniform(0.008, 0.035)
        a = rng.uniform(0.05, 0.16)
        y0, y1 = max(0, int((cy - r * 2) * h)), min(h, int((cy + r * 2) * h) + 1)
        x0, x1 = max(0, int((cx - r * 2) * h)), min(w, int((cx + r * 2) * h) + 1)
        dd = np.sqrt((X[y0:y1, x0:x1] - cx) ** 2 + (Y[y0:y1, x0:x1] - cy) ** 2) / r
        glints[y0:y1, x0:x1] += a * np.clip(1.15 - dd, 0, 1) ** 0.6 * (dd < 1.15)
    img = img + glints[..., None] * gl

    # Vignette and a whisper of noise against banding.
    vx = (X / (w / h) - 0.5) * 1.4
    vy = (Y - 0.55) * 1.6
    img = img * (1 - 0.28 * np.clip(vx ** 2 + vy ** 2, 0, 1))[..., None]
    img = img + rng.normal(0, 1.2 / 255, img.shape).astype(np.float32)
    return Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8), "RGB")


def main():
    (ROOT / "wallpapers").mkdir(exist_ok=True)
    bg = ROOT / "theme" / "aero7" / "backgrounds"
    bg.mkdir(parents=True, exist_ok=True)
    for n, (name, v) in enumerate(VARIANTS.items(), start=1):
        for w, h in SIZES:
            im = draw(w, h, v)
            im.save(ROOT / "wallpapers" / f"aero-{name}-{w}x{h}.webp", quality=90, method=6)
            if (w, h) == (3840, 2160):
                im.save(bg / f"{n}-aero-{name}.webp", quality=90, method=6)
                if name == "blue":
                    im.resize((640, 360), Image.LANCZOS).save(ROOT / "tools" / ".wallpaper-thumb.png")
        print("drew", name)


if __name__ == "__main__":
    main()
