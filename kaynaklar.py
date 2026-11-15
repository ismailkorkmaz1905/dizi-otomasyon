"""YouTube'a bagli olmayan yedek kaynaklar: dizinin kendi kanalinin sitesi (cerez gerekmez).

  Muhtemel Ask         showtv.com.tr  - bolum sayfasinda dogrudan 1080p mp4 (JSON-LD contentUrl)
  Baskalarinin Hayati  startv.com.tr  - HLS (sayfayi Chrome acinca playlist.m3u8 + gecici token gelir)

  python kaynaklar.py test <dizi> <bolum>   bulur, ilk 60 sn'yi indirir (Drive/Scribe yok)
"""
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
MIN_DK = 90   # bundan kisa icerik fragman/klip sayilir
SITELER = {
    'muhtemel_ask': dict(tur='showtv', sayfalar=['https://www.showtv.com.tr/dizi/tanitim/muhtemel-ask/3072'], slug='muhtemel-ask'),
    # Star TV (BH) kapali: site sadece 360p veriyor (13 Kas 2026), kalite kabul edilmedi. Kod duruyor:
    # 'baskalarinin_hayati': dict(tur='startv', slug='baskalarinin-hayati'),
}


def log(*a):
    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'YEDEK', *a, flush=True)


def _get(url: str, timeout: int = 30) -> str | None:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'tr'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode('utf-8', 'replace')
    except Exception as e:
        log('okunamadi', url, str(e)[:120])
        return None


def _sure_dk(iso: str) -> float:
    m = re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso or '')
    return (int(m.group(1) or 0) * 60 + int(m.group(2) or 0) + int(m.group(3) or 0) / 60) if m else 0


def bul(dizi: str, ep: int) -> dict | None:
    """dict(url, title, kaynak, mp4?, dakika) ya da bolum sitede yoksa None."""
    s = SITELER.get(dizi)
    if not s:
        return None
    if s['tur'] == 'startv':
        url = f"https://www.startv.com.tr/dizi/{s['slug']}/bolumler/{ep}-bolum"
        page = _get(url)
        m = page and re.search(r'"duration":"(PT[0-9HMS]+)"', page)
        dk = _sure_dk(m.group(1)) if m else 0
        if dk < MIN_DK:
            return None
        up = re.search(r'"uploadDate":"([^"]+)"', page)
        return dict(url=url, title=f'{ep}. Bolum (Star TV)', kaynak='startv', dakika=round(dk), yuklenme_iso=up and up.group(1))
    link = None   # showtv
    for p in s['sayfalar']:
        page = _get(p) or ''
        m = re.search(rf'/dizi/tum_bolumler/{s["slug"]}-sezon-\d+-bolum-{ep}-izle/\d+', page)
        if m:
            link = 'https://www.showtv.com.tr' + m.group(0)
            break
    if not link:
        return None
    page = _get(link) or ''
    mp4 = re.search(r'"contentUrl":"(https://[^"]+\.mp4)"', page)
    m = re.search(r'"duration":"(PT[0-9HMS]+)"', page)
    dk = _sure_dk(m.group(1)) if m else 0
    if not mp4 or dk < MIN_DK:
        return None
    up = re.search(r'"datePublished":"([^"]+)"', page) or re.search(r'"uploadDate":"([^"]+)"', page)
    return dict(url=link, title=f'{ep}. Bolum (Show TV)', kaynak='showtv', mp4=mp4.group(1), dakika=round(dk), yuklenme_iso=up and up.group(1))


def _m3u8(page_url: str) -> str:
    """Star TV: sayfayi Chrome ile acip oynaticinin istedigi playlist.m3u8'i (tokenli) yakalar."""
    from playwright.sync_api import sync_playwright
    found = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        pg = b.new_page(user_agent=UA)
        pg.on('request', lambda r: found.append(r.url) if 'playlist.m3u8' in r.url else None)
        pg.goto(page_url, wait_until='domcontentloaded', timeout=60000)
        pg.wait_for_timeout(6000)
        for _ in range(45):
            if found:
                break
            try:
                pg.evaluate("document.querySelector('video')&&document.querySelector('video').play()")
            except Exception:
                pass
            pg.wait_for_timeout(1000)
        b.close()
    if not found:
        raise RuntimeError('Star TV: playlist.m3u8 yakalanamadi')
    return found[0]


def indir(info: dict, dest: Path, bolge: str = ''):
    """info = bul() sonucu. bolge: '*0-60' gibi (sadece deneme icin). dest: .mp4"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if info['kaynak'] == 'showtv':
        if bolge:
            sn = int(bolge.split('-')[1])
            subprocess.run(['ffmpeg', '-v', 'error', '-user_agent', UA, '-i', info['mp4'], '-t', str(sn), '-c', 'copy', '-y', str(dest)], check=True)
        else:
            subprocess.run(['curl', '-L', '--fail', '--retry', '8', '--retry-all-errors', '--retry-delay', '10', '-C', '-', '-sS',
                            '-A', UA, '-o', str(dest), info['mp4']], check=True)
        info['akis'] = 'Show TV mp4 1080p'
        return
    m3u8 = _m3u8(info['url'])
    cmd = [sys.executable, '-m', 'yt_dlp', '--no-warnings', '--newline', '--progress-delta', '30', '-f', 'bv*[height<=1080]+ba/b',
           '--merge-output-format', 'mp4', '--user-agent', UA, '-o', str(dest)]
    if bolge:
        cmd += ['--download-sections', bolge]
    subprocess.run(cmd + [m3u8], check=True)
    info['akis'] = 'Star TV HLS 360p'


def ep_numarasi(dest: Path | str) -> int | None:
    m = re.search(r'S\d+E(\d+)', Path(dest).name)
    return int(m.group(1)) if m else None


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        dizi, ep = sys.argv[2], int(sys.argv[3])
        info = bul(dizi, ep)
        print('BUL:', json.dumps(info, ensure_ascii=False))
        if info:
            out = Path('/tmp/yedek_test.mp4')
            out.unlink(missing_ok=True)
            indir(info, out, '*0-60')
            print('INDI:', out.exists() and out.stat().st_size, info.get('akis'))
            subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_name,width,height', '-of', 'compact', str(out)])
