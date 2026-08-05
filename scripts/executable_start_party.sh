#!/bin/bash
pkill -9 -f sysstats.py
sleep 5
killall openrgb
openrgb --startminimized --config ~/.config/OpenRGB/pidu </dev/null >/dev/null 2>/dev/null & disown
sleep 10
pushd /home/$USER/.softweb/sources/steelseries-oled >/dev/null
python3 /home/$USER/.softweb/sources/steelseries-oled/party.py >/dev/null
popd >/dev/null
echo Pidu läks käima!
