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

BASE_TAGS = "#yamaçparaşütü #paragliding #yamacparasutu #uçuşokulu #paraglidingturkey #merzifon #amasya #derinyamaçsporkulübü"
TOPIC_TAGS = {
    1: "#aerodinamik #nasılucar", 2: "#kanat #ekipman", 3: "#ekipman #güvenlik", 4: "#aerodinamik #hücumaçısı",
    5: "#meteoroloji #rüzgar", 6: "#meteoroloji #soaring", 7: "#termik #thermal", 8: "#rotor #türbülans",
    9: "#meteoroloji #fırtına", 10: "#güvenlik #checklist", 11: "#kalkış #launch", 12: "#terskalkış #groundhandling",
    13: "#uçuştekniği #aktifpilotaj", 14: "#uçuştekniği #dönüş", 15: "#speedbar #süzülme", 16: "#bigears #kulakkatlama",
    17: "#iniş #landing", 18: "#palya #flare #iniş", 19: "#plf #güvenlik", 20: "#kapanma #sivkursu",
    21: "#kapanma #aktifpilotaj", 22: "#stol #negatif", 23: "#yedekparaşüt #güvenlik", 24: "#havakuralları #güvenlik",
}


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


def caption(no, e, ep):
    recap = next((b["p"]["items"] for b in ep["beats"] if b.get("scene") == "recap"), [])
    q = next((b["p"]["q"] for b in ep["beats"] if b.get("scene") == "outro"), "")
    hook = ep["beats"][0].get("sub", ep["beats"][0]["say"])
    lines = [f"🪂 Ders {no:02d}/{len(SERIES)} · {e['title']}", "", hook, ""]
    for it in recap:
        lines.append(f"✅ {it}")
    lines += ["", f"💬 {q} Yorumlara yaz!", "🔖 Kaydet, uçuş arkadaşınla paylaş.",
              "⚠️ Bu video bilgilendirme amaçlıdır; uçuş eğitimini lisanslı eğitmenle al.", "",
              f"{BASE_TAGS} {TOPIC_TAGS.get(no, '')}"]
    return "\n".join(lines)


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
        md += ["", "**Instagram açıklaması:**", "", "```text", caption(no, e, ep), "```"]
    out = os.path.join(ROOT, "SENARYOLAR.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("yazıldı:", out)


if __name__ == "__main__":
    main()
