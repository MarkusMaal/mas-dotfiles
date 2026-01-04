#!/bin/bash

STATE_FILE="/tmp/eww_last_click"
THRESHOLD=400   # milliseconds
LOCK_FILE="/tmp/eww_double_click.lock"
EXECUTABLE="$*"

exec 9>"$LOCK_FILE"
flock -n 9 || exit 0   # exit if another instance is running

now=$(date +%s%3N)

if [[ -f "$STATE_FILE" ]]; then
    last=$(cat "$STATE_FILE")
    diff=$((now - last))
    if [[ $diff -le $THRESHOLD ]]; then
        rm -f "$STATE_FILE"
        [[ "$EXECUTABLE" == "xdg-open"* ]] && $EXECUTABLE || exec "$EXECUTABLE"
        exit 0
    fi
fi

echo "$now" > "$STATE_FILE"