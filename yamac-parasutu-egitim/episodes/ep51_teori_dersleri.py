"""Ders 51 · Teorik dersler ve ilk uçuş"""

EP = dict(
    slug="teori-dersleri", title="TEORİ\nDERSLERİ", subtitle="6 DERS", module_label="MODÜL 12 · PİLOT",
    beats=[
        dict(scene="hook", p=dict(bg="statement", bgp=dict(icon="📚", accent="#FFB020", icon_y=600), title_y=1135),
             say="Yamaç paraşütünün de dersleri var: tam altı tane."),
        dict(scene="cards", p=dict(items=[("📜", "SPORUN TARİHİ"), ("🎒", "EKİPMAN"), ("✈️", "AERODİNAMİK"),
                                          ("🕹️", "SEVK VE İDARE"), ("🚦", "HAVA TRAFİK KURALLARI"), ("🌦️", "METEOROLOJİ")],
                                   cols=2, ch=200, y0=560, accent="#FFB020"),
             say="Sporun tarihi, ekipman, aerodinamik, sevk ve idare, hava trafik kuralları ve meteoroloji."),
        dict(scene="statement", p=dict(icon="📝", text="Sonunda yazılı sınav", accent="#FFB020"),
             say="Sonunda yazılı bir sınav var. Geçmek için yüzde yetmiş beş gerekir.",
             sub="Sonunda yazılı bir sınav var. Geçmek için %75 gerekir.",
             k=[("%75 İLE GEÇ", "yellow")]),
        dict(scene="statement", p=dict(icon="⛰️", text="Başlangıçta alçak tepeler", accent="#22D3EE"),
             say="Başlangıç pilotları genelde yetmiş beş ile altı yüz metre arası tepelerde uçar.",
             sub="Başlangıç pilotları genelde 75 ile 600 metre arası tepelerde uçar.",
             k=[("75–600 m", "cyan")]),
        dict(scene="statement", p=dict(icon="🏔️", text="Dağlar yarın da orada olacak", accent="#22C55E"),
             say="Daha yükseğe çıkmak daha fazla bilgi ve tecrübe ister. Unutma: dağlar yarın da orada olacak.",
             k=[("ACELE ETME", "green")]),
        dict(scene="outro", p=dict(q="Teori derslerinden hangisi en zor?", options=["Meteoroloji", "Aerodinamik", "Kurallar", "Ekipman", "Hiçbiri 😎"]),
             say="Sence teori derslerinden hangisi en zor? Yorumlara yaz."),
    ],
)
