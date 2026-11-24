"""Ders 46 · Kanat sınıfları"""

CARDS = dict(items=[("A", "EN AFFEDİCİ", "#16A34A"), ("B", "GELİŞEN PİLOT", "#CA8A04"),
                    ("C", "PERFORMANS", "#EA580C"), ("D", "YARIŞMA", "#DC2626")],
             cols=2, ch=270, y0=600, reveal=[0, 1, 2, 3], accent="#FFB020")

EP = dict(
    slug="kanat-siniflari", title="KANAT\nSINIFLARI", subtitle="A · B · C · D", module_label="MODÜL 12 · PİLOT",
    beats=[
        dict(scene="hook", p=dict(bg="sky_glider"),
             say="Kanatlar dört sınıfa ayrılır. Hangisinden başlarsın?"),
        dict(scene="cards", p=dict(focus=0, **CARDS), say="A sınıfı: en affedici kanat. Eğitim ve ilk yıllar için."),
        dict(p=dict(focus=1), say="B sınıfı: biraz daha hızlı ve hassas. Düzenli uçan, gelişen pilotlar için."),
        dict(p=dict(focus=2), say="C sınıfı: performans kanadı. Deneyimli ve aktif pilotajı oturmuş pilotlar için."),
        dict(p=dict(focus=3), say="D sınıfı: yarışma ve uzman kanadı. Hata affı çok azdır.", k=[("UZMANLAR İÇİN", "red")]),
        dict(scene="statement", p=dict(icon="🧭", text="Sınıfı egon değil, becerin seçsin", accent="#22C55E"),
             say="Kanadını egon değil, uçuş saatin ve becerin seçsin.",
             k=[("EGO DEĞİL, BECERİ", "green")]),
        dict(scene="outro", p=dict(q="Senin kanadın hangi sınıf?", options=["A", "B", "C", "D", "Henüz yok"]),
             say="Senin kanadın hangi sınıf? Yorumlara yaz."),
    ],
)
