"""Kalkış, iniş pisti düzeni (üstten), hava trafik kuralları ve PLF sahneleri."""
import math
import numpy as np
import skia
from ..core import scene
from ..gfx import (C, P, W, H, draw_text, text_width, glass, chip, rrect, lin, rad, clamp, lerp, ease_out, ease_in,
                   ease_io, ease_back, smooth, remap, smooth_path, poly, arrow, line_arrow, pulse, circle, icon_check, icon_cross, trim_path)
from .. import world, glider3d as g3
from .stage import draw_callouts

G_BLUE = g3.Glider(colors={"main": "#22D3EE", "tip": "#0F172A", "center": "#F8FAFC", "stripe": "#FF6A1A"})
G_GREEN = g3.Glider(colors={"main": "#34D399", "tip": "#065F46", "center": "#F8FAFC", "stripe": "#FFD23F"})
G_VIOLET = g3.Glider(colors={"main": "#A78BFA", "tip": "#312E81", "center": "#F8FAFC", "stripe": "#22D3EE"})


# ---------------------------------------------------------------- kalkış
def _slope_y(x):
    return 1010 + (x + 60) * 0.42 + 30 * math.sin(x / 260)


@scene("launch")
def launch(c, S):
    t = S.gt
    world.sky(c, "day", sun=(880, 330))
    world.clouds(c, t, 0, alpha=0.8, count=4, y_range=(280, 700), speed=10)
    world.mountains(c, base_y=1180, camx=0)
    # yamaç
    xs = np.linspace(-60, 1140, 40)
    pts = [(x, _slope_y(x)) for x in xs]
    path = skia.Path()
    path.moveTo(-60, H)
    for p in pts:
        path.lineTo(*p)
    path.lineTo(1140, H)
    path.close()
    c.drawPath(path, skia.Paint(AntiAlias=True, Shader=lin((0, 1000), (0, H), [C("#7BC96F"), C("#2F7D43")])))
    c.drawPath(smooth_path(pts), P("#FFFFFF", 0.3, stroke=4))
    world.windsock(c, 980, _slope_y(980), 0.8, strength=S.get("wind", 0.55), t=t, direction=-1, pole=220)
    line_arrow(c, 1040, 760, 820, 760 + 0.42 * -220 * 0 - 40, color="#FFD23F", width=10, alpha=0.9, head=30)
    draw_text(c, "RÜZGAR", 930, 700, 30, "#FFD23F", "black", "center")
    # aşama: 0 serim, 1 şişirme, 2 tepede, 3 koşu, 4 kalkış ; abort: iptal
    st = S.v("stage", 0.0, dur=S.get("stage_dur", 1.4))
    abort = S.v("abort", 0.0, dur=1.0)
    reverse = S.get("reverse", False)
    turn = S.v("turn", math.pi if reverse else 0.0, dur=0.9)   # pilotun dönüklüğü (pi = kanada dönük)
    run_x = 360 + 330 * smooth(remap(st, 2.6, 4.0)) + 80 * smooth(remap(st, 3.6, 4.6))
    lift = 2.2 * smooth(remap(st, 3.5, 4.6))     # metre, yamaçtan yükseklik
    scale = 44
    px = run_x
    feet_y = _slope_y(px)
    py = feet_y - (1.32 + lift) * scale
    # kanat yunuslaması
    ground_pitch = -1.26
    pitch = lerp(ground_pitch, -0.35, smooth(remap(st, 0.3, 1.5)))
    pitch = lerp(pitch, 0.05, smooth(remap(st, 1.4, 2.2)))
    pitch = lerp(pitch, -1.5, abort)
    flat = lerp(0.65, 0.0, smooth(remap(st, 0.2, 1.3)))
    flat = lerp(flat, 0.5, abort)
    inflate = lerp(0.15, 1.0, smooth(remap(st, 0.2, 1.2)))
    inflate = lerp(inflate, 0.3, abort)
    running = clamp(remap(st, 2.4, 2.7)) * (1 - smooth(remap(st, 4.0, 4.4))) * (1 - abort)
    stand = 1.0 - smooth(remap(st, 4.0, 4.8))
    brake = 0.15 * smooth(remap(st, 3.6, 4.2)) + abort * 0.9
    lean = 0.25 * smooth(remap(st, 0.6, 1.2)) * (1 - smooth(remap(st, 2.0, 2.4)))
    info = g3.render(c, px, py, scale, yaw=g3.SIDE + 0.3, elev=0.12, pitch=pitch, anchor="pilot", t=t, pose=stand,
                     run=running, brake_l=brake, brake_r=brake, flat=flat, inflate=inflate, crumple=0.25 * (1 - inflate) + 0.2 * abort,
                     pilot_turn=turn, fold_l=S.v("tangle", 0.0) * 0.6, roll=-lean * 0.0)
    if S.get("look"):
        a = ease_out(remap(S.pts, 0.2, 0.6))
        c.drawLine(px + 10, py - 30, px + 70, py - 230, P("#FFD23F", a, stroke=5, dash=(14, 10)))
        draw_text(c, "👀", px + 90, py - 240, 60, "white", "bold", "center", a)
    if S.get("rise_arrow"):
        a = ease_out(remap(S.pts, 0.0, 0.5)) * (1 - smooth(remap(st, 1.6, 2.0)))
        path = skia.Path()
        path.addArc(skia.Rect.MakeXYWH(px - 330, py - 330, 660, 660), 200, 60)
        arrow(c, path, "#FFD23F", width=10, progress=ease_io(remap(S.pts, 0.2, 1.2)), alpha=a, head=30, glow=True)
    draw_callouts(c, S, info, S.get("callouts"))
    if abort > 0.3:
        icon_cross(c, 540, 1300, 60, "red", abort, progress=remap(S.pts, 0.3, 0.9))


# ---------------------------------------------------------------- iniş pisti (üstten)
MAP_K, MAP_CY, MAP_SRC = 0.6, 935, 1030


def _mp(x, y):
    """Harita koordinatını ekrana çevir (harita küçültülerek ortalanır)."""
    return (540 + (x - 540) * MAP_K, MAP_CY + (y - MAP_SRC) * MAP_K)


def _field(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=lin((0, 0), (W, H), [C("#4E8F4F"), C("#6DB36A"), C("#4C8A4A")])))
    for k in range(-8, 16):
        c.drawLine(k * 110, 0, k * 110 + 400, H, P("#FFFFFF", 0.03, stroke=40))
    c.save()
    c.translate(540, MAP_CY)
    c.scale(MAP_K, MAP_K)
    c.translate(-540, -MAP_SRC)
    # orman lekeleri
    for (x, y, r) in [(90, 420, 120), (980, 520, 140), (120, 1600, 160), (1000, 1700, 130), (60, 980, 90)]:
        c.drawCircle(x, y, r, P("#2E6B3A", 0.9))
        c.drawCircle(x - r * 0.3, y - r * 0.3, r * 0.5, P("#3E7D4B", 0.8))
    # yol
    c.drawPath(smooth_path([(-20, 1260), (300, 1230), (700, 1290), (1100, 1250)]), P("#CBD5E1", 0.7, stroke=26))
    # iniş alanı
    rrect(c, 330, 560, 420, 1000, 30, P("#8BD17C"))
    for k in range(7):
        c.drawRect(skia.Rect.MakeXYWH(330 + k * 60, 560, 30, 1000), P("#FFFFFF", 0.06))
    rrect(c, 330, 560, 420, 1000, 30, P("#FFFFFF", 0.5, stroke=4, dash=(20, 14)))
    world.target(c, 540, 760, 70, 70, pulse_t=t)
    c.restore()


PATTERN = {
    "eights": [(860, 520), (980, 600), (860, 680), (740, 600), (860, 520), (980, 440), (860, 360), (740, 440), (860, 520)],
    "downwind": [(860, 560), (880, 900), (880, 1300), (870, 1640)],
    "base": [(870, 1640), (720, 1700), (540, 1700)],
    "final": [(540, 1700), (540, 1300), (540, 790)],
}
LEG_LABEL = {"eights": ("8 ÇİZ", (880, 290)), "downwind": ("RÜZGARALTI BACAĞI", (880, 1100)),
             "base": ("BAZ", (700, 1770)), "final": ("FİNAL", (420, 1150))}


@scene("pattern")
def pattern(c, S):
    t = S.gt
    _field(c, t)
    # rüzgar (yukarıdan aşağı eser: kuzeyden)
    for k in range(5):
        ph = (S.t * 0.7 + k / 5) % 1
        xx = 120 + k * 210
        yy = 560 + ph * 260
        line_arrow(c, xx, yy, xx, yy + 70, color="#FFD23F", width=7, alpha=0.7 * math.sin(ph * math.pi), head=20)
    chip(c, "RÜZGAR ↓", 170, 620, 32, "yellow", "#1F1300", weight="black")
    # rüzgar tulumu sembolü (üstten): ok
    legs = S.get("legs", [])
    active = S.get("active")
    labels = []
    for name in legs:
        pts = [_mp(*p) for p in PATTERN[name]]
        path = smooth_path(pts, tension=0.6 if name == "eights" else 0.3)
        is_active = name == active
        prog = ease_io(remap(S.pts, 0.1, max(0.6, S.pd - 0.3))) if is_active else 1.0
        col = {"eights": "#FFD23F", "downwind": "#22D3EE", "base": "#A78BFA", "final": "#FF6A1A"}[name]
        arrow(c, path, col, width=9, progress=prog, alpha=1.0, head=28, glow=is_active)
        lab, (lx, ly) = LEG_LABEL[name]
        la = ease_out(remap(S.pts, 0.3, 0.8)) if is_active else 0.9
        labels.append((lab, _mp(lx, ly), col, la, name))
        if is_active:
            seg, end = trim_path(path, 0, max(0.01, prog))
            if end and end[0] is not None:
                ex, ey = end[0].x(), end[0].y()
                tx, ty = end[1].x(), end[1].y()
                hd = math.atan2(-tx, ty)
                g3.render(c, ex, ey, 13, yaw=0.0, elev=math.pi / 2, heading=hd, anchor="pilot", t=t, lines=False)
    for lab, (lx, ly), col, la, name in labels:
        chip(c, lab, lx, ly, 32, col, "#0B1220" if name in ("eights", "downwind") else "white", alpha=la, weight="black")
    if S.get("no_low_turn"):
        a = ease_out(remap(S.pts, 0.4, 0.9))
        x, y = _mp(540, 900)
        c.drawCircle(x, y, 90, P("#F43F5E", 0.18 * a))
        c.drawCircle(x, y, 90, P("#F43F5E", 0.9 * a, stroke=5, dash=(14, 10)))
        chip(c, "ALÇAKTA DÖNÜŞ YOK", x - 150, y + 130, 32, "red", "white", alpha=a, weight="black")


# ---------------------------------------------------------------- hava trafik kuralları (üstten)
def _top_glider(c, x, y, hd, g=None, scale=26, t=0.0, alpha=1.0, arrow_len=110):
    g3.render(c, x, y, scale, yaw=0.0, elev=math.pi / 2, heading=hd, anchor="pilot", t=t, lines=False, glider=g, alpha=alpha)
    if arrow_len:
        dx, dy = -math.sin(hd), math.cos(hd)
        line_arrow(c, x + dx * 50, y + dy * 50, x + dx * (50 + arrow_len), y + dy * (50 + arrow_len), color="#FFFFFF",
                   width=6, alpha=0.75 * alpha, head=20)


def _hd(dx, dy):
    return math.atan2(-dx, dy)


@scene("traffic")
def traffic(c, S):
    t = S.gt
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=lin((0, 0), (0, H), [C("#1E3A5F"), C("#2B5C8A"), C("#3A78B0")])))
    for k in range(0, H, 90):
        c.drawLine(0, k, W, k, P("#FFFFFF", 0.04, stroke=2))
    case = S.get("case", "headon")
    k = ease_io(remap(S.pts, 0.2, S.pd - 0.2))
    if case == "headon":
        y = 950
        ax = lerp(120, 980, k)
        bx = lerp(960, 100, k)
        off = 170 * smooth(remap(k, 0.25, 0.5))
        _top_glider(c, ax, y + off, _hd(1, 1.2 * (0.25 < k < 0.5)), t=t)
        _top_glider(c, bx, y - off, _hd(-1, -1.2 * (0.25 < k < 0.5)), G_BLUE, t=t)
        if S.get("arrows", True):
            a = ease_out(remap(S.pts, 0.1, 0.5))
            arrow(c, smooth_path([(300, 950), (470, 960), (620, 1120)]), "#34D399", width=8, progress=a, head=26)
            arrow(c, smooth_path([(780, 950), (610, 940), (460, 780)]), "#34D399", width=8, progress=a, head=26)
            chip(c, "SAĞA", 690, 1200, 36, "green", "white", alpha=a, weight="black")
            chip(c, "SAĞA", 390, 700, 36, "green", "white", alpha=a, weight="black")
    elif case == "ridge":
        ry = 620
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, ry), skia.Paint(Shader=lin((0, 0), (0, ry), [C("#2E5E3A"), C("#4E8F4F")])))
        c.drawLine(0, ry, W, ry, P("#1F3B26", stroke=10))
        draw_text(c, "YAMAÇ", 540, ry - 90, 40, "white", "black", "center")
        ax = lerp(1000, 80, k)
        _top_glider(c, ax, ry + 130, _hd(-1, 0), t=t)
        bx = lerp(80, 1000, k)
        off = 230 * smooth(remap(k, 0.2, 0.45))
        _top_glider(c, bx, ry + 130 + off, _hd(1, 1.5 * (0.2 < k < 0.45)), G_BLUE, t=t)
        a = ease_out(remap(S.pts, 0.2, 0.6))
        chip(c, "YOL VER ↓", 540, ry + 560, 32, "cyan", "#06222A", alpha=a, weight="black")
    elif case == "thermal":
        cx, cy, R = 540, 980, 230
        c.drawCircle(cx, cy, R + 90, skia.Paint(AntiAlias=True, Shader=rad((cx, cy), R + 90, [C("#FB923C", 0.35), C("#FB923C", 0.0)])))
        gl = [None, G_BLUE, G_GREEN]
        for i in range(3):
            th = S.t * 0.9 + i * 2 * math.pi / 3
            x, y = cx + R * math.cos(th), cy + R * math.sin(th)
            _top_glider(c, x, y, _hd(-math.sin(th), math.cos(th)), gl[i], t=t)
        path = skia.Path()
        path.addArc(skia.Rect.MakeXYWH(cx - R + 60, cy - R + 60, 2 * R - 120, 2 * R - 120), -60, 220)
        arrow(c, path, "#FFD23F", width=9, progress=1.0, head=30)
        # yeni katılan
        a = ease_out(remap(S.pts, 0.8, 1.3))
        th = S.t * 0.9 + math.pi / 3
        jx = lerp(1000, cx + (R + 0) * math.cos(th), ease_io(remap(S.pts, 0.8, 2.6)))
        jy = lerp(1500, cy + (R + 0) * math.sin(th), ease_io(remap(S.pts, 0.8, 2.6)))
        _top_glider(c, jx, jy, _hd(cx - jx, cy - jy), G_VIOLET, t=t, alpha=a)
        chip(c, "AYNI YÖNE DÖN", 540, 1335, 36, "yellow", "#1F1300", alpha=a, weight="black")
    elif case == "landing":
        # yandan şematik: iki pilot, alçaktaki öncelikli
        c.drawRect(skia.Rect.MakeXYWH(0, 1450, W, H - 1450), P("#3E7D4B"))
        world.target(c, 540, 1480, 140, 30, pulse_t=t)
        g3.render(c, lerp(260, 470, k), lerp(1150, 1370, k), 20, yaw=g3.SIDE_34, elev=0.2, anchor="pilot", t=t)
        g3.render(c, 760 + 80 * math.sin(S.t * 0.9), 720, 20, yaw=g3.SIDE_34 + 0.6 * math.sin(S.t * 0.9), elev=0.2, anchor="pilot", t=t, glider=G_BLUE)
        a = ease_out(remap(S.pts, 0.2, 0.6))
        chip(c, "ÖNCELİK", 300, 1010, 34, "green", "white", alpha=a, weight="black")
        chip(c, "BEKLE", 760, 560, 34, "cyan", "#06222A", alpha=a, weight="black")


# ---------------------------------------------------------------- PLF
def _seg(a, ang, L):
    r = math.radians(ang)
    return (a[0] + math.sin(r) * L, a[1] - math.cos(r) * L)


def _cap(c, a, b, r, col, alpha=1.0):
    c.drawLine(a[0], a[1], b[0], b[1], P(col, alpha, stroke=2 * r))


@scene("plf")
def plf(c, S):
    t = S.gt
    world.studio_bg(c, "#22C55E", S.t)
    gy = 1300
    c.drawRect(skia.Rect.MakeXYWH(0, gy, W, 8), P("#FFFFFF", 0.5))
    c.drawRect(skia.Rect.MakeXYWH(0, gy + 8, W, 260), skia.Paint(Shader=lin((0, gy), (0, gy + 260), [C("#22C55E", 0.28), C("#22C55E", 0.0)])))
    roll = S.v("roll", 0.0, dur=S.pd * 0.8, ease=ease_io)
    bend = S.v("bend", 0.3, dur=0.6)
    bad = S.v("bad_hand", 0.0, dur=0.5)
    sc = 2.55
    fx, fy = 600 - roll * 40, gy - 4
    th = -math.radians(92) * roll
    # açılar (dikeyden, + = ileri)
    a_shin = 12 + 22 * bend + 25 * roll
    a_thigh = -10 - 35 * bend - 30 * roll
    a_torso = 10 + 15 * bend + 10 * roll
    a_up = 160 if bad < 0.5 else -150
    a_fore = 15 if bad < 0.5 else -175
    ank = (0.0, 0.0)
    knee = _seg(ank, a_shin, 46)
    hip = _seg(knee, a_thigh, 46)
    sh = _seg(hip, a_torso, 58)
    head = _seg(sh, a_torso + 5, 26)
    elb = _seg(sh, a_up, 27)
    hand = _seg(elb, a_fore, 25)

    def T(p):
        x, y = p
        return (fx + (x * math.cos(th) - y * math.sin(th)) * sc, fy + (x * math.sin(th) + y * math.cos(th)) * sc)
    # gölge
    c.drawOval(skia.Rect.MakeXYWH(fx - 150, gy - 6, 300, 22), P("#000000", 0.35, blur=10))
    # arka bacak ve kol (koyu)
    off = lambda p: (p[0] - 6, p[1])
    _cap(c, T(off(ank)), T(off(knee)), 11 * sc, "#111827")
    _cap(c, T(off(knee)), T(off(hip)), 13 * sc, "#111827")
    _cap(c, T((ank[0] - 6, 0)), T((ank[0] + 10, 2)), 7 * sc, "#5B2310")
    _cap(c, T(off(sh)), T(off(elb)), 7.5 * sc, "#111827")
    _cap(c, T(off(elb)), T(off(hand)), 6.5 * sc, "#111827")
    # oturak/sırt koruması
    back = lambda p, k=16: (p[0] - k * math.cos(math.radians(a_torso)), p[1] - k * math.sin(math.radians(a_torso)))
    _cap(c, T(back(hip, 14)), T(back(sh, 12)), 17 * sc, "#0F172A")
    # ön bacak
    _cap(c, T(ank), T(knee), 11 * sc, "#1F2937")
    _cap(c, T(knee), T(hip), 13 * sc, "#1F2937")
    _cap(c, T((0, 0)), T((16, 2)), 7 * sc, "#7C2D12")
    # gövde
    _cap(c, T(hip), T(sh), 15 * sc, "#1E3A8A")
    _cap(c, T(_seg(hip, a_torso, 12)), T(_seg(hip, a_torso, 40)), 15 * sc, "#2747A8")
    # ön kol
    _cap(c, T(sh), T(elb), 7.5 * sc, "#2747A8")
    _cap(c, T(elb), T(hand), 6.5 * sc, "#2747A8")
    hx_, hy_ = T(hand)
    c.drawCircle(hx_, hy_, 7 * sc, P("#111827"))
    # kask
    hx, hy = T(head)
    hr = 15 * sc
    c.drawCircle(hx, hy, hr, skia.Paint(AntiAlias=True, Shader=rad((hx - 12, hy - 14), hr * 1.3, [C("#FFFFFF"), C("#CBD5E1")])))
    c.save()
    clip = skia.Path()
    clip.addCircle(hx, hy, hr)
    c.clipPath(clip, skia.ClipOp.kIntersect, True)
    fx_, fy_ = T(_seg(head, a_torso + 90, 14))
    c.drawCircle(fx_, fy_ + 0.15 * hr, hr * 0.62, P("#0F172A", 0.92))
    bx_, by_ = T(_seg(head, a_torso - 60, 13))
    c.drawCircle(bx_, by_, hr * 0.5, P("#FF6A1A"))
    c.restore()
    c.drawCircle(hx, hy, hr, P("#0F172A", 0.5, stroke=2))
    # temas noktaları
    pts = [("1  AYAK TABANI", (6, -2), 0.02), ("2  BALDIR", back(_seg(ank, a_shin, 26), 10), 0.28),
           ("3  KALÇA / UYLUK", back(_seg(knee, a_thigh, 36), 12), 0.55), ("4  SIRT", back(_seg(hip, a_torso, 40), 16), 0.85)]
    if S.get("show_points", False):
        for i, (lab, p, th_on) in enumerate(pts):
            on = (roll >= th_on) if S.get("seq_points", True) else True
            a = 1.0 if on else 0.3
            x, y = T(p)
            c.drawCircle(x, y, 22 + 8 * pulse(S.t + i * 0.2, 0.9) * on, P("#FFD23F", 0.3 * a))
            c.drawCircle(x, y, 13, P("#FFD23F", a))
            c.drawCircle(x, y, 13, P("#0B1220", a, stroke=3))
            chip(c, lab, 300, 640 + i * 96, 36, "yellow" if on else "glass", "#1F1300" if on else "white", alpha=1.0, weight="black", align="left")
    if S.get("roll_arrow"):
        a = ease_out(remap(S.pts, 0, 0.4))
        path = skia.Path()
        path.addArc(skia.Rect.MakeXYWH(fx - 420, fy - 420, 840, 840), -70, -100)
        arrow(c, path, "#22D3EE", width=10, progress=ease_io(remap(S.pts, 0.1, 1.2)), alpha=a, head=30, glow=True)
    if S.get("together"):
        a = ease_out(remap(S.pts, 0.2, 0.6))
        kx, ky = T(knee)
        c.drawRoundRect(skia.Rect.MakeXYWH(kx - 80, ky - 70, 170, 230), 40, 40, P("#22D3EE", a, stroke=6, dash=(16, 10)))
        chip(c, "AYAK + DİZ BİTİŞİK", kx + 260, ky + 20, 34, "cyan", "#06222A", alpha=a, weight="black")
    if bad > 0.5:
        icon_cross(c, hx_ - 40, hy_ - 110, 54, "red", 1.0, progress=remap(S.pts, 0.3, 0.8))
