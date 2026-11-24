"""Ders 16 · Kulak katlama"""
from ._common import REAR, SIDE_34, SITES

EP = dict(
    slug="kulak-katlama", title="KULAK\nKATLAMA", subtitle="HIZLI ALÇALMA", module_label="MODÜL 4 · UÇUŞ",
    beats=[
        dict(scene="hook", p=dict(bg="stage", bgp=dict(bg="high", yaw=REAR, elev=0.12, ears=1, ears_hands=True, y=1230, scale=46)),
             say="Hızlıca alçalman gerektiğinde ilk tekniğin: kulak katlama."),
        dict(scene="stage", p=dict(bg="high", yaw=REAR, elev=0.12, scale=60, ears0=0.0, ears=1.0, ears_hands=True,
                                   hl={"A": "#FFD23F"}),
             say="En dış A hatlarını tutup aşağı çekersin. Kanadın uçları içe katlanır.",
             k=[("DIŞ A HATLARI", "yellow")]),
        dict(p=dict(hl=None, widgets=["vario"], vario0=-1.1, vario=-3.0, arrows=[("down",)]),
             say="Kanat alanı küçülür, alçalma hızın artar ama ileri hızın korunur.",
             k=["DAHA HIZLI ALÇALMA", ("≈ −3 m/s", "dark")], sfx=[("sink", 0.5)]),
        dict(p=dict(weight=1.0, roll=0.15, arrows=[("weight", 1)]),
             say="Kulaklar katlıyken yön değiştirmek için fren değil, ağırlık kullanırsın.",
             k=[("YÖN: AĞIRLIKLA", "cyan")]),
        dict(p=dict(weight=0.0, roll=0.0, bar=1.0, yaw=SIDE_34, elev=0.2, arrows=[], widgets=["vario", "speed"], kmh=45),
             say="Hızlandırıcıyla birleştirirsen hem alçalır hem ilerlersin. Örneğin bir buluttan uzaklaşırken.",
             k=[("+ HIZLANDIRICI", "yellow")]),
        dict(p=dict(ears=0.0, bar=0.0, yaw=REAR, elev=0.12, widgets=["vario"], vario=-1.1, kmh=37, pump=1, arrows=[("pump", 1)]),
             say="Bıraktığında uçlar genelde kendiliğinden açılır. Açılmazsa o taraftaki freni bir kez uzun pompala.",
             k=["BIRAK", ("GEREKİRSE POMPALA", "dark")]),
        dict(scene="statement", p=dict(icon="⚠️", text="İnişe yaklaşmadan kulakları bırak", accent="#F43F5E"),
             say="İnişe yaklaşmadan kulakları bırak. Kulaklar katlıyken palya yapma.",
             k=[("İNİŞTEN ÖNCE BIRAK", "red")]),
        dict(scene="recap", p=dict(items=["Dış A hatlarını çek: uçlar katlanır", "Alçalma hızı artar",
                                          "Yön ağırlıkla", "İnişten önce bırak"]),
             say="Kulak katlama, en sakin hızlı alçalma yöntemidir. Önce eğitmenle, yüksekte dene."),
        dict(scene="outro", p=dict(q="Kulak katlamayı ilk nerede denedin?", options=SITES),
             say="Kulak katlamayı ilk nerede denedin? Yorumlara yaz."),
    ],
)
