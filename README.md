# dizi-otomasyon

Deneysel, Colab'ın yerine çalışıyor. Asıl sistem Google Drive'da duruyor: Colab dosyalarına ve `sistem/` klasörüne dokunulmaz. Bölüm çıktıları (video, `_iş/SxxEyy`, SRT, `Yakılı/`) Colab'daki gibi Drive'a yazılır. Drive'da zaten olan dosyanın üstüne yazılmaz. Bölüm Telegram'a ve Drive'a gidince geçici her şey silinir: Drive'da sadece yakılı video ve `_iş/SxxEyy/scribe_raw.json` kalır, repoda sadece son bölümün `ozet.md`'si, GitHub cache'leri ve 7 günden eski işler de silinir. Eski bölümler için elle: "1 - Bölüm hazırla", iş = temizlik.

## Akış

1. **Bölümü hazırla** (`bolum.yml`): Geçmiş bölümlerin YouTube'a yüklendiği saatlerde 5 dakikada bir, sonra seyrekleşerek YouTube'a bakar (saatler `bolum.yml`'in başında). Yeni bölüm varsa videoyu indirir, Scribe ile Türkçe metni çıkarır, çeviri girdisini `bolumler/<dizi>/SxxEyy/` altına koyar.
2. **Çeviri:** Claude rutini (Perşembe-Cumartesi, Singapur saatiyle 2 saatte bir) bekleyen bölüm var mı bakar. Varsa `ceviri/YONTEM.md`'ye göre 8 Opus ajanla çevirir ve aynı klasöre `ceviri.txt` ile `ozet.md` koyar. Çeviri kuralları her bölümde Drive'daki "Çeviri Talimatı.md"den (`talimat.md`) gelir.
3. **Yak ve gönder** (`yak.yml`): Çeviri gelince kendiliğinden başlar, SRT'yi Türkçe zamanlarla kurar. Video 12 parçaya bölünür ve 12 makinede aynı anda yakılır. Parçalar birleştirilip Telegram'a gönderilir.

İşin kendisini Drive'daki `sistem/pipeline.py` yapar: Colab'daki kod, kalite ve yazı stili aynıdır. Drive'da kod değişirse burası da otomatik olarak yenisini kullanır.

Elle çalıştırmak için **Actions** sekmesine gir, işi seç ve **Run workflow**'a bas. "Bölümü hazırla"da **kontrol** seçilirse kurulum denenir: hiçbir şey gönderilmez, kredi harcanmaz.

## Bakım: neler bozulabilir

| Ne | Belirti | Ne yapılır |
|---|---|---|
| YouTube çerezi eskir | Hazırla işi "bot engeli" hatası verir | Colab'da yaptığın gibi `sistem/youtube_cookies.txt` dosyasını yenile |
| Scribe kalan kredi "okunamadi" | Rapor ve kontrol kalan krediyi göstermez | ElevenLabs'ta API anahtarına "User: Read" izni ver |
| ElevenLabs kredisi biter ya da anahtar iptal olur | Hazırla işi "Scribe 401/402" hatası verir | Krediyi yükle ya da `sistem/elevenlabs.json`'daki anahtarı yenile. Burada Whisper yedeği yok |
| Telegram oturumu düşer (Telegram'da "Aktif oturumlar"dan kapatılırsa) | Yak işi Telegram adımında hata verir | Colab'da "2 - Yak ve Gönder" ile bir kez giriş yap |
| Drive paylaşımı kalkar | Her iş "klasör paylaşılmamış" hatası verir | Dizi klasörünü servis hesabıyla (`GDRIVE_SA` içindeki `client_email`) Görüntüleyen olarak paylaş |
| GitHub dakikası biter (gizli repoda ayda 2.000 dk) | İşler başlamaz | Bölüm başına yaklaşık 250 dk gider. Settings > Billing'den bak, gerekirse repoyu açık yap (açık repoda dakika sınırsız) |
| Drive yazma izni (`GDRIVE_OAUTH`) | İş "invalid_grant" verir, Drive'a dosya gelmez (Telegram yine gider) | 6 ay hiç kullanılmazsa ya da myaccount.google.com/permissions'tan kaldırılırsa ölür. OAuth Playground'dan yeni refresh token alıp secret'ı güncelle |
| Servis hesabı anahtarı | Süresi dolmaz | Sadece silinirse ya da sızarsa yenisini `GDRIVE_SA` secret'ına koy |
| Claude rutini | Çeviri gelmez | Claude planının 5 saatlik limitinden harcar. Limit dolarsa rutin, pencere sıfırlanana kadar çalışmaz |

Her bölüm bitince yakma işinin özet sayfasında ve logunda bir rapor çıkar (yakalanma saati, süreler, commitler); Claude bunu thread'e taşır. Hata olunca GitHub e-posta atar. İşin logu Actions sekmesinde durur.
