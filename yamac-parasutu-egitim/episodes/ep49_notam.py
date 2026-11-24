"""Ders 49 · NOTAM ve hava sahası"""

EP = dict(
    slug="notam", title="NOTAM", subtitle="HAVACILARA DUYURU", module_label="MODÜL 12 · PİLOT",
    beats=[
        dict(scene="hook", p=dict(bg="statement", bgp=dict(icon="📜", accent="#FFB020", icon_y=600), title_y=1135),
             say="Pilotlar uçmadan önce bir duyuru okur: NOTAM."),
        dict(scene="statement", p=dict(icon="📢", text="Havacılara yapılan resmi duyuru", accent="#FFB020"),
             say="NOTAM, havacılara yapılan resmi duyurudur.", k=["NOTAM"]),
        dict(scene="cards", p=dict(items=[("⛔", "GEÇİCİ KAPANMA"), ("🎯", "TATBİKAT"), ("🎪", "ETKİNLİK"), ("🚁", "ÖZEL UÇUŞ")],
                                   cols=2, ch=240, y0=600, accent="#F43F5E"),
             say="Bir bölgenin tatbikat, etkinlik ya da özel uçuş nedeniyle geçici olarak kapandığını haber verir."),
        dict(scene="statement", p=dict(icon="🗺️", text="Yasak, tehlikeli ve kısıtlı bölgeler", accent="#F43F5E"),
             say="Haritada yasak, tehlikeli ve kısıtlı bölgeler işaretlidir. Buralara izinsiz girilmez.",
             k=[("YASAK · TEHLİKELİ · KISITLI", "red")]),
        dict(scene="statement", p=dict(icon="✈️", text="Havaalanlarından uzak dur", accent="#22D3EE"),
             say="Havaalanlarından ve kontrollü hava sahasından uzak dur.",
             k=[("KONTROLLÜ HAVA SAHASI", "yellow")]),
        dict(scene="statement", p=dict(icon="✅", text="Uçmadan önce kontrol et", accent="#22C55E"),
             say="Uçuştan önce NOTAM'ları ve sahanın kurallarını kontrol et. Emin değilsen eğitmenine sor.",
             k=[("UÇMADAN ÖNCE KONTROL", "green")]),
        dict(scene="outro", p=dict(q="NOTAM'ı daha önce duymuş muydun?", options=["Evet", "Hayır", "Okuyorum", "Şimdi öğrendim"]),
             say="NOTAM'ı daha önce duymuş muydun? Yorumlara yaz."),
    ],
)
