#!/usr/bin/env bash
# apt ile paket kurar. Kullanim: bash kur.sh ffmpeg [fonts-liberation ...]
# 23 Ekim 2026: runner'in Azure Ubuntu mirror'i aralikli olarak ~60 KB/sn'ye dusuyor; ffmpeg icin 94 MB ~26 dk
# (22 Ekim'deki 16 dk'lik "takilma" buydu, cikti gizli oldugu icin gorunmuyordu).
# 1. deneme varsayilan mirror'la 3 dk; olmazsa Azure mirror'i cikarilir, 2. deneme ana Ubuntu sunucusundan 10 dk.
set -u
o=(-q -o Acquire::Retries=3 -o Acquire::http::Timeout=30 -o Acquire::https::Timeout=30 -o DPkg::Lock::Timeout=120)
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
    echo "::group::apt deneme $i: install $*"
    timeout "$sure" sudo DEBIAN_FRONTEND=noninteractive apt-get "${o[@]}" install -y "$@"
    r=$?
    echo "::endgroup::"
    [ "$r" = 0 ] && exit 0
  fi
  echo "apt deneme $i basarisiz (kod $r, 124 = $((sure / 60)) dk zaman asimi)"
done
exit 1
