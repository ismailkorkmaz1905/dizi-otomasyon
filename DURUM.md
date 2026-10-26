# Son durum ve notlar (26 Ekim 2026)

Yeni bir Claude oturumu buradan devam edecekse önce bunu, sonra `ceviri/YONTEM.md`'yi okusun. Akışın kendisi `README.md`'de.

## Diziler

| Dizi | `dizi` değeri | Son teslim | Yayın | YouTube'a düşme | Otomatik arama |
|---|---|---|---|---|---|
| Muhtemel Aşk | `muhtemel_ask` | S01E19 (23 Ekim) | perşembe gecesi | cuma 01:00-01:04 TR | var (`bolum.yml` cron), ama güvenilmez |
| Başkalarının Hayatı | `baskalarinin_hayati` | S01E05 (25 Ekim) | cumartesi 20:00 Star TV | gece 23:30-00:30 TR (E3: 00:16, E4: 23:39, E5: 04:34 SGT = 23:34 TR) | **yok**, elle başlat |
| Yeraltı | `yeralti` | - | - | - | 16 Ekim'de takipten çıktı |

## Bölüm nasıl başlatılır

1. Actions > "1 - Bölüm hazırla" > Run workflow: `is = hazirla`, `dizi = ...`, `bolum` = numara (ör. `6`) ya da boş (sıradaki).
   - Bölüm YouTube'da yoksa iş "Yeni bolum yok" deyip biter, kredi harcamaz.
   - `bolum = bekle`: ~100 dk boyunca 5 dk'da bir bakar.
   - "kontrol" işi bölümün çıkıp çıkmadığını **söylemez** ("YouTube son bolum" satırı hep 1. bölümü gösteriyor).
2. Hazırlık `bolumler/<dizi>/SxxEyy/ceviri_girdi.txt`'yi `main`'e koyar. Çeviri `ceviri/YONTEM.md`'ye göre yapılır.
3. `ceviri.txt` `main`'e push edilince "2 - Yak ve gönder" kendiliğinden başlar, Telegram'a gönderir, Drive'a yazar, temizlik yapar.

## Krediler ve kotalar

- **Scribe (ElevenLabs):** kalan 5.345 / 31.729 kredi, yenilenme 13.11.2026. Bölüm başına 2.900-3.700 kredi (E3 3.721, E4 3.222, MA E19 3.336, E5 2.858). Kalanla ~1-2 bölüm.
- **Google Drive:** 25 Ekim'de dolmuştu (yükleme `403 Forbidden`), İsmail depolamayı yükseltti, sonra sorunsuz.
- **Claude:** bulut oturumu için verilen hediye kredi 26 Ekim'de bitti. Rutinin hâlâ çalışıp çalışmadığı kontrol edilmeli.

## Bu hafta yapılan değişiklikler

- **ffmpeg önbelleği** (`.github/actions/ffmpeg/`): runner'ın Azure Ubuntu mirror'ı aralıklı ~60 KB/sn'ye düşüyor, 94 MB'lık ffmpeg 16-33 dk sürüyordu (S01E19 yakması ~1 saat gecikti). Artık `.deb`'ler GitHub cache'inde (anahtar runner image sürümüne bağlı), kurulum 8-18 sn. Cache yoksa apt: 3 dk varsayılan mirror, olmazsa Azure çıkarılıp ana Ubuntu sunucusundan 10 dk. Yedek yol gerçek bir yavaşlıkta henüz denenmedi.
- **YONTEM.md:** kontrol ajanının effort'u (`medium`/`high`) başlamadan İsmail'e sorulur; 30 dk cevap yoksa `medium`. Çeviri ajanları her zaman `medium`. İsmail bir sonraki bölümde `high` denemek istedi (kıyas için: E3 95+30, E4 83+62, MA E19 135+22, E5 83+19 satır düzeltme, hepsi `medium`).

## Bilinen tuhaflıklar

- **Cron:** `bolum.yml` cron'u bazen hiç tetiklenmiyor (22 Ekim akşamı çalışmadı, elle başlatıldı). Dosyanın başındaki nota bak.
- **Hazırlık işi kırmızı ama girdi gelmiş:** commit, Drive yüklemesinden önce yapılıyor. Drive hatası işi kırmızı yapar ama çeviri ve yakma etkilenmez.
- **YouTube Premium akışı:** S01E19 ve S01E05'te "Premium 1080p akışını sunmadı, standart akış iniyor" uyarısı çıktı (h264 ~1,55 Mbps; E3/E4 Premium vp9 ~1,7-1,8 Mbps). Nedeni araştırılmadı.
- **Ses tanıma hataları:** Muhtemel Aşk'ta "Kader" (Ali'nin annesi) ile "Kadir" (dayı) karışıyor. Başkalarının Hayatı'nda "Betiş" diye biri yok, "Mediş" (Mediha). Salih'in Hülya lakabı "kecoak hitam".
- **Başkalarının Hayatı'nda satır az:** dakikada ~60 kelime (Muhtemel Aşk ~86), bölümler daha kısa. E5: 1584 satır, 127 dk. Normal.
- **E5 satır 571** (flashback, "Anne... sen, ben, ablam"): kontrol ajanı kaynağa döndü, ilk çeviri "Kak... kamu, aku, Mama" idi. Sahne izlenerek doğrulanmadı.

## GitHub erişimi

- YONTEM'deki `gh api ...` komutları yerine GitHub MCP araçları da olur (`actions_run_trigger`, `actions_list`, `get_job_logs`).
- Çeviri ve kod değişiklikleri doğrudan `main`'e push ediliyor (İsmail'in tercihi). `claude/cool-albattani-s83dbr` dalında `main`'de olmayan bir şey yok, silinebilir.
