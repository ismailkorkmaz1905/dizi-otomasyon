# Yeraltı - Endonezce çeviri talimatı (Claude için)

Bu dosya Claude'un her bölümde çeviri adımını nasıl yapacağını anlatır. İzleyen: İsmail ve Endonezyalı kız arkadaşı. Amaç: TV'de Infuse ile izlenen, doğal, sokak ağzıyla konuşan Endonezce altyazı. Son güncelleme: 13 Ekim 2026 (şarkı sözü kuralı).

## Klasörler (Google Drive, "Yeraltı" klasörü)

- `Sezon N/Yeralti.SxxEyy.mp4` : video (Colab indirir)
- `Sezon N/Yeralti.SxxEyy.ind.srt` : SONUÇ, Claude yazar. Infuse bunu otomatik yükler.
- `_iş/SxxEyy/ceviri_girdi.txt` : çevrilecek satırlar
- `_iş/SxxEyy/tr_cues.json` : zamanlar (build için)
- `_iş/SxxEyy/HAZIR.txt` : Colab bitti işareti
- `_iş/SxxEyy/words.json`, `scribe_raw.json`, `whisper_words.json`, `log.txt` : ses tanıma ara dosyaları (çeviride gerekmez)
- `Yakılı/` : altyazısı videoya yakılmış kopyalar (2. defter)
- `sistem/pipeline.py` : kod (iki dizide aynı dosya). Parça kontrolü `check.py` Muhtemel Aşk/sistem klasöründe.
- `sistem/1 - Bölümü Hazırla.ipynb`, `sistem/2 - Yak ve Gönder.ipynb` : Colab defterleri

## Adımlar

1. Drive'da `_iş/SxxEyy/HAZIR.txt` var mı bak. Yoksa Colab henüz bitmemiş, dur ve söyle.
2. İsmail'e sor: "Çeviri ajanları Sonnet mi Opus mu?" Cevap gelmeden ajan başlatma.
3. `ceviri_girdi.txt`, `tr_cues.json` ve `sistem/pipeline.py` dosyalarını indir. Projede bir önceki bölümün özeti (`claude/OZET_SxxEyy.md`) varsa oku.
4. Satırları ~8 eşit parçaya böl. Her parçayı ayrı ajan çevirir: bu talimat, önceki bölüm özeti, parçanın 40 satır öncesi ve 20 satır sonrası bağlam olarak verilir. Her ajan parçasını `check.py` ile denetler.
5. Parçaları birleştir. build'den ÖNCE tek bir kontrol geçişi yap: bütün bölümü kaynakla yan yana oku; hitap tutarlılığı (gue/lo ve aku/kamu), isimler, parça sınırları, `(?)` / `[kelime?]` / `{W: ...}` işaretli satırlar, aşağıdaki "yalancı eşdeğer" tablosu.
6. build'i Claude çalıştırır (kullanıcıya hücre verme):
   `python pipeline.py build tr_cues.json ceviri_tum.txt Yeralti.SxxEyy.ind.srt`
   Eksik/fazla/tekrarlanan satır numarası varsa hata verir, düzelt. `too_fast` / `too_long` listesindeki satırları kısalt, tekrar build et.
7. SRT'yi kontrol et: üst üste binen altyazı ve 0,7 saniyeden kısa süre olmamalı.
8. `.ind.srt` dosyasını `Sezon N` klasörüne ana oturumdan tek çağrıyla yükle (text/plain, dönüştürme kapalı). Geri indirip yerel dosyayla bayt bayt karşılaştır. Aynı isimde eski dosya varsa ancak yenisi doğrulandıktan SONRA eskisini çöpe at.
9. Bu bölümün özetini (Olaylar / Bölüm sonunda durum / İlişkiler ve hitap / Emin olunamayanlar) yazıp projeye `claude/OZET_SxxEyy.md` olarak kaydet.
10. Kullanıcıya kısa haber ver. Videoya yakmak/Telegram için `2 - Yak ve Gönder` defterini hatırlat.

## Girdi formatı

```
0012 [1.9s|38] (?) K3 Lan Haydar, [kes?] sesini! {W: Lan Haydar, kes sesini!}
```
- `0012` satır numarası. Çıktıda aynen kullan.
- `[1.9s|38]` ekranda kalma süresi ve Endonezce için en fazla karakter (okuma hızı 20 kar/sn). Bu sınırı aşma, gerekirse anlamı koruyarak kısalt.
- `K3` konuşmacı etiketi (sadece metin Scribe'dan geldiyse). İsim DEĞİL: "aynı numara = aynı ses" demek, otomatik olduğu için yer yer yanılır (aynı kişiye birkaç numara verebilir). Kimin kime konuştuğunu ve hitabı anlamak için kullan, çıktıya YAZMA.
- `K2>K1` aynı satırda önce K2, sonra K1 konuşuyor. Gerçekten iki farklı kişi konuşuyorsa satırı iki parça yap: `- birinci|- ikinci`. Buna etikete körü körüne değil içeriğe bakarak karar ver. Aynı kişi devam ediyorsa tire kullanma. Üç konuşmacı varsa en doğal iki parçaya indir.
- `[kelime?]` kaynak tam o kelimeden emin değil. Önce o kelimenin yerine bağlama uyan benzer sesli Türkçeyi düşün.
- `(?)` kaynak satırın çoğundan emin değil. Bağlama bakıp en makul Türkçeyi tahmin ederek çevir.
- `{W: ...}` ikinci göz: Whisper aynı yeri belirgin farklı duymuş. Asıl metin (Scribe) çoğunlukla doğrudur; ama asıl metin bağlama oturmuyorsa `{W: ...}` içindekine bak, hangisi sahneye uyuyorsa onu çevir. İkisini birden çevirme, `{W: ...}` kısmını çıktıya yazma.
- `--` yarıda kesilen konuşma. Doğal çevir, gerekirse `...` ile bitir.
- Kaynak ses tanıma çıktısıdır, yazım/duyma hataları olabilir. Önceki/sonraki satırlara bakarak düzelt, ama uydurma. Emin değilsen kısa ve nötr çevir.
- Satırlarda hiç `K` etiketi yoksa metin sadece Whisper'dan gelmiştir (Scribe çalışmamış): duyma hatası daha çoktur. O durumda bilinen yanlışlar: Bozu -> Bozo; Cidem -> Çiğdem; "Next Next Star Televizyon yer altını sunar" -> jenerik, "Next Star Televizyon mempersembahkan Yeraltı."

## Çıktı formatı

Her satır: numara, boşluk, Endonezce metin.
```
0012 Heh Haydar, tutup mulut lo!
```
- Satır sayısı ve numaralar girdiyle birebir aynı. Birleştirme, bölme, sıra değiştirme YOK. Zamanlar Python'da, dokunulmaz.
- İki satıra bölmek istersen `|` kullan: `0020 Lo pikir gue takut?|Gue udah bosen masuk bui.` Yoksa kod otomatik böler.
- En fazla 2 ekran satırı; her satır en fazla 42 karakter (kesin üst sınır 46). 42 karakteri geçmeyen tek konuşmacılı metinde `|` koyma.
- `-` (satırı altyazıdan çıkarır: `0031 -`) sadece şunlar için: konuşma olmayan çöp (müzik, "Altyazı M.K."), tek başına anlamsız dolgu sesi ("Ee", "Hı", "Hıh", "Hah", "Hmm"), gülme/ağlama/nefes. Anlamlı ünlemler ve tekrar eden kısa sözler gerçek konuşmadır: çevir, silme.
- Şarkı sözü (arka planda çalan ya da karakterin söylediği): kısa ve doğal çevir, italik ve nota işaretiyle yaz: `0123 <i>♪ Lirik ♪</i>`; iki satır gerekirse `<i>♪ birinci|ikinci ♪</i>`. Etiketler karakter sınırına sayılmaz. Konuşmayla aynı satıra karışırsa konuşmayı öncele.
- Düz tırnak ve düz tire kullan; süslü Unicode yok.

## Üslup: suç / gangster dizisi

Yeraltı bir suç dizisi: mafya, hapishane, intikam, tehdit, çatışma. Diyaloglar sert, argolu, küfürlü. Endonezcede de aynı sertlikte, doğal sokak dilinde çevir. SANSÜRLEME, yumuşatma, "kibarlaştırma" yok. Kitap dili ve çeviri kokan cümle yok; bir Endonezya suç filminin altyazısı gibi okunmalı.

- Kelimeyi değil işlevi çevir: Türkçe kalıp o sahnede ne iş görüyorsa (tehdit, saygı, yemin, sitem) Endonezcede o işi gören sözü yaz.
- **Hitap (aku/kamu mu, gue/lo mu):** İlişkiye göre seç ve aynı ilişki içinde tutarlı kal.
  - Adamlar arası, rakipler, tehdit, kavga, sokak: `gue` / `lo`.
  - Aile, sevgililer, yakınlar arası duygusal konuşma (ör. Haydar Ali ile Halide, anne-oğul): `aku` / `kamu`.
  - Büyüğe/patrona saygılı hitap: `Bos`, `Pak`, `Bang`. Resmi görevliyle (savcı, polis, avukat): `saya` / `Anda`.
- **Hitap sözcükleri:** Abi / Ağabey -> `Bang` / `Abang`; Abla -> `Kak` / `Mbak`; Reis / Patron -> `Bos`; Hanım -> `Bu` / `Nyonya` (bağlama göre); X Bey -> `Pak X` (mafya büyüğüyse `Tuan X` de olur); Kardeşim (sokak ağzı) -> `bro` ya da atla; Oğlum (azarlama/hitap) -> atla ya da `nak` (babadan oğula); Anne / Ana -> `Ma`; Baba -> `Pa` / `Ayah`.
- **Ünlem/argo:** "lan", "ulan", "be" genelde atlanır ya da `woi`, `heh`, `anjir` ile karşılanır; her satıra koyma.
- **Küfür ve hakaret (aynı sertlikte):**

| Türkçe | Endonezce (doğal karşılık) |
|---|---|
| Siktir! / Siktir git! | Anjing! / Bangsat! / Pergi lo, anjing! |
| Orospu çocuğu | Bajingan / Anak haram / Bangsat |
| Şerefsiz / Namussuz | Bajingan / Brengsek / Keparat |
| Pezevenk | Germo / Bangsat |
| Köpek / It | Anjing |
| Salak / Gerizekalı / Aptal | Goblok / Tolol / Bego |
| Hassiktir | Anjir / Sialan |
| Kes sesini! / Kapa çeneni! | Diem lo! / Tutup mulut lo! |
| Seni gebertirim / Öldürürüm | Gue bunuh lo / Mati lo di tangan gue |
| Ananı ... (anaya küfür) | Bangsat / Anjing (Endonezcede anaya küfür doğal değil; en sert eşdeğeri kullan) |

- **Mafya / sokak jargonu:**

| Türkçe | Endonezce |
|---|---|
| iş, mesele (suç işi) | urusan / kerjaan / bisnis |
| mal (uyuşturucu, kaçak mal) | barang |
| haraç | setoran / uang keamanan |
| tetikçi | pembunuh bayaran |
| ispiyoncu, muhbir, gammaz | cepu |
| içeri girmek, yatmak | masuk bui / dipenjara |
| hapis, cezaevi, kodes | penjara / bui |
| aynasız, polis | polisi / aparat |
| adam (birinin adamı) | anak buah / orang (X) |
| rakip aile | keluarga saingan / musuh |
| kan davası | dendam darah |
| silah, tabanca, demir | pistol / senjata |
| hesap sormak | bikin perhitungan / balas |
| namus, şeref | kehormatan / harga diri |
| racon | aturan main |

- Tehdit ve kavga repliklerini KISA ve vurucu tut. Uzun açıklayıcı cümle kurma.
- İsimleri çevirme. Sayı, tarih, para değerlerini değiştirme.
- Kısa ve net: altyazı okunacak, ekran süresi kısa.

## İsimler (doğru yazım)

İsmail'in doğruladıkları (24 Eylül 2026, S01E16 testi):
- **Bozo**: lakap (Bozkurt). Diyalogda hep "Bozo" geçer, aynen yaz.
- **Ceylan**: Bozo'nun karısı.
- **Kartal**: Bozo'nun düşmanı.

S01E16 testinde geçen diğer isimler: Haydar Ali, Sezai, Emre, Hasan, Melek, Çiğdem, Volkan, Hande, Can, Cengiz, Ferhat, Aslı Hanım, Azize (kadın; "Aziz" yazma).

NOW oyuncular sayfası (karakter tam adları): Haydar Ali (Aslan), Halide (Ceylan), Bozkurt (Hanoğlu), Sultan (Hanoğlu), Yılmaz (Doğan), Merdan (Hanoğlu), Melek (Aslan), Ferhat (Hanoğlu), Ümmü Gülsüm (Mert), Efraim (Güney), Paşa (Hanoğlu), Yavuz (Mert), Aslı (Kartal), Adnan (Yolcu), Pınar (Esen)

- Aile adları: Aslan, Hanoğlu, Mert, Ceylan. "Hanoğulları" gibi aile hitapları aynen kalır.

## Yalancı eşdeğerler ve kalıp sözler

Türkçe kalıbın Endonezcede aynı kelimeyle karşılığı çoğu zaman BAŞKA anlama gelir (Muhtemel Aşk E16'da bu yüzden hatalar çıktı). İşleve göre seç; tablo aku/kamu ile yazıldı, sokak sahnesinde gue/lo'ya uyarla:

| Türkçe (işlev) | Endonezce | Yapma |
|---|---|---|
| Estağfurullah (nezaket: "ne demek, olur mu öyle şey") | Ah, nggak kok / Nggak apa-apa, Bang | "Astagfirullah" yazma: o dehşet ünlemidir |
| Tövbe tövbe / Tövbe estağfurullah (kınama) | Astagfirullah / Amit-amit | "Tobat" yazma: "tövbe et" emri gibi okunur |
| Allah korusun / Allah göstermesin | Amit-amit / Jangan sampai / Naudzubillah | |
| Allah aşkına (yakarma, bıkkınlık) | Ya ampun / Tolonglah / Astaga | "Demi Allah" yazma: o yemindir |
| Vallahi / Yemin ederim / Kitap çarpsın (yemin) | Sumpah / Demi Allah | Her "vallahi"ye koyma |
| Allah Allah (şaşkınlık, sitem) | Ya ampun / Astaga / Lho | |
| Allah'ım / Ya Rabbim (korku, yakarış) | Ya Allah / Ya Rabb | |
| İnşallah / Maşallah | Insyaallah / Masyaallah | |
| Çok şükür | Alhamdulillah / Syukurlah | |
| Eyvallah (tamam, sağ ol, hoşça kal) | Siap / Makasih, Bang / Oke | Tek karşılık yok, sahneye bak |
| Helal olsun (takdir) | Mantap / Salut | |
| Hakkını helal et (veda, ölüm öncesi) | Maafin semua salahku | |
| Allah razı olsun | Makasih banyak / Semoga Allah membalas kebaikanmu | |
| Allah belanı versin (beddua) | Terkutuk lo / Semoga Allah melaknat lo | |
| Allah rahmet eylesin | Semoga Allah merahmatinya | |
| Başın sağ olsun | Turut berduka cita | |
| Geçmiş olsun | Semoga cepat sembuh (hastalık, yara) / Syukurlah udah lewat | |
| Hayırlı olsun | Selamat, ya / Semoga berkah | |
| Kolay gelsin | Semangat, ya | |
| Hayırdır? (tehditkâr ya da meraklı) | Ada apa, nih? / Mau apa lo? | |
| Alo | Halo | |

Genel ilke: Insyaallah, Masyaallah, Alhamdulillah, Astagfirullah, Ya Allah Endonezce gündelik konuşmada doğaldır; gerçek dua ve bedduada "Allah"ı koru ("Semoga Allah ..."). Ama Türkçedeki her "Allah"lı ünlemi Arapça kalıba çevirme; sıradan şaşkınlık ve sitemde "Ya ampun", "Astaga", "Lho" daha doğal.
