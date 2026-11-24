"""Tüm senaryoları ve Instagram paylaşım metinlerini Markdown olarak dışa aktar.

Kullanım: python tools/export_docs.py
"""
import importlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from episodes import SERIES, MODULES  # noqa: E402
from episodes.instagram import caption  # noqa: E402

def load(no):
    e = [x for x in SERIES if x["no"] == no][0]
    return e, importlib.import_module(f"episodes.{e['module']}").EP


def kick_text(k):
    out = []
    for it in k or []:
        out.append(it if isinstance(it, str) else it[0])
    return " · ".join(out)


def duration(no, ep):
    meta = os.path.join(ROOT, "videolar", f".tmp_{no:02d}", "meta.json")
    if os.path.exists(meta):
        with open(meta) as f:
            return json.load(f)["duration"]
    return None


def main():
    md = ["# Yamaç Paraşütü Eğitim Seti · Senaryolar ve Paylaşım Metinleri", "",
          "Bu dosya `tools/export_docs.py` ile senaryo kaynaklarından (`episodes/`) otomatik üretilir.", ""]
    md.append("## İçindekiler\n")
    cur = None
    for e in SERIES:
        mod = MODULES[e["no"]]
        if mod != cur:
            md.append(f"\n**{mod}**\n")
            cur = mod
        md.append(f"- [Ders {e['no']:02d} · {e['title']}](#ders-{e['no']:02d})")
    for e in SERIES:
        no = e["no"]
        _, ep = load(no)
        d = duration(no, ep)
        md += ["", "---", "", f"<a id=\"ders-{no:02d}\"></a>", f"## Ders {no:02d} · {e['title']}", "",
               f"*{MODULES[no]}* · Ekranda: **{ep['title'].replace(chr(10), ' ')}** / {ep.get('subtitle', '')}"
               + (f" · Süre: **{d:.0f} sn**" if d else ""), "",
               "| # | Sahne | Seslendirme (altyazı) | Ekran yazısı |", "|---|---|---|---|"]
        scene = None
        for i, b in enumerate(ep["beats"], 1):
            scene = b.get("scene", scene)
            sub = b.get("sub", b["say"]).replace("|", "/")
            md.append(f"| {i} | {scene} | {sub} | {kick_text(b.get('k'))} |")
        md += ["", "**Instagram açıklaması:**", "", "```text", caption(no), "```"]
    out = os.path.join(ROOT, "SENARYOLAR.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("yazıldı:", out)
    ig = ["# Instagram Açıklamaları · Ders 1-51", "",
          "Her dersin açıklaması ve hashtag'leri ayrı kutuda. Kutunun sağ üstündeki kopyala simgesiyle al, Instagram'a yapıştır.",
          "Her gönderide 5 hashtag var (Instagram'ın yeni sınırı).", ""]
    for e in SERIES:
        ig += [f"## Ders {e['no']:02d} · {e['title']}", "", "```text", caption(e["no"]), "```", ""]
    out2 = os.path.join(ROOT, "INSTAGRAM_ACIKLAMALAR.md")
    with open(out2, "w", encoding="utf-8") as f:
        f.write("\n".join(ig))
    print("yazıldı:", out2)


if __name__ == "__main__":
    main()
