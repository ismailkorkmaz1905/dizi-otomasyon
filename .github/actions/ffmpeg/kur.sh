#!/usr/bin/env bash
# ffmpeg'i kurar ve PATH'e koyar. Sira: 1) GitHub cache'teki statik ffmpeg (~1 sn), 2) BtbN statik build'i
# github.com'dan (~150 MB, saniyeler), 3) son care apt.
# Neden: apt mirror'lari (Azure, Kasim 2026'dan beri AWS us-east-2.ec2) aralikli olarak paket basina 30-60 sn takiliyor,
# 105 MB'lik ffmpeg 16-33 dk suruyordu (22-23 Ekim: S01E19 ~1 saat kayip; 20 Kasim: S01E22 parca 8 iki denemede
# 13 dk sonra dustu, fail-fast diger 7 parcayi da iptal etti). Statik build mirror'a hic ugramaz.
# 20 Kasim 2026 testi (deneme-ffmpeg.yml): statik 8.1 ile apt 6.1 ayni altyaziyi ciziyor, karisik parcalar birlesiyor.
set -u
d=/tmp/ffmpeg-kur
BTBN=https://github.com/BtbN/FFmpeg-Builds/releases/download
# Sabit surum: yakma ciktisi haftadan haftaya degismesin. BtbN eski autobuild'leri bir sure sonra siler; o zaman
# "latest" 8.1'e duser (cache'e yine sabit anahtarla girer). Surumu degistirince action.yml'deki anahtari da degistir.
URLS=("$BTBN/autobuild-2026-11-19-12-39/ffmpeg-n8.1.3-36-ge22a4510c9-linux64-gpl-8.1.tar.xz"
      "$BTBN/latest/ffmpeg-n8.1-latest-linux64-gpl-8.1.tar.xz")

fontlar() {   # altyazi fontu (runner image'inde zaten var; yoksa kucuk bir apt kurulumu)
  fc-list 2> /dev/null | grep -qi 'Liberation Sans' && return 0
  echo "Liberation Sans yok, apt ile kuruluyor"
  timeout 600 sudo DEBIAN_FRONTEND=noninteractive apt-get -qq -o DPkg::Lock::Timeout=120 install -y fonts-liberation
}
bitti() {
  echo "$d/bin" >> "$GITHUB_PATH"
  "$d/bin/ffmpeg" -hide_banner -version | head -1
  fontlar
  exit 0
}

if "$d/bin/ffmpeg" -version > /dev/null 2>&1; then
  echo "statik ffmpeg cache'ten"
  bitti
fi

mkdir -p "$d/bin"
for u in "${URLS[@]}"; do
  echo "statik ffmpeg indiriliyor: $u"
  if curl -fsSL --retry 3 --connect-timeout 20 --max-time 300 "$u" -o /tmp/ffmpeg.tar.xz \
     && tar -xJf /tmp/ffmpeg.tar.xz -C "$d/bin" --strip-components=2 --wildcards '*/bin/ffmpeg' '*/bin/ffprobe' \
     && "$d/bin/ffmpeg" -version > /dev/null 2>&1; then
    rm -f /tmp/ffmpeg.tar.xz
    echo "yeni=1" >> "$GITHUB_OUTPUT"   # action.yml cache'e koyar
    bitti
  fi
  echo "olmadi: $u"
done
rm -rf "$d" /tmp/ffmpeg.tar.xz

# Son care apt. 1. deneme varsayilan mirror'la 3 dk; olmazsa butun mirror'lar ana Ubuntu sunucusuyla degistirilir, 10 dk.
echo "::warning::statik ffmpeg indirilemedi, apt ile kuruluyor"
o=(-q -o Acquire::Retries=3 -o Acquire::http::Timeout=30 -o Acquire::https::Timeout=30 -o DPkg::Lock::Timeout=120)
for i in 1 2; do
  sure=180
  if [ "$i" = 2 ]; then
    sure=600
    sudo dpkg --configure -a   # ilk deneme dpkg ortasinda kesildiyse
    m=/etc/apt/apt-mirrors.txt
    if [ -f "$m" ]; then
      echo "Mirror listesi ana sunucuyla degistiriliyor. Onceki $m:"; cat "$m"
      printf 'http://archive.ubuntu.com/ubuntu/\tpriority:1\n' | sudo tee "$m" > /dev/null
    fi
    sudo sed -i -E 's#https?://[a-z0-9.-]+\.archive\.ubuntu\.com/ubuntu#http://archive.ubuntu.com/ubuntu#g' \
      /etc/apt/sources.list /etc/apt/sources.list.d/*.sources 2> /dev/null
  fi
  echo "::group::apt deneme $i"
  timeout "$sure" sudo apt-get "${o[@]}" update \
    && timeout "$sure" sudo DEBIAN_FRONTEND=noninteractive apt-get "${o[@]}" install -y ffmpeg fonts-liberation
  r=$?
  echo "::endgroup::"
  [ "$r" = 0 ] && exit 0
  echo "apt deneme $i basarisiz (kod $r, 124 = $((sure / 60)) dk zaman asimi)"
done
exit 1
