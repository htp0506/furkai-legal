"""Profil ızgarasının üst sırası: TEK bir afiş, 3 parçaya bölünmüş.

Ana tuval 3240x1920. Her parça 1080x1920 (9:16). Profil ızgarası her gönderinin
ortadaki 1080x1440 (3:4) kısmını gösterir; bu yüzden asıl tasarım y=240..1680
bandındadır ve üç parça yan yana kusursuz birleşir.

Paylaşım sırası: önce SAĞ, sonra ORTA, en son SOL (en yeni gönderi solda durur).

Kullanım: python tools/ig_banner_tek.py
"""
import math
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import skia  # noqa: E402
from PIL import Image as PILImage  # noqa: E402
from engine.gfx import C, P, draw_text, text_width, lin, rad  # noqa: E402

TW, TH = 1080, 1920
BW = TW * 3
G0, G1 = 240, 1680          # ızgarada görünen bant
OUT = os.path.join(ROOT, "instagram_profil", "afis_tek")
LOGOS = os.path.join(ROOT, "instagram_profil", "logolar")
CLUB_LOGO = os.path.join(ROOT, "assets", "brand", "logo.jpg")


def mountains(c, base_y, amp, color, seed):
    rnd = random.Random(seed)
    pts, x = [], -40
    while x <= BW + 200:
        pts.append((x, base_y - amp * (0.35 + 0.65 * rnd.random())))
        x += rnd.randint(160, 340)
    path = skia.Path()
    path.moveTo(-40, TH)
    path.lineTo(*pts[0])
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        path.quadTo(x0 + (x1 - x0) * 0.5, min(y0, y1) - 25, x1, y1)
    path.lineTo(BW + 200, TH)
    path.close()
    c.drawPath(path, P(color))


def paraglider(c, x, y, s, tilt=-8):
    c.save()
    c.translate(x, y)
    c.rotate(tilt)
    c.scale(s, s)
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
    for fx in (-0.42, -0.2, 0.0, 0.2, 0.42):
        c.drawLine(fx * w, -h / 2 + 34 + abs(fx) * 40, 0, 210, P("#E2E8F0", 0.75, stroke=2))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-16, 205, 32, 46), 12, 12), P("#0F172A"))
    c.drawCircle(0, 198, 12, P("#F8FAFC"))
    c.restore()


def logo_disc(c, cx, cy, r, path):
    c.drawCircle(cx, cy + 8, r + 6, P("#000000", 0.4, blur=18))
    c.drawCircle(cx, cy, r + 6, P("#FFFFFF"))
    img = skia.Image.open(path)
    px = PILImage.open(path).convert("RGBA").getpixel((2, 2))
    c.save()
    clip = skia.Path()
    clip.addCircle(cx, cy, r)
    c.clipPath(clip, skia.ClipOp.kIntersect, True)
    iw, ih = img.width(), img.height()
    if path == CLUB_LOGO:
        k = 2 * r / min(iw, ih)
    elif px[3] > 200 and sum(px[:3]) < 600:      # renkli kare logo
        c.drawCircle(cx, cy, r, P("#%02X%02X%02X" % px[:3]))
        k = min(2 * r * 0.74 / iw, 2 * r * 0.74 / ih)
    else:
        k = min(2 * r * 0.9 / iw, 2 * r * 0.9 / ih)
    dw, dh = iw * k, ih * k
    c.drawImageRect(img, skia.Rect.MakeXYWH(cx - dw / 2, cy - dh / 2, dw, dh),
                    skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    c.restore()
    c.drawCircle(cx, cy, r + 6, P("#FF8A3D", 1.0, stroke=7))


def centered_two_color(c, parts, cy, size, weight="black"):
    """[(metin, renk), ...] parçalarını tek satırda ortalar."""
    widths = [text_width(t, size, weight) for t, _ in parts]
    x = BW / 2 - sum(widths) / 2
    for (t, col), w in zip(parts, widths):
        draw_text(c, t, x, cy, size, col, weight, "left", shadow=(0, 10, 0.5, 22))
        x += w


def draw(c):
    # gökyüzü
    c.drawRect(skia.Rect.MakeWH(BW, TH), skia.Paint(Shader=lin((0, 0), (0, TH), [
        C("#050F1C"), C("#0B2647"), C("#1D5694"), C("#F0874A"), C("#F6B26B")], [0.0, 0.3, 0.6, 0.86, 1.0])))
    c.drawRect(skia.Rect.MakeWH(BW, TH), skia.Paint(Shader=rad((BW * 0.5, G1 - 80), 1700, [
        C("#FFD08A", 0.5), C("#FF8A3D", 0.15), C("#FF8A3D", 0.0)], [0.0, 0.4, 1.0])))
    rnd = random.Random(5)
    for _ in range(260):
        x, y = rnd.uniform(0, BW), rnd.uniform(0, TH * 0.42)
        c.drawCircle(x, y, rnd.uniform(0.8, 2.4), P("#FFFFFF", rnd.uniform(0.15, 0.6)))
    mountains(c, 1560, 300, "#123150", 3)
    mountains(c, 1660, 220, "#0B2138", 11)
    mountains(c, 1760, 150, "#06121F", 21)
    paraglider(c, 2830, 500, 1.15, -12)

    # logolar: federasyon (en başta), THK, kulüp
    ly, lr = G0 + 190, 112
    logos = [os.path.join(LOGOS, "federasyon.png"), os.path.join(LOGOS, "thk.png"), CLUB_LOGO]
    for i, p in enumerate(logos):
        logo_disc(c, 180 + i * 270, ly, lr, p)
    draw_text(c, "DERİN YAMAÇ SPOR KULÜBÜ", TW + 70, ly - 6, 64, "white", "black", "left", shadow=(0, 4, 0.6, 10))
    draw_text(c, "Merzifon · Amasya  ·  2010'dan beri", TW + 70, ly + 60, 44, "#E2E8F0", "bold", "left", shadow=(0, 3, 0.6, 8))

    # başlık: tek satır üç parçaya yayılır
    centered_two_color(c, [("YAMAÇ PARAŞÜTÜ", "white")], G0 + 640, 290)
    centered_two_color(c, [("P2 ", "#FF8A3D"), ("PİLOT EĞİTİMİ", "white")], G0 + 960, 290)

    # şerit
    by = G0 + 1050
    c.drawRect(skia.Rect.MakeXYWH(0, by, BW, 130), skia.Paint(Shader=lin((0, 0), (BW, 0), [
        C("#FF6A1A", 0.96), C("#F43F5E", 0.96), C("#FF6A1A", 0.96)])))
    # ince yazılar parça sınırına denk gelmesin: her parçanın ortasına
    for i, t in enumerate(["51 DERS", "TEMELDEN P2 SEVİYESİNE", "DERS 1'DEN BAŞLA  ↓"]):
        draw_text(c, t, TW * i + TW / 2, by + 90, 70, "white", "black", "center")
    for i, t in enumerate(["Kaydet", "@derinyamacsporkulubu", "Takip et"]):
        draw_text(c, t, TW * i + TW / 2, by + 250, 52, "#F1F5F9", "bold", "center", shadow=(0, 3, 0.6, 8))


def main():
    os.makedirs(OUT, exist_ok=True)
    surf = skia.Surface(BW, TH)
    draw(surf.getCanvas())
    full = surf.makeImageSnapshot()
    full.save(os.path.join(OUT, "afis_tam.png"), skia.kPNG)
    for i, n in enumerate(["1_sol", "2_orta", "3_sag"]):
        full.makeSubset(skia.IRect.MakeXYWH(TW * i, 0, TW, TH)).save(os.path.join(OUT, n + ".png"), skia.kPNG)
        print("hazır:", n)


if __name__ == "__main__":
    main()
