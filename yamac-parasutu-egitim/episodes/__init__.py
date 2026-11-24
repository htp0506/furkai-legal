"""Eğitim serisi: modüller ve dersler."""

SERIES = [
    # MODÜL 1 · TEMELLER
    dict(no=1, module="ep01_nasil_ucar", title="Yamaç paraşütü nasıl uçar?"),
    dict(no=2, module="ep02_anatomi", title="Kanadın anatomisi"),
    dict(no=3, module="ep03_ekipman", title="Uçuş ekipmanı"),
    dict(no=4, module="ep04_hucum_acisi", title="Hücum açısı"),
    # MODÜL 2 · METEOROLOJİ
    dict(no=5, module="ep05_ruzgar_tulumu", title="Rüzgarı oku: rüzgar tulumu"),
    dict(no=6, module="ep06_yamac_kaldirmasi", title="Yamaç (dinamik) kaldırması"),
    dict(no=7, module="ep07_termik", title="Termik nedir?"),
    dict(no=8, module="ep08_rotor", title="Rotor ve türbülans"),
    dict(no=9, module="ep09_kumulonimbus", title="Fırtına bulutu: Kümülonimbüs"),
    # MODÜL 3 · KALKIŞ
    dict(no=10, module="ep10_bes_nokta_kontrol", title="Uçuş öncesi 5 nokta kontrol"),
    dict(no=11, module="ep11_onden_kalkis", title="Önden kalkış"),
    dict(no=12, module="ep12_ters_kalkis", title="Ters kalkış"),
    # MODÜL 4 · UÇUŞ TEKNİKLERİ
    dict(no=13, module="ep13_fren_hiz", title="Fren ve hız kontrolü"),
    dict(no=14, module="ep14_donus", title="Dönüş tekniği"),
    dict(no=15, module="ep15_suzulme_speedbar", title="Süzülme oranı ve hızlandırıcı"),
    dict(no=16, module="ep16_kulak_katlama", title="Kulak katlama"),
    # MODÜL 5 · İNİŞ
    dict(no=17, module="ep17_inis_yaklasmasi", title="İniş yaklaşması"),
    dict(no=18, module="ep18_palya", title="Palya (Flare)"),
    dict(no=19, module="ep19_plf", title="PLF: güvenli yuvarlanma"),
    # MODÜL 6 · ACİL DURUMLAR & KURALLAR
    dict(no=20, module="ep20_asimetrik_kapanma", title="Asimetrik kapanma"),
    dict(no=21, module="ep21_onden_kapanma", title="Önden kapanma"),
    dict(no=22, module="ep22_stol_negatif", title="Stol ve negatif"),
    dict(no=23, module="ep23_yedek_parasut", title="Yedek paraşüt atma"),
    dict(no=24, module="ep24_hava_kurallari", title="Hava kuralları ve doğru karar"),
    # MODÜL 7 · TERMİK & NAVİGASYON
    dict(no=25, module="ep25_yer_hizi", title="Hava hızı ve yer hızı"),
    dict(no=26, module="ep26_termikte_donus", title="Termikte dönüş: 5 adım"),
    dict(no=27, module="ep27_termik_bulma", title="Termik nasıl bulunur?"),
    dict(no=28, module="ep28_termik_trafigi", title="Kalabalık termikte kurallar"),
    # MODÜL 8 · İLERİ MANEVRALAR
    dict(no=29, module="ep29_spiral", title="Derin spiral ve tam spiral"),
    dict(no=30, module="ep30_derin_stol", title="Derin stol ve tam stol"),
    dict(no=31, module="ep31_wingover", title="Wingover"),
    # MODÜL 9 · KALKIŞ USTALIĞI
    dict(no=32, module="ep32_kalkis_yollari", title="Kalkışın üç yolu"),
    dict(no=33, module="ep33_kobra_kalkis", title="Kobra kalkış"),
    dict(no=34, module="ep34_yer_hakimiyeti", title="Yer hakimiyeti"),
    dict(no=35, module="ep35_kalkis_oncesi", title="Kalkıştan önce alanı ve rüzgarı oku"),
    dict(no=36, module="ep36_bes_saniye", title="Koşmadan önce 5 saniye"),
    dict(no=37, module="ep37_ip_karisikligi", title="İpler karıştı: nasıl çözülür?"),
    # MODÜL 10 · İNİŞ USTALIĞI
    dict(no=38, module="ep38_inis_planla", title="İnişi havada planla"),
    dict(no=39, module="ep39_fren_konumu", title="Frenin konumu: çeyrek, yarım, tam"),
    # MODÜL 11 · METEOROLOJİ+
    dict(no=40, module="ep40_ruzgari_oku", title="Rüzgarı 5 yoldan oku"),
    dict(no=41, module="ep41_turbulans", title="Türbülans nereden gelir?"),
    dict(no=42, module="ep42_toz_hortumu", title="Toz hortumu"),
    dict(no=43, module="ep43_yagmur", title="Yağmurda uçulur mu?"),
    dict(no=44, module="ep44_irtifa_sicaklik", title="Yükseldikçe neden üşürsün?"),
    dict(no=45, module="ep45_sabah_egitim", title="Eğitim neden sabah erken?"),
    # MODÜL 12 · PİLOT & EKİPMAN
    dict(no=46, module="ep46_kanat_siniflari", title="Kanat sınıfları: A, B, C, D"),
    dict(no=47, module="ep47_ekipman_bakimi", title="Ekipman bakımı: ipler ve yedek"),
    dict(no=48, module="ep48_death_kurali", title="Pilot sağlığı: DEATH kuralı"),
    dict(no=49, module="ep49_notam", title="NOTAM ve hava sahası"),
    dict(no=50, module="ep50_pilot_seviyeleri", title="P2 ve P3: pilotluk seviyeleri"),
    dict(no=51, module="ep51_teori_dersleri", title="Teorik dersler ve ilk uçuş"),
]

MODULES = {
    1: "MODÜL 1 · TEMELLER", 2: "MODÜL 1 · TEMELLER", 3: "MODÜL 1 · TEMELLER", 4: "MODÜL 1 · TEMELLER",
    5: "MODÜL 2 · METEOROLOJİ", 6: "MODÜL 2 · METEOROLOJİ", 7: "MODÜL 2 · METEOROLOJİ", 8: "MODÜL 2 · METEOROLOJİ",
    9: "MODÜL 2 · METEOROLOJİ", 10: "MODÜL 3 · KALKIŞ", 11: "MODÜL 3 · KALKIŞ", 12: "MODÜL 3 · KALKIŞ",
    13: "MODÜL 4 · UÇUŞ", 14: "MODÜL 4 · UÇUŞ", 15: "MODÜL 4 · UÇUŞ", 16: "MODÜL 4 · UÇUŞ",
    17: "MODÜL 5 · İNİŞ", 18: "MODÜL 5 · İNİŞ", 19: "MODÜL 5 · İNİŞ", 20: "MODÜL 6 · ACİL DURUM",
    21: "MODÜL 6 · ACİL DURUM", 22: "MODÜL 6 · ACİL DURUM", 23: "MODÜL 6 · ACİL DURUM", 24: "MODÜL 6 · KURALLAR",
    25: "MODÜL 7 · TERMİK", 26: "MODÜL 7 · TERMİK", 27: "MODÜL 7 · TERMİK", 28: "MODÜL 7 · TERMİK",
    29: "MODÜL 8 · İLERİ MANEVRA", 30: "MODÜL 8 · İLERİ MANEVRA", 31: "MODÜL 8 · İLERİ MANEVRA",
    32: "MODÜL 9 · KALKIŞ+", 33: "MODÜL 9 · KALKIŞ+", 34: "MODÜL 9 · KALKIŞ+", 35: "MODÜL 9 · KALKIŞ+",
    36: "MODÜL 9 · KALKIŞ+", 37: "MODÜL 9 · KALKIŞ+", 38: "MODÜL 10 · İNİŞ+", 39: "MODÜL 10 · İNİŞ+",
    40: "MODÜL 11 · METEOROLOJİ+", 41: "MODÜL 11 · METEOROLOJİ+", 42: "MODÜL 11 · METEOROLOJİ+",
    43: "MODÜL 11 · METEOROLOJİ+", 44: "MODÜL 11 · METEOROLOJİ+", 45: "MODÜL 11 · METEOROLOJİ+",
    46: "MODÜL 12 · PİLOT", 47: "MODÜL 12 · PİLOT", 48: "MODÜL 12 · PİLOT", 49: "MODÜL 12 · PİLOT",
    50: "MODÜL 12 · PİLOT", 51: "MODÜL 12 · PİLOT",
}
