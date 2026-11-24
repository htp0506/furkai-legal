"""Ders 32 · Kalkışın üç yolu"""

EP = dict(
    slug="kalkis-yollari", title="KALKIŞIN\n3 YOLU", subtitle="HANGİSİ NE ZAMAN?", module_label="MODÜL 9 · KALKIŞ+",
    beats=[
        dict(scene="hook", p=dict(bg="launch", bgp=dict(stage=4.6)),
             say="Kalkışın üç yolu var. Hangisi ne zaman?"),
        dict(scene="launch", p=dict(stage0=0.6, stage=1.8, stage_dur=3.0, rise_arrow=True),
             say="Düz kalkış: rüzgar hafifken. Kanat arkanda, yüzün vadiye dönük; koşarak kalkarsın.",
             k=["1 · DÜZ KALKIŞ", ("HAFİF RÜZGAR", "green")]),
        dict(scene="launch", p=dict(reverse=True, wind=0.75, stage0=0.6, stage=1.9, stage_dur=3.0, rise_arrow=True),
             say="Ters kalkış: rüzgar güçlüyken. Yüzün kanada dönük, kanadı görerek kaldırırsın.",
             k=["2 · TERS KALKIŞ", ("GÜÇLÜ RÜZGAR", "yellow")]),
        dict(scene="launch", p=dict(reverse=True, cobra=True, wind=0.7, stage0=0.2, stage=1.9, stage_dur=3.2),
             say="Kobra kalkış: kanat yanda, istifli başlar. Dar alanlarda ve deneyimli pilotlar için.",
             k=["3 · KOBRA", ("DENEYİMLİ PİLOT", "red")]),
        dict(scene="recap", p=dict(items=["Hafif rüzgar: düz kalkış", "Güçlü rüzgar: ters kalkış",
                                          "Dar alan, deneyim: kobra", "Seçimi rüzgar ve alan belirler"]),
             say="Doğru kalkış; rüzgara, alana ve deneyimine göre seçilir."),
        dict(scene="outro", p=dict(q="Senin favori kalkışın hangisi?", options=["Düz", "Ters", "Kobra", "Hepsi"]),
             say="Senin favori kalkışın hangisi? Yorumlara yaz."),
    ],
)
