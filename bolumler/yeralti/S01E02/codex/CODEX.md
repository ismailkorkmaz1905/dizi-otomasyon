# Codex ceviri gorevi: Yeralti S01E02

Bu dosyayi okuyan Codex: Turkce dizi altyazisini Endonezceye ceviriyorsun. Ceviriyi SEN yapacaksin, satir satir, kendi dil bilginle. Ceviri icin script, sozluk, kutuphane ya da dis servis KULLANMA; Python sadece check.py icin.

Klasor: `bolumler/yeralti/S01E02/codex`. Butun komutlari repo kokunden calistir.

## 1. Oku
Sirayla ve tamamen: `bolumler/yeralti/S01E02/codex/talimat.md` (her kuralina uy), varsa `bolumler/yeralti/S01E02/codex/onceki_ozet.md`. Baska dosya okuma, sadece asagidaki girdi dosyalari.

## 2. Cevir (parcalari sirayla, birer birer)
- `bolumler/yeralti/S01E02/codex/girdi_1.txt` -> `parca_1.txt`, BAS SON = 1 434
- `bolumler/yeralti/S01E02/codex/girdi_2.txt` -> `parca_2.txt`, BAS SON = 435 860
- `bolumler/yeralti/S01E02/codex/girdi_3.txt` -> `parca_3.txt`, BAS SON = 861 1265
- `bolumler/yeralti/S01E02/codex/girdi_4.txt` -> `parca_4.txt`, BAS SON = 1266 1661
- `bolumler/yeralti/S01E02/codex/girdi_5.txt` -> `parca_5.txt`, BAS SON = 1662 2104

Her parca icin: `girdi_<k>.txt` oku. Sadece `=== CEVIR: BAS-SON ===` altindaki satirlari cevir; `=== BAGLAM ===` altindakiler sadece baglam. Ciktiyi `bolumler/yeralti/S01E02/codex/parca_<k>.txt` dosyasina yaz: her satir `NNNN metin`, araliktaki her numara tam bir kez, sirayla, bos satir yok. 100-150 satirlik bolumler halinde ekleyerek yazabilirsin ama hicbir satiri atlama ya da kisaltma.
Kontrol: `python3 bolumler/yeralti/S01E02/codex/check.py bolumler/yeralti/S01E02/codex/ceviri_girdi.txt bolumler/yeralti/S01E02/codex/parca_<k>.txt BAS SON`. MISSING, DUP, FORMAT ya da LONG cikarsa duzelt ve tekrar calistir; `OK` cikip LONG kalmayinca sonraki parcaya gec.

## 3. Kendi kontrolun (bir tur)
Butun parcalar bitince hepsini Turkce kaynakla yan yana bastan sona bir kez oku. Bak: anlam hatalari, hitap tutarliligi (ayni iki kisi her yerde ayni hitap), isim yazimlari ve talimattaki karistirilan isimler, parca sinirlarinda kopukluk, `(?)` ve `[kelime?]` isaretli satirlar, kitap dili. Sadece gereken satirlari duzelt, sonra her parca icin check'i tekrar calistir.

## 4. Rapor ve push
`bolumler/yeralti/S01E02/codex/codex_rapor.md` yaz (Turkce): model ve effort, her parcanin check sonucu, kontrol turunda degistirdigin satir sayisi, emin olmadigin en fazla 15 satir (numara + bir cumle), bu bolumdeki onemli olaylar ve yeni hitaplar/isimler (5-10 madde), kaba sure.
Sadece `bolumler/yeralti/S01E02/codex/` altina yaz, `ceviri.txt` adinda dosya OLUSTURMA, baska dosyaya dokunma. Tek commit: "Yeralti S01E02 - codex ceviri". `main`'e push et; edemiyorsan branch'e push et.
