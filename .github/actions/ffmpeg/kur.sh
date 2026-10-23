#!/usr/bin/env bash
# ffmpeg ve fonts-liberation'i kurar. .deb'ler /tmp/apt-deb'de varsa (GitHub cache'inden, ~1 sn) oradan kurulur;
# yoksa apt indirir, indirilenler ayni klasorde kalir ve action.yml onlari cache'e koyar.
# Neden: runner'in Azure Ubuntu mirror'i aralikli olarak ~60 KB/sn'ye dusuyor, 94 MB'lik ffmpeg 16-33 dk suruyordu
# (22-23 Ekim 2026: hazirlik 16 dk takildi; Muhtemel Ask S01E19 yakmasinda 14 makinenin 4'u, ~1 saat kayip).
# apt yolu: 1. deneme varsayilan mirror'la 3 dk; olmazsa Azure mirror'i cikarilir, 2. deneme ana Ubuntu sunucusundan 10 dk.
set -u
p=(ffmpeg fonts-liberation)
d=/tmp/apt-deb
if ls "$d"/*.deb > /dev/null 2>&1; then
  echo "::group::cache'ten kurulum: $(ls "$d"/*.deb | wc -l) paket"
  sudo DEBIAN_FRONTEND=noninteractive dpkg -i "$d"/*.deb
  r=$?
  echo "::endgroup::"
  [ "$r" = 0 ] && command -v ffmpeg > /dev/null && exit 0
  echo "cache'teki paketler kurulamadi (kod $r), apt ile indiriliyor"
  sudo dpkg --configure -a
fi
mkdir -p "$d/partial"
o=(-q -o Dir::Cache::archives="$d" -o Acquire::Retries=3 -o Acquire::http::Timeout=30 -o Acquire::https::Timeout=30
   -o DPkg::Lock::Timeout=120)
for i in 1 2; do
  sure=180
  if [ "$i" = 2 ]; then
    sure=600
    sudo dpkg --configure -a   # ilk deneme dpkg ortasinda kesildiyse
    m=/etc/apt/apt-mirrors.txt
    if [ -f "$m" ]; then
      echo "Azure mirror'i cikariliyor. Onceki $m:"; cat "$m"
      sudo sed -i '/azure\.archive\.ubuntu\.com/d' "$m"
      grep -q . "$m" || echo "http://archive.ubuntu.com/ubuntu/" | sudo tee "$m" > /dev/null
    fi
    sudo sed -i 's#http://azure\.archive\.ubuntu\.com/ubuntu#http://archive.ubuntu.com/ubuntu#g' \
      /etc/apt/sources.list /etc/apt/sources.list.d/*.sources 2> /dev/null
  fi
  echo "::group::apt deneme $i: update"
  timeout "$sure" sudo apt-get "${o[@]}" update
  r=$?
  echo "::endgroup::"
  if [ "$r" = 0 ]; then
    echo "::group::apt deneme $i: install ${p[*]}"
    timeout "$sure" sudo DEBIAN_FRONTEND=noninteractive apt-get "${o[@]}" install -y "${p[@]}"
    r=$?
    echo "::endgroup::"
    if [ "$r" = 0 ]; then
      sudo rm -rf "$d/partial" "$d/lock"; sudo chown -R "$(id -u):$(id -g)" "$d"   # cache'e koyabilmek icin
      echo "cache'e girecek: $(ls "$d"/*.deb 2> /dev/null | wc -l) paket, $(du -sh "$d" | cut -f1)"
      exit 0
    fi
  fi
  echo "apt deneme $i basarisiz (kod $r, 124 = $((sure / 60)) dk zaman asimi)"
done
exit 1
