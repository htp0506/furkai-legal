"""Ders 17 · İniş yaklaşması"""

LEGS = ["eights", "downwind", "base", "final"]

EP = dict(
    slug="inis-yaklasmasi", title="İNİŞ\nYAKLAŞMASI", subtitle="PİST DÜZENİ", module_label="MODÜL 5 · İNİŞ",
    beats=[
        dict(scene="hook", p=dict(bg="pattern", bgp=dict(legs=LEGS)),
             say="İyi iniş, iniş alanına varmadan başlar."),
        dict(scene="pattern", p=dict(legs=[]),
             say="Önce rüzgar tulumuna bak. İniş her zaman rüzgara karşı yapılır.",
             k=[("RÜZGARA KARŞI", "yellow")]),
        dict(p=dict(legs=["eights"], active="eights"),
             say="Fazla yüksekliği, iniş alanının yanında güvenli bir bölgede sekiz çizerek erit.",
             k=[("8 ÇİZ · YÜKSEKLİK ERİT", "yellow")]),
        dict(p=dict(legs=LEGS[:2], active="downwind"),
             say="Sonra rüzgar yönüne paralel, rüzgaraltı bacağını uçarsın.",
             k=[("RÜZGARALTI BACAĞI", "cyan")]),
        dict(p=dict(legs=LEGS[:3], active="base"),
             say="Doksan derece dönüp baz bacağına geçersin.",
             k=[("BAZ BACAĞI", "violet")]),
        dict(p=dict(legs=LEGS, active="final"),
             say="Son dönüşle finale girer, rüzgara karşı düz ve sakin uçarsın.",
             k=[("FİNAL", "orange")]),
        dict(p=dict(active=None, no_low_turn=True),
             say="Alçakta asla dönüş yapma. Finalde ellerin yukarıda ve hızın yerinde olsun; palyaya hazırsın.",
             k=[("ALÇAKTA DÖNÜŞ YOK", "red")]),
        dict(scene="recap", p=dict(items=["İniş rüzgara karşı", "Fazla yüksekliği 8 çizerek erit",
                                          "Rüzgaraltı → baz → final", "Alçakta dönüş yok"]),
             say="Planlı bir yaklaşma, sakin bir iniş demektir."),
        dict(scene="outro", p=dict(q="İniş alanında en zor şey ne?",
                                   options=["Küçük alan", "Ağaçlar", "Elektrik hattı", "Rotor", "Rüzgar dönüşü", "Kalabalık"]),
             say="Senin iniş alanında en zor şey ne? Yorumlara yaz."),
    ],
)
