"""Ders 48 · Pilot sağlığı: DEATH kuralı"""

CARDS = dict(items=[("D", "İLAÇ", "#7C3AED"), ("E", "YORGUNLUK", "#2563EB"), ("A", "ALKOL", "#DC2626"),
                    ("T", "TÜTÜN", "#CA8A04"), ("H", "AÇLIK", "#16A34A")],
             cols=2, ch=215, y0=560, reveal=[0, 1, 2, 3, 4], accent="#F43F5E")

EP = dict(
    slug="death-kurali", title="DEATH\nKURALI", subtitle="PİLOT SAĞLIĞI", module_label="MODÜL 12 · PİLOT",
    beats=[
        dict(scene="hook", p=dict(bg="statement", bgp=dict(icon="☠️", accent="#F43F5E", icon_y=600), title_y=1135),
             say="Uçmadan önce beş harflik kuralı hatırla. İngilizcede ölüm demek."),
        dict(scene="cards", p=dict(focus=0, **CARDS), say="Bir: ilaç. Uyku yapan bir ilaç bile tepkini yavaşlatır."),
        dict(p=dict(focus=1), say="İki: yorgunluk. Uykusuz pilot yanlış karar verir."),
        dict(p=dict(focus=2), say="Üç: alkol. Uçuştan önce asla."),
        dict(p=dict(focus=3), say="Dört: tütün. Sigara kandaki oksijeni azaltır; irtifada daha çabuk yorulursun."),
        dict(p=dict(focus=4), say="Beş: açlık. Kan şekerin düşerse dikkatin dağılır. Yanına su ve atıştırmalık al."),
        dict(scene="statement", p=dict(icon="🛑", text="Biri bile varsa, o gün uçma", accent="#F43F5E"),
             say="Bunlardan biri bile varsa, o gün uçma.",
             k=[("BİRİ BİLE VARSA UÇMA", "red")]),
        dict(scene="outro", p=dict(q="Uçmadan önce ne yersin?", options=["Hafif kahvaltı", "Muz 🍌", "Hiçbir şey", "Simit 🥯"]),
             say="Uçmadan önce ne yersin? Yorumlara yaz."),
    ],
)
