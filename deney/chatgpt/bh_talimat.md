# Başkalarının Hayatı - Endonezce çeviri talimatı

İzleyen: İsmail ve Endonezyalı kız arkadaşı. Amaç: TV'de izlenen, doğal, konuşma dilinde Endonezce altyazı; bir Endonezya dizisinin altyazısı gibi okunmalı. Akış `ceviri/YONTEM.md`'de, bu dosya sadece çeviri kurallarıdır. Son güncelleme: 10 Kasım 2026.

Dizi: Star TV, cumartesi 20:00 TR. Thackeray'in "Vanity Fair"inden esinlenme. Hülya yoksul bir aileden gelen, hırslı bir genç kadın; zengin Özkaran ailesinin dünyasına girer. Sınıf farkı, sırlar, aşk üçgenleri.

## Girdi

```
0012 [1.9s|38] (?) K3 Tövbe bismillah, [bile?] yaklaşmayacak.
```
- `0012` satır numarası, çıktıda aynen kullanılır.
- `[1.9s|38]` ekranda kalma süresi ve Endonezce için en fazla karakter (20 kar/sn). Aşma; gerekirse anlamı koruyarak kısalt.
- `K3` konuşmacı etiketi, isim değil: "aynı numara = aynı ses". Otomatik olduğu için yanılabilir. Kimin kime konuştuğunu anlamak için kullan.
- `K2>K1` aynı satırda önce K2, sonra K1 konuşuyor. İçeriğe bak: gerçekten iki kişi konuşuyorsa (soru-cevap, karşılıklı laf) `- birinci|- ikinci` yaz, aynı kişi devam ediyorsa tire kullanma. Üç konuşmacı varsa en doğal iki parçaya indir.
- `[kelime?]` kaynak o kelimeden, `(?)` satırın çoğundan emin değil. Bağlama uyan benzer sesli Türkçeyi düşün, ona göre çevir.
- `{W: ...}` varsa ikinci bir duyuştur; asıl metin bağlama oturmuyorsa ona bak.
- `--` ya da sonda `-` yarıda kesilen konuşma: doğal çevir, `...` ya da `--` ile bitir.
- Kaynak ses tanıma çıktısıdır. Önceki ve sonraki satırlara bakarak duyma hatalarını düzelt ama uydurma; emin değilsen kısa ve nötr çevir. "Alo" gerçek telefon açılışıdır ("Halo").
- Etiketlerin hiçbiri (`K3`, `(?)`, `[..?]`, `{W:}`) çıktıya yazılmaz.

## Çıktı

```
0012 Astagfirullah, dia nggak bakal mendekat lagi.
```
- Her satır: numara, boşluk, Endonezce metin. Satır sayısı ve numaralar girdiyle birebir aynı; birleştirme, bölme, sıra değiştirme yok.
- En fazla 2 ekran satırı, her biri en fazla 42 karakter (kesin sınır 46). Uzun metni kod kendisi iki satıra böler; `|` koymak zorunlu değil ve eksikliği hata değil. Bölme yeri anlam için önemliyse koy (`Kamu gila, ya?|Ngapain kamu ke sini?`); 42 karakteri geçmeyen tek konuşmacılı metinde koyma.
- Bir cümle birkaç satıra yayılmışsa önce cümlenin tamamını Endonezce kur, sonra Endonezce söz dizimine göre satırlara dağıt. Türkçede fiil sonda olduğu için kelime kelime gitme. Her satır tek başına okunabilir olsun, hiçbiri boş kalmasın.
- `-` (örnek `0031 -`) satırı altyazıdan çıkarır. Sadece şunlar için: konuşma olmayan çöp (müzik, "Altyazı M.K."), tek başına anlamsız dolgu sesi ("Ee", "Hı", "Hıh", "Hmm"), gülme, ağlama, nefes. Anlamlı ünlemler ("Aha", "Ay", "Of", "Aman") ve tekrar eden kısa sözler gerçek konuşmadır, çevrilir.
- Şarkı sözü (arka planda ya da karakter söylüyor): tam sözleri çevirme; kısa bir öz, italik ve nota işaretiyle: `0123 <i>♪ Lirik ♪</i>`, iki satırsa `<i>♪ birinci|ikinci ♪</i>`. Etiketler sınıra sayılmaz. Konuşmayla karışırsa konuşmayı öncele.
- Düz tırnak ve düz tire; süslü Unicode yok.

## Üslup: doğal Endonezce

- Kelimeyi değil işlevi çevir: Türkçe söz o sahnede ne iş görüyorsa (teşekkür, sitem, şaşkınlık, yemin, nezaket, alay) Endonezcede o işi gören sözü yaz. "Bir Endonezyalı bu sahnede ne derdi?" diye sor.
- Günlük sahnelerde konuşma dili: `aku`, `kamu`, `nggak`, `udah`, `aja`, `cuma`, `banget`, `bakal`, `mau`, `pengin`, `gimana`, `kenapa`, `kayak`, `sama` (dengan/kepada yerine), `bilang`, `ngomong`, `-in` ekli fiiller (`beresin`, `bilangin`, `tungguin`). Bu sahnelerde `tidak`, `sudah`, `saja`, `hanya`, `sangat`, `akan`, `ingin`, `apakah`, `bagaimana`, `mengapa`, `adalah`, `tetapi`, `namun`, `kepada` kullanma.
- Duygu ve ton parçacıklarla verilir, cümle uzatılmaz: `sih`, `kok`, `dong`, `deh`, `lho`, `kan`, `nih`, `tuh`, `ya`, `yuk`. Her satıra doldurma; Türkçedeki "ya", "be", "ki", "işte", "yani", "hadi" neye yarıyorsa onu karşılayanı seç.
- Özne ve nesne bağlamdan belliyse at (`Udah makan?`, `Nggak tahu.`). Türkçedeki her "ben", "sen"i yazma.
- Resmi ve saygılı sahnelerde (doktor, müdür, memur, polis, mahkeme, resmi telefon) `saya` / `Anda` ya da `Bapak` / `Ibu`, `tidak`, `sudah`. Argo yok ama cümle yine kısa ve sade; yazı dili (`adalah`, `tersebut`, `merupakan`) yine yok.
- Aynı iki kişi arasındaki hitap ve zamir (aku/kamu, saya/Anda, gue/lo) bölüm boyunca aynı kalır; ilişki değişmedikçe değiştirme.
- Deyim ve atasözü: kelime kelime çevirme. Endonezcede aynı işi gören deyim varsa onu, yoksa düz anlamını yaz.
- Duyguyu koru: romantizm, öfke, alay, kıskançlık, mizah. Sansürleme, yumuşatma, açıklama ekleme. Küfür ve hakaret aynı şiddette Endonezce karşılığıyla.
- Kısa ve net. Sınıra sığmıyorsa önce dolgu sözleri, tekrarları ve hitabı at; anlamı taşıyan kısmı koru.

## Özel isimler

- Kişi adları ve soyadları Türkçe yazımıyla, Türkçe harfleriyle kalır (Hülya, Özlem, Çiğdem); çevrilmez, Latinleştirilmez. Türkçe ekleri at: "Hülya'nın" -> "Hülya", "Kadir'e" -> "Kadir".
- Doğru yazım aşağıdaki "Kişiler" listesi ve `onceki_ozet.md`'dir. Ses tanıma bir ismi benzer sesle yanlış yazdıysa listedeki yazımı kullan. Listede olmayan yeni isimde kaynaktaki yazımı koru ve raporuna "yeni isim" diye yaz.
- İsme Endonezce ek tireyle gelir: `Gülizar-ku`.
- Unvan başa gelir: "Fikret Bey" -> `Pak Fikret`, "Jale Hanım" -> `Bu Jale`, "Doktor Sarp" -> `Dokter Sarp`, "Avukat Defne Hanım" -> `Bu Defne`.
- Lakaplar ve kısaltmalar aynen kalır. Anlamı sahnede önemli olan takma ad (hakaret, sevgi sözü) çevrilir ve her yerde aynı çevrilir; ilk kullandığını raporuna yaz.
- Yer adları: Endonezcede yerleşik adı olan ülke ve şehirler o adla (`Istanbul`, `Izmir`, `Ankara`, `London`, `Jerman`, `Amerika`, `Prancis`, `Yunani`, `Turki`). Semt, sokak, mahalle, okul, şirket, marka adları aynen (Türkçe harfleriyle).
- Türk yemekleri ve kültür sözleri: Endonezyalının tanıdığı aynen (`kebab`, `baklava`, `börek`, `simit`, `rakı`); tanımadığı ve sahnede önemsiz olan genel adla (`kue`, `sup`, `teh`). Açıklama ekleme.
- Para, sayı, tarih, saat değiştirilmez: "500 bin lira" -> `500 ribu lira`.

## Hitaplar (bölümler arası tutarlı)

| Türkçe | Endonezce |
|---|---|
| Anne / Ana | Ma (yetişkin evladın sevgiyle "anneciğim"i: Mama) |
| Baba | Pa (sevgiyle "babacığım": Papa) |
| Abi / Abla (isimsiz ya da isimle) | Kak (Kak Tolga) |
| amca / dayı | Om |
| teyze / hala | Tante |
| anneanne / babaanne / nine | Nenek |
| dede | Kakek |
| X Bey / X Hanım | Pak X / Bu X |
| hocam | Pak / Bu |
| doktor bey / doktor hanım | Dokter / Dok |
| canım / hayatım / aşkım (sevgililer) | Sayang |
| kızım / oğlum (ebeveynden ya da büyükten) | Nak |
| kardeşim (arkadaşlar arası) | Bro |
| efendim / hanımefendi / beyefendi (hizmetliden) | Tuan / Nyonya |
| X Hanım (çalışanlardan genç kıza: Neslihan, Hülya) | Nona X |

- Zengin aileler (Özkaran, Korhanlı) içindeki resmi, soğuk konuşmalarda ve hizmetli-patron arasında saya / Anda ya da Pak / Bu; arkadaşlar, sevgililer ve gençler arasında aku / kamu. Kaba sokak ağzında (Salih ve çevresi) gue / lo.
- Hülya-Neslihan aku / kamu; Hülya-Sema Kak / Dek; Erim-Sarp aku / kamu, Bro; Mediha-Fikret Pak Fikret / Bu Mediha, saya / Anda.
- Yeni hitap ya da takma ad çıkarsa raporuna yaz; `ozet.md`'ye girer, sonraki bölüm onu izler. `onceki_ozet.md` buradakiyle çelişirse özete uy.

## Kişiler

- **Hülya** (Hülya Aydın; asla "Hulya"): ana karakter. Annesi **Nermin** (terzi; "Neriman" DEĞİL), ablası **Sema**, babası **Salih** (hapisten çıktı; Hülya'ya lakabı "karaböcük" = `kecoak hitam`). Komşular: **Gülizar** ("Gül"), **Mustafa** ("Mustim"), babası **Hüseyin**, **Zehra**.
- **Neslihan Özkaran**: Fikret'in kızı, Erim'in çocukluk aşkı. **Fikret Özkaran**: babası; ölen karısı **Nisan**. **Mediha** (lakabı **Mediş**; ses tanıma "Betiş", "Meda" yazabilir): Neslihan'ı büyüten çalışan. Şoför **Nihat**, çalışanlar **Gülşah**, **Kübra**, **Zeynep**, **Hasan**. **İlayda**, **Orhan**.
- **Erim Korhanlı**: **Haluk** ve **Jale Korhanlı**'nın oğlu. **Yusuf**: Haluk'un sağ kolu.
- **Sarp**: doktor, Erim'in en yakın arkadaşı. Annesi **Perihan**, kız kardeşi **Dila**.
- Sema'nın patronu **Burak**, iş yerinden **Ceren**. Aileler: `Özkaran`, `Korhanlı`, `Sezginel`.

## Yalancı eşdeğerler ve kalıp sözler

Türkçe kalıbın Endonezcede aynı kelimeyle karşılığı çoğu zaman BAŞKA anlama gelir. İşleve göre seç:

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
| Eline sağlık | Makasih, enak banget | |
| Afiyet olsun | Selamat makan | |
| Çok yaşa / Sen de gör (hapşırma) | Panjang umur / Sehat selalu | |
| Hoş geldin / Hoş bulduk | Selamat datang / Makasih | |
| Hayırdır? | Ada apa, nih? | |
| Buyurun (kapıda / ikramda / "sizi dinliyorum") | Silakan masuk / Silakan / Ya, ada apa? | |
| Efendim? (duymadım / telefonda) | Apa? / Ya? / Halo? | "Tuan" yazma |
| Tamam / Peki / Olur | Oke / Iya / Ya udah / Baik (resmi) | Hep "Oke" yazma, tona göre seç |
| Hadi (teşvik / acele / inanmama) | Ayo / Cepat / Masa sih | |
| Yok artık / Hadi canım (inanmama) | Masa sih / Yang bener aja | |
| Boş ver / Neyse | Udahlah / Ya udahlah | |
| Kusura bakma / Affedersin | Maaf, ya / Sori | |
| Aman / Sakın (uyarı) | Jangan sampai / Awas, ya | |

Genel ilke: Insyaallah, Masyaallah, Alhamdulillah, Astagfirullah, Ya Allah Endonezce gündelik konuşmada doğaldır; gerçek dua ve yakarışta "Allah"ı koru ("Semoga Allah ..."). Ama Türkçedeki her "Allah"lı ünlemi Arapça kalıba çevirme; sıradan şaşkınlık ve sitemde "Ya ampun", "Astaga", "Lho" daha doğal.
