"""Ders 44 · Yükseldikçe neden üşürsün?"""

EP = dict(
    slug="irtifa-sicaklik", title="YÜKSEKTE\nSOĞUK", subtitle="NEDEN ÜŞÜRSÜN?", module_label="MODÜL 11 · METEOROLOJİ+",
    beats=[
        dict(scene="hook", p=dict(bg="lapse", bgp=dict(climb=1.0, seq=False)),
             say="Yükseldikçe neden üşürsün?"),
        dict(scene="lapse", p=dict(climb0=0.0, climb=0.25),
             say="Yükseldikçe hava basıncı azalır. Hava genleşir ve soğur.",
             k=["BASINÇ AZALIR"]),
        dict(p=dict(climb=0.6),
             say="Ortalama olarak her bin metrede sıcaklık yaklaşık altı buçuk derece düşer.",
             sub="Ortalama olarak her 1000 metrede sıcaklık yaklaşık 6,5 derece düşer.",
             k=[("1000 m ≈ −6,5 °C", "cyan")]),
        dict(p=dict(climb=1.0),
             say="Yerde yirmi beş derece ise, iki bin metrede yaklaşık on iki derecedir.",
             sub="Yerde 25 derece ise, 2000 metrede yaklaşık 12 derecedir.",
             k=[("25 °C → ≈ 12 °C", "yellow")]),
        dict(p=dict(cold=True),
             say="Bir de uçuş rüzgarı eklenince hissedilen sıcaklık daha da düşer.",
             k=[("RÜZGAR SOĞUĞU", "cyan")]),
        dict(scene="cards", p=dict(items=[("🧤", "ELDİVEN"), ("🧥", "RÜZGARLIK"), ("🧣", "BOYUNLUK"), ("💧", "SU")],
                                   cols=2, ch=240, y0=600, accent="#22D3EE"),
             say="Sıcak bir günde bile eldiven, rüzgarlık ve boyunluk al.",
             k=[("KATMANLI GİYİN", "green")]),
        dict(scene="outro", p=dict(q="Havada en çok neren üşür?", options=["Eller", "Ayaklar", "Yüz", "Hiç üşümem 😎"]),
             say="Havada en çok neren üşüyor? Yorumlara yaz."),
    ],
)
