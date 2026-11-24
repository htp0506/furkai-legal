"""Genel sahneler: açılış (hook), özet, kapanış (CTA), ifade kartı, karşılaştırma, ikon kartları."""
import math
import skia
from ..core import scene, SCENES, SceneState
from ..gfx import (C, P, W, H, draw_text, text_width, wrap, glass, chip, rrect, circle, lin, rad, clamp, lerp,
                   ease_out, ease_back, ease_io, smooth, remap, icon_check, icon_cross, icon_warn, pulse)
from .. import world, glider3d as g3
from ..brand import BRAND


def _bg(c, S, name, params):
    """Başka bir sahneyi arka plan olarak çiz."""
    fn = SCENES[name]
    st = SceneState(S.gt, S.gt - S.t, S.gt - S.t + S.T, [(0, S.T, params)], S.ep)
    fn(c, st)


@scene("hook")
def hook(c, S):
    ep = S.ep
    bg = S.get("bg", "sky_glider")
    _bg(c, S, bg, S.get("bgp", {}))
    # karartma
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=lin((0, 500), (0, 1300), [C("#000000", 0.0), C("#000000", 0.35), C("#000000", 0.0)], [0, 0.5, 1])))
    t = S.t
    title = ep["title"]
    sub = ep.get("subtitle")
    module = ep.get("module_label")
    ty = S.get("title_y", 860)
    # modül etiketi
    a0 = ease_out(remap(t, 0.15, 0.55))
    if module:
        chip(c, module, 540, ty - 230 + (1 - a0) * 20, 34, "glass", "white", alpha=a0, weight="xbold", pad=(26, 14))
    # alt başlık (üstte, renkli)
    if sub:
        a1 = ease_back(remap(t, 0.25, 0.7))
        c.save()
        c.translate(540, ty - 140)
        c.scale(0.7 + 0.3 * a1, 0.7 + 0.3 * a1)
        chip(c, sub, 0, 0, 54, "orange", "white", alpha=clamp(a1 * 1.2), weight="black", pad=(36, 18))
        c.restore()
    # ana başlık
    lines = title.split("\n")
    widest = max(text_width(l, 100, "black") for l in lines)
    size = S.get("title_size", min(176, 100 * 930 / max(1, widest)))
    for li, ln in enumerate(lines):
        a2 = ease_out(remap(t, 0.35 + li * 0.12, 0.85 + li * 0.12))
        sc = 1.25 - 0.25 * ease_out(remap(t, 0.35 + li * 0.12, 1.0 + li * 0.12))
        c.save()
        c.translate(540, ty + li * size * 1.0)
        c.scale(sc, sc)
        draw_text(c, ln, 0, size * 0.36, size, "white", "black", "center", a2, shadow=(0, 10, 0.5, 24))
        c.restore()
    # alt çizgi
    a3 = ease_out(remap(t, 0.8, 1.3))
    lw = 300 * a3
    yb = ty + (len(lines) - 1) * size + size * 0.62
    rrect(c, 540 - lw / 2, yb, lw, 10, 5, P("#FFB020", a3))


@scene("sky_glider")
def sky_glider(c, S):
    """Basit arka plan: gökyüzü + dağlar + süzülen kanat."""
    t = S.gt
    theme = S.get("theme", "day")
    world.sky(c, theme)
    world.clouds(c, t, 0, alpha=0.85, count=4, y_range=(250, 760), speed=10)
    world.mountains(c, base_y=S.get("mbase", 1420), camx=t * 40)
    if S.get("ground", True):
        world.ground(c, S.get("gy", 1560), camx=t * 120)
    x = S.get("x", 540) + math.sin(t * 0.6) * 30
    y = S.get("y", 1250) + math.sin(t * 1.1) * 12
    g3.render(c, x, y, S.get("scale", 42), yaw=S.get("yaw", g3.SIDE_34), elev=S.get("elev", 0.22),
              pitch=math.sin(t * 1.3) * 0.04, roll=S.get("roll", 0.0) + math.sin(t * 0.7) * 0.03,
              anchor="center", t=t)


@scene("statement")
def statement(c, S):
    """Büyük ikon + ifade. p: icon (emoji), text, color, bg"""
    t = S.t
    world.studio_bg(c, S.get("accent", "#FF6A1A"), t)
    icon = S.get("icon")
    a = ease_back(remap(S.pts, 0.0, 0.5))
    if icon:
        c.save()
        c.translate(540, 820)
        c.scale(0.6 + 0.4 * a, 0.6 + 0.4 * a)
        c.drawCircle(0, 0, 190, P(S.get("accent", "#FF6A1A"), 0.22 * clamp(a)))
        c.drawCircle(0, 0, 190, P(S.get("accent", "#FF6A1A"), 0.6 * clamp(a), stroke=6))
        draw_text(c, icon, 0, 70, 200, "white", "bold", "center", clamp(a))
        c.restore()
    txt = S.get("text")
    if txt:
        lines = wrap(txt, 74, 920, "black")
        for i, ln in enumerate(lines):
            aa = ease_out(remap(S.pts, 0.2 + i * 0.1, 0.6 + i * 0.1))
            draw_text(c, ln, 540, 1130 + i * 86 + (1 - aa) * 20, 74, "white", "black", "center", aa)


@scene("recap")
def recap(c, S):
    t = S.t
    world.studio_bg(c, "#FF6A1A", t)
    items = S.get("items", [])
    a0 = ease_back(remap(t, 0.05, 0.45))
    c.save()
    c.translate(540, 400)
    c.scale(0.7 + 0.3 * a0, 0.7 + 0.3 * a0)
    chip(c, "📌 ÖZET", 0, 0, 52, "orange", "white", alpha=clamp(a0), weight="black")
    c.restore()
    n = len(items)
    rowh = 150 if n <= 4 else 128
    y0 = 560 + (4 - min(n, 4)) * 40
    total_t = S.T - 1.0
    for i, it in enumerate(items):
        ti = 0.35 + i * min(0.9, total_t / max(1, n))
        a = ease_out(remap(t, ti, ti + 0.4))
        if a <= 0:
            continue
        y = y0 + i * rowh
        x0 = 90 + (1 - a) * 60
        glass(c, x0, y, 900, rowh - 26, 34, alpha=0.5 * a, blur=0, border=0.12)
        icon_check(c, x0 + 66, y + (rowh - 26) / 2, 34, "green", a, progress=remap(t, ti + 0.15, ti + 0.5))
        lines = wrap(it, 44, 720, "bold")
        for k, ln in enumerate(lines[:2]):
            yy = y + (rowh - 26) / 2 + 15 - (len(lines[:2]) - 1) * 26 + k * 52
            draw_text(c, ln, x0 + 125, yy, 44, "white", "bold", "left", a)


@scene("outro")
def outro(c, S):
    t = S.t
    ep = S.ep
    bg = S.get("bg")
    if bg:
        _bg(c, S, bg, S.get("bgp", {}))
        c.drawRect(skia.Rect.MakeWH(W, H), P("#0B1220", 0.55))
    else:
        world.studio_bg(c, "#FFB020", t)
    q = S.get("q", "Yorumlara yaz!")
    a = ease_back(remap(t, 0.05, 0.5))
    c.save()
    c.translate(540, 420)
    c.scale(0.7 + 0.3 * a, 0.7 + 0.3 * a)
    chip(c, "💬 YORUMLARA YAZ", 0, 0, 44, "yellow", "#1F1300", alpha=clamp(a), weight="black")
    c.restore()
    qs = 82
    lines = wrap(q, qs, 940, "black")
    if len(lines) > 2:
        qs = 64
        lines = wrap(q, qs, 960, "black")
    lh = qs * 1.17
    for i, ln in enumerate(lines):
        aa = ease_out(remap(t, 0.2 + i * 0.12, 0.6 + i * 0.12))
        draw_text(c, ln, 540, 590 + i * lh + (1 - aa) * 24, qs, "white", "black", "center", aa, shadow=(0, 6, 0.4, 12))
    # cevap seçenekleri (dönen etiketler)
    opts = S.get("options", [])
    if opts:
        yb = min(870, 590 + len(lines) * lh + 70)
        aa = ease_out(remap(t, 0.7, 1.1))
        # 2 satır halinde, kayan şerit
        row = opts
        rw = [text_width(o, 40, "xbold") + 70 for o in row]
        total = sum(rw) + 20 * len(row)
        off = (t * 70) % total
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(40, yb - 50, W - 80, 220))
        for rr in range(2):
            x = (40 - off) if rr == 0 else (40 - total + off * 0.8)
            yy = yb + rr * 100
            for rep in range(3):
                for o, w in zip(row, rw):
                    hl = (int(t * 1.6) % len(row)) == row.index(o) and rr == 0
                    chip(c, o, x + w / 2, yy, 40, "orange" if hl else "glass", "white", alpha=aa, weight="xbold", shadow=False)
                    x += w + 20
        c.restore()
        c.drawRect(skia.Rect.MakeXYWH(40, yb - 50, 80, 220), skia.Paint(Shader=lin((40, 0), (120, 0), [C("#0B1220", 0.9), C("#0B1220", 0.0)])))
        c.drawRect(skia.Rect.MakeXYWH(W - 120, yb - 50, 80, 220), skia.Paint(Shader=lin((W - 120, 0), (W - 40, 0), [C("#0B1220", 0.0), C("#0B1220", 0.9)])))
    # alt bölüm: takip / kaydet / sonraki ders
    a2 = ease_out(remap(t, 1.0, 1.5))
    yb2 = 1050
    if ep.get("next_title"):
        glass(c, 90, yb2, 900, 120, 36, alpha=0.55 * a2, border=0.15)
        draw_text(c, "SONRAKİ DERS", 140, yb2 + 48, 26, "#FFB020", "black", "left", a2, tracking=0.08)
        draw_text(c, ep["next_title"], 140, yb2 + 94, 42, "white", "xbold", "left", a2)
        draw_text(c, "→", 930, yb2 + 82, 60, "white", "black", "center", a2 * (0.6 + 0.4 * pulse(t, 0.8)))
    else:
        glass(c, 90, yb2, 900, 120, 36, alpha=0.55 * a2, border=0.15)
        draw_text(c, "SERİ TAMAMLANDI 🎉", 540, yb2 + 76, 44, "white", "xbold", "center", a2)
    a3 = ease_out(remap(t, 1.3, 1.8))
    chip(c, "🔖 Kaydet", 300, 1250, 36, "glass", "white", alpha=a3, weight="bold", shadow=False)
    chip(c, "📤 Paylaş", 540, 1250, 36, "glass", "white", alpha=a3, weight="bold", shadow=False)
    chip(c, "➕ Takip et", 790, 1250, 36, "orange", "white", alpha=a3, weight="bold", shadow=False)
    draw_text(c, BRAND.handle, 540, 1350, 34, "white", "bold", "center", a3 * 0.95)
    draw_text(c, "Bu video bilgilendirme amaçlıdır. Uçuş eğitimini lisanslı eğitmenle al.", 540, 1398, 24,
              "#CBD5E1", "medium", "center", a3 * 0.8)


@scene("compare")
def compare(c, S):
    """İki durum yan yana. p: left/right = dict(title, verdict('ok'|'bad'|'warn'), glider=dict(...), note)"""
    t = S.t
    world.sky(c, S.get("theme", "day"))
    world.clouds(c, S.gt, 0, alpha=0.6, count=3, y_range=(300, 700), speed=8)
    world.mountains(c, base_y=1380, camx=S.gt * 25)
    world.ground(c, 1450, camx=S.gt * 60)
    for i, side in enumerate(("left", "right")):
        d = S.get(side)
        if not d:
            continue
        ti = 0.1 + i * 0.35
        a = ease_out(remap(S.t, ti, ti + 0.45))
        cx = 280 if i == 0 else 800
        glass(c, cx - 250, 560, 500, 820, 44, alpha=0.32 * a, blur=0, border=0.18)
        draw_text(c, d.get("title", ""), cx, 640, 44, "white", "black", "center", a)
        gp = dict(d.get("glider", {}))
        anim = gp.pop("anim", None)
        tt = S.gt
        if anim == "shake":
            gp["roll"] = gp.get("roll", 0) + math.sin(tt * 9) * 0.06
        if anim == "flutter":
            gp["crumple"] = gp.get("crumple", 0.3) * (0.7 + 0.3 * math.sin(tt * 6))
        sc = gp.pop("scale", 34)
        yy = gp.pop("y", 1000)
        g3.render(c, cx, yy + (1 - a) * 40, sc, alpha=a, t=tt, anchor="center", **{"yaw": g3.SIDE_34, "elev": 0.2, **gp})
        v = d.get("verdict")
        if v == "ok":
            icon_check(c, cx, 1300, 44, "green", a, progress=remap(S.t, ti + 0.3, ti + 0.8))
        elif v == "bad":
            icon_cross(c, cx, 1300, 44, "red", a, progress=remap(S.t, ti + 0.3, ti + 0.8))
        elif v == "warn":
            icon_warn(c, cx, 1300, 44, "amber", a)
        if d.get("note"):
            for k, ln in enumerate(wrap(d["note"], 32, 440, "bold")):
                draw_text(c, ln, cx, 700 + k * 40, 32, "#FDE68A", "bold", "center", a)


@scene("cards")
def cards(c, S):
    """İkon kartları ızgarası (ekipman vb.). p: items=[(emoji, başlık)], focus=index, cols"""
    t = S.t
    world.studio_bg(c, S.get("accent", "#22D3EE"), t)
    items = S.get("items", [])
    focus = S.get("focus", None)
    cols = S.get("cols", 2)
    shown = S.get("shown", len(items))
    cw, ch = (430, S.get("ch", 250)) if cols == 2 else (290, S.get("ch", 250))
    gx = (W - cols * cw - (cols - 1) * 30) / 2
    y0 = S.get("y0", 560)
    for i, (em, title) in enumerate(items):
        if i >= shown:
            break
        r, k = divmod(i, cols)
        x = gx + k * (cw + 30)
        y = y0 + r * (ch + 30)
        reveal = S.get("reveal")
        if reveal is not None:
            appear = S.start(reveal[i]) + 0.1 + 0.25 * sum(1 for j in range(i) if reveal[j] == reveal[i])
        else:
            appear = 0.1 + i * 0.12
        a = ease_out(remap(S.t, appear, appear + 0.4))
        if a <= 0:
            continue
        is_f = focus is not None and (i == focus if not isinstance(focus, (list, tuple)) else i in focus)
        dim = 1.0 if (focus is None or is_f) else 0.45
        sc = 1.0 + (0.06 * ease_back(S.prog(S.ph, 0.4)) if is_f else 0)
        c.save()
        c.translate(x + cw / 2, y + ch / 2 + (1 - a) * 30)
        c.scale(sc, sc)
        glass(c, -cw / 2, -ch / 2, cw, ch, 36, tint="#FFB020" if is_f else "#0B1220", alpha=(0.22 if is_f else 0.5) * a * dim, blur=0,
              border=0.5 if is_f else 0.12)
        draw_text(c, em, 0, 22 - (250 - ch) * 0.25, 128 * min(1, ch / 250 + 0.1), "white", "bold", "center", a * dim)
        draw_text(c, title, 0, ch / 2 - 30, 36, "white", "xbold", "center", a * dim)
        c.restore()


@scene("checklist")
def checklist(c, S):
    """Numaralı kontrol listesi. p: items=[metin], active=index (o ana kadar işaretlenir)"""
    t = S.t
    world.studio_bg(c, "#22C55E", t)
    items = S.get("items", [])
    active = S.get("active", -1)
    y0 = S.get("y0", 600)
    rowh = 128
    for i, it in enumerate(items):
        a = ease_out(remap(t, 0.1 + i * 0.1, 0.5 + i * 0.1))
        y = y0 + i * rowh
        cur = i == active
        done = i < active or (cur and S.pts > 1.2)
        glass(c, 80, y, 920, rowh - 20, 30, tint="#16A34A" if cur else "#0B1220", alpha=(0.35 if cur else 0.45) * a, blur=0,
              border=0.6 if cur else 0.1)
        circle(c, 150, y + (rowh - 20) / 2, 36, P("#FFB020" if cur else "#334155", a))
        draw_text(c, str(i + 1), 150, y + (rowh - 20) / 2 + 15, 40, "#0B1220" if cur else "white", "black", "center", a)
        col = "white" if (cur or done) else "#94A3B8"
        draw_text(c, it, 215, y + (rowh - 20) / 2 + 15, 42, col, "xbold", "left", a)
        if done:
            pr = remap(S.pts, 1.2, 1.6) if cur else 1.0
            icon_check(c, 940, y + (rowh - 20) / 2, 30, "green", a, progress=pr)
