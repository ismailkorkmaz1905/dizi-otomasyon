"""Cloudflare WARP (ucretsiz) SOCKS5 vekili: GitHub runner'inin datacenter IP'si yerine Cloudflare IP'si ile cikar.
YouTube bu IP'lere bot engeli koymuyor (13 Kas 2026 denemesi: 8 denemenin ~5'i ilk seferde gecti, kalanlar yeni kayitla gecer).
wgcf anonim WARP hesabi acar, wireproxy WireGuard tunelini SOCKS5'e cevirir. Hesap/anahtar sadece /tmp/warp'ta, log'a yazilmaz.

Kullanim: ARGS = warp.baslat(); yt-dlp cmd'ye ARGS eklenir (pipeline'da 'cookies' listesinin yerine gecer).
NOT: yt-dlp --download-sections ffmpeg kullanir ve vekili GORMEZ (googlevideo 403); tam indirmede sorun yok.
"""
import atexit
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

WGCF = 'https://github.com/ViRb3/wgcf/releases/download/v2.2.29/wgcf_2.2.29_linux_amd64'
WIREPROXY = 'https://github.com/pufferffish/wireproxy/releases/download/v1.0.9/wireproxy_linux_amd64.tar.gz'
PORT = 25344
DIR = Path('/tmp/warp')
HESAP = Path('/tmp/warp-hesap')   # actions/cache ile kosular arasi saklanir: her kosuda yeni kayit Cloudflare'de 429 veriyor
PROBE = 'https://www.youtube.com/watch?v=jNQXAC9IBTc'   # kisa, herkese acik; sadece "bot engeli yok mu" sinanir
_state = {'args': None, 'proc': None}


def log(*a):
    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'WARP', *a, flush=True)


def _sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def _kur():
    DIR.mkdir(exist_ok=True)
    if not (DIR / 'wgcf').exists():
        _sh(['curl', '-sSL', '--retry', '4', '-o', str(DIR / 'wgcf'), WGCF], check=True)
        (DIR / 'wgcf').chmod(0o755)
    if not (DIR / 'wireproxy').exists():
        _sh(['curl', '-sSL', '--retry', '4', '-o', str(DIR / 'w.tgz'), WIREPROXY], check=True)
        _sh(['tar', 'xzf', str(DIR / 'w.tgz'), '-C', str(DIR)], check=True)


def yenile():
    """Saklanan hesabi birakir; sonraki baslat() yeni kayitla (yeni Cloudflare IP'si) kurar."""
    _durdur()
    _state['args'] = None
    for f in HESAP.glob('wgcf-*'):
        f.unlink()


def _durdur():
    p = _state.get('proc')
    if p and p.poll() is None:
        p.terminate()
    _state['proc'] = None


def baslat(deneme: int = 0) -> list[str]:
    """WARP vekilini kurar ve YouTube'da bot engeli olmadigini dogrular; yt-dlp icin ['--proxy', ...] doner.
    Her denemede yeni anonim hesap acilir (her kayit baska bir Cloudflare IP'si verir). Olmazsa RuntimeError."""
    if _state['args']:
        return _state['args']
    deneme = deneme or int(os.environ.get('WARP_DENEME') or 8)
    _kur()
    atexit.register(_durdur)
    son = ''
    for n in range(1, deneme + 1):
        _durdur()
        for f in DIR.glob('wgcf-*'):
            f.unlink()
        kayitli = n == 1 and (HESAP / 'wgcf-profile.conf').exists()   # ilk deneme: saklanan hesap; olmazsa yeni kayit
        if kayitli:
            for f in HESAP.glob('wgcf-*'):
                shutil.copyfile(f, DIR / f.name)
            r = subprocess.CompletedProcess([], 0, '', '')
        else:
            r = _sh([str(DIR / 'wgcf'), 'register', '--accept-tos'], cwd=DIR)
            if r.returncode == 0:
                r = _sh([str(DIR / 'wgcf'), 'generate'], cwd=DIR)
            if r.returncode == 0 and (DIR / 'wgcf-profile.conf').exists():
                HESAP.mkdir(exist_ok=True)
                for f in DIR.glob('wgcf-*'):
                    shutil.copyfile(f, HESAP / f.name)
        if r.returncode != 0 or not (DIR / 'wgcf-profile.conf').exists():
            son = 'wgcf: ' + re.sub(r'\s+', ' ', (r.stderr or r.stdout))[-120:]
            log(f'deneme {n}/{deneme}: kayit olmadi ({son}), tekrar')
            time.sleep(20)
            continue
        conf = DIR / 'wgcf-profile.conf'
        conf.write_text(conf.read_text() + f'\n[Socks5]\nBindAddress = 127.0.0.1:{PORT}\n')
        _state['proc'] = subprocess.Popen([str(DIR / 'wireproxy'), '-c', str(conf)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(4)
        args = ['--proxy', f'socks5://127.0.0.1:{PORT}']
        t = _sh(['curl', '-s', '-m', '15', '--socks5-hostname', f'127.0.0.1:{PORT}', 'https://www.cloudflare.com/cdn-cgi/trace'])
        if 'warp=on' not in t.stdout:
            son = 'tunel kurulamadi'
            log(f'deneme {n}/{deneme}: {son}, tekrar')
            continue
        y = _sh([sys.executable, '-m', 'yt_dlp', '--no-warnings', '--no-playlist', '--simulate', '--socket-timeout', '30'] + args + [PROBE], timeout=150)
        bot = 'confirm' in y.stderr and 'bot' in y.stderr
        ag = any(k in y.stderr for k in ('Unable to connect', 'timed out', 'Connection', 'Proxy'))
        if y.returncode == 0 or not (bot or ag):   # "video unavailable" gibi cevaplar da IP'nin engelli olmadigini gosterir
            colo = re.search(r'colo=(\w+)', t.stdout)
            log(f'hazir (deneme {n}, {"saklanan hesap" if kayitli else "yeni hesap"}, cikis {colo.group(1) if colo else "?"}), YouTube bot engeli yok')
            _state['args'] = args
            return args
        son = 'YouTube: ' + ('bot engeli' if bot else re.sub(r'\s+', ' ', y.stderr)[-100:])
        log(f'deneme {n}/{deneme}: {son}, yeni IP ile tekrar')
    _durdur()
    raise RuntimeError('WARP kurulamadi: ' + son)
