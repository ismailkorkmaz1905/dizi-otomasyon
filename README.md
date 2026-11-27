# dizi-otomasyon

Deneysel, Colab'ın yerine çalışıyor. Asıl sistem Google Drive'da duruyor: Colab dosyalarına ve `sistem/` klasörüne dokunulmaz. Bölüm çıktıları (video, `_iş/SxxEyy`, SRT, `Yakılı/`) Colab'daki gibi Drive'a yazılır. Drive'da zaten olan dosyanın üstüne yazılmaz. Bölüm Telegram'a ve Drive'a gidince geçici her şey silinir: Drive'da sadece yakılı video ve `_iş/SxxEyy/scribe_raw.json` kalır, repoda sadece son bölümün `ozet.md`'si, GitHub cache'leri ve 7 günden eski işler de silinir. Eski bölümler için elle: "1 - Bölüm hazırla", iş = temizlik.

Son durum, krediler ve bilinen sorunlar: `DURUM.md`.

## Akış

1. **Bölümü hazırla** (`bolum.yml`): Geçmiş bölümlerin YouTube'a yüklendiği saatlerde 5 dakikada bir, sonra seyrekleşerek YouTube'a bakar (saatler `bolum.yml`'in başında). Yeni bölüm varsa videoyu indirir, Scribe ile Türkçe metni çıkarır, çeviri girdisini `bolumler/<dizi>/SxxEyy/` altına koyar.
2. **Çeviri:** Proje sohbetine "<dizi> <N>. bölümü çevir" yazılır; yeni bir Claude thread'i `ceviri/YONTEM.md`'ye göre çevirir ve aynı klasöre `ceviri.txt` ile `ozet.md` koyar. Çeviri kuralları her bölümde Drive'daki "Çeviri Talimatı.md"den (`talimat.md`) gelir.
3. **Yak ve gönder** (`yak.yml`): Çeviri gelince kendiliğinden başlar, SRT'yi Türkçe zamanlarla kurar. Video 12 parçaya bölünür ve 12 makinede aynı anda yakılır. Parçalar birleştirilip Telegram'a gönderilir.

Altyazı üretimi, video kalite ayarları ve varsayılan yazı stili Drive'daki `sistem/pipeline.py`'den gelir. Drive'da kod değişirse burası da otomatik olarak yenisini kullanır.

Elle çalıştırmak için **Actions** sekmesine gir, işi seç ve **Run workflow**'a bas. "Bölümü hazırla"da **kontrol** seçilirse kurulum denenir: hiçbir şey gönderilmez, kredi harcanmaz.

## Altyazı stilleri

**Actions > 2 - Yak ve gönder > Run workflow > Altyazı stili** menüsünde **GTA VI** (varsayılan) veya **Mevcut** seçilir. Mevcut, Drive'daki `BURN_STYLE`'dır. Çeviri gönderildiğinde başlayan otomatik işler de GTA VI kullanır; eski stile dönmek için GitHub Actions depo değişkeni `ALTYAZI_PRESET` değerini `Mevcut` yap.

GTA VI stili, oyun içi diyalog görünümüne yakın bir sonuç için 1920 × 1080 ASS koordinatlarında 60 px Figtree Regular (Mevcut stille aynı boyut) (400), beyaz dolgu, 2 px siyah kontur ve 1 px siyah gölge kullanır. Harf aralığına ek boşluk verilmez. Altyazı kutusuz ve yatay ortalıdır. Alt kenar payı 124 px, yan kenar payları 96 px'dir. Ölçüler çözünürlükle ölçeklenir. GTA Art Deco Regular, karşılaştırılan konsol altyazı örneklerine en yakın Rockstar fontuydu. Açık lisanslı alternatifler arasında [Figtree Regular v2.0.3](https://github.com/erikdkennedy/figtree/tree/v2.0.3/fonts/ttf) en yakın sonucu verdi ve `ç, ğ, ı, İ, ö, ş, ü` karakterlerinin tamamını içeriyor. [SIL Open Font License 1.1](fonts/OFL.txt)

Yerel çalıştırmada, kullanım iznin olan bir TTF, OTF veya WOFF dosyası için `GTA_VI_FONT_FILE` değişkenine dosya yolunu, `GTA_VI_FONT_NAME` değişkenine fontun tam adını yaz. Yerelde `ALTYAZI_PRESET='GTA VI'` ile `plan` çalıştırıp font değişkenlerini `parca` komutlarının ortamında ayarla. Rockstar font dosyalarının lisansı kullanımı Rockstar marka materyalleriyle sınırlar.

## Bakım: neler bozulabilir

| Ne | Belirti | Ne yapılır |
|---|---|---|
| YouTube çerezi eskir | "3 - Çerez kontrol" kırmızı olur ve Telegram'a yazar; hazırla işi "bot engeli" verir | Aşağıdaki "Çerez yenileme" |
| Scribe kalan kredi "okunamadi" | Rapor ve kontrol kalan krediyi göstermez | ElevenLabs'ta API anahtarına "User: Read" izni ver |
| ElevenLabs kredisi biter ya da anahtar iptal olur | Hazırla işi "Scribe 401/402" hatası verir | Krediyi yükle ya da `sistem/elevenlabs.json`'daki anahtarı yenile. Burada Whisper yedeği yok |
| Telegram oturumu düşer (Telegram'da "Aktif oturumlar"dan kapatılırsa) | Yak işi Telegram adımında hata verir | Colab'da "2 - Yak ve Gönder" ile bir kez giriş yap |
| Drive paylaşımı kalkar | Her iş "klasör paylaşılmamış" hatası verir | Dizi klasörünü servis hesabıyla (`GDRIVE_SA` içindeki `client_email`) Görüntüleyen olarak paylaş |
| GitHub dakikası biter (gizli repoda ayda 2.000 dk) | İşler başlamaz | Bölüm başına yaklaşık 250 dk gider. Settings > Billing'den bak, gerekirse repoyu açık yap (açık repoda dakika sınırsız) |
| Drive yazma izni (`GDRIVE_OAUTH`) | İş "invalid_grant" verir, Drive'a dosya gelmez (Telegram yine gider) | 6 ay hiç kullanılmazsa ya da myaccount.google.com/permissions'tan kaldırılırsa ölür. OAuth Playground'dan yeni refresh token alıp secret'ı güncelle |
| Servis hesabı anahtarı | Süresi dolmaz | Sadece silinirse ya da sızarsa yenisini `GDRIVE_SA` secret'ına koy |
| Claude rutini | Çeviri gelmez | Claude planının 5 saatlik limitinden harcar. Limit dolarsa rutin, pencere sıfırlanana kadar çalışmaz |

Her bölüm bitince yakma işinin özet sayfasında ve logunda bir rapor çıkar (yakalanma saati, süreler, commitler); Claude bunu thread'e taşır. Hata olunca GitHub e-posta atar. İşin logu Actions sekmesinde durur.

## Çerez yenileme

Kontrol (`cerez.yml`): her gün 02:00 UTC, Muhtemel Aşk için perşembe 10:00 UTC, Başkalarının Hayatı için cumartesi 11:00 UTC. İndirmez, kredi harcamaz. Çerez ölmüşse Telegram'a tarifle birlikte yazar. Cron geciktiği/atladığı olur: bölümden önce **Actions > 3 - Çerez kontrol > Run workflow** ile elle de çalıştırılabilir. "1 - Bölüm hazırla" hata verirse de Telegram'a haber gider.

Tek satır: gizli pencerede YouTube'a gir, aynı sekmede `youtube.com/robots.txt` aç, çerez eklentisiyle Export et, Drive'daki `sistem/youtube_cookies.txt`'in üstüne aynı adla yükle (Yeni dosya değil, "Yeni sürüm yükle"), pencereyi hemen kapat, "3 - Çerez kontrol"ü çalıştır.

Telefondan (iOS): Safari ve iOS Chrome çerez dosyası vermez. Tek yol eklenti destekleyen bir tarayıcı (Orion) ya da bir bilgisayar. Dosya Drive'a Drive uygulaması ya da Dosyalar uygulamasıyla yüklenir.
