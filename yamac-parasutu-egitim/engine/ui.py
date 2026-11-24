"""Videonun üst katmanları: marka başlığı, ilerleme çubuğu, ekran yazıları (kicker), altyazı."""
import math
import skia
from .gfx import (C, P, W, H, cached, draw_text, text_width, wrap, glass, chip, rrect, lin, rad, clamp, lerp,
                  ease_out, ease_back, smooth, remap, tr_upper)
from .brand import BRAND

KICK_COLORS = {
    "red": ("#F43F5E", "white"), "green": ("#16A34A", "white"), "yellow": ("#FFD23F", "#1F1300"),
    "orange": ("#FF6A1A", "white"), "blue": ("#2563EB", "white"), "cyan": ("#22D3EE", "#06222A"),
    "dark": ("glass", "white"), "white": ("#FFFFFF", "#0B1220"), "violet": ("#7C3AED", "white"),
}


def brand_badge(c, x, y, r, alpha=1.0):
    """Kulüp rozeti (logo dosyası yoksa vektör rozet)."""
    img = BRAND.logo_image()
    c.drawCircle(x, y + 4, r + 2, P("#000000", 0.3 * alpha, blur=8))
    if img is not None:
        c.save()
        path = skia.Path()
        path.addCircle(x, y, r)
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        c.drawImageRect(img, skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), skia.SamplingOptions(skia.FilterMode.kLinear),
                        skia.Paint(Alphaf=alpha))
        c.restore()
        c.drawCircle(x, y, r, P("#FFFFFF", 0.9 * alpha, stroke=3))
        return
    c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Shader=lin((x - r, y - r), (x + r, y + r), [C("#FF7A1A", alpha), C("#E11D48", alpha)])))
    c.drawCircle(x, y, r * 0.78, P("#FFFFFF", 0.95 * alpha))
    # küçük kanat ikonu
    path = skia.Path()
    path.addArc(skia.Rect.MakeXYWH(x - r * 0.55, y - r * 0.42, r * 1.1, r * 0.7), 200, 140)
    c.drawPath(path, P("#FF6A1A", alpha, stroke=r * 0.2))
    for dx in (-0.32, 0.0, 0.32):
        c.drawLine(x + dx * r, y - r * 0.12, x, y + r * 0.38, P("#1E293B", alpha, stroke=max(1, r * 0.05)))
    c.drawCircle(x, y + r * 0.42, r * 0.1, P("#1E293B", alpha))


def header(c, ep_no, total_eps, progress, alpha=1.0, module=None):
    if alpha <= 0:
        return
    y = 150
    # sol: marka
    nm1, nm2 = BRAND.line1, BRAND.line2
    w1 = max(text_width(nm1, 30, "black"), text_width(nm2, 21, "semi")) + 130
    glass(c, 40, y - 48, w1, 96, 48, alpha=0.42 * alpha, blur=22)
    brand_badge(c, 88, y, 34, alpha)
    draw_text(c, nm1, 136, y - 4, 30, "white", "black", "left", alpha)
    draw_text(c, nm2, 136, y + 26, 21, "#E2E8F0", "semi", "left", alpha * 0.9)
    # sağ: ders sayacı
    s1 = f"DERS {ep_no:02d}"
    s2 = f"/{total_eps}"
    tw = text_width(s1, 34, "black") + text_width(s2, 24, "semi") + 56
    glass(c, W - 40 - tw, y - 40, tw, 80, 40, alpha=0.42 * alpha, blur=22)
    draw_text(c, s1, W - 40 - tw + 28, y + 12, 34, "white", "black", "left", alpha)
    draw_text(c, s2, W - 40 - 28, y + 11, 24, "#FFB020", "bold", "right", alpha)
    # ilerleme çubuğu
    by = 228
    rrect(c, 60, by, W - 120, 7, 4, P("#FFFFFF", 0.22 * alpha))
    pw = (W - 120) * clamp(progress)
    if pw > 2:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(60, by, pw, 7), 4, 4),
                    skia.Paint(AntiAlias=True, Shader=lin((60, 0), (W - 60, 0), [C("#FFB020", alpha), C("#FF6A1A", alpha), C("#F43F5E", alpha)])))
        c.drawCircle(60 + pw, by + 3.5, 8, P("#FFFFFF", alpha))


def kicker(c, items, t_in, t_out, now, y=360, gap=22):
    """Ekran yazıları. items: ['BAŞLIK', ('ETİKET','red'), ...]."""
    if not items:
        return
    out = smooth(remap(now, t_out - 0.22, t_out)) if t_out is not None else 0.0
    cy = y
    for i, it in enumerate(items):
        t0 = t_in + 0.08 + i * 0.22
        a = ease_out(remap(now, t0, t0 + 0.35))
        if a <= 0:
            break
        sc = 0.86 + 0.14 * ease_back(remap(now, t0, t0 + 0.45))
        dy = (1 - a) * 46 - out * 20
        alpha = a * (1 - out)
        if isinstance(it, str):
            size = 96 if len(it) <= 12 else (80 if len(it) <= 18 else 66)
            lines = wrap(it, size, 960, "black")
            for ln in lines:
                c.save()
                c.translate(540, cy + size * 0.5 + dy)
                c.scale(sc, sc)
                draw_text(c, ln, 0, size * 0.36, size, "white", "black", "center", alpha,
                          shadow=(0, 6, 0.45, 14))
                c.restore()
                cy += size * 1.05
            cy += gap * 0.4
        else:
            txt, col = it[0], it[1]
            bg, fg = KICK_COLORS.get(col, (col, "white"))
            size = 50 if len(txt) <= 22 else 42
            c.save()
            c.translate(540, cy + 44 + dy)
            c.scale(sc, sc)
            chip(c, txt, 0, 0, size, bg, fg, alpha=alpha, weight="black", pad=(34, 20))
            c.restore()
            cy += 88 + size * 0.4 + gap


def _chunks(text, size=50, maxw=900, max_lines=2):
    lines = wrap(text, size, maxw, "bold")
    out = []
    for i in range(0, len(lines), max_lines):
        out.append(lines[i:i + max_lines])
    return out


def subtitles(c, text, t0, t1, now, y=1500):
    """Kelime kelime vurgulanan altyazı."""
    if not text or now < t0 - 0.05 or now > t1 + 0.25:
        return
    size = 48
    chunks = _chunks(text, size)
    lens = [sum(len(l) for l in ch) for ch in chunks]
    total = sum(lens)
    dur = max(0.1, t1 - t0)
    # hangi parça
    acc = 0
    prog = clamp((now - t0) / dur)
    ci = 0
    for i, L in enumerate(lens):
        if prog * total <= acc + L or i == len(lens) - 1:
            ci = i
            break
        acc += L
    ch = chunks[ci]
    local = clamp((prog * total - acc) / max(1, lens[ci]))
    cs = t0 + dur * acc / total
    a_in = ease_out(remap(now, cs - 0.02, cs + 0.18))
    a_out = 1 - smooth(remap(now, t1 + 0.05, t1 + 0.25))
    alpha = a_in * a_out
    if alpha <= 0:
        return
    lh = size * 1.32
    boxw = max(text_width(l, size, "bold") for l in ch) + 70
    boxh = lh * len(ch) + 44
    bx, by = 540 - boxw / 2, y - boxh / 2 + (1 - a_in) * 16
    glass(c, bx, by, boxw, boxh, 30, alpha=0.6 * alpha, blur=24, border=0.12)
    # kelime vurgusu
    words_total = sum(len(l) for l in ch)
    spoken = local * words_total
    k = 0
    for li, ln in enumerate(ch):
        lw = text_width(ln, size, "bold")
        x = 540 - lw / 2
        yy = by + 22 + lh * li + size * 1.0
        words = ln.split(" ")
        for wi, wd in enumerate(words):
            seg = wd + (" " if wi < len(words) - 1 else "")
            ww = text_width(seg, size, "bold")
            w_start, w_end = k, k + len(wd)
            if spoken >= w_end:
                col, a = "white", 1.0
            elif spoken >= w_start:
                col, a = "#FFD23F", 1.0
            else:
                col, a = "white", 0.62
            draw_text(c, wd, x, yy, size, col, "bold", "left", alpha * a)
            x += ww
            k += len(seg)


def vignette(c, strength=0.35):
    def draw(cv):
        cv.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=rad((540, 900), 1250, [C("#000000", 0.0), C("#000000", strength)], [0.55, 1.0])))
        cv.drawRect(skia.Rect.MakeXYWH(0, 0, W, 320), skia.Paint(Shader=lin((0, 0), (0, 320), [C("#000000", 0.38), C("#000000", 0.0)])))
        cv.drawRect(skia.Rect.MakeXYWH(0, 1380, W, 540), skia.Paint(Shader=lin((0, 1380), (0, H), [C("#000000", 0.0), C("#000000", 0.42)])))
    c.drawImage(cached(("vignette", round(strength, 2)), W, H, draw), 0, 0)
