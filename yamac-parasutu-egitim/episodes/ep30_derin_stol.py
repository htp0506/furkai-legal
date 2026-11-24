"""Ders 30 · Derin stol ve tam stol"""
from ._common import SIDE_34

BASE = dict(bg="high", yaw=SIDE_34, elev=0.2, scale=58)

EP = dict(
    slug="derin-stol", title="DERİN STOL", subtitle="VE TAM STOL", module_label="MODÜL 8 · İLERİ MANEVRA",
    beats=[
        dict(scene="hook", p=dict(bg="stage", bgp=dict(BASE, stall=0.45, brake_l=0.7, brake_r=0.7, pitch=-0.2, y=1230, scale=44)),
             say="Derin stol ile tam stol aynı şey mi?"),
        dict(scene="stage", p=dict(BASE, stall0=0.0, stall=0.4, brake_l=0.7, brake_r=0.7, pitch=-0.15,
                                   widgets=["vario", "speed"], vario0=-1.2, vario=-4.5, kmh0=37, kmh=5),
             say="Derin stolde kanat şeklini korur ama ileri gitmez. Dikine, sessizce alçalırsın.",
             k=["DERİN STOL", ("ŞEKİL VAR · HIZ YOK", "yellow")]),
        dict(p=dict(rain=0.7),
             say="Islak kanat, aşırı fren ya da yıpranmış kumaş derin stolu tetikleyebilir.",
             k=[("ISLAK KANAT = RİSK", "red")]),
        dict(p=dict(rain=0.0, stall=1.0, brake_l=1.0, brake_r=1.0, pitch=-0.7, crumple=0.5, vario=-8.0, kmh=0),
             say="Tam stolde kanat şeklini kaybeder ve pilotun arkasına yıkılır. Düşüş çok hızlıdır.",
             k=["TAM STOL", ("ŞEKİL YOK", "red")], sfx=[("alarm", 0.4, 0.5)]),
        dict(scene="compare",
             p=dict(left=dict(title="DERİN STOL", verdict="warn", note="Eller yukarı, A'ları hafif ileri it",
                              glider=dict(stall=0.4, brake_l=0.6, brake_r=0.6, pitch=-0.15)),
                    right=dict(title="TAM STOL", verdict="bad", note="Sadece eğitmenle, SIV'de",
                               glider=dict(stall=1.0, brake_l=1, brake_r=1, pitch=-0.6, crumple=0.45, anim="flutter"))),
             say="Derin stolde ellerini kaldır, gerekirse A askılarını hafifçe ileri it. Tam stolü ise yalnızca eğitmenle çalış.",
             k=[("ÇIKIŞ: ELLER YUKARI", "green")]),
        dict(scene="outro", p=dict(q="Hangisini daha tehlikeli buluyorsun?", options=["Derin stol", "Tam stol", "İkisi de", "Bilmiyordum"]),
             say="Sence hangisi daha tehlikeli? Yorumlara yaz."),
    ],
)
