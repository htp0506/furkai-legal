"""'stage' sahnesi: havada tek kanat, her parametre faz faz yumuşakça değişir.

Kapanma, kulak katlama, dönüş, stol, negatif, yedek paraşüt ve anatomi derslerinin ana sahnesi.
Parametreler (hepsi isteğe bağlı):
  bg: 'sky' | 'high' (yüksek irtifa, aşağıda dağlar) | 'studio'
  x, y, scale, yaw, elev, pitch, roll, heading, spin (rad/sn dönme hızı)
  brake_l, brake_r, fold_l, fold_r, ears, front, stall, crumple, inflate, weight, bar
  shake: türbülans titreşimi
  callouts: [(metin, çapa, (etiket_x, etiket_y), renk)]  çapa: 'le:0.3', 'te:-0.6', 'top:0', 'mouth:0.2',
            'pilot', 'pt:x,y,z' (model noktası), 'ppt:x,y,z' (pilot çerçevesi)
  hl: vurgulanacak hat grupları {'A':'#renk', 'B':..., 'brake':...}
  arrows: [('rot', yön)], [('down',)], [('weight', yön)], [('pump', taraf)], [('air',)]
  widgets: ['vario', 'speed', 'brakes']; vario, kmh değerleri
  reserve: 0..1 yedek paraşüt açılması, reserve_throw: 0..1 atılış
"""
import math
import skia
from ..core import scene
from ..gfx import (C, P, W, H, draw_text, text_width, glass, chip, rrect, lin, rad, clamp, lerp, ease_out, ease_in,
                   ease_io, ease_back, smooth, remap, smooth_path, poly, arrow, line_arrow, pulse, circle)
from .. import world, glider3d as g3
from .flight import widget_speed, widget_brake


def _bg(c, S, t):
    bg = S.get("bg", "sky")
    if bg == "studio":
        world.studio_bg(c, S.get("accent", "#FF6A1A"), S.t)
        return
    theme = S.get("theme", "day")
    world.sky(c, theme)
    drift = t * S.get("drift", 30)
    if bg == "high":
        world.clouds(c, t, 1, alpha=0.55, count=3, y_range=(1350, 1700), speed=20, scale=0.7, camx=drift)
        world.mountains(c, base_y=1880, camx=drift,
                        layers=[(11, 300, "#9BBCE6", "#C3DAF3", 0.15), (23, 240, "#7FA3CF", "#A5C1E3", 0.3)])
        world.clouds(c, t, 0, alpha=0.85, count=4, y_range=(250, 900), speed=14, camx=drift * 2)
    else:
        world.clouds(c, t, 0, alpha=0.85, count=5, y_range=(250, 1300), speed=14, camx=drift * 2)
        world.mountains(c, base_y=1750, camx=drift)


def resolve_anchor(info, anchor):
    kind, _, arg = anchor.partition(":")
    if kind in ("le", "te", "top", "mouth"):
        return info["surf"](kind, float(arg or 0))
    if kind == "pilot":
        return info["pilot"]
    if kind == "pt":
        return info["proj"]([float(v) for v in arg.split(",")])
    if kind == "ppt":
        return info["proj"]([float(v) for v in arg.split(",")], pilot_frame=True)
    raise ValueError(anchor)


def draw_callouts(c, S, info, callouts, t0_key=None):
    for i, co in enumerate(callouts or []):
        txt, anchor, lab = co[0], co[1], co[2]
        col = co[3] if len(co) > 3 else "#FFD23F"
        delay = co[4] if len(co) > 4 else 0.15 + i * 0.25
        a = ease_out(remap(S.pts, delay, delay + 0.4))
        if a <= 0 or info is None:
            continue
        ax, ay = resolve_anchor(info, anchor)
        lx, ly = lab
        # bağlantı çizgisi
        k = ease_io(remap(S.pts, delay, delay + 0.35))
        c.drawLine(ax, ay, lerp(ax, lx, k), lerp(ay, ly, k), P("#FFFFFF", 0.9 * a, stroke=3))
        r = 12 + 6 * pulse(S.t, 1.0)
        c.drawCircle(ax, ay, r + 6, P(col, 0.25 * a))
        c.drawCircle(ax, ay, 10, P(col, a))
        c.drawCircle(ax, ay, 10, P("#FFFFFF", a, stroke=3))
        fg = "#1F1300" if col in ("#FFD23F", "#FFB020", "#22D3EE", "#34D399") else "white"
        chip(c, txt, lx, ly, 38, col, fg, alpha=a, weight="black", pad=(24, 14))


def reserve_canopy(c, cx, cy, r, open_k, t, alpha=1.0, pilot=None):
    """Yuvarlak yedek paraşüt (2D). open_k 0..1"""
    if open_k <= 0.01:
        return
    w = r * (0.25 + 0.75 * ease_out(open_k))
    h = r * (0.55 + 0.25 * (1 - open_k))
    breath = 1 + 0.03 * math.sin(t * 3)
    rect = skia.Rect.MakeXYWH(cx - w * breath, cy - h, 2 * w * breath, 2 * h)
    path = skia.Path()
    path.addArc(rect, 180, 180)
    path.close()
    c.drawPath(path, skia.Paint(AntiAlias=True, Shader=lin((cx, cy - h), (cx, cy), [C("#FFFFFF", alpha), C("#CBD5E1", alpha)])))
    # dilimler
    for k in range(1, 8):
        a = math.pi + k * math.pi / 8
        x2, y2 = cx + math.cos(a) * w * breath, cy + math.sin(a) * h
        col = "#F43F5E" if k % 2 else "#FFFFFF"
        c.drawLine(cx, cy - h * 0.92, x2, y2, P("#94A3B8", 0.6 * alpha, stroke=2))
    c.drawPath(path, P("#F43F5E", alpha, stroke=5))
    # etek ve hatlar
    if pilot:
        px, py = pilot
        for k in range(9):
            xx = cx - w * breath + k * (2 * w * breath) / 8
            c.drawLine(xx, cy, px, py, P("#CBD5E1", 0.8 * alpha, stroke=1.6))


def _rot_arrow(c, cx, cy, rx, ry, direction, t, color="#F43F5E", alpha=1.0):
    path = skia.Path()
    n = 40
    ph = (t * 1.2) % 1.0
    a0 = -0.3
    pts = []
    for i in range(n + 1):
        u = i / n
        a = a0 + direction * u * 2.4
        pts.append((cx + math.cos(a) * rx, cy + math.sin(a) * ry))
    path = smooth_path(pts)
    arrow(c, path, color, width=10, progress=0.35 + 0.65 * ease_io(min(1, ph * 1.6)), alpha=alpha, head=34, glow=True)


@scene("stage")
def stage(c, S):
    t = S.gt
    _bg(c, S, t)
    shake = S.v("shake", 0.0)
    sx = math.sin(t * 13.0) * 8 * shake
    sy = math.cos(t * 11.0) * 6 * shake
    x = S.v("x", 540) + sx
    y = S.v("y", 1000) + sy + math.sin(t * 1.3) * 6
    scale = S.v("scale", 62, dur=1.0)
    heading = S.v("heading", 0.0, dur=1.0) + S.get("spin", 0.0) * S.pts
    kw = dict(
        yaw=S.v("yaw", g3.REAR_34, dur=1.0), elev=S.v("elev", 0.18, dur=1.0),
        pitch=S.v("pitch", 0.0) + shake * 0.06 * math.sin(t * 7), roll=S.v("roll", 0.0) + shake * 0.05 * math.sin(t * 9),
        heading=heading, brake_l=S.v("brake_l", 0.0, dur=0.5), brake_r=S.v("brake_r", 0.0, dur=0.5),
        fold_l=S.v("fold_l", 0.0, dur=S.get("fold_dur", 0.35)), fold_r=S.v("fold_r", 0.0, dur=S.get("fold_dur", 0.35)),
        fold_pos=S.get("fold_pos", 0.3),
        ears=S.v("ears", 0.0, dur=0.9), front=S.v("front", 0.0, dur=S.get("front_dur", 0.35)),
        stall=S.v("stall", 0.0, dur=0.8), crumple=S.v("crumple", 0.0) + shake * 0.08,
        inflate=S.v("inflate", 1.0, dur=1.2), weight=S.v("weight", 0.0, dur=0.6), bar=S.v("bar", 0.0, dur=0.6),
        flat=S.v("flat", 0.0, dur=1.0), pose=S.v("stand", 0.0), hl=S.get("hl"), line_alpha=S.v("line_alpha", 1.0),
        anchor=S.get("anchor", "center"), t=t,
    )
    # pompa: fren tek tarafta yavaş bas-bırak
    pump = S.get("pump")
    if pump:
        k = 0.5 - 0.5 * math.cos(S.pts * 2 * math.pi / 1.6)
        kw["brake_l" if pump < 0 else "brake_r"] = 0.15 + 0.75 * k
    # kulak katlama: dış A hatlarını tutan eller
    if S.get("ears_hands"):
        e = kw["ears"]
        kw["hands"] = {-1: [-0.55 * e - 0.32 * (1 - e), 0.55 + 0.25 * e, 0.05], 1: [0.55 * e + 0.32 * (1 - e), 0.55 + 0.25 * e, 0.05]}
    info = g3.render(c, x, y, scale, **kw)
    # yedek paraşüt
    rv = S.v("reserve", 0.0, dur=1.2)
    if rv > 0 and info:
        px, py = info["pilot"]
        thr = S.v("reserve_throw", 1.0, dur=0.6)
        rx = px + 240 * (1 - rv) * thr
        ry = py - (430 * rv + 120 * (1 - rv)) * thr
        if rv < 0.25:
            # paket uçuyor
            c.drawCircle(lerp(px + 40, rx, thr), lerp(py, ry, thr), 26, P("#F43F5E"))
            c.drawLine(px, py, lerp(px + 40, rx, thr), lerp(py, ry, thr), P("#CBD5E1", stroke=2))
        else:
            reserve_canopy(c, rx, ry, 230, remap(rv, 0.25, 1.0), t, pilot=(px, py))
    # oklar
    for ar in S.get("arrows", []) or []:
        kind = ar[0]
        aa = ease_out(remap(S.pts, 0.2, 0.6))
        if kind == "rot" and info:
            bx0, by0, bx1, by1 = info["bbox"]
            _rot_arrow(c, x, (by0 + by1) / 2 - 60, (bx1 - bx0) / 2 + 30, 120, ar[1], S.t, ar[2] if len(ar) > 2 else "#F43F5E", aa)
        elif kind == "down" and info:
            px, py = info["pilot"]
            for k in range(3):
                ph = ((S.t * 1.4 + k / 3) % 1.0)
                yy = py + 80 + ph * 240
                line_arrow(c, px - 200, yy - 70, px - 200, yy, color="#22D3EE", width=8, alpha=aa * (1 - ph), head=22)
                line_arrow(c, px + 200, yy - 70, px + 200, yy, color="#22D3EE", width=8, alpha=aa * (1 - ph), head=22)
        elif kind == "weight" and info:
            px, py = info["pilot"]
            d = ar[1]
            line_arrow(c, px - d * 30, py + 95, px + d * 170, py + 95, color="#FFD23F", width=12, alpha=aa, head=34, glow=True)
            draw_text(c, "AĞIRLIK", px + d * 290, py + 106, 34, "#FFD23F", "black", "center", aa, shadow=(0, 3, 0.5, 6))
        elif kind == "air" and info:
            for k in range(7):
                sv = -0.8 + k * 0.27
                tx, ty = info["surf"]("le", sv)
                ph = (S.t * 1.3 + k * 0.17) % 1.0
                sxx, syy = tx + (0 - 0) * 0, ty + 260 * (1 - ph)
                line_arrow(c, tx, ty + 260 - ph * 200, tx, ty + 200 - ph * 200 + 40, color="#22D3EE", width=7, alpha=aa * (1 - ph) * 0.9, head=18)
        elif kind == "pump" and info:
            px, py = info["pilot"]
            side = ar[1]
            hx = px + side * 95
            k = 0.5 - 0.5 * math.cos(S.pts * 2 * math.pi / 1.6)
            line_arrow(c, hx, py - 60, hx, py - 60 + 90 * k + 10, color="#FFD23F", width=10, alpha=aa, head=26)
            draw_text(c, "POMPA", hx, py - 90, 30, "#FFD23F", "black", "center", aa)
    draw_callouts(c, S, info, S.get("callouts"))
    # göstergeler
    widgets = S.get("widgets", [])
    wy = 1250
    wa = ease_out(remap(S.t, 0.3, 0.8))
    xs = {1: [415], 2: [265, 565], 3: [125, 415, 705]}.get(len(widgets), [125, 415, 705])
    for name, wx in zip(widgets, xs):
        if name == "vario":
            world.vario(c, wx + 125, wy + 60, S.v("vario", -1.1, dur=1.2), t, wa, scale=0.85)
        elif name == "speed":
            widget_speed(c, wx, wy, S.v("kmh", 37, dur=1.0), wa)
        elif name == "brake_l":
            widget_brake(c, wx, wy, kw["brake_l"], wa, label="SOL FREN")
        elif name == "brake_r":
            widget_brake(c, wx, wy, kw["brake_r"], wa, label="SAĞ FREN")
    legend = S.get("legend")
    if legend:
        la = ease_out(remap(S.pts, 0.2, 0.6))
        ws = [text_width(tx, 36, "black") + 64 for tx, _ in legend]
        x0 = 540 - (sum(ws) + 16 * (len(ws) - 1)) / 2
        for (tx, col), w_ in zip(legend, ws):
            chip(c, tx, x0 + w_ / 2, 1300, 36, col, "#0B1220", alpha=la, weight="black")
            x0 += w_ + 16
