#!/bin/bash
killall openrgb
openrgb --startminimized </dev/null >/dev/null 2>/dev/null & disown
sleep 10
pushd /home/$USER/.softweb/sources/steelseries-oled/ >/dev/null
python3 /home/$USER/.softweb/sources/steelseries-oled/sysstats.py </dev/null >/dev/null & disown
popd >/dev/null
echo Tavarežiim taastati
