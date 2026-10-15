# Muhtemel Aşk - Endonezce çeviri talimatı (Claude için)

Bu dosya Claude'un her bölümde çeviri adımını nasıl yapacağını anlatır. İzleyen: İsmail ve Endonezyalı kız arkadaşı. Amaç: TV'de Infuse ile izlenen, doğal, konuşma dilinde Endonezce altyazı. Son güncelleme: 13 Ekim 2026 (şarkı sözü ve anne hitabı).

## Klasörler (Google Drive, "Muhtemel Aşk" klasörü)

- `Sezon 1/Muhtemel.Ask.SxxEyy.mp4` : video (Colab indirir)
- `Sezon 1/Muhtemel.Ask.SxxEyy.ind.srt` : SONUÇ, Claude yazar. Infuse bunu otomatik yükler.
- `_iş/SxxEyy/ceviri_girdi.txt` : çevrilecek satırlar
- `_iş/SxxEyy/tr_cues.json` : zamanlar (build için)
- `_iş/SxxEyy/HAZIR.txt` : Colab bitti işareti
- `_iş/SxxEyy/words.json`, `scribe_raw.json`, `whisper_words.json`, `log.txt` : ses tanıma ara dosyaları (çeviride gerekmez)
- `Yakılı/` : altyazısı videoya yakılmış kopyalar (2. defter)
- `sistem/pipeline.py` : kod (iki dizide aynı dosya), `sistem/check.py` : parça kontrolü
- `sistem/1 - Bölümü Hazırla.ipynb`, `sistem/2 - Yak ve Gönder.ipynb` : Colab defterleri

## Adımlar

1. Drive'da `_iş/SxxEyy/HAZIR.txt` var mı bak. Yoksa Colab henüz bitmemiş, dur ve söyle.
2. İsmail'e sor: "Çeviri ajanları Sonnet mi Opus mu?" Cevap gelmeden ajan başlatma.
3. `ceviri_girdi.txt`, `tr_cues.json` ve `sistem/pipeline.py` dosyalarını indir. Projedeki bir önceki bölümün özetini (`claude/OZET_SxxEyy.md`) oku.
4. Satırları ~8 eşit parçaya böl. Her parçayı ayrı ajan çevirir: bu talimat, önceki bölüm özeti, parçanın 40 satır öncesi ve 20 satır sonrası bağlam olarak verilir. Her ajan parçasını `check.py` ile denetler.
5. Parçaları birleştir. build'den ÖNCE tek bir kontrol geçişi yap: bütün bölümü kaynakla yan yana oku; hitap tutarlılığı, isimler, parça sınırları, `(?)` / `[kelime?]` / `{W: ...}` işaretli satırlar, aşağıdaki "yalancı eşdeğer" tablosu.
6. build'i Claude çalıştırır (kullanıcıya hücre verme):
   `python pipeline.py build tr_cues.json ceviri_tum.txt Muhtemel.Ask.SxxEyy.ind.srt`
   Eksik/fazla/tekrarlanan satır numarası varsa hata verir, düzelt. `too_fast` / `too_long` listesindeki satırları kısalt, tekrar build et.
7. SRT'yi kontrol et: üst üste binen altyazı ve 0,7 saniyeden kısa süre olmamalı.
8. `.ind.srt` dosyasını `Sezon 1` klasörüne ana oturumdan tek çağrıyla yükle (text/plain, dönüştürme kapalı). Geri indirip yerel dosyayla bayt bayt karşılaştır. Aynı isimde eski dosya varsa ancak yenisi doğrulandıktan SONRA eskisini çöpe at.
9. Bu bölümün özetini aynı biçimde yazıp projeye `claude/OZET_SxxEyy.md` olarak kaydet.
10. Kullanıcıya kısa haber ver. Videoya yakmak/Telegram için `2 - Yak ve Gönder` defterini hatırlat.

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

## Sadece Whisper metninde geçerli duyma hataları

Satırlarda hiç `K` etiketi yoksa metin sadece Whisper'dan gelmiştir (Scribe çalışmamış) ve duyma hatası çoktur. O DURUMDA şu kalıplara dikkat et; Scribe metninde bunları uygulama:
- "Alo" (dramatik anda, ortada telefon yoksa) -> "Allah'ım"
- "Umut ama", "Unutulmuş" -> "Unut onu", "Unut onuymuş"
- "Refne", "Etna Hanım" -> Defne, "Defne Hanım"; "Emin da", "Emin Dağ", "Kadir Emin" -> Emindağ
- "Anamgül" -> "anamgil" (annemler); "barbağı" -> "barbar"
- İsimler: Def/Defter/Medefne -> Defne; Kadeh/Katiş -> Kadir; Dolgu -> Tolga; Levan/Levhat/Elifat -> Levent; Emine/Mina/Müniş/Nina -> Mine; Melisa/Menis -> Melis; Selam/Selvi -> Selim; Selman/Selva -> Selma; Bartner/partner/Atner -> Bartıner; Suzy -> Suzi. "selam", "partner", "kader" normal kelime de olabilir; sadece bağlam isim gerektiriyorsa düzelt.

## Çıktı formatı

Her satır: numara, boşluk, Endonezce metin.
```
0012 Astagfirullah, dia nggak bakal mendekat lagi.
```
- Satır sayısı ve numaralar girdiyle birebir aynı. Birleştirme, bölme, sıra değiştirme YOK. Zamanlar Python'da, dokunulmaz.
- İki satıra bölmek istersen `|` kullan: `0020 Kamu gila, ya?|Ngapain kamu ke sini?` Yoksa kod otomatik böler.
- En fazla 2 ekran satırı; her satır en fazla 42 karakter (kesin üst sınır 46). 42 karakteri geçmeyen tek konuşmacılı metinde `|` koyma.
- `-` (satırı altyazıdan çıkarır: `0031 -`) sadece şunlar için: konuşma olmayan çöp (müzik, "Altyazı M.K."), tek başına anlamsız dolgu sesi ("Ee", "Hı", "Hıh", "Hah", "Hmm"), gülme/ağlama/nefes. Anlamlı ünlemler ("Aha", "Ay", "Of", "Aman") ve tekrar eden kısa sözler ("Ali." beş kez) gerçek konuşmadır: çevir, silme.
- Şarkı sözü (arka planda çalan ya da karakterin söylediği): kısa ve doğal çevir, italik ve nota işaretiyle yaz: `0123 <i>♪ Lirik ♪</i>`; iki satır gerekirse `<i>♪ birinci|ikinci ♪</i>`. Etiketler karakter sınırına sayılmaz. Konuşmayla aynı satıra karışırsa konuşmayı öncele.
- Düz tırnak ve düz tire kullan; süslü Unicode yok.

## Üslup

- Doğal, konuşma dilinde Endonezce. Kitap dili, çeviri kokan cümle yok. Bir Endonezya dizisinin altyazısı gibi okunmalı.
- Günlük diyalogda `aku`, `kamu`, `nggak`, `udah`, `aja`, `banget`, `sih`, `kok`, `dong` uygun. Resmi/saygılı sahnelerde (doktor, müdür, memur, telefonla resmi görüşme) `saya` / `Anda`, `Pak`, `Bu`; zorlama argo kullanma.
- Duyguyu koru: romantizm, öfke, alay, komedi. Sansürleme, yumuşatma, açıklama ekleme.
- Kelimeyi değil işlevi çevir: Türkçe kalıp o sahnede ne iş görüyorsa (teşekkür, sitem, şaşkınlık, yemin, nezaket) Endonezcede o işi gören sözü yaz. Aşağıdaki tablolar bunun için.
- İsimleri çevirme. Sayı, tarih, para değerlerini değiştirme.
- Kısa ve net: altyazı okunacak, ekran süresi kısa.

## İsimler ve kişiler

Defne, Kadir, Tolga, Levent, Levent Bartıner, Mine, Melis, Özlem, Selim, Selma, Sultan, Zeynep, Suzi, Leyla, Kader, Kader Emindağ, Tamer, Yiğit, Zümrüt, Oğuz, Yavuz, Zeliha, Ali, Elif, Güliz, Nihan, Hatice, Çiğdem, Cengiz Taşdağ, Eren Korgül. Okul: Minik Meşeler Koleji. Güvercinler: Huysuz, Boncuk (isim, çevrilmez).

- **Kader Emindağ = Kadir'in ikiz kız kardeşi, Ali'nin annesi.** Tolga'nın eski sevgilisi. "Kader Hanım", "Kader'in çocuğu" gibi yerlerde Kader'i KORU, Kadir'e çevirme. Döküm ikisini karıştırabilir: aranan, kayıp olan, Ali'nin annesi olan kişi Kader'dir. Ali'nin annesi Leyla DEĞİL.
- `Emindağ` tek kelime (asla "Emin Dağ"). `Bartıner` bu şekilde (asla "Bartiner", "Bartınar", "Vartınar").
- Lakaplar aynen kalır: Selo (Selim), Minoş (Mine), Zeyno (Zeynep), Aliş / Aliko (Ali), Maviş (Ali'nin Defne'ye taktığı ad).

## Hitaplar (bölümler arası tutarlı)

| Türkçe | Endonezce |
|---|---|
| Anne / Ana | Ma (yetişkin evladın sevgiyle "anneciğim"i: Mama) |
| Baba | Pa (Özlem'in Levent'e: Papa) |
| Abi / Abla (isimsiz ya da isimle) | Kak (Kak Tolga, Kak Mine) |
| dayı (Ali'nin Kadir'e) | Om |
| teyze (Ali'nin Mine'ye, Zeynep'e) | Tante |
| anneanne | Nenek |
| X Bey / X Hanım | Pak X / Bu X |
| ablacığım, anneciğim (çocuğa sevgi hitabı) | Sayang / Nak |
| koçum, aslanım, paşam, yiğidim (Kadir'in Ali'ye) | Jagoan |
| avukat (Kadir'in Defne'ye) | Pengacara |
| karıcığım (Kadir'in alayla) | Istriku |
| doktor (Kadir'in Tamer'e küçümseyerek) | Dokter |
| prenses (Tamer'in Elif'e) | Tuan Putri |
| kardeşim (Kadir'in Selim'e) | Bro |
| yenge (Selim'in Defne'ye; Defne istemez) | Kakak Ipar |
| ayı / kutup ayısı (Defne'nin Kadir'e) | beruang / beruang kutub |
| "Unut onu" | "Lupakan" |

- Kadir ile Defne birbirine aku / kamu. Tamer ile Defne aku / kamu. Levent ile Mine birbirine resmi: saya / Anda, "Bu Mine", "Pak Levent".
- Ofis ve kurum konuşmaları (Tolga-Nihan, müdür, sosyal hizmet): saya / Anda.

## Yalancı eşdeğerler ve kalıp sözler

Türkçe kalıbın Endonezcede aynı kelimeyle karşılığı çoğu zaman BAŞKA anlama gelir. E16'da bu yüzden hatalar çıktı. İşleve göre seç:

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
