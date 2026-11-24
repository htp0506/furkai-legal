"""Ders 29 · Derin spiral ve tam spiral"""
from ._common import REAR_34

BASE = dict(bg="high", yaw=REAR_34, elev=0.32, scale=56, y=900, drift=60)

EP = dict(
    slug="spiral", title="SPİRAL", subtitle="DERİN VE TAM SPİRAL", module_label="MODÜL 8 · İLERİ MANEVRA",
    beats=[
        dict(scene="hook", p=dict(bg="stage", bgp=dict(BASE, roll=1.2, spin=2.4, pitch=0.3, y=1230, scale=40)),
             say="En hızlı alçalma yöntemi: spiral. Peki bedeli ne?"),
        dict(scene="stage", p=dict(BASE, roll=1.0, spin=2.2, pitch=0.25, widgets=["vario", "bank", "gmeter"],
                                   vario0=-1.2, vario=-12.0, bank_deg=55, g=2.8),
             say="Derin spiralde kanat yatar ve hızla döner. Alçalma saniyede on ila yirmi metreye çıkar.",
             k=["DERİN SPİRAL", ("10–20 m/s", "dark")]),
        dict(p=dict(roll=1.45, spin=2.8, bank_deg=85, vario=-22.0, g=4.2),
             say="Tam spiralde kanat neredeyse yere paralel olur. Ön kenar yere bakar.",
             k=["TAM SPİRAL", ("≈ 90° YATIŞ", "red")], sfx=[("alarm", 0.6, 0.4)]),
        dict(p=dict(g=4.6),
             say="Yük arttıkça kan baştan çekilir. Dört G'nin üstünde görme kararabilir, bilinç kaybı riski başlar.",
             k=[("G KUVVETİ", "red")]),
        dict(p=dict(roll=0.5, spin=1.0, widgets=["vario"], vario=-6.0, altbar=True, alt0=1200, alt=420),
             say="Bazı kanatlar bırakınca kendiliğinden çıkmaz. Çıkışı dış frenle yönet; en geç üç yüz metrede bitmiş olsun.",
             k=["ÇIKIŞ", ("EN GEÇ 300 m", "red")]),
        dict(scene="statement", p=dict(icon="🌊", text="Sadece SIV kursunda, su üstünde, eğitmenle", accent="#22D3EE"),
             say="Spirali yalnızca güvenlik kursunda, su üstünde ve eğitmenle öğren.",
             k=[("SADECE SIV'DE", "cyan")]),
        dict(scene="recap", p=dict(items=["Derin spiral: 10–20 m/s alçalma", "Tam spiral: ≈ 90° yatış",
                                          "4 G üstü: bilinç kaybı riski", "Çıkış en geç 300 m'de biter"]),
             say="Spiral güçlü bir araçtır; saygı duymazsan seni yorar."),
        dict(scene="outro", p=dict(q="Spirali hiç denedin mi?", options=["SIV'de", "Hayır", "Planlıyorum", "Kulak katlama yeter"]),
             say="Spirali hiç denedin mi? Yorumlara yaz."),
    ],
)
