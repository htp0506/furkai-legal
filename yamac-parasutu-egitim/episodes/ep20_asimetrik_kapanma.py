"""Ders 20 · Asimetrik kapanma"""
from ._common import REAR

BASE = dict(bg="high", yaw=REAR, elev=0.12, scale=60)

EP = dict(
    slug="asimetrik-kapanma", title="ASİMETRİK\nKAPANMA", subtitle="ÖNCE YÖN, SONRA KANAT", module_label="MODÜL 6 · ACİL DURUM",
    beats=[
        dict(scene="hook", p=dict(bg="stage", bgp=dict(BASE, fold_l=1.0, crumple=0.25, shake=0.3, y=1230, scale=46)),
             say="Kanadının bir tarafı aniden kapandı. Ne yaparsın?"),
        dict(scene="stage", p=dict(BASE, shake=0.8, fold_l0=0.0, fold_l=1.0, crumple=0.2),
             say="Türbülans, kanadın bir tarafının basıncını kaçırabilir. O taraf katlanır; buna asimetrik kapanma denir.",
             k=[("TEK TARAF KATLANIR", "red")], sfx=[("alarm", 0.2, 0.6)]),
        dict(p=dict(shake=0.3, roll=-0.28, arrows=[("rot", -1)]),
             say="Kanat, kapanan tarafa doğru dönmeye başlar. İlk işin yönü korumak.",
             k=["1 · YÖNÜ KORU"]),
        dict(p=dict(shake=0.15, roll=-0.08, weight=1.0, brake_r=0.35, arrows=[("weight", 1)],
                    callouts=[("AÇIK TARAF", "te:0.6", (820, 640), "#34D399"), ("KAPANAN", "te:-0.8", (250, 640), "#F43F5E")]),
             say="Ağırlığını açık tarafa ver ve açık taraftaki freni dikkatli bir dozda çek.",
             k=[("AÇIK TARAF: AĞIRLIK + FREN", "green")]),
        dict(p=dict(brake_r=0.95, callouts=[], arrows=[], widgets=["brake_r"]),
             say="Fazla fren, açık tarafı da stola sokabilir. Dozunda kal.",
             k=[("AŞIRI FREN YOK", "red")]),
        dict(p=dict(brake_r=0.3, weight=0.4, pump=-1, arrows=[("pump", -1)], fold_l=0.0, fold_dur=3.0, widgets=["brake_l"]),
             say="Yön kontrol altındaysa ve kapanan taraf açılmadıysa, o taraftaki freni uzun ve yumuşak bir pompayla çek.",
             k=["2 · POMPALA"]),
        dict(scene="statement", p=dict(icon="🌊", text="Su üstünde, eğitmenle: güvenlik kursu", accent="#22D3EE"),
             say="Bu tepkiler, eğitmenli güvenlik kurslarında su üstünde güvenle çalışılır.",
             k=[("GÜVENLİK KURSU (SIV)", "cyan")]),
        dict(scene="recap", p=dict(items=["Önce yön: ağırlık açık tarafa", "Açık tarafa dozunda fren",
                                          "Aşırı fren yok", "Sonra kapanan tarafı pompala"]),
             say="Önce yön, sonra kanat. Panik değil, sıra."),
        dict(scene="outro", p=dict(q="Hiç kapanma yaşadın mı?", options=["Evet 😬", "Hayır", "Küçük bir tane", "SIV'de", "Rotorda"]),
             say="Hiç kapanma yaşadın mı? Yorumlara yaz."),
    ],
)
