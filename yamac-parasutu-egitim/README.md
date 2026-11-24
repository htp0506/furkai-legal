# Yamaç Paraşütü Eğitim Seti · Derin Yamaç Spor Kulübü

Instagram Reels / YouTube Shorts için **24 derslik**, Türkçe seslendirmeli, animasyonlu yamaç paraşütü eğitim video seti.
Gönderilen *"Palya, yani flare"* reelinin anlatım tarzı (tek konu, kısa ve net cümleler, ikinci tekil şahıs, sonda yorum sorusu)
temel alındı; görsel kalite modernleştirildi ve konu kapsamı temellerden acil durumlara kadar eksiksiz bir müfredata genişletildi.

## Neler eklendi / iyileştirildi?

| Orijinal reel | Bu set |
|---|---|
| Tek konu (palya) | 6 modül, 24 ders: temeller → meteoroloji → kalkış → uçuş → iniş → acil durum ve kurallar |
| Sabit 3D sahneler | Gerçek zamanlı 3D kanat modeli: kapanma, kulak katlama, stol, negatif, fren bükümü, yedek paraşüt |
| Ekran yazısı + altyazı | Kelime kelime vurgulanan altyazı, büyük ekran yazıları, ayrıca `.srt` altyazı dosyası |
| — | Canlı göstergeler: hız, fren yüzdesi, yükseklik, vario |
| — | Her derste **sık yapılan hata / risk** bölümü ve **özet kartı** |
| "Hangi şehrin pilotusun?" | Her derse özel yorum sorusu + kayan cevap seçenekleri + **sonraki ders** yönlendirmesi |
| — | Ders sayacı (DERS 18/24), ilerleme çubuğu, kulüp logosu ve kullanıcı adı |
| — | Güvenlik notu: "Uçuş eğitimini lisanslı eğitmenle al" |
| — | Her ders için hazır Instagram açıklaması ve hashtagler (`SENARYOLAR.md`) |

## Müfredat ve videolar

<!-- TABLO -->
<!-- /TABLO -->

Tüm seslendirme metinleri, ekran yazıları ve Instagram açıklamaları: **[SENARYOLAR.md](SENARYOLAR.md)**

## Teknik özellikler

- 1080×1920 (9:16), 30 fps, H.264 (High) + AAC 48 kHz stereo, ses −14 LUFS (Instagram/YouTube standardı)
- Her video 33–50 sn; Reels için ideal aralık
- Altyazılar Reels arayüzünün güvenli alanında (alt bölüm ve sağ butonlar dışında)

## Kendin üretmek / değiştirmek

```bash
pip install -r requirements.txt
./tools/indir_sesler.sh                 # Türkçe ses modelleri (CC0)
python -m engine.build 18               # tek ders
python -m engine.build all              # tüm set  -> videolar/
python -m engine.build 7 --beat-stills  # her cümleden önizleme karesi (PNG)
python tools/export_docs.py             # SENARYOLAR.md'yi yeniden üret
```

- **Senaryo değiştirmek:** `episodes/epXX_*.py`. Her `beat` bir cümledir: `say` (seslendirilen metin; telaffuz için
  "fler", "spid bar", "pe le fe" gibi yazımlar), `sub` (ekranda görünen altyazı), `k` (büyük ekran yazısı),
  `scene` ve `p` (sahne ve parametreleri).
- **Marka:** `engine/brand.py` ya da ortam değişkenleri: `BRAND_LINE1`, `BRAND_LINE2`, `BRAND_HANDLE`, `BRAND_LOGO`.
- **Ses:** `TTS_VOICE=tr_TR-fahrettin-medium` ile daha pes bir erkek sesine geçilebilir. Varsayılan: `tr_TR-fettah-medium`.
- **Müzik:** `assets/music/muzik_ana.mp3` (her ders parçanın farklı bir bölümünü kullanır).

## Yapı

```
engine/          render motoru (Skia + NumPy, ffmpeg)
  glider3d.py    3D kanat + pilot modeli (kapanma, kulak, stol, fren, hızlandırıcı)
  world.py       gökyüzü, dağlar, bulut, rüzgar tulumu, termik, rotor, kümülonimbüs
  ui.py          üst bilgi, ilerleme çubuğu, ekran yazıları, karaoke altyazı
  audio.py       Türkçe TTS (Piper), ses efektleri, müzik miksajı ve loudnorm
  scenes/        sahne türleri (uçuş, kesit, yamaç, termik, kalkış, pist düzeni, trafik, PLF...)
episodes/        24 dersin senaryoları
videolar/        üretilmiş MP4 ve SRT dosyaları
```

## Kaynaklar ve lisanslar

- Seslendirme: [Piper](https://github.com/rhasspy/piper) Türkçe "fettah" sesi, veri seti CC0
- Müzik: yapay zekâ ile üretilmiş, telifsiz enstrümantal parça
- Yazı tipi: Inter (SIL Open Font License), emoji: Noto Color Emoji (SIL OFL)
- Logo: Derin Yamaç Spor Kulübü

> **Önemli:** İçerik genel eğitim bilgisidir ve yayından önce kulübün eğitmeni tarafından gözden geçirilmelidir.
> Rüzgar limitleri, kanat hızları ve acil durum prosedürleri kanada ve eğitim kurumuna göre değişebilir.
