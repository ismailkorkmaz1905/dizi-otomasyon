#!/usr/bin/env bash
# apt ile paket kurar. Kullanim: bash kur.sh ffmpeg [fonts-liberation ...]
# 22 Ekim 2026: apt-get sinirsiz bekledi, cikti gizli oldugu icin is 16 dk sessizce takildi (westus3 runner).
# Simdi her apt cagrisi 3 dk'da kesilir, bir kez daha denenir; cikti logda gorunur.
set -u
o=(-q -o Acquire::Retries=3 -o Acquire::http::Timeout=30 -o Acquire::https::Timeout=30 -o DPkg::Lock::Timeout=120)
for i in 1 2; do
  [ "$i" = 2 ] && sudo dpkg --configure -a   # ilk deneme dpkg ortasinda kesildiyse
  echo "::group::apt deneme $i: update"
  timeout 180 sudo apt-get "${o[@]}" update
  r=$?
  echo "::endgroup::"
  if [ "$r" = 0 ]; then
    echo "::group::apt deneme $i: install $*"
    timeout 180 sudo DEBIAN_FRONTEND=noninteractive apt-get "${o[@]}" install -y "$@"
    r=$?
    echo "::endgroup::"
    [ "$r" = 0 ] && exit 0
  fi
  echo "apt deneme $i basarisiz (kod $r, 124 = 3 dk zaman asimi)"
done
exit 1
