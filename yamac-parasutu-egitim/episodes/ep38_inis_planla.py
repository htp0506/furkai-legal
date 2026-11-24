"""Ders 38 · İnişi havada planla"""

LEGS = ["eights", "downwind", "base", "final"]

EP = dict(
    slug="inis-planla", title="İNİŞİ\nPLANLA", subtitle="YERE GELMEDEN", module_label="MODÜL 10 · İNİŞ+",
    beats=[
        dict(scene="hook", p=dict(bg="pattern", bgp=dict(legs=LEGS)),
             say="İnişi yere gelmeden planla."),
        dict(scene="statement", p=dict(icon="⏱️", text="200 metrenin altında ≈ 2 dakikan var", accent="#FFB020"),
             say="Yerden iki yüz metrenin altında yaklaşık iki dakikan var. Planı bundan önce yap.",
             k=[("200 m ALTI ≈ 2 DK", "yellow")]),
        dict(scene="cards", p=dict(items=[("📏", "DÜZ VE BÜYÜK"), ("🌳", "AĞAÇTAN UZAK"), ("⚡", "ELEKTRİK HATTINDAN UZAK"),
                                          ("🏠", "BİNA VE İNSANDAN UZAK")], cols=2, ch=230, y0=580, accent="#22C55E"),
             say="İniş alanı düz, büyük ve engelsiz olmalı. Ağaçtan, telden, binadan ve insandan uzak.",
             k=[("İYİ İNİŞ ALANI", "green")]),
        dict(scene="pattern", p=dict(legs=["eights"], active="eights"),
             say="Dönüşlerini yüksekte bitir.",
             k=[("DÖNÜŞLER YÜKSEKTE", "yellow")]),
        dict(p=dict(legs=LEGS, active="final"),
             say="Sonra rüzgara karşı uzun ve düz bir final uç.",
             k=[("UZUN, DÜZ FİNAL", "orange")]),
        dict(scene="statement", p=dict(icon="🅱️", text="Her zaman bir yedek iniş alanın olsun", accent="#22D3EE"),
             say="Ve her zaman bir yedek iniş alanın olsun.",
             k=[("B PLANI", "cyan")]),
        dict(scene="recap", p=dict(items=["200 m altında ≈ 2 dakika", "Düz, büyük, engelsiz alan",
                                          "Dönüşler yüksekte, final uzun", "Her zaman bir yedek alan"]),
             say="İyi iniş tesadüf değil, plandır."),
        dict(scene="outro", p=dict(q="Senin yedek iniş alanın neresi?", options=["Tarla", "Sahil", "Çayır", "Okul bahçesi 😄", "Hiç düşünmedim"]),
             say="Senin yedek iniş alanın neresi? Yorumlara yaz."),
    ],
)
