"""Dizi otomasyonu (GitHub Actions). Asil sistem Google Drive'da; Colab dosyalarina ve sistem/'e dokunulmaz.

Drive'daki dizi klasorunun sistem/ dosyalari (pipeline.py, elevenlabs.json, youtube_cookies.txt, telegram.json)
servis hesabiyla indirilip yerel bir Drive kopyasina (/tmp/drive) konur; isi Colab'daki ayni pipeline.py yapar.
Bolum ciktilari (video, _iş/SxxEyy, SRT, Yakılı) Colab'daki gibi Drive'a yazilir; Drive'da olan dosyanin ustune yazilmaz.
Bolum teslim edilince sadece yakili video ve scribe_raw.json kalir, gerisi silinir.

  python otomasyon.py kontrol      kurulumu dener: Drive, YouTube cerezi (1 dk indirme), Telegram oturumu
  python otomasyon.py saatler      gecmis bolumlerin YouTube'a yuklenme saatleri
  python otomasyon.py hazirla      yeni bolumu indir, Scribe ile Turkce metin, ceviri girdisini bolumler/'e koy
  python otomasyon.py plan         yakma: video cache'te yoksa indir, parcalari planla
  python otomasyon.py parca <i>    i. parcayi yak (sadece goruntu)
  python otomasyon.py birlestir    parcalari birlestir, sesi ekle, Telegram'a gonder, sonra gecici dosyalari sil
  python otomasyon.py temizlik     bitmis butun bolumlerin gecici dosyalari ve yedekler (Drive cop kutusuna)

Ortam: GDRIVE_SA (servis hesabi anahtari, okuma), GDRIVE_OAUTH (senin hesabin, yazma; yoksa Drive'a yazilmaz), DIZI (muhtemel_ask / yeralti / baskalarinin_hayati), BOLUM (bos = siradaki; ya da 18 / S01E18),
       PARCA (yakma parca sayisi), TELEGRAM (1 = gonder)
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent
MIRROR = Path('/tmp/drive')   # Drive'in yerel kopyasi: pipeline.py burayi Drive sanar
VIDEO_DIR = Path('/tmp/video')
PARTS = Path('/tmp/parcalar')
API = 'https://www.googleapis.com/drive/v3/files'
FOLDER = 'application/vnd.google-apps.folder'
SYSTEM_FILES = ('pipeline.py', 'elevenlabs.json', 'youtube_cookies.txt', 'telegram.json', 'Çeviri Talimatı.md')
NAMES = {'muhtemel_ask': 'Muhtemel Aşk', 'yeralti': 'Yeraltı', 'baskalarinin_hayati': 'Başkalarının Hayatı'}
# Drive'daki pipeline.py'de olmayan diziler (pipeline.py'ye dokunulmaz, ayar buradan eklenir). Bunlarin sistem/
# klasorunde sadece Çeviri Talimatı.md durur; pipeline.py, anahtarlar, cerez ve Telegram Muhtemel Ask'tan alinir.
EXTRA = {'baskalarinin_hayati': dict(
    root='Başkalarının Hayatı', prefix='Baskalarinin.Hayati',
    search='Başkalarının Hayatı {ep}. Bölüm',   # Star TV, cumartesi 20:00 TR; tam bolum resmi YouTube kanalinda
    kanal='Başkalarının Hayatı',
    prompt='Hülya, Neslihan, Erim, Sarp, Fikret, Mediha, Haluk, Jale, Salih, Özkaran, Korhanlı, Sezginel.')}
KEEP = ('ceviri_girdi.txt', 'tr_cues.json', 'kaynak.json')   # repoya giden hazirlik dosyalari (+ talimat.md, rapor.json)
DIZI = os.environ.get('DIZI') or 'muhtemel_ask'
RUN_URL = f"https://github.com/{os.environ.get('GITHUB_REPOSITORY')}/actions/runs/{os.environ.get('GITHUB_RUN_ID')}"


# ---------------------------------------------------------------- Drive

def connect():
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account
    cred = service_account.Credentials.from_service_account_info(
        json.loads(os.environ['GDRIVE_SA']), scopes=['https://www.googleapis.com/auth/drive.readonly'])
    return AuthorizedSession(cred)


def ls(s, folder_id: str) -> dict[str, dict]:
    out, token = {}, None
    while True:
        r = s.get(API, params=dict(q=f"'{folder_id}' in parents and trashed=false", pageSize=1000, pageToken=token,
                                   fields='nextPageToken,files(id,name,mimeType)'))
        r.raise_for_status()
        out.update({f['name']: f for f in r.json().get('files', [])})
        token = r.json().get('nextPageToken')
        if not token:
            return out


def series_root(s, dizi: str = DIZI) -> dict:
    r = s.get(API, params=dict(q=f"sharedWithMe and mimeType='{FOLDER}' and name='{NAMES[dizi]}' and trashed=false",
                               fields='files(id,name)'))
    r.raise_for_status()
    hits = r.json().get('files', [])
    if not hits:
        raise SystemExit(f"'{NAMES[dizi]}' klasoru servis hesabiyla paylasilmamis.")
    return dict(hits[0], kids=ls(s, hits[0]['id']))


def load_pipeline():
    """Drive'daki sistem dosyalarini yerel kopyaya indirir, pipeline.py'yi oradan yukler."""
    s = connect()
    root = series_root(s)
    system = MIRROR / root['name'] / 'sistem'
    system.mkdir(parents=True, exist_ok=True)
    have = ls(s, root['kids']['sistem']['id'])
    if DIZI in EXTRA:
        have = ls(s, series_root(s, 'muhtemel_ask')['kids']['sistem']['id']) | have
    for name in SYSTEM_FILES:
        if name in have:
            r = s.get(f"{API}/{have[name]['id']}", params={'alt': 'media'}, timeout=120)
            r.raise_for_status()
            (system / name).write_bytes(r.content)
    if (system / 'telegram.json').exists():   # repo public: alici numarasi ve hesap bilgisi loglarda gorunmesin
        for v in json.loads((system / 'telegram.json').read_text()).values():
            if str(v).strip():
                print(f'::add-mask::{v}')
    sys.path.insert(0, str(system))
    import pipeline
    pipeline.DRIVE = MIRROR
    if DIZI in EXTRA:
        pipeline.SERIES.setdefault(DIZI, EXTRA[DIZI])
    pipeline.LOCAL = Path('/content/altyazi_tmp')
    return pipeline, s, root


def writer():
    """Drive'a yazan oturum: senin hesabinla, cunku servis hesabinin depolama kotasi yok. GDRIVE_OAUTH yoksa None."""
    if not os.environ.get('GDRIVE_OAUTH'):
        print("GDRIVE_OAUTH yok: Drive'a yazilmayacak.")
        return None
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2.credentials import Credentials
    k = json.loads(os.environ['GDRIVE_OAUTH'])
    return AuthorizedSession(Credentials(None, refresh_token=k['refresh_token'], client_id=k['client_id'],
                                         client_secret=k['client_secret'], token_uri='https://oauth2.googleapis.com/token',
                                         scopes=['https://www.googleapis.com/auth/drive']))


def folder(w, parent: str, name: str) -> str:
    have = ls(w, parent)
    if name in have:
        return have[name]['id']
    r = w.post(API, json=dict(name=name, mimeType=FOLDER, parents=[parent]), params={'fields': 'id'})
    r.raise_for_status()
    return r.json()['id']


def upload(w, parent: str, path: Path, name: str = ''):
    """Dosyayi Drive klasorune yukler (256 MB'lik parcalarla). Ayni adla dosya varsa dokunmaz."""
    name = name or path.name
    if name in ls(w, parent):
        print("Drive'da zaten var, dokunulmadi:", name)
        return
    size = path.stat().st_size
    r = w.post('https://www.googleapis.com/upload/drive/v3/files', params=dict(uploadType='resumable', fields='id'),
               json=dict(name=name, parents=[parent]), headers={'X-Upload-Content-Length': str(size)})
    r.raise_for_status()
    url, pos = r.headers['Location'], 0
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(256 << 20)
            r = w.put(url, data=chunk, headers={'Content-Range': f'bytes {pos}-{pos + len(chunk) - 1}/{size}'},
                      timeout=900)
            if r.status_code != 308:
                break
            pos += len(chunk)
    r.raise_for_status()
    print(f"Drive'a yazildi: {name} ({size / 1e6:.1f} MB)", flush=True)


def season_folder(bolum: str) -> str:
    return f"Sezon {int(bolum[1:3])}"


def output(**kv):
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a', encoding='utf-8') as f:
        for k, v in kv.items():
            f.write(f'{k}={v}\n')


def upload_time(url: str, cookies: list[str]) -> int | None:
    """Videonun YouTube'a yuklendigi an (unix sn)."""
    r = subprocess.run([sys.executable, '-m', 'yt_dlp', '--no-warnings', '--skip-download', '--ignore-no-formats-error',
                        '--no-playlist'] + cookies + ['--print', '%(release_timestamp)s|%(timestamp)s', url],
                       capture_output=True, text=True, timeout=180)
    return next((int(float(x)) for x in r.stdout.strip().split('|') if x.replace('.', '').isdigit()), None)


GUN = ('Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz')


def sgt(ts: float) -> str:
    import datetime as dt
    d = dt.datetime.fromtimestamp(ts, dt.timezone(dt.timedelta(hours=8)))
    return f"{GUN[d.weekday()]} {d:%H:%M} SGT"


def sure(sn: float) -> str:
    m = round(sn / 60)
    return f'{m // 60} sa {m % 60} dk' if m >= 60 else f'{m} dk'


def commit(paths: list[Path], message: str):
    git = ['git', '-C', str(REPO), '-c', 'user.name=github-actions', '-c', 'user.email=github-actions@users.noreply.github.com']
    subprocess.run(git + ['add'] + [str(p) for p in paths], check=True)
    if subprocess.run(git + ['diff', '--cached', '--quiet']).returncode == 0:
        return   # degisiklik yok
    subprocess.run(git + ['commit', '-q', '-m', message], check=True)
    subprocess.run(git + ['pull', '-q', '--rebase'], check=True)
    subprocess.run(git + ['push', '-q'], check=True)


# ---------------------------------------------------------------- kontrol

def kontrol():
    pipeline, _, root = load_pipeline()
    system = MIRROR / root['name'] / 'sistem'
    print('Sistem dosyalari:', {n: (system / n).exists() for n in SYSTEM_FILES})
    c = pipeline.cfg(DIZI)
    cookies = pipeline._cookies(c)
    hit = pipeline.find_source(c, '', '', cookies)
    print('YouTube son bolum:', hit)
    k = pipeline.scribe_credits(DIZI)
    print('Scribe kredisi:', pipeline.credits_text(k) if k else "okunamadi (ElevenLabs anahtarina 'User: Read' izni ver)")
    r = subprocess.run([sys.executable, '-m', 'yt_dlp'] + cookies + [
        '-f', pipeline.YT_FORMAT, '--merge-output-format', 'mp4', '--download-sections', '*0-60',
        '-o', '/tmp/deneme.mp4', hit['url']], capture_output=True, text=True)
    print('YouTube indirme:', 'TAMAM' if os.path.exists('/tmp/deneme.mp4') else 'OLMADI\n' + r.stderr[-1500:])
    tg = json.loads((system / 'telegram.json').read_text())
    import asyncio
    from telethon import TelegramClient
    from telethon.sessions import StringSession

    async def check():
        client = TelegramClient(StringSession(tg.get('oturum', '')), int(tg['api_id']), tg['api_hash'])
        await client.connect()
        try:
            return await client.is_user_authorized()
        finally:
            await client.disconnect()
    print('Telegram oturumu:', 'gecerli' if asyncio.run(check()) else "GECERSIZ (Colab'da bir kez tekrar giris yap)")
    w = writer()
    if w:
        r = w.get(f"{API}/{root['id']}", params={'fields': 'capabilities(canAddChildren)'})
        ok = r.ok and r.json()['capabilities']['canAddChildren']
        print('Drive yazma:', 'hazir' if ok else f'OLMADI ({r.status_code} {r.text[:300]})')


# ---------------------------------------------------------------- hazirla

def hazirla():
    pipeline, s, root = load_pipeline()
    pipeline._whisper = lambda *a, **k: False   # GPU yok: sadece Scribe (Scribe olmazsa is durur)
    c = pipeline.cfg(DIZI)
    # biten bolumler yerel kopyada bos .ind.srt ile isaretlenir; prepare() siradaki bolumu bunlardan bulur
    done = [(name, n) for name, f in root['kids'].items() if name.startswith('Sezon ') and f['mimeType'] == FOLDER
            for n in ls(s, f['id']) if n.endswith('.ind.srt')]
    yakili = root['kids'].get(pipeline.BURN_DIR)   # teslim edilen bolumun SRT'si silinir, yakili video kalir
    for n in (ls(s, yakili['id']) if yakili else {}):
        if m := re.fullmatch(r'(.+\.S(\d+)E\d+)\.ind\.\d+p\.mp4', n):
            done.append((f'Sezon {int(m.group(2))}', f'{m.group(1)}.ind.srt'))
    for d in (REPO / 'bolumler' / DIZI).glob('S*E*'):
        m = re.fullmatch(r'S(\d+)E(\d+)', d.name)
        if m and (d / 'ceviri_girdi.txt').exists():
            done.append((f'Sezon {int(m.group(1))}', pipeline.ep_name(c, int(m.group(1)), int(m.group(2))) + '.ind.srt'))
    for season, name in done:
        (c['root'] / season).mkdir(parents=True, exist_ok=True)
        (c['root'] / season / name).touch()
    w = writer()
    rapor = dict(basladi=time.time(), run=RUN_URL)   # bolum.yml raporu: birlestir sonunda Telegram raporuna girer
    find, log = pipeline.find_source, pipeline.log

    def find_source(c_, episode, url, cookies):
        hit = find(c_, episode, url, cookies)
        rapor.update(bulundu=time.time(), yuklenme=upload_time(hit['url'], cookies))
        return hit

    def log_(*a):
        line = ' '.join(map(str, a))
        if line.startswith('AKIS '):
            rapor['akis'] = line[5:]
        log(*a)
    pipeline.find_source, pipeline.log = find_source, log_
    scribe = pipeline.scribe_words

    def scribe_words(series, video, out):   # Scribe yaniti hemen _iş/SxxEyy'ye: is sonra patlarsa tekrar ucret odenmez
        raw, ep = Path(out).with_name('scribe_raw.json'), Path(out).parent.name
        f = root['kids'].get(pipeline.WORK_DIR)
        d = f and ls(s, f['id']).get(ep)
        have = d and ls(s, d['id']).get('scribe_raw.json')
        rapor['scribe'] = "Drive'daki yanit (ucretsiz)" if have else 'yeni istek'
        if have:
            r = s.get(f"{API}/{have['id']}", params={'alt': 'media'}, timeout=300)
            r.raise_for_status()
            raw.write_bytes(r.content)
        scribe(series, video, out)
        if w and raw.exists():
            upload(w, folder(w, folder(w, root['id'], pipeline.WORK_DIR), ep), raw)
    pipeline.scribe_words = scribe_words
    bolum = os.environ.get('BOLUM', '')
    if not bolum and not c.get('search') and done:   # Yeralti: listedeki en son video degil, siradaki bolum aranir
        se = max(tuple(map(int, re.search(r'S(\d+)E(\d+)', n).groups())) for _, n in done)
        bolum = f'S{se[0]:02d}E{se[1] + 1:02d}'
        print('Aranan bolum:', bolum)
    try:
        r = pipeline.prepare(DIZI, bolum, scribe=True)
    except SystemExit as exc:
        if 'henuz yok' in str(exc):
            print('Yeni bolum yok:', exc)
            return
        raise
    p = pipeline.paths(c, r['season'], r['episode'])
    out = REPO / 'bolumler' / DIZI / p['work'].name
    out.mkdir(parents=True, exist_ok=True)
    for name in KEEP:
        if (p['work'] / name).exists():
            shutil.copyfile(p['work'] / name, out / name)
    shutil.copyfile(MIRROR / root['name'] / 'sistem' / 'Çeviri Talimatı.md', out / 'talimat.md')   # Claude rutini okur
    kredi = p['work'] / 'scribe_kredi.json'
    if kredi.exists():
        k = json.loads(kredi.read_text())
        rapor['kredi'] = f"{pipeline._num(k['harcanan'])} kredi, {pipeline.credits_text(k['sonra'])}"
    rapor.update({k: r.get(k) for k in ('cues', 'asr', 'indirme_sn', 'asr_sn', 'toplam_sn')},
                 video_gb=round(p['video'].stat().st_size / 1e9, 2), bitti=time.time())
    (out / 'rapor.json').write_text(json.dumps(rapor, ensure_ascii=False, indent=1))
    VIDEO_DIR.mkdir(exist_ok=True)
    shutil.move(p['video'], VIDEO_DIR / p['video'].name)
    commit([out], f"{NAMES[DIZI]} {p['work'].name} - hazırlık ({r['cues']} satır, {r.get('asr')})")
    output(anahtar=f"video-{DIZI}-{p['work'].name}")
    if w:   # Colab'daki gibi: video Sezon klasorune, calisma dosyalari _iş/SxxEyy'ye
        upload(w, folder(w, root['id'], season_folder(p['work'].name)), VIDEO_DIR / p['video'].name)
        work = folder(w, folder(w, root['id'], pipeline.WORK_DIR), p['work'].name)
        for f in sorted(p['work'].iterdir()):
            if f.is_file():
                upload(w, work, f)


# ---------------------------------------------------------------- yakma (paralel) ve gonderme

def plan():
    bolum = (os.environ.get('BOLUM') or '').strip().upper()
    work = REPO / 'bolumler' / DIZI / bolum
    m = re.fullmatch(r'S(\d+)E(\d+)', bolum)
    if not m or not (work / 'tr_cues.json').exists():
        raise SystemExit(f'bolumler/{DIZI}/{bolum}/ hazirlanmamis.')
    pipeline, _, _ = load_pipeline()
    name = pipeline.ep_name(pipeline.cfg(DIZI), int(m.group(1)), int(m.group(2)))
    VIDEO_DIR.mkdir(exist_ok=True)
    srt = next(work.glob('*.ind.srt'), None)
    if not srt:   # Claude rutini ceviri.txt koyar; SRT Turkce zamanlarla burada kurulur
        if not (work / 'ceviri.txt').exists():
            raise SystemExit(f'bolumler/{DIZI}/{bolum}/ altinda ceviri.txt ya da .ind.srt yok.')
        srt = VIDEO_DIR / f'{name}.ind.srt'
        r = pipeline.build(str(work / 'tr_cues.json'), str(work / 'ceviri.txt'), str(srt))
        cues = [b.split('\n') for b in srt.read_text(encoding='utf-8').strip().split('\n\n')]
        ms = lambda t: sum(int(x) * k for x, k in zip(re.split('[:,]', t), (3600000, 60000, 1000, 1)))
        span = [tuple(map(ms, c[1].split(' --> '))) for c in cues]
        print('SRT kontrol:', dict(cakisma=sum(a[1] > b[0] for a, b in zip(span, span[1:])),
                                   kisa=sum(e - s < 700 for s, e in span),
                                   uzun_satir=sum(len(l) > 46 for c in cues for l in c[2:]),
                                   uc_satir=sum(len(c) > 4 for c in cues), cok_hizli=len(r['too_fast'])), flush=True)
    video = VIDEO_DIR / f'{name}.mp4'
    if not video.exists():   # cache'te yoksa (hazirlik 7 gunden eski) tekrar indir
        info = json.loads((work / 'kaynak.json').read_text())
        pipeline.youtube_download(info['url'], video, pipeline._cookies(pipeline.cfg(DIZI)))
    src = pipeline.probe(video)
    a, b = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
                           '-of', 'csv=p=0', str(video)], capture_output=True, text=True, check=True).stdout.split('/')
    fps = int(a) / int(b)
    h, mb = pipeline._target('1080p', src)
    n = int(os.environ.get('PARCA') or 12)
    frames = round(src['duration'] * fps)
    p = dict(dizi=DIZI, bolum=bolum, srt=str(srt), video=str(video), name=name, fps=fps,
             frames=frames, per=-(-frames // n), n=n, height=h, src_height=src['height'], mbps=mb,
             style=pipeline.BURN_STYLE, duration=src['duration'])
    print(f"{name}: {src['duration'] / 60:.0f} dk, {fps:.3f} fps, kaynak {src['height']}p {src['codec']} "
          f"-> {h}p {mb} Mbps, {n} parca", flush=True)
    (VIDEO_DIR / 'plan.json').write_text(json.dumps(p))   # videoyla ayni cache'te makinelere gider


def parca(i: int):
    p = json.loads((VIDEO_DIR / 'plan.json').read_text())
    start, count = i * p['per'] / p['fps'], min(p['per'], p['frames'] - i * p['per'])
    if count <= 0:
        return
    PARTS.mkdir(exist_ok=True)
    out = PARTS / f'{i:03d}.mp4'
    shutil.copyfile(REPO / p['srt'], '/tmp/alt.srt')
    mb = p['mbps']
    scale = f"scale=-2:{p['height']}," if p['height'] < p['src_height'] else ''
    # parca 0 sn'den baslar: altyazi zamanlari tutsun diye once gercek zamana kaydirilir, sonra geri alinir
    vf = (f"setpts=PTS+{start:.6f}/TB,{scale}subtitles=/tmp/alt.srt:charenc=UTF-8:force_style='{p['style']}',"
          'setpts=PTS-STARTPTS')
    t0 = time.time()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{start:.6f}', '-i', p['video'], '-frames:v', str(count),
                    '-an', '-vf', vf, '-c:v', 'libx264', '-preset', 'medium', '-b:v', f'{mb}M',
                    '-maxrate', f'{mb * 1.5:.2f}M', '-bufsize', f'{mb * 2:.2f}M', '-r', str(p['fps']), str(out)],
                   check=True)
    print(f'Parca {i}: {count} kare, {time.time() - t0:.0f} sn, {out.stat().st_size / 1e6:.0f} MB', flush=True)


def telegram(pipeline, video: Path, workers: int = 16):
    """pipeline.send_telegram ile ayni is (ayni hesap, ayni alici, 2 GB ustu parcalanir, ayni aciklama), ama dosya
    parcalari 16'sar 16'sar paralel yuklenir: GitHub makinesinden Telegram'a tek tek gonderim cok yavas."""
    import asyncio
    import math
    import random
    from telethon import TelegramClient
    from telethon.sessions import StringSession
    from telethon.tl.functions.contacts import ImportContactsRequest
    from telethon.tl.functions.upload import SaveBigFilePartRequest
    from telethon.tl.types import DocumentAttributeVideo, InputFileBig, InputPhoneContact
    c = pipeline.cfg(DIZI)
    tg = json.loads((c['system'] / 'telegram.json').read_text())
    parts, size = [video], video.stat().st_size
    if size > pipeline.TELEGRAM_MAX:
        n = math.ceil(size / (pipeline.TELEGRAM_MAX - 1e8))
        pdir = Path('/content/parca')
        shutil.rmtree(pdir, ignore_errors=True)
        pdir.mkdir()
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-map', '0', '-c', 'copy', '-f', 'segment',
                        '-segment_time', str(math.ceil(pipeline.probe(video)['duration'] / n)), '-reset_timestamps', '1',
                        str(pdir / f'{video.stem}_%d.mp4')], check=True)
        parts = sorted(pdir.glob('*.mp4'), key=lambda x: int(x.stem.rsplit('_', 1)[1]))
        print(f'{size / 1e9:.2f} GB > 2 GB: {len(parts)} parcaya bolundu.', flush=True)

    async def upload(client, path: Path, caption: str):
        chunk = 512 * 1024
        total, fid, done, t0 = -(-path.stat().st_size // chunk), random.getrandbits(63), [0], time.time()
        sem = asyncio.Semaphore(workers)

        async def one(i):
            async with sem:
                with open(path, 'rb') as f:
                    f.seek(i * chunk)
                    data = f.read(chunk)
                for _ in range(100):   # Premium'suz hesapta Telegram hizi FLOOD_PREMIUM_WAIT_N ile keser: N sn bekle, tekrar
                    try:
                        await client(SaveBigFilePartRequest(fid, i, total, data))
                        break
                    except Exception as exc:
                        m = re.search(r'WAIT_(\d+)', str(exc))
                        if not m:
                            raise
                        await asyncio.sleep(int(m.group(1)) + 1)
                else:
                    raise SystemExit(f'Telegram parca {i}: 100 kez beklendi, gitmedi.')
                done[0] += 1
                if done[0] % max(1, total // 10) == 0:
                    print(f'Telegram {caption}: %{done[0] * 100 // total} '
                          f'({done[0] * chunk / 1e6 / (time.time() - t0):.1f} MB/sn)', flush=True)
        await asyncio.gather(*(one(i) for i in range(total)))
        return InputFileBig(fid, total, path.name)

    async def go():
        client = TelegramClient(StringSession(tg['oturum']), int(tg['api_id']), tg['api_hash'])
        await client.connect()
        if not await client.is_user_authorized():
            raise SystemExit("Telegram oturumu gecersiz: Colab'da '2 - Yak ve Gonder' ile bir kez giris yap.")
        try:
            to = await client.get_entity(tg['hedef'])
        except Exception:
            r = await client(ImportContactsRequest([InputPhoneContact(0, tg['hedef'], 'Dizi', 'Alici')]))
            if not r.users:
                raise SystemExit("Alici bulunamadi: telegram.json'daki 'hedef' numara Telegram'da kayitli mi?")
            to = r.users[0]
        for i, part in enumerate(parts, 1):
            v = pipeline.probe(part)
            caption = video.stem + (f' ({i}/{len(parts)})' if len(parts) > 1 else '')
            f = await upload(client, part, caption)
            await client.send_file(to, f, caption=caption, supports_streaming=True,
                                   attributes=[DocumentAttributeVideo(duration=int(v['duration']), w=v['width'],
                                                                      h=v['height'], supports_streaming=True)])
            sent.append(part)
            print(f'Telegram {caption}: gitti', flush=True)
        await client.disconnect()

    print(f"Telegram'a gonderiliyor: {video.name} ({size / 1e9:.2f} GB)", flush=True)
    t0, sent = time.time(), []
    try:
        asyncio.run(go())
    except Exception as exc:
        if sent:   # bir kismi gitti: tekrar gondermek kopya yaratir
            raise
        print(f'Hizli gonderim olmadi ({exc!r}), Colab yontemiyle gonderiliyor.', flush=True)
        pipeline.send_telegram(c, video)
    print(f'TELEGRAM TAMAM ({(time.time() - t0) / 60:.1f} dk).', flush=True)
    return dict(parca=len(parts), gb=size / 1e9, sn=time.time() - t0)


def birlestir():
    p = json.loads((VIDEO_DIR / 'plan.json').read_text())
    parts = sorted(PARTS.glob('*.mp4'))
    if len(parts) != p['n']:
        raise SystemExit(f"{len(parts)}/{p['n']} parca var, birlestirilmedi.")
    (PARTS / 'liste.txt').write_text(''.join(f"file '{x}'\n" for x in parts))
    out = Path('/content') / f"{p['name']}.ind.{p['height']}p.mp4"
    ses = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name',
                          '-of', 'csv=p=0', p['video']], capture_output=True, text=True).stdout.strip()
    ses = ['-c:a', 'copy'] if ses == 'aac' else ['-c:a', 'aac', '-b:a', '128k']   # YouTube sesi zaten AAC: kayipsiz kopya
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(PARTS / 'liste.txt'),
                    '-i', p['video'], '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', *ses,
                    '-movflags', '+faststart', str(out)], check=True)
    print('Ses:', 'kopyalandi (AAC)' if ses[1] == 'copy' else 'AAC 128k kodlandi', flush=True)
    shutil.rmtree(PARTS)
    o = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries',
                                   'stream=nb_read_packets:format=duration', '-of', 'json', str(out)],
                                  capture_output=True, text=True, check=True).stdout)
    dur, frames = float(o['format']['duration']), int(o['streams'][0]['nb_read_packets'])
    print(f"Birlesti: {out.name} | {dur / 60:.1f} dk (kaynak {p['duration'] / 60:.1f}) | {frames} kare "
          f"(beklenen {p['frames']}) | {out.stat().st_size / 1e9:.2f} GB", flush=True)
    if abs(dur - p['duration']) > 2 or abs(frames - p['frames']) > p['n']:
        raise SystemExit('Birlesen video kaynakla ayni uzunlukta degil, gonderilmedi.')
    pipeline, _, root = load_pipeline()
    tg, w, drive_sn = None, writer(), [None]

    def drive():   # Colab'daki gibi: SRT Sezon klasorune, yakili video Yakılı'ya
        t0 = time.time()
        upload(w, folder(w, root['id'], season_folder(p['bolum'])), REPO / p['srt'])
        upload(w, folder(w, root['id'], pipeline.BURN_DIR), out)
        drive_sn[0] = time.time() - t0
    # Drive Telegram'la ayni anda yuklenir: Telegram patlasa da yakili video Drive'da kalir
    with ThreadPoolExecutor(1) as ex:
        yukleme = ex.submit(drive) if w else None
        if (REPO / 'bolumler' / DIZI / p['bolum'] / 'telegram_yok').exists():   # deneme bolumleri icin
            print('telegram_yok dosyasi var: Telegram atlandi.')
        elif os.environ.get('TELEGRAM') == '1':
            tg = telegram(pipeline, out)
        else:
            print('Telegram kapali: gonderilmedi.')
        if yukleme:
            yukleme.result()
    try:
        rapor(p, out, tg, drive_sn[0])
    except Exception as exc:   # rapor yazilamadi diye is kirmizi olmasin
        print('Rapor yazilamadi:', repr(exc))
    try:
        temizle(p, w, root)
    except Exception as exc:
        print('Temizlik yarim kaldi:', repr(exc))


def temizle(p: dict, w, root: dict):
    """Bolum teslim edildi: gecici her sey silinir. Repoda sadece son bolumun ozet.md'si kalir (sonraki ceviri
    okur), GitHub cache'leri ve 7 gunden eski isler silinir, Drive'da _iş/SxxEyy'den sadece scribe_raw.json kalir
    (bolum tekrar hazirlanirsa Scribe'a tekrar para odenmez)."""
    import datetime as dt
    import requests
    gh = f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/actions"
    h = {'Authorization': f"Bearer {os.environ['GITHUB_TOKEN']}", 'Accept': 'application/vnd.github+json'}
    run = os.environ.get('GITHUB_RUN_ID')
    keys = [f"video-{DIZI}-{p['bolum']}", f'video-{run}'] + [f'parca-{run}-{i}' for i in range(p['n'])]
    n = sum(requests.delete(f'{gh}/caches', headers=h, params={'key': k}, timeout=30).ok for k in keys)
    print(f'GitHub cache: {n} silindi')
    sinir = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7)).strftime('%Y-%m-%d')
    r = requests.get(f'{gh}/runs', headers=h, params={'created': f'<{sinir}', 'status': 'completed', 'per_page': 100},
                     timeout=30)
    eski = r.json().get('workflow_runs', []) if r.ok else []
    n = sum(requests.delete(f"{gh}/runs/{x['id']}", headers=h, timeout=30).ok for x in eski)
    print(f'7 gunden eski is: {n} silindi')
    dizi = REPO / 'bolumler' / DIZI
    sil = [f for f in dizi.rglob('*') if f.is_file() and f != dizi / p['bolum'] / 'ozet.md']
    for f in sil:
        f.unlink()
    if sil:   # [skip ci]: ceviri.txt silinmesi yakmayi tekrar tetiklemesin
        commit([dizi], f"{NAMES[DIZI]} {p['bolum']} - temizlik [skip ci]")
    print(f'Repo: {len(sil)} gecici dosya silindi')
    if w:
        drive_temizle(w, root, p['bolum'])


def drive_temizle(w, root: dict, bolum: str = ''):
    """Yakılı'da videosu olan bolumlerin kaynak mp4'u, SRT'si ve _iş/SxxEyy dosyalari cop kutusuna (Drive 30 gun
    tutar); scribe_raw.json kalir. bolum bos ise butun bolumler, ayrica sistem/ yedekleri ve _eski klasorleri."""
    kids = ls(w, root['id'])
    yakili = ls(w, kids['Yakılı']['id']) if 'Yakılı' in kids else {}
    isler = ls(w, kids['_iş']['id']) if '_iş' in kids else {}
    cop = []
    for name in yakili:
        m = re.fullmatch(r'(.+\.S(\d+)E(\d+))\.ind\.\d+p\.mp4', name)
        tag = m and f'S{m.group(2)}E{m.group(3)}'
        if not m or (bolum and tag != bolum):
            continue
        sezon = kids.get(f'Sezon {int(m.group(2))}')
        have = ls(w, sezon['id']) if sezon else {}
        cop += [have[n] for n in (f'{m.group(1)}.mp4', f'{m.group(1)}.ind.srt') if n in have]
        if tag in isler:
            cop += [x for n, x in ls(w, isler[tag]['id']).items() if n != 'scribe_raw.json']
    if not bolum:
        cop += [x for n, x in ls(w, kids['sistem']['id']).items() if '_yedek_' in n]
        cop += [x for n, x in kids.items() if n.startswith('_eski')]
    ok = [x['name'] for x in cop if w.patch(f"{API}/{x['id']}", json={'trashed': True}, timeout=30).ok]
    print(f'Drive: {len(ok)}/{len(cop)} dosya cop kutusuna:', ', '.join(ok) or '-')


def temizlik():
    """Elle: bu dizinin butun bitmis bolumlerinde drive_temizle."""
    _, _, root = load_pipeline()
    drive_temizle(writer(), root)


def rapor(p: dict, out: Path, tg: dict | None, drive_sn: float | None):
    """Bolumun bastan sona raporu: log'da RAPOR satirlari arasinda ve islemin ozet sayfasinda. Claude thread'e tasir."""
    import datetime as dt
    import requests
    work = REPO / 'bolumler' / DIZI / p['bolum']
    h = json.loads((work / 'rapor.json').read_text()) if (work / 'rapor.json').exists() else {}
    log = subprocess.run(['git', '-C', str(REPO), 'log', '--reverse', '--format=%h|%ct|%s', '--', str(work)],
                         capture_output=True, text=True).stdout.splitlines()
    commits = [c.split('|', 2) for c in log]
    ceviri = next((int(c[1]) for c in commits if ' - çeviri' in c[2] or c[2].startswith('Ceviri')), None)
    r = requests.get(f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}/jobs",
                     headers={'Authorization': f"Bearer {os.environ.get('GITHUB_TOKEN', '')}"}, timeout=30)
    ts = lambda s: dt.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()
    jobs = r.json().get('jobs', []) if r.ok else []
    plan_j = [j for j in jobs if j['name'] == 'plan' and j.get('completed_at')]
    parca_j = [j for j in jobs if j['name'].startswith('parca') and j.get('completed_at')]
    now = time.time()
    L = [f"RAPOR: {p['name']}"]
    if h.get('yuklenme'):
        L.append(f"YouTube'a yuklendi: {sgt(h['yuklenme'])}")
    if h.get('bulundu'):
        L.append(f"Yakalandi: {sgt(h['bulundu'])}" + (f" (yuklemeden {sure(h['bulundu'] - h['yuklenme'])} sonra)" if h.get('yuklenme') else ''))
    if h:
        L.append(f"Hazirlik: indirme {sure(h.get('indirme_sn') or 0)} ({h.get('akis') or '?'}, {h.get('video_gb')} GB), "
                 f"metin {h.get('asr')} {sure(h.get('asr_sn') or 0)} ({h.get('scribe', '?')}"
                 + (f", {h['kredi']}" if h.get('kredi') else '') + f"), {h.get('cues')} satir, toplam {sure(h['bitti'] - h['basladi'])}")
        if ceviri:
            L.append(f"Ceviri: girdi hazir {sgt(h['bitti'])}, ceviri geldi {sgt(ceviri)} ({sure(ceviri - h['bitti'])}, Claude rutini)")
    if plan_j and parca_j:
        L.append(f"Yakma: {p['n']} parca, {p['height']}p {p['mbps']} Mbps; hazirlik {sure(ts(plan_j[0]['completed_at']) - ts(plan_j[0]['started_at']))}, "
                 f"parcalar {sure(max(ts(j['completed_at']) for j in parca_j) - min(ts(j['started_at']) for j in parca_j))}")
    L.append(f"Video: {out.name}, {out.stat().st_size / 1e9:.2f} GB")
    L.append(f"Telegram: {tg['parca']} parca, {sure(tg['sn'])}" if tg else 'Telegram: gonderilmedi')
    if drive_sn is not None:
        L.append(f"Drive: SRT ve yakili video yazildi ({sure(drive_sn)})")
    if h.get('yuklenme'):
        L.append(f"Toplam: YouTube'dan teslime {sure(now - h['yuklenme'])} (bitis {sgt(now)})")
    L.append('Commitler: ' + '; '.join(f'{c[0]} {c[2]}' for c in commits))
    L.append(f"Hazirlik isi: {h.get('run', '?')} | Yakma isi: {RUN_URL}")
    text = '\n'.join(L)
    print('===== RAPOR =====\n' + text + '\n===== RAPOR SONU =====', flush=True)
    with open(os.environ.get('GITHUB_STEP_SUMMARY', '/dev/null'), 'a', encoding='utf-8') as f:
        f.write('\n'.join(f'- {x}' if i else f'### {x}' for i, x in enumerate(L)) + '\n')


# ---------------------------------------------------------------- saatler

def saatler():
    """Gecmis bolumlerin YouTube'a yuklenme saatleri: bolum.yml'deki arama saatlerini buna gore ayarlamak icin."""
    import datetime as dt
    pipeline, _, _ = load_pipeline()
    c = pipeline.cfg(DIZI)
    cookies = pipeline._cookies(c)
    if c.get('search'):
        eps = [dict(ep=n, **h) for n in range(1, 31) if (h := pipeline.youtube_search(c['search'].format(ep=n), n, cookies, c.get('kanal', '')))]
    else:
        eps = pipeline.youtube_list(c, cookies)
    r = subprocess.run([sys.executable, '-m', 'yt_dlp', '--no-warnings', '--skip-download', '--ignore-no-formats-error']
                       + cookies + ['--print', '%(id)s|%(timestamp)s|%(release_timestamp)s|%(live_status)s|%(channel)s']
                       + [e['url'] for e in eps], capture_output=True, text=True)
    info = {line.split('|')[0]: line.split('|')[1:] for line in r.stdout.splitlines() if line.count('|') == 4}
    sgt, tr = dt.timezone(dt.timedelta(hours=8)), dt.timezone(dt.timedelta(hours=3))
    for e in eps:
        ts, rel, live, channel = info.get(e['url'].rsplit('=', 1)[1], ['NA'] * 4)
        t = next((int(float(x)) for x in (rel, ts) if x not in ('NA', 'None', '')), None)
        when = dt.datetime.fromtimestamp(t, dt.timezone.utc) if t else None
        print(f"{e['ep']:>3}. bolum | " + (f"{when.astimezone(tr):%a %d.%m %H:%M} TR | {when.astimezone(sgt):%a %H:%M} SGT"
                                           if when else 'saat yok') + f" | {live} | {channel} | {e['title'][:60]}")
    if r.returncode:
        print(r.stderr[-1500:])


def bekle(dk: int = 100):
    """BOLUM=bekle: bolum YouTube'a dusene kadar ~5 dk'da bir hazirla calistirir (bakmak ~1 dk + 4 dk ara; isin
    120 dk sinirina sigar).
    GitHub cron'u gecikip dustugu icin Claude rutini bunu bolum saatinden once bir kez baslatir."""
    son, out = time.time() + dk * 60, Path(os.environ.get('GITHUB_OUTPUT', '/dev/null'))
    while True:
        r = subprocess.run([sys.executable, __file__, 'hazirla'], env=dict(os.environ, BOLUM=''))
        if r.returncode:   # gercek hata: tekrar denenmez (Scribe'a tekrar para gidebilir)
            sys.exit(r.returncode)
        if out.is_file() and 'anahtar=' in out.read_text():
            return
        if time.time() + 240 > son:
            print(f'{dk} dk beklendi, bolum gelmedi.')
            return
        time.sleep(240)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    steps = dict(kontrol=kontrol, saatler=saatler, hazirla=hazirla, plan=plan, birlestir=birlestir, temizlik=temizlik)
    if cmd == 'hazirla' and os.environ.get('BOLUM', '').strip().lower() == 'bekle':
        bekle()
    elif cmd == 'parca':
        parca(int(sys.argv[2]))
    elif cmd in steps:
        steps[cmd]()
    else:
        print(__doc__)
