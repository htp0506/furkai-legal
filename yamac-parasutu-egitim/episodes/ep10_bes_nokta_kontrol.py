"""Ders 10 · Uçuş öncesi 5 nokta kontrol"""

ITEMS = ["Kask takılı, çene kayışı bağlı", "Bacak ve göğüs tokaları kapalı", "Yedek pimleri yerinde, kol erişilebilir",
         "Hatlar açık, askılar doğru", "Rüzgar uygun, önün boş"]

EP = dict(
    slug="bes-nokta-kontrol", title="5 NOKTA\nKONTROL", subtitle="HER KALKIŞTAN ÖNCE", module_label="MODÜL 3 · KALKIŞ",
    beats=[
        dict(scene="hook", p=dict(bg="launch", bgp=dict(stage=0.0)),
             say="Kalkıştan önce on saniye. Hayat kurtaran beş kontrol."),
        dict(scene="checklist", p=dict(items=ITEMS, active=0), say="Bir: kask takılı ve çene kayışı bağlı.",
             sfx=[("ding", 1.3)]),
        dict(p=dict(active=1), say="İki: bacak ve göğüs tokaları kapalı. Bacak tokası unutulursa sonuç çok ağır olabilir.",
             k=[("BACAK TOKALARI!", "red")], sfx=[("ding", 1.3)]),
        dict(p=dict(active=2), say="Üç: yedek paraşütün pimleri yerinde, kolu kolayca ulaşılabilir.", sfx=[("ding", 1.3)]),
        dict(p=dict(active=3), say="Dört: hatlar açık; düğüm ve dolanma yok, askılar ve frenler doğru tarafta.",
             sfx=[("ding", 1.3)]),
        dict(p=dict(active=4), say="Beş: rüzgar uygun ve önün boş. Hava sahasını da kontrol et.", sfx=[("ding", 1.3)]),
        dict(p=dict(active=5), say="Her uçuşta aynı sırayla, yüksek sesle say. Alışkanlık seni korur.",
             k=[("HER UÇUŞTA · AYNI SIRA", "green")], sfx=[("ding2", 0.2)]),
        dict(scene="outro", p=dict(q="Sen kontrol listeni nasıl yapıyorsun?",
                                   options=["Sesli", "İçimden", "Kartla", "Eğitmenle", "Arkadaşımla"]),
             say="Sen kontrol listeni nasıl yapıyorsun? Yorumlara yaz."),
    ],
)
