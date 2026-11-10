# Çeviri rutini: Türkçe -> Endonezce altyazı

GitHub hazırlık işi her yeni bölüm için `bolumler/<dizi>/SxxEyy/` altına `ceviri_girdi.txt` (numaralı Türkçe satırlar), `tr_cues.json` (zamanlar), `kaynak.json` ve `talimat.md` (Drive'daki "Çeviri Talimatı.md" kopyası) koyar. Rutinin işi aynı klasöre `ceviri.txt` ve `ozet.md` koymak. Push yakmayı ve Telegram'ı kendiliğinden başlatır.

## Token kuralları (10 Kasım 2026)

Bölüm başına harcamanın çoğu çeviri metninden değil, tekrar okunan bağlamdan ve gereksiz yazılan çıktıdan geliyor. Bu yüzden:

- Her bölüm yeni bir thread'de çevrilir. Teslim ve rapordan sonra o thread'de başka iş yapılmaz.
- Ana oturum Sonnet'te çalışır ve büyük dosyaları (`ceviri_girdi.txt`, `parca_*.txt`, `ceviri_*.txt`, `yan_yana.txt`, `tr_cues.json`) ASLA Read ile açmaz, `cat`/`head` ile de basmaz. Bölme, birleştirme, doğrulama `ceviri/arac.py` ile yapılır; ana oturum sadece komutun kısa çıktısını görür.
- Her ajan sadece kendi dosyasını okur (`girdi_<k>.txt` ya da `yan_yana.txt`), bütün girdiyi değil.
- Kontrol ajanı bütün çeviriyi yeniden yazmaz, sadece değişen satırları yazar.
- Alt ajan sayısı: parça başına ~450 satır (Başkalarının Hayatı 4, Muhtemel Aşk 5 parça). Daha fazla ajan aynı talimatı daha çok kez okutur, kaliteye katkısı yok, parça sınırı sayısını artırır.
- Thread'e kısa notlar: başladı, çeviri bitti, push, rapor. Ajan çıktısını thread'e yapıştırma.

## 0. Hazırlık

- `DURUM.md`'yi oku. Repo `ismailkorkmaz1905/dizi-otomasyon`, dal `main`.
- Bekleyen bölüm: `ceviri_girdi.txt` olan ama `ceviri.txt` ya da `*.ind.srt` olmayan `bolumler/*/*/` klasörü. Yoksa "Bekleyen bölüm yok" de ve bitir. Birden fazlaysa eskisinden başla.
- Son 2 saatte kırmızı biten iş varsa (`actions_list` ya da `gh api 'repos/ismailkorkmaz1905/dizi-otomasyon/actions/runs?status=failure&per_page=5'`) thread'e kısa yaz. Scribe'a tekrar para gidebilecek bir işi kendiliğinden yeniden çalıştırma.
- Böl: `python3 ceviri/arac.py bol bolumler/<dizi>/<SxxEyy> /tmp/ceviri/<dizi>_<SxxEyy>`. Çalışma klasörüne `talimat.md`, `onceki_ozet.md` (varsa), `check.py`, `arac.py`, `girdi_<k>.txt` dosyalarını koyar, parça sınırlarını sahne arası sessizliklere denk getirir ve yazdırır.
- Aynı mesajda İsmail'e tek satır sor: kontrol ajanının effort'u `medium` mı `high` mı? Cevabı BEKLEME, çeviri ajanlarını hemen başlat. Çeviri bittiğinde cevap yoksa `medium` kullan ve thread'e not düş.

## 1. Çeviri ajanları (paralel, tek mesajda)

Model: İsmail başlatırken başka bir şey demediyse `opus`. Effort verme. Her parça için Agent aracıyla şunu gönder:

> Klasör: <çalışma klasörü>. Türkçe dizi altyazısını Endonezceye çeviriyorsun.
> 1. Sırayla ve birer kez oku: `talimat.md` (her kuralına uy), varsa `onceki_ozet.md`, sonra `girdi_<k>.txt`. Başka dosya okuma.
> 2. `girdi_<k>.txt`'de sadece `=== CEVIR: <BAS>-<SON> ===` başlığının altındaki satırları çevir. `=== BAGLAM ===` altındakiler sadece bağlam.
> 3. Çıktıyı tek seferde `parca_<k>.txt`'ye yaz: her satır `NNNN metin`, aralıktaki her numara tam bir kez, boş satır yok.
> 4. Doğrula: `python3 check.py ceviri_girdi.txt parca_<k>.txt <BAS> <SON>`. `OK` çıkana ve `LONG` kalmayana kadar sadece hatalı satırları Edit ile düzelt, dosyayı baştan yazma.
>
> Başka dosyaya ve git'e dokunma. Bitince kısa döndür: check sonucu; emin olmadığın en fazla 10 satır (birer cümle); bu aralıktaki önemli olaylar ve yeni hitaplar (3-6 madde, Türkçe).

Dönen raporları `raporlar.md`'ye yaz. Sonra `python3 arac.py birlestir <çalışma klasörü>`: parçaları `ceviri_v1.txt` ve `ceviri_tum.txt` yapar, doğrular, `yan_yana.txt`'yi üretir. Hata verirse ilgili ajana düzelttir.

## 2. İki turlu kontrol (1 Opus ajan, effort İsmail'in cevabı)

> Klasör: <çalışma klasörü>. Türkçeden Endonezceye çevrilmiş dizi altyazısını kontrol ediyorsun.
> - Oku: `talimat.md`, varsa `onceki_ozet.md`, `raporlar.md`, sonra `yan_yana.txt` (her satır: `NNNN [süre|sınır] Türkçe => Endonezce`). Başka dosya okuma.
> - Baştan sona oku ve şunlara bak: anlam hataları; hitap tutarlılığı (aynı iki kişi her yerde aynı hitap); isim yazımları ve talimattaki karıştırılan isimler; parça sınırları (<sınırlar>) çevresinde kopukluk ya da tekrar; `(?)` ve `[kelime?]` işaretli ve raporlarda şüpheli denen satırlar; "Yalancı eşdeğerler" tablosu; kitap dili.
> - Bütün çeviriyi yeniden YAZMA. Sadece değiştirdiğin satırları `duzeltme_1.txt`'ye yaz (`NNNN yeni metin`, satırın tamamı). Sonra `python3 arac.py uygula . duzeltme_1.txt`. Hata verirse düzeltme dosyasını onar ve tekrar çalıştır. `DEGISEN n satir` çıkınca `ceviri_tum.txt` ve `yan_yana.txt` güncellenmiştir.
> - İkinci tur: güncel `yan_yana.txt`'yi baştan sona bir kez daha oku; kaçan anlam hatalarını, hitap/isim tutarsızlıklarını ve doğal olmayan satırları `duzeltme_2.txt`'ye yaz ve aynı şekilde uygula. Üçüncü tur yok.
> - Döndür: iki turun `DEGISEN` sayıları ve en önemli 10 değişiklik.

45 dakika içinde dönmezse ajanı durdur; `ceviri_tum.txt` her zaman doğrulanmış son hâldir, onu kullan.

## 3. Teslim

- `ceviri_tum.txt`'yi repoda `bolumler/<dizi>/<SxxEyy>/ceviri.txt` olarak kopyala (`cp`).
- Aynı klasöre `ozet.md` yaz: Türkçe, 8-15 madde. Olaylar, kim kime ne hitap etti, yeni isimler. Kaynak: `raporlar.md`. Sonraki bölümün çevirmenleri okuyacak.
- İkisini tek commit'te `main`'e push et, mesaj tek satır: `<Dizi adı> <SxxEyy> - çeviri (<N> satır)`. Önce `git pull --rebase`.
- Drive'a yazma, workflow tetikleme. Thread'e kısa not: bölüm, satır sayısı, iki turda düzeltilen satır sayıları.

## 4. Rapor

- Push'un başlattığı "Yak ve gonder" işini bul (`head_sha=<push sha>`), bitmesini arka planda bekle (Bash `run_in_background`, 60 sn'de bir durum, timeout 3 saat) ve turu bitir.
- Yeşil bittiyse `birlestir` işinin logundan `===== RAPOR =====` bloğunu al (`get_job_logs`, `tail_lines` 60) ve thread'e tek mesajla Türkçe harflerle yaz; bu oturumun sürelerini (başladı, çeviri bitti, kontrol bitti, push) ve commit linklerini ekle.
- Kırmızı bittiyse: hangi iş ve adım, logdaki hata, ne yapılacağı. Kendiliğinden yeniden çalıştırma. İstisna: sadece `birlestir` Telegram hatasıyla düştüyse ve logda hiç "gitti" satırı yoksa bir kez `rerun-failed-jobs` çalıştır ve onu da bekle (yakılmış parçalar saklı, para tutmaz).
