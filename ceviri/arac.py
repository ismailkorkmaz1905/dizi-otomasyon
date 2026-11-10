"""Ceviri rutininin dosya isleri. Ana oturum buyuk dosyalari okumaz, bunlari calistirir (token harcamaz).
  python3 arac.py bol <bolumler/dizi/SxxEyy> <is klasoru> [parca basina satir=450]
  python3 arac.py birlestir <is klasoru>
  python3 arac.py uygula <is klasoru> <duzeltme dosyasi>"""
import json, re, shutil, subprocess, sys
from pathlib import Path

BURASI = Path(__file__).resolve().parent
ONCE, SONRA, ARA = 40, 20, 25   # baglam satirlari; parca siniri ideal yerin +-ARA satiri icindeki en uzun sessizlige kayar


def oku(f: Path) -> dict[int, str]:
    return {int(l[:4]): l[5:].rstrip('\n') for l in f.open(encoding='utf-8') if re.match(r'\d{4} ', l)}


def check(d: Path, dosya: str, a: int, b: int) -> bool:
    out = subprocess.run([sys.executable, str(BURASI / 'check.py'), str(d / 'ceviri_girdi.txt'), str(d / dosya), str(a), str(b)],
                         capture_output=True, text=True).stdout.strip()
    print(out)
    return out.splitlines()[-1].startswith('OK') and 'LONG' not in out


def yan_yana(d: Path):
    """Kontrol ajani tek dosya okur: her satirda Turkce girdi => Endonezce ceviri."""
    girdi, cev = oku(d / 'ceviri_girdi.txt'), oku(d / 'ceviri_tum.txt')
    (d / 'yan_yana.txt').write_text(''.join(f'{n:04d} {girdi[n]} => {cev[n]}\n' for n in sorted(girdi)), encoding='utf-8')


def bol(bolum: Path, d: Path, boy: int = 450):
    d.mkdir(parents=True, exist_ok=True)
    for f in ('ceviri_girdi.txt', 'talimat.md'):
        shutil.copyfile(bolum / f, d / f)
    for f in ('check.py', 'arac.py'):
        if BURASI != d.resolve():
            shutil.copyfile(BURASI / f, d / f)
    onceki = sorted(p for p in bolum.parent.glob('S*E*/ozet.md') if p.parent.name < bolum.name)
    if onceki:
        shutil.copyfile(onceki[-1], d / 'onceki_ozet.md')
    satir = (d / 'ceviri_girdi.txt').read_text(encoding='utf-8').splitlines()
    N, n = len(satir), max(1, round(len(satir) / boy))
    cues = json.loads((bolum / 'tr_cues.json').read_text())['cues'] if (bolum / 'tr_cues.json').exists() else []
    son = []
    for k in range(1, n):   # k. parcanin son satiri
        ideal = round(k * N / n)
        aday = range(max(ideal - ARA, (son[-1] if son else 0) + 50), min(ideal + ARA, N - 50) + 1)
        son.append(max(aday, key=lambda j: cues[j]['s'] - cues[j - 1]['e']) if len(cues) == N and aday else ideal)
    parcalar = list(zip([1] + [s + 1 for s in son], son + [N]))
    for k, (a, b) in enumerate(parcalar, 1):
        govde = []
        if a > 1:
            govde += ['=== BAGLAM (cevirme) ==='] + satir[max(0, a - 1 - ONCE):a - 1]
        govde += [f'=== CEVIR: {a:04d}-{b:04d} ==='] + satir[a - 1:b]
        if b < N:
            govde += ['=== BAGLAM (cevirme) ==='] + satir[b:b + SONRA]
        (d / f'girdi_{k}.txt').write_text('\n'.join(govde) + '\n', encoding='utf-8')
    (d / 'parcalar.json').write_text(json.dumps(parcalar))
    print(f'{N} satir, {n} parca:', ' '.join(f'{k}:{a}-{b}' for k, (a, b) in enumerate(parcalar, 1)))
    print('onceki_ozet.md:', 'var' if onceki else 'yok')


def birlestir(d: Path):
    parcalar = json.loads((d / 'parcalar.json').read_text())
    (d / 'ceviri_v1.txt').write_text(''.join((d / f'parca_{k}.txt').read_text(encoding='utf-8').rstrip('\n') + '\n'
                                             for k in range(1, len(parcalar) + 1)), encoding='utf-8')
    if not check(d, 'ceviri_v1.txt', 1, parcalar[-1][1]):
        raise SystemExit('ceviri_v1.txt hatali')
    shutil.copyfile(d / 'ceviri_v1.txt', d / 'ceviri_tum.txt')
    yan_yana(d)


def uygula(d: Path, duzeltme: Path):
    """Duzeltme dosyasinda sadece degisen satirlar olur (NNNN yeni metin). Kontrol gecerse ceviri_tum.txt guncellenir."""
    cev, yeni = oku(d / 'ceviri_tum.txt'), oku(duzeltme)
    if yabanci := sorted(set(yeni) - set(cev)):
        raise SystemExit(f'Olmayan satir numarasi: {yabanci[:20]}')
    degisen = [n for n, t in yeni.items() if t != cev[n]]
    cev.update(yeni)
    (d / 'deneme.txt').write_text(''.join(f'{n:04d} {cev[n]}\n' for n in sorted(cev)), encoding='utf-8')
    if not check(d, 'deneme.txt', 1, max(cev)):
        raise SystemExit('Duzeltme uygulanmadi: yukaridaki satirlari duzeltip tekrar calistir.')
    (d / 'deneme.txt').replace(d / 'ceviri_tum.txt')
    yan_yana(d)
    print(f'DEGISEN {len(degisen)} satir')


if __name__ == '__main__':
    is_, *a = sys.argv[1:]
    if is_ == 'bol':
        bol(Path(a[0]), Path(a[1]), int(a[2]) if len(a) > 2 else 450)
    elif is_ == 'birlestir':
        birlestir(Path(a[0]))
    elif is_ == 'uygula':
        uygula(Path(a[0]), Path(a[1]))
    else:
        raise SystemExit(__doc__)
