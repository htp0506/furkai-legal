"""Ders 39 · Frenin konumu: çeyrek, yarım, tam"""

EP = dict(
    slug="fren-konumu", title="FREN\nKONUMU", subtitle="ÇEYREK · YARIM · TAM", module_label="MODÜL 10 · İNİŞ+",
    beats=[
        dict(scene="hook", p=dict(bg="brakepos", bgp=dict(brake=0.49)),
             say="Fren konumunu nereden anlarsın? Ellerinin yüksekliğinden."),
        dict(scene="brakepos", p=dict(brake=0.0),
             say="Eller yukarıdayken kanat trim hızında, en verimli şekilde uçar.",
             k=["ELLER YUKARI", ("TRİM", "green")]),
        dict(p=dict(brake=0.49, mark="ÇEYREK"), say="Çeyrek fren: eller omuz hizasında.", k=["ÇEYREK FREN"]),
        dict(p=dict(brake=0.76, mark="YARIM"), say="Yarım fren: eller göğüs hizasında.", k=["YARIM FREN"]),
        dict(p=dict(brake=1.27, mark="TAM"),
             say="Tam fren: eller kalça hizasında. Burada kanat stola girebilir.",
             k=[("TAM FREN = STOL RİSKİ", "red")], sfx=[("alarm", 0.6, 0.4)]),
        dict(p=dict(brake=0.62, mark=None),
             say="Normal uçuşta verimli aralık, çeyrek ile yarım fren arasıdır. Tam freni yalnız palyanın sonunda kullan.",
             k=[("ÇEYREK – YARIM ARASI", "green")]),
        dict(scene="outro", p=dict(q="Uçarken ellerin genelde nerede?", options=["Yukarıda", "Omuzda", "Göğüste", "Bilmiyorum 😅"]),
             say="Uçarken ellerin genelde nerede duruyor? Yorumlara yaz."),
    ],
)
