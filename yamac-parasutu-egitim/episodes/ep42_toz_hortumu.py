"""Ders 42 · Toz hortumu"""

EP = dict(
    slug="toz-hortumu", title="TOZ\nHORTUMU", subtitle="DUST DEVIL", module_label="MODÜL 11 · METEOROLOJİ+",
    beats=[
        dict(scene="hook", p=dict(bg="dustdevil", bgp=dict(grow=1.0, x=760)),
             say="Kalkış alanında bir anda hortum çıkabilir mi? Evet: toz hortumu."),
        dict(scene="dustdevil", p=dict(grow=0.0, x=760),
             say="Sıcak, güneşli ve rüzgarın az olduğu günlerde zemin çok ısınır.",
             k=["SICAK, SAKİN GÜN"]),
        dict(p=dict(grow=1.0),
             say="Isınan hava kopar ve dönerek yükselir. Toz ve kuru otları havaya kaldırır.",
             k=[("DÖNEN SICAK HAVA", "orange")], sfx=[("whoosh", 0.3, 0.6)]),
        dict(p=dict(x=380, lift=1.0),
             say="Yerdeki kanadı yakalarsa savurur; havadaysan sert türbülans yaşatır.",
             k=[("KANADI SAVURUR", "red")], sfx=[("alarm", 0.6, 0.4)]),
        dict(p=dict(x=860, lift=0.0),
             say="Görürsen kanadını söndür, üstüne çök ve geçmesini bekle.",
             k=[("SÖNDÜR · BEKLE", "green")]),
        dict(scene="dustdevil", p=dict(grow=1.0, x=760, wing=False, glider_air=True),
             say="Uçarken görürsen ondan uzak dur. Çevresinde güçlü ve düzensiz termik vardır.",
             k=[("UZAK DUR", "red")]),
        dict(scene="outro", p=dict(q="Hiç toz hortumu gördün mü?", options=["Evet 😮", "Hayır", "Videoda", "Kalkışta"]),
             say="Hiç toz hortumu gördün mü? Yorumlara yaz."),
    ],
)
