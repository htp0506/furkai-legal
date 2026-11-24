"""Uçuş sahnesi: kamera kanadı takip eder; irtifa, hız, fren, yunuslama (pitch) ve iniş."""
import math
import skia
from ..core import scene
from ..gfx import (C, P, W, H, draw_text, text_width, glass, chip, rrect, lin, rad, clamp, lerp, ease_out, ease_in,
                   ease_io, smooth, remap, smooth_path, poly, arrow, pulse)
from .. import world, glider3d as g3


def widget_speed(c, x, y, kmh, alpha=1.0, label="HIZ"):
    glass(c, x, y, 250, 118, 30, alpha=0.6 * alpha, blur=0, border=0.14)
    draw_text(c, label, x + 26, y + 38, 22, "#94A3B8", "bold", "left", alpha, tracking=0.1)
    draw_text(c, f"{kmh:.0f}", x + 26, y + 98, 58, "white", "black", "left", alpha)
    draw_text(c, "km/sa", x + 26 + text_width(f"{kmh:.0f}", 58, "black") + 10, y + 96, 26, "#CBD5E1", "semi", "left", alpha)


def widget_brake(c, x, y, b, alpha=1.0, label="FREN"):
    glass(c, x, y, 250, 118, 30, alpha=0.6 * alpha, blur=0, border=0.14)
    draw_text(c, label, x + 26, y + 38, 22, "#94A3B8", "bold", "left", alpha, tracking=0.1)
    draw_text(c, f"%{b * 100:.0f}", x + 26, y + 98, 52, "white", "black", "left", alpha)
    # dikey çubuk
    bx, by, bh = x + 200, y + 22, 76
    rrect(c, bx, by, 22, bh, 11, P("#FFFFFF", 0.15 * alpha))
    col = "#22C55E" if b < 0.55 else ("#FFB020" if b < 0.85 else "#F43F5E")
    if b > 0.01:
        rrect(c, bx, by, 22, bh * clamp(b), 11, P(col, alpha))


def widget_alt(c, x, y, m, alpha=1.0):
    glass(c, x, y, 250, 118, 30, alpha=0.6 * alpha, blur=0, border=0.14)
    draw_text(c, "YÜKSEKLİK", x + 26, y + 38, 22, "#94A3B8", "bold", "left", alpha, tracking=0.1)
    s = f"{m:.1f}" if m < 10 else f"{m:.0f}"
    draw_text(c, s, x + 26, y + 98, 58, "white", "black", "left", alpha)
    draw_text(c, "m", x + 26 + text_width(s, 58, "black") + 10, y + 96, 26, "#CBD5E1", "semi", "left", alpha)


def _camx(S):
    """Dünya kayması: faz hızlarının integrali."""
    x = 0.0
    prev_sp = S.phases[0][2].get("speed", 260)
    acc = {}
    for i, (s, e, p) in enumerate(S.phases):
        acc.update(p)
        sp = acc.get("speed", 260)
        dur = (min(S.t, e) - s)
        if dur <= 0:
            break
        ramp = min(dur, 0.7)
        x += sp * dur - (sp - prev_sp) * ramp / 2
        prev_sp = sp
    return x


def _land_x(S):
    """Pilotun yere değdiği andaki dünya konumu (iniş hedefi oraya konur)."""
    acc = {}
    for i, (s0, e0, p) in enumerate(S.phases):
        acc.update(p)
        if acc.get("landed", 0) > 0:
            return _camx(S.at(s0 + 0.01))
    return _camx(S.at(S.T))


def _alt(S):
    return S.v("alt", 30.0, dur=S.pd * S.get("alt_k", 1.0), ease=S.get("alt_ease", None) and {"in": ease_in, "out": ease_out}.get(S.get("alt_ease"), ease_io) or ease_io)


@scene("flight")
def flight(c, S):
    t = S.gt
    zoom = S.v("zoom", 50, dur=1.0)
    gx = S.v("gx", 560, dur=0.9)
    gy = S.v("gy", 1010, dur=0.9)
    alt = _alt(S)
    camx = _camx(S)
    env = S.get("env", "field")
    theme = S.get("theme", "day")
    ground_y = gy + (1.35 + alt) * zoom
    # --- arka plan
    world.sky(c, theme, sun=(880, 330))
    world.clouds(c, t, 0, alpha=0.8, count=4, y_range=(260, 820), speed=6, camx=camx)
    mb = min(1500, max(ground_y - 30, 1100)) if env == "field" else 1500
    world.mountains(c, base_y=mb, camx=camx)
    if env == "field" and ground_y < H + 50:
        world.ground(c, ground_y, camx=camx)
        # ağaçlar (uzak sıra)
        for k in range(-2, 9):
            wx = k * 420 - (camx * 0.85) % 420
            world.tree(c, wx + 60, ground_y + 6, 0.9, alpha=0.9)
        # iniş alanı nesneleri
        tx = S.get("target_x", None)
        if tx == "land":
            tx = _land_x(S)
        if tx is not None:
            sx = gx + (tx - camx)
            world.target(c, sx, ground_y + 55, 170, 34, pulse_t=t)
        sock_x = S.get("sock_x", None)
        if sock_x == "land":
            sock_x = _land_x(S) + 520
        if sock_x is not None:
            sx = gx + (sock_x - camx)
            world.windsock(c, sx, ground_y + 20, 0.75, strength=S.get("wind", 0.55), t=t, direction=-1, pole=230)
        # gölge
        sh_a = clamp(1 - alt / 25) * 0.35
        if sh_a > 0:
            c.drawOval(skia.Rect.MakeXYWH(gx - 120 - alt * 3, ground_y + 6, 240 + alt * 6, 26), P("#000000", sh_a, blur=8))
    # rüzgar parçacıkları (karşıdan esen)
    if S.get("windfx", True):
        world.wind_particles(c, t, (0, 300, W, 1100), n=26, speed=-520, alpha=0.35, length=70, angle=math.pi)
    # --- iz çizgisi
    if S.get("trail", True):
        pts = []
        for k in range(22):
            tau = S.t - k * 0.16
            if tau < 0:
                break
            st = S.at(tau)
            dx = camx - _camx(st)
            da = _alt(st) - alt
            pts.append((gx - dx, gy - da * zoom + 0.0 * zoom))
        if len(pts) > 2:
            path = smooth_path(pts[::-1])
            c.drawPath(path, P("#FFB020", 0.9, stroke=6, dash=(22, 16)))
    # --- kanat
    pitch = S.v("pitch", 0.0, dur=S.get("pitch_dur", 0.8))
    osc = S.get("osc", 0.0)
    if osc:
        pitch += osc * math.sin(S.pts * 2.2) * math.exp(-S.pts * 0.6)
    brake = S.v("brake", 0.0, dur=S.get("brake_dur", 0.6), ease=ease_io)
    if S.get("brake_ramp"):
        b0, b1, r0, r1 = S.get("brake_ramp")
        brake = lerp(b0, b1, smooth(remap(S.pts, r0, r1)))
    stand = S.v("stand", 0.0, dur=0.8)
    landed = S.v("landed", 0.0, dur=1.1)
    run = S.get("run", 0.0)
    bob = math.sin(t * 1.6) * 6 * (1 - landed)
    yaw = S.v("yaw", g3.SIDE_34, dur=1.0)
    elev = S.v("elev", 0.2, dur=1.0)
    lk = ease_in(landed) if landed < 1 else 1.0
    g3.render(c, gx, gy + bob, zoom, yaw=yaw, elev=elev, pitch=pitch * (1 - lk) - lk * 1.85, roll=math.sin(t * 0.9) * 0.02 * (1 - lk),
              brake_l=brake, brake_r=brake, pose=stand, run=run, t=t, anchor="pilot",
              stall=lk * 0.5, crumple=lk * 0.35 + S.get("crumple", 0.0), front=S.v("front", 0.0, dur=0.5),
              inflate=1 - lk * 0.75, flat=lk * 0.55)
    # --- yunuslama yayı (dalış göstergesi)
    if S.get("show_pitch"):
        ax, ay = gx, gy
        r = 7.2 * zoom
        a0, a1 = -90, -90 + math.degrees(pitch)
        if abs(a1 - a0) > 2:
            path = skia.Path()
            path.addArc(skia.Rect.MakeXYWH(ax - r, ay - r, 2 * r, 2 * r), a0, a1 - a0)
            col = "#F43F5E" if pitch > 0.12 else "#FFD23F"
            c.drawPath(path, P(col, 0.9, stroke=7))
            c.drawLine(ax, ay, ax, ay - r, P("#FFFFFF", 0.45, stroke=3, dash=(14, 10)))
    # --- göstergeler
    wa = ease_out(remap(S.t, 0.3, 0.8))
    widgets = S.get("widgets", [])
    wy = 1260
    xs = {1: [415], 2: [265, 565], 3: [125, 415, 705]}.get(len(widgets), [125, 415, 705])
    for wname, wx in zip(widgets, xs):
        if wname == "speed":
            widget_speed(c, wx, wy, S.v("kmh", 37, dur=0.8), wa)
        elif wname == "brake":
            widget_brake(c, wx, wy, brake, wa)
        elif wname == "alt":
            widget_alt(c, wx, wy, max(0.0, alt), wa)
