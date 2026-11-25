"""Instagram profil kiti: öne çıkan (highlight) kapakları.

Kullanım: python tools/ig_profil.py  -> instagram_profil/one_cikan_*.png
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import skia  # noqa: E402
from engine.gfx import W, H, C, P, draw_text, lin, rad  # noqa: E402

OUT = os.path.join(ROOT, "instagram_profil")

# (dosya adı, emoji, öne çıkan adı, içerdiği dersler)
HIGHLIGHTS = [
    ("01_basla", "🪂", "BAŞLA", "Ders 1, 2, 3, 4"),
    ("02_hava", "🌤️", "HAVA", "Ders 5–9, 40–45"),
    ("03_kalkis", "🏃", "KALKIŞ", "Ders 10–12, 32–37"),
    ("04_ucus", "🧭", "UÇUŞ", "Ders 13–16, 25–28"),
    ("05_inis", "🎯", "İNİŞ", "Ders 17–19, 38–39"),
    ("06_acil", "⚠️", "ACİL", "Ders 20–24, 29–31"),
    ("07_ekipman", "🎒", "EKİPMAN", "Ders 2, 3, 46, 47"),
    ("08_pilot", "🎓", "PİLOT", "Ders 48–51"),
    ("09_kulup", "📍", "KULÜP", "Kulüp, iletişim, uçuş fotoğrafları"),
]


def cover(emoji, path):
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=lin((0, 0), (0, H), [C("#0B1F33"), C("#06121F")])))
    cx, cy, r = W / 2, H / 2, 400
    c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Shader=lin((cx - r, cy - r), (cx + r, cy + r),
                                                                [C("#FF8A3D"), C("#E8590C")])))
    c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Shader=rad((cx - r * 0.35, cy - r * 0.45), r * 1.2,
                                                                [C("#FFFFFF", 0.22), C("#FFFFFF", 0.0)])))
    c.drawCircle(cx, cy, r - 14, P("#FFFFFF", 0.85, stroke=10))
    draw_text(c, emoji, cx, cy + 180, 500, "white", "bold", "center")
    surf.makeImageSnapshot().save(path, skia.kPNG)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, emo, _, _ in HIGHLIGHTS:
        cover(emo, os.path.join(OUT, f"one_cikan_{name}.png"))
        print("hazır:", name)
