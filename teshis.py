import json, math, struct, subprocess, sys
from pathlib import Path
import otomasyon as o

ad = 'Muhtemel.Ask.S01E22.ind.1080p.mp4'
s = o.connect()
root = o.series_root(s)
f = o.ls(s, o.ls(s, root['id'])['Yakılı']['id'])[ad]
src = Path('/tmp') / ad
with s.get(f"{o.API}/{f['id']}", params={'alt': 'media'}, stream=True, timeout=600) as r:
    r.raise_for_status()
    with open(src, 'wb') as out:
        for c in r.iter_content(8 << 20):
            out.write(c)
print('indi', src.stat().st_size, flush=True)


def kutular(p):
    o_, i, n = [], 0, p.stat().st_size
    with open(p, 'rb') as fh:
        while i < n:
            fh.seek(i)
            sz, t = struct.unpack('>I4s', fh.read(8))
            if sz == 1:
                sz = struct.unpack('>Q', fh.read(8))[0]
            o_.append(f"{t.decode()}@{i}({sz})")
            i += sz or n
    return o_


def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


def incele(p):
    print('=====', p.name, p.stat().st_size, flush=True)
    print('kutular:', kutular(p))
    print(sh('ffprobe', '-v', 'error', '-show_entries', 'format=start_time,duration,bit_rate:stream=index,codec_name,'
             'profile,level,pix_fmt,width,height,r_frame_rate,start_time,duration,nb_frames,has_b_frames', '-of', 'compact', str(p)))
    for st in 'va':
        print(st, sh('ffprobe', '-v', 'error', '-select_streams', st, '-show_entries', 'packet=pts_time,dts_time,flags',
                     '-of', 'csv', '-read_intervals', '%+#5', str(p)))
    print('elst:', [l for l in sh('ffmpeg', '-v', 'trace', '-i', str(p)).splitlines() if 'edit list' in l][:6])
    print('ilk 60 sn decode hatalari:', sh('ffmpeg', '-v', 'error', '-t', '60', '-i', str(p), '-f', 'null', '-')[:2000] or 'yok')


incele(src)
dur = float(sh('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(src)))
n = math.ceil(src.stat().st_size / (1.9e9 - 1e8))
pd = Path('/tmp/eski'); pd.mkdir()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-map', '0', '-c', 'copy', '-f', 'segment',
                '-segment_time', str(math.ceil(dur / n)), '-reset_timestamps', '1', str(pd / 'p_%d.mp4')], check=True)
for p in sorted(pd.glob('*.mp4')):
    incele(p)
