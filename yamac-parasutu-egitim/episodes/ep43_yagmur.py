"""Ders 43 · Yağmurda uçulur mu?"""
from ._common import REAR

BASE = dict(bg="sky", theme="storm", yaw=REAR, elev=0.14, scale=58)

EP = dict(
    slug="yagmur", title="YAĞMURDA\nUÇULUR MU?", subtitle="ISLAK KANAT", module_label="MODÜL 11 · METEOROLOJİ+",
    beats=[
        dict(scene="hook", p=dict(bg="stage", bgp=dict(BASE, rain=1.0, y=1230, scale=44)),
             say="Yağmurda uçulur mu?"),
        dict(scene="stage", p=dict(BASE, rain0=0.0, rain=0.35),
             say="Hafif yağmurda kısa süre sorun olmayabilir. Ama en doğrusu hemen inmek.",
             k=[("HAFİF YAĞMUR: İN", "yellow")]),
        dict(p=dict(rain=1.0),
             say="Şiddetli yağmurda su kanadın içine dolar ve dışarı çıkamaz. Kanat ağırlaşır.",
             k=[("KANAT AĞIRLAŞIR", "red")]),
        dict(scene="airfoil", p=dict(aoa=14, brake=0.3, stall=0.35, flow=0.7, show_aoa=1),
             say="Islak kanat daha yavaş uçar ve derin stola girmeye yatkındır.",
             k=[("ISLAK KANAT = DERİN STOL RİSKİ", "red")]),
        dict(scene="stage", p=dict(BASE, rain=0.6, brake_l=0.08, brake_r=0.08, widgets=["brake_l", "brake_r"]),
             say="Islak kanatla frenleri derin çekme. Hızını koru ve ilk uygun yere in.",
             k=[("DERİN FREN YOK", "yellow")]),
        dict(scene="statement", p=dict(icon="☀️", text="Islak kanadı katlamadan önce kurut", accent="#FFB020"),
             say="Yerde de ıslak kanadı katlayıp bekletme. Gölgede, açık havada kurut.",
             k=[("KANADI KURUT", "cyan")]),
        dict(scene="outro", p=dict(q="Yağmura yakalandığın oldu mu?", options=["Evet 🌧️", "Hayır", "Az kalsın", "Hemen indim"]),
             say="Hiç havada yağmura yakalandın mı? Yorumlara yaz."),
    ],
)
