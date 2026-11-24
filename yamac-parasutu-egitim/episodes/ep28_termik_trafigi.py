"""Ders 28 · Kalabalık termikte kurallar"""

EP = dict(
    slug="termik-trafigi", title="KALABALIK\nTERMİK", subtitle="5 DİKKAT", module_label="MODÜL 7 · TERMİK",
    beats=[
        dict(scene="hook", p=dict(bg="traffic", bgp=dict(case="thermal", n=6)),
             say="Aynı termikte on pilot varsa ne yaparsın?"),
        dict(scene="traffic", p=dict(case="thermal", n=6),
             say="Bir: girmeden önce bak. Termikte kaç kişi var, hangi yöne dönüyorlar?",
             k=[("1 · ÖNCE BAK", "cyan")]),
        dict(p=dict(n=4),
             say="İki: ilk giren pilot hangi yöne dönüyorsa sen de o yöne dön. Ters yöne dönmek çarpışma demektir.",
             k=[("2 · AYNI YÖNE DÖN", "yellow")]),
        dict(scene="traffic", p=dict(case="landing"),
             say="Üç: alttaki pilotun önceliği var. O, yukarıyı göremeyebilir.",
             k=[("3 · ALTTAKİ ÖNCELİKLİ", "cyan")]),
        dict(scene="thermal_top", p=dict(tight=1.0, drift0=0.0, drift=1.0, show_wind=True),
             say="Dört: termik rüzgarla sürüklenir. İrtifanı ve iniş alanına uzaklığını takip et.",
             k=[("4 · İNİŞ ALANINI UNUTMA", "yellow")]),
        dict(scene="statement", p=dict(icon="👀", text="Çok kalabalıksa başka termik ara", accent="#22C55E"),
             say="Beş: kalabalık çok fazlaysa zorlama. Başka bir termik ara.",
             k=[("5 · KALABALIKSA UZAKLAŞ", "green")]),
        dict(scene="outro", p=dict(q="Aynı termikte en fazla kaç kişi oldunuz?", options=["2", "5", "10", "20+", "Hep tek başıma"]),
             say="Aynı termikte en fazla kaç kişi oldunuz? Yorumlara yaz."),
    ],
)
