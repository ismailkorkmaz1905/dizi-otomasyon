# Başkalarının Hayatı - Endonezce çeviri talimatı (Claude için)

Bu dosya Claude'un her bölümde çeviri adımını nasıl yapacağını anlatır. İzleyen: İsmail ve Endonezyalı kız arkadaşı. Amaç: TV'de Infuse ile izlenen, doğal, konuşma dilinde Endonezce altyazı. Kurallar Muhtemel Aşk talimatından alındı, dizinin isimleri ve hitapları bölümler ilerledikçe `ozet.md`'lerle tamamlanır. Oluşturma: 19 Ekim 2026.

Dizi: Star TV, cumartesi 20:00 TR (ilk bölüm 26 Eylül 2026). Ay Yapım, senaryo Banu Kiremitçi Bozkurt; Thackeray'in "Vanity Fair"inden esinlenme. Hülya yoksul bir aileden gelen, yarı burslu üniversiteli, hırslı bir genç kadın. Zengin Özkaran ailesinin kızı Neslihan'la arkadaş olur ve o dünyaya girmeye çalışır. Sınıf farkı, sırlar, aşk üçgenleri.

## Girdi formatı

```
0012 [1.9s|38] (?) K3 Tövbe bismillah, [bile?] yaklaşmayacak. {W: Tövbe bismillah, bir daha yaklaşmayacak.}
```
- `0012` satır numarası. Çıktıda aynen kullan.
- `[1.9s|38]` ekranda kalma süresi ve Endonezce için en fazla karakter (okuma hızı 20 kar/sn). Bu sınırı aşma, gerekirse anlamı koruyarak kısalt.
- `K3` konuşmacı etiketi (sadece metin Scribe'dan geldiyse). İsim DEĞİL: "aynı numara = aynı ses" demek, otomatik olduğu için yer yer yanılır (aynı kişiye birkaç numara verebilir). Kimin kime konuştuğunu ve hitabı anlamak için kullan, çıktıya YAZMA.
- `K2>K1` aynı satırda önce K2, sonra K1 konuşuyor. Gerçekten iki farklı kişi konuşuyorsa satırı iki parça yap: `- birinci|- ikinci`. Buna etikete körü körüne değil içeriğe bakarak karar ver (soru-cevap, karşılıklı laf). Aynı kişi devam ediyorsa tire kullanma. Üç konuşmacı varsa en doğal iki parçaya indir.
- `[kelime?]` kaynak tam o kelimeden emin değil. Önce o kelimenin yerine bağlama uyan benzer sesli Türkçeyi düşün.
- `(?)` kaynak satırın çoğundan emin değil. Bağlama bakıp en makul Türkçeyi tahmin ederek çevir.
- `{W: ...}` ikinci göz: Whisper aynı yeri belirgin farklı duymuş. Asıl metin (Scribe) çoğunlukla doğrudur; ama asıl metin bağlama oturmuyorsa `{W: ...}` içindekine bak, hangisi sahneye uyuyorsa onu çevir. İkisini birden çevirme, `{W: ...}` kısmını çıktıya yazma.
- `--` yarıda kesilen konuşma. Doğal çevir, gerekirse `...` ile bitir.
- Kaynak ses tanıma çıktısıdır, yazım/duyma hataları olabilir. Önceki/sonraki satırlara bakarak düzelt, ama uydurma. Emin değilsen kısa ve nötr çevir.
- Scribe metnine güven: "Alo" gerçek telefon açılışıdır ("Halo"), başka bir şeye çevirme.

## Çıktı formatı

Her satır: numara, boşluk, Endonezce metin.
```
0012 Astagfirullah, dia nggak bakal mendekat lagi.
```
- Satır sayısı ve numaralar girdiyle birebir aynı. Birleştirme, bölme, sıra değiştirme YOK. Zamanlar Python'da, dokunulmaz.
- İki satıra bölmek istersen `|` kullan: `0020 Kamu gila, ya?|Ngapain kamu ke sini?` Yoksa kod otomatik böler.
- En fazla 2 ekran satırı; her satır en fazla 42 karakter (kesin üst sınır 46). 42 karakteri geçmeyen tek konuşmacılı metinde `|` koyma.
- `-` (satırı altyazıdan çıkarır: `0031 -`) sadece şunlar için: konuşma olmayan çöp (müzik, "Altyazı M.K."), tek başına anlamsız dolgu sesi ("Ee", "Hı", "Hıh", "Hah", "Hmm"), gülme/ağlama/nefes. Anlamlı ünlemler ("Aha", "Ay", "Of", "Aman") ve tekrar eden kısa sözler gerçek konuşmadır: çevir, silme.
- Şarkı sözü (arka planda çalan ya da karakterin söylediği): tam sözleri çevirme; kısa ve doğal bir öz, italik ve nota işaretiyle: `0123 <i>♪ Lirik ♪</i>`; iki satır gerekirse `<i>♪ birinci|ikinci ♪</i>`. Etiketler karakter sınırına sayılmaz. Konuşmayla aynı satıra karışırsa konuşmayı öncele.
- Düz tırnak ve düz tire kullan; süslü Unicode yok.

## Üslup

- Doğal, konuşma dilinde Endonezce. Kitap dili, çeviri kokan cümle yok. Bir Endonezya dizisinin altyazısı gibi okunmalı.
- Günlük diyalogda `aku`, `kamu`, `nggak`, `udah`, `aja`, `banget`, `sih`, `kok`, `dong` uygun. Resmi/saygılı sahnelerde (doktor, hoca, müdür, memur, telefonla resmi görüşme) `saya` / `Anda`, `Pak`, `Bu`; zorlama argo kullanma.
- Zengin aile (Özkaran, Korhanlı) içindeki resmi, soğuk konuşmalarda ve hizmetli-patron arasında `saya` / `Anda` ya da `Pak` / `Bu` daha doğal olabilir; arkadaşlar, sevgililer ve gençler arasında aku / kamu. Kaba ya da sokak ağzı konuşmada (ör. Salih ve çevresi) gue / lo uygun olabilir; sahneye göre seç ve aynı ikili için bölüm boyunca tutarlı kal.
- Duyguyu koru: romantizm, öfke, alay, kıskançlık, sınıf aşağılaması. Sansürleme, yumuşatma, açıklama ekleme.
- Kelimeyi değil işlevi çevir: Türkçe kalıp o sahnede ne iş görüyorsa (teşekkür, sitem, şaşkınlık, yemin, nezaket) Endonezcede o işi gören sözü yaz. Aşağıdaki tablolar bunun için.
- İsimleri çevirme. Sayı, tarih, para değerlerini değiştirme.
- Kısa ve net: altyazı okunacak, ekran süresi kısa.

## İsimler ve kişiler

Kaynak: basındaki oyuncu listeleri (19 Ekim 2026). İlişkiler bölüm özetleriyle (`onceki_ozet.md`) düzeltilir; özet buradakiyle çelişirse özete güven.

- **Hülya**: ana karakter, yoksul aileden, yarı burslu üniversite öğrencisi. Annesi terzi, ablası evin geçimine ve Hülya'nın okuluna destek oluyor. Babası **Salih** hapisten çıkıyor (3. bölüm).
- **Neslihan Özkaran**: Hülya'nın üniversitedeki yakın arkadaşı, Fikret Özkaran'ın kızı. Erim'in çocukluk aşkı; Erim ona evlenme teklif etti. Bir sırrı var.
- **Fikret Özkaran**: Neslihan'ın babası. **Mediha**: Özkaranlara yakın, Hülya'dan şüphelenen kadın (ilişkisi bölümlerden öğrenilecek).
- **Erim Korhanlı**: Haluk ve Jale Korhanlı'nın oğlu, Londra'dan döndü. Hülya ona yaklaşmaya çalışıyor.
- **Haluk Korhanlı**, **Jale Korhanlı**: Erim'in anne babası.
- **Sarp**: doktor; Hülya ile aralarında çekim var, Hülya'nın sırlarından şüpheleniyor.
- Diğerleri: Sema, Neriman, Perihan, Yusuf, Dila, Mustafa, Cengo, Gülizar, Hüseyin, Nihat, Zeynep. Aileler: Özkaran, Korhanlı, Sezginel (Salih'in geçmişiyle bağlantılı).
- Soyadları aynen: `Özkaran`, `Korhanlı`, `Sezginel` (Türkçe harfleriyle). "Hülya" asla "Hulya" değil.

## Hitaplar (bölümler arası tutarlı)

| Türkçe | Endonezce |
|---|---|
| Anne / Ana | Ma (yetişkin evladın sevgiyle "anneciğim"i: Mama) |
| Baba | Pa (sevgiyle "babacığım": Papa) |
| Abi / Abla (isimsiz ya da isimle) | Kak (Kak Neslihan) |
| amca / dayı | Om |
| teyze / hala | Tante |
| anneanne / babaanne / nine | Nenek |
| dede | Kakek |
| X Bey / X Hanım | Pak X / Bu X |
| efendim / hanımefendi / beyefendi (hizmetliden) | Tuan / Nyonya |
| hocam | Pak / Bu (isimsiz) |
| doktor bey / doktor hanım | Dokter / Dok |
| canım / hayatım / aşkım (sevgililer) | Sayang |
| kızım / oğlum (ebeveynden) | Nak |
| kardeşim (arkadaşlar arası) | Bro |

- Hülya ile Neslihan birbirine aku / kamu.
- Yeni hitaplar çıktıkça bölüm `ozet.md`'sine yaz; sonraki bölüm onu izler.

## Yalancı eşdeğerler ve kalıp sözler

Türkçe kalıbın Endonezcede aynı kelimeyle karşılığı çoğu zaman BAŞKA anlama gelir. İşleve göre seç:

| Türkçe (işlev) | Endonezce | Yapma |
|---|---|---|
| Estağfurullah (nezaket: "ne demek, rica ederim, olur mu öyle şey") | Ah, nggak kok / Nggak apa-apa / Jangan gitu | "Astagfirullah" yazma: o dehşet ünlemidir |
| Tövbe tövbe / Tövbe de / Tövbe estağfurullah (kınama, "ağzından yel alsın") | Astagfirullah / Hus, amit-amit | "Tobat" yazma: "tövbe et" emri gibi okunur |
| Allah korusun / Allah göstermesin | Amit-amit / Jangan sampai / Naudzubillah | |
| Allah aşkına (yakarma, bıkkınlık) | Ya ampun / Tolonglah / Astaga | "Demi Allah" yazma: o yemindir |
| Vallahi / Yemin ederim / Allah şahidim (yemin, vurgu) | Sumpah / Demi Allah | Her "vallahi"ye koyma; vurgu zayıfsa "beneran", "asli" |
| Allah Allah (şaşkınlık, sitem) | Ya ampun / Astaga / Lho | |
| Allah'ım / Ya Rabbim (korku, yakarış, sabır) | Ya Allah / Ya Rabb | |
| La havle... (sabır taşması) | Ya Allah, beri aku sabar | Arapçasını yazma, sığmaz |
| İnşallah | Insyaallah | |
| Maşallah | Masyaallah | |
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
| Alo | Halo | |

Genel ilke: Insyaallah, Masyaallah, Alhamdulillah, Astagfirullah, Ya Allah Endonezce gündelik konuşmada doğaldır, gerçek dua ve yakarışta "Allah"ı koru ("Semoga Allah ..."). Ama Türkçedeki her "Allah"lı ünlemi Arapça kalıba çevirme; sıradan şaşkınlık ve sitemde "Ya ampun", "Astaga", "Lho" daha doğal.
