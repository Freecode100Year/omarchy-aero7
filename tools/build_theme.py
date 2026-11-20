#!/usr/bin/env python3
"""Builds theme/aero7/ (colors.toml, shell.toml, preview.png) and checks contrast.

    python3 tools/build_theme.py /path/to/omarchy        # build
    python3 tools/build_theme.py --check                 # only the contrast check

shell.toml is rendered with Omarchy's own template renderer from the checkout given
(so every key Omarchy knows about is present), then the Aero glass values below are
written over it. Run tools/make_wallpapers.py first for the preview background.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEME = ROOT / "theme" / "aero7"

# Light window content with Aero blue chrome, as in the design document:
# primary #74B8E8, deep accent #245A91, highlight #D8F0FF, glass #8AB9D8, dark text #172B40.
COLORS = {
    "mode": "light",
    "accent": "#245a91", "selection": "#c4e0f6", "muted": "#566d84",
    "background": "#f4f9fd", "dark_background": "#e4eff8", "darker_background": "#d3e4f2",
    "lighter_background": "#ffffff",
    "foreground": "#172b40", "dark_foreground": "#3b536b", "light_foreground": "#10202f",
    "bright_foreground": "#0a1520",
    "red": "#b0261c", "yellow": "#755600", "orange": "#9c4600", "green": "#2b661c",
    "cyan": "#0b6474", "blue": "#245a91", "magenta": "#782d8a", "brown": "#6b4a2b",
    "bright_red": "#931f17", "bright_yellow": "#604700", "bright_green": "#235516",
    "bright_cyan": "#085462", "bright_blue": "#1b4a7a", "bright_magenta": "#652576",
    # Window border: white highlight running into Aero blue, like the glass rim.
    "hyprland_active_border": "rgba(d8f0ffee) rgba(74b8e8ee) 90deg",
    "hyprland_inactive_border": "rgba(8ab9d899)",
}
ORDER = ["mode", "", "accent", "selection", "muted", "", "background", "dark_background", "darker_background",
         "lighter_background", "", "foreground", "dark_foreground", "light_foreground", "bright_foreground", "",
         "red", "yellow", "orange", "green", "cyan", "blue", "magenta", "brown", "", "bright_red", "bright_yellow",
         "bright_green", "bright_cyan", "bright_blue", "bright_magenta", "", "hyprland_active_border",
         "hyprland_inactive_border"]

GLASS_RIM = "rgba(ffffffd9) rgba(74b8e8d9) 90deg"
# section -> key -> value written over Omarchy's generated shell.toml
SHELL = {
    # Omarchy's bar panels (battery, network, audio...) draw their text in bar.text
    # on the popups background, so bar.text must be dark like the other text. The
    # glassy bar picks a legible text colour over the wallpaper by itself (dark
    # bar.text or the light theme background), and the opaque bar is light glass.
    "bar": {"background": "#dcecf8", "background-alpha": 0.9, "text": "#172b40", "active": "#b0261c", "size-horizontal": 32},
    "popups": {"background": "#eaf5fd", "background-alpha": 0.9, "border": GLASS_RIM},
    "tooltip": {"background": "#f7fbfe", "background-alpha": 0.96},
    "notifications": {"background": "#eaf5fd", "background-alpha": 0.9, "border": GLASS_RIM},
    "launcher": {"background": "#e3f1fc", "background-alpha": 0.86, "border": GLASS_RIM,
                 "selected-background": "#74b8e8", "selected-background-alpha": 0.32,
                 "selected-text": "#10324f", "selected-border": "#74b8e8", "selected-border-alpha": 0.9},
    "menu": {"background": "#e3f1fc", "background-alpha": 0.88, "border": GLASS_RIM,
             "selected-background": "#74b8e8", "selected-background-alpha": 0.32,
             "selected-text": "#10324f", "selected-border": "#74b8e8", "selected-border-alpha": 0.9},
    "polkit": {"background": "#eaf5fd", "background-alpha": 0.94, "border": GLASS_RIM},
    "lock": {"background": "#eaf5fd", "background-alpha": 0.8, "border": GLASS_RIM},
}


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(h):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def blend(fg, bg, alpha):
    """Colour of a surface `fg` at `alpha` over `bg`."""
    return "#" + "".join(f"{round(a * alpha + b * (1 - alpha)):02x}" for a, b in zip(rgb(fg), rgb(bg)))


def _darker(h, f=1.4):
    """Qt.darker(colour, 1.4), which the bar panels use for secondary labels (HSV value / f)."""
    import colorsys
    r, g, b = (v / 255 for v in rgb(h))
    hh, ss, vv = colorsys.rgb_to_hsv(r, g, b)
    r, g, b = colorsys.hsv_to_rgb(hh, ss, vv / f)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def check():
    bad = []
    c = COLORS
    for bg in ("background", "dark_background", "lighter_background"):
        for k in ("foreground", "light_foreground", "bright_foreground"):
            if contrast(c[k], c[bg]) < 7:
                bad.append(f"{k} on {bg}: {contrast(c[k], c[bg]):.2f} < 7")
        for k in ("dark_foreground", "muted", "accent", "red", "yellow", "orange", "green", "cyan", "blue",
                  "magenta", "bright_red", "bright_yellow", "bright_green", "bright_cyan", "bright_blue",
                  "bright_magenta"):
            if contrast(c[k], c[bg]) < 4.5:
                bad.append(f"{k} on {bg}: {contrast(c[k], c[bg]):.2f} < 4.5")
    if contrast(c["foreground"], c["selection"]) < 4.5:
        bad.append("foreground on selection < 4.5")
    # Glass surfaces are see-through: check text against them over both the
    # darkest and the lightest part of the wallpaper.
    # The bar reserves its own strip of screen, so only the wallpaper is behind it;
    # menus and panels can float over anything.
    bar = SHELL["bar"]
    opaque = bar["background"]  # `omarchy bar background opaque` (the solid level)
    if contrast(bar["text"], opaque) < 4.5:
        bad.append(f"opaque bar text: {contrast(bar['text'], opaque):.2f} < 4.5")
    if contrast(bar["active"], opaque) < 3:
        bad.append(f"opaque bar alert colour: {contrast(bar['active'], opaque):.2f} < 3")
    for wall in ("#082c5c", "#8ccaf0", "#ffffff", "#000000"):
        # Glassy bar: Omarchy draws the bar colour at no more than 35% and picks the
        # more legible of bar.text and the theme background for the text.
        glass = blend(bar["background"], wall, min(bar["background-alpha"], 0.35))
        best = max(contrast(bar["text"], glass), contrast(c["background"], glass))
        if best < 4.5:
            bad.append(f"glassy bar text over {wall}: {best:.2f} < 4.5")
        # Bar panels: bar.text on the popups surface (the bug users saw in v1.0/v1.1).
        panel = blend(SHELL["popups"]["background"], wall, SHELL["popups"]["background-alpha"])
        if contrast(bar["text"], panel) < 7:
            bad.append(f"bar panel text over {wall}: {contrast(bar['text'], panel):.2f} < 7")
        if contrast(_darker(bar["text"]), panel) < 7:
            bad.append(f"bar panel labels over {wall}: {contrast(_darker(bar['text']), panel):.2f} < 7")
        for s in ("menu", "launcher", "notifications", "popups"):
            surf = blend(SHELL[s]["background"], wall, SHELL[s]["background-alpha"])
            if contrast(c["foreground"], surf) < 7:
                bad.append(f"{s} text over {wall}: {contrast(c['foreground'], surf):.2f} < 7")
        for s in ("menu", "launcher"):
            surf = blend(SHELL[s]["background"], wall, SHELL[s]["background-alpha"])
            sel = blend(SHELL[s]["selected-background"], surf, SHELL[s]["selected-background-alpha"])
            if contrast(SHELL[s]["selected-text"], sel) < 7:
                bad.append(f"{s} selected text over {wall}: {contrast(SHELL[s]['selected-text'], sel):.2f} < 7")
    return bad


def write_colors():
    THEME.mkdir(parents=True, exist_ok=True)
    lines = ["# Omarchy Aero7 — style after the Windows 7 Aero look. Generated by tools/build_theme.py."]
    lines += ["" if k == "" else f'{k} = "{COLORS[k]}"' for k in ORDER]
    (THEME / "colors.toml").write_text("\n".join(lines) + "\n")


def render_shell(omarchy):
    """Render Omarchy's shell.toml template for our colors.toml, then apply SHELL."""
    with tempfile.TemporaryDirectory() as home:
        nxt = Path(home) / ".local/state/omarchy/current/next-theme"
        nxt.mkdir(parents=True)
        shutil.copy(THEME / "colors.toml", nxt / "colors.toml")
        env = dict(os.environ, HOME=home, OMARCHY_PATH=str(omarchy),
                   PATH=f"{omarchy}/bin:" + os.environ["PATH"])
        subprocess.run(["bash", f"{omarchy}/bin/omarchy-theme-set-templates"], env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        text = (nxt / "shell.toml").read_text()
    section = ""
    out = []
    seen = set()
    for line in text.splitlines():
        m = re.match(r"^\[([A-Za-z0-9_-]+)\]", line.strip())
        if m:
            section = m.group(1)
        kv = re.match(r"^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)(.*)$", line)
        if kv and section in SHELL and kv.group(2) in SHELL[section]:
            v = SHELL[section][kv.group(2)]
            v = f'"{v}"' if isinstance(v, str) else str(v)
            line = f"{kv.group(1)}{kv.group(2)}{kv.group(3)}{v}"
            seen.add((section, kv.group(2)))
        out.append(line)
    missing = [f"{s}.{k}" for s in SHELL for k in SHELL[s] if (s, k) not in seen]
    if missing:
        sys.exit("Omarchy's shell.toml no longer has: " + ", ".join(missing))
    header = ("# Omarchy Aero7 glass surfaces. Rendered from Omarchy's shell.toml template by\n"
              "# tools/build_theme.py, with the Aero values written over it.\n")
    (THEME / "shell.toml").write_text(header + "\n".join(out) + "\n")


def write_preview():
    from PIL import Image, ImageDraw
    thumb = ROOT / "tools" / ".wallpaper-thumb.png"
    im = Image.open(thumb).convert("RGBA")
    over = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    w, h = im.size
    # A glass window
    d.rounded_rectangle((120, 60, 520, 290), 7, fill=(244, 249, 253, 235), outline=(116, 184, 232, 255), width=2)
    d.rectangle((122, 62, 518, 90), fill=(216, 240, 255, 150))
    for i, ln in enumerate((300, 260, 330, 220, 280)):
        d.rectangle((140, 110 + i * 30, 140 + ln, 122 + i * 30), fill=(23, 43, 64, 255))
    # The taskbar at the bottom with its light top rim
    d.rectangle((0, h - 26, w, h), fill=(29, 79, 130, 150))
    d.line((0, h - 26, w, h - 26), fill=(255, 255, 255, 170), width=1)
    d.ellipse((6, h - 23, 26, h - 3), fill=(116, 184, 232, 255), outline=(216, 240, 255, 255))
    for i in range(4):
        d.rounded_rectangle((40 + i * 34, h - 22, 68 + i * 34, h - 4), 3,
                            fill=(255, 255, 255, 60 if i else 110))
    Image.alpha_composite(im, over).convert("RGB").save(THEME / "preview.png")


if __name__ == "__main__":
    if "--check" not in sys.argv:
        if len(sys.argv) < 2:
            sys.exit("usage: build_theme.py /path/to/omarchy-checkout | --check")
        write_colors()
        render_shell(Path(sys.argv[1]).resolve())
        write_preview()
    problems = check()
    for p in problems:
        print("FAIL", p)
    if problems:
        sys.exit(1)
    print(f"contrast ok: text {contrast(COLORS['foreground'], COLORS['background']):.1f}:1, "
          f"bar panel text {contrast(SHELL['bar']['text'], SHELL['popups']['background']):.1f}:1, "
          f"opaque bar text {contrast(SHELL['bar']['text'], SHELL['bar']['background']):.1f}:1")
