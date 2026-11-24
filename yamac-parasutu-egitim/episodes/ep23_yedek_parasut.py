"""Ders 23 · Yedek paraşüt atma"""
from ._common import SIDE_34, REAR

STEPS = dict(items=[("👀", "1 · BAK"), ("✊", "2 · TUT"), ("💪", "3 · ÇEK"), ("🤾", "4 · AT")], cols=2, ch=250,
             y0=600, reveal=[0, 1, 2, 3], accent="#F43F5E")

EP = dict(
    slug="yedek-parasut", title="YEDEK\nPARAŞÜT", subtitle="BAK · TUT · ÇEK · AT", module_label="MODÜL 6 · ACİL DURUM",
    beats=[
        dict(scene="hook", p=dict(bg="stage", bgp=dict(bg="high", yaw=SIDE_34, elev=0.2, reserve=1.0, pitch=2.7, crumple=0.5,
                                                         flat=0.5, inflate=0.3, anchor="pilot", y=1320, scale=40)),
             say="Her şey ters gittiyse son çaren: yedek paraşüt."),
        dict(scene="stage", p=dict(bg="high", yaw=REAR, elev=0.3, scale=56, spin=4.0, crumple=0.55, fold_l=0.8, stall=0.4,
                                   shake=0.5, widgets=["vario"], vario0=-3.0, vario=-12.0),
             say="Kanat toparlanamıyorsa ve yükseklik hızla azalıyorsa tereddüt etme. Hemen at.",
             k=[("TEREDDÜT ETME", "red")], sfx=[("alarm", 0.2, 0.6)]),
        dict(scene="cards", p=dict(focus=0, **STEPS), say="Bir, bak: yedek kolunun yerini gözünle bul."),
        dict(p=dict(focus=1), say="İki, tut: kolu tek elinle sıkıca kavra."),
        dict(p=dict(focus=2), say="Üç, çek: kolu kararlı bir hareketle dışarı çek ve konteyneri aç."),
        dict(p=dict(focus=3), say="Dört, at: paketi boş havaya, yana doğru güçlüce fırlat.", sfx=[("whoosh", 0.5)]),
        dict(scene="stage", p=dict(bg="high", yaw=SIDE_34, elev=0.2, scale=46, anchor="pilot", y=1180, reserve0=0.0, reserve=1.0,
                                   pitch=2.7, crumple=0.5, flat=0.5, inflate=0.3),
             say="Yedek açılınca ana kanadı etkisizleştir: Be hatlarını ya da bir freni sararak topla.",
             sub="Yedek açılınca ana kanadı etkisizleştir: B hatlarını ya da bir freni sararak topla.",
             k=[("ANA KANADI TOPLA", "yellow")]),
        dict(scene="statement", p=dict(icon="🔁", text="PLF ile in, simülatörde düzenli çalış", accent="#22C55E"),
             say="Yere değerken pe le fe yap. Ve bu hareketi yerde, simülatörde sık sık çalış.",
             sub="Yere değerken PLF yap. Ve bu hareketi yerde, simülatörde sık sık çalış.",
             k=[("PLF · DÜZENLİ PRATİK", "green")]),
        dict(scene="recap", p=dict(items=["Tereddüt etme", "Bak · Tut · Çek · At", "Ana kanadı topla", "PLF ile in, düzenli çalış"]),
             say="Yedek, kullanmayı umduğun değil, kullanmayı bildiğin bir hayat sigortasıdır."),
        dict(scene="outro", p=dict(q="Yedeğini en son ne zaman katlattın?",
                                   options=["Bu ay", "3 ay önce", "6 ay önce", "1 yıl önce", "Hiç 😬"]),
             say="Yedeğini en son ne zaman katlattın? Yorumlara yaz."),
    ],
)
