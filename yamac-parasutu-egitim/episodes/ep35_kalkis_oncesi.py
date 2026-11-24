"""Ders 35 · Kalkıştan önce alanı ve rüzgarı oku"""

ITEMS = ["Alan temiz: taş, diken, çalı yok", "Rüzgarı en az 5 dakika izle", "Kalkış stilini seç",
         "Kanadı ser, hatları kontrol et"]

EP = dict(
    slug="kalkis-oncesi", title="KALKIŞTAN\nÖNCE", subtitle="4 KONTROL", module_label="MODÜL 9 · KALKIŞ+",
    beats=[
        dict(scene="hook", p=dict(bg="sock", bgp=dict(strength=0.5, meter=False)),
             say="Kalkıştan önce dört kontrol. Sonra hazırsın."),
        dict(scene="checklist", p=dict(items=ITEMS, active=0),
             say="Bir: alan temiz mi? Taş, diken ve çalı kanadına ve iplerine zarar verir.", sfx=[("ding", 1.3)]),
        dict(p=dict(active=1),
             say="İki: rüzgarı en az beş dakika izle. Rüzgar değişir, ani darbeler sınırı aşabilir.",
             k=[("EN AZ 5 DAKİKA", "yellow")], sfx=[("ding", 1.3)]),
        dict(p=dict(active=2), say="Üç: kalkış stilini seç. Hafif rüzgarda düz, güçlü rüzgarda ters.", sfx=[("ding", 1.3)]),
        dict(p=dict(active=3), say="Dört: kanadı ser; hatları ve askıları kontrol et.", sfx=[("ding", 1.3)]),
        dict(scene="sock", p=dict(strength0=0.5, strength=0.55, gusty=0.6),
             say="Rüzgar sınır içinde ve istikrarlıysa uç. Değilse bekle; beklemek de bir karardır.",
             k=[("İSTİKRARLI DEĞİLSE BEKLE", "yellow")]),
        dict(scene="outro", p=dict(q="Kalkışta en uzun ne kadar bekledin?", options=["5 dk", "30 dk", "1 saat", "Bütün gün 😅"]),
             say="Kalkışta en uzun ne kadar bekledin? Yorumlara yaz."),
    ],
)
