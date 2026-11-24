"""Ortam çizimleri: gökyüzü, bulut, dağ, zemin, ağaç, rüzgar tulumu, akış çizgileri, termik, girdap."""
import math
import random
import numpy as np
import skia
from .gfx import C, P, W, H, lin, rad, cached, SAMPLING, clamp, lerp, smooth, ease_out, smooth_path, poly, mix, shade, hexrgb, PAL

THEMES = {
    "day": ["#1557E0", "#3D8BFA", "#8CC8FF", "#D8F0FF"],
    "bright": ["#2F7BF5", "#5AA9FF", "#A6DBFF", "#E6F6FF"],
    "golden": ["#2B3E8F", "#6A6FC0", "#F1A86B", "#FFE0B0"],
    "storm": ["#1F2937", "#3B4656", "#6B7787", "#9AA5B1"],
    "dusk": ["#0F1B3D", "#2C3E8C", "#B75D7A", "#F7B26A"],
    "studio": ["#0B1220", "#111C33", "#162544", "#1B2D52"],
}


def sky(c, theme="day", sun=(860, 300), sun_alpha=1.0, y0=0, y1=H):
    def draw(cv):
        cols = THEMES.get(theme, THEMES["day"])
        cv.drawRect(skia.Rect.MakeXYWH(0, 0, W, y1 - y0), skia.Paint(Shader=lin((0, 0), (0, y1 - y0), cols, [0, 0.35, 0.75, 1.0])))
        if sun and sun_alpha > 0 and theme not in ("storm", "studio"):
            sx, sy = sun[0], sun[1] - y0
            cv.drawCircle(sx, sy, 520, skia.Paint(Shader=rad((sx, sy), 520, [C("#FFF6D8", 0.55 * sun_alpha), C("#FFF6D8", 0.0)])))
            cv.drawCircle(sx, sy, 70, P("#FFFBEA", 0.95 * sun_alpha, blur=6))
    img = cached(("sky", theme, tuple(sun) if sun else None, round(sun_alpha, 2), y0, y1), W, y1 - y0, draw)
    c.drawImage(img, 0, y0)


def studio_bg(c, accent="#FF6A1A", t=0.0):
    """Diyagramlar için koyu, modern 'stüdyo' arka plan (ızgara + ışık)."""
    def base(cv):
        cols = THEMES["studio"]
        cv.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=lin((0, 0), (0, H), cols, [0, 0.35, 0.75, 1.0])))
        cv.drawCircle(540, 900, 900, skia.Paint(Shader=rad((540, 900), 900, [C(accent, 0.16), C(accent, 0.0)])))
    def vig(cv):
        cv.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=rad((540, 960), 1300, [C("#000000", 0.0), C("#000000", 0.55)], [0.45, 1.0])))
    c.drawImage(cached(("studio", accent), W, H, base), 0, 0)
    gp = P("#FFFFFF", 0.045, stroke=2)
    off = (t * 12) % 90
    path = skia.Path()
    for x in range(-90, W + 90, 90):
        path.moveTo(x + off, 0)
        path.lineTo(x + off, H)
    for y in range(-90, H + 90, 90):
        path.moveTo(0, y + off)
        path.lineTo(W, y + off)
    c.drawPath(path, gp)
    c.drawImage(cached(("studio_vig",), W, H, vig), 0, 0)


# ---------------------------------------------------------------- bulutlar
_CLOUD_IMG = {}


def _cloud_image(seed, w=520, h=230, dark=0.0):
    key = (seed, w, h, round(dark, 2))
    if key in _CLOUD_IMG:
        return _CLOUD_IMG[key]
    rnd = random.Random(seed)
    s = skia.Surface(w + 160, h + 160)
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    top = mix("#FFFFFF", "#6B7280", dark)
    bot = mix("#DCE7F3", "#374151", dark)
    shader = lin((0, 40), (0, h + 120), [C(top), C(bot)])
    p = skia.Paint(AntiAlias=True, Shader=shader, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 7))
    base_y = h + 60
    for i in range(14):
        cx = 80 + rnd.uniform(0.12, 0.88) * w
        rr = rnd.uniform(0.18, 0.34) * h * (1.3 - abs(cx - 80 - w / 2) / w)
        cy = base_y - rr * rnd.uniform(0.6, 1.4)
        c.drawCircle(cx, cy, rr, p)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(80 + w * 0.08, base_y - h * 0.22, w * 0.84, h * 0.22), 40, 40), p)
    img = s.makeImageSnapshot()
    _CLOUD_IMG[key] = img
    return img


def clouds(c, t=0.0, layer=0, alpha=0.9, count=4, y_range=(180, 900), speed=8.0, scale=1.0, seed=3, dark=0.0, camx=0.0):
    rnd = random.Random(seed * 101 + layer)
    for i in range(count):
        img = _cloud_image(seed * 7 + i, 520, 220, dark)
        sc = rnd.uniform(0.6, 1.25) * scale
        span = W + 900
        x = (rnd.uniform(0, span) + t * speed * sc - camx * (0.15 + 0.1 * layer)) % span - 450
        y = rnd.uniform(*y_range)
        dst = skia.Rect.MakeXYWH(x - img.width() * sc / 2, y - img.height() * sc / 2, img.width() * sc, img.height() * sc)
        c.drawImageRect(img, dst, skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(AntiAlias=True, Alphaf=alpha))


# ---------------------------------------------------------------- dağlar
_RIDGE = {}


def _ridge_profile(seed, n=400, rough=0.5):
    if (seed, n, rough) in _RIDGE:
        return _RIDGE[(seed, n, rough)]
    rnd = np.random.default_rng(seed)
    xs = np.linspace(0, 1, n)
    y = np.zeros(n)
    amp = 1.0
    for octv in range(5):
        k = 2 ** octv * 2
        ph = rnd.uniform(0, 2 * np.pi, 3)
        y += amp * (np.sin(xs * k * np.pi + ph[0]) * 0.6 + np.sin(xs * k * 1.7 * np.pi + ph[1]) * 0.4)
        amp *= rough
    y = (y - y.min()) / (y.max() - y.min() + 1e-9)
    _RIDGE[(seed, n, rough)] = y
    return y


def _mountain_layer_img(seed, hgt, ctop, cbot, i):
    period = 2600
    prof = _ridge_profile(seed)
    n = len(prof)
    top = hgt + i * 10 + 10
    hh = top + 70

    def draw(cv):
        path = skia.Path()
        path.moveTo(0, hh)
        steps = 260
        for k in range(steps + 1):
            sx = k * (period + W) / steps
            u = (sx % period) / period
            idx = u * (n - 1)
            i0 = int(idx)
            fr = idx - i0
            v = prof[i0] * (1 - fr) + prof[min(i0 + 1, n - 1)] * fr
            path.lineTo(sx, top - v * hgt - i * 10)
        path.lineTo(period + W, hh)
        path.close()
        cv.drawPath(path, skia.Paint(AntiAlias=True, Shader=lin((0, top - hgt), (0, top + 60), [C(ctop), C(cbot)])))
    return cached(("mtn", seed, hgt, ctop, cbot, i), period + W, hh, draw), top, hh


def mountains(c, base_y=1150, camx=0.0, layers=None, haze="#BFE3FF"):
    """Paralaks dağ katmanları. layers: [(seed, yükseklik, renk_üst, renk_alt, paralaks)]"""
    if layers is None:
        layers = [
            (11, 330, "#8DB6E8", "#B9D7F3", 0.10),
            (23, 260, "#5C86C0", "#86A9D6", 0.22),
            (37, 210, "#3F6E8C", "#5B8AA6", 0.40),
        ]
    for i, (seed, hgt, ctop, cbot, par) in enumerate(layers):
        img, top, hh = _mountain_layer_img(seed, hgt, ctop, cbot, i)
        off = (camx * par) % 2600
        y = base_y - top
        c.drawImageRect(img, skia.Rect.MakeXYWH(off, 0, W, hh), skia.Rect.MakeXYWH(0, y, W, hh), SAMPLING, None)
        if y + hh < H:
            c.drawRect(skia.Rect.MakeXYWH(0, y + hh - 1, W, H - (y + hh) + 1), P(cbot))
    def hz(cv):
        cv.drawRect(skia.Rect.MakeXYWH(0, 0, W, 220), skia.Paint(Shader=lin((0, 0), (0, 220), [C(haze, 0.0), C(haze, 0.45)])))
    c.drawImage(cached(("haze", haze), W, 220, hz), 0, base_y - 140)


def ground(c, y=1350, camx=0.0, color_top="#6CC46A", color_bot="#2F7D43", stripes=True):
    def gd(cv):
        cv.drawRect(skia.Rect.MakeWH(W, 1000), skia.Paint(Shader=lin((0, 0), (0, 1000), [C(color_top), C(color_bot)])))
    if y < H:
        c.drawImageRect(cached(("ground", color_top, color_bot), W, 1000, gd), skia.Rect.MakeXYWH(0, y, W, max(1, H - y)), SAMPLING)
    if stripes:
        # perspektif biçilmiş çim şeritleri
        p = skia.Path()
        for k in range(-12, 13):
            x0 = 540 + k * 160 - (camx * 1.0) % 160
            p.moveTo(x0, y)
            p.lineTo(x0 + 80, y)
            p.lineTo(540 + (x0 + 80 - 540) * 3.2, H)
            p.lineTo(540 + (x0 - 540) * 3.2, H)
            p.close()
        c.drawPath(p, P("#FFFFFF", 0.045))
    c.drawRect(skia.Rect.MakeXYWH(0, y - 2, W, 6), P("#FFFFFF", 0.18))


def tree(c, x, y, s=1.0, color="#2E7D4F", alpha=1.0):
    c.drawLine(x, y, x, y - 40 * s, P("#5B3A1E", alpha, stroke=9 * s))
    c.drawCircle(x, y - 70 * s, 38 * s, P(color, alpha))
    c.drawCircle(x - 14 * s, y - 80 * s, 18 * s, P(shade(color, 1.25), alpha * 0.6))


def target(c, x, y, rx=150, ry=40, alpha=1.0, pulse_t=None):
    for k, col in enumerate(["#FFFFFF", "#F43F5E", "#FFFFFF", "#F43F5E"]):
        f = 1 - k * 0.25
        c.drawOval(skia.Rect.MakeXYWH(x - rx * f, y - ry * f, 2 * rx * f, 2 * ry * f), P(col, alpha * 0.85))
    if pulse_t is not None:
        k = (pulse_t % 1.2) / 1.2
        f = 1 + k * 0.8
        c.drawOval(skia.Rect.MakeXYWH(x - rx * f, y - ry * f, 2 * rx * f, 2 * ry * f), P("#FFFFFF", alpha * (1 - k) * 0.8, stroke=4))


# ---------------------------------------------------------------- rüzgar tulumu
def windsock(c, x, y, s=1.0, strength=0.6, t=0.0, direction=1, gusty=0.0, alpha=1.0, pole=260):
    """strength: 0 (sarkık) .. 1 (dimdik). direction: +1 sağa doğru eser, -1 sola."""
    top = y - pole * s
    c.drawLine(x, y, x, top, P("#E5E7EB", alpha, stroke=10 * s))
    c.drawCircle(x, top, 9 * s, P("#E5E7EB", alpha))
    st = clamp(strength + gusty * 0.35 * math.sin(t * 7.3) * math.sin(t * 3.1))
    flap = (0.06 + 0.10 * (1 - st)) * math.sin(t * (6 + 6 * st))
    ang = math.radians(lerp(8, 86, st)) + flap  # 0: dikey sarkık, 1: yatay dimdik
    L = 230 * s
    segs = 5
    pts_top, pts_bot = [], []
    r0 = 34 * s
    for k in range(segs + 1):
        u = k / segs
        a = ang + (1 - st) * 0.5 * u + math.sin(t * 8 + u * 4) * 0.05 * (1 + gusty)
        px = x + direction * math.sin(a) * L * u
        py = top + math.cos(a) * L * u
        rr = r0 * (1 - 0.45 * u) * (0.55 + 0.45 * st)
        nx, ny = math.cos(a) * direction, -math.sin(a)
        pts_top.append((px - nx * rr, py - ny * rr))
        pts_bot.append((px + nx * rr, py + ny * rr))
    for k in range(segs):
        quad = [pts_top[k], pts_top[k + 1], pts_bot[k + 1], pts_bot[k]]
        col = "#FF6A1A" if k % 2 == 0 else "#F8FAFC"
        c.drawPath(poly(quad), P(col, alpha))
    c.drawOval(skia.Rect.MakeLTRB(min(pts_top[0][0], pts_bot[0][0]) - 4, min(pts_top[0][1], pts_bot[0][1]) - 2,
                                  max(pts_top[0][0], pts_bot[0][0]) + 4, max(pts_top[0][1], pts_bot[0][1]) + 2), P("#9CA3AF", alpha, stroke=4 * s))


# ---------------------------------------------------------------- akış / rüzgar
def flow_lines(c, paths, t, color="#FFFFFF", alpha=0.85, width=5, speed=0.35, dash=0.18, gap=0.12, glow=True):
    """Yollar boyunca akan kesikli çizgiler (rüzgar)."""
    for i, path in enumerate(paths):
        meas = skia.PathMeasure(path, False)
        L = meas.getLength()
        if L <= 0:
            continue
        period = (dash + gap) * L
        ph = ((t * speed + i * 0.137) % 1.0) * period
        p = P(color, alpha, stroke=width)
        p.setPathEffect(skia.DashPathEffect.Make([dash * L, gap * L], -ph))
        if glow:
            g = P(color, alpha * 0.25, stroke=width * 2.6, blur=width)
            g.setPathEffect(skia.DashPathEffect.Make([dash * L, gap * L], -ph))
            c.drawPath(path, g)
        c.drawPath(path, p)


def wind_particles(c, t, rect, n=40, speed=420, color="#FFFFFF", alpha=0.6, length=60, seed=5, angle=0.0, wobble=0.0):
    rnd = random.Random(seed)
    x0, y0, w, h = rect
    ca, sa = math.cos(angle), math.sin(angle)
    for i in range(n):
        px = (rnd.uniform(0, w + 300) + t * speed * rnd.uniform(0.7, 1.3)) % (w + 300) - 150
        py = rnd.uniform(0, h) + math.sin(t * 2 + i) * wobble
        x, y = x0 + px, y0 + py
        ln = length * rnd.uniform(0.5, 1.2)
        a = alpha * rnd.uniform(0.4, 1.0) * clamp(min(px + 150, w + 150 - px) / 150)
        c.drawLine(x, y, x - ca * ln, y - sa * ln, P(color, a, stroke=3))


def swirl(c, x, y, r, t, color="#F43F5E", alpha=0.85, turns=1.6, width=6, spin=1.0):
    """Rotor/türbülans girdabı."""
    for k in range(3):
        path = skia.Path()
        ph = t * 3.2 * spin + k * 2.094
        first = True
        for i in range(60):
            u = i / 59
            a = ph + u * turns * 2 * math.pi
            rr = r * (0.25 + 0.75 * u)
            px, py = x + math.cos(a) * rr, y + math.sin(a) * rr * 0.75
            if first:
                path.moveTo(px, py)
                first = False
            else:
                path.lineTo(px, py)
        c.drawPath(path, P(color, alpha * (0.5 + 0.25 * k), stroke=width * (0.6 + 0.2 * k)))


def bubble(c, x, y, r, t=0.0, color="#FB923C", alpha=0.55):
    """Termik baloncuğu (sıcak hava kütlesi)."""
    c.drawCircle(x, y, r * 1.25, skia.Paint(AntiAlias=True, Shader=rad((x, y), r * 1.25, [C(color, alpha * 0.9), C(color, 0.0)])))
    c.drawCircle(x, y, r, P(color, alpha * 0.6, stroke=4))
    for i in range(5):
        a = t * 1.5 + i * 1.26
        c.drawCircle(x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.4, r * 0.12, P("#FFFFFF", alpha * 0.5))


def cumulus(c, x, y, w, growth=1.0, dark=0.0, alpha=1.0, seed=9, tall=0.0, anvil=0.0, t=0.0):
    """Kümülüs -> kümülonimbüs. tall: dikey gelişim (0..1), anvil: örs (0..1)."""
    if growth <= 0.01:
        return
    rnd = random.Random(seed)
    top = mix("#FFFFFF", "#4B5563", dark)
    bot = mix("#CBD5E1", "#1F2937", dark)
    hgt = w * (0.35 + 0.95 * tall) * growth
    p = skia.Paint(AntiAlias=True, Shader=lin((0, y - hgt), (0, y), [C(top, alpha), C(bot, alpha)]),
                   MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5))
    n = 9 + int(tall * 12)
    for i in range(n):
        u = rnd.random()
        v = rnd.random()
        width_at = w * (0.5 + 0.3 * (1 - v)) * growth * (1 - 0.35 * tall * v)
        cx = x + (u - 0.5) * width_at
        cy = y - v * hgt * 0.85 - w * 0.08
        rr = w * rnd.uniform(0.13, 0.22) * growth * (1 + 0.4 * tall)
        cy += math.sin(t * 0.8 + i) * 3
        c.drawCircle(cx, cy, rr, p)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w * 0.45 * growth, y - w * 0.16 * growth, w * 0.9 * growth, w * 0.16 * growth), 30, 30), p)
    if anvil > 0:
        aw = w * (0.8 + 0.75 * anvil)
        ay = y - hgt - w * 0.02
        pa = skia.Paint(AntiAlias=True, Color=C(mix("#E5E7EB", "#6B7280", dark * 0.8), alpha * anvil),
                        MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - aw / 2, ay - 70, aw, 90), 45, 45), pa)
        rnd2 = random.Random(seed + 5)
        for i in range(9):
            u = rnd2.uniform(-0.45, 0.45)
            c.drawCircle(x + u * aw, ay - 70 + rnd2.uniform(-10, 20), w * rnd2.uniform(0.07, 0.12), pa)
        # örsün sivri uçları
        tri = skia.Path()
        tri.moveTo(x + aw / 2 - 20, ay - 60)
        tri.lineTo(x + aw / 2 + 90 * anvil, ay - 40)
        tri.lineTo(x + aw / 2 - 30, ay + 15)
        tri.close()
        c.drawPath(tri, pa)


def lightning(c, x, y, h, t, alpha=1.0, seed=1):
    rnd = random.Random(seed + int(t * 3))
    if (t * 3) % 1.0 > 0.25:
        return
    pts = [(x, y)]
    for i in range(6):
        pts.append((pts[-1][0] + rnd.uniform(-40, 40), pts[-1][1] + h / 6))
    path = poly(pts, close=False)
    c.drawPath(path, P("#FDE68A", alpha * 0.5, stroke=18, blur=10))
    c.drawPath(path, P("#FFFBEB", alpha, stroke=5))


def rain(c, rect, t, alpha=0.5, n=80, seed=2):
    rnd = random.Random(seed)
    x0, y0, w, h = rect
    for i in range(n):
        px = x0 + rnd.uniform(0, w)
        py = y0 + (rnd.uniform(0, h) + t * 900) % h
        c.drawLine(px, py, px - 8, py + 34, P("#CBD5E1", alpha, stroke=2.5))


def hill_profile(x0, x1, base, peak_x, peak_y, steep_l=1.0, steep_r=1.0, n=60):
    """Yamaç kesiti (dağ profili) nokta listesi."""
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        if x <= peak_x:
            u = (x - x0) / max(1, peak_x - x0)
            v = smooth(u) ** steep_l
        else:
            u = (x1 - x) / max(1, x1 - peak_x)
            v = smooth(u) ** steep_r
        pts.append((x, base - (base - peak_y) * v))
    return pts


def draw_hill(c, pts, base, col_top="#4F9A5B", col_bot="#2E6B3C", rock=False, alpha=1.0):
    path = skia.Path()
    path.moveTo(pts[0][0], base + 400)
    for p in pts:
        path.lineTo(*p)
    path.lineTo(pts[-1][0], base + 400)
    path.close()
    top_y = min(p[1] for p in pts)
    c.drawPath(path, skia.Paint(AntiAlias=True, Shader=lin((0, top_y), (0, base + 200), [C(col_top, alpha), C(col_bot, alpha)])))
    c.drawPath(smooth_path(pts), P("#FFFFFF", 0.22 * alpha, stroke=4))


def vario(c, x, y, value, t=0.0, alpha=1.0, scale=1.0):
    """Vario göstergesi: değer m/s (pozitif = yükselme)."""
    w, h = 300 * scale, 130 * scale
    from .gfx import glass, draw_text
    glass(c, x - w / 2, y - h / 2, w, h, 30 * scale, alpha=0.62 * alpha)
    col = "#34D399" if value > 0.05 else ("#F43F5E" if value < -1.5 else "#FBBF24")
    sign = "+" if value > 0.05 else ("−" if value < -0.05 else "")
    draw_text(c, f"{sign}{abs(value):.1f}", x - 20 * scale, y + 26 * scale, 76 * scale, col, "black", "center", alpha)
    draw_text(c, "m/s", x + 105 * scale, y + 22 * scale, 30 * scale, "#CBD5E1", "semi", "center", alpha)
    draw_text(c, "VARİO", x, y - 40 * scale, 22 * scale, "#94A3B8", "bold", "center", alpha, tracking=0.12)
    # ok
    ax = x - 125 * scale
    if abs(value) > 0.05:
        d = -1 if value > 0 else 1
        bob = math.sin(t * 8) * 4 * scale
        pts = [(ax, y + d * 22 * scale + bob), (ax - 16 * scale, y - d * 8 * scale + bob), (ax + 16 * scale, y - d * 8 * scale + bob)]
        c.drawPath(poly(pts), P(col, alpha))
