"""Ders 26 · Termikte dönüş: 5 adım"""
from ._common import REAR

EP = dict(
    slug="termikte-donus", title="TERMİKTE\nDÖNÜŞ", subtitle="5 ADIM", module_label="MODÜL 7 · TERMİK",
    beats=[
        dict(scene="hook", p=dict(bg="thermal", bgp=dict(heat=1, column=1, cloud=1, circle=1, vario_widget=False, labels=False)),
             say="Termiği buldun. Şimdi doğru dönmenin beş adımı."),
        dict(scene="thermal_top", p=dict(tight0=0.0, tight=1.0),
             say="Bir: termiğin içinde kal. Geniş değil, dar bir daire çiz.",
             k=["1 · DAR DAİRE"]),
        dict(scene="stage", p=dict(bg="high", yaw=REAR, elev=0.14, scale=58, weight=1.0, brake_r=0.45, roll=0.4,
                                   arrows=[("weight", 1), ("rot", 1, "#34D399")]),
             say="İki: içteki freni çek ve ağırlığını içeri ver.",
             k=["2 · İÇ FREN + AĞIRLIK"]),
        dict(scene="speedrange", p=dict(kmh0=33, kmh=26, brake=0.7, zone="STOL"),
             say="Üç: hızını koru. Fazla fren çekersen kanat stol sınırına yaklaşır.",
             k=["3 · HIZINI KORU", ("FAZLA FREN = STOL", "red")]),
        dict(scene="thermal_top", p=dict(tight=1.0, drift0=0.0, drift=1.0, show_wind=True),
             say="Dört: termik rüzgarla sürüklenir. Daireni de onunla birlikte kaydır.",
             k=["4 · DAİREYİ KAYDIR"]),
        dict(scene="stage", p=dict(bg="high", yaw=REAR, elev=0.14, scale=58, brake_l=0.1, brake_r=0.1, widgets=["brake_l", "brake_r"]),
             say="Beş: çıkarken frenleri eşitle. Önce çevreye, sonra iniş alanına bak.",
             k=["5 · FRENLER EŞİT", ("ÇEVREYE BAK", "dark")]),
        dict(scene="recap", p=dict(items=["Dar daire, termiğin içinde", "İç fren + ağırlık içeri",
                                          "Hızını koru, stola yaklaşma", "Daireyi rüzgarla kaydır"]),
             say="Dar dön, hızını koru, termikle birlikte kay. Gerisini vario söyler."),
        dict(scene="outro", p=dict(q="Termikte hangi yöne dönmeyi seversin?", options=["Sağa", "Sola", "Fark etmez", "İlk pilot neyse"]),
             say="Termikte hangi yöne dönmeyi seversin? Yorumlara yaz."),
    ],
)
