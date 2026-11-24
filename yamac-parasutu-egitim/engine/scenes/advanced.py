"""İkinci set sahneleri: yer hızı, termik merkezleme (üstten), irtifa-sıcaklık, gün içi saatler,
toz hortumu, fren konumları ve HUD göstergeleri."""
import math
import random
import skia
from ..core import scene
from ..gfx import (C, P, W, H, draw_text, text_width, glass, chip, rrect, lin, rad, clamp, lerp, ease_out, ease_in,
                   ease_io, ease_back, smooth, remap, smooth_path, poly, arrow, line_arrow, pulse, circle, mix,
                   icon_check, icon_cross, icon_warn, angle_arc)
from .. import world, glider3d as g3


# ---------------------------------------------------------------- HUD göstergeleri
def hud_gmeter(c, x, y, g, alpha=1.0, limit=4.5):
    glass(c, x, y, 250, 150, 30, alpha=0.62 * alpha, blur=0, border=0.14)
    col = "#34D399" if g < 2.5 else ("#FFB020" if g < limit - 0.3 else "#F43F5E")
    draw_text(c, "G KUVVETİ", x + 26, y + 38, 22, "#94A3B8", "bold", "left", alpha, tracking=0.1)
    draw_text(c, f"{g:.1f} G", x + 26, y + 104, 60, col, "black", "left", alpha)
    rrect(c, x + 26, y + 120, 198, 10, 5, P("#FFFFFF", 0.15 * alpha))
    rrect(c, x + 26, y + 120, 198 * clamp(g / 6.0), 10, 5, P(col, alpha))
    lx = x + 26 + 198 * limit / 6.0
    c.drawLine(lx, y + 114, lx, y + 136, P("#F43F5E", alpha, stroke=3))


def hud_bank(c, x, y, deg, alpha=1.0):
    glass(c, x, y, 250, 150, 30, alpha=0.62 * alpha, blur=0, border=0.14)
    draw_text(c, "YATIŞ", x + 26, y + 38, 22, "#94A3B8", "bold", "left", alpha, tracking=0.1)
    cx, cy, r = x + 180, y + 112, 52
    c.drawLine(cx - r, cy, cx + r, cy, P("#FFFFFF", 0.3 * alpha, stroke=3))
    a = math.radians(deg)
    c.drawLine(cx, cy, cx + math.cos(-a) * r, cy + math.sin(-a) * r, P("#FFB020", alpha, stroke=6))
    angle_arc(c, cx, cy, r * 0.7, -deg, 0, "#FFB020", 4, alpha)
    draw_text(c, f"{deg:.0f}°", x + 26, y + 112, 54, "white", "black", "left", alpha)


def hud_altbar(c, x, y, alt, floor=300, top=1500, alpha=1.0):
    glass(c, x, y, 150, 420, 30, alpha=0.62 * alpha, blur=0, border=0.14)
    draw_text(c, "İRTİFA", x + 75, y + 40, 22, "#94A3B8", "bold", "center", alpha, tracking=0.1)
    bx, by, bh = x + 60, y + 60, 300
    rrect(c, bx, by, 30, bh, 15, P("#FFFFFF", 0.12 * alpha))
    fy = by + bh * (1 - floor / top)
    c.drawRect(skia.Rect.MakeXYWH(bx, fy, 30, by + bh - fy), P("#F43F5E", 0.35 * alpha))
    c.drawLine(bx - 10, fy, bx + 40, fy, P("#F43F5E", alpha, stroke=4))
    draw_text(c, f"{floor} m", x + 75, fy + 34, 22, "#FDA4AF", "black", "center", alpha)
    my = by + bh * (1 - clamp(alt / top))
    c.drawPath(poly([(bx + 34, my), (bx + 56, my - 12), (bx + 56, my + 12)]), P("white", alpha))
    draw_text(c, f"{alt:.0f}", x + 75, y + 400, 34, "white", "black", "center", alpha)


# ---------------------------------------------------------------- hava hızı / yer hızı
@scene("groundspeed")
def groundspeed(c, S):
    """p: air (km/sa), wind (+ karşı, - arka), ok etiketleri"""
    t = S.gt
    air = S.v("air", 38.0, dur=0.8)
    wind = S.v("wind", 0.0, dur=0.9)
    gs = air - wind
    world.sky(c, "bright")
    camx = S.t * gs * 9
    world.clouds(c, t, 0, alpha=0.75, count=4, y_range=(300, 700), speed=0, camx=camx * 0.6)
    world.mountains(c, base_y=1250, camx=camx)
    world.ground(c, 1300, camx=camx * 2.2)
    for k in range(-2, 9):
        wx = k * 380 - (camx * 2.0) % 380
        world.tree(c, wx + 60, 1306, 0.9)
    # rüzgar parçacıkları
    if abs(wind) > 1:
        world.wind_particles(c, t, (0, 560, W, 600), n=int(10 + abs(wind) * 1.2), speed=-wind * 22, alpha=0.5,
                             length=40 + abs(wind) * 2, angle=math.pi if wind > 0 else 0.0)
    gx, gy = 560, 960
    g3.render(c, gx, gy + math.sin(t * 1.4) * 8, 36, yaw=g3.SIDE_34, elev=0.18, anchor="center", t=t)
    # oklar
    a = ease_out(remap(S.pts, 0.1, 0.6))
    y0 = 1170
    sc = 9.0
    line_arrow(c, gx - 150, y0, gx - 150 + air * sc, y0, color="#22D3EE", width=12, alpha=a, head=30)
    chip(c, f"HAVA HIZI {air:.0f}", gx - 150 + air * sc / 2, y0 - 50, 30, "cyan", "#06222A", alpha=a, weight="black")
    if abs(wind) > 1:
        wy = y0 + 70
        if wind > 0:
            line_arrow(c, gx - 150 + air * sc, wy, gx - 150 + (air - wind) * sc, wy, color="#F43F5E", width=12, alpha=a, head=30)
            chip(c, f"KARŞI RÜZGAR {wind:.0f}", gx - 150 + (air - wind / 2) * sc, wy + 48, 30, "red", "white", alpha=a, weight="black")
        else:
            line_arrow(c, gx - 150 + air * sc, wy, gx - 150 + (air - wind) * sc, wy, color="#22C55E", width=12, alpha=a, head=30)
            chip(c, f"ARKA RÜZGAR {-wind:.0f}", gx - 150 + (air - wind / 2) * sc, wy + 48, 30, "green", "white", alpha=a, weight="black")
    # sonuç
    col = "#22C55E" if gs > 30 else ("#FFB020" if gs > 0 else "#F43F5E")
    glass(c, 300, 600, 480, 150, 40, alpha=0.6 * a, blur=0, border=0.18)
    draw_text(c, "YER HIZI", 540, 650, 26, "#CBD5E1", "black", "center", a, tracking=0.12)
    draw_text(c, f"{gs:.0f} km/sa", 540, 725, 64, col, "black", "center", a)
    if gs < 0:
        draw_text(c, "← GERİ GİDİYORSUN", 540, 800, 34, "#FDA4AF", "black", "center", a * pulse(t, 0.8))


# ---------------------------------------------------------------- termik (üstten)
@scene("thermal_top")
def thermal_top(c, S):
    """p: tight (0 geniş daire .. 1 dar daire), drift (0..1 rüzgarla kayma), show_wind"""
    t = S.gt
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=lin((0, 0), (W, H), [C("#4E8F4F"), C("#76BD6E"), C("#4C8A4A")])))
    for (x, y, r) in [(120, 520, 110), (960, 640, 130), (150, 1500, 150), (980, 1600, 120)]:
        c.drawCircle(x, y, r, P("#2E6B3A", 0.85))
    drift = S.v("drift", 0.0, dur=S.pd * 0.9)
    cx = 540 + 220 * drift * math.sin(min(1, S.t / 8) * 1.2)
    cy = 960
    R0 = 300
    c.drawCircle(cx, cy, R0, skia.Paint(AntiAlias=True, Shader=rad((cx, cy), R0, [C("#FB923C", 0.55), C("#FB923C", 0.18), C("#FB923C", 0.0)], [0, 0.6, 1])))
    c.drawCircle(cx, cy, R0 * 0.38, P("#F97316", 0.35 + 0.1 * pulse(t, 1.4)))
    c.drawCircle(cx, cy, R0, P("#FDBA74", 0.6, stroke=3, dash=(14, 10)))
    draw_text(c, "ÇEKİRDEK", cx, cy + 10, 30, "#FFF7ED", "black", "center", 0.9)
    draw_text(c, "ZAYIF", cx + R0 * 0.72, cy - R0 * 0.75, 26, "#FFEDD5", "black", "center", 0.8)
    tight = S.v("tight", 0.0, dur=1.2)
    R = lerp(R0 * 1.25, R0 * 0.55, tight)
    th = S.t * 1.25
    pts = [(cx + R * math.cos(a), cy + R * math.sin(a)) for a in [i / 40 * 2 * math.pi for i in range(41)]]
    c.drawPath(smooth_path(pts), P("#FFFFFF", 0.6, stroke=4, dash=(16, 12)))
    x, y = cx + R * math.cos(th), cy + R * math.sin(th)
    hd = math.atan2(math.sin(th), math.cos(th))   # teğet yön (saat yönü tersi)
    g3.render(c, x, y, 20, yaw=0.0, elev=math.pi / 2, heading=hd, anchor="pilot", t=t, lines=False)
    if S.get("show_wind"):
        a = ease_out(remap(S.pts, 0.1, 0.5))
        for k in range(5):
            ph = (S.t * 0.7 + k / 5) % 1
            yy = 600 + k * 160
            xx = lerp(60, 1000, ph)
            line_arrow(c, xx, yy, xx + 90, yy, color="#FFD23F", width=7, alpha=a * math.sin(ph * math.pi), head=20)
        chip(c, "RÜZGAR →", 170, 1380, 32, "yellow", "#1F1300", alpha=a, weight="black")
    lab = S.get("label")
    if lab:
        chip(c, lab, 540, 1330, 38, "orange", "white", alpha=ease_out(remap(S.pts, 0.3, 0.7)), weight="black")


# ---------------------------------------------------------------- irtifa - sıcaklık
@scene("lapse")
def lapse(c, S):
    t = S.gt
    world.sky(c, "day", sun=(900, 260))
    world.mountains(c, base_y=1500, camx=0)
    world.ground(c, 1520, camx=0)
    ground_t = S.get("ground_t", 25)
    levels = [0, 1000, 2000, 3000]
    y_of = lambda h: 1500 - h * 0.30
    shown = S.v("shown", 4, dur=0.01)
    for i, h in enumerate(levels):
        if i >= shown + 0.5:
            break
        a = ease_out(remap(S.t, 0.2 + i * 0.5, 0.6 + i * 0.5)) if S.get("seq", True) else 1.0
        y = y_of(h)
        c.drawLine(60, y, 1020, y, P("#FFFFFF", 0.35 * a, stroke=2, dash=(12, 10)))
        draw_text(c, f"{h} m", 80, y - 14, 30, "white", "black", "left", a, shadow=(0, 2, 0.5, 4))
        temp = ground_t - 6.5 * h / 1000
        col = "#F97316" if temp > 15 else ("#FBBF24" if temp > 8 else "#38BDF8")
        chip(c, f"{temp:.1f} °C", 880, y - 28, 34, col, "white" if temp > 8 else "#06222A", alpha=a, weight="black")
    climb = S.v("climb", 0.0, dur=S.pd * 0.9)
    gy = lerp(1380, y_of(2000) + 60, climb)
    g3.render(c, 470, gy, 22, yaw=g3.SIDE_34, elev=0.2, anchor="center", t=t)
    if S.get("cold"):
        a = ease_out(remap(S.pts, 0.2, 0.6))
        for k in range(14):
            rnd = random.Random(k)
            x = (rnd.uniform(0, W) + S.t * 40) % W
            y = (rnd.uniform(300, 900) + S.t * 60) % 700 + 300
            draw_text(c, "❄", x, y, 30, "white", "bold", "center", a * 0.8)


# ---------------------------------------------------------------- gün içi saatler
@scene("daytime")
def daytime(c, S):
    """p: hour (6..20)"""
    t = S.gt
    hour = S.v("hour", 8.0, dur=S.pd * 0.7)
    u = clamp((hour - 6) / 14)
    sun_x = lerp(100, 980, u)
    sun_y = 900 - math.sin(u * math.pi) * 600
    noon = math.sin(u * math.pi)
    theme = "bright" if 0.25 < u < 0.75 else "golden"
    world.sky(c, theme, sun=(int(sun_x / 20) * 20, int(sun_y / 20) * 20))
    world.mountains(c, base_y=1350, camx=0)
    world.ground(c, 1380, camx=0)
    # termik/türbülans yoğunluğu
    strength = clamp((noon - 0.55) / 0.45)
    for k in range(int(2 + strength * 8)):
        rnd = random.Random(k)
        x = rnd.uniform(150, 930)
        y = rnd.uniform(800, 1250)
        world.swirl(c, x, y, 30 + 30 * strength, t + k, "#F97316", 0.25 + 0.55 * strength, turns=1.1, width=4)
    shake = strength
    g3.render(c, 540 + math.sin(t * 9) * 10 * shake, 950 + math.cos(t * 7) * 8 * shake, 30, yaw=g3.SIDE_34, elev=0.2,
              anchor="center", t=t, roll=math.sin(t * 6) * 0.15 * shake)
    hh, mm = int(hour), int((hour % 1) * 60)
    glass(c, 340, 1150, 400, 110, 40, alpha=0.6, blur=0, border=0.16)
    draw_text(c, f"{hh:02d}:{mm:02d}", 540, 1230, 64, "white", "black", "center")


# ---------------------------------------------------------------- toz hortumu
@scene("dustdevil")
def dustdevil(c, S):
    t = S.gt
    world.sky(c, "bright", sun=(880, 260))
    world.mountains(c, base_y=1250, camx=0)
    world.ground(c, 1300, camx=0, color_top="#C8B27A", color_bot="#8C7A4F")
    grow = S.v("grow", 0.0, dur=1.6)
    xpos = S.v("x", 700, dur=S.pd * 0.9)
    if grow > 0:
        H_ = 700 * grow
        for k in range(60):
            rnd = random.Random(k)
            h = rnd.uniform(0, 1)
            yy = 1300 - h * H_
            r = 30 + 110 * h
            a = t * 5 + k * 0.7
            x = xpos + math.cos(a) * r
            al = (0.25 + 0.5 * (1 - h)) * grow
            c.drawCircle(x, yy, 6 + 10 * h, P("#A16207", al, blur=3))
        path = skia.Path()
        path.moveTo(xpos - 30, 1300)
        path.lineTo(xpos - 140 * grow, 1300 - H_)
        path.lineTo(xpos + 140 * grow, 1300 - H_)
        path.lineTo(xpos + 30, 1300)
        path.close()
        c.drawPath(path, P("#D6B98C", 0.25 * grow, blur=18))
        world.swirl(c, xpos, 1300 - H_ * 0.5, 90 * grow, t, "#92400E", 0.6 * grow, turns=1.3, width=5, spin=2.0)
    # yerde serili kanat + pilot
    wing = S.get("wing", True)
    if wing:
        lift = S.v("lift", 0.0, dur=0.8)
        g3.render(c, 300, 1260 - 70, 28, yaw=g3.SIDE + 0.3, elev=0.14, pitch=lerp(-1.3, -0.2, lift), anchor="pilot", t=t,
                  pose=1.0, flat=lerp(0.6, 0.0, lift), inflate=lerp(0.2, 1.0, lift), crumple=0.25 + 0.3 * lift,
                  roll=0.4 * lift * math.sin(t * 5))
    if S.get("glider_air"):
        g3.render(c, 300 + math.sin(t * 8) * 12, 650, 22, yaw=g3.SIDE_34, elev=0.2, anchor="center", t=t,
                  roll=math.sin(t * 7) * 0.2, crumple=0.2)


# ---------------------------------------------------------------- fren konumları
@scene("brakepos")
def brakepos(c, S):
    t = S.gt
    world.sky(c, "day")
    world.clouds(c, t, 0, alpha=0.6, count=3, y_range=(300, 800), speed=10)
    world.mountains(c, base_y=1750, camx=t * 20)
    b = S.v("brake", 0.0, dur=0.9)
    x, y, sc = 540, 1180, 230
    info = g3.render(c, x, y, sc, yaw=math.pi, elev=0.05, anchor="pilot", t=t, brake_l=b, brake_r=b, lines=True,
                     pose=0.0, alpha=1.0, line_alpha=0.35)
    if not info:
        return
    marks = [("ÇEYREK · omuz", 0.18, "#22D3EE", 0.49), ("YARIM · göğüs", -0.02, "#FFB020", 0.76),
             ("TAM · kalça", -0.40, "#F43F5E", 1.27)]
    act = S.get("mark")
    for name, my, col, bb in marks:
        _, sy = info["proj"]([0, my, 0], pilot_frame=True)
        on = act is None or act == name.split(" ")[0]
        a = 1.0 if on else 0.3
        c.drawLine(120, sy, 960, sy, P(col, 0.8 * a, stroke=4, dash=(18, 12)))
        chip(c, name, 230, sy - 34, 30, col, "#0B1220" if col != "#F43F5E" else "white", alpha=a, weight="black")
    from .flight import widget_brake
    widget_brake(c, 700, 1240, min(1.0, b / 1.27), ease_out(remap(S.t, 0.2, 0.6)))
