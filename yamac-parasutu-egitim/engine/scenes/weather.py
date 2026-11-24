"""Meteoroloji sahneleri: rüzgar tulumu, yamaç kaldırması, rotor, termik, fırtına bulutu."""
import math
import numpy as np
import skia
from ..core import scene
from ..gfx import (C, P, W, H, draw_text, text_width, glass, chip, rrect, lin, rad, clamp, lerp, ease_out, ease_in,
                   ease_io, ease_back, smooth, remap, smooth_path, poly, arrow, line_arrow, pulse, circle, mix, icon_check, icon_cross)
from .. import world, glider3d as g3


# ---------------------------------------------------------------- rüzgar tulumu
@scene("sock")
def sock(c, S):
    t = S.gt
    strength = S.v("strength", 0.5, dur=1.0)
    gusty = S.v("gusty", 0.0, dur=0.6)
    world.sky(c, S.get("theme", "day"))
    world.clouds(c, t, 0, alpha=0.8, count=4, y_range=(300, 820), speed=10 + 60 * strength)
    world.mountains(c, base_y=1150, camx=t * 10)
    gy = 1190
    world.ground(c, gy, camx=0)
    world.wind_particles(c, t, (0, 500, W, 640), n=int(10 + 40 * strength), speed=120 + 900 * strength, alpha=0.25 + 0.45 * strength,
                         length=30 + 90 * strength, wobble=60 * gusty)
    world.windsock(c, S.get("sx", 600), gy + 10, 1.6, strength=strength, t=t, direction=1, gusty=gusty)
    if S.get("show_glider"):
        a = ease_out(remap(S.t, 0.0, 0.6))
        g3.render(c, 230, gy - 70, 26, yaw=math.pi / 2 + 0.5, elev=0.15, anchor="pilot", pose=1.0, t=t, alpha=a)
        line_arrow(c, 120, gy - 330, 360, gy - 330, color="#FFD23F", width=10, alpha=a, head=30)
        draw_text(c, "RÜZGAR", 240, gy - 360, 30, "#FFD23F", "black", "center", a)
    # şiddet göstergesi
    if S.get("meter", True):
        y = 1320
        x0, x1 = 120, 960
        a = ease_out(remap(S.t, 0.2, 0.7))
        glass(c, 70, y - 95, 940, 190, 40, alpha=0.6 * a, blur=0, border=0.14)
        segs = [(0.0, 0.3, "#94A3B8", "SARKIK"), (0.3, 0.72, "#22C55E", "İDEAL"), (0.72, 1.0, "#F43F5E", "GÜÇLÜ")]
        for s0, s1, col, name in segs:
            rrect(c, lerp(x0, x1, s0) + 4, y - 10, (s1 - s0) * (x1 - x0) - 8, 20, 10, P(col, 0.9 * a))
            draw_text(c, name, lerp(x0, x1, (s0 + s1) / 2), y + 60, 30, col, "black", "center", a, tracking=0.05)
        draw_text(c, "RÜZGAR ŞİDDETİ", 540, y - 40, 24, "#CBD5E1", "black", "center", a, tracking=0.12)
        nx = lerp(x0, x1, clamp(strength + gusty * 0.12 * math.sin(t * 6)))
        c.drawCircle(nx, y, 20, P("white", a))
        c.drawCircle(nx, y, 20, P("#0B1220", a, stroke=4))


# ---------------------------------------------------------------- yamaç kesiti
def _hill(x):
    base, peak_x, peak_y = 1430, 640, 800
    if x <= peak_x:
        u = clamp((x + 150) / (peak_x + 150))
        return base - (base - peak_y) * smooth(u) ** 1.3
    u = clamp((1250 - x) / (1250 - peak_x))
    return base - (base - peak_y) * smooth(u) ** 0.8


@scene("ridge")
def ridge(c, S):
    t = S.gt
    wind = S.v("wind", 0.6, dur=1.0)
    world.sky(c, S.get("theme", "day"))
    world.clouds(c, t, 0, alpha=0.7, count=3, y_range=(280, 560), speed=20 + 40 * wind)
    base = 1430
    hx = np.linspace(-160, 1240, 90)
    hy = [_hill(x) for x in hx]
    hill_pts = list(zip(hx, hy))
    world.draw_hill(c, hill_pts, base + 200, "#5FAE63", "#2F6B3C")
    c.drawRect(skia.Rect.MakeXYWH(0, base + 150, W, H), P("#2F6B3C"))
    # akış çizgileri
    peak = 640
    lines = []
    for hk in (40, 110, 200, 310, 440, 590):
        pts = []
        for x in np.linspace(-60, 1140, 64):
            terr = base - _hill(x)
            if x > peak:
                sep = (base - _hill(peak)) * math.exp(-(x - peak) / (380 + 300 * (1 - wind)))
                terr = max(terr, sep * 0.95)
            decay = math.exp(-hk / 650)
            pts.append((x, base - 40 - hk - terr * (0.35 + 0.65 * decay)))
        lines.append(smooth_path(pts))
    world.flow_lines(c, lines, t, "#FFFFFF", 0.8, width=4, speed=0.15 + 0.35 * wind, dash=0.06, gap=0.05)
    # kaldırma bandı
    ba = S.v("band", 0.0, dur=0.8)
    if ba > 0:
        band = skia.Path()
        top_pts = [(x, _hill(x) - 330) for x in np.linspace(260, 700, 20)]
        bot_pts = [(x, _hill(x) - 60) for x in np.linspace(700, 260, 20)]
        band = smooth_path(top_pts + bot_pts + [top_pts[0]], close=False)
        c.drawPath(band, P("#22C55E", 0.28 * ba * (0.8 + 0.2 * pulse(t, 1.4)), blur=12))
        c.drawPath(band, P("#86EFAC", 0.8 * ba, stroke=4, dash=(16, 12)))
        draw_text(c, "KALDIRMA BANDI", 400, _hill(400) - 370, 36, "#BBF7D0", "black", "center", ba, shadow=(0, 3, 0.5, 6))
        for k in range(4):
            ph = (S.t * 0.8 + k / 4) % 1
            xx = 330 + k * 95
            yy = _hill(xx) - 80 - ph * 220
            line_arrow(c, xx, yy, xx + 25, yy - 70, color="#34D399", width=8, alpha=ba * math.sin(ph * math.pi), head=20)
    # rotor
    ra = S.v("rotor", 0.0, dur=0.8)
    if ra > 0:
        for k, (rx, ry, rr) in enumerate([(820, 1170, 90), (950, 1270, 70), (760, 1030, 60)]):
            world.swirl(c, rx, ry, rr * (0.7 + 0.6 * wind), t + k, "#F43F5E", 0.85 * ra, turns=1.4, width=6)
        draw_text(c, "ROTOR", 900, 1000, 44, "#FECDD3", "black", "center", ra, shadow=(0, 3, 0.5, 6))
    # rüzgar oku
    a = ease_out(remap(S.t, 0.0, 0.5))
    line_arrow(c, 30, 1020, 220, 1020, color="#FFD23F", width=12, alpha=a, head=34)
    draw_text(c, "RÜZGAR", 40, 985, 32, "#FFD23F", "black", "left", a)
    # kanat
    drift = S.v("drift", 0.0, dur=S.pd * 0.9)
    gx = lerp(470, 980, drift) + math.sin(t * 0.7) * 25 * (1 - drift)
    gy = lerp(_hill(470) - 210, 1080, drift ** 1.5) + math.sin(t * 1.1) * 10
    if S.get("glider", True):
        shake = smooth(remap(drift, 0.6, 1.0))
        g3.render(c, gx + math.sin(t * 12) * 6 * shake, gy, 18, yaw=math.pi - 0.45 + 0.3 * math.sin(t * 0.35), elev=0.15,
                  roll=math.sin(t * 9) * 0.12 * shake, crumple=0.3 * shake, fold_l=0.6 * shake * (0.5 + 0.5 * math.sin(t * 3)),
                  anchor="center", t=t)


@scene("ridge_top")
def ridge_top(c, S):
    """Üstten görünüm: yamaç boyunca 8 çizerek uçuş, dönüşler yamaçtan dışarı."""
    t = S.gt
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=lin((0, 0), (0, H), [C("#3E7D4B"), C("#6FBF73"), C("#A7D9A1")], [0, 0.5, 1])))
    # eş yükselti eğrileri (yamaç sırtı üstte)
    for k in range(9):
        y = 520 + k * 85
        pts = [(x, y + 40 * math.sin(x / 170 + k * 0.6)) for x in np.linspace(-20, W + 20, 30)]
        c.drawPath(smooth_path(pts), P("#FFFFFF", 0.12 + 0.02 * k, stroke=3))
    ridge_y = 520
    c.drawPath(smooth_path([(x, ridge_y + 40 * math.sin(x / 170)) for x in np.linspace(-20, W + 20, 30)]), P("#1F3B26", 0.9, stroke=10))
    draw_text(c, "SIRT", 900, ridge_y - 30, 34, "white", "black", "center")
    draw_text(c, "YAMAÇ", 170, 1010, 34, "#E2E8F0", "black", "center", 0.9)
    # rüzgar (aşağıdan yukarı)
    for k in range(6):
        ph = (S.t * 0.6 + k / 6) % 1
        xx = 120 + k * 170
        yy = 1700 - ph * 400
        line_arrow(c, xx, yy, xx, yy - 80, color="#FFD23F", width=8, alpha=0.8 * math.sin(ph * math.pi), head=22)
    draw_text(c, "RÜZGAR ↑", 140, 1640, 34, "#FFD23F", "black", "left")
    # 8 çizen rota: yamaca paralel bacaklar, uçlarda yamaçtan dışarı (aşağı) dönüş
    y1, y2 = 720, 900
    path_pts = []
    N = 200
    for i in range(N + 1):
        u = i / N * 2 * math.pi
        x = 540 + 380 * math.sin(u)
        y = (y1 + y2) / 2 + (y2 - y1) / 2 * math.sin(2 * u) * (-1)
        path_pts.append((x, y))
    path = smooth_path(path_pts)
    a = ease_out(remap(S.t, 0.2, 0.8))
    c.drawPath(path, P("#FFFFFF", 0.7 * a, stroke=5, dash=(18, 14)))
    # kanat konumu
    k = (S.t * 0.09) % 1.0
    i = int(k * N)
    x, y = path_pts[i]
    x2, y2_ = path_pts[(i + 2) % (N + 1)]
    hd = math.atan2(-(x2 - x), (y2_ - y))
    g3.render(c, x, y, 21, yaw=0.0, elev=math.pi / 2, heading=hd, anchor="pilot", t=t, lines=False)
    # dönüş yönü vurgusu
    if S.get("show_turns", True):
        aa = ease_out(remap(S.t, 0.6, 1.2))
        for sx in (-1, 1):
            cx = 540 + sx * 395
            c.drawCircle(cx, (y1 + y2) / 2, 95, P("#22C55E", 0.25 * aa))
            c.drawCircle(cx, (y1 + y2) / 2, 95, P("#22C55E", 0.9 * aa, stroke=5))
        draw_text(c, "DIŞARI DÖN", 540, 1060, 44, "#BBF7D0", "black", "center", aa, shadow=(0, 3, 0.5, 6))
        icon_check(c, 540, 1140, 34, "green", aa)


# ---------------------------------------------------------------- engeller & rotor
@scene("obstacles")
def obstacles(c, S):
    t = S.gt
    world.studio_bg(c, "#F43F5E", S.t)
    shown = S.get("shown", 3)
    rows = [("DAĞ", "mountain"), ("AĞAÇ SIRASI", "trees"), ("BİNALAR", "buildings")]
    for i, (name, kind) in enumerate(rows):
        if i >= shown:
            break
        appear = 0.15 + i * S.get("stagger", 0.3)
        a = ease_out(remap(S.t, appear, appear + 0.5))
        y0 = 540 + i * 295
        glass(c, 60, y0, 960, 270, 36, alpha=0.4 * a, blur=0, border=0.12)
        gy = y0 + 225
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(60, y0, 960, 270))
        c.drawRect(skia.Rect.MakeXYWH(60, gy, 960, 60), P("#2F6B3C", a))
        ox = 430
        if kind == "mountain":
            pts = [(ox - 220, gy), (ox, gy - 200), (ox + 160, gy)]
            c.drawPath(smooth_path(pts + [pts[0]], tension=0.2), P("#4B7F52", a))
            c.drawPath(poly(pts), P("#4B7F52", a))
        elif kind == "trees":
            for k in range(5):
                world.tree(c, ox - 120 + k * 60, gy, 1.2, alpha=a)
        else:
            for k, hh in enumerate((150, 210, 120)):
                rrect(c, ox - 110 + k * 75, gy - hh, 66, hh, 6, P("#64748B", a))
                for wy in range(int(gy - hh + 20), int(gy - 15), 34):
                    c.drawRect(skia.Rect.MakeXYWH(ox - 98 + k * 75, wy, 16, 14), P("#FDE68A", 0.7 * a))
        # akış ve girdap
        for k in range(3):
            yy = gy - 230 + k * 45
            pts = [(70, yy), (ox - 160, yy), (ox, yy - 40), (ox + 200, yy - 10), (1010, yy)]
            world.flow_lines(c, [smooth_path(pts)], t + k * 0.3, "#FFFFFF", 0.6 * a, width=3, speed=0.4, dash=0.08, gap=0.06, glow=False)
        world.swirl(c, ox + 250, gy - 70, 60, t + i, "#F43F5E", 0.9 * a, turns=1.4, width=5)
        world.swirl(c, ox + 380, gy - 50, 40, t + i + 1, "#F43F5E", 0.6 * a, turns=1.2, width=4)
        c.restore()
        draw_text(c, name, 100, y0 + 60, 38, "white", "black", "left", a)
        line_arrow(c, 820, y0 + 45, 960, y0 + 45, color="#FFD23F", width=7, alpha=a, head=20)


# ---------------------------------------------------------------- termik
@scene("thermal")
def thermal(c, S):
    t = S.gt
    world.sky(c, S.get("theme", "bright"), sun=(900, 260))
    gy = 1290
    world.mountains(c, base_y=gy - 20, camx=0)
    # zemin yamaları
    patches = [(-20, 230, "#C9A227", "TARLA"), (230, 420, "#9CA3AF", "KAYA"), (420, 700, "#374151", "ASFALT"),
               (700, 900, "#2E7D4F", "ORMAN"), (900, 1100, "#3B82F6", "GÖL")]
    heat = S.v("heat", 0.0, dur=1.0)
    for x0, x1, col, name in patches:
        c.drawRect(skia.Rect.MakeXYWH(x0, gy, x1 - x0, H - gy), P(col))
        c.drawRect(skia.Rect.MakeXYWH(x0, gy, x1 - x0, H - gy), skia.Paint(Shader=lin((0, gy), (0, H), [C("#FFFFFF", 0.12), C("#000000", 0.35)])))
        if S.get("labels", True):
            draw_text(c, name, (x0 + x1) / 2, gy + 62, 30, "white", "black", "center", 0.95)
    # güneş ışınları
    if heat > 0:
        for k in range(5):
            ph = (S.t * 0.5 + k / 5) % 1
            sx, sy = 900, 260
            tx, ty = 200 + k * 180, gy
            line_arrow(c, lerp(sx, tx, ph * 0.8), lerp(sy, ty, ph * 0.8), lerp(sx, tx, ph * 0.8 + 0.12), lerp(sy, ty, ph * 0.8 + 0.12),
                       color="#FDE68A", width=6, alpha=heat * math.sin(ph * math.pi) * 0.8, head=18)
        # ısınma pırıltısı
        for k in range(6):
            xx = 450 + k * 45
            pts = [(xx + 10 * math.sin(t * 4 + j + k), gy - 10 - j * 22) for j in range(6)]
            c.drawPath(smooth_path(pts), P("#FDBA74", 0.6 * heat, stroke=3))
    # termik sütunu
    col_a = S.v("column", 0.0, dur=1.0)
    if col_a > 0:
        path = skia.Path()
        path.moveTo(470, gy)
        path.cubicTo(420, 1100, 520, 800, 430, 470)
        path.lineTo(700, 470)
        path.cubicTo(640, 800, 720, 1100, 650, gy)
        path.close()
        c.drawPath(path, skia.Paint(AntiAlias=True, Shader=lin((0, 470), (0, gy), [C("#FB923C", 0.08 * col_a), C("#FB923C", 0.32 * col_a)])))
        for k in range(5):
            ph = (S.t * 0.5 + k / 5) % 1
            yy = lerp(gy - 60, 520, ph)
            line_arrow(c, 560 + 40 * math.sin(k), yy, 560 + 40 * math.sin(k), yy - 60, color="#FDBA74", width=7, alpha=col_a * math.sin(ph * math.pi), head=18)
    # baloncuk
    bub = S.v("bubble", 0.0, dur=S.pd)
    if 0 < bub < 1.0 and S.get("show_bubble", True):
        by = lerp(gy - 60, 600, ease_in(bub))
        world.bubble(c, 560, by, 60 + 90 * bub, t, "#FB923C", 0.7)
    # bulut
    cg = S.v("cloud", 0.0, dur=1.6)
    world.cumulus(c, 570, 470, 420, growth=cg, t=t)
    # kanat(lar) daire çiziyor
    circ = S.v("circle", 0.0, dur=0.8)
    if circ > 0:
        climb = S.get("climb_from", 1060)
        cy = climb - (S.t - S.start(S.get("circle_phase", 0))) * S.get("climb_rate", 38)
        cy = max(cy, 620)
        R = 190
        for gi, (off, lag) in enumerate([(0.0, 0.0)] + ([(math.pi, 260)] if S.get("second") else [])):
            if gi == 1:
                a2 = ease_out(remap(S.pts, 0.3, 0.9)) if S.ph >= S.get("second_phase", 99) else 0
                if a2 <= 0:
                    continue
            th = S.t * 1.1 + off
            x = 570 + R * math.cos(th)
            y = cy + lag + 40 * math.sin(th)
            sc = 15 + 4 * math.sin(th)
            hd = th + math.pi / 2
            g3.render(c, x, y, sc, yaw=g3.SIDE, elev=0.25, heading=hd, roll=-0.45, anchor="center", t=t,
                      alpha=circ if gi == 0 else a2)
        if S.get("vario_widget", True):
            world.vario(c, 860, 1150, S.v("vario", 2.4, dur=1.0), t, circ, scale=0.85)


# ---------------------------------------------------------------- fırtına bulutu
@scene("storm")
def storm(c, S):
    t = S.gt
    dark = S.v("dark", 0.0, dur=1.2)
    # gökyüzü karışımı
    world.sky(c, "day", sun_alpha=round(1 - dark, 1))
    if dark > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=lin((0, 0), (0, H), [C("#111827", 0.85 * dark), C("#4B5563", 0.7 * dark)])))
    gy = 1460
    world.mountains(c, base_y=gy, camx=0, layers=[(11, 260, mix("#8DB6E8", "#4B5563", dark), mix("#B9D7F3", "#6B7280", dark), 0.1),
                                                   (37, 200, mix("#3F6E8C", "#1F2937", dark), mix("#5B8AA6", "#374151", dark), 0.4)])
    world.ground(c, gy, camx=0, color_top=mix("#6CC46A", "#2F4F3A", dark), color_bot=mix("#2F7D43", "#1A2E22", dark))
    growth = S.v("growth", 0.6, dur=1.5)
    tall = S.v("tall", 0.0, dur=2.0)
    anvil = S.v("anvil", 0.0, dur=1.6)
    base_y = 1190
    rain = S.v("rain", 0.0)
    if rain > 0:
        world.rain(c, (300, base_y, 480, gy - base_y), t, alpha=0.55 * rain, n=90)
    world.cumulus(c, 540, base_y, 470, growth=growth, dark=0.2 + 0.45 * tall, tall=tall, anvil=anvil, t=t)
    if S.get("lightning"):
        world.lightning(c, 520, base_y + 10, gy - base_y - 20, t)
    suck = S.v("suck", 0.0)
    if suck > 0:
        for k in range(6):
            ph = (S.t * 0.9 + k / 6) % 1
            xx = 380 + k * 65
            yy = lerp(base_y + 250, base_y + 30, ph)
            line_arrow(c, xx, yy, xx, yy - 70, color="#F43F5E", width=8, alpha=suck * math.sin(ph * math.pi), head=22)
        gxp = 700 - 120 * suck
        gyp = base_y + 190 - 110 * suck * smooth(remap(S.pts, 0, S.pd))
        g3.render(c, gxp, gyp, 12, yaw=g3.SIDE_34, elev=0.2, anchor="center", t=t, roll=math.sin(t * 8) * 0.1)
    gust = S.v("gust", 0.0)
    if gust > 0:
        for sx in (-1, 1):
            for k in range(4):
                ph = (S.t * 0.8 + k / 4) % 1
                x0 = 540 + sx * (120 + ph * 420)
                line_arrow(c, x0, gy - 30 - k * 18, x0 + sx * 120, gy - 30 - k * 18, color="#FBBF24", width=9,
                           alpha=gust * math.sin(ph * math.pi), head=24)
        draw_text(c, "ANİ RÜZGAR CEPHESİ", 540, gy + 90, 34, "#FDE68A", "black", "center", gust)
    if S.get("land_glider"):
        a = ease_out(remap(S.pts, 0, 0.5))
        k = smooth(remap(S.pts, 0, S.pd))
        g3.render(c, lerp(880, 960, k), lerp(1150, gy - 60, k), 14, yaw=g3.SIDE_34, elev=0.2, anchor="pilot", t=t, alpha=a,
                  brake_l=k, brake_r=k, pose=k)
