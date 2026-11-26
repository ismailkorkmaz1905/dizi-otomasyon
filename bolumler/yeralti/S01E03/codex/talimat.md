# Yeraltı - Endonezce çeviri talimatı

İzleyen: İsmail ve Endonezyalı kız arkadaşı. Amaç: TV'de izlenen, doğal, sokak ağzıyla konuşan Endonezce altyazı; bir Endonezya suç filminin altyazısı gibi okunmalı. Akış `ceviri/YONTEM.md`'de, bu dosya sadece çeviri kurallarıdır. Son güncelleme: 26 Kasım 2026.

Dizi: suç / mafya dramı (NOW). İstanbul'da aileler, hapishane, intikam, kan davası, sadakat. Ton sert, argolu, yer yer küfürlü; aile ve aşk sahnelerinde duygusal.

## Girdi

```
0012 [1.9s|38] (?) K3 Lan Haydar, [kes?] sesini!
```
- `0012` satır numarası, çıktıda aynen kullanılır.
- `[1.9s|38]` ekranda kalma süresi ve Endonezce için en fazla karakter (20 kar/sn). Aşma; gerekirse anlamı koruyarak kısalt.
- `K3` konuşmacı etiketi, isim değil: "aynı numara = aynı ses". Otomatik olduğu için yanılabilir. Kimin kime konuştuğunu anlamak için kullan.
- `K2>K1` aynı satırda önce K2, sonra K1 konuşuyor. İçeriğe bak: gerçekten iki kişi konuşuyorsa (soru-cevap, karşılıklı laf) `- birinci|- ikinci` yaz, aynı kişi devam ediyorsa tire kullanma. Üç konuşmacı varsa en doğal iki parçaya indir.
- `[kelime?]` kaynak o kelimeden, `(?)` satırın çoğundan emin değil. Bağlama uyan benzer sesli Türkçeyi düşün, ona göre çevir.
- `{W: ...}` varsa ikinci bir duyuştur; asıl metin bağlama oturmuyorsa ona bak.
- `--` ya da sonda `-` yarıda kesilen konuşma: doğal çevir, `...` ya da `--` ile bitir.
- Kaynak ses tanıma çıktısıdır. Önceki ve sonraki satırlara bakarak duyma hatalarını düzelt ama uydurma; emin değilsen kısa ve nötr çevir. "Alo" gerçek telefon açılışıdır ("Halo"). Jenerik: "Next Star Televizyon Yeraltı'nı sunar" -> `Next Star Televizyon mempersembahkan Yeraltı.`
- Etiketlerin hiçbiri (`K3`, `(?)`, `[..?]`, `{W:}`) çıktıya yazılmaz.

## Çıktı

```
0012 Haydar, tutup mulut lo!
```
- Her satır: numara, boşluk, Endonezce metin. Satır sayısı ve numaralar girdiyle birebir aynı; birleştirme, bölme, sıra değiştirme yok.
- En fazla 2 ekran satırı, her biri en fazla 42 karakter (kesin sınır 46). Uzun metni kod kendisi iki satıra böler; `|` koymak zorunlu değil ve eksikliği hata değil. Bölme yeri anlam için önemliyse koy (`Lo pikir gue takut?|Gue udah bosen masuk bui.`); 42 karakteri geçmeyen tek konuşmacılı metinde koyma.
- Bir cümle birkaç satıra yayılmışsa önce cümlenin tamamını Endonezce kur, sonra Endonezce söz dizimine göre satırlara dağıt. Türkçede fiil sonda olduğu için kelime kelime gitme. Her satır tek başına okunabilir olsun, hiçbiri boş kalmasın.
- `-` (örnek `0031 -`) satırı altyazıdan çıkarır. Sadece şunlar için: konuşma olmayan çöp (müzik, "Altyazı M.K."), tek başına anlamsız dolgu sesi ("Ee", "Hı", "Hıh", "Hmm"), gülme, ağlama, nefes. Anlamlı ünlemler ve tekrar eden kısa sözler gerçek konuşmadır, çevrilir.
- Şarkı sözü (arka planda ya da karakter söylüyor): tam sözleri çevirme; kısa bir öz, italik ve nota işaretiyle: `0123 <i>♪ Lirik ♪</i>`, iki satırsa `<i>♪ birinci|ikinci ♪</i>`. Etiketler sınıra sayılmaz. Konuşmayla karışırsa konuşmayı öncele.
- Düz tırnak ve düz tire; süslü Unicode yok.

## Üslup: suç dizisi, doğal Endonezce

- Kelimeyi değil işlevi çevir: Türkçe söz o sahnede ne iş görüyorsa (tehdit, saygı, yemin, sitem, alay) Endonezcede o işi gören sözü yaz. "Bir Endonezyalı gangster/aile bu sahnede ne derdi?" diye sor.
- SANSÜRLEME, yumuşatma, kibarlaştırma, açıklama ekleme yok. Küfür ve hakaret aynı şiddette.
- Konuşma dili: `nggak`, `udah`, `aja`, `cuma`, `banget`, `bakal`, `mau`, `gimana`, `kenapa`, `kayak`, `sama`, `bilang`, `ngomong`, `-in` ekli fiiller. Gündelik sahnede `tidak`, `sudah`, `saja`, `akan`, `ingin`, `apakah`, `bagaimana`, `adalah`, `tetapi`, `namun`, `kepada` kullanma. Yazı dili (`tersebut`, `merupakan`) hiç yok.
- Ton parçacıkları (`sih`, `kok`, `dong`, `deh`, `lho`, `kan`, `nih`, `tuh`, `ya`) ölçülü; her satıra doldurma.
- Özne/nesne bağlamdan belliyse at. Türkçedeki her "ben", "sen"i yazma.
- Tehdit ve kavga replikleri KISA ve vurucu. Uzun açıklayıcı cümle kurma.
- Resmi sahnelerde (savcı, polis, avukat, hâkim, doktor, gardiyan resmi konuşurken) `saya` / `Anda`, `Pak` / `Bu`; argo yok ama yine kısa ve sade.
- Deyim ve atasözü kelime kelime çevrilmez; Endonezce eşdeğeri ya da düz anlamı.
- Sınıra sığmıyorsa önce dolgu sözleri, tekrarları ve hitabı at; anlamı taşıyan kısmı koru.

## Zamirler (aynı iki kişi arasında bölüm boyunca aynı)

- Erkekler arası, sokak, rakipler, tehdit, kavga, hapishane, arkadaşlar: `gue` / `lo`.
- Aile içi, sevgililer, karı-koca, anne-oğul, duygusal ve saygılı yakın konuşma: `aku` / `kamu`.
- Büyüğe / patrona / aile reisine saygıyla: konuşan `saya` ya da `aku`, karşısındakine hitapla (`Bos`, `Bang`, `Pak`, `Bu`); `lo` deme.
- Resmi görevliyle: `saya` / `Anda`.
- Aynı kişi öfkelenince geçici olarak `lo`'ya dönebilir (sahnede belirgin kopuş varsa); sakin sahnede eski zamire dön.

## Hitaplar

| Türkçe | Endonezce |
|---|---|
| Abi / Ağabey (isimle ya da isimsiz) | Bang (Bang Haydar) / Abang |
| Abla | Kak / Mbak |
| Reis / Patron / Büyük | Bos |
| X Bey / X Hanım | Pak X / Bu X (mafya büyüğü: Tuan X olabilir, karar verince sabit kal) |
| Anne / Ana | Ma (sevgiyle: Mama) |
| Baba | Pa (sevgiyle: Papa; reis babaya saygıyla: Ayah) |
| amca / dayı | Om (isimle: Om X) |
| teyze / hala | Tante |
| nine / babaanne / anneanne | Nenek |
| dede | Kakek |
| oğlum / kızım (büyükten) | Nak; sokak azarı "oğlum" -> atla |
| kardeşim / birader (sokak) | bro / atla |
| yeğen | atla ya da isim |
| canım / hayatım / aşkım | Sayang |
| yenge | Kakak ipar / Mbak |

## Küfür ve hakaret

| Türkçe | Endonezce |
|---|---|
| Siktir! / Siktir git! | Anjing! / Bangsat! / Pergi lo, anjing! |
| Orospu çocuğu | Bajingan / Anak haram / Bangsat |
| Şerefsiz / Namussuz | Bajingan / Brengsek / Keparat |
| Pezevenk | Germo / Bangsat |
| Köpek / İt | Anjing |
| Salak / Gerizekalı / Aptal | Goblok / Tolol / Bego |
| Hassiktir | Anjir / Sialan |
| Kes sesini! / Kapa çeneni! | Diem lo! / Tutup mulut lo! |
| Seni gebertirim / Öldürürüm | Gue bunuh lo / Mati lo di tangan gue |
| Ananı ... (anaya küfür) | Bangsat / Anjing (anaya küfür Endonezcede doğal değil, en sert eşdeğer) |
| "lan", "ulan", "be" | çoğunlukla at; gerekirse `woi`, `heh` (her satıra koyma) |

## Mafya / sokak jargonu

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
| delikanlı (racon anlamında) | laki-laki sejati / jantan |
| koğuş | sel / blok |

## Özel isimler

- Kişi adları Türkçe yazımıyla, Türkçe harfleriyle kalır (Çiğdem, Ümmü Gülsüm); çevrilmez. Türkçe ekleri at: "Haydar'ın" -> "Haydar".
- Doğru yazım aşağıdaki "Kişiler" listesi ve `onceki_ozet.md`'dir. Ses tanıma bir ismi benzer sesle yanlış yazdıysa listedekini kullan. Listede olmayan yeni isimde kaynaktaki yazımı koru ve raporuna "yeni isim" diye yaz.
- İsme Endonezce ek tireyle: `Halide-ku`.
- Unvan başa: "Yılmaz Bey" -> `Pak Yılmaz`, "Sultan Hanım" -> `Bu Sultan`, "Savcı Bey" -> `Pak Jaksa`, "Komiserim" -> `Komandan` / `Pak`.
- Lakaplar aynen. Anlamı sahnede önemli takma ad çevrilir ve her yerde aynı çevrilir; ilk kullandığını raporuna yaz.
- Yer adları: Endonezcede yerleşik adı olanlar o adla (`Istanbul`, `Ankara`, `Turki`, `Jerman`); semt, sokak, mahalle, mekân, şirket adları aynen.
- Para, sayı, tarih, saat değiştirilmez: "500 bin lira" -> `500 ribu lira`.

## Kişiler

Kaynak: NOW/haber siteleri (Milli Gazete, Habertürk, TVmaze; 26 Kasım 2026 tarandı) ve İsmail'in S01E16 doğrulaması. Bölümde gördüğün sahne bu listeyle çelişirse sahneye uy ve raporuna yaz.

Konu: Haydar Ali, derin devletin gizli görevle mafyaya soktuğu adam. Ailesinin katili Bedrettin Hanoğlu'nu öldürüp hapse girer; İstanbul'un en tehlikeli kartellerinden birinin ortasında kalır. 1. bölümde Ceylan'la tanışır. Üç yıl sonra çıktığında unutamadığı kadın en yakın adamının (Bozo) karısıdır.

**Aslan ailesi**
- **Haydar Ali Aslan**: ana karakter. Ailesini küçükken kaybetti, Avrupa'da büyüdü, dövüş eğitimli. Bozo ile hem dost hem rakip.
- **Melek Aslan**: Haydar Ali'nin kız kardeşi; suç dünyasının dışında kalmak istiyor, Ceylan'la yakın.

**Hanoğlu ailesi** ("Hanoğulları" aynen kalır)
- **Bozkurt Hanoğlu, lakabı Bozo**: diyalogda hep "Bozo". Kartelin başına geçen asi, tehlikeli adam; Ceylan'a âşık, sonra kocası. Sultan'ın abisi. Ses tanıma "Bozu" yazabilir -> Bozo.
- **Sultan Hanoğlu**: Bozo'nun kız kardeşi, aile parasını yönetir. 1. bölüm sonunda Bozo onun Ferhat'la nişanını bozup Haydar Ali'yle nişanlar.
- **Merdan Hanoğlu**: hesapçı, stratejik; Bozo'nun yükselişini kabullenir ama kendi oyununu oynar.
- **Ferhat Hanoğlu**: Bedrettin'in oğlu, Merdan'ın küçük kardeşi; Bozo'ya Bang der.
- **Paşa Hanoğlu**: Bozo'nun baba bir kardeşi; fevri, ağabeyine bağlı, kız kardeşine yumuşak. ("Paşa" isimdir; "paşam" hitabıyla karıştırma.)
- **Bedrettin Hanoğlu (Bedo)**: Bozo'nun amcası, Ferhat ve Merdan'ın babası; 1. bölümde Haydar onu öldürür; Bozo'nun babasını ve Haydar Ali'nin ailesini öldürdü.

**Diğerleri**
- **Efraim (Efo)**: Bozo'nun sağ kolu. **Yavuz**: Bozo'nun kan bağı olmayan "has kardeşi", mahalleyi yönetir. **Adnan**: hapiste Haydar'ın "gölgesi". **Vefo**: Bozo'nun adamı. **Yılmaz**: istihbarat amiri (Haydar'ın bağlantısı), yardımcısı Aslı. Ayrıca gardiyan/başgardiyan bir Yılmaz da olabilir, karıştırma.
- Ceylan Haydar'a "Ali" der. Haydar, Bozo'nun yanında Ceylan'a "yenge" -> `Mbak`.
- Sabit karşılıklar (1. bölüm): "aslanım" -> `Jagoan`; "ömrüm" -> `Sayangku`; başgardiyan "başefendi" -> `Komandan`; cezaevi müdürü -> `Pak Kalapas`; koğuş -> `sel`; mahalle -> `wilayah`; amca oğlu -> `Sepupu`; Bozo'nun "kızım" (Sultan'a) -> `Dik`.
- **Ceylan** (tam adı Halide Ceylan): herkes "Ceylan" der, sen de hep `Ceylan` yaz. Haydar Ali'nin aşkı.
- **Komiser Pınar** (Pınar Esen): polis; ona ve ondan resmi hitap (`Komisaris Pınar` / `Bu Pınar`, `saya` / `Anda`).
- Gülsüm (kaynaklarda "Ümmü Gülsüm" de geçer), Yılmaz, Efraim, Yavuz, Aslı, Adnan, Ayşen, Yıldız, Hamburglu (lakap; aynen). Rolleri kaynakta yok; sahneden anla, raporuna yaz.
- **Kartal**: Bozo'nun düşmanı (İsmail, S01E16).
- S01E16'da ayrıca: Sezai, Emre, Hasan, Çiğdem ("Cidem" değil), Volkan, Hande, Can, Cengiz, Azize (kadın; "Aziz" yazma).

## Yalancı eşdeğerler ve kalıp sözler

Türkçe kalıbın Endonezcede aynı kelimeyle karşılığı çoğu zaman BAŞKA anlama gelir. İşleve göre seç; sokak sahnesinde gue/lo'ya uyarla:

| Türkçe (işlev) | Endonezce | Yapma |
|---|---|---|
| Estağfurullah (nezaket: "ne demek, olur mu öyle şey") | Ah, nggak kok / Nggak apa-apa / Jangan gitu | "Astagfirullah" yazma: o dehşet ünlemidir |
| Tövbe tövbe / Tövbe de (kınama, "ağzından yel alsın") | Astagfirullah / Hus, amit-amit | "Tobat" yazma: "tövbe et" emri gibi okunur |
| Allah korusun / Allah göstermesin | Amit-amit / Jangan sampai / Naudzubillah | |
| Allah aşkına (yakarma, bıkkınlık) | Ya ampun / Tolonglah / Astaga | "Demi Allah" yazma: o yemindir |
| Vallahi / Yemin ederim (yemin, vurgu) | Sumpah / Demi Allah | Her "vallahi"ye koyma; vurgu zayıfsa "beneran", "asli" |
| Allah Allah (şaşkınlık, sitem) | Ya ampun / Astaga / Lho | |
| Allah'ım / Ya Rabbim (korku, yakarış, sabır) | Ya Allah / Ya Rabb | |
| La havle... (sabır taşması) | Ya Allah, beri aku sabar | Arapçasını yazma, sığmaz |
| İnşallah / Maşallah | Insyaallah / Masyaallah | |
| Çok şükür / Hamdolsun | Alhamdulillah / Syukurlah | |
| Allah razı olsun | Makasih banyak (gündelik) / Semoga Allah membalas kebaikanmu (içten dua) | |
| Allah rahatlık versin | Selamat tidur | |
| Geçmiş olsun | Semoga cepat sembuh (hastalık) / Syukurlah udah lewat (atlatılan sıkıntı) | |
| Başın sağ olsun | Turut berduka cita | |
| Hayırlı olsun | Selamat, ya / Semoga berkah | |
| Kolay gelsin | Semangat, ya / Selamat bekerja | |
| Eyvallah (tamam, sağ ol, hoşça kal) | Siap / Makasih, Bang / Oke | Tek karşılık yok, sahneye bak |
| Helal olsun (takdir) | Mantap / Salut | |
| Hakkını helal et (veda) | Maafin semua salahku | |
| Allah belanı versin (beddua) | Terkutuk lo / Semoga Allah melaknat lo | |
| Allah rahmet eylesin | Semoga Allah merahmatinya | |
| Eline sağlık | Makasih, enak banget | |
| Afiyet olsun | Selamat makan | |
| Çok yaşa / Sen de gör (hapşırma) | Panjang umur / Sehat selalu | |
| Hoş geldin / Hoş bulduk | Selamat datang / Makasih | |
| Hayırdır? (meraklı / tehditkâr) | Ada apa, nih? / Mau apa lo? | |
| Buyurun (kapıda / ikramda / "sizi dinliyorum") | Silakan masuk / Silakan / Ya, ada apa? | |
| Efendim? (duymadım / telefonda) | Apa? / Ya? / Halo? | "Tuan" yazma |
| Tamam / Peki / Olur | Oke / Iya / Ya udah / Baik (resmi) | Hep "Oke" yazma, tona göre seç |
| Hadi (teşvik / acele / inanmama) | Ayo / Cepat / Masa sih | |
| Yok artık / Hadi canım (inanmama) | Masa sih / Yang bener aja | |
| Boş ver / Neyse | Udahlah / Ya udahlah | |
| Kusura bakma / Affedersin | Maaf, ya / Sori | |
| Aman / Sakın (uyarı) | Jangan sampai / Awas, ya | |

Genel ilke: Insyaallah, Masyaallah, Alhamdulillah, Astagfirullah, Ya Allah Endonezce gündelik konuşmada doğaldır; gerçek dua ve yakarışta "Allah"ı koru ("Semoga Allah ..."). Ama Türkçedeki her "Allah"lı ünlemi Arapça kalıba çevirme; sıradan şaşkınlık ve sitemde "Ya ampun", "Astaga", "Lho" daha doğal.
