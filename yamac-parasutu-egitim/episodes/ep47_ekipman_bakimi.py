"""Ders 47 · Ekipman bakımı: ipler ve yedek"""

CARDS = dict(items=[("🪢", "İPLER"), ("🪂", "YEDEK PARAŞÜT"), ("☀️", "UV IŞIĞI"), ("💧", "NEM")],
             cols=2, ch=250, y0=600, reveal=[0, 1, 2, 3], accent="#22D3EE")

EP = dict(
    slug="ekipman-bakimi", title="EKİPMAN\nBAKIMI", subtitle="İPLER VE YEDEK", module_label="MODÜL 12 · PİLOT",
    beats=[
        dict(scene="hook", p=dict(bg="statement", bgp=dict(icon="🧰", accent="#22D3EE", icon_y=600), title_y=1135),
             say="Ekipmanın da bakım ister. İşte dört kural."),
        dict(scene="cards", p=dict(focus=0, **CARDS),
             say="İpler zamanla kısalır ya da uzar; kanadın ayarı bozulur.", k=[("1 · İPLER", "dark")]),
        dict(p=dict(focus=0),
             say="Üreticiler ip kontrolünü belirli saatlerde önerir; çoğu kanatta yaklaşık yüz saatte bir.",
             sub="Üreticiler ip kontrolünü belirli saatlerde önerir; çoğu kanatta yaklaşık 100 saatte bir.",
             k=[("≈ 100 SAATTE BİR KONTROL", "yellow")]),
        dict(p=dict(focus=1),
             say="Yedek paraşüt düzenli olarak açılır, havalandırılır ve yetkili biri tarafından yeniden katlanır.",
             k=[("2 · YEDEK: 6–12 AYDA BİR", "cyan")]),
        dict(p=dict(focus=2), say="Kanadı güneşte uzun süre bekletme; UV ışığı kumaşı yıpratır.", k=[("3 · UV", "dark")]),
        dict(p=dict(focus=3), say="Islak kanadı ve ipleri kurutmadan katlama; nem kumaşı ve ipleri bozar.", k=[("4 · NEM", "dark")]),
        dict(scene="outro", p=dict(q="Kanadını en son ne zaman kontrol ettirdin?", options=["Bu yıl", "Geçen yıl", "Hiç 😬", "Yeni aldım"]),
             say="Kanadını en son ne zaman kontrol ettirdin? Yorumlara yaz."),
    ],
)
