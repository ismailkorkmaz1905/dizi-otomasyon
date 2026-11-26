# Yeraltı S01E03 Codex çeviri raporu

Model GPT-6 tabanlı Codex. Çalıştırmanın effort değeri oturumda görünmüyor. Çeviri ve kontrol yaklaşık 12 dakika sürdü.

## Doğrulama

| Dosya | Satır aralığı | Son `check.py` çıktısı | Kontrol turunda değişen satır |
| --- | --- | --- | ---: |
| `parca_1.txt` | 0001–0467 | `OK 467 lines` | 20 |
| `parca_2.txt` | 0468–0942 | `OK 475 lines` | 21 |
| `parca_3.txt` | 0943–1443 | `OK 501 lines` | 27 |
| `parca_4.txt` | 1444–1910 | `OK 467 lines` | 36 |
| **Toplam** | **0001–1910** | **1.910 satır** | **104** |

Dört parça numara, biçim ve karakter sınırı kontrollerinden geçti. İki konuşmacılı altyazılarda her konuşmacının ekran satırı ayrıca ölçüldü.

## Belirsiz replikler

- 0099 numaralı satırda Aslı'nın “Halitciğim” hitabındaki Halit adını kaynakta geçtiği biçimde korudum.
- 0159 numaralı satırda son ibare anlaşılmadığı için Merdan'ın Sultan'a yakınlık belirttiği kısmı aktardım.
- 0288 numaralı satırda bozuk ibareyi, Yavuz'un Paşa'yı yine birinin başından uzaklaştırmak zorunda kalmasına bağladım.
- 0372 numaralı satırda Paşa'nın “Sezar” deyişine verilen tepkiyi, lakabı Efo'nun bulup bulmadığını soran bir replik olarak yorumladım.
- 0665 numaralı satırda “[Han?] [Mutlu?]” dizisinde Mutlu adını korudum.
- 0794 numaralı satırda “Cezayir”i, Bozo'nun yüzleşmede de kullandığı ad olarak korudum.
- 1022 numaralı satırda Pınar'ın telefon kapandıktan sonraki sözünü kendi yaptığına şaşırması olarak yorumladım.
- 1041 numaralı satırda parçalı cümleyi Pınar'ın duruma müdahale ettiği anlamıyla verdim.
- 1169 numaralı satırda bozuk şarkı satırını gözyaşı ve yas imgesine indirgedim.
- 1266 numaralı satırda Gülsüm'ün sözünü dışarıdan biri gibi kendini tanıtmayı reddetmesi olarak yorumladım.
- 1305 numaralı satırda Azize'nin “Gülcihan” deyişini kaynakta duyulduğu biçimde korudum.
- 1358 numaralı satırda kesik cümlede duyulan arşiv ifadesini korudum.
- 1615 numaralı satırda “Alex”i, sahnedeki bağlama dayanarak Haydar Ali'ye “Ali” hitabı olarak yorumladım.
- 1891 numaralı satırda “Ekrem”i, sahne sonunda Bozo'nun birlikte götürüldüğü Efraim'e seslenmesine dayanarak Efraim olarak verdim.
- 1896 numaralı satırda “Osman”ı, ailenin emanet edildiği Paşa'ya hitap olarak yorumladım.

## Olaylar ve hitaplar

- Sezai, İstanbul'da satış ve dağıtım yapmak için Bozo'ya açık çek sunar. Bozo aileye danışır ve “yeraltı”ndan haber bekler. Sezai'ye takılan “Sezar” adı esprili repliklerde, “Cezayir” ise geçtiği yerlerde korunur.
- Hanoğulları, Yaşar'dan kalan işleri oğlu Fikri'ye bırakır ve kan parası yollar. Fikri adamlarına Yavuz'u vurdurur. Yavuz'un koluna kurşun sıyırır.
- Aslı, Paşa ile ilişkisini belgeleyen dosyayla Komisaris Pınar'a iş birliği teklif eder. Pınar, Paşa'nın Fikri'yi bulmasına yardım eder ve jandarmaya onu muhbiri olarak tanıtır. Paşa görüşmeyi kesmek ister. Bozo bu durumla “K9” diyerek alay eder.
- Sultan, Haydar Ali'yle göstermelik evlilik konusunda anlaşır. Ferhat'ı başka bir kadınla basınca Haydar Ali'yi aile sofrasında öper. Ferhat ile konuşmalarında `aku/kamu`, Haydar Ali'ye konukların yanında `Sayang` kullanılır.
- Çiftlikte Ceylan, Bozo'yla evliliğini dürüstlükle açıklar. Melek, Ceylan'ın Haydar Ali'yle geçmişini Bozo'dan sakladığını yüzüne vurur. Melek ayrıca Adnan'dan gizlice kendisine silah vermesini ister.
- Gülsüm, Yıldız'la Sezai'nin saklı evine gider ve kendini Bozkurt'un annesi olarak tanıtır. Sezai'nin kız kardeşleri Bu Azize ve Bu Hülya'yı da yemeğe çağırır. Yıldız, Gülsüm'e `Tante`, Azize'ye bir replikte `Ma Azize` der.
- Aslı, Hande'yle hukuk bürosunda ortak olur. Merdan, Aslı'nın bağlantısının istihbarat olduğunu sezer ve Ferhat'tan Hande'ye yaklaşmasını ister.
- Diğer yeni adlar arasında Bahar, Selim, Zeki, Ahmet, Metin ve Aziz geçer. Selim, Sultan'a `Bu Sultan` ve Ferhat'a `Pak Ferhat` diye hitap eder.
- Yemekte Bozo, Sezai'nin İstanbul'da uyuşturucu satmasına izin vermeyeceğini söyler. Finalde Pınar gözaltı ve arama kararıyla gelir. Bozo aileyi Paşa'ya emanet eder.
