"""Ders 34 · Yer hakimiyeti"""

L = dict(reverse=True, wind=0.7)

EP = dict(
    slug="yer-hakimiyeti", title="YER\nHAKİMİYETİ", subtitle="KANADI YERDE EVCİLLEŞTİR", module_label="MODÜL 9 · KALKIŞ+",
    beats=[
        dict(scene="hook", p=dict(bg="launch", bgp=dict(L, stage=2.1)),
             say="Pilot olmak istiyorsan, önce kanadı yerde evcilleştirirsin."),
        dict(scene="launch", p=dict(L, stage0=0.0, stage=1.5, stage_dur=2.4, rise_arrow=True),
             say="Bir: şişir. Rüzgarla kanadı başının üstüne getir.",
             k=["1 · ŞİŞİR"], sfx=[("whoosh_down", 0.4, 0.5)]),
        dict(p=dict(stage=2.12, stage_dur=1.0, rise_arrow=False),
             say="İki: tut. Önce on saniye, sonra otuz saniye kanadı tepede tut.",
             k=["2 · TUT", ("10 sn → 30 sn", "dark")]),
        dict(p=dict(stage=2.05),
             say="Üç: düzelt. Kanat bir yana kayarsa altına adım at, frenle dengele.",
             k=["3 · DÜZELT"]),
        dict(p=dict(abort=1.0),
             say="Dört: söndür. Frenleri ya da arka askıları çekerek kanadı kontrollü indir.",
             k=["4 · SÖNDÜR"]),
        dict(scene="statement", p=dict(icon="🎯", text="Her fırsatta yer hakimiyeti çalış", accent="#FFB020"),
             say="Yer hakimiyeti iyi olan pilotun kalkışı da inişi de sakindir. Her fırsatta çalış.",
             k=[("HER FIRSATTA ÇALIŞ", "green")]),
        dict(scene="outro", p=dict(q="Kanadı tepede kaç saniye tutabiliyorsun?", options=["5 sn", "10 sn", "30 sn", "1 dk+", "Hiç denemedim"]),
             say="Kanadı tepede kaç saniye tutabiliyorsun? Yorumlara yaz."),
    ],
)
