"""Ders 31 · Wingover"""
from ._common import REAR

BASE = dict(bg="high", yaw=REAR, elev=0.14, scale=56)

EP = dict(
    slug="wingover", title="WINGOVER", subtitle="SARKAÇ HAREKETİ", module_label="MODÜL 8 · İLERİ MANEVRA",
    beats=[
        dict(scene="hook", p=dict(bg="stage", bgp=dict(BASE, wingover=0.8, y=1230, scale=42)),
             say="Kanat neden sağa sola sallanıyor? Buna vingover denir.",
             sub="Kanat neden sağa sola sallanıyor? Buna wingover denir."),
        dict(scene="stage", p=dict(BASE, wingover0=0.0, wingover=0.5),
             say="Vingover, kanadı frenlerle sağa sola, sarkaç gibi sallamaktır.",
             sub="Wingover, kanadı frenlerle sağa sola, sarkaç gibi sallamaktır.",
             k=["WINGOVER", ("SARKAÇ", "cyan")]),
        dict(p=dict(wingover=0.95, widgets=["bank", "vario"], bank_deg=60, vario=-4.0),
             say="Her salınımda yatış, hız ve alçalma artar.",
             k=[("YATIŞ ARTAR", "yellow")]),
        dict(p=dict(wingover=1.1, crumple=0.25, fold_r=0.4, fold_dur=1.2),
             say="Zamanlama kaçarsa kanat kapanabilir. Büyük salınımlarda risk hızla artar.",
             k=[("ZAMANLAMA KAÇARSA: KAPANMA", "red")], sfx=[("alarm", 0.4, 0.5)]),
        dict(scene="statement", p=dict(icon="🎓", text="Akro hazırlığı: önce SIV ve eğitmen", accent="#22D3EE"),
             say="Vingover bir akro hazırlığıdır. Önce güvenlik kursu ve eğitmen gerekir.",
             sub="Wingover bir akro hazırlığıdır. Önce güvenlik kursu ve eğitmen gerekir.",
             k=[("ÖNCE SIV", "cyan")]),
        dict(scene="outro", p=dict(q="Akro uçuşa ilgin var mı?", options=["Evet 🤩", "Hayır", "Sadece izlerim", "SIV'den sonra"]),
             say="Akro uçuşa ilgin var mı? Yorumlara yaz."),
    ],
)
