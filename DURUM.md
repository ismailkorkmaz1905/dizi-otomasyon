# Son durum ve notlar (20 Kasım 2026)

Yeni bir Claude oturumu buradan devam edecekse önce bunu, sonra `ceviri/YONTEM.md`'yi okusun. Akışın kendisi `README.md`'de.

## Diziler

| Dizi | `dizi` değeri | Son teslim | Yayın | YouTube'a düşme | Otomatik arama |
|---|---|---|---|---|---|
| Muhtemel Aşk | `muhtemel_ask` | S01E22 (20 Kasım) | perşembe gecesi | cuma 01:00-01:04 TR | var (`bolum.yml` cron), ama güvenilmez |
| Başkalarının Hayatı | `baskalarinin_hayati` | S01E07 (15 Kasım) | cumartesi 20:00 Star TV | gece 23:30-00:30 TR (E3: 00:16, E4: 23:39, E5: 04:34 SGT = 23:34 TR) | **yok**, elle başlat |
| Yeraltı | `yeralti` | - | - | - | 16 Ekim'de takipten çıktı |

## Bölüm nasıl başlatılır

1. Actions > "1 - Bölüm hazırla" > Run workflow: `is = hazirla`, `dizi = ...`, `bolum` = numara (ör. `6`) ya da boş (sıradaki).
   - Bölüm YouTube'da yoksa iş "Yeni bolum yok" deyip biter, kredi harcamaz.
   - `bolum = bekle`: ~100 dk boyunca 5 dk'da bir bakar.
   - "kontrol" işi bölümün çıkıp çıkmadığını **söylemez** ("YouTube son bolum" satırı hep 1. bölümü gösteriyor).
2. Hazırlık `bolumler/<dizi>/SxxEyy/ceviri_girdi.txt`'yi `main`'e koyar. Çeviri `ceviri/YONTEM.md`'ye göre yapılır.
3. `ceviri.txt` `main`'e push edilince "2 - Yak ve gönder" kendiliğinden başlar, Telegram'a gönderir, Drive'a yazar, temizlik yapar.

## Krediler ve kotalar

- **Scribe (ElevenLabs):** iki anahtar var, kod kredisi olanı seçer. 8 Kasım: kalan 36.745 / 40.000 kredi (yenilenme 06.12.2026), diğer anahtarda 2.062. Bölüm başına 2.900-3.700 kredi.
- **Google Drive:** 25 Ekim'de dolmuştu (yükleme `403 Forbidden`), İsmail depolamayı yükseltti, sonra sorunsuz.
- **Claude:** çeviri İsmail'in plan limitinden harcar. Her bölüm yeni thread'de çevrilir; token kuralları `ceviri/YONTEM.md`'nin başında.

## Son değişiklikler

- **ffmpeg (20 Kasım):** apt yerine BtbN statik ffmpeg 8.1 (sabit sürüm, libass ve x264 içinde), `.github/actions/ffmpeg/`. Cache'te sabit anahtarla durur (`ffmpeg-statik-8.1-20261119`), yoksa github.com'dan ~10 sn'de iner; o da olmazsa apt (2. denemede bütün mirror'lar `archive.ubuntu.com` olur). Neden: 20 Kasım'da MA S01E22 yakmasında yeni runner image'i (AWS, `us-east-2.ec2` mirror'ı) eski cache anahtarını bulamadı, apt iki denemede 13 dk sonra düştü; aynı gün testte apt 14,5 dk sürüp yine düştü, statik 10 sn. Test: font Liberation Sans seçiliyor, parçalar birleşiyor. Gerçek yakmada henüz denenmedi (ilk: BH S01E08). `yak.yml`'de `fail-fast: false`: bir parça düşerse diğerleri biter, sadece o tekrar çalışır.
- **Otomatik arama (20 Kasım):** `bolum.yml` cron'u 14 Kasım'dan beri hiç çalışmadı (`cerez.yml` cron'u çalışıyor). MA S01E22 elle başlatıldı. 15 Ekim'de aynı durum İsmail'in github.com'dan `bolum.yml`'e attığı tek satırlık commit'le düzelmişti. Perşembe gecesi MA için hazırlığı elle başlatmak gerekebilir.
- **YouTube çerezi:** 16 Kasım'dan beri ölü, yenilenmedi. Hazırlık WARP ile çerezsiz indiriyor (S01E22: 9 dk).
- **YONTEM.md (10 Kasım):** parça başına ~450 satır (4-5 ajan), ajanlar sadece kendi `girdi_<k>.txt` dosyasını okur, kontrol ajanı sadece değişen satırları yazar (`ceviri/arac.py`). Kontrol effort'u başta sorulur, cevap beklenmez; yoksa `medium`. Kıyas için iki turda düzeltilen satırlar: E3 95+30, E4 83+62, MA E19 135+22, E5 83+19 (Opus çevirmen, `medium`); BH E6 307+59 (Sonnet çevirmen).

## Bilinen tuhaflıklar

- **YouTube çerezi (15 Kasım, S01E07):** hazırlık "Sign in to confirm you're not a bot" ile düşerse çerez ölmüştür. Girişsiz alınan çerez (~1,2 KB) işe yaramaz, girişli çerez ~20 KB olur. Girişli çerezle arama kişiselleşip bölümü listelemeyebiliyor ("Yeni bolum yok"); `otomasyon.py` bu durumda aramayı çerezsiz tekrarlar. Hazırlığı başlattıktan 2 dk sonra işin durumuna bak, sadece girdi dosyasını bekleme.
- **Cron:** `bolum.yml` cron'u bazen hiç tetiklenmiyor (22 Ekim akşamı çalışmadı, elle başlatıldı). Dosyanın başındaki nota bak.
- **Hazırlık işi kırmızı ama girdi gelmiş:** commit, Drive yüklemesinden önce yapılıyor. Drive hatası işi kırmızı yapar ama çeviri ve yakma etkilenmez.
- **YouTube Premium akışı:** S01E19 ve S01E05'te "Premium 1080p akışını sunmadı, standart akış iniyor" uyarısı çıktı (h264 ~1,55 Mbps; E3/E4 Premium vp9 ~1,7-1,8 Mbps). Nedeni araştırılmadı.
- **Ses tanıma hataları:** Muhtemel Aşk'ta "Kader" (Ali'nin annesi) ile "Kadir" (dayı) karışıyor. Başkalarının Hayatı'nda "Betiş" diye biri yok, "Mediş" (Mediha). Salih'in Hülya lakabı "kecoak hitam".
- **Başkalarının Hayatı'nda satır az:** dakikada ~60 kelime (Muhtemel Aşk ~86), bölümler daha kısa. E5: 1584 satır, 127 dk. Normal.
- **E5 satır 571** (flashback, "Anne... sen, ben, ablam"): kontrol ajanı kaynağa döndü, ilk çeviri "Kak... kamu, aku, Mama" idi. Sahne izlenerek doğrulanmadı.

## GitHub erişimi

- YONTEM'deki `gh api ...` komutları yerine GitHub MCP araçları da olur (`actions_run_trigger`, `actions_list`, `get_job_logs`).
- Çeviri ve kod değişiklikleri doğrudan `main`'e push ediliyor (İsmail'in tercihi). `claude/cool-albattani-s83dbr` dalında `main`'de olmayan bir şey yok, silinebilir.
