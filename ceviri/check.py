"""Ceviri parcasi kontrolu: python check.py ceviri_girdi.txt parca.txt BAS SON
Numara eksik/fazla/tekrar ve karakter siniri (girdi [Xs|N], | ve <i> sayilmaz) kontrol eder."""
import re, sys
girdi, f, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
lim = {}
for l in open(girdi, encoding='utf-8'):
    m = re.match(r'(\d{4}) \[([\d.]+)s\|(\d+)\]', l)
    if m: lim[int(m.group(1))] = int(m.group(3))
got, bad = {}, 0
for l in open(f, encoding='utf-8'):
    l = l.rstrip('\n')
    if not l.strip(): continue
    m = re.match(r'(\d{4}) (.+)$', l)
    if not m: print('FORMAT:', l); bad += 1; continue
    n = int(m.group(1))
    if n in got: print('DUP', n); bad += 1
    got[n] = m.group(2)
miss = [n for n in range(a, b + 1) if n not in got]
extra = [n for n in got if not a <= n <= b]
if miss: print('MISSING', miss[:30]); bad += 1
if extra: print('EXTRA', extra[:30]); bad += 1
for n, t in sorted(got.items()):
    if t.strip() == '-': continue
    L = len(re.sub(r'</?i>', '', t).replace('|', ''))   # sarki sozu italik etiketi sayilmaz
    if n in lim and L > lim[n]: print(f'LONG {n:04d} {L}>{lim[n]}: {t}')
print('OK' if not bad else 'ERRORS', len(got), 'lines')
