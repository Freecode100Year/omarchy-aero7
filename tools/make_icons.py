#!/usr/bin/env python3
"""Draws the Aero7 icon set: glossy glass tiles with white pictograms, one SVG per
app icon Omarchy's own sets cover (tools/icon-names.txt), plus the project logo.

    python3 tools/make_icons.py     # then tools/optimize_svg.sh (SVGO) and the previews

Everything is drawn from scratch: brand apps get a generic pictogram of what they do
(a chat bubble, a play button, a globe...), never someone else's logo. The SVGs stay
inside SVG Tiny (gradients, paths, no filters, masks or clip paths), so the Omarchy
shell (Qt SVG), GTK (librsvg) and browsers all draw them the same.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "icons" / "aero7"

# Aero glass colours: (top, bottom) of each tile.
PALETTE = {
    "blue": ("#6fc3ff", "#1b5fae"),
    "sky": ("#9ee2ff", "#2a8fd0"),
    "teal": ("#6fe3d8", "#0f7f86"),
    "green": ("#9be37a", "#2b8a2f"),
    "lime": ("#d4f070", "#6e9a14"),
    "gold": ("#ffe07a", "#c38610"),
    "orange": ("#ffc06a", "#d4600f"),
    "red": ("#ff9a8a", "#b8231c"),
    "pink": ("#ffa6d8", "#b52a7d"),
    "purple": ("#c9a6ff", "#5b2fb0"),
    "indigo": ("#9db0ff", "#2f3fa8"),
    "graphite": ("#b9c6d4", "#3e4c5c"),
    "night": ("#6a86b8", "#14213f"),
}

W = 28  # stroke width of the pictograms

# Pictograms on a 512 grid, drawn in white strokes inside the 128..384 square.
def P(d, fill=False, width=W):
    return ("f" if fill else "s", d, width)

GLYPHS = {
    "terminal": [P("M150 150h212a20 20 0 0 1 20 20v172a20 20 0 0 1-20 20H150a20 20 0 0 1-20-20V170a20 20 0 0 1 20-20z"), P("M176 214l44 38-44 38"), P("M244 300h72")],
    "globe": [P("M256 136a120 120 0 1 0 0.1 0z"), P("M256 136c-44 34-60 78-60 120s16 86 60 120c44-34 60-78 60-120s-16-86-60-120z"), P("M140 216h232M140 296h232")],
    "bubble": [P("M150 160h212a30 30 0 0 1 30 30v116a30 30 0 0 1-30 30H232l-62 44v-44h-20a30 30 0 0 1-30-30V190a30 30 0 0 1 30-30z")],
    "bubbles": [P("M136 150h160a26 26 0 0 1 26 26v88a26 26 0 0 1-26 26h-96l-44 32v-32h-20a26 26 0 0 1-26-26v-88a26 26 0 0 1 26-26z"), P("M346 216h20a26 26 0 0 1 26 26v80a26 26 0 0 1-26 26h-12v30l-40-30h-76")],
    "note": [P("M226 330V160l132-28v168"), P("M190 330a36 30 0 1 0 72 0a36 30 0 1 0-72 0z", fill=True), P("M322 300a36 30 0 1 0 72 0a36 30 0 1 0-72 0z", fill=True)],
    "play": [P("M200 152l160 104-160 104z", fill=True)],
    "screen-play": [P("M136 156h240a20 20 0 0 1 20 20v140a20 20 0 0 1-20 20H136a20 20 0 0 1-20-20V176a20 20 0 0 1 20-20z"), P("M232 206l64 40-64 40z", fill=True), P("M200 372h112")],
    "film": [P("M160 132h192v248H160z"), P("M160 196h192M160 316h192"), P("M190 152v20M190 340v20M322 152v20M322 340v20", width=18)],
    "doc": [P("M176 124h120l60 60v204H176z"), P("M296 124v60h60"), P("M212 240h108M212 284h108M212 328h72")],
    "docs": [P("M150 150h132l48 48v190H150z"), P("M330 150h32v222"), P("M186 250h108M186 294h108M186 338h64")],
    "sheet": [P("M144 152h224v208H144z"), P("M144 208h224M144 262h224M144 312h224M216 152v208M292 152v208")],
    "slides": [P("M128 148h256v156H128z"), P("M256 304v60M210 380l46-16 46 16"), P("M168 270l48-48 36 30 56-60", width=24)],
    "photo": [P("M132 160h248v192H132z"), P("M132 318l78-76 60 58 40-34 70 60", width=24), P("M300 206a22 22 0 1 0 0.1 0z", fill=True)],
    "folder": [P("M128 176v-24a12 12 0 0 1 12-12h80l28 32h124a12 12 0 0 1 12 12v176a12 12 0 0 1-12 12H140a12 12 0 0 1-12-12z"), P("M128 216h256")],
    "drive": [P("M140 196h232l-24-56H164z"), P("M140 196v148a12 12 0 0 0 12 12h208a12 12 0 0 0 12-12V196z"), P("M318 296a14 14 0 1 0 0.1 0z", fill=True)],
    "treemap": [P("M136 140h240v232H136z"), P("M256 140v232M136 270h120M256 220h120M316 220v152")],
    "printer": [P("M176 212v-76h160v76"), P("M136 212h240v108h-40M176 320h-40V212"), P("M176 280h160v100H176z")],
    "graph": [P("M136 136v240h240"), P("M168 316l56-72 48 40 80-104", width=26), P("M332 180h28v28", width=24)],
    "brush": [P("M352 136L232 268"), P("M230 268c-34 0-60 26-60 58 0 20-14 34-38 40 46 20 122 14 134-38z", fill=True)],
    "record": [P("M256 136a120 120 0 1 0 0.1 0z"), P("M256 206a50 50 0 1 0 0.1 0z", fill=True)],
    "wave": [P("M152 236v40M200 196v120M248 156v200M296 204v104M344 228v56")],
    "key": [P("M196 196a60 60 0 1 0 0.1 0z"), P("M238 296l120 0v44M318 296v32")],
    "lock": [P("M156 236h200v140H156z"), P("M196 236v-40a60 60 0 0 1 120 0v40"), P("M256 290v36")],
    "shield": [P("M256 128l112 40v80c0 74-48 120-112 140-64-20-112-66-112-140v-80z"), P("M206 258l36 36 66-70")],
    "nodes": [P("M178 178a26 26 0 1 0 0.1 0zM334 178a26 26 0 1 0 0.1 0zM256 334a26 26 0 1 0 0.1 0z", fill=True), P("M178 204v40l78 64M334 204v40l-78 64M204 178h104")],
    "king": [P("M256 120v52M230 146h52"), P("M196 352l18-140h84l18 140z"), P("M172 380h168")],
    "card": [P("M180 128h152a16 16 0 0 1 16 16v224a16 16 0 0 1-16 16H180a16 16 0 0 1-16-16V144a16 16 0 0 1 16-16z"), P("M256 200c-30 30-48 50-48 72a24 24 0 0 0 48 0a24 24 0 0 0 48 0c0-22-18-42-48-72z", fill=True)],
    "gamepad": [P("M188 196h136c48 0 72 52 72 104 0 44-40 56-64 22l-28-38h-96l-28 38c-24 34-64 22-64-22 0-52 24-104 72-104z"), P("M194 246v52M168 272h52"), P("M318 258a10 10 0 1 0 0.1 0zM344 286a10 10 0 1 0 0.1 0z", fill=True)],
    "calc": [P("M168 124h176v264H168z"), P("M196 156h120v52H196z"), P("M206 256h0M256 256h0M306 256h0M206 302h0M256 302h0M306 302h0M206 348h0M256 348h0M306 348h0", width=34)],
    "pin": [P("M256 384c-56-72-96-118-96-168a96 96 0 0 1 192 0c0 50-40 96-96 168z"), P("M256 216a34 34 0 1 0 0.1 0z", fill=True)],
    "person": [P("M256 160a52 52 0 1 0 0.1 0z"), P("M156 380c0-64 44-104 100-104s100 40 100 104")],
    "flower": [P("M256 256m-30 0a30 30 0 1 0 60 0a30 30 0 1 0-60 0", fill=True), P("M256 226c-40-60 0-100 0-100s40 40 0 100M286 256c60-40 100 0 100 0s-40 40-100 0M256 286c40 60 0 100 0 100s-40-40 0-100M226 256c-60 40-100 0-100 0s40-40 100 0", width=22)],
    "code": [P("M204 178l-72 78 72 78M308 178l72 78-72 78"), P("M276 150l-40 212")],
    "sparkle": [P("M256 128c12 76 52 116 128 128-76 12-116 52-128 128-12-76-52-116-128-128 76-12 116-52 128-128z", fill=True)],
    "robot": [P("M164 200h184a20 20 0 0 1 20 20v120a20 20 0 0 1-20 20H164a20 20 0 0 1-20-20V220a20 20 0 0 1 20-20z"), P("M256 200v-48M256 140a12 12 0 1 0 0.1 0"), P("M206 272a16 16 0 1 0 0.1 0zM306 272a16 16 0 1 0 0.1 0z", fill=True), P("M216 326h80", width=22)],
    "pen": [P("M180 372h176"), P("M332 124l44 44-148 148-56 12 12-56z")],
    "edit": [P("M168 128h136l40 40v212H168z"), P("M204 228h104M204 272h64"), P("M352 232l36 36-92 92-44 8 8-44z", width=22)],
    "moon": [P("M300 140a124 124 0 1 0 72 196 100 100 0 0 1-72-196z")],
    "aurora": [P("M128 300c40-60 80-60 128 0s88 60 128 0", width=26), P("M128 236c40-60 80-60 128 0s88 60 128 0", width=20), P("M128 172c40-60 80-60 128 0s88 60 128 0", width=14)],
    "monitor": [P("M128 148h256v168H128z"), P("M256 316v52M200 372h112")],
    "scissors": [P("M196 316a36 36 0 1 0 0.1 0zM196 196a36 36 0 1 0 0.1 0z"), P("M224 220l152 108M224 292l152-108")],
    "crop": [P("M176 128v208h208"), P("M128 176h208v208")],
    "send": [P("M132 256l244-112-76 240-52-92z"), P("M248 292l128-148")],
    "hand": [P("M196 380c-40-24-64-80-64-120v-60M196 300V164a20 20 0 0 1 40 0v100M236 252V140a20 20 0 0 1 40 0v112M276 252V156a20 20 0 0 1 40 0v108M316 264v-64a20 20 0 0 1 40 0v80c0 56-40 100-96 100")],
    "gem": [P("M192 148h128l56 64-120 164-120-164z"), P("M136 212h240M216 148l-24 64 64 164 64-164-24-64")],
    "lion": [P("M256 136l84 28 20 76-28 92-76 44-76-44-28-92 20-76z"), P("M220 252a12 12 0 1 0 0.1 0zM292 252a12 12 0 1 0 0.1 0z", fill=True), P("M236 316h40l-20 20z", fill=True)],
    "sun": [P("M256 206a50 50 0 1 0 0.1 0z", fill=True), P("M256 128v34M256 350v34M128 256h34M350 256h34M166 166l24 24M322 322l24 24M166 346l24-24M322 190l24-24", width=24)],
    "mail": [P("M128 168h256v176H128z"), P("M128 168l128 104 128-104")],
    "grid-dots": [P("M196 196h0M256 196h0M316 196h0M196 256h0M256 256h0M316 256h0M196 316h0M256 316h0M316 316h0", width=40)],
    "hash": [P("M164 220h196M152 292h196M236 148l-28 216M316 148l-28 216")],
    "x": [P("M168 156l176 200M344 156L168 356")],
    "video": [P("M132 192h168a20 20 0 0 1 20 20v88a20 20 0 0 1-20 20H132a20 20 0 0 1-20-20v-88a20 20 0 0 1 20-20z"), P("M320 236l80-44v128l-80-44z", fill=True)],
    "roll": [P("M256 168a88 88 0 1 0 0.1 0z"), P("M256 220a36 36 0 1 0 0.1 0z", fill=True)],
}

# icon name -> (glyph, colour)
ICONS = {
    "1password": ("key", "blue"), "aether": ("brush", "purple"), "basecamp": ("sun", "gold"),
    "brave-origin": ("lion", "orange"), "btop": ("graph", "green"), "cards": ("card", "red"),
    "chatgpt": ("sparkle", "teal"), "checkmate": ("king", "graphite"), "chromium": ("globe", "blue"),
    "cliamp": ("wave", "orange"), "com.github.PintaProject.Pinta": ("brush", "sky"),
    "com.mitchellh.ghostty": ("terminal", "night"), "com.obsproject.Studio": ("record", "graphite"),
    "disktree": ("treemap", "teal"), "fantasi": ("aurora", "night"), "folio": ("folder", "gold"),
    "foot": ("terminal", "graphite"), "gliff": ("monitor", "blue"), "google-chrome": ("globe", "green"),
    "google-contacts": ("person", "blue"), "google-maps": ("pin", "red"), "google-messages": ("bubble", "blue"),
    "google-photos": ("flower", "pink"), "gvim": ("code", "green"), "herdr": ("terminal", "lime"),
    "herdr-app": ("terminal", "lime"), "hey": ("hand", "gold"), "hype": ("slides", "pink"),
    "imv": ("photo", "sky"), "kdenlive": ("film", "indigo"), "libreoffice-calc": ("sheet", "green"),
    "libreoffice-impress": ("slides", "orange"), "libreoffice-writer": ("doc", "blue"),
    "localsend": ("send", "teal"), "monologue": ("record", "red"), "moonlight": ("moon", "night"),
    "mpv": ("screen-play", "purple"), "netflix": ("screen-play", "red"), "nvim": ("code", "teal"),
    "obsidian": ("gem", "purple"), "omacalc": ("calc", "graphite"), "omacut": ("film", "orange"),
    "omarchy-agent": ("robot", "indigo"), "omarchy-browser": ("globe", "sky"),
    "omarchy-discord": ("gamepad", "indigo"), "omarchy-game-vibes": ("gamepad", "lime"),
    "omarchy-spotify": ("note", "green"), "omarchy-terminal": ("terminal", "night"),
    "omasnap": ("crop", "sky"), "omaview": ("photo", "teal"), "omawrite": ("edit", "blue"),
    "org.gnome.DiskUtility": ("drive", "graphite"), "org.gnome.Papers": ("docs", "red"),
    "plain": ("hash", "graphite"), "printer": ("printer", "graphite"), "rawmakase": ("roll", "green"),
    "signal-desktop": ("bubble", "indigo"), "signed": ("pen", "blue"), "slack": ("hash", "purple"),
    "spotify-client": ("note", "green"), "superwhisper": ("wave", "purple"), "tailscale": ("grid-dots", "graphite"),
    "wechat": ("bubbles", "green"), "whatsapp": ("bubble", "green"), "x": ("x", "night"),
    "youtube": ("screen-play", "red"), "zoom": ("video", "blue"),
}
AGENT_COLOURS = ["purple", "indigo", "teal", "blue", "pink", "orange", "green", "sky", "gold", "red"]

TITLES = {}  # filled from the names list when run


def tile(top, bottom, uid):
    """Glass tile: gradient body, darker rim, gloss over the top half, glow at the foot."""
    return f"""  <defs>
    <linearGradient id="b{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>
    <linearGradient id="g{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".75"/><stop offset="1" stop-color="#fff" stop-opacity=".08"/></linearGradient>
    <radialGradient id="f{uid}" cx=".5" cy="1" r=".6"><stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
  </defs>
  <rect x="40" y="52" width="432" height="432" rx="96" fill="#000" opacity=".18"/>
  <rect x="40" y="40" width="432" height="432" rx="96" fill="url(#b{uid})"/>
  <rect x="40" y="40" width="432" height="432" rx="96" fill="url(#f{uid})"/>
  <path d="M136 52h240a84 84 0 0 1 84 84v74c-60-28-132-42-204-42s-144 14-204 42v-74a84 84 0 0 1 84-84z" fill="url(#g{uid})"/>
  <rect x="42" y="42" width="428" height="428" rx="94" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="4"/>
  <rect x="40" y="40" width="432" height="432" rx="96" fill="none" stroke="{bottom}" stroke-width="3"/>"""


def glyph(parts, shadow):
    out = []
    for kind, d, width in parts:
        if kind == "f":
            attrs = 'fill="{c}"'
        else:
            attrs = f'fill="none" stroke="{{c}}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"'
        out.append((d, attrs))
    s = []
    for d, a in out:  # soft shadow first, 6px lower
        s.append(f'  <path transform="translate(0 6)" opacity=".28" d="{d}" {a.format(c=shadow)}/>')
    for d, a in out:
        s.append(f'  <path d="{d}" {a.format(c="#fff")}/>')
    return "\n".join(s)


def icon_svg(name, title, glyph_name, colour):
    top, bottom = PALETTE[colour]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">\n'
            f'  <title>{title}</title>\n'
            f'  <desc>Omarchy Aero7: a {colour} glass tile with a white {glyph_name} pictogram.</desc>\n'
            f'{tile(top, bottom, "")}\n{glyph(GLYPHS[glyph_name], "#0b2a4a")}\n</svg>\n')


def logo_svg():
    """Project logo: an Aero glass orb with ribbons of light and a bold 7."""
    return """<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <title>Omarchy Aero7</title>
  <desc>A glossy blue glass orb crossed by ribbons of light, with a white 7.</desc>
  <defs>
    <radialGradient id="o" cx=".5" cy=".38" r=".62"><stop offset="0" stop-color="#9ee2ff"/><stop offset=".55" stop-color="#2f86d6"/><stop offset="1" stop-color="#0b3a78"/></radialGradient>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity=".05"/></linearGradient>
    <radialGradient id="f" cx=".5" cy=".95" r=".45"><stop offset="0" stop-color="#d8f0ff" stop-opacity=".8"/><stop offset="1" stop-color="#d8f0ff" stop-opacity="0"/></radialGradient>
  </defs>
  <ellipse cx="256" cy="482" rx="150" ry="18" fill="#0b2a4a" opacity=".25"/>
  <circle cx="256" cy="256" r="216" fill="url(#o)"/>
  <circle cx="256" cy="256" r="216" fill="url(#f)"/>
  <path d="M62 300c80-70 190-80 388-30" fill="none" stroke="#d8f0ff" stroke-opacity=".55" stroke-width="10" stroke-linecap="round"/>
  <path d="M74 340c96-60 200-60 360-10" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="6" stroke-linecap="round"/>
  <path transform="translate(0 8)" opacity=".3" d="M176 170h168l-96 210" fill="none" stroke="#0b2a4a" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M176 170h168l-96 210" fill="none" stroke="#fff" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M120 150c34-60 82-94 136-94s102 34 136 94c-40-18-86-28-136-28s-96 10-136 28z" fill="url(#g)"/>
  <circle cx="256" cy="256" r="214" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="4"/>
</svg>
"""


def main():
    names = [n.strip() for n in (ROOT / "tools" / "icon-names.txt").read_text().split() if n.strip()]
    OUT.mkdir(parents=True, exist_ok=True)
    titles = {}
    tf = ROOT / "tools" / "icon-titles.txt"
    if tf.exists():
        for line in tf.read_text().splitlines():
            if "\t" in line:
                k, v = line.split("\t", 1)
                titles[k] = v
    agent_i = 0
    missing = []
    for n in names:
        if n in ICONS:
            g, c = ICONS[n]
        elif n.startswith("omarchy-agent-"):
            g, c = "sparkle", AGENT_COLOURS[agent_i % len(AGENT_COLOURS)]
            agent_i += 1
        else:
            missing.append(n)
            g, c = "terminal", "graphite"
        title = titles.get(n, n).replace("&", "&amp;").replace("<", "&lt;")
        (OUT / f"{n}.svg").write_text(icon_svg(n, title, g, c))
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "logo.svg").write_text(logo_svg())
    print(f"{len(names)} icons, logo; no mapping (drawn as a terminal): {missing or 'none'}")


if __name__ == "__main__":
    main()
