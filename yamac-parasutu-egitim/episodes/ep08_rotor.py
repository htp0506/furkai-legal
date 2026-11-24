"""Ders 08 · Rotor ve türbülans"""
from ._common import REAR

EP = dict(
    slug="rotor", title="ROTOR", subtitle="GÖRÜNMEYEN TEHLİKE", module_label="MODÜL 2 · METEOROLOJİ",
    beats=[
        dict(scene="hook", p=dict(bg="ridge", bgp=dict(rotor=1, glider=False, wind=0.8)),
             say="Gökyüzünde görünmeyen bir girdap var: rotor."),
        dict(scene="ridge", p=dict(rotor=1, glider=False, wind=0.7),
             say="Rüzgar bir engeli aştığında, arkasında dönen ve çalkantılı hava oluşur. Buna rotor denir.",
             k=["ENGEL ARKASI", ("ROTOR", "red")]),
        dict(scene="obstacles", p=dict(stagger=0.9),
             say="Dağ, tepe, ağaç sırası, hatta binalar bile rotor yaratır."),
        dict(scene="stage", p=dict(bg="sky", yaw=REAR, elev=0.12, shake=1.0, fold_r=0.55, crumple=0.2, scale=58,
                                   widgets=["vario"], vario0=-1.0, vario=-4.5),
             say="Rotorda kanat çalkalanır; kapanmalar ve ani alçalmalar olur.",
             k=[("KAPANMA RİSKİ", "red")], sfx=[("alarm", 0.4, 0.6)]),
        dict(scene="ridge", p=dict(rotor=1, glider=False, wind0=0.5, wind=1.0),
             say="Rüzgar ne kadar güçlüyse, rotor o kadar büyük ve sert olur.",
             k=[("GÜÇLÜ RÜZGAR = BÜYÜK ROTOR", "red")]),
        dict(scene="statement", p=dict(icon="🛑", text="Engellerin rüzgaraltına girme", accent="#22C55E"),
             say="Kural basit: engellerin rüzgaraltına girme, iniş alanını rotordan uzak seç.",
             k=[("RÜZGARALTINDAN UZAK DUR", "green")]),
        dict(scene="recap", p=dict(items=["Engel arkasında dönen hava: rotor", "Dağ, ağaç, bina: hepsi rotor yapar",
                                          "Rüzgar arttıkça rotor büyür", "Rüzgaraltından uzak dur"]),
             say="Rotoru göremezsin ama tahmin edebilirsin: rüzgarın nereye estiğini düşün."),
        dict(scene="outro", p=dict(q="Hiç rotora girdin mi?",
                                   options=["Evet 😬", "Hayır", "Az kalsın", "Kalkışta", "İnişte", "Sadece duydum"]),
             say="Hiç rotora girdin mi? Nasıl hissettirdi? Yorumlara yaz."),
    ],
)
