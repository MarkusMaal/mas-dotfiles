#!/bin/bash
killall openrgb
DISPLAY=:1 openrgb --startminimized </dev/null &>/dev/null & disown
([ "$(date +%H)" -ge 9 ] && [ "$(date +%H)" -le 22 ]) && omarchy toggle nightlight || (omarchy toggle nightlight; omarchy toggle nightlight)
