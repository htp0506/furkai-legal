"""Ders 21 · Önden kapanma"""
from ._common import SIDE_34

BASE = dict(bg="high", yaw=SIDE_34, elev=0.2, scale=58)

EP = dict(
    slug="onden-kapanma", title="ÖNDEN\nKAPANMA", subtitle="FRONTAL KAPANMA", module_label="MODÜL 6 · ACİL DURUM",
    beats=[
        dict(scene="hook", p=dict(bg="stage", bgp=dict(BASE, front=1.0, pitch=-0.4, crumple=0.2, y=1230, scale=44)),
             say="Kanadının ön kenarı bir anda içe katlandı!"),
        dict(scene="airfoil", p=dict(aoa=2, lefold0=0.0, lefold=0.9, show_aoa=1, show_chord=1),
             say="Hücum açısı çok düştüğünde, örneğin sert bir dalışta ya da türbülansta, hücum kenarı içe katlanır.",
             k=[("AÇI ÇOK DÜŞTÜ", "red")]),
        dict(scene="stage", p=dict(BASE, front0=0.0, front=1.0, pitch=-0.45, shake=0.35, crumple=0.15),
             say="Kanat geriye kaçar, sen bir an öne sallanırsın.",
             k=["KANAT GERİDE"], sfx=[("alarm", 0.1, 0.6)]),
        dict(p=dict(brake_l=0.4, brake_r=0.4, front=0.0, front_dur=1.6, pitch=0.0, shake=0.1, widgets=["brake_l", "brake_r"]),
             say="Çoğu kanat kendi kendine hızla açılır. Kısa, simetrik ve kararlı bir fren dokunuşu açılmaya yardım eder.",
             k=[("KISA SİMETRİK FREN", "yellow")]),
        dict(p=dict(pitch=0.32, brake_l=0.35, brake_r=0.35),
             say="Kanat açılırken öne dalarsa kontra ver. Ama freni uzun tutma, stola girebilirsin.",
             k=["DALIŞA KONTRA", ("STOLA DİKKAT", "red")]),
        dict(p=dict(pitch=0.0, brake_l=0.15, brake_r=0.15, shake=0.35, widgets=[]),
             say="Önlemenin yolu: türbülansta hafif fren tut, kanadı hisset ve aktif pilotaj yap.",
             k=[("ÖNLEM: AKTİF PİLOTAJ", "green")]),
        dict(scene="recap", p=dict(items=["Düşük açı: hücum kenarı katlanır", "Çoğu kanat kendiliğinden açılır",
                                          "Kısa simetrik fren, dalışa kontra", "Önlem: aktif pilotaj"]),
             say="Kanadını hissetmeyi öğren; kapanmayı başlamadan önlersin."),
        dict(scene="outro", p=dict(q="Aktif pilotajı nasıl öğrendin?",
                                   options=["Yer hakimiyeti", "Termikte", "SIV kursu", "Eğitmenle", "Hâlâ öğreniyorum"]),
             say="Aktif pilotajı nasıl öğrendin? Yorumlara yaz."),
    ],
)
