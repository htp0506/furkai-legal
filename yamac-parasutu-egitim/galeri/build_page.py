"""Galeri sayfasını şablon + ders listesi + yüklenen video adreslerinden üretir."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/furkai-legal/yamac-parasutu-egitim")
from episodes import SERIES  # noqa: E402

MODULES = [
    ("Temeller", range(1, 5)), ("Meteoroloji", range(5, 10)), ("Kalkış", range(10, 13)),
    ("Uçuş Teknikleri", range(13, 17)), ("İniş", range(17, 20)), ("Acil Durumlar ve Kurallar", range(20, 25)),
    ("Termik ve Navigasyon", range(25, 29)), ("İleri Manevralar", range(29, 32)), ("Kalkış Ustalığı", range(32, 38)),
    ("İniş Ustalığı", range(38, 40)), ("Meteoroloji+", range(40, 46)), ("Pilot ve Ekipman", range(46, 52)),
]
TEMP_VOICE = set(range(37, 52))  # Piper sesi; 24 Aralık'ta Matilda ile yenilenecek

meta = {}
for line in open(os.path.join(HERE, "meta.tsv"), encoding="utf-8"):
    n, f, d, s = line.rstrip("\n").split("\t")
    meta[int(n)] = (f, float(d), int(s))

urls_path = os.path.join(HERE, "urls.json")
urls = json.load(open(urls_path)) if os.path.exists(urls_path) else {}
temp_path = os.path.join(HERE, "temp_voice.json")
temp = set(json.load(open(temp_path))) if os.path.exists(temp_path) else TEMP_VOICE

mod_of = {n: i + 1 for i, (_, r) in enumerate(MODULES) for n in r}
lessons = []
for ep in SERIES:
    n = ep["no"]
    f, d, s = meta[n]
    lessons.append(dict(no=n, title=ep["title"], mod=mod_of[n], file=f, dur=round(d, 1), size=s,
                        url=urls.get(str(n), ""), temp=n in temp))
data = dict(lessons=lessons, modules=[dict(name=m, lessons=list(r)) for m, r in MODULES],
            voiceDate="24 Aralık")
blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
html = open(os.path.join(HERE, "template.html"), encoding="utf-8").read().replace("__DATA__", blob)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
print("lessons", len(lessons), "with url", sum(1 for l in lessons if l["url"]), "bytes", len(html.encode()))
