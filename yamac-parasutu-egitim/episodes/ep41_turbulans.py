"""Ders 41 · Türbülans nereden gelir?"""
from ._common import REAR

EP = dict(
    slug="turbulans", title="TÜRBÜLANS", subtitle="NEREDEN GELİR?", module_label="MODÜL 11 · METEOROLOJİ+",
    beats=[
        dict(scene="hook", p=dict(bg="stage", bgp=dict(bg="high", yaw=REAR, elev=0.12, shake=0.7, crumple=0.15, y=1230, scale=44)),
             say="Türbülans nereden gelir? Üç ana kaynaktan."),
        dict(scene="thermal", p=dict(heat=1, column=1, circle=1, cloud=0.7, labels=False, vario=3.0),
             say="Bir: ısınan hava. Termiklerin kenarı çalkantılıdır.", k=["1 · TERMİK"]),
        dict(scene="ridge", p=dict(rotor=1, glider=False, wind=0.8),
             say="İki: dağ, tepe ve vadi gibi yeryüzü şekilleri. Rüzgaraltında rotor oluşur.", k=["2 · YERYÜZÜ ŞEKİLLERİ"]),
        dict(scene="statement", p=dict(icon="🌬️", text="Rüzgarın yön ya da hız değiştirdiği katmanlar", accent="#22D3EE"),
             say="Üç: rüzgar kırılması. Rüzgarın yön ya da hız değiştirdiği yerlerde hava çalkalanır.", k=["3 · RÜZGAR KIRILMASI"]),
        dict(scene="stage", p=dict(bg="high", yaw=REAR, elev=0.12, scale=58, shake=0.6, brake_l=0.18, brake_r=0.18,
                                   widgets=["brake_l", "brake_r"]),
             say="Türbülansta hafif fren tut, kanadı hisset ve aktif pilotaj yap.",
             k=[("AKTİF PİLOTAJ", "green")]),
        dict(scene="recap", p=dict(items=["Termik: ısınan hava", "Yeryüzü şekilleri: rotor", "Rüzgar kırılması",
                                          "Çözüm: hafif fren, aktif pilotaj"]),
             say="Türbülansın kaynağını bilen pilot, nerede bekleyeceğini de bilir."),
        dict(scene="outro", p=dict(q="En sert türbülansı nerede yaşadın?", options=["Termikte", "Rotorda", "Kalkışta", "İnişte", "Hiç 😇"]),
             say="En sert türbülansı nerede yaşadın? Yorumlara yaz."),
    ],
)
