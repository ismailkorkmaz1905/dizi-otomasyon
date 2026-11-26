# ChatGPT çeviri deneyi (26 Kasım 2026)

Amaç: GPT-6.2 Sol ve GPT-6.1 Terra'nın Türkçe -> Endonezce altyazı kalitesini Opus ile kıyaslamak. Aynı iki parça, 10 Kasım Opus/Sonnet testinde kullanılanlarla aynı.

| Dosya | İçerik |
|---|---|
| `ma_girdi.txt` | Muhtemel Aşk S01E20, satır 0882-1336 (455 satır) + bağlam |
| `bh_girdi.txt` | Başkalarının Hayatı S01E06, satır 0430-0896 (467 satır) + bağlam |
| `ma_talimat.md`, `bh_talimat.md` | Çeviri kuralları (Drive'daki güncel talimat) |
| `ma_onceki_ozet.md`, `bh_onceki_ozet.md` | Bir önceki bölümün özeti |
| `ma_ceviri_girdi.txt`, `bh_ceviri_girdi.txt` | Bölümün tamamı, sadece `check.py` için |
| `check.py` | Numara ve karakter sınırı kontrolü |

Kollar: `sol_xhigh` (GPT-6.2 Sol, Extra high), `sol_high` (GPT-6.2 Sol, High), `terra_xhigh` (GPT-6.1 Terra, Extra high).
Her kol çıktısını kendi klasörüne yazar: `deney/chatgpt/<kol>/ma.txt`, `bh.txt`, `rapor.md`.

## Codex promptu (KOL yerine kol adını yaz)

```
Repo: ismailkorkmaz1905/dizi-otomasyon. Kol adı: KOL

Türkçe dizi altyazısını Endonezceye çeviriyorsun. Bu bir kalite deneyi: çeviriyi SEN yapacaksın, satır satır, kendi dil bilginle. Çeviri için script, sözlük, kütüphane ya da dış servis KULLANMA; Python sadece check.py'yi çalıştırmak için.

İki iş var, sırayla yap: önce "ma", sonra "bh". Her biri için (X = ma ya da bh):
1. Sırayla ve tamamen oku: deney/chatgpt/X_talimat.md (her kuralına uy), deney/chatgpt/X_onceki_ozet.md, deney/chatgpt/X_girdi.txt. Başka dosya okuma (README.md hariç).
2. X_girdi.txt'de sadece "=== CEVIR: BAS-SON ===" başlığının altındaki satırları çevir. "=== BAGLAM ===" altındakiler sadece bağlam, onları çevirme.
3. Çıktıyı deney/chatgpt/KOL/X.txt dosyasına yaz: her satır "NNNN metin", aralıktaki her numara tam bir kez, sırayla, boş satır yok, başka hiçbir şey yok. Uzun olduğu için 100-150 satırlık bölümler halinde ekleyerek yazabilirsin, ama hiçbir satırı atlama, kısaltma ya da "..." ile geçiştirme.
4. Kontrol: python3 deney/chatgpt/check.py deney/chatgpt/X_ceviri_girdi.txt deney/chatgpt/KOL/X.txt BAS SON
   (ma için BAS SON = 882 1336, bh için 430 896). MISSING, DUP, FORMAT ya da LONG çıkarsa ilgili satırları düzelt ve tekrar çalıştır. "OK" çıkıp LONG kalmayınca bitti.

Sonunda deney/chatgpt/KOL/rapor.md yaz (Türkçe): kullandığın model ve effort, iki işin check sonucu, emin olmadığın en fazla 10 satır (numara + bir cümle), kaba süre, check kaç turda geçti ve hangi hataları düzelttin, takıldığın ya da tekrar denediğin yerler, biliyorsan harcadığın token (bilmiyorsan "bilinmiyor" yaz, tahmin etme).

Sadece deney/chatgpt/KOL/ klasörüne yaz, başka dosyaya dokunma. Bitince tek commit: "Deney KOL: ceviri". Sonra PR aç (ya da branch'i push et).
```
