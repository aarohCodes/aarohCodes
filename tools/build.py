#!/usr/bin/env python3
"""Generates the animated SVG artwork used by README.md.

    python tools/build.py

Everything is plain SVG + SMIL: no scripts, no web fonts, no external images.
That is what lets it animate inside GitHub's image sandbox, and it means the
profile never depends on a third-party stats service being up.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

BG, PANEL, LINE = "#070b14", "#0b1220", "#1c2a47"
CYAN, PINK, AMBER, GREEN, RED = "#22d3ee", "#ff3d9a", "#ffb224", "#3dffa2", "#ff4d5e"
TEXT, DIM, GOLD = "#e6eefb", "#7388a8", "#ffcf4a"
MONO = "ui-monospace,'SF Mono','Cascadia Code','JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace"


# ── helpers ──────────────────────────────────────────────────────────────────
def n(x: float) -> str:
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


def svg(w: int, h: int, body: str, defs: str = "", rx: int = 16, title: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" font-family="{MONO}">'
        f"<title>{title}</title>"
        f'<defs><clipPath id="frame"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>{defs}</defs>'
        f'<g clip-path="url(#frame)">{body}</g>'
        f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{rx}" fill="none" '
        f'stroke="{LINE}" stroke-width="1.5"/></svg>\n'
    )


def brackets(w: int, h: int, c: str = CYAN, inset: int = 12, k: int = 18, op: float = 0.7) -> str:
    i = inset
    d = (
        f"M{i},{i + k} V{i} H{i + k} M{w - i - k},{i} H{w - i} V{i + k} "
        f"M{w - i},{h - i - k} V{h - i} H{w - i - k} M{i + k},{h - i} H{i} V{h - i - k}"
    )
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.5" opacity="{op}"/>'


def loop(content: str, dist: float, dur: float) -> str:
    """Scroll `content` left by `dist` px every `dur` seconds, forever."""
    return (
        f"<g>{content}<animateTransform attributeName=\"transform\" type=\"translate\" "
        f'from="0 0" to="{-dist} 0" dur="{dur}s" repeatCount="indefinite"/></g>'
    )


def keyed(values: list, times: list[float]) -> tuple[str, str]:
    """Drop repeated keyTimes so the SMIL lists stay strictly valid."""
    vs, ts = [], []
    for v, t in zip(values, times):
        if ts and abs(t - ts[-1]) < 1e-6:
            vs[-1] = v
            continue
        vs.append(v)
        ts.append(t)
    return ";".join(str(v) for v in vs), ";".join(f"{t:.3f}".rstrip("0").rstrip(".") or "0" for t in ts)


# ── the car ──────────────────────────────────────────────────────────────────
CAR_BODY = (
    "M16,74 L12,56 L20,44 L62,40 C92,36 112,18 150,15 L186,15 C216,17 240,34 264,41 "
    "L300,48 C312,51 318,60 316,72 L314,76 L280,76 A28,28 0 0 0 224,76 L100,76 A28,28 0 0 0 44,76 Z"
)
CAR_CANOPY = "M110,38 C124,24 140,20 152,20 L184,20 C208,22 226,32 242,40 Z"


def car_defs() -> str:
    return (
        '<linearGradient id="carBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3f6e"/>'
        '<stop offset="1" stop-color="#0a1020"/></linearGradient>'
        f'<linearGradient id="carGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".6"/>'
        '<stop offset="1" stop-color="#0b1220" stop-opacity=".75"/></linearGradient>'
        '<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".55"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="tail" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{PINK}" stop-opacity=".95"/>'
        f'<stop offset="1" stop-color="{PINK}" stop-opacity="0"/></linearGradient>'
        '<filter id="glow" x="-50%" y="-300%" width="200%" height="700%"><feGaussianBlur stdDeviation="4"/></filter>'
    )


def wheel(cx: int, cy: int = 72, dur: float = 0.45) -> str:
    spokes = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{n(cx + 13 * math.cos(a))}" y2="{n(cy + 13 * math.sin(a))}"/>'
        for a in (i * 2 * math.pi / 5 for i in range(5))
    )
    return (
        f'<circle cx="{cx}" cy="{cy}" r="22" fill="#04060c" stroke="#2a3a5c" stroke-width="2"/>'
        f'<g stroke="{CYAN}" stroke-width="2" stroke-linecap="round">'
        f'<circle cx="{cx}" cy="{cy}" r="14" fill="#0b1220" stroke-dasharray="14 3.6"/>{spokes}'
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" '
        f'dur="{dur}s" repeatCount="indefinite"/></g>'
        f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{PINK}"/>'
    )


def car() -> str:
    pulses = "".join(
        f'<circle cx="169" cy="10" r="6" fill="none" stroke="{CYAN}" stroke-width="1.4" opacity="0">'
        f'<animate attributeName="r" from="6" to="430" dur="3.6s" begin="{b}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".6;0" dur="3.6s" begin="{b}s" repeatCount="indefinite"/></circle>'
        for b in (0, 1.2, 2.4)
    )
    return (
        "<g>"
        f"{pulses}"
        f'<ellipse cx="165" cy="96" rx="150" ry="5" fill="{CYAN}" opacity=".3" filter="url(#glow)"/>'
        '<polygon points="314,54 610,20 610,112 314,64" fill="url(#beam)" opacity=".5">'
        '<animate attributeName="opacity" values=".5;.36;.5;.44;.5" dur="1.7s" repeatCount="indefinite"/></polygon>'
        '<rect x="-190" y="50" width="202" height="3" fill="url(#tail)"/>'
        '<rect x="-120" y="57" width="132" height="2" fill="url(#tail)" opacity=".6"/>'
        f'<path d="M6,24 L44,24 L46,30 L8,30 Z" fill="#16233f" stroke="{CYAN}" stroke-width="1.2"/>'
        f'<path d="M26,30 L32,42" stroke="{CYAN}" stroke-width="2"/>'
        f'<path d="{CAR_BODY}" fill="url(#carBody)" stroke="{CYAN}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<path d="{CAR_CANOPY}" fill="url(#carGlass)" stroke="{CYAN}" stroke-width="1"/>'
        f'<path d="M170,20 L174,39" stroke="{CYAN}" stroke-width="1" opacity=".7"/>'
        f'<path d="M22,62 H44 M100,62 H224 M280,62 H309" stroke="{PINK}" stroke-width="2" stroke-linecap="round"/>'
        f'<path d="M116,46 L150,46 L143,56 L112,56 Z" fill="{BG}" stroke="{PINK}" stroke-width="1"/>'
        f'<text x="184" y="55" font-size="9" font-weight="700" fill="{CYAN}" letter-spacing="1">AN-01</text>'
        '<path d="M298,50 L313,54 L315,62 L296,58 Z" fill="#eaffff"/>'
        f'<rect x="11" y="47" width="5" height="12" rx="1" fill="{PINK}"/>'
        f'<rect x="158" y="7" width="22" height="8" rx="2" fill="#0d1730" stroke="{CYAN}" stroke-width="1"/>'
        f'<rect x="160" y="10" width="5" height="2" fill="{GREEN}">'
        '<animate attributeName="x" values="160;173;160" dur=".5s" repeatCount="indefinite"/></rect>'
        + wheel(72)
        + wheel(252)
        + '<animateTransform attributeName="transform" type="translate" values="0 0;0 -1.2;0 0;0 .6;0 0" '
        'dur=".9s" repeatCount="indefinite"/></g>'
    )


def mini_car(accent: str) -> str:
    """Silhouette version for headers and the footer (drawn at ~0.22 scale)."""
    return (
        '<rect x="-230" y="50" width="244" height="7" fill="url(#mt)"/>'
        f'<path d="{CAR_BODY}" fill="#16233f" stroke="{accent}" stroke-width="5" stroke-linejoin="round"/>'
        f'<path d="{CAR_CANOPY}" fill="{accent}" opacity=".55"/>'
        f'<circle cx="72" cy="72" r="21" fill="#04060c" stroke="{accent}" stroke-width="5"/>'
        f'<circle cx="252" cy="72" r="21" fill="#04060c" stroke="{accent}" stroke-width="5"/>'
    )


def mini_trail(accent: str) -> str:
    return (
        f'<linearGradient id="mt" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{accent}" stop-opacity=".9"/>'
        f'<stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>'
    )


# ── hero ─────────────────────────────────────────────────────────────────────
def glyph(ch: str, w: float, h: float) -> str:
    m = h / 2
    if ch == "A":
        return f"M0,{n(h)} L{n(w / 2)},0 L{n(w)},{n(h)} M{n(w * 0.17)},{n(h * 0.66)} H{n(w * 0.83)}"
    if ch == "R":
        r = h * 0.18
        return (
            f"M0,{n(h)} V0 H{n(w - r)} Q{n(w)},0 {n(w)},{n(r)} V{n(m - r)} Q{n(w)},{n(m)} {n(w - r)},{n(m)} H0 "
            f"M{n(w * 0.45)},{n(m)} L{n(w)},{n(h)}"
        )
    if ch == "O":
        r = h * 0.22
        return (
            f"M{n(r)},0 H{n(w - r)} Q{n(w)},0 {n(w)},{n(r)} V{n(h - r)} Q{n(w)},{n(h)} {n(w - r)},{n(h)} "
            f"H{n(r)} Q0,{n(h)} 0,{n(h - r)} V{n(r)} Q0,0 {n(r)},0 Z"
        )
    if ch == "H":
        return f"M0,0 V{n(h)} M{n(w)},0 V{n(h)} M0,{n(m)} H{n(w)}"
    if ch == "N":
        return f"M0,{n(h)} V0 L{n(w)},{n(h)} V0"
    if ch == "T":
        return f"M0,0 H{n(w)} M{n(w / 2)},0 V{n(h)}"
    if ch == "I":
        return f"M0,0 V{n(h)}"
    raise ValueError(ch)


def name_block(text: str, x0: float, y0: float, gw: float, gh: float, gap: float, space: float) -> tuple[str, str]:
    letters, x = [], x0
    for ch in text:
        if ch == " ":
            x += space
            continue
        w = 0 if ch == "I" else gw
        letters.append((x, glyph(ch, w, gh)))
        x += w + gap
    x_end = x - gap
    total = 2.4
    drawn, sparks = [], []
    for i, (gx, d) in enumerate(letters):
        s = i * 0.06
        vals, times = keyed([1, 1, 0, 0], [0, s, s + 0.4, 1])
        drawn.append(
            f'<path transform="translate({n(gx)},{n(y0)})" d="{d}" pathLength="1" stroke-dasharray="1">'
            f'<animate attributeName="stroke-dashoffset" values="{vals}" keyTimes="{times}" dur="{total}s" fill="freeze"/></path>'
        )
        sparks.append(
            f'<path transform="translate({n(gx)},{n(y0)})" d="{d}" pathLength="1" stroke-dasharray=".1 .9">'
            f'<animate attributeName="stroke-dashoffset" values="1;0" dur="{n(2.6 + (i * 0.37) % 1.3)}s" repeatCount="indefinite"/></path>'
        )
    common = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
    markup = (
        f'<g {common} stroke="url(#nm)" stroke-width="9" opacity=".75" filter="url(#glowBig)">{"".join(drawn)}</g>'
        f'<g {common} stroke="url(#nm)" stroke-width="7">{"".join(drawn)}</g>'
        f'<g {common} stroke="#fff" stroke-width="2.2" opacity=".9">{"".join(sparks)}</g>'
    )
    grad = (
        f'<linearGradient id="nm" gradientUnits="userSpaceOnUse" x1="{n(x0)}" y1="0" x2="{n(x_end)}" y2="0">'
        f'<stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="#8b7bff"/><stop offset="1" stop-color="{PINK}"/></linearGradient>'
    )
    return markup, grad


def typed_lines(lines: list[str], x: int, y: int, width: int, hold: float = 3.6) -> str:
    total = hold * len(lines)
    out = [f'<text x="{x - 26}" y="{y}" font-size="21" font-weight="700" fill="{PINK}">&gt;</text>']
    for i, line in enumerate(lines):
        s, e = i / len(lines), (i + 1) / len(lines)
        p0, p1 = f"M{x},{y} h0", f"M{x},{y} h{width}"
        vals, times = keyed([p0, p0, p1, p1, p0, p0], [0, s, s + 0.08, e - 0.03, e, 1])
        out.append(
            f'<path id="tl{i}" d="{p0}" fill="none"><animate attributeName="d" values="{vals}" keyTimes="{times}" '
            f'dur="{n(total)}s" repeatCount="indefinite"/></path>'
            f'<text font-size="21" font-weight="600" fill="{TEXT}"><textPath xlink:href="#tl{i}">{line}</textPath></text>'
        )
    return "".join(out)


def hero() -> str:
    W, H, HZ, ROAD = 1000, 400, 286, 322
    r = random.Random(7)
    b: list[str] = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']

    for _ in range(70):
        x, y, s, o = r.uniform(0, W), r.uniform(4, HZ - 30), r.choice([0.6, 0.8, 1, 1.2, 1.6]), r.uniform(0.25, 0.9)
        if r.random() < 0.35:
            b.append(
                f'<circle cx="{n(x)}" cy="{n(y)}" r="{s}" fill="#fff" opacity="{o:.2f}"><animate attributeName="opacity" '
                f'values="{o:.2f};.08;{o:.2f}" dur="{n(r.uniform(2, 5))}s" begin="-{n(r.uniform(0, 4))}s" repeatCount="indefinite"/></circle>'
            )
        else:
            b.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="{s}" fill="#fff" opacity="{o:.2f}"/>')

    # sun
    b.append('<circle cx="790" cy="262" r="170" fill="url(#halo)"/>')
    b.append('<circle cx="790" cy="262" r="92" fill="url(#sun)" clip-path="url(#sunc)"/>')

    # skyline (far parallax)
    sky, x = [], 0
    while x < W:
        bw, bh = r.randint(18, 46), r.randint(12, 66)
        bw = min(bw, W - x)
        sky.append(f'<rect x="{x}" y="{HZ - bh}" width="{bw}" height="{bh}" fill="#0a1230"/>')
        sky.append(f'<rect x="{x}" y="{HZ - bh}" width="{bw}" height="1" fill="#3a4f8a" opacity=".8"/>')
        for wy in range(HZ - bh + 5, HZ - 4, 7):
            for wx in range(x + 4, x + bw - 4, 6):
                if r.random() < 0.22:
                    c = r.choice([AMBER, CYAN, "#ffffff", PINK])
                    sky.append(f'<rect x="{wx}" y="{wy}" width="2" height="3" fill="{c}" opacity="{r.uniform(.3, .85):.2f}"/>')
        if bw > 24 and r.random() < 0.3:
            ax = x + bw // 2
            sky.append(f'<path d="M{ax},{HZ - bh} v-{r.randint(8, 16)}" stroke="#3a4f8a" stroke-width="1"/>')
            sky.append(f'<circle cx="{ax}" cy="{HZ - bh - 16}" r="1.3" fill="{RED}"><animate attributeName="opacity" values="1;.1;1" dur="1.8s" repeatCount="indefinite"/></circle>')
        x += bw + r.choice([0, 0, 2, 6])
    skyline = "".join(sky)
    b.append(loop(skyline + f'<g transform="translate({W},0)">{skyline}</g>', W, 90))

    # ground + horizon
    b.append(f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#gnd)"/>')
    b.append(f'<rect y="{HZ - 3}" width="{W}" height="6" fill="{PINK}" opacity=".5" filter="url(#glow)"/>')
    b.append(f'<rect y="{HZ - 1}" width="{W}" height="1.5" fill="{PINK}"/>')

    # shoulder: rail + posts (mid parallax)
    b.append(f'<rect y="309" width="{W}" height="2" fill="#22335c"/>')
    posts = "".join(
        f'<path d="M{px},298 V{ROAD}" stroke="#2b3f73" stroke-width="2"/><circle cx="{px}" cy="297" r="2.2" fill="{AMBER}"/>'
        for px in range(0, W + 251, 125)
    )
    b.append(loop(posts, 125, 0.9))

    # perception targets riding the same parallax layer
    def target(tx: int, kind: str, label: str) -> str:
        if kind == "cone":
            art = (
                f'<path d="M{tx - 8},{ROAD} L{tx},{ROAD - 20} L{tx + 8},{ROAD} Z" fill="#ff7a1a"/>'
                f'<path d="M{tx - 4.4},{ROAD - 9} H{tx + 4.4}" stroke="#fff" stroke-width="2.4"/>'
            )
            bx, by, bw_, bh_ = tx - 14, ROAD - 27, 28, 30
        elif kind == "sign":
            art = (
                f'<path d="M{tx},{ROAD} V{ROAD - 30}" stroke="#93a4c4" stroke-width="2"/>'
                f'<rect x="{tx - 9}" y="{ROAD - 48}" width="18" height="18" fill="{AMBER}" transform="rotate(45 {tx} {ROAD - 39})"/>'
            )
            bx, by, bw_, bh_ = tx - 18, ROAD - 58, 36, 61
        else:
            stripes = "".join(f'<rect x="{tx - 20 + k * 10}" y="{ROAD - 15}" width="5" height="10" fill="{RED}"/>' for k in range(4))
            art = (
                f'<rect x="{tx - 20}" y="{ROAD - 15}" width="40" height="10" fill="#e6eefb"/>{stripes}'
                f'<path d="M{tx - 15},{ROAD - 5} V{ROAD} M{tx + 15},{ROAD - 5} V{ROAD}" stroke="#93a4c4" stroke-width="2"/>'
            )
            bx, by, bw_, bh_ = tx - 26, ROAD - 22, 52, 25
        return (
            art
            + f'<g><rect x="{bx}" y="{by}" width="{bw_}" height="{bh_}" fill="{GREEN}" fill-opacity=".07" stroke="{GREEN}" '
            f'stroke-width="1.2" stroke-dasharray="5 3"/><text x="{bx}" y="{by - 4}" font-size="9" fill="{GREEN}">{label}</text>'
            '<animate attributeName="opacity" values="1;.5;1" dur="1.1s" repeatCount="indefinite"/></g>'
        )

    PW = 1500
    targets = target(330, "cone", "cone 0.98") + target(830, "sign", "sign 0.95") + target(1300, "barrier", "barrier 0.91")
    b.append(loop(targets + f'<g transform="translate({PW},0)">{targets}</g>', PW, round(PW / (125 / 0.9), 2)))

    # road (near parallax)
    b.append(f'<rect y="{ROAD}" width="{W}" height="{H - ROAD}" fill="#070a14"/>')
    b.append(f'<rect y="{ROAD}" width="{W}" height="2" fill="{CYAN}" opacity=".85"/>')
    dashes = "".join(f'<rect x="{dx}" y="384" width="46" height="3" fill="#e6eefb" opacity=".55"/>' for dx in range(0, W + 231, 115))
    b.append(loop(dashes, 115, 0.42))
    for _ in range(9):
        sy = r.choice(list(range(328, 398, 5)) + [120, 205, 250])
        sw, dur = r.randint(50, 150), r.uniform(2.2, 4.2)
        b.append(
            f'<rect x="{W + 20}" y="{sy}" width="{sw}" height="1.5" fill="#fff" opacity="{r.uniform(.12, .3):.2f}">'
            f'<animate attributeName="x" values="{W + 20};{-sw - 20};{-sw - 20}" keyTimes="0;.28;1" dur="{n(dur)}s" '
            f'begin="-{n(r.uniform(0, 4))}s" repeatCount="indefinite"/></rect>'
        )

    b.append(f'<g transform="translate(250,262) scale(1.12)">{car()}</g>')

    # name + typed tagline
    name, name_grad = name_block("AAROH NANOTI", 58, 60, 42, 58, 13, 32)
    b.append(f'<text x="58" y="42" font-size="12" letter-spacing="5" fill="{DIM}">HELLO WORLD, I\'M</text>')
    b.append(name)
    b.append(typed_lines(["CS @ UT Dallas", "5x hackathon winner", "autonomous vehicles + ADAS", "medical-imaging ML", "LLM agents that ship"], 84, 164, 440))
    b.append(f'<text x="58" y="192" font-size="12.5" letter-spacing="1.5" fill="{DIM}">systems that perceive, decide, and move</text>')

    # HUD
    b.append(
        f'<g font-size="11" letter-spacing="2" text-anchor="end">'
        f'<text x="936" y="42" fill="{GREEN}">AUTONOMY ENGAGED</text>'
        f'<circle cx="948" cy="38" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;.2;1" dur="1.2s" repeatCount="indefinite"/></circle>'
        f'<text x="954" y="60" fill="{DIM}">LIDAR 360° / 40 HZ</text>'
        f'<text x="954" y="78" fill="{DIM}">PLANNER OK / 12 MS</text></g>'
    )
    b.append(brackets(W, H))

    defs = (
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03050c"/>'
        '<stop offset=".42" stop-color="#090e28"/><stop offset=".715" stop-color="#3b1459"/></linearGradient>'
        '<linearGradient id="gnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#170e36"/>'
        '<stop offset="1" stop-color="#05070f"/></linearGradient>'
        '<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd166"/>'
        '<stop offset=".5" stop-color="#ff5e7e"/><stop offset="1" stop-color="#b517ff"/></linearGradient>'
        '<radialGradient id="halo"><stop offset="0" stop-color="#ff5e7e" stop-opacity=".4"/>'
        '<stop offset="1" stop-color="#ff5e7e" stop-opacity="0"/></radialGradient>'
        '<clipPath id="sunc"><rect x="680" y="150" width="220" height="87"/><rect x="680" y="240" width="220" height="8"/>'
        '<rect x="680" y="252" width="220" height="7"/><rect x="680" y="264" width="220" height="6"/>'
        '<rect x="680" y="276" width="220" height="4"/></clipPath>'
        '<filter id="glowBig" x="-5%" y="-60%" width="110%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>'
        + car_defs()
        + name_grad
    )
    return svg(W, H, "".join(b), defs, rx=18, title="Aaroh Nanoti: an autonomous race car drives through a neon city at night")


# ── section headers ──────────────────────────────────────────────────────────
def header(idx: str, label: str, accent: str, mode: str = "car", seed: int = 0) -> str:
    W, H = 1000, 72
    r = random.Random(seed)
    b = [
        f'<rect width="{W}" height="{H}" fill="{PANEL}"/>',
        f'<rect x="14" y="14" width="56" height="44" rx="9" fill="{accent}"/>',
        f'<text x="42" y="44" text-anchor="middle" font-size="22" font-weight="800" fill="{BG}">{idx}</text>',
        f'<text x="90" y="45" font-size="25" font-weight="700" letter-spacing="5" fill="{TEXT}">{label}</text>',
    ]
    defs = ""
    if mode == "car":
        dur = 4.6 + (seed % 4) * 0.5
        defs = mini_trail(accent) + '<clipPath id="lane"><rect x="561" y="0" width="440" height="72"/></clipPath>'
        b.append(f'<path d="M560,52 H968" stroke="{LINE}" stroke-width="2" stroke-dasharray="10 8"/>')
        b.append(f'<path d="M560,22 V58" stroke="{accent}" stroke-width="2"/>')
        b.append("".join(
            f'<rect x="{968 + (k % 2) * 7}" y="{22 + k * 6}" width="7" height="6" fill="{TEXT}" opacity=".8"/>'
            f'<rect x="{975 - (k % 2) * 7}" y="{22 + k * 6}" width="7" height="6" fill="{TEXT}" opacity=".12"/>'
            for k in range(6)
        ))
        b.append(
            f'<g clip-path="url(#lane)"><g><g transform="scale(.24)">{mini_car(accent)}</g>'
            f'<animateTransform attributeName="transform" type="translate" values="470 29;1080 29;1080 29" '
            f'keyTimes="0;.42;1" dur="{n(dur)}s" repeatCount="indefinite"/></g></g>'
        )
    elif mode == "lights":
        b.append(f'<rect x="712" y="14" width="258" height="44" rx="10" fill="#04060c" stroke="{LINE}" stroke-width="1.5"/>')
        for i in range(5):
            on, off = (0.6 + i * 0.7) / 6, 4.6 / 6
            b.append(
                f'<circle cx="{745 + i * 48}" cy="36" r="13" fill="#2a0d14" stroke="#3a1420" stroke-width="1.5">'
                f'<animate attributeName="fill" values="#2a0d14;#ff2b3d;#2a0d14" keyTimes="0;{on:.3f};{off:.3f}" '
                'calcMode="discrete" dur="6s" repeatCount="indefinite"/></circle>'
            )
        b.append(
            f'<text x="700" y="42" text-anchor="end" font-size="12" letter-spacing="3" fill="{accent}" opacity="0">LIGHTS OUT'
            '<animate attributeName="opacity" values="0;1;0" keyTimes="0;0.767;0.98" calcMode="discrete" dur="6s" repeatCount="indefinite"/></text>'
        )
    elif mode == "trophy":
        for i in range(5):
            on, off = (0.5 + i * 0.6) / 6, 5.2 / 6
            b.append(
                f'<g opacity=".2">{trophy(750 + i * 44, 20, 1.35, GOLD)}'
                f'<animate attributeName="opacity" values=".2;1;.2" keyTimes="0;{on:.3f};{off:.3f}" calcMode="discrete" dur="6s" repeatCount="indefinite"/></g>'
            )
    elif mode == "shift":
        for i in range(15):
            c = GREEN if i < 5 else (AMBER if i < 10 else RED)
            on, off = (0.3 + i * 0.13) / 3.6, 2.9 / 3.6
            b.append(
                f'<rect x="{610 + i * 24}" y="26" width="17" height="20" rx="4" fill="#141d33">'
                f'<animate attributeName="fill" values="#141d33;{c};#141d33" keyTimes="0;{on:.3f};{off:.3f}" '
                'calcMode="discrete" dur="3.6s" repeatCount="indefinite"/></rect>'
            )
    elif mode == "radio":
        for i in range(30):
            hgt = r.randint(10, 40)
            lo, mid = r.uniform(0.15, 0.4), r.uniform(0.4, 0.8)
            b.append(
                f'<g transform="translate({600 + i * 12.4:.1f},36)"><rect x="-2.5" y="{-hgt / 2}" width="5" height="{hgt}" rx="2.5" fill="{accent}">'
                f'<animateTransform attributeName="transform" type="scale" values="1 {lo:.2f};1 1;1 {mid:.2f};1 .9;1 {lo:.2f}" '
                f'dur="{n(r.uniform(.7, 1.5))}s" begin="-{n(r.uniform(0, 1.5))}s" repeatCount="indefinite"/></rect></g>'
            )
    return svg(W, H, "".join(b), defs, rx=14, title=f"{idx} / {label}")


# ── project cards ────────────────────────────────────────────────────────────
TROPHY = (
    '<path d="M6,2 H18 V9 A6,6 0 0 1 6,9 Z M10.5,14.5 H13.5 V19 H10.5 Z M7,19 H17 V22 H7 Z" stroke-width="0"/>'
    '<path d="M6,4 H2.5 V7 A3.5,3.5 0 0 0 6,10.5 M18,4 H21.5 V7 A3.5,3.5 0 0 1 18,10.5" fill="none" stroke-width="1.7"/>'
)


def trophy(x: float, y: float, scale: float, color: str = "url(#gold)") -> str:
    return f'<g transform="translate({n(x)},{n(y)}) scale({scale})" fill="{color}" stroke="{color}">{TROPHY}</g>'


GOLD_GRAD = (
    '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1a8"/>'
    f'<stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="#e08a00"/></linearGradient>'
)


def card(pos: str, name: str, tag: str, accent: str, art: str, defs: str = "", badge: str | None = None) -> str:
    W, H = 600, 250
    plain = pos.replace("&#215;", "x")
    bw = max(46, 20 + round(len(plain) * 9.6))
    grid = '<pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M25,0 H0 V25" fill="none" stroke="#111c33"/></pattern>'
    b = (
        f'<rect width="{W}" height="{H}" fill="{PANEL}"/><rect width="{W}" height="{H}" fill="url(#grid)"/>'
        f"{art}"
        f'<rect x="18" y="18" width="{bw}" height="28" rx="7" fill="{badge or accent}"/>'
        f'<text x="{n(18 + bw / 2)}" y="38" text-anchor="middle" font-size="15" font-weight="800" fill="{BG}">{pos}</text>'
        f'<text x="{18 + bw + 12}" y="37" font-size="12" letter-spacing="3" fill="{DIM}">{tag}</text>'
        f'<text x="20" y="216" font-size="32" font-weight="800" fill="{TEXT}">{name}</text>'
        f'<rect x="20" y="227" width="56" height="3" fill="{accent}"/>'
        + brackets(W, H, accent, 10, 14, 0.55)
    )
    return svg(W, H, b, grid + defs, title=f"{pos} {name}")


def art_ovascope() -> tuple[str, str]:
    r = random.Random(11)
    ax, ay, R, half = 440, 18, 204, math.radians(33)
    lx, ly, rx_ = ax - R * math.sin(half), ay + R * math.cos(half), ax + R * math.sin(half)
    out = [f'<path d="M{ax},{ay} L{n(lx)},{n(ly)} A{R},{R} 0 0 0 {n(rx_)},{n(ly)} Z" fill="url(#us)" stroke="#2b3f73"/>']
    for _ in range(190):
        a, d = r.uniform(-half * 0.95, half * 0.95), r.uniform(26, R - 6)
        out.append(
            f'<circle cx="{n(ax + d * math.sin(a))}" cy="{n(ay + d * math.cos(a))}" r="{r.choice([.7, 1, 1.3, 1.8])}" '
            f'fill="#bcd0ee" opacity="{r.uniform(.06, .34):.2f}"/>'
        )
    for rr in (72, 138):
        x1, y1, x2 = ax - rr * math.sin(half), ay + rr * math.cos(half), ax + rr * math.sin(half)
        out.append(f'<path d="M{n(x1)},{n(y1)} A{rr},{rr} 0 0 0 {n(x2)},{n(y1)}" fill="none" stroke="#2b3f73" stroke-dasharray="3 5"/>')
    blob = "M418,128 C424,108 452,102 472,112 C494,122 498,146 484,160 C468,176 436,174 422,160 C412,150 414,138 418,128 Z"
    T = 7
    out.append(f'<path d="{blob}" fill="#03050a" opacity=".85"/>')
    out.append(
        f'<g opacity="0"><rect x="404" y="98" width="102" height="84" fill="none" stroke="{AMBER}" stroke-width="1.5" stroke-dasharray="6 4"/>'
        f'<text x="404" y="92" font-size="10" fill="{AMBER}" letter-spacing="1">box prompt</text>'
        f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.08;.86;.94;1" dur="{T}s" repeatCount="indefinite"/></g>'
    )
    out.append(
        f'<path d="{blob}" fill="{CYAN}" fill-opacity="0" stroke="{CYAN}" stroke-width="2.2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
        f'<animate attributeName="stroke-dashoffset" values="1;1;0;0;1" keyTimes="0;.14;.45;.94;1" dur="{T}s" repeatCount="indefinite"/>'
        f'<animate attributeName="fill-opacity" values="0;0;.24;.24;0" keyTimes="0;.42;.55;.9;1" dur="{T}s" repeatCount="indefinite"/></path>'
    )
    out.append(
        f'<line x1="{ax}" y1="{ay}" x2="{ax}" y2="{ay + R}" stroke="{GREEN}" stroke-width="1.5" opacity=".55">'
        f'<animateTransform attributeName="transform" type="rotate" values="-33 {ax} {ay};33 {ax} {ay};-33 {ax} {ay}" dur="4s" repeatCount="indefinite"/></line>'
    )
    out.append(f'<rect x="{ax - 15}" y="{ay - 7}" width="30" height="9" rx="3" fill="#2a3f6e"/>')
    out.append(f'<text x="582" y="236" text-anchor="end" font-size="10" letter-spacing="1" fill="{DIM}">DINOv2 &#8594; SAM 2.1</text>')
    defs = (
        f'<radialGradient id="us" gradientUnits="userSpaceOnUse" cx="{ax}" cy="{ay}" r="{R}"><stop offset="0" stop-color="#22355c"/>'
        '<stop offset="1" stop-color="#0a1322"/></radialGradient>'
    )
    return "".join(out), defs


def art_pondr() -> tuple[str, str]:
    nodes = [(440, 124, 15), (352, 66, 10), (455, 46, 8), (535, 72, 11), (566, 152, 9), (505, 206, 11), (392, 196, 9), (318, 142, 8)]
    edges = [(0, i) for i in range(1, 8)] + [(i, i % 7 + 1) for i in range(1, 8)]
    out = [
        f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[c][0]}" y2="{nodes[c][1]}" stroke="#24365c" stroke-width="1.5"/>'
        for a, c in edges
    ]
    for k, i in enumerate((1, 3, 5, 7)):
        out.append(
            f'<circle r="2.4" fill="{CYAN}"><animateMotion dur="2.6s" begin="-{n(k * 0.65)}s" repeatCount="indefinite" '
            f'path="M{nodes[0][0]},{nodes[0][1]} L{nodes[i][0]},{nodes[i][1]}"/></circle>'
        )
    for i, (x, y, rad) in enumerate(nodes):
        dur, off = 7 + (i * 1.7) % 5, (i * 2.3) % 7
        anim = f'dur="{n(dur)}s" begin="-{n(off)}s" repeatCount="indefinite"'
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{rad}" fill="none" stroke="{GREEN}" stroke-width="2" opacity="0">'
            f'<animate attributeName="r" values="{rad};{rad};{n(rad * 2.6)}" keyTimes="0;.88;1" {anim}/>'
            f'<animate attributeName="opacity" values="0;0;.9;0" keyTimes="0;.879;.88;1" {anim}/></circle>'
            f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{GREEN}" stroke="{PANEL}" stroke-width="3">'
            f'<animate attributeName="fill" values="{GREEN};{AMBER};{RED};{RED};{GREEN};{GREEN}" keyTimes="0;.45;.8;.88;.92;1" {anim}/></circle>'
        )
    out.append(f'<text x="582" y="236" text-anchor="end" font-size="10" letter-spacing="1" fill="{DIM}">retention decays, reviews refresh</text>')
    return "".join(out), ""


def art_maternal() -> tuple[str, str]:
    def beat(x: int) -> str:
        return f" L{x + 18},100 q7,-11 14,0 l10,0 l5,7 l8,-56 l9,74 l7,-25 l14,0 q11,-17 22,0 l33,0"

    ecg = "M296,100" + beat(296) + beat(436)
    out = [
        f'<path d="{ecg}" fill="none" stroke="{PINK}" stroke-width="2" opacity=".22" stroke-linejoin="round"/>',
        f'<path d="{ecg}" fill="none" stroke="{PINK}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round" pathLength="1" stroke-dasharray=".3 .7">'
        '<animate attributeName="stroke-dashoffset" values="1;0" dur="2.2s" repeatCount="indefinite"/></path>',
        '<path d="M436,138 V232" stroke="#2b3f73" stroke-width="1.5"/>',
        f'<text x="582" y="236" text-anchor="end" font-size="10" letter-spacing="1" fill="{DIM}">SHAP</text>',
    ]
    for i, w in enumerate((82, 54, -46, 30, -22)):
        y = 142 + i * 18
        bar = (
            f'<rect x="0" y="{y}" width="0" height="11" rx="2" fill="{PINK if w > 0 else CYAN}">'
            f'<animate attributeName="width" values="0;{abs(w)};{abs(w)};0" keyTimes="0;.18;.9;1" dur="5s" begin="{n(i * 0.15)}s" repeatCount="indefinite"/></rect>'
        )
        out.append(f'<g transform="translate(436,0){" scale(-1,1)" if w < 0 else ""}">{bar}</g>')
    return "".join(out), ""


def art_jarvis() -> tuple[str, str]:
    r = random.Random(3)
    cx, cy = 446, 108
    out = [
        "".join(
            f'<path d="M{n(cx + 80 * math.cos(a))},{n(cy + 80 * math.sin(a))} L{n(cx + 86 * math.cos(a))},{n(cy + 86 * math.sin(a))}" stroke="#2b3f73" stroke-width="1.5"/>'
            for a in (math.radians(k * 15) for k in range(24))
        )
    ]
    for rad, col, sw, dash, dur, sign in ((70, CYAN, 2, "110 30 20 30", 14, 1), (54, PINK, 3, "8 10", 9, -1), (38, CYAN, 1.5, "60 20", 6, 1)):
        out.append(
            f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-dasharray="{dash}">'
            f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="{360 * sign} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/></circle>'
        )
    out.append(
        f'<circle cx="{cx}" cy="{cy}" r="22" fill="{CYAN}" opacity=".18"><animate attributeName="r" values="20;27;20" dur="2.4s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{cx}" cy="{cy}" r="13" fill="{CYAN}"><animate attributeName="opacity" values="1;.55;1" dur="2.4s" repeatCount="indefinite"/></circle>'
    )
    for i in range(23):
        hgt = r.randint(10, 30)
        lo = r.uniform(0.15, 0.4)
        out.append(
            f'<g transform="translate({336 + i * 10},218)"><rect x="-2" y="{-hgt / 2}" width="4" height="{hgt}" rx="2" fill="{PINK}">'
            f'<animateTransform attributeName="transform" type="scale" values="1 {lo:.2f};1 1;1 .5;1 .85;1 {lo:.2f}" '
            f'dur="{n(r.uniform(.7, 1.4))}s" begin="-{n(r.uniform(0, 1.4))}s" repeatCount="indefinite"/></rect></g>'
        )
    return "".join(out), ""


def art_f1tenth() -> tuple[str, str]:
    track = (
        "M340,58 L510,48 C556,45 582,68 574,98 C568,122 536,126 506,128 C478,130 468,152 492,166 "
        "C520,182 572,172 572,198 C572,224 540,226 510,224 L360,218 C318,216 302,196 306,172 "
        "C310,146 346,148 350,124 C353,106 316,106 312,86 C309,70 322,59 340,58 Z"
    )
    out = [
        f'<use xlink:href="#trk" fill="none" stroke="#2b3f73" stroke-width="24" stroke-linejoin="round"/>',
        f'<use xlink:href="#trk" fill="none" stroke="#0e1830" stroke-width="20" stroke-linejoin="round"/>',
        '<use xlink:href="#trk" fill="none" stroke="#fff" stroke-width="1" stroke-dasharray="4 7" opacity=".28"/>',
        '<path d="M344,47 V69" stroke="#fff" stroke-width="3" stroke-dasharray="3 3"/>',
        f'<use xlink:href="#trk" fill="none" stroke="{CYAN}" stroke-width="2.6" stroke-linecap="round" pathLength="1000" stroke-dasharray="150 850">'
        '<animate attributeName="stroke-dashoffset" values="150;-850" dur="7s" repeatCount="indefinite"/></use>',
        f'<g><path d="M0,0 L54,-26 A60,60 0 0 1 54,26 Z" fill="{CYAN}" opacity=".2">'
        '<animate attributeName="opacity" values=".2;.1;.2" dur=".6s" repeatCount="indefinite"/></path>'
        f'<rect x="-11" y="-6.5" width="22" height="13" rx="3.5" fill="{PINK}"/><rect x="2" y="-4.5" width="5" height="9" rx="1" fill="{BG}"/>'
        '<animateMotion dur="7s" repeatCount="indefinite" rotate="auto"><mpath xlink:href="#trk"/></animateMotion></g>',
        f'<text x="582" y="244" text-anchor="end" font-size="10" letter-spacing="1" fill="{DIM}">/drive  AckermannDriveStamped</text>',
    ]
    return "".join(out), f'<path id="trk" d="{track}"/>'


def art_quada() -> tuple[str, str]:
    r = random.Random(5)
    pts = [(330 + 245 * t, 204 - 158 * math.sqrt(t)) for t in (i / 40 for i in range(41))]
    frontier = "M" + " L".join(f"{n(x)},{n(y)}" for x, y in pts)
    rf = (312, 188)
    tx, ty = max(pts[1:], key=lambda p: (rf[1] - p[1]) / (p[0] - rf[0]))
    slope = (ty - rf[1]) / (tx - rf[0])
    ex = rf[0] + (40 - rf[1]) / slope
    out = [f'<path d="M312,34 V216 H586" fill="none" stroke="#2b3f73" stroke-width="1.5"/>']
    for _ in range(48):
        t = r.uniform(0.04, 1)
        top = 204 - 158 * math.sqrt(t) + 9
        if top < 206:
            out.append(f'<circle cx="{n(330 + 245 * t + r.uniform(0, 8))}" cy="{n(r.uniform(top, 208))}" r="2" fill="#5c74a3" opacity="{r.uniform(.35, .8):.2f}"/>')
    T = 6
    fade = f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.35;.45;.9;1" dur="{T}s" repeatCount="indefinite"/>'
    out.append(
        f'<path d="{frontier}" fill="none" stroke="{AMBER}" stroke-width="2.6" stroke-linecap="round" pathLength="1" stroke-dasharray="1">'
        f'<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;.35;.9;1" dur="{T}s" repeatCount="indefinite"/></path>'
        f'<path d="M{rf[0]},{rf[1]} L{n(ex)},40" stroke="{CYAN}" stroke-width="1.5" stroke-dasharray="6 5" opacity="0">{fade}</path>'
        f'<g opacity="0"><circle cx="{n(tx)}" cy="{n(ty)}" r="6" fill="none" stroke="{GREEN}" stroke-width="2">'
        '<animate attributeName="r" values="6;16;6" dur="1.6s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{n(tx)}" cy="{n(ty)}" r="5" fill="{GREEN}"/>'
        f'<text x="{n(tx + 12)}" y="{n(ty + 20)}" font-size="10" fill="{GREEN}" letter-spacing="1">max Sharpe</text>{fade}</g>'
        f'<text x="320" y="44" font-size="9" letter-spacing="1" fill="{DIM}">RETURN</text>'
        f'<text x="582" y="232" text-anchor="end" font-size="9" letter-spacing="1" fill="{DIM}">RISK</text>'
    )
    return "".join(out), ""


def art_harmoniq() -> tuple[str, str]:
    tx, ty = 336, 112
    out = [
        f'<path d="M{tx},{ty} L{tx - 17},{ty + 86} M{tx},{ty} L{tx + 17},{ty + 86} M{tx - 9},{ty + 46} H{tx + 9} M{tx - 13},{ty + 66} H{tx + 13}" '
        f'fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round"/>',
        f'<circle cx="{tx}" cy="{ty}" r="4.5" fill="{CYAN}"/>',
    ]
    for k, rad in enumerate((15, 26, 37)):
        dx, dy = rad * 0.72, rad * 0.69
        for sgn, sweep in ((1, 1), (-1, 0)):
            out.append(
                f'<path d="M{n(tx + sgn * dx)},{n(ty - dy)} A{rad},{rad} 0 0 {sweep} {n(tx + sgn * dx)},{n(ty + dy)}" fill="none" '
                f'stroke="{CYAN}" stroke-width="2" stroke-linecap="round"><animate attributeName="opacity" values=".12;1;.12" dur="1.8s" '
                f'begin="-{n(1.8 - k * 0.3)}s" repeatCount="indefinite"/></path>'
            )
    out.append(
        f'<circle cx="412" cy="74" r="5" fill="none" stroke="{RED}" stroke-width="1.5">'
        '<animate attributeName="r" values="5;18" dur="1.4s" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="1;0" dur="1.4s" repeatCount="indefinite"/></circle>'
        f'<circle cx="412" cy="74" r="4.5" fill="{RED}"/>'
        f'<text x="424" y="78" font-size="10.5" letter-spacing="1" fill="{RED}">outage risk</text>'
    )
    gx, gy, gr = 492, 178, 62
    arc = f"M{gx - gr},{gy} A{gr},{gr} 0 0 1 {gx + gr},{gy}"
    out.append(f'<path d="{arc}" fill="none" stroke="#141d33" stroke-width="14"/>')
    for k, col in enumerate((RED, AMBER, GREEN)):
        out.append(
            f'<path d="{arc}" fill="none" stroke="{col}" stroke-width="10" pathLength="3" stroke-dasharray=".94 2.06" '
            f'stroke-dashoffset="{-k - 0.03}" opacity=".9"/>'
        )
    rot = ";".join(f"{a} {gx} {gy}" for a in (-62, -20, -48, 55, 30, 62, -62))
    out.append(
        f'<g><path d="M{gx},{gy} V{gy - gr + 12}" stroke="{TEXT}" stroke-width="3" stroke-linecap="round"/>'
        f'<animateTransform attributeName="transform" type="rotate" values="{rot}" keyTimes="0;.15;.3;.55;.7;.88;1" dur="7s" repeatCount="indefinite"/></g>'
        f'<circle cx="{gx}" cy="{gy}" r="6" fill="{TEXT}"/>'
        f'<text x="{gx}" y="{gy + 26}" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="3" fill="{DIM}">CHI</text>'
        f'<text x="582" y="236" text-anchor="end" font-size="10" letter-spacing="1" fill="{DIM}">customer happiness index</text>'
    )
    return "".join(out), ""


def art_rsna() -> tuple[str, str]:
    out = [
        f'<rect x="{318 + ox}" y="{30 + oy}" width="128" height="172" rx="9" fill="#060911" stroke="#2b3f73" stroke-width="1.5" opacity="{op}"/>'
        for ox, oy, op in ((-16, 16, 0.45), (-8, 8, 0.7), (0, 0, 1))
    ]
    out.append(
        '<g fill="#cdd9ee" opacity=".88">'
        '<path d="M364,38 V92 C352,100 347,116 355,127 C365,138 397,138 407,127 C415,116 410,100 398,92 V38 Z"/>'
        '<path d="M352,150 H410 L402,164 L400,196 H364 L360,164 Z"/>'
        '<ellipse cx="424" cy="112" rx="6.5" ry="14" opacity=".8"/></g>'
        '<path d="M356,141 L372,146 L356,148 Z M406,141 L390,146 L406,148 Z" fill="#6f84a8"/>'
        '<circle cx="381" cy="143" r="15" fill="url(#heat)"><animate attributeName="r" values="12;21;12" dur="2.2s" repeatCount="indefinite"/></circle>'
        f'<path d="M362,131 v-6 h6 M400,131 v-6 h-6 M362,155 v6 h6 M400,155 v6 h-6" fill="none" stroke="{CYAN}" stroke-width="1.6"/>'
        f'<rect x="319" y="32" width="126" height="2" fill="{GREEN}" opacity=".6">'
        '<animate attributeName="y" values="32;198;32" dur="4.5s" repeatCount="indefinite"/></rect>'
    )
    for i, v in enumerate((0.91, 0.34, 0.78, 0.22, 0.63, 0.18, 0.47, 0.85, 0.3, 0.12, 0.56, 0.08)):
        y, hot = 36 + i * 14.2, v > 0.6
        out.append(
            f'<rect x="468" y="{n(y)}" width="112" height="7" rx="3.5" fill="#141d33"/>'
            f'<rect x="468" y="{n(y)}" width="0" height="7" rx="3.5" fill="{PINK if hot else CYAN}" opacity="{1 if hot else 0.75}">'
            f'<animate attributeName="width" values="0;{n(112 * v)};{n(112 * v)};0" keyTimes="0;.2;.92;1" dur="6s" begin="{n(i * 0.08)}s" repeatCount="indefinite"/></rect>'
        )
    out.append(f'<text x="582" y="224" text-anchor="end" font-size="10" letter-spacing="1" fill="{DIM}">12 findings per study</text>')
    defs = (
        f'<radialGradient id="heat"><stop offset="0" stop-color="{PINK}" stop-opacity=".95"/>'
        f'<stop offset=".5" stop-color="{AMBER}" stop-opacity=".55"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'
    )
    return "".join(out), defs


def art_arkos() -> tuple[str, str]:
    def load(x: float) -> float:  # daily demand cycle with a slow upward drift
        return 138 - 34 * math.sin((x - 300) / 280 * 2 * math.pi * 2.5) - (x - 300) * 0.06

    def line(pts: list[tuple[float, float]]) -> str:
        return "M" + " L".join(f"{x},{n(y)}" for x, y in pts)

    hist = [(x, load(x)) for x in range(300, 441, 5)]
    fut = [(x, load(x) - (x - 440) * 0.05) for x in range(440, 581, 5)]
    band = (
        "M" + " L".join(f"{x},{n(y - 7 - (x - 440) * 0.11)}" for x, y in fut)
        + " L" + " L".join(f"{x},{n(y + 7 + (x - 440) * 0.11)}" for x, y in reversed(fut)) + " Z"
    )
    T = 6
    stroke = 'fill="none" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1"'
    out = (
        '<path d="M300,74 V200 H584" fill="none" stroke="#2b3f73" stroke-width="1.5"/>'
        f'<path d="M440,58 V200" stroke="{DIM}" stroke-dasharray="3 5"/>'
        f'<text x="446" y="66" font-size="9" letter-spacing="1" fill="{DIM}">NOW</text>'
        f'<path d="{band}" fill="{AMBER}" opacity="0"><animate attributeName="opacity" values="0;0;.22;.22;0" keyTimes="0;.4;.62;.92;1" dur="{T}s" repeatCount="indefinite"/></path>'
        f'<path d="{line(hist)}" stroke="{CYAN}" {stroke}>'
        f'<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;.35;.92;1" dur="{T}s" repeatCount="indefinite"/></path>'
        f'<path d="{line(fut)}" stroke="{AMBER}" {stroke} stroke-dashoffset="1">'
        f'<animate attributeName="stroke-dashoffset" values="1;1;0;0;1" keyTimes="0;.35;.62;.92;1" dur="{T}s" repeatCount="indefinite"/></path>'
        f'<path d="M332,24 l-13,23 h9 l-5,19 l16,-27 h-9 l6,-15 Z" fill="{AMBER}"><animate attributeName="opacity" values="1;.45;1" dur="1.6s" repeatCount="indefinite"/></path>'
        f'<text x="582" y="224" text-anchor="end" font-size="10" letter-spacing="1" fill="{DIM}">LSTM demand forecast</text>'
    )
    return out, ""


def art_codered() -> tuple[str, str]:
    mx, my = 340, 104
    out = [
        f'<circle cx="{mx}" cy="{my}" r="{rad}" fill="none" stroke="{RED}" stroke-width="1.5" opacity="0">'
        f'<animate attributeName="opacity" values="0;.7;0" dur="2.1s" begin="-{n(2.1 - k * 0.35)}s" repeatCount="indefinite"/></circle>'
        for k, rad in enumerate((30, 43, 56))
    ]
    out.append(
        f'<rect x="{mx - 11}" y="{my - 26}" width="22" height="40" rx="11" fill="{RED}"/>'
        f'<path d="M{mx - 18},{my + 2} a18,18 0 0 0 36,0 M{mx},{my + 20} v12 M{mx - 10},{my + 32} h20" fill="none" stroke="{TEXT}" '
        'stroke-width="2.5" stroke-linecap="round"/>'
        '<path d="M434,110 H582 M434,192 H582" stroke="#2b3f73" stroke-width="3" stroke-linecap="round"/>'
    )
    items = [
        (446, 108, 22, 30, CYAN), (478, 108, 28, 40, AMBER), (516, 108, 14, 46, GREEN), (540, 108, 22, 26, PINK),
        (446, 190, 30, 34, PINK), (486, 190, 22, 28, GREEN), (518, 190, 24, 44, CYAN), (552, 190, 18, 22, AMBER),
    ]
    for x, base, w, h, c in items:
        out.append(
            f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" rx="3" fill="{c}" fill-opacity=".18" stroke="{c}" stroke-width="1.6"/>'
            f'<rect x="{x + 3}" y="{n(base - h + h * 0.38)}" width="{w - 6}" height="{n(max(4, h * 0.22))}" fill="{c}" opacity=".7"/>'
        )
    stops = [(x - 5, base - h - 6, w + 10, h + 11) for x, base, w, h, _ in (items[1], items[3], items[4], items[6])]
    hops = "".join(
        f'<animate attributeName="{attr}" values="{";".join(str(s[i]) for s in stops)}" calcMode="discrete" dur="6s" repeatCount="indefinite"/>'
        for i, attr in enumerate(("x", "y", "width", "height"))
    )
    x0, y0, w0, h0 = stops[0]
    out.append(
        f'<rect x="{x0}" y="{y0}" width="{w0}" height="{h0}" fill="{GREEN}" fill-opacity=".08" stroke="{GREEN}" stroke-width="1.5" stroke-dasharray="5 3">{hops}</rect>'
        f'<text x="582" y="224" text-anchor="end" font-size="10" letter-spacing="1" fill="{DIM}">wake word / pantry / vision</text>'
    )
    return "".join(out), ""


# ── trophy wall ──────────────────────────────────────────────────────────────
def wins() -> str:
    W, H = 1000, 210
    r = random.Random(21)
    items = [
        ("HACK AI 2026", "DALLAS AI TRACK"), ("AXXESS 2026", "AI HEALTH PARTNER"), ("HACKUTD 2025", "T-MOBILE"),
        ("HACKUTD 2025", "BEST USE OF AUTH0"), ("FINHACK 2025", "WINNER"),
    ]
    b = [f'<rect width="{W}" height="{H}" fill="{PANEL}"/><rect width="{W}" height="{H}" fill="url(#grid)"/>']
    for _ in range(20):
        x, c = r.uniform(290, 985), r.choice([GOLD, PINK, CYAN, GREEN])
        b.append(
            f'<rect x="{n(x)}" y="-12" width="4" height="9" rx="1" fill="{c}" opacity=".45" transform="rotate({r.randint(-25, 25)} {n(x)} 0)">'
            f'<animate attributeName="y" values="-12;{H + 12}" dur="{n(r.uniform(4, 8))}s" begin="-{n(r.uniform(0, 8))}s" repeatCount="indefinite"/></rect>'
        )
    b.append(
        '<text x="36" y="128" font-size="108" font-weight="800" fill="url(#gold)">5&#215;</text>'
        f'<text x="40" y="168" font-size="15" font-weight="700" letter-spacing="5" fill="{TEXT}">HACKATHON WINS</text>'
        f'<path d="M270,30 V180" stroke="{LINE}" stroke-width="1.5"/>'
    )
    star = "M0,-7 L1.6,-1.6 L7,0 L1.6,1.6 L0,7 L-1.6,1.6 L-7,0 L-1.6,-1.6 Z"
    for i, (event, prize) in enumerate(items):
        cx, a = 350 + i * 140, 0.08 + i * 0.13
        b.append(
            f'<g>{trophy(cx - 33.6, 30, 2.8)}<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -9;0 0;0 0" '
            f'keyTimes="0;{a:.2f};{a + 0.04:.2f};{a + 0.09:.2f};1" dur="6s" repeatCount="indefinite"/></g>'
            f'<path transform="translate({cx + 26},{40})" d="{star}" fill="#fff" opacity="0"><animate attributeName="opacity" values="0;1;0" '
            f'dur="1.9s" begin="-{n(r.uniform(0, 1.9))}s" repeatCount="indefinite"/></path>'
            f'<text x="{cx}" y="132" text-anchor="middle" font-size="13.5" font-weight="700" letter-spacing="1.5" fill="{TEXT}">{event}</text>'
            f'<text x="{cx}" y="152" text-anchor="middle" font-size="10.5" letter-spacing="1" fill="{GOLD}">{prize}</text>'
        )
    b.append(brackets(W, H, GOLD, 10, 14, 0.55))
    grid = '<pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M25,0 H0 V25" fill="none" stroke="#111c33"/></pattern>'
    return svg(W, H, "".join(b), grid + GOLD_GRAD, title="Five hackathon wins: Hack AI 2026, Axxess 2026, HackUTD 2025 (two prizes), FinHack 2025")


# ── radar ────────────────────────────────────────────────────────────────────
def radar() -> str:
    W = H = 420
    cx, cy, T = 210, 214, 6
    b = [f'<rect width="{W}" height="{H}" fill="{PANEL}"/>']
    for rad in (60, 120, 180):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    b.append(f'<path d="M{cx - 186},{cy} H{cx + 186} M{cx},{cy - 186} V{cy + 186}" stroke="{LINE}" stroke-dasharray="3 6"/>')
    tx, ty = cx - 180 * math.sin(math.radians(55)), cy - 180 * math.cos(math.radians(55))
    b.append(
        f'<g><path d="M{cx},{cy} L{n(tx)},{n(ty)} A180,180 0 0 1 {cx},{cy - 180} Z" fill="url(#sw)"/>'
        f'<path d="M{cx},{cy} V{cy - 180}" stroke="{CYAN}" stroke-width="2"/>'
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{T}s" repeatCount="indefinite"/></g>'
    )
    blips = [
        (30, 150, "SELF-DRIVING", CYAN), (80, 100, "ADAS", CYAN), (135, 150, "LLM AGENTS", PINK),
        (200, 112, "ENERGY ML", AMBER), (255, 150, "MEDICAL AI", GREEN), (320, 105, "ROS 2", CYAN),
    ]
    for ang, rad, label, col in blips:
        x, y = cx + rad * math.sin(math.radians(ang)), cy - rad * math.cos(math.radians(ang))
        hit = ang / 360 * T
        b.append(
            f'<g opacity=".3"><circle cx="{n(x)}" cy="{n(y)}" r="5" fill="{col}"/>'
            f'<circle cx="{n(x)}" cy="{n(y)}" r="5" fill="none" stroke="{col}" stroke-width="1.5">'
            f'<animate attributeName="r" values="5;20" dur="{T}s" begin="{n(hit - T)}s" repeatCount="indefinite"/></circle>'
            f'<text x="{n(x)}" y="{n(y + 20)}" text-anchor="middle" font-size="12.5" font-weight="700" letter-spacing="1" fill="{col}">{label}</text>'
            f'<animate attributeName="opacity" values="1;.3" dur="{T}s" begin="{n(hit - T)}s" repeatCount="indefinite"/></g>'
        )
    b.append(
        f'<rect x="{cx - 8}" y="{cy - 15}" width="16" height="30" rx="5" fill="#16233f" stroke="{CYAN}" stroke-width="1.5"/>'
        f'<rect x="{cx - 5}" y="{cy - 9}" width="10" height="6" rx="1.5" fill="{CYAN}" opacity=".7"/>'
        f'<path d="M{cx - 10},{cy - 9} v6 M{cx + 10},{cy - 9} v6 M{cx - 10},{cy + 5} v6 M{cx + 10},{cy + 5} v6" stroke="{TEXT}" stroke-width="3" stroke-linecap="round"/>'
        f'<text x="22" y="34" font-size="13" letter-spacing="4" fill="{DIM}">ON MY RADAR</text>'
        f'<text x="398" y="400" text-anchor="end" font-size="10" letter-spacing="2" fill="{DIM}">360° / 40 HZ</text>'
    )
    b.append(brackets(W, H, CYAN, 10, 14, 0.55))
    defs = (
        f'<linearGradient id="sw" gradientUnits="userSpaceOnUse" x1="{n(tx)}" y1="{n(ty)}" x2="{cx}" y2="{cy - 120}">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".4"/></linearGradient>'
    )
    return svg(W, H, "".join(b), defs, title="Radar sweep: self-driving, ADAS, LLM agents, energy ML, medical AI, ROS 2")


# ── contact buttons + footer ─────────────────────────────────────────────────
def button(label: str, accent: str, w: int = 260) -> str:
    H = 58
    b = (
        f'<rect width="{w}" height="{H}" fill="{PANEL}"/>'
        f'<circle cx="28" cy="29" r="3.5" fill="{accent}"/>'
        + "".join(
            f'<path d="M{28 + rad * 0.5:.1f},{29 - rad * 0.87:.1f} A{rad},{rad} 0 0 1 {28 + rad * 0.5:.1f},{29 + rad * 0.87:.1f}" fill="none" '
            f'stroke="{accent}" stroke-width="2" stroke-linecap="round"><animate attributeName="opacity" values=".15;1;.15" dur="1.5s" '
            f'begin="-{n(1.5 - k * 0.25)}s" repeatCount="indefinite"/></path>'
            for k, rad in enumerate((9, 15))
        )
        + f'<text x="56" y="35" font-size="16" font-weight="700" letter-spacing="3" fill="{TEXT}">{label}</text>'
        f'<g><path d="M{w - 32},22 l7,7 l-7,7" fill="none" stroke="{accent}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<animateTransform attributeName="transform" type="translate" values="0 0;5 0;0 0" dur="1.4s" repeatCount="indefinite"/></g>'
    )
    return svg(w, H, b, rx=12, title=label)


def footer() -> str:
    W, H = 1000, 112
    chk = (
        '<pattern id="chk" width="24" height="24" patternUnits="userSpaceOnUse"><rect width="12" height="12" fill="#e6eefb"/>'
        '<rect x="12" y="12" width="12" height="12" fill="#e6eefb"/></pattern>'
    )
    b = (
        f'<rect width="{W}" height="{H}" fill="{PANEL}"/>'
        + loop(f'<rect width="{W + 48}" height="12" fill="url(#chk)" opacity=".8"/><rect y="{H - 12}" width="{W + 48}" height="12" fill="url(#chk)" opacity=".8"/>', 24, 1.2)
        + f'<text x="500" y="50" text-anchor="middle" font-size="19" font-weight="700" letter-spacing="7" fill="{TEXT}">THANKS FOR STOPPING BY</text>'
        f'<path d="M0,90 H{W}" stroke="{LINE}" stroke-width="2" stroke-dasharray="10 8"/>'
        f'<g><g transform="scale(.26)">{mini_car(CYAN)}</g><animateTransform attributeName="transform" type="translate" '
        f'values="-120 65;1090 65;1090 65" keyTimes="0;.4;1" dur="7s" repeatCount="indefinite"/></g>'
    )
    return svg(W, H, b, chk + mini_trail(CYAN), rx=14, title="Chequered flag. Thanks for stopping by.")


# ── build ────────────────────────────────────────────────────────────────────
def main() -> None:
    OUT.mkdir(exist_ok=True)
    files = {
        "hero.svg": hero(),
        "h-profile.svg": header("01", "DRIVER PROFILE", CYAN, "car", 1),
        "h-podium.svg": header("02", "PODIUM", GOLD, "trophy"),
        "wins.svg": wins(),
        "h-grid.svg": header("03", "STARTING GRID", PINK, "lights"),
        "h-power.svg": header("04", "POWER UNIT", GREEN, "shift"),
        "h-radio.svg": header("05", "TEAM RADIO", CYAN, "radio", 5),
        "radar.svg": radar(),
        "footer.svg": footer(),
        "btn-email.svg": button("EMAIL", PINK, 200),
        "btn-github.svg": button("ALL REPOS", CYAN, 240),
    }
    winners = [
        ("w1-pondr.svg", "WINNER", "Pondr", "HACK AI 2026", GREEN, art_pondr),
        ("w2-maternalguard.svg", "WINNER", "MaternalGuard", "AXXESS HACKATHON 2026", PINK, art_maternal),
        ("w3-harmoniq.svg", "2&#215; WINNER", "HarmoniQ", "HACKUTD 2025", CYAN, art_harmoniq),
        ("w4-quada.svg", "WINNER", "QUADA", "FINHACK 2025", AMBER, art_quada),
    ]
    grid = [
        ("p1-rsna.svg", "P1", "RSNA Knee", "KAGGLE / KNEE MRI", PINK, art_rsna),
        ("p2-arkos.svg", "P2", "Arkos", "HACK AI 2025", AMBER, art_arkos),
        ("p3-ovascope.svg", "P3", "OvaScope", "MEDICAL IMAGING", CYAN, art_ovascope),
        ("p4-jarvis.svg", "P4", "Jarvis", "PERSONAL AI ASSISTANT", CYAN, art_jarvis),
        ("p5-f1tenth.svg", "P5", "F1TENTH", "AUTONOMOUS RACING", PINK, art_f1tenth),
        ("p6-codered.svg", "P6", "CodeRed", "VOICE KITCHEN ASSISTANT", RED, art_codered),
    ]
    for fname, pos, name, tag, accent, art in winners:
        body, defs = art()
        files[fname] = card(pos, name, tag, accent, body, defs, badge=GOLD)
    for fname, pos, name, tag, accent, art in grid:
        body, defs = art()
        files[fname] = card(pos, name, tag, accent, body, defs)
    for stale in OUT.glob("*.svg"):
        if stale.name not in files:
            stale.unlink()
    for fname, content in files.items():
        (OUT / fname).write_text(content, encoding="utf-8", newline="\n")
        print(f"{fname:24} {len(content) / 1024:5.1f} KB")


if __name__ == "__main__":
    main()
