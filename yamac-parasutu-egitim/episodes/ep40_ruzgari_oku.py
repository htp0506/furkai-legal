"""Ders 40 · Rüzgarı 5 yoldan oku"""

CARDS = dict(items=[("🎏", "RÜZGAR TULUMU"), ("🔠", "T PANOSU"), ("🌳", "AĞAÇLAR"), ("💨", "DUMAN"), ("🌊", "SU YÜZEYİ")],
             cols=2, ch=215, y0=560, reveal=[0, 0, 1, 2, 3], accent="#22D3EE")

EP = dict(
    slug="ruzgari-oku", title="RÜZGARI\nOKU", subtitle="5 YOL", module_label="MODÜL 11 · METEOROLOJİ+",
    beats=[
        dict(scene="hook", p=dict(bg="sock", bgp=dict(strength=0.55, meter=False)),
             say="Rüzgarı hangi beş yoldan okursun?"),
        dict(scene="sock", p=dict(strength=0.5),
             say="Bir: rüzgar tulumu. Ağzı yönü, şişme oranı şiddeti gösterir.",
             k=["1 · RÜZGAR TULUMU"]),
        dict(scene="cards", p=dict(focus=1, **CARDS), say="İki: yere serilen T panosu. Sadece yönü gösterir.", k=[("2 · T PANOSU", "dark")]),
        dict(p=dict(focus=2), say="Üç: ağaçların yatışı. Hem yönü hem şiddeti anlatır.", k=[("3 · AĞAÇLAR", "dark")]),
        dict(p=dict(focus=3), say="Dört: duman. Gidişi yönü, eğimi şiddeti gösterir.", k=[("4 · DUMAN", "dark")]),
        dict(p=dict(focus=4), say="Beş: su yüzeyi. Kırışan ve dalgalanan su, rüzgarın geldiğini haber verir.", k=[("5 · SU YÜZEYİ", "dark")]),
        dict(scene="sock", p=dict(strength=0.45),
             say="Standart bir tulumda yarı açık yaklaşık on, neredeyse yatay yaklaşık yirmi kilometre demektir.",
             sub="Standart bir tulumda yarı açık ≈ 10 km/sa, neredeyse yatay ≈ 20 km/sa demektir.",
             k=[("YARI AÇIK ≈ 10 · YATAY ≈ 20", "dark")]),
        dict(scene="outro", p=dict(q="Rüzgarı en çok neyle okursun?", options=["Tulum", "Ağaçlar", "Duman", "Su", "Diğer pilotlar"]),
             say="Sen rüzgarı en çok neyle okursun? Yorumlara yaz."),
    ],
)
