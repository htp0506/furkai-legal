"""Ders 36 · Koşmadan önce 5 saniye"""

ITEMS = ["Kanat tamamen dolu mu?", "İpler düzgün, düğüm yok mu?", "Omzunun üstünden bak: trafik?",
         "Frenler ve askılar doğru elde mi?", "Her şey tamamsa: kalk!"]

EP = dict(
    slug="bes-saniye", title="ÖNCE\n5 SANİYE", subtitle="HEMEN KOŞMA", module_label="MODÜL 9 · KALKIŞ+",
    beats=[
        dict(scene="hook", p=dict(bg="launch", bgp=dict(stage=2.2, look=True)),
             say="Kanat tepede. Hemen koşma: önce beş saniye."),
        dict(scene="checklist", p=dict(items=ITEMS, active=0), say="Bir: kanat tamamen dolu mu?", sfx=[("ding", 1.0)]),
        dict(p=dict(active=1), say="İki: ipler düzgün mü, düğüm var mı?", sfx=[("ding", 1.0)]),
        dict(p=dict(active=2), say="Üç: omzunun üstünden bak. Hava trafiği var mı?", sfx=[("ding", 1.0)]),
        dict(p=dict(active=3), say="Dört: frenler ve askılar doğru elinde mi?", sfx=[("ding", 1.0)]),
        dict(p=dict(active=5), say="Beş: her şey tamamsa kalk.", k=[("KALK!", "green")], sfx=[("ding2", 0.3)]),
        dict(scene="launch", p=dict(stage0=2.0, stage=2.0, abort=1.0, tangle=1.0),
             say="Bir şey yolunda değilse vazgeç. Kanadı söndür, sakinleş ve yeniden dene.",
             k=[("VAZGEÇMEK DE BECERİDİR", "yellow")]),
        dict(scene="outro", p=dict(q="Kalkıştan vazgeçtiğin oldu mu?", options=["Evet, iyi ki", "Hayır", "Birkaç kez", "Çok kez 😄"]),
             say="Kalkıştan vazgeçtiğin oldu mu? Yorumlara yaz."),
    ],
)
