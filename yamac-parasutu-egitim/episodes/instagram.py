"""Instagram açıklama metinleri ve hashtag'ler (Ders 1-51).

Instagram 2025 sonunda gönderi başına hashtag sınırını 5'e indirdiğini duyurdu;
bu yüzden her derste 3 sabit + 2 konuya özel = 5 hashtag var.
"""
from . import SERIES

TOTAL = len(SERIES)
BASE_TAGS = ["#yamaçparaşütü", "#paragliding", "#merzifon"]
MODULE_NAMES = [
    ("Temeller", range(1, 5)), ("Meteoroloji", range(5, 10)), ("Kalkış", range(10, 13)),
    ("Uçuş Teknikleri", range(13, 17)), ("İniş", range(17, 20)), ("Acil Durumlar ve Kurallar", range(20, 25)),
    ("Termik ve Navigasyon", range(25, 29)), ("İleri Manevralar", range(29, 32)), ("Kalkış Ustalığı", range(32, 38)),
    ("İniş Ustalığı", range(38, 40)), ("Meteoroloji+", range(40, 46)), ("Pilot ve Ekipman", range(46, 52)),
]

# no: (ilk satır, maddeler, ek satır veya "", yorum sorusu, [2 konu etiketi])
# Madde "1 · ..." ile başlıyorsa numaralı emoji, "x ..." ile başlıyorsa ❌, diğerleri ✅ alır.
CAPTIONS = {
    1: ("Motoru yok. Peki yamaç paraşütü nasıl uçuyor?",
        ["Kanat şeklini içindeki havadan alır", "İleri hız kaldırma kuvveti yaratır",
         "Sakin havada sürekli süzülürsün", "Yükselen hava seni yukarı taşır"], "",
        "İlk uçuşun nerede oldu?", ["#aerodinamik", "#uçuşokulu"]),
    2: ("Kanadını parça parça tanımadan, ona güvenemezsin.",
        ["Hücum kenarı ve hücre ağızları", "Firar kenarı: frenle bükülür",
         "A · B · C ve fren hatları", "Askılar ve karabinalar"], "",
        "Senin kanadının rengi ne?", ["#paraglider", "#ekipman"]),
    3: ("Uçuş çantanda bunlar yoksa, kalkışa çıkma.",
        ["1 · Sertifikalı ve tam oturan kask", "2 · Korumalı oturak (harness)", "3 · Her uçuşta takılı yedek paraşüt",
         "4 · Telsiz", "5 · Vario", "6 · Bot, eldiven ve kanca bıçağı"],
        "Yedek paraşütünü 6–12 ayda bir katlatmayı unutma.",
        "Çantanda olmazsa olmaz ne var?", ["#ekipman", "#güvenlik"]),
    4: ("Kanadının en önemli ayarı: hücum açısı.",
        ["Veter ile bağıl rüzgar arasındaki açı", "Fren çek: açı büyür, kanat yavaşlar",
         "Aşırı açı: stol", "Çok küçük açı: kapanma"], "",
        "Sence en zor teknik hangisi?", ["#aerodinamik", "#uçuşokulu"]),
    5: ("Kalkıştan önce ilk bakacağın yer: rüzgar tulumu.",
        ["Tulum rüzgarın geldiği yönü gösterir", "Kalkış ve iniş rüzgara karşı yapılır",
         "Sarkık · yarı şişkin · dimdik: şiddeti okur", "Düzensiz ve sert esiyorsa uçma"], "",
        "Senin sahanda rüzgar nereden eser?", ["#rüzgar", "#meteoroloji"]),
    6: ("Rüzgar dağa çarptığında sana bedava yükseklik verir.",
        ["Rüzgar yamaca çarpar, yukarı yönelir", "Kaldırma bandı: yamacın önü ve üstü",
         "Dönüşler her zaman yamaçtan dışarı", "Rüzgar artarsa: geri sürüklenme ve rotor"], "",
        "En sevdiğin yamaç sahası hangisi?", ["#soaring", "#meteoroloji"]),
    7: ("Bulutlara kadar yükselmenin yolu: termik.",
        ["Güneş zemini farklı ısıtır", "Sıcak hava baloncuk gibi yükselir",
         "Daire çiz, varioyu dinle", "Kümülüs bulutu termiğin işaretidir"], "",
        "Termikle en yüksek kaç metreye çıktın?", ["#termik", "#thermal"]),
    8: ("Gökyüzünde görünmeyen bir girdap var: rotor.",
        ["Engelin arkasında dönen hava: rotor", "Dağ, ağaç, bina: hepsi rotor yapar",
         "Rüzgar arttıkça rotor büyür", "Rüzgaraltından uzak dur"], "",
        "Hiç rotora girdin mi?", ["#rotor", "#türbülans"]),
    9: ("Bu bulutu gördüysen, hemen in.",
        ["Dikey büyüyen, kararan bulut", "Örs şekli: kümülonimbüs",
         "Bulut emmesi ve ani rüzgar cephesi", "İlk işarette in, bekleme"], "",
        "Hava bozarken ilk neye bakarsın?", ["#meteoroloji", "#fırtına"]),
    10: ("Kalkıştan önce on saniye. Hayat kurtaran beş kontrol.",
         ["1 · Kask takılı, çene kayışı bağlı", "2 · Bacak ve göğüs tokaları kapalı",
          "3 · Yedek pimleri yerinde, kolu erişilebilir", "4 · Hatlar açık; askılar ve frenler doğru tarafta",
          "5 · Rüzgar uygun, önün ve hava sahası boş"],
         "Her uçuşta aynı sırayla, yüksek sesle say.",
         "Sen kontrol listeni nasıl yapıyorsun?", ["#güvenlik", "#checklist"]),
    11: ("Hafif rüzgarda kalkışın adı: önden kalkış.",
         ["Hilal serim, sırtın kanada dönük", "Öne eğil, kararlı koş",
          "Kanat tepedeyken kontrol et", "Şüphe varsa kalkışı iptal et"], "",
         "İlk kalkışında kaç deneme yaptın?", ["#kalkış", "#uçuşokulu"]),
    12: ("Rüzgar artınca yüzünü kanadına dön: ters kalkış.",
         ["Kanada dönük dur, askılar çapraz", "A askılarını yumuşak çek",
          "Kanat tepede: frenle durdur", "Dön ve rüzgara karşı kalk"], "",
         "Yer hakimiyetine haftada kaç saat ayırıyorsun?", ["#terskalkış", "#groundhandling"]),
    13: ("Ellerin yukarıdaysa hızlısın, aşağıdaysa yavaşsın.",
         ["Eller yukarı: trim hızı", "Biraz fren: minimum batış",
          "Derin fren: stol sınırı", "Türbülansta hafif fren"], "",
         "Kanadının trim hızını biliyor musun?", ["#uçuştekniği", "#aktifpilotaj"]),
    14: ("Güzel bir dönüş üç adımdır: bak, ağırlık ver, fren çek.",
         ["Bak: hava sahası boş mu?", "Ağırlığını dönüş tarafına ver",
          "İç fren yumuşak, dış fren destek", "Sert ve ani fren yok"], "",
         "Sağa mı sola mı dönmek daha rahat?", ["#uçuştekniği", "#pilotaj"]),
    15: ("Bin metreden kaç kilometre uzağa gidebilirsin?",
         ["Süzülme 1:9 → 1000 m'den ≈ 9 km", "Karşı rüzgar mesafeyi kısaltır",
          "Hızlandırıcı: açı azalır, hız artar", "Türbülansta ve alçakta hızlandırıcı kullanma"], "",
         "En uzun süzülüşün kaç km?", ["#speedbar", "#süzülme"]),
    16: ("Hızlıca alçalman gerektiğinde ilk tekniğin: kulak katlama.",
         ["Dış A hatlarını çek: uçlar katlanır", "Alçalma hızı artar",
          "Yönü ağırlıkla verirsin", "İnişten önce bırak"], "",
         "Kulak katlamayı ilk nerede denedin?", ["#bigears", "#kulakkatlama"]),
    17: ("İyi iniş, iniş alanına varmadan başlar.",
         ["İniş her zaman rüzgara karşı", "Fazla yüksekliği 8 çizerek erit",
          "Rüzgaraltı → baz → final", "Alçakta dönüş yok"], "",
         "İniş alanında en zor şey ne?", ["#iniş", "#landing"]),
    18: ("Palya, yani flare. Yumuşak inişin sırrı.",
         ["Finalde eller yukarı, dik pozisyon", "Dalışa kontra: yeterli fren",
          "Kademeli palya, yere değerken tam fren", "Zamanlamayı eğitmenle çalış"], "",
         "Hangi şehrin pilotusun?", ["#palya", "#iniş"]),
    19: ("İnişin sert olacaksa, düşmeyi bilmek seni korur.",
         ["Ayaklar ve dizler bitişik", "Dizler hafif bükük",
          "Ayak → baldır → kalça → sırt", "Elle yere dayanma"],
         "Yerde, alçak bir basamaktan atlayarak çalış.",
         "Sen hiç PLF çalıştın mı?", ["#plf", "#güvenlik"]),
    20: ("Kanadının bir tarafı aniden kapandı. Ne yaparsın?",
         ["Önce yön: ağırlık açık tarafa", "Açık tarafa dozunda fren",
          "Aşırı fren yok", "Sonra kapanan tarafı pompala"], "",
         "Hiç kapanma yaşadın mı?", ["#kapanma", "#sivkursu"]),
    21: ("Kanadının ön kenarı bir anda içe katlandı!",
         ["Düşük hücum açısı: ön kenar katlanır", "Çoğu kanat kendiliğinden açılır",
          "Kısa simetrik fren, dalışa kontra", "Önlem: aktif pilotaj"], "",
         "Aktif pilotajı nasıl öğrendin?", ["#kapanma", "#aktifpilotaj"]),
    22: ("Kanadı durduran şey: fazla fren.",
         ["Derin fren: tam stol", "Belirti: yumuşayan fren, sessizlik",
          "Tek tarafa fazla fren: negatif", "Önlem: alçakta yavaş uçma"], "",
         "Sence en tehlikeli hata hangisi?", ["#stol", "#sivkursu"]),
    23: ("Her şey ters gittiyse son çaren: yedek paraşüt.",
         ["Tereddüt etme", "Bak · Tut · Çek · At",
          "Ana kanadı topla", "PLF ile in ve düzenli çalış"], "",
         "Yedeğini en son ne zaman katlattın?", ["#yedekparaşüt", "#güvenlik"]),
    24: ("Gökyüzünün de trafik kuralları var.",
         ["Karşılaşmada ikiniz de sağa", "Yamaç sağınızdaysa öncelik sizde",
          "Termikte ilk girenin yönüne dön", "Alçaktaki pilot önceliklidir"], "",
         "Hangi ders sana en çok yardım etti?", ["#havakuralları", "#güvenlik"]),
    25: ("Hava hızı ile yer hızı aynı şey değil.",
         ["Kanat havaya göre hep aynı hızda uçar", "Karşı rüzgar yer hızını düşürür",
          "Arka rüzgar yer hızını artırır", "Rüzgar hava hızından fazlaysa geri gidersin"], "",
         "Hiç geri gittiğin oldu mu?", ["#rüzgar", "#uçuştekniği"]),
    26: ("Termiği buldun. Şimdi doğru dönmenin beş adımı.",
         ["Dar daire, termiğin içinde", "İç fren ve ağırlık içeri",
          "Hızını koru, stola yaklaşma", "Daireyi rüzgarla birlikte kaydır"], "",
         "Termikte hangi yöne dönmeyi seversin?", ["#termik", "#thermalling"]),
    27: ("Termik görünmez ama izini bırakır. İşte beş ipucu.",
         ["1 · Daire çizen kuşlar ve kanatlar", "2 · Güneşe bakan yamaçlar ve kayalıklar",
          "3 · Kümülüs bulutunun tabanı", "4 · Havalanan toz ve yapraklar",
          "5 · Vario ötmeye başladığı yerde daireye gir"], "",
         "Termiği en çok neyle bulursun?", ["#termik", "#xc"]),
    28: ("Aynı termikte on pilot varsa ne yaparsın?",
         ["1 · Girmeden önce bak: kaç kişi, hangi yön?", "2 · İlk girenle aynı yöne dön",
          "3 · Alttaki pilot önceliklidir", "4 · Sürüklenmeyi ve iniş alanını takip et",
          "5 · Çok kalabalıksa başka termik ara"], "",
         "Aynı termikte en fazla kaç kişi oldunuz?", ["#termik", "#havakuralları"]),
    29: ("En hızlı alçalma yöntemi: spiral. Peki bedeli ne?",
         ["Derin spiral: 10–20 m/s alçalma", "Tam spiral: ≈ 90° yatış",
          "4 G üstü: bilinç kaybı riski", "Çıkış en geç 300 m'de biter"],
         "Spirali yalnızca eğitmen eşliğinde, güvenlik kursunda çalış.",
         "Spirali hiç denedin mi?", ["#spiral", "#sivkursu"]),
    30: ("Derin stol ile tam stol aynı şey mi?",
         ["Derin stol: kanat şekilli ama ileri gitmez", "Islak kanat, aşırı fren, yıpranmış kumaş tetikler",
          "Tam stol: kanat şeklini kaybeder, arkaya yıkılır", "Derin stolden çıkış: eller yukarı, gerekirse A'ları hafif it"],
         "Tam stolü yalnızca eğitmenle çalış.",
         "Hangisini daha tehlikeli buluyorsun?", ["#stol", "#sivkursu"]),
    31: ("Kanat neden sağa sola sallanıyor? Buna wingover denir.",
         ["Frenlerle sarkaç gibi salınım", "Her salınımda yatış ve hız artar",
          "Zamanlama kaçarsa kapanma riski", "Önce güvenlik kursu (SIV) ve eğitmen"], "",
         "Akro uçuşa ilgin var mı?", ["#wingover", "#akro"]),
    32: ("Kalkışın üç yolu var. Hangisi ne zaman?",
         ["Hafif rüzgar: önden (düz) kalkış", "Güçlü rüzgar: ters kalkış",
          "Dar alan ve deneyim: kobra", "Seçimi rüzgar ve alan belirler"], "",
         "Senin favori kalkışın hangisi?", ["#kalkış", "#groundhandling"]),
    33: ("Kobra kalkış: kanat yandan kalkar.",
         ["Kanat yanda, istifli; bir ucu açık", "Bir elde A kolonu, diğerinde fren",
          "Öne giderse fren, geri düşerse A", "Tepede kontrol et, dön ve kalk"],
         "İleri seviyedir: önce düz ve ters kalkışta ustalaş.",
         "Kobra kalkışı denedin mi?", ["#kobrakalkış", "#groundhandling"]),
    34: ("Pilot olmak istiyorsan, önce kanadı yerde evcilleştirirsin.",
         ["1 · Şişir: kanadı başının üstüne getir", "2 · Tut: önce 10, sonra 30 saniye",
          "3 · Düzelt: altına adım at, frenle dengele", "4 · Söndür: kontrollü indir"],
         "Yer hakimiyeti iyi olanın kalkışı da inişi de sakindir.",
         "Kanadı tepede kaç saniye tutabiliyorsun?", ["#groundhandling", "#yerhakimiyeti"]),
    35: ("Kalkıştan önce dört kontrol. Sonra hazırsın.",
         ["1 · Alan temiz mi? Taş, diken, çalı", "2 · Rüzgarı en az 5 dakika izle",
          "3 · Stili seç: hafifte düz, güçlüde ters", "4 · Kanadı ser; hat ve askıları kontrol et"],
         "Rüzgar istikrarlı değilse bekle. Beklemek de bir karardır.",
         "Kalkışta en uzun ne kadar bekledin?", ["#kalkış", "#güvenlik"]),
    36: ("Kanat tepede. Hemen koşma: önce beş saniye.",
         ["1 · Kanat tamamen dolu mu?", "2 · İpler düzgün, düğüm yok mu?",
          "3 · Omzunun üstünden bak: trafik var mı?", "4 · Fren ve askılar doğru elde mi?",
          "5 · Her şey tamamsa kalk"],
         "Bir şey yolunda değilse vazgeç. Vazgeçmek de beceridir.",
         "Kalkıştan vazgeçtiğin oldu mu?", ["#kalkış", "#güvenlik"]),
    37: ("İpler karıştı. Nereden başlarsın?",
         ["x Düğümü ortadan ya da yukarıdan çözmek", "x Harnesi iplerin arasından geçirmek",
          "Kanadı rüzgarsız yere çek, sakince yay", "Askılardan başla, her ipi aşağıdan yukarı takip et",
          "Fren ipini firar kenarına kadar kontrol et"],
         "İçinde şüphe kalan bir düğüm varsa uçma.",
         "İp karışıklığını en hızlı kim çözer?", ["#ekipman", "#groundhandling"]),
    38: ("İnişi yere gelmeden planla.",
         ["200 m altında ≈ 2 dakikan var", "Düz, büyük, engelsiz alan seç",
          "Dönüşler yüksekte, final uzun", "Her zaman bir yedek alan"], "",
         "Senin yedek iniş alanın neresi?", ["#iniş", "#landing"]),
    39: ("Fren konumunu nereden anlarsın? Ellerinin yüksekliğinden.",
         ["Eller yukarı: trim hızı", "Çeyrek fren: omuz hizası",
          "Yarım fren: göğüs hizası", "Tam fren: kalça hizası, stol riski"],
         "Normal uçuşta çeyrek ile yarım fren arası; tam fren sadece palyanın sonunda.",
         "Uçarken ellerin genelde nerede?", ["#fren", "#uçuştekniği"]),
    40: ("Rüzgarı hangi beş yoldan okursun?",
         ["1 · Rüzgar tulumu: yön ve şiddet", "2 · T panosu: sadece yön",
          "3 · Ağaçların yatışı", "4 · Dumanın gidişi ve eğimi", "5 · Su yüzeyindeki kırışıklık"],
         "Standart tulum yarı açık ≈ 10 km/sa, neredeyse yatay ≈ 20 km/sa.",
         "Rüzgarı en çok neyle okursun?", ["#rüzgar", "#meteoroloji"]),
    41: ("Türbülans nereden gelir? Üç ana kaynaktan.",
         ["Termik: ısınan hava", "Yeryüzü şekilleri: rotor",
          "Rüzgar kırılması", "Çözüm: hafif fren, aktif pilotaj"], "",
         "En sert türbülansı nerede yaşadın?", ["#türbülans", "#meteoroloji"]),
    42: ("Kalkış alanında bir anda hortum çıkabilir mi? Evet: toz hortumu.",
         ["Sıcak, güneşli ve rüzgarsız günlerde oluşur", "Dönen sıcak hava toz ve otu kaldırır",
          "Yerdeysen kanadı söndür, üstüne çök, bekle", "Havadaysan uzak dur: çevresi sert termik"], "",
         "Hiç toz hortumu gördün mü?", ["#tozhortumu", "#meteoroloji"]),
    43: ("Yağmurda uçulur mu?",
         ["Hafif yağmurda bile en doğrusu inmek", "Su kanadın içine dolar, kanat ağırlaşır",
          "Islak kanat derin stola yatkındır", "Derin fren yok: hızını koru, ilk uygun yere in"],
         "Islak kanadı katlayıp bekletme; gölgede, açık havada kurut.",
         "Yağmura yakalandığın oldu mu?", ["#yağmur", "#güvenlik"]),
    44: ("Yükseldikçe neden üşürsün?",
         ["Yükseldikçe basınç düşer, hava soğur", "Her 1000 m'de ≈ 6,5 °C düşüş",
          "Yerde 25 °C ise 2000 m'de ≈ 12 °C", "Uçuş rüzgarı hissedileni daha da düşürür"],
         "Sıcak günde bile eldiven, rüzgarlık ve boyunluk al.",
         "Havada en çok neren üşür?", ["#meteoroloji", "#irtifa"]),
    45: ("Eğitim neden sabahın erken saatinde başlar?",
         ["Sabah: serin ve sakin", "Kuşluk: termikler başlar",
          "Öğle: türbülans artar", "Akşamüstü: hava yine sakinleşir"], "",
         "Sabah mı akşam mı uçmayı seversin?", ["#meteoroloji", "#uçuşeğitimi"]),
    46: ("Kanatlar dört sınıfa ayrılır. Hangisinden başlarsın?",
         ["A: en affedici; eğitim ve ilk yıllar", "B: biraz daha hızlı ve hassas",
          "C: performans; deneyimli pilotlar", "D: yarışma ve uzman kanadı"],
         "Kanadını egon değil, uçuş saatin ve becerin seçsin.",
         "Senin kanadın hangi sınıf?", ["#paraglider", "#ekipman"]),
    47: ("Ekipmanın da bakım ister. İşte dört kural.",
         ["1 · İpler: çoğu kanatta ≈ 100 saatte bir kontrol", "2 · Yedek: 6–12 ayda bir yetkili kişi katlasın",
          "3 · UV: kanadı güneşte bekletme", "4 · Nem: ıslak kanadı kurutmadan katlama"], "",
         "Kanadını en son ne zaman kontrol ettirdin?", ["#ekipman", "#bakım"]),
    48: ("Uçmadan önce beş harflik kuralı hatırla: DEATH.",
         ["D · İlaç (Drugs): uyku yapanı bile tepkini yavaşlatır", "E · Yorgunluk (Exhaustion): uykusuz pilot yanlış karar verir",
          "A · Alkol (Alcohol): uçuştan önce asla", "T · Tütün (Tobacco): kandaki oksijeni azaltır",
          "H · Açlık (Hunger): yanına su ve atıştırmalık al"],
         "Bunlardan biri bile varsa, o gün uçma.",
         "Uçmadan önce ne yersin?", ["#pilotsağlığı", "#güvenlik"]),
    49: ("Pilotlar uçmadan önce bir duyuru okur: NOTAM.",
         ["NOTAM: havacılara yapılan resmi duyuru", "Geçici kapanan bölgeleri bildirir",
          "Yasak, tehlikeli, kısıtlı bölgelere izinsiz girme", "Havaalanı ve kontrollü hava sahasından uzak dur"],
         "Uçmadan önce kontrol et; emin değilsen eğitmenine sor.",
         "NOTAM'ı daha önce duymuş muydun?", ["#notam", "#havasahası"]),
    50: ("P2 mi, P3 mü? Fark tek cümle: tek başına uçmak.",
         ["P2: eğitmen eşliğinde uçan öğrenci pilot", "P3: kendi kararını veren, tek başına uçan pilot",
          "P2 sonunda kurs belgesi, P3 sonunda pilot kartı", "Güncel şartları kulübünden öğren"],
         "Her seviye bir öncekinin üstüne kurulur. Acele etme.",
         "Hangi seviyedesin?", ["#uçuşokulu", "#pilotluk"]),
    51: ("Yamaç paraşütünün de dersleri var: tam altı tane.",
         ["Tarih, ekipman, aerodinamik", "Sevk ve idare, hava trafik kuralları, meteoroloji",
          "Yazılı sınav: geçme notu %75", "Başlangıçta 75–600 m'lik tepeler"],
         "Unutma: dağlar yarın da orada olacak.",
         "Teori derslerinden hangisi en zor?", ["#uçuşokulu", "#ilkuçuş"]),
}

_NUM = {"1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣", "5": "5️⃣", "6": "6️⃣"}


def module_of(no):
    for i, (name, r) in enumerate(MODULE_NAMES, 1):
        if no in r:
            return i, name
    raise KeyError(no)


def _bullet(item):
    if item[:1] in _NUM and item[1:4] == " · ":
        return f"{_NUM[item[0]]} {item[4:]}"
    if len(item) > 4 and item[0].isupper() and item[1:4] == " · ":
        return f"🔸 {item}"
    if item.startswith("x "):
        return f"❌ {item[2:]}"
    return f"✅ {item}"


def hashtags(no):
    return " ".join(BASE_TAGS + CAPTIONS[no][4])


# Akışta ilk görünen satır: emojili, büyük harfli dikkat çekici başlık.
HEADLINES = {
    1: "🪂 MOTORSUZ UÇMANIN SIRRI", 2: "🧩 KANADIN İÇİNDE NELER VAR?", 3: "🎒 UÇUŞ ÇANTASI KONTROLÜ",
    4: "📐 KANADIN GİZLİ AYARI", 5: "🌬️ RÜZGARI OKUMAYAN UÇAMAZ!", 6: "⛰️ SAATLERCE HAVADA KALMANIN SIRRI",
    7: "☀️ GÜNEŞ SENİ NASIL YÜKSELTİR?", 8: "🌀 DAĞIN ARKASINDA NE SAKLANIR?",
    9: "⛈️ GÖKYÜZÜNÜN EN TEHLİKELİ BULUTU", 10: "✅ HER UÇUŞTA 5 KONTROL, İSTİSNASIZ!",
    11: "🏃 KOŞ, KALK, UÇ!", 12: "🔄 RÜZGAR SERTLEŞTİ Mİ?", 13: "🎚️ HIZIN ELLERİNDE!",
    14: "↪️ KUSURSUZ DÖNÜŞÜN FORMÜLÜ", 15: "📏 1000 METREDEN 9 KİLOMETRE!", 16: "👂 KANADA KULAK VER: BIG EARS",
    17: "🛬 8 ÇİZ, RÜZGARA DÖN, YUMUŞAK İN", 18: "🦶 TÜY GİBİ İNİŞİN SIRRI", 19: "🤸 DÜŞMEYİ BİLEN PİLOT KAZANIR",
    20: "⚠️ BİR TARAF KAPANDI: PANİK YOK!", 21: "😱 KANADIN ÖNÜ ÇÖKTÜ!", 22: "🛑 FRENİ FAZLA ÇEKERSEN NE OLUR?",
    23: "🆘 HAYATINI KURTARACAK 4 HAREKET", 24: "🚦 HAVADA KİMİN YOLU ÖNCE?", 25: "💨 RÜZGARDA GERİ GİTMEK MÜMKÜN MÜ?",
    26: "🌀 TERMİKTE KUSURSUZ DAİRE", 27: "🔍 GÖRÜNMEYENİ GÖRMEK: TERMİK AVI", 28: "👥 TERMİKTE ÇARPIŞMAMANIN 5 KURALI",
    29: "🌪️ EN HIZLI ALÇALMA, EN BÜYÜK RİSK", 30: "🧊 KANAT HAVADA DURURSA?", 31: "🎢 GÖKYÜZÜNDE SALINCAK: WINGOVER",
    32: "🛫 RÜZGAR SEÇER, SEN KALKARSIN", 33: "🐍 USTALARIN KALKIŞI: KOBRA", 34: "🐎 İYİ PİLOT YERDE BELLİ OLUR",
    35: "👀 ÖNCE GÖZLE, SONRA UÇ", 36: "⏱️ KALKIŞI KURTARAN 5 SANİYE", 37: "🪢 EN SİNİR BOZUCU AN: İP KARIŞIKLIĞI",
    38: "🗺️ 200 METREDE 2 DAKİKAN VAR!", 39: "✋ ELLERİN NEREDE, KANADIN ÖYLE UÇAR", 40: "🌬️ TULUM YOKSA RÜZGARI NASIL OKURSUN?",
    41: "🌊 HAVA NEDEN SARSAR?", 42: "🌪️ SICAK GÜNLERİN SİNSİ TEHLİKESİ", 43: "🌧️ ISLAK KANAT = TEHLİKE!",
    44: "🥶 YAZ ORTASINDA HAVADA ÜŞÜMEK", 45: "🌅 ERKEN KALKAN PİLOT KAZANIR!", 46: "🏷️ HANGİ KANATLA BAŞLAMALI?",
    47: "🔧 100 SAATTE BİR NE YAPILIR?", 48: "☠️ BU 5 ŞEYDEN BİRİ VARSA UÇMA!", 49: "📢 HER PİLOTUN BİLMESİ GEREKEN: NOTAM",
    50: "🎓 PİLOTLUKTA SEVİYE ATLAMAK", 51: "📖 ALTI DERS, BİR SINAV, İLK UÇUŞ!",
}


def caption(no):
    first, items, extra, question, _ = CAPTIONS[no]
    title = next(e["title"] for e in SERIES if e["no"] == no)
    mi, mname = module_of(no)
    lines = [HEADLINES[no], "", f"{first} 👇", "",
             f"📚 Ders {no:02d}/{TOTAL} · {title}", f"🗂️ Modül {mi}: {mname}", ""]
    lines += [_bullet(i) for i in items]
    if extra:
        lines += ["", f"👉 {extra}"]
    lines += ["", f"💬 {question} Yorumlara yaz!",
              "🔖 Kaydet, uçuştan önce tekrar izle.",
              "🔔 Serinin tamamı için takip et.",
              "📍 Derin Yamaç Spor Kulübü · Merzifon",
              "⚠️ Bilgilendirme amaçlıdır; uçuş eğitimini lisanslı eğitmenle al.",
              "", hashtags(no)]
    return "\n".join(lines)


if __name__ == "__main__":
    assert set(CAPTIONS) == set(range(1, TOTAL + 1)), "eksik ders"
    assert set(HEADLINES) == set(CAPTIONS), "eksik başlık"
    for n in range(1, TOTAL + 1):
        assert len(BASE_TAGS + CAPTIONS[n][4]) == 5
    print(caption(18))
    print(max(len(caption(n)) for n in CAPTIONS), "karakter (en uzun)")
