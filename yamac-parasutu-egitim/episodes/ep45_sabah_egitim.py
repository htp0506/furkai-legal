"""Ders 45 · Eğitim neden sabah erken?"""

EP = dict(
    slug="sabah-egitim", title="NEDEN\nSABAH?", subtitle="EĞİTİM SAATİ", module_label="MODÜL 11 · METEOROLOJİ+",
    beats=[
        dict(scene="hook", p=dict(bg="daytime", bgp=dict(hour=7.5)),
             say="Eğitim neden sabahın erken saatinde başlar?"),
        dict(scene="daytime", p=dict(hour0=6.5, hour=8.0),
             say="Sabah hava serindir. Rüzgar az ve sakindir.",
             k=["SABAH: SAKİN"]),
        dict(p=dict(hour=11.0),
             say="Güneş yükseldikçe zemin ısınır ve termikler başlar.",
             k=[("TERMİK BAŞLAR", "yellow")]),
        dict(p=dict(hour=13.5),
             say="Öğleye doğru hava hareketlenir. Türbülans ve ani rüzgarlar artar.",
             k=[("ÖĞLE: TÜRBÜLANS", "red")]),
        dict(p=dict(hour=18.5),
             say="Akşamüstü hava yeniden sakinleşir ve ikinci eğitim penceresi açılır.",
             k=[("AKŞAM: YİNE SAKİN", "green")]),
        dict(scene="recap", p=dict(items=["Sabah: serin ve sakin", "Kuşluk: termikler başlar",
                                          "Öğle: türbülans artar", "Akşamüstü: yine sakin"]),
             say="Doğru saatte uçmak, öğrenmenin en kolay yoludur."),
        dict(scene="outro", p=dict(q="Sabah mı akşam mı uçmayı seversin?", options=["Sabah 🌅", "Akşam 🌇", "Öğle ☀️", "Fark etmez"]),
             say="Sen sabah mı akşam mı uçmayı seversin? Yorumlara yaz."),
    ],
)
