"""Ders 37 · İpler karıştı: nasıl çözülür?"""

CARDS = dict(items=[("🚫", "ORTADAN ÇÖZME"), ("🧍", "HARNESİ ARADAN GEÇİRME"), ("🌬️", "RÜZGARSIZ YERE ÇEK"),
                    ("🪢", "ASKIDAN BAŞLA"), ("🔍", "FRENİ AYRI TAKİP ET"), ("⛔", "ŞÜPHE VARSA UÇMA")],
             cols=2, ch=200, y0=560, reveal=[0, 1, 2, 3, 4, 5], accent="#F43F5E")

EP = dict(
    slug="ip-karisikligi", title="İPLER\nKARIŞTI", subtitle="NEREDEN BAŞLARSIN?", module_label="MODÜL 9 · KALKIŞ+",
    beats=[
        dict(scene="hook", p=dict(bg="launch", bgp=dict(stage=0.0)),
             say="İpler karıştı. Nereden başlarsın?"),
        dict(scene="cards", p=dict(focus=0, **CARDS),
             say="En büyük hata: düğümü ortadan ya da yukarıdan çözmeye çalışmak.", k=[("HATA", "red")]),
        dict(p=dict(focus=1), say="Harnesi iplerin arasından geçirmek de düğümü büyütür.", k=[("HATA", "red")]),
        dict(p=dict(focus=2), say="Karışıklık kötüyse kanadı rüzgar almayan bir yere çek ve sakince yay.", k=[("DOĞRU", "green")]),
        dict(p=dict(focus=3), say="Askılardan başla. Her ipi aşağıdan yukarıya takip ederek ayır.", k=[("DOĞRU", "green")]),
        dict(p=dict(focus=4), say="Fren ipini ayrıca takip et; firar kenarına kadar serbest gitmeli.", k=[("DOĞRU", "green")]),
        dict(p=dict(focus=5), say="İçinde şüphe kalan bir düğüm varsa uçma.", k=[("ŞÜPHE VARSA UÇMA", "red")]),
        dict(scene="outro", p=dict(q="İp karışıklığını en hızlı kim çözer?", options=["Ben 💪", "Eğitmenim", "Arkadaşım", "Hiçbirimiz 😅"]),
             say="Sizde ip karışıklığını en hızlı kim çözer? Yorumlara yaz."),
    ],
)
