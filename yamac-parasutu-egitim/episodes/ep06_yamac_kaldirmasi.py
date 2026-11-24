"""Ders 06 · Yamaç (dinamik) kaldırması"""
from ._common import SITES

EP = dict(
    slug="yamac-kaldirmasi", title="YAMAÇ\nKALDIRMASI", subtitle="DİNAMİK KALDIRMA", module_label="MODÜL 2 · METEOROLOJİ",
    beats=[
        dict(scene="hook", p=dict(bg="ridge", bgp=dict(band=1, wind=0.6)),
             say="Rüzgar dağa çarptığında sana bedava yükseklik verir."),
        dict(scene="ridge", p=dict(band=0, rotor=0, wind=0.6),
             say="Yamaca dik esen rüzgar, eğime çarpınca yukarı yönelir. Buna yamaç ya da dinamik kaldırma denir.",
             k=["DİNAMİK KALDIRMA"]),
        dict(p=dict(band=1),
             say="En güçlü kaldırma, yamacın önünde ve biraz üstündedir. Bu bölgeye kaldırma bandı denir.",
             k=[("KALDIRMA BANDI", "green")]),
        dict(scene="ridge_top", p=dict(),
             say="Yamaç boyunca gidip gelirsin. Dönüşlerini her zaman yamaçtan dışarı, rüzgara doğru yaparsın.",
             k=[("DÖNÜŞ: YAMAÇTAN DIŞARI", "yellow")]),
        dict(scene="ridge", p=dict(band=0, wind0=0.6, wind=1.0, drift=0.85, rotor=0.4),
             say="Rüzgar çok artarsa geri sürüklenip yamacın arkasına düşebilirsin.",
             k=[("ÇOK RÜZGAR = GERİ SÜRÜKLENME", "red")], sfx=[("alarm", 1.5, 0.5)]),
        dict(p=dict(rotor=1.0),
             say="Yamacın arkası rotor bölgesidir. Oraya asla girme.",
             k=[("ARKA TARAF: ROTOR", "red")]),
        dict(scene="recap", p=dict(items=["Rüzgar yamaca çarpar, yukarı yönelir", "Kaldırma bandı: yamacın önü ve üstü",
                                          "Dönüşler yamaçtan dışarı", "Rüzgar artarsa: geri sürüklenme, rotor"]),
             say="Kural basit: bandın içinde kal, yamaçtan uzağa dön, rüzgar artarsa erken in."),
        dict(scene="outro", p=dict(q="En sevdiğin yamaç sahası hangisi?", options=SITES),
             say="En sevdiğin yamaç uçuşu sahası hangisi? Yorumlara yaz."),
    ],
)
