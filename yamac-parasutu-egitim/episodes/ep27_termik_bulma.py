"""Ders 27 · Termik nasıl bulunur?"""

CARDS = dict(items=[("🦅", "KUŞLAR"), ("🪂", "DAİRE ÇİZEN KANAT"), ("☀️", "GÜNEŞE BAKAN YAMAÇ"),
                    ("☁️", "KÜMÜLÜS TABANI"), ("🍂", "UÇUŞAN TOZ, YAPRAK")],
             cols=2, ch=215, y0=560, reveal=[0, 0, 1, 2, 3], accent="#FFB020")

EP = dict(
    slug="termik-bulma", title="TERMİĞİ\nBUL", subtitle="5 İPUCU", module_label="MODÜL 7 · TERMİK",
    beats=[
        dict(scene="hook", p=dict(bg="thermal", bgp=dict(heat=1, column=1, cloud=1, circle=1, vario_widget=False, labels=False)),
             say="Termik görünmez, ama izini bırakır. İşte beş ipucu."),
        dict(scene="cards", p=dict(focus=[0, 1], **CARDS),
             say="Bir: kuşlara ve daire çizen kanatlara bak. Termiği çoktan bulmuşlardır.", k=[("1 · DAİRE ÇİZENLER", "dark")]),
        dict(p=dict(focus=2), say="İki: güneşe bakan yamaçlar ve kayalık alanlar daha çabuk ısınır.", k=[("2 · GÜNEŞLİ YAMAÇ", "dark")]),
        dict(p=dict(focus=3), say="Üç: kümülüs bulutunun tabanı, altındaki termiğin işaretidir.", k=[("3 · KÜMÜLÜS", "dark")]),
        dict(p=dict(focus=4), say="Dört: yerden kalkan toz ve uçuşan yapraklar, yükselen havayı gösterir.", k=[("4 · TOZ VE YAPRAK", "dark")]),
        dict(scene="thermal", p=dict(heat=1, column=1, circle=1, cloud=0.8, labels=False, vario=2.2),
             say="Beş: varioyu dinle. Ötmeye başladığı yerde daireye gir.",
             k=["5 · VARİOYU DİNLE"], sfx=[("vario_long", 0.3)]),
        dict(scene="outro", p=dict(q="Termiği en çok neyle bulursun?", options=["Kuşlar", "Bulutlar", "Vario", "Diğer pilotlar", "Şans 😄"]),
             say="Sen termiği en çok neyle bulursun? Yorumlara yaz."),
    ],
)
