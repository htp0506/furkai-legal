"""Ders 03 · Uçuş ekipmanı"""

ITEMS = [("⛑️", "KASK"), ("💺", "OTURAK"), ("🪂", "YEDEK PARAŞÜT"), ("📻", "TELSİZ"),
         ("📈", "VARİO"), ("🥾", "BOT"), ("🧤", "ELDİVEN"), ("✂️", "KANCA BIÇAĞI")]
CARDS = dict(items=ITEMS, cols=2, ch=188, y0=520, reveal=[0, 1, 2, 3, 4, 5, 5, 5], accent="#22D3EE")

EP = dict(
    slug="ekipman", title="UÇUŞ\nEKİPMANI", subtitle="ÇANTANDA NE OLMALI?", module_label="MODÜL 1 · TEMELLER",
    beats=[
        dict(scene="hook", p=dict(bg="sky_glider"),
             say="Uçuş çantanda bunlar yoksa, kalkışa çıkma."),
        dict(scene="cards", p=dict(focus=0, **CARDS),
             say="Kask: başını korur. Sertifikalı olsun ve tam otursun.", k=[("1 · KASK", "dark")]),
        dict(p=dict(focus=1), say="Oturak ve koruması: sert inişte sırtını ve omurganı korur.", k=[("2 · OTURAK", "dark")]),
        dict(p=dict(focus=2), say="Yedek paraşüt: her uçuşta takılı olmalı ve düzenli olarak katlanmalı.",
             k=[("3 · YEDEK PARAŞÜT", "dark")]),
        dict(p=dict(focus=3), say="Telsiz: eğitmeninle ve diğer pilotlarla iletişimin.", k=[("4 · TELSİZ", "dark")]),
        dict(p=dict(focus=4), say="Vario: yükseldiğini ya da alçaldığını sesle söyler.", k=[("5 · VARİO", "dark")],
             sfx=[("vario", 1.2)]),
        dict(p=dict(focus=[5, 6, 7]),
             say="Bileği saran bot, eldiven ve gerektiğinde hatları kesebilen bir kanca bıçağı da listede olsun.",
             k=[("6 · BOT · ELDİVEN · BIÇAK", "dark")]),
        dict(scene="statement", p=dict(icon="🗓️", text="Yedeğini düzenli katlat", accent="#22D3EE"),
             say="Yedek paraşütünü üreticinin önerdiği aralıkta, genelde altı ila on iki ayda bir katlat.",
             k=[("6–12 AYDA BİR", "cyan")]),
        dict(scene="outro", p=dict(q="Çantanda olmazsa olmaz ne var?",
                                   options=["Vario", "Telsiz", "Termos çay ☕", "Güneş kremi", "Su", "Yedek pil", "Kamera", "Eldiven"]),
             say="Senin çantanda olmazsa olmaz ne var? Yorumlara yaz."),
    ],
)
