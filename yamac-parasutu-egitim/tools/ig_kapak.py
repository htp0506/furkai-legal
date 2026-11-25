"""Instagram için kapaklı video sürümleri üretir.

Instagram, API ile paylaşılan Reels'te kapak olarak videonun ilk karesini kullanır.
Bu araç her ders için ders numarası ve başlığı büyük yazan bir kapak çizer, videonun
başına tek kare olarak ekler ve sonucu videolar_ig/ klasörüne yazar.

Kullanım: python tools/ig_kapak.py [ders numaraları]   (boşsa 1-51)
"""
import importlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import skia  # noqa: E402
from engine.gfx import W, H, C, P, draw_text, wrap, chip, lin, tr_upper  # noqa: E402
from engine.ui import brand_badge  # noqa: E402
from episodes import SERIES  # noqa: E402
from episodes.instagram import module_of, TOTAL  # noqa: E402

SRC = os.path.join(ROOT, "videolar")
OUT = os.path.join(ROOT, "videolar_ig")


def video_path(no):
    return next(os.path.join(SRC, f) for f in sorted(os.listdir(SRC)) if f.startswith(f"{no:02d}_") and f.endswith(".mp4"))


def cover(no, bg_png, out_png):
    e = next(x for x in SERIES if x["no"] == no)
    ep = importlib.import_module(f"episodes.{e['module']}").EP
    mi, mname = module_of(no)
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    bg = skia.Image.open(bg_png)
    c.drawImageRect(bg, skia.Rect.MakeWH(W, H), skia.SamplingOptions(skia.FilterMode.kLinear))
    # okunurluk için koyulaştırma (ızgara kırpması: y 240-1680)
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=lin((0, 0), (0, H), [
        C("#06121F", 0.55), C("#06121F", 0.30), C("#06121F", 0.45), C("#06121F", 0.80)], [0.0, 0.35, 0.6, 1.0])))
    # kulüp rozeti ve ders numarası
    brand_badge(c, W / 2, 430, 78)
    chip(c, f"DERS {no:02d}", W / 2, 610, 70, "#FF6A1A", "white", weight="black", pad=(44, 22))
    # başlık
    title = tr_upper(ep["title"].replace("\n", " "))
    size = 150 if len(title) <= 10 else (124 if len(title) <= 16 else 104)
    lines = wrap(title, size, 960, "black")
    while len(lines) > 3 and size > 70:
        size -= 10
        lines = wrap(title, size, 960, "black")
    lh = size * 1.02
    block = lh * len(lines)
    y0 = 1010 - block / 2 + size * 0.78
    for i, ln in enumerate(lines):
        draw_text(c, ln, W / 2, y0 + i * lh, size, "white", "black", "center", shadow=(0, 8, 0.55, 18))
    sub = ep.get("subtitle")
    ysub = y0 + (len(lines) - 1) * lh + size * 0.55 + 70
    if sub:
        chip(c, tr_upper(sub), W / 2, ysub, 50, "#FFD23F", "#1F1300", weight="black", pad=(34, 18))
    # modül
    chip(c, f"MODÜL {mi} · {tr_upper(mname)}", W / 2, 1520, 40, "glass", "white", weight="xbold", pad=(32, 18))
    # ızgarada kırpılan alt şerit: seri bilgisi
    draw_text(c, f"YAMAÇ PARAŞÜTÜ EĞİTİM SETİ · {no}/{TOTAL}", W / 2, 1790, 34, "#E2E8F0", "bold", "center",
              shadow=(0, 3, 0.6, 8))
    surf.makeImageSnapshot().save(out_png, skia.kPNG)


def build(no):
    os.makedirs(OUT, exist_ok=True)
    src = video_path(no)
    tmp = os.path.join(OUT, f".kapak_{no:02d}")
    os.makedirs(tmp, exist_ok=True)
    bg = os.path.join(tmp, "bg.png")
    png = os.path.join(tmp, "kapak.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-i", src, "-frames:v", "1", bg], check=True)
    cover(no, bg, png)
    out = os.path.join(OUT, os.path.basename(src))
    one = "0.0333333"
    subprocess.run([
        "ffmpeg", "-v", "error", "-y",
        "-loop", "1", "-framerate", "30", "-t", one, "-i", png,
        "-f", "lavfi", "-t", one, "-i", "anullsrc=r=48000:cl=stereo",
        "-i", src,
        "-filter_complex",
        "[0:v]scale=1080:1920,format=yuv420p,setsar=1[cv];[2:v]setsar=1[ov];[cv][1:a][ov][2:a]concat=n=2:v=1:a=1[v][a]",
        "-map", "[v]", "-map", "[a]", "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    return out, png


if __name__ == "__main__":
    nos = [int(a) for a in sys.argv[1:]] or list(range(1, TOTAL + 1))
    for n in nos:
        o, _ = build(n)
        print("hazır:", o, flush=True)
