"""Çizim yardımcıları: renkler, fontlar, metin, şekiller, oklar, easing."""
import math
import skia

W, H = 1080, 1920
FPS = 30

# ---------------------------------------------------------------- palet
PAL = {
    "ink": "#0B1220",
    "navy": "#14213D",
    "white": "#FFFFFF",
    "orange": "#FF6A1A",
    "amber": "#FFB020",
    "yellow": "#FFD23F",
    "cyan": "#22D3EE",
    "sky": "#38BDF8",
    "green": "#22C55E",
    "mint": "#34D399",
    "red": "#F43F5E",
    "violet": "#8B5CF6",
    "gray": "#94A3B8",
}


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def C(color, a=1.0):
    """Renk -> skia int rengi. color: '#RRGGBB', palet adı ya da (r,g,b)."""
    if isinstance(color, str):
        color = PAL.get(color, color)
        r, g, b = hexrgb(color)
    else:
        r, g, b = color[:3]
    a = max(0.0, min(1.0, a))
    return skia.ColorSetARGB(int(a * 255), int(r), int(g), int(b))


def mix(c1, c2, t):
    a = hexrgb(PAL.get(c1, c1)) if isinstance(c1, str) else c1
    b = hexrgb(PAL.get(c2, c2)) if isinstance(c2, str) else c2
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def shade(color, k):
    r, g, b = hexrgb(PAL.get(color, color)) if isinstance(color, str) else color
    if k >= 1:
        return tuple(int(v + (255 - v) * (k - 1)) for v in (r, g, b))
    return tuple(int(v * k) for v in (r, g, b))


# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def remap(x, a, b):
    """x'i [a,b] aralığından [0,1]'e sıkıştır."""
    if b == a:
        return 1.0 if x >= b else 0.0
    return clamp((x - a) / (b - a))


def smooth(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in(t):
    t = clamp(t)
    return t ** 3


def ease_io(t):
    t = clamp(t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def ease_back(t, s=1.7):
    t = clamp(t)
    t -= 1
    return t * t * ((s + 1) * t + s) + 1


def spring(t, freq=4.5, damp=5.0):
    if t <= 0:
        return 0.0
    return 1 - math.exp(-damp * t) * math.cos(freq * 2 * math.pi * t * 0.25)


def pulse(t, period=1.0):
    return 0.5 + 0.5 * math.sin(t * 2 * math.pi / period)


# ---------------------------------------------------------------- fontlar
_FONT_FILES = {
    "black": "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf",
    "xbold": "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf",
    "bold": "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf",
    "semi": "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf",
    "medium": "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf",
    "regular": "/usr/share/fonts/opentype/inter/InterDisplay-Regular.otf",
    "light": "/usr/share/fonts/opentype/inter/InterDisplay-Light.otf",
}
_TF = {}
_EMOJI_TF = None
_FONT_CACHE = {}


def typeface(weight):
    if weight not in _TF:
        _TF[weight] = skia.Typeface.MakeFromFile(_FONT_FILES[weight])
    return _TF[weight]


def emoji_tf():
    global _EMOJI_TF
    if _EMOJI_TF is None:
        _EMOJI_TF = skia.Typeface.MakeFromFile("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf")
    return _EMOJI_TF


def font(size, weight="bold"):
    key = (round(size, 1), weight)
    f = _FONT_CACHE.get(key)
    if f is None:
        tf = emoji_tf() if weight == "emoji" else typeface(weight)
        f = skia.Font(tf, size)
        f.setEdging(skia.Font.Edging.kAntiAlias)
        f.setSubpixel(True)
        _FONT_CACHE[key] = f
    return f


def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


def _is_emoji(ch):
    o = ord(ch)
    return (0x1F000 <= o <= 0x1FAFF) or (0x2600 <= o <= 0x27BF) or (0x2B00 <= o <= 0x2BFF) or o in (0x2194, 0x2195, 0x21A9, 0x2934, 0x2935, 0x23F1, 0x23F0, 0x231A)


def _runs(s):
    """Metni emoji / normal parçalara böl."""
    runs = []
    cur, cur_e = "", None
    for ch in s:
        if ord(ch) in (0xFE0F, 0x200D):
            if cur_e:
                cur += ch
            continue
        e = _is_emoji(ch)
        if cur_e is None or e == cur_e:
            cur += ch
            cur_e = e
        else:
            runs.append((cur, cur_e))
            cur, cur_e = ch, e
    if cur:
        runs.append((cur, cur_e))
    return runs


def text_width(s, size, weight="bold", tracking=0.0):
    w = 0.0
    for r, e in _runs(s):
        if e:
            w += font(size * 0.9, "emoji").measureText(r.replace("️", ""))
        else:
            w += font(size, weight).measureText(r) + tracking * size * len(r)
    return w


def draw_text(c, s, x, y, size, color="white", weight="bold", align="center", alpha=1.0,
              tracking=0.0, shadow=None, stroke=None):
    """y = metnin taban çizgisi (baseline)."""
    if alpha <= 0.003 or not s:
        return 0
    w = text_width(s, size, weight, tracking)
    if align == "center":
        x0 = x - w / 2
    elif align == "right":
        x0 = x - w
    else:
        x0 = x
    p = skia.Paint(AntiAlias=True, Color=C(color, alpha) if not isinstance(color, int) else color)
    if shadow:
        sp = skia.Paint(AntiAlias=True, Color=C("#000000", shadow[2] * alpha),
                        MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, shadow[3] if len(shadow) > 3 else 8))
    cx = x0
    for r, e in _runs(s):
        if e:
            f = font(size * 0.9, "emoji")
            txt = r.replace("️", "")
            pe = skia.Paint(AntiAlias=True, Color=C("#FFFFFF", alpha))
            c.drawString(txt, cx, y, f, pe)
            cx += f.measureText(txt)
        else:
            f = font(size, weight)
            if tracking:
                for ch in r:
                    if shadow:
                        c.drawString(ch, cx + shadow[0], y + shadow[1], f, sp)
                    if stroke:
                        st = skia.Paint(AntiAlias=True, Color=C(stroke[0], alpha), Style=skia.Paint.kStroke_Style,
                                        StrokeWidth=stroke[1], StrokeJoin=skia.Paint.kRound_Join)
                        c.drawString(ch, cx, y, f, st)
                    c.drawString(ch, cx, y, f, p)
                    cx += f.measureText(ch) + tracking * size
            else:
                if shadow:
                    c.drawString(r, cx + shadow[0], y + shadow[1], f, sp)
                if stroke:
                    st = skia.Paint(AntiAlias=True, Color=C(stroke[0], alpha), Style=skia.Paint.kStroke_Style,
                                    StrokeWidth=stroke[1], StrokeJoin=skia.Paint.kRound_Join)
                    c.drawString(r, cx, y, f, st)
                c.drawString(r, cx, y, f, p)
                cx += f.measureText(r)
    return w


def wrap(s, size, maxw, weight="bold"):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if text_width(t, size, weight) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- şekiller
def P(color="white", alpha=1.0, stroke=0, blur=0, shader=None, cap="round", dash=None):
    p = skia.Paint(AntiAlias=True)
    if shader is not None:
        p.setShader(shader)
        p.setAlphaf(clamp(alpha))
    else:
        p.setColor(C(color, alpha) if not isinstance(color, int) else color)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap if cap == "round" else skia.Paint.kButt_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if dash:
        p.setPathEffect(skia.DashPathEffect.Make([float(dash[0]), float(dash[1])], float(dash[2]) if len(dash) > 2 else 0.0))
    return p


def lin(p0, p1, colors, pos=None):
    cols = [c if isinstance(c, int) else C(*c) if isinstance(c, tuple) and len(c) == 2 and isinstance(c[1], float) else C(c) for c in colors]
    return skia.GradientShader.MakeLinear([skia.Point(*p0), skia.Point(*p1)], cols, pos)


def rad(center, r, colors, pos=None):
    cols = [c if isinstance(c, int) else C(c) for c in colors]
    return skia.GradientShader.MakeRadial(skia.Point(*center), r, cols, pos)


def rrect(c, x, y, w, h, r, paint):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), paint)


def circle(c, x, y, r, paint):
    c.drawCircle(x, y, r, paint)


def poly(pts, close=True):
    path = skia.Path()
    if not pts:
        return path
    path.moveTo(*pts[0])
    for p in pts[1:]:
        path.lineTo(*p)
    if close:
        path.close()
    return path


def smooth_path(pts, close=False, tension=0.5):
    """Catmull-Rom -> kübik Bezier."""
    path = skia.Path()
    n = len(pts)
    if n < 2:
        return path
    path.moveTo(*pts[0])
    if n == 2:
        path.lineTo(*pts[1])
        return path
    P_ = list(pts)
    if close:
        P_ = [pts[-1]] + list(pts) + [pts[0], pts[1]]
    else:
        P_ = [pts[0]] + list(pts) + [pts[-1]]
    rng = range(1, len(P_) - 2)
    for i in rng:
        p0, p1, p2, p3 = P_[i - 1], P_[i], P_[i + 1], P_[i + 2]
        k = tension / 3 * 2
        c1 = (p1[0] + (p2[0] - p0[0]) * k / 2, p1[1] + (p2[1] - p0[1]) * k / 2)
        c2 = (p2[0] - (p3[0] - p1[0]) * k / 2, p2[1] - (p3[1] - p1[1]) * k / 2)
        path.cubicTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    if close:
        path.close()
    return path


def trim_path(path, t0, t1):
    """Yolun [t0,t1] kesitini döndür (0..1)."""
    if t1 <= t0:
        return skia.Path(), None
    meas = skia.PathMeasure(path, False)
    L = meas.getLength()
    out = skia.Path()
    meas.getSegment(L * t0, L * t1, out, True)
    pos, tan = meas.getPosTan(L * t1)
    return out, (pos, tan)


def arrow(c, path, color="white", width=10, progress=1.0, alpha=1.0, head=26, start=0.0, glow=False):
    if progress <= start + 0.001 or alpha <= 0:
        return
    seg, end = trim_path(path, start, progress)
    if glow:
        c.drawPath(seg, P(color, alpha * 0.35, stroke=width * 2.2, blur=width))
    c.drawPath(seg, P(color, alpha, stroke=width))
    if head and end and end[0] is not None:
        (px, py), (tx, ty) = (end[0].x(), end[0].y()), (end[1].x(), end[1].y())
        ang = math.atan2(ty, tx)
        hs = head
        pts = [
            (px + math.cos(ang) * hs * 0.55, py + math.sin(ang) * hs * 0.55),
            (px + math.cos(ang + 2.5) * hs, py + math.sin(ang + 2.5) * hs),
            (px + math.cos(ang - 2.5) * hs, py + math.sin(ang - 2.5) * hs),
        ]
        c.drawPath(poly(pts), P(color, alpha))


def line_arrow(c, x0, y0, x1, y1, **kw):
    path = skia.Path()
    path.moveTo(x0, y0)
    path.lineTo(x1, y1)
    arrow(c, path, **kw)


_BLUR = {}


def glass(c, x, y, w, h, r, tint="#0B1220", alpha=0.55, blur=28, border=0.18, use_blur=False):
    rect = skia.Rect.MakeXYWH(x, y, w, h)
    rr = skia.RRect.MakeRectXY(rect, r, r)
    if not use_blur:
        alpha = min(0.92, alpha * 1.18 + 0.04) if blur else alpha
        blur = 0
    if blur:
        bf = _BLUR.get(blur)
        if bf is None:
            bf = _BLUR[blur] = skia.ImageFilters.Blur(blur, blur, skia.TileMode.kClamp)
        rec = skia.Canvas.SaveLayerRec(rect, None, bf, 0)
        c.save()
        c.clipRRect(rr, skia.ClipOp.kIntersect, True)
        c.saveLayer(rec)
        c.restore()
        c.restore()
    c.drawRRect(rr, P(tint, alpha))
    if border:
        c.drawRRect(rr, P("#FFFFFF", border, stroke=2))


def chip(c, s, x, y, size=44, bg="orange", fg="white", align="center", alpha=1.0, scale=1.0,
         weight="xbold", pad=(30, 18), radius=None, shadow=True, outline=None):
    """Hap şeklinde etiket. (x,y) = kutunun merkezi (align=center) ya da sol-orta."""
    if alpha <= 0.003:
        return (0, 0)
    size *= scale
    tw = text_width(s, size, weight)
    w, h = tw + pad[0] * 2 * scale, size + pad[1] * 2 * scale
    x0 = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    y0 = y - h / 2
    r = radius * scale if radius is not None else h / 2
    if shadow:
        rrect(c, x0, y0 + 10 * scale, w, h, r, P("#000000", 0.25 * alpha, blur=16))
    if isinstance(bg, str) and bg.startswith("glass"):
        glass(c, x0, y0, w, h, r, alpha=0.55 * alpha)
    else:
        rrect(c, x0, y0, w, h, r, P(bg, alpha))
    if outline:
        rrect(c, x0, y0, w, h, r, P(outline, alpha, stroke=3))
    draw_text(c, s, x0 + w / 2, y0 + h / 2 + size * 0.36, size, fg, weight, "center", alpha)
    return (w, h)


def icon_check(c, x, y, r, color="green", alpha=1.0, progress=1.0):
    circle(c, x, y, r, P(color, alpha))
    path = skia.Path()
    path.moveTo(x - r * 0.45, y + r * 0.02)
    path.lineTo(x - r * 0.12, y + r * 0.35)
    path.lineTo(x + r * 0.48, y - r * 0.32)
    seg, _ = trim_path(path, 0, max(0.001, progress))
    c.drawPath(seg, P("white", alpha, stroke=r * 0.22))


def icon_cross(c, x, y, r, color="red", alpha=1.0, progress=1.0):
    circle(c, x, y, r, P(color, alpha))
    k = r * 0.38
    pr = clamp(progress * 2)
    c.drawLine(x - k, y - k, x - k + 2 * k * pr, y - k + 2 * k * pr, P("white", alpha, stroke=r * 0.22))
    pr2 = clamp(progress * 2 - 1)
    if pr2 > 0:
        c.drawLine(x + k, y - k, x + k - 2 * k * pr2, y - k + 2 * k * pr2, P("white", alpha, stroke=r * 0.22))


def icon_warn(c, x, y, r, color="amber", alpha=1.0):
    pts = [(x, y - r), (x + r * 1.05, y + r * 0.8), (x - r * 1.05, y + r * 0.8)]
    c.drawPath(smooth_path(pts + [pts[0]], close=False, tension=0.0), P(color, alpha))
    c.drawPath(poly(pts), P(color, alpha))
    c.drawPath(poly(pts), P(color, alpha, stroke=r * 0.25))
    c.drawLine(x, y - r * 0.35, x, y + r * 0.25, P("#1F1300", alpha, stroke=r * 0.18))
    circle(c, x, y + r * 0.52, r * 0.1, P("#1F1300", alpha))


def angle_arc(c, cx, cy, r, a0, a1, color="yellow", width=6, alpha=1.0):
    """a0,a1 derece (skia: 0=sağ, saat yönü pozitif)."""
    rect = skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r)
    path = skia.Path()
    path.addArc(rect, a0, a1 - a0)
    c.drawPath(path, P(color, alpha, stroke=width))


_IMG_CACHE = {}


def cached(key, w, h, draw_fn):
    """Statik katmanı bir kez çizip görüntü olarak sakla."""
    img = _IMG_CACHE.get(key)
    if img is None:
        surf = skia.Surface(int(w), int(h))
        cv = surf.getCanvas()
        cv.clear(skia.ColorTRANSPARENT)
        draw_fn(cv)
        img = surf.makeImageSnapshot()
        if len(_IMG_CACHE) > 120:
            _IMG_CACHE.clear()
        _IMG_CACHE[key] = img
    return img


SAMPLING = skia.SamplingOptions(skia.FilterMode.kLinear)
