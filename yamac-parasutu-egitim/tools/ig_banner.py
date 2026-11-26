"""Instagram profil ızgarasının en üst sırası için 3 parçalı afiş.

3 görsel yan yana tek bir afiş gibi görünür (her biri 1080x1350, 4:5).
Ayrı ayrı paylaşılır: önce SAĞ, sonra ORTA, en son SOL (en yeni gönderi solda durur).

Logolar: instagram_profil/logolar/ klasörüne
  federasyon.png (sol), kulup.(png|jpg) (orta), thk.png (sağ)
koyulursa kullanılır; yoksa yerine "LOGO" yazan boş daire çizilir.

Kullanım: python tools/ig_banner.py
"""
import math
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import skia  # noqa: E402
from engine.gfx import C, P, draw_text, lin, rad, chip  # noqa: E402

TW, TH = 1080, 1350          # bir parça
BW = TW * 3                  # tüm afiş
OUT = os.path.join(ROOT, "instagram_profil", "afis")
LOGOS = os.path.join(ROOT, "instagram_profil", "logolar")


def find_logo(name):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(LOGOS, name + ext)
        if os.path.exists(p):
            return p
    if name == "kulup":
        p = os.path.join(ROOT, "assets", "brand", "logo.jpg")
        if os.path.exists(p):
            return p
    return None


def mountains(c, base_y, amp, color, seed, alpha=1.0):
    rnd = random.Random(seed)
    path = skia.Path()
    path.moveTo(0, TH)
    x = 0
    pts = []
    while x <= BW + 40:
        pts.append((x, base_y - amp * (0.35 + 0.65 * rnd.random())))
        x += rnd.randint(140, 320)
    path.lineTo(0, pts[0][1])
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        mx = (x0 + x1) / 2
        path.quadTo(x0 + (x1 - x0) * 0.25, y0 - 30, mx, (y0 + y1) / 2)
        path.quadTo(x1 - (x1 - x0) * 0.25, y1 + 20, x1, y1)
    path.lineTo(BW, TH)
    path.close()
    c.drawPath(path, P(color, alpha))


def paraglider(c, x, y, s, tilt=-8):
    c.save()
    c.translate(x, y)
    c.rotate(tilt)
    c.scale(s, s)
    # kanat
    w, h = 300, 70
    path = skia.Path()
    path.addArc(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h * 2), 200, 140)
    path.arcTo(skia.Rect.MakeXYWH(-w / 2 + 18, -h / 2 + 26, w - 36, h * 2 - 30), 340, -140, False)
    path.close()
    c.drawPath(path, skia.Paint(AntiAlias=True, Shader=lin((-w / 2, 0), (w / 2, 0), [C("#FFB020"), C("#FF6A1A"), C("#E11D48")])))
    for i in range(1, 9):
        a = math.radians(200 + i * 140 / 9)
        x0, y0 = math.cos(a) * w / 2, -h / 2 + h + math.sin(a) * h
        c.drawLine(x0, y0, x0 * 0.94, y0 + 22, P("#7C2D12", 0.45, stroke=3))
    # ipler ve pilot
    for fx in (-0.42, -0.2, 0.0, 0.2, 0.42):
        c.drawLine(fx * w, -h / 2 + 34 + abs(fx) * 40, 0, 210, P("#E2E8F0", 0.75, stroke=2))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-16, 205, 32, 46), 12, 12), P("#0F172A"))
    c.drawCircle(0, 198, 12, P("#F8FAFC"))
    c.restore()


def background(c):
    c.drawRect(skia.Rect.MakeWH(BW, TH), skia.Paint(Shader=lin((0, 0), (0, TH), [
        C("#071526"), C("#0E2D55"), C("#1F5C99"), C("#F08A4B")], [0.0, 0.38, 0.7, 1.0])))
    # güneş parıltısı
    c.drawRect(skia.Rect.MakeWH(BW, TH), skia.Paint(Shader=rad((BW * 0.62, TH * 0.86), 1300, [
        C("#FFD08A", 0.55), C("#FF8A3D", 0.18), C("#FF8A3D", 0.0)], [0.0, 0.35, 1.0])))
    rnd = random.Random(7)
    for _ in range(140):  # yıldızlar
        x, y = rnd.uniform(0, BW), rnd.uniform(0, TH * 0.35)
        c.drawCircle(x, y, rnd.uniform(0.8, 2.2), P("#FFFFFF", rnd.uniform(0.15, 0.55)))
    mountains(c, 1130, 260, "#12304F", 3, 0.9)
    mountains(c, 1210, 190, "#0B2138", 11)
    mountains(c, 1290, 120, "#06121F", 21)
    paraglider(c, TW * 0.86, 420, 0.72, -10)
    paraglider(c, TW * 1.86, 470, 0.45, 6)


def logo_disc(c, cx, cy, r, path):
    c.drawCircle(cx, cy + 8, r + 6, P("#000000", 0.35, blur=18))
    c.drawCircle(cx, cy, r + 6, P("#FFFFFF"))
    if path:
        img = skia.Image.open(path)
        c.save()
        clip = skia.Path()
        clip.addCircle(cx, cy, r)
        c.clipPath(clip, skia.ClipOp.kIntersect, True)
        iw, ih = img.width(), img.height()
        # köşesi dolu renkli kare logolar (ör. federasyon): daireyi o renkle doldur, logoyu iç kareye sığdır
        from PIL import Image as _PIL
        px = _PIL.open(path).convert("RGBA").getpixel((2, 2))
        square_logo = px[3] > 200 and sum(px[:3]) < 600 and not path.endswith("logo.jpg")
        if square_logo:
            c.drawCircle(cx, cy, r, P("#%02X%02X%02X" % px[:3]))
            k = min(2 * r * 0.74 / iw, 2 * r * 0.74 / ih)
        elif path.endswith("logo.jpg"):
            k = 2 * r / min(iw, ih)
        else:
            k = min(2 * r * 0.9 / iw, 2 * r * 0.9 / ih)
        dw, dh = iw * k, ih * k
        c.drawImageRect(img, skia.Rect.MakeXYWH(cx - dw / 2, cy - dh / 2, dw, dh),
                        skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
        c.restore()
    else:
        c.drawCircle(cx, cy, r, P("#E2E8F0"))
        draw_text(c, "LOGO", cx, cy + 22, 64, "#64748B", "black", "center")
    c.drawCircle(cx, cy, r + 6, P("#FF8A3D", 1.0, stroke=8))


def text_shadow():
    return (0, 8, 0.5, 18)


def draw_banner(c):
    background(c)
    logo_y, logo_r = 250, 150
    # SOL: federasyon + P2
    x0 = TW * 0 + TW / 2
    logo_disc(c, x0, logo_y, logo_r, find_logo("federasyon"))
    draw_text(c, "P2", x0, 820, 440, "white", "black", "center", shadow=text_shadow())
    chip(c, "PİLOT EĞİTİMİ", x0, 930, 66, "#FF6A1A", "white", weight="black", pad=(40, 22))
    # ORTA: kulüp + 51 ders
    x1 = TW * 1 + TW / 2
    logo_disc(c, x1, logo_y, logo_r, find_logo("kulup"))
    draw_text(c, "51", x1, 790, 400, "white", "black", "center", shadow=text_shadow())
    draw_text(c, "DERS", x1, 905, 120, "#FFD23F", "black", "center", shadow=text_shadow())
    # SAĞ: THK + izle
    x2 = TW * 2 + TW / 2
    logo_disc(c, x2, logo_y, logo_r, find_logo("thk"))
    draw_text(c, "İZLE", x2, 720, 230, "white", "black", "center", shadow=text_shadow())
    draw_text(c, "ÖĞREN", x2, 880, 160, "white", "black", "center", shadow=text_shadow())
    # alt şerit: üç parçayı birbirine bağlar
    band_y = 1060
    c.drawRect(skia.Rect.MakeXYWH(0, band_y, BW, 120), skia.Paint(Shader=lin((0, 0), (BW, 0), [
        C("#FF6A1A", 0.95), C("#F43F5E", 0.95), C("#FF6A1A", 0.95)])))
    for i, t in enumerate(["YAMAÇ PARAŞÜTÜ", "DERİN YAMAÇ SPOR KULÜBÜ", "DERS 1'DEN BAŞLA  ↓"]):
        draw_text(c, t, TW * i + TW / 2, band_y + 80, 62 if i != 1 else 56, "white", "black", "center")
    for i, t in enumerate(["Temelden P2 seviyesine", "Merzifon · Amasya", "Kaydet · Takip et"]):
        draw_text(c, t, TW * i + TW / 2, 1262, 50, "#F1F5F9", "bold", "center", shadow=(0, 3, 0.6, 8))


def main():
    os.makedirs(OUT, exist_ok=True)
    surf = skia.Surface(BW, TH)
    c = surf.getCanvas()
    draw_banner(c)
    full = surf.makeImageSnapshot()
    full.save(os.path.join(OUT, "afis_tam.png"), skia.kPNG)
    names = ["1_sol.png", "2_orta.png", "3_sag.png"]
    for i, n in enumerate(names):
        part = full.makeSubset(skia.IRect.MakeXYWH(TW * i, 0, TW, TH))
        part.save(os.path.join(OUT, n), skia.kPNG)
        print("hazır:", os.path.join(OUT, n))


if __name__ == "__main__":
    main()
