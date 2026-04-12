#!/usr/bin/env bash
# omarchy-menu-nas.sh
#
# What this does (high level):
# - Reads the upstream Omarchy menu script (the one shipped by Omarchy)
# - Patches it *in memory* to:
#     1) Add a new "Custom" entry to the main menu
#     2) Add routing so selecting Custom opens a new custom submenu
#     3) Inject show_custom_menu() (NAS mounts, VPN toggles, cheatsheets, etc.)
#     4) Wrap shutdown/reboot calls so your shutdown-sound wrapper runs first
# - Writes the patched result to a temp file and executes it
#
# Why this approach is nice:
# - You do NOT modify Omarchy’s upstream script permanently
# - If Omarchy updates the menu, you can re-run this and re-patch on the fly
#
# SECURITY / PUBLISH NOTES:
# - This script contains *no passwords, tokens, or IP addresses*.
# - It DOES reveal some local paths (PIA path, Nautilus, your $HOME layout).
#   That’s generally fine to publish. If you want it more generic, you *can*
#   mention in your blog that those paths may vary per system.

set -euo pipefail

#rm /tmp/omarchy-menu.patched.*

# Upstream Omarchy menu script we will patch.
UPSTREAM="$HOME/.local/share/omarchy/bin/omarchy-menu"

# Temporary file where we write the patched copy of the upstream menu.
PATCHED="$(mktemp /tmp/omarchy-menu.patched.XXXXXX)"

# Desktop notification helper (silent fallback if notify-send isn't installed).
notify() {
  command -v notify-send >/dev/null 2>&1 && notify-send "Omarchy Integratsioon Menu" "$1" || true
}

# Hard fail if upstream menu cannot be read.
if [[ ! -r "$UPSTREAM" ]]; then
  notify "Can't read upstream menu: $UPSTREAM"
  exit 1
fi

# Patch the upstream menu using an embedded Python script.
# Arguments passed to Python:
#   $1 = upstream menu path
#   $2 = output path (PATCHED)
python3 ~/.mas/cust-menu.py $UPSTREAM $PATCHED

# Ensure patched menu script is executable and then run it.
chmod +x "$PATCHED"

# Notify user whether our marker exists (basic success check).
grep -q "OMARCHY_INTEGRATSIOON_PATCH_MARKER" "$PATCHED" || notify "Patch didn’t apply (upstream changed?) — running stock menu."

# Execute patched menu, passing through any args
exec bash "$PATCHED" "$@"
