"""README'deki müfredat tablosunu (süre ve dosya adlarıyla) güncelle."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from episodes import SERIES, MODULES  # noqa: E402

rows = ["| Ders | Modül | Konu | Süre | Video |", "|---|---|---|---|---|"]
total = 0.0
for e in SERIES:
    no = e["no"]
    meta = os.path.join(ROOT, "videolar", f".tmp_{no:02d}", "meta.json")
    dur, fn = "–", "–"
    if os.path.exists(meta):
        m = json.load(open(meta))
        dur = f"{m['duration']:.0f} sn"
        total += m["duration"]
        fn = f"[`{m['file']}`](videolar/{m['file']})"
    rows.append(f"| {no:02d} | {MODULES[no].split('·')[1].strip().title()} | {e['title']} | {dur} | {fn} |")
rows.append(f"| | | **Toplam** | **{total / 60:.1f} dk** | |")
table = "\n".join(rows)
p = os.path.join(ROOT, "README.md")
s = open(p, encoding="utf-8").read()
s = re.sub(r"<!-- TABLO -->.*<!-- /TABLO -->", "<!-- TABLO -->\n" + table + "\n<!-- /TABLO -->", s, flags=re.S)
open(p, "w", encoding="utf-8").write(s)
print(table)
