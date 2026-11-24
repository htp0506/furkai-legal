"""Diyagram sahneleri: kanat kesiti (airfoil), hız aralığı, süzülme oranı."""
import math
import numpy as np
import skia
from ..core import scene
from ..gfx import (C, P, W, H, draw_text, text_width, glass, chip, rrect, lin, rad, clamp, lerp, ease_out, ease_in,
                   ease_io, ease_back, smooth, remap, smooth_path, poly, arrow, line_arrow, pulse, angle_arc, circle)
from .. import world, glider3d as g3
from ..glider3d import _airfoil
from .flight import widget_brake, widget_speed


def _airfoil_pts(cx, cy, L, aoa_deg, lefold=0.0, brake=0.0, n=60):
    u = (1 - np.cos(np.linspace(0, np.pi, n))) / 2
    up, lo = _airfoil(u, t=0.17, m=0.05)
    # firar kenarı fren bükümü
    defl = brake * np.clip((u - 0.6) / 0.4, 0, 1) ** 2 * 0.18
    up, lo = up - defl, lo - defl
    xs = np.concatenate([u, u[::-1]])
    ys = np.concatenate([up, lo[::-1]])
    dx = (xs - 0.25) * L
    dy = -ys * L
    if lefold > 0:
        uf = 0.36
        fx, fy = (uf - 0.25) * L, -np.interp(uf, u, lo) * L
        g = -math.radians(166) * lefold
        mask = xs < uf
        rx, ry = dx - fx, dy - fy
        cg, sg = math.cos(g), math.sin(g)
        dx = np.where(mask, fx + rx * cg - ry * sg, dx)
        dy = np.where(mask, fy + rx * sg + ry * cg, dy)
    a = math.radians(aoa_deg)
    X = cx + dx * math.cos(a) - dy * math.sin(a)
    Y = cy + dx * math.sin(a) + dy * math.cos(a)
    return X, Y, n


@scene("airfoil")
def airfoil(c, S):
    t = S.gt
    world.studio_bg(c, S.get("accent", "#22D3EE"), S.t)
    cx, cy, L = S.get("cx", 400), S.v("cy", 1010), S.get("chord", 560)
    aoa = S.v("aoa", 8.0, dur=1.0)
    stall = S.v("stall", 0.0, dur=0.8)
    lefold = S.v("lefold", 0.0, dur=0.6)
    brake = S.v("brake", 0.0, dur=0.8)
    flow_speed = S.v("flow", 1.0)
    X, Y, n = _airfoil_pts(cx, cy, L, aoa, lefold, brake)
    X0, Y0, _ = _airfoil_pts(cx, cy, L, aoa, 0.0, brake)
    # not: ekran koordinatında burun yukarı = negatif dönüş (y aşağı)
    le = (X[0], Y[0])
    te = (X[n - 1], Y[n - 1])
    # --- akış çizgileri
    if S.get("show_flow", True):
        lines = []
        xs = np.linspace(40, 1040, 70)
        up_env = np.interp(xs, X[:n], Y[:n], left=np.nan, right=np.nan)
        lo_x, lo_y = X0[n:][::-1], Y0[n:][::-1]
        order = np.argsort(lo_x)
        lo_env = np.interp(xs, lo_x[order], lo_y[order])
        order_u = np.argsort(X0[:n])
        up_env = np.interp(xs, X0[:n][order_u], Y0[:n][order_u])
        span_lo, span_hi = min(X0), max(X0)
        for d in (-300, -200, -125, 110, 200, 300):
            A = math.exp(-abs(d) / 260)
            ys = []
            for i, x in enumerate(xs):
                base = cy + d
                inside = span_lo - 60 < x < span_hi + 40
                env = up_env[i] if d < 0 else lo_env[i]
                hump = cy - env
                # yumuşatılmış tümsek
                w = smooth(remap(x, span_lo - 160, span_lo + 40)) * (1 - smooth(remap(x, span_hi - 20, span_hi + 220)))
                down = aoa * 5.0 * A * smooth(remap(x, span_lo + 100, span_hi + 300)) * (1 - stall * 0.6 if d < 0 else 1)
                up_wash = -aoa * 2.5 * A * smooth(remap(x, span_lo - 260, span_lo)) * (1 - smooth(remap(x, span_lo, span_lo + 200)))
                y = base - hump * A * 1.35 * w + down * 1.3 + up_wash
                if stall > 0 and d < 0 and abs(d) < 200 and x > span_lo + L * 0.3:
                    # ayrılma: çizgi kanattan kopar, düz devam eder
                    y = lerp(y, ys[-1] if ys else y, stall)
                ys.append(y)
            lines.append(smooth_path(list(zip(xs, ys))))
        world.flow_lines(c, lines, t, "#7DD3FC", 0.55, width=5, speed=0.22 * flow_speed, dash=0.16, gap=0.05, glow=True)
    # --- basınç bölgeleri
    pa = ease_out(remap(S.t, 0.3, 0.9)) * S.get("show_pressure", 0)
    if pa > 0:
        mx = (le[0] + te[0]) / 2
        c.drawOval(skia.Rect.MakeXYWH(mx - 300, cy - 300, 520, 230), P("#3B82F6", 0.35 * pa * (1 - stall * 0.6), blur=40))
        c.drawOval(skia.Rect.MakeXYWH(mx - 260, cy + 40, 520, 200), P("#F97316", 0.32 * pa, blur=40))
        for k in range(3):
            draw_text(c, "−", mx - 180 + k * 150, cy - 160 + math.sin(t * 2 + k) * 8, 70, "#93C5FD", "black", "center", pa)
            draw_text(c, "+", mx - 160 + k * 150, cy + 170 + math.sin(t * 2 + k) * 8, 62, "#FDBA74", "black", "center", pa)
        draw_text(c, "ALÇAK BASINÇ", mx - 40, cy - 250, 30, "#93C5FD", "black", "center", pa, tracking=0.08)
        draw_text(c, "YÜKSEK BASINÇ", mx - 40, cy + 270, 30, "#FDBA74", "black", "center", pa, tracking=0.08)
    # --- kanat kesiti
    pts = list(zip(X, Y))
    path = poly(pts)
    if lefold > 0.02:
        # katlanan ön kısım ayrı (koyu) çizilir, arka gövde üstte
        Xr, Yr, nr = _airfoil_pts(cx, cy, L, aoa, 0.0, brake)
        uu = (1 - np.cos(np.linspace(0, np.pi, nr))) / 2
        keep = uu >= 0.36
        rear = list(zip(Xr[:nr][keep], Yr[:nr][keep])) + list(zip(Xr[nr:][::-1][keep][::-1], Yr[nr:][::-1][keep][::-1]))
        front_mask = uu <= 0.37
        fr_up = list(zip(X[:n][front_mask], Y[:n][front_mask]))
        fr_lo = list(zip(X[n:][::-1][front_mask], Y[n:][::-1][front_mask]))
        front = fr_up + fr_lo[::-1]
        c.drawPath(poly(front), P("#C2410C"))
        c.drawPath(poly(front), P("#FFFFFF", 0.7, stroke=3))
        path = poly(rear)
        pts = rear
    c.drawPath(path, P("#000000", 0.35, blur=18))
    c.drawPath(path, skia.Paint(AntiAlias=True, Shader=lin((cx, cy - 120), (cx, cy + 60), [C("#FF8A3D"), C("#E8590C")])))
    # iç kaburgalar (hücre)
    for k in (0.12, 0.3, 0.5, 0.7):
        i = int(k * (n - 1))
        c.drawLine(X[i], Y[i], X[2 * n - 1 - i], Y[2 * n - 1 - i], P("#FFFFFF", 0.25, stroke=3))
    c.drawPath(path, P("#FFFFFF", 0.9, stroke=4))
    # hücre ağzı
    if lefold < 0.3:
        mx_, my_ = X[2 * n - 4], Y[2 * n - 4]
        c.drawCircle(mx_, my_, 12, P("#0B1220", 0.9))
    if lefold > 0.3:
        world.swirl(c, X0[0] + 40, Y0[0] + 30, 50, t, "#F43F5E", 0.8 * lefold, turns=1.2, width=5)
        world.swirl(c, X0[0] + 150, Y0[0] - 60, 40, t + 1, "#F43F5E", 0.6 * lefold, turns=1.2, width=4)
    # --- türbülans (stol)
    if stall > 0.05:
        for k in range(4):
            u = 0.4 + k * 0.17
            i = int(u * (n - 1))
            world.swirl(c, X[i] + 20, Y[i] - 60 - k * 8, 42 + k * 8, t + k, "#F43F5E", 0.8 * stall, turns=1.2, width=5)
    # --- veter çizgisi ve hücum açısı
    if S.get("show_chord", 0):
        a = ease_out(remap(S.t, 0.2, 0.7))
        dxc, dyc = te[0] - le[0], te[1] - le[1]
        c.drawLine(le[0] - dxc * 0.35, le[1] - dyc * 0.35, te[0] + dxc * 0.2, te[1] + dyc * 0.2, P("#FFFFFF", 0.85 * a, stroke=4, dash=(18, 12)))
        draw_text(c, "VETER", te[0] + dxc * 0.12, te[1] + dyc * 0.12 + 50, 28, "#E2E8F0", "black", "center", a, tracking=0.1)
    if S.get("show_wind", 1):
        a = ease_out(remap(S.t, 0.1, 0.6))
        line_arrow(c, 70, le[1], le[0] - 30, le[1], color="#FFD23F", width=10, alpha=a, head=30)
        draw_text(c, "BAĞIL RÜZGAR", 90, le[1] - 30, 30, "#FFD23F", "black", "left", a, tracking=0.06)
    if S.get("show_aoa", 0):
        a = ease_out(remap(S.t, 0.3, 0.8))
        r = 230
        ang_chord = math.degrees(math.atan2(te[1] - le[1], te[0] - le[0]))
        a0, a1 = min(0, ang_chord), max(0, ang_chord)
        col = "#FFD23F" if aoa < 14 and stall < 0.3 else "#F43F5E"
        if aoa < 2.5:
            col = "#F43F5E"
        angle_arc(c, le[0], le[1], r, a0, a1, col, 7, a)
        c.drawLine(le[0], le[1], le[0] + r + 60, le[1], P("#FFD23F", 0.6 * a, stroke=3, dash=(12, 10)))
        chip(c, f"α = {aoa:.0f}°", le[0] + 20, le[1] + 150, 46, "#0B1220", col, alpha=a, weight="black", outline=col)
    # --- kaldırma oku
    if S.get("show_lift", 0):
        a = ease_out(remap(S.t, 0.4, 1.0))
        lift = (120 + 16 * min(aoa, 14)) * (1 - 0.65 * stall) * (1 - 0.7 * lefold)
        lx, ly = cx - 30, cy - 70
        line_arrow(c, lx, ly, lx, ly - lift * a - 10, color="#34D399", width=16, alpha=a, head=44, glow=True)
        draw_text(c, "KALDIRMA", lx + 40, ly - lift * a + 10, 40, "#34D399", "black", "left", a)


@scene("speedrange")
def speedrange(c, S):
    t = S.gt
    world.sky(c, "day")
    world.clouds(c, t, 0, alpha=0.7, count=4, y_range=(300, 900), speed=12, camx=t * 30)
    world.mountains(c, base_y=1700, camx=t * 30)
    kmh = S.v("kmh", 37, dur=1.0)
    brake = S.v("brake", 0.0, dur=1.0)
    bar = S.v("bar", 0.0, dur=0.8)
    pitch = S.v("pitch", 0.0, dur=0.8)
    g3.render(c, 560, 830, 60, yaw=g3.SIDE_34, elev=0.2, pitch=pitch + math.sin(t * 1.3) * 0.02, brake_l=brake, brake_r=brake,
              bar=bar, anchor="center", t=t, stall=S.v("stall", 0.0), crumple=S.v("crumple", 0.0))
    # hız skalası
    x0, x1, y = 90, 990, 1200
    vmin, vmax = 20, 55
    X = lambda v: x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)
    glass(c, 50, y - 120, 980, 230, 40, alpha=0.6, blur=0, border=0.14)
    zones = [(20, 25, "#F43F5E", "STOL"), (27, 32, "#FFB020", "MİN. BATIŞ"), (35, 40, "#22C55E", "TRİM"), (44, 53, "#3B82F6", "HIZLANDIRICI")]
    rrect(c, x0, y - 8, x1 - x0, 16, 8, P("#FFFFFF", 0.15))
    hz = S.get("zone")
    for a, b, col, name in zones:
        on = hz is None or hz == name
        rrect(c, X(a), y - 10, X(b) - X(a), 20, 10, P(col, 0.95 if on else 0.35))
        draw_text(c, name, (X(a) + X(b)) / 2, y + 62, 26, col if on else "#64748B", "black", "center", 1.0, tracking=0.05)
    for v in range(20, 56, 5):
        draw_text(c, str(v), X(v), y - 40, 24, "#94A3B8", "semi", "center")
    nx = X(clamp(kmh, vmin, vmax))
    c.drawPath(poly([(nx, y - 22), (nx - 18, y - 62), (nx + 18, y - 62)]), P("white"))
    c.drawLine(nx, y - 24, nx, y + 26, P("white", stroke=5))
    draw_text(c, f"{kmh:.0f} km/sa", nx, y - 76, 38, "white", "black", "center")
    widget_brake(c, 70, 1390 - 380 - 40, brake, ease_out(remap(S.t, 0.3, 0.8))) if S.get("show_brake", True) else None


@scene("glide_ratio")
def glide_ratio(c, S):
    t = S.gt
    world.sky(c, "bright")
    world.clouds(c, t, 0, alpha=0.6, count=3, y_range=(300, 700), speed=8)
    gy = 1180
    world.ground(c, gy, camx=0)
    ratio = S.get("ratio", 9)
    wind = S.v("wind", 0.0, dur=1.0)       # +: arka rüzgar, -: karşı rüzgar (km/s)
    x0, y0 = 120, 520
    dist_px = 640 * (1 + wind / 37.0)
    x1 = x0 + dist_px
    prog = ease_io(remap(S.t, 0.3, 2.6)) if not S.get("static") else 1.0
    # yükseklik ekseni
    c.drawLine(x0, y0, x0, gy, P("#FFFFFF", 0.9, stroke=5))
    draw_text(c, "1000 m", x0 + 20, (y0 + gy) / 2, 40, "white", "black", "left", 1.0, shadow=(0, 3, 0.4, 6))
    # süzülüş yolu
    path = skia.Path()
    path.moveTo(x0, y0)
    path.lineTo(x1, gy)
    c.drawPath(path, P("#FFFFFF", 0.25, stroke=5, dash=(16, 12)))
    seg, end = None, None
    arrow(c, path, "#FFB020", width=9, progress=prog, head=0)
    gx = lerp(x0, x1, prog)
    gyy = lerp(y0, gy, prog)
    g3.render(c, gx, gyy - 20, 16, yaw=g3.SIDE_34, elev=0.2, anchor="pilot", t=t, lines=False)
    # mesafe
    a = ease_out(remap(S.t, 2.0, 2.6)) if not S.get("static") else 1.0
    c.drawLine(x0, gy + 60, x1, gy + 60, P("#FFFFFF", a, stroke=4))
    for xx in (x0, x1):
        c.drawLine(xx, gy + 45, xx, gy + 75, P("#FFFFFF", a, stroke=4))
    km = ratio * (1 + wind / 37.0)
    draw_text(c, f"≈ {km:.0f} km", (x0 + x1) / 2, gy + 125, 56, "white", "black", "center", a, shadow=(0, 3, 0.4, 6))
    # oran etiketi
    chip(c, f"1 : {ratio}", 760, 600, 70, "orange", "white", alpha=ease_back(remap(S.t, 0.2, 0.7)), weight="black", pad=(36, 18))
    if abs(wind) > 1:
        aw = ease_out(remap(S.pts, 0.0, 0.5))
        txt = "KARŞI RÜZGAR" if wind < 0 else "ARKA RÜZGAR"
        col = "#F43F5E" if wind < 0 else "#22C55E"
        world.wind_particles(c, t, (0, 700, W, 400), n=30, speed=420 * (1 if wind > 0 else -1), alpha=0.6, length=80,
                             angle=0 if wind > 0 else math.pi)
        chip(c, txt, 760, 720, 40, col, "white", alpha=aw, weight="black")
