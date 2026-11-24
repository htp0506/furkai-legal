"""Ders 01 · Yamaç paraşütü nasıl uçar?"""
from ._common import SIDE_34, SITES

EP = dict(
    slug="nasil-ucar", title="NASIL\nUÇAR?", subtitle="MOTORSUZ UÇUŞ", module_label="MODÜL 1 · TEMELLER",
    beats=[
        dict(scene="hook", p=dict(bg="sky_glider"),
             say="Motoru yok. Peki yamaç paraşütü nasıl uçuyor?"),
        dict(scene="stage", p=dict(bg="sky", yaw=0.0, elev=0.12, inflate0=0.12, inflate=1.0, scale=64, y=1020, arrows=[("air",)]),
             say="Yamaç paraşütü aslında bir kanat. Önündeki ağızlardan giren hava, hücreleri doldurur ve ona şeklini verir.",
             k=["HAVA DOLU KANAT", ("HÜCRELER ŞİŞER", "cyan")]),
        dict(scene="airfoil", p=dict(aoa=8, show_pressure=1, show_lift=1),
             say="Kanat ileri giderken üstünde alçak, altında yüksek basınç oluşur. Bu fark, kaldırma kuvvetidir.",
             k=["KALDIRMA KUVVETİ"]),
        dict(scene="stage", p=dict(bg="high", yaw=SIDE_34, elev=0.2, scale=60, widgets=["vario"], vario0=-1.1, vario=-1.1, arrows=[("down",)]),
             say="Motor olmadığı için hep hafifçe alçalırsın. Sakin havada saniyede yaklaşık bir metre.",
             k=["SÜREKLİ SÜZÜLÜŞ", ("≈ 1 m/s ALÇALMA", "dark")], sfx=[("sink", 0.6)]),
        dict(scene="thermal", p=dict(heat=1, column=1, circle=1, cloud0=0.0, cloud=0.6, labels=False, vario=2.4),
             say="Ama etrafındaki hava senden hızlı yükselirse, sen de yükselirsin.",
             k=["YÜKSELEN HAVA", ("= YÜKSELİŞ", "green")], sfx=[("vario_long", 0.5)]),
        dict(p=dict(cloud=1.0),
             say="Uzun uçuşların sırrı bu: yükselen havayı bulmak ve içinde kalmak.",
             k=[("SIR: YÜKSELEN HAVA", "yellow")]),
        dict(scene="recap", p=dict(items=["Kanat şeklini içindeki havadan alır", "İleri hız kaldırma kuvveti yaratır",
                                          "Sakin havada sürekli süzülürsün", "Yükselen hava seni yukarı taşır"]),
             say="Özetle: kanat şeklini havadan alır, ileri hız kaldırma yaratır, yükselen hava seni taşır."),
        dict(scene="outro", p=dict(q="İlk uçuşun nerede oldu?", options=SITES),
             say="Sen ilk uçuşunu nerede yaptın? Yorumlara yaz."),
    ],
)
