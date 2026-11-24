"""Ders 14 · Dönüş tekniği"""
from ._common import REAR, REAR_34

EP = dict(
    slug="donus", title="DÖNÜŞ\nTEKNİĞİ", subtitle="BAK · AĞIRLIK · FREN", module_label="MODÜL 4 · UÇUŞ",
    beats=[
        dict(scene="hook", p=dict(bg="sky_glider", bgp=dict(yaw=REAR_34, roll=0.3)),
             say="Güzel bir dönüş üç adımdır: bak, ağırlık ver, fren çek."),
        dict(scene="stage", p=dict(bg="high", yaw=REAR, elev=0.14, scale=60,
                                   callouts=[("SAĞ TARAF BOŞ MU?", "pilot", (790, 1180), "#22D3EE")]),
             say="Önce döneceğin yöne bak. Hava sahası boş mu?", k=["1 · BAK"]),
        dict(p=dict(callouts=[], weight=1.0, arrows=[("weight", 1)]),
             say="Sonra ağırlığını o tarafa ver. Oturakta o yöne doğru yaslan.", k=["2 · AĞIRLIK"]),
        dict(p=dict(brake_r=0.5, brake_l=0.12, roll=0.35, arrows=[("rot", 1, "#34D399")], widgets=["brake_l", "brake_r"]),
             say="Son olarak o taraftaki freni yumuşakça çek. Dış freni hafif tutarak dönüşü kontrol et.",
             k=["3 · İÇ FREN", ("DIŞ FREN DESTEK", "dark")]),
        dict(p=dict(brake_r=0.15, brake_l=0.15, roll=0.0, weight=0.0, pitch=0.25, arrows=[], widgets=[]),
             say="Dönüşten çıkarken freni yavaşça bırak. Kanat öne dalarsa hafif kontra ver.",
             k=[("YUMUŞAK ÇIKIŞ", "green")]),
        dict(p=dict(pitch=0.0, brake_r=1.0, brake_l=0.0, fold_r=0.35, crumple=0.35, spin=3.2, elev=0.4,
                    widgets=["brake_l", "brake_r"]),
             say="Ani ve sert tek taraflı fren, kanadı negatife sokabilir. Dönüşlerde her zaman yumuşak ol.",
             k=[("SERT FREN = NEGATİF RİSKİ", "red")], sfx=[("alarm", 0.4, 0.5)]),
        dict(scene="recap", p=dict(items=["Bak: hava sahası boş mu?", "Ağırlığını dönüş tarafına ver",
                                          "İç fren yumuşak, dış fren destek", "Sert ve ani fren yok"]),
             say="Bak, ağırlık, fren. Bu sırayı alışkanlık hâline getir."),
        dict(scene="outro", p=dict(q="Sağa mı sola mı dönmek daha rahat?", options=["Sağa ➡️", "Sola ⬅️", "İkisi de", "Fark etmez"]),
             say="Sağa mı sola mı dönmek sana daha rahat geliyor? Yorumlara yaz."),
    ],
)
