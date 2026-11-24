"""Ders 50 · P2 ve P3: pilotluk seviyeleri"""

CARDS = dict(items=[("P2", "EĞİTMEN EŞLİĞİNDE", "#2563EB"), ("P3", "KENDİ KONTROLÜNDE", "#16A34A")],
             cols=2, ch=300, y0=640, reveal=[0, 1], accent="#22D3EE")

EP = dict(
    slug="pilot-seviyeleri", title="P2 Mİ,\nP3 MÜ?", subtitle="PİLOTLUK SEVİYELERİ", module_label="MODÜL 12 · PİLOT",
    beats=[
        dict(scene="hook", p=dict(bg="sky_glider"),
             say="Pe iki mi, pe üç mü? Fark tek cümle: tek başına uçmak.",
             sub="P2 mi, P3 mü? Fark tek cümle: tek başına uçmak."),
        dict(scene="cards", p=dict(focus=0, **CARDS),
             say="Pe iki, eğitmen eşliğinde uçan öğrenci pilot seviyesidir.",
             sub="P2, eğitmen eşliğinde uçan öğrenci pilot seviyesidir."),
        dict(p=dict(focus=1),
             say="Pe üç ise kendi kararını verebilen, tek başına uçan başlangıç pilotudur.",
             sub="P3 ise kendi kararını verebilen, tek başına uçan başlangıç pilotudur."),
        dict(scene="statement", p=dict(icon="📄", text="P2: kurs bitirme belgesi · P3: pilot kartı", accent="#FFB020"),
             say="Pe iki sonunda kurs bitirme belgesi, pe üç sonunda başlangıç pilot kartı alırsın.",
             sub="P2 sonunda kurs bitirme belgesi, P3 sonunda başlangıç pilot kartı alırsın."),
        dict(scene="statement", p=dict(icon="📋", text="Şartları kulübünden ve THK'dan öğren", accent="#22D3EE"),
             say="Pe üç için daha fazla uçuş ve saat gerekir. Güncel şartları kulübünden öğren.",
             sub="P3 için daha fazla uçuş ve saat gerekir. Güncel şartları kulübünden öğren."),
        dict(scene="statement", p=dict(icon="🪜", text="Her seviye bir öncekinin üstüne kurulur", accent="#22C55E"),
             say="Her seviye bir öncekinin üstüne kurulur. Acele etme.", k=[("ADIM ADIM", "green")]),
        dict(scene="outro", p=dict(q="Hangi seviyedesin?", options=["P1", "P2", "P3", "P4", "Henüz başlamadım"]),
             say="Sen hangi seviyedesin? Yorumlara yaz."),
    ],
)
