# Çeviri rutini: Türkçe -> Endonezce altyazı

Bu dosyayı Claude rutini okur ve uygular. GitHub hazırlık işi her yeni bölüm için `bolumler/<dizi>/SxxEyy/` altına şunları koyar:
- `ceviri_girdi.txt`: numaralı Türkçe satırlar
- `tr_cues.json`: zamanlar
- `kaynak.json`: YouTube kaynağı
- `talimat.md`: dizinin Drive'daki "Çeviri Talimatı.md" dosyasının kopyası

Rutinin işi o bölümü çevirip aynı klasöre `ceviri.txt` koymak. Push yakmayı ve Telegram'ı kendiliğinden başlatır, SRT GitHub'da kurulur.

## 0. Hazırlık
- Repoyu `ismailkorkmaz1905/dizi-otomasyon` klonla (`main`). Erişim yoksa önce `add_repo` ile ekle.
- Bekleyen bölüm: `ceviri_girdi.txt` dosyası olan ama içinde `ceviri.txt` ya da `*.ind.srt` olmayan `bolumler/*/*/` klasörleri.
- Önce son 2 saatte kırmızı biten iş var mı bak: `gh api 'repos/ismailkorkmaz1905/dizi-otomasyon/actions/runs?status=failure&per_page=5'`. Varsa ve daha önce haber verilmediyse thread'e kısa yaz: hangi iş, hangi dizi, logdaki hata satırı, ne yapılacağı. Scribe'a tekrar para gidebilecek bir işi kendiliğinden yeniden çalıştırma.
  - **Hiç yoksa:** "Bekleyen bölüm yok" de ve hemen bitir. Başka hiçbir şey yapma.
  - **Birden fazlaysa:** sırayla hepsini yap, eskisinden başla.
- Bölüm başına bir çalışma klasörü aç: `/tmp/ceviri/<dizi>_<SxxEyy>/`. İçine şunları kopyala: `ceviri_girdi.txt`, `talimat.md`, `ceviri/check.py`. Varsa aynı dizinin bir önceki bölümünün `ozet.md` dosyasını da `onceki_ozet.md` adıyla kopyala.

## 1. Sekiz parçaya böl
- Satır sayısı N: girdideki son satır numarası.
- 1..N aralığını 8 eşit parçaya böl; parça sınırlarını not et.

## 2. Sekiz Opus ajan (paralel, tek mesajda)
Her ajana Agent aracıyla `model: opus` ver ve aşağıdaki metni `<...>` yerlerini doldurarak gönder:

> Klasör: <çalışma klasörü>. Türkçe dizi altyazısını Endonezceye çeviriyorsun.
> 1. Önce şunları baştan sona oku:
>    - `talimat.md`: HER kuralına uy (girdi/çıktı formatı, hitap tablosu, "Yalancı eşdeğerler" tablosu, `-` satırları, `|` kullanımı, karakter sınırı).
>    - Varsa `onceki_ozet.md`: önceki bölümün olayları, ilişkileri ve hitapları.
> 2. `ceviri_girdi.txt`'den <BAS>..<SON> aralığını çevir. Bağlam için aralığın 40 satır öncesini ve 20 satır sonrasını da oku ama ÇEVİRME.
> 3. Çıktıyı `parca_<k>.txt` dosyasına yaz:
>    - Her satır `NNNN metin` biçiminde olsun.
>    - Aralıktaki her numara tam bir kez geçsin, başka numara olmasın.
>    - Boş satır olmasın.
> 4. Doğrula: `python3 check.py ceviri_girdi.txt parca_<k>.txt <BAS> <SON>`. Sonuç `OK` olana ve hiç `LONG` kalmayana kadar düzelt.
>
> Kurallar:
> - Doğal, günlük konuşma Endonezcesi kullan (aku/kamu, nggak, udah, aja, banget, sih, kok, dong). Kitap dili kullanma.
> - `K3` ve `K2>K1` gibi etiketler sadece konuşmacı ipucu, çıktıya YAZMA. Satırda iki ayrı kişi konuşuyorsa `- birinci|- ikinci` yaz.
> - `{W: ...}` ikinci duyuşu gösterir. Ana metin anlamsızsa ona bak, çıktıya YAZMA.
> - `[kelime?]` ve `(?)` şüpheli yerler. Bağlama en uygun tahmini yap.
> - Bir ekran satırı en fazla 42 karakter (kesin sınır 46), bir altyazı en fazla 2 satır. `[Xs|N]` içindeki N, `|` hariç toplam karakter sınırıdır.
> - Başka dosyaya dokunma, git'e dokunma, mesaj gönderme.
>
> Bitince kısa döndür:
> - check sonucu
> - emin olmadığın satırlar: en fazla 10, her biri bir cümle
> - bu aralıktaki önemli olaylar: 3-6 madde, Türkçe

Ajanların raporlarını `raporlar.md`'ye yaz. Her parçayı kendin de `check.py` ile doğrula. Hata varsa aynı ajana düzelttir.

## 3. Tek geçişli kontrol (1 Opus ajan)
`parca_1..8.txt` dosyalarını sırayla birleştirip `ceviri_v1.txt` yap. Sonra bir Opus ajana şunu gönder:

> Klasör: <çalışma klasörü>.
> - Önce `talimat.md`, `onceki_ozet.md` (varsa) ve `raporlar.md`'yi oku.
> - Sonra `ceviri_v1.txt`'yi `ceviri_girdi.txt` ile yan yana baştan sona oku ve düzelt:
>   1. Hitap tutarlılığı: aynı iki kişi her yerde aynı hitabı kullanmalı.
>   2. İsim yazımları ve talimattaki karıştırılan isimler.
>   3. Parça sınırları (<sınırlar>): her sınırın 15 satır öncesi ve sonrası. Kopukluk, tekrar ya da yarım cümle olmasın.
>   4. Şüpheli işaretli satırlar ve raporlarda şüpheli denen satırlar.
>   5. Talimattaki "Yalancı eşdeğerler" tablosu.
>   6. Kitap dili.
> - Satır numaraları ve satır sayısı aynen kalır. Karakter sınırları aynı.
> - Sonucu TEK SEFERDE `ceviri_tum.txt` olarak yaz ve doğrula: `python3 check.py ceviri_girdi.txt ceviri_tum.txt 1 <N>`, sonuç OK olmalı, LONG kalmamalı.
> - Doğrulayınca HEMEN bitir. İkinci tur okuma yapma.
> - Döndür: değiştirdiğin satır sayısı ve en önemli 10 değişiklik.

Kontrol ajanı 30 dakika içinde dönmezse ve `ceviri_tum.txt` check'ten geçiyorsa ajanı durdur ve o dosyayı kullan. Dosya yoksa `ceviri_v1.txt`'yi kullan.

## 4. Teslim
- Son dosyayı `check.py` ile doğrula; sonuç OK olmalı.
- Dosyayı repoda `bolumler/<dizi>/<SxxEyy>/ceviri.txt` olarak koy.
- Aynı klasöre `ozet.md` yaz: Türkçe, 8-15 madde. Bölümün olayları, kim kime ne hitap etti, yeni isimler. Kaynak: ajan raporları. Sonraki bölümün çevirmenleri bunu okuyacak.
- İkisini tek commit'te push et, mesaj tek satır: `<Dizi adı> <SxxEyy> - çeviri (<N> satır)`, örnek `Yeraltı S02E01 - çeviri (2324 satır)`.
  - Önce `git pull --rebase`, push reddedilirse tekrar dene.
- Push yakmayı başlatır. Drive'a yazma, workflow tetikleme.
- Thread'e kısa not: hangi bölüm, kaç satır, kaç satır düzeltildi.

## 5. Rapor (her bölümün sonunda)
- Push'un başlattığı "Yak ve gonder" işini bul: `gh api 'repos/ismailkorkmaz1905/dizi-otomasyon/actions/runs?head_sha=<push sha>' --jq '.workflow_runs[0].id'` (birkaç saniye sonra çıkar).
- Bitmesini arka planda bekle (Bash, `run_in_background`, timeout 3 saat): `while [ "$(gh api repos/ismailkorkmaz1905/dizi-otomasyon/actions/runs/<id> --jq .status)" != completed ]; do sleep 60; done`. Beklerken başka bir şey yapma, turu bitir; iş bitince uyandırılırsın.
- Yeşil bittiyse `birlestir` işinin logundan `===== RAPOR =====` ile `===== RAPOR SONU =====` arasını al (`mcp__github__get_job_logs`, `tail_lines` 60). Thread'e tek mesaj at: raporu Türkçe harflerle madde madde yaz, çeviri satırına bu oturumdaki süreleri ekle (rutin başladı, 8 ajan bitti, kontrol bitti, push), commitleri `https://github.com/ismailkorkmaz1905/dizi-otomasyon/commit/<sha>` linkiyle ver.
- Kırmızı bittiyse: hangi iş ve adım, logdaki hata, ne yapılacağı. Kendiliğinden yeniden çalıştırma.
  - İstisna: sadece `birlestir` Telegram hatasıyla düştüyse ve logda hiç "gitti" satırı yoksa bir kez `gh api -X POST repos/ismailkorkmaz1905/dizi-otomasyon/actions/runs/<id>/rerun-failed-jobs` çalıştır ve onu da bekle. Yakılmış 12 parça saklı, yeniden yakmaz, para tutmaz.
