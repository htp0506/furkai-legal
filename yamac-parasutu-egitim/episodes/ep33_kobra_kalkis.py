"""Ders 33 · Kobra kalkış"""

L = dict(reverse=True, cobra=True, wind=0.7)

EP = dict(
    slug="kobra-kalkis", title="KOBRA\nKALKIŞ", subtitle="KANAT YANDAN KALKAR", module_label="MODÜL 9 · KALKIŞ+",
    beats=[
        dict(scene="hook", p=dict(bg="launch", bgp=dict(L, stage=1.6)),
             say="Kobra kalkış: kanat yandan kalkar."),
        dict(scene="launch", p=dict(L, stage=0.0),
             say="Kanat yanında, istifli yatar. Bir ucu açık kalır.",
             k=["KANAT YANDA", ("İSTİFLİ", "dark")]),
        dict(p=dict(stage=0.3),
             say="Bir elinde A kolonu, diğerinde fren.",
             k=[("A KOLONU + FREN", "yellow")]),
        dict(p=dict(stage=1.4, stage_dur=2.2, rise_arrow=True),
             say="A ile açık ucu kaldır. Rüzgar kanadı yandan doldurur.",
             k=[("AÇIK UCU KALDIR", "cyan")], sfx=[("whoosh_down", 0.5, 0.5)]),
        dict(p=dict(stage=1.9, stage_dur=1.2, rise_arrow=False),
             say="Kobra duruşu: kanat öne giderse fren, geri düşerse A kolonu.",
             k=["KOBRA DURUŞU", ("ÖNE: FREN · GERİ: A", "dark")]),
        dict(p=dict(stage=4.6, stage_dur=4.0, turn=0.0, look=True),
             say="Kanat tepede, eller yukarıda. Son kontrolü yap, dön ve kalk.",
             k=[("KONTROL · DÖN · KALK", "green")]),
        dict(scene="statement", p=dict(icon="⚠️", text="Sadece deneyimli pilotlar için", accent="#F43F5E"),
             say="Kobra kalkış ileri seviyedir. Önce düz ve ters kalkışta ustalaş.",
             k=[("SADECE DENEYİMLİ PİLOT", "red")]),
        dict(scene="outro", p=dict(q="Kobra kalkışı denedin mi?", options=["Evet", "Hayır", "Öğreniyorum", "Sadece videoda 😄"]),
             say="Kobra kalkışı hiç denedin mi? Yorumlara yaz."),
    ],
)
