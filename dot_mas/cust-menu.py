import sys, re

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, "r", encoding="utf-8").read()

# The label inserted into the Omarchy main menu.
# Note: requires Nerd Font support for the icon glyph to render nicely.
INTEGRATSIOON_LABEL = "󰠱  Integratsioon"

# Wrapper script used to play shutdown sound before power actions.
ACTION = '"$HOME/.config/omarchy/bin/action-with-shutdown-sound.sh"'

# Menu action that lets you pick startup/shutdown sounds.
SOUND_PICKER = '"$HOME/.config/omarchy/bin/change-startup-shutdown-sounds.sh"'

# -----------------------------
# 1) Add Custom to main menu list (just above System)
# -----------------------------
# This regex finds the options text passed to the upstream "menu" call inside
# show_main_menu(). We then splice in CUSTOM_LABEL before "System".
main_menu_pat = r'(show_main_menu\(\)\s*\{\s*\n\s*go_to_menu "\$\(\s*menu "Go" "\s*)([^"]+)("\s*\)\s*"\s*\n\s*\}\s*)'
m = re.search(main_menu_pat, s, re.S)

# If upstream changed and the regex can't find what we expect:
# - write the original unmodified script out
# - exit cleanly (your wrapper will still run, but without custom menu)
if not m:
  open(out_path, "w", encoding="utf-8").write(s)
  sys.exit(0)

options = m.group(2)

# Only insert if Custom is not already present.
if ("Integratsioon" not in options) and (INTEGRATSIOON_LABEL not in options):
  items = options.split("\\n")

  # Defensive cleanup: remove any existing Custom lines to avoid duplicates.
  items = [x for x in items if ("Integratsioon" not in x and x != INTEGRATSIOON_LABEL)]

  # Find the first "System" entry and insert Custom just above it.
  sys_idx = None
  for i, it in enumerate(items):
    if "System" in it:
      sys_idx = i
      break

  # If "System" wasn't found, append Custom at the end.
  if sys_idx is None:
    items.append(INTEGRATSIOON_LABEL)
  else:
    items.insert(sys_idx, INTEGRATSIOON_LABEL)

  options = "\\n".join(items)

# Splice the updated options back into the upstream script text.
s = s[:m.start(2)] + options + s[m.end(2):]

# -----------------------------
# 2) Route in go_to_menu()
# -----------------------------
# Upstream routes menu selections like:
#   *trigger*) show_trigger_menu ;;
# We add:
#   *custom*) show_custom_menu ;;
if "show_integratsioon_menu" not in s:
  if "*trigger*) show_trigger_menu ;;" in s:
    s = s.replace(
      "*trigger*) show_trigger_menu ;;",
      "*trigger*) show_trigger_menu ;;\n  *integratsioon*) show_integratsioon_menu ;;"
    )

# -----------------------------
# 3) Inject show_custom_menu()
# -----------------------------
# We locate "show_trigger_menu() {" and insert our custom menu function right
# after that function ends (after the next "}\n\n").
if "show_integratsioon_menu()" not in s:
  inject_after = "show_trigger_menu() {"
  idx = s.find(inject_after)
  if idx != -1:
    insert_point = s.find("}\n\n", idx)
    if insert_point != -1:
      # This is the actual custom menu definition inserted into upstream.
      # It depends on upstream helper functions:
      # - menu
      # - present_terminal
      # - show_main_menu
      custom_fn = r'''

show_integratsioon_menu() {
  case $(menu "Integratsioon" "  Markuse arvuti juhtpaneel\n  TUI juhtpaneel (eelvaade)\n  Käsurea tööriistad\n󰖺  Käivita MarkuStation\n𝅘𝅥𝅮 Käivita Pidu\n󰍲 Taaskäivita Windowsisse\n💡 Tuled kustu\n💡 Tuled põlema\n🗔 Lae töölauaikoonid uuesti") in

    *"Markuse arvuti juhtpaneel"*)
      exec "$HOME/.mas/Markuse asjad/Markuse arvuti juhtpaneel"
      ;;
      
    *"TUI juhtpaneel (eelvaade)"*)
      present_terminal "$HOME/.mas/Markuse\ asjad/MasCpanel"
      ;;

    *"Käsurea tööriistad"*)
      present_terminal "$HOME/scripts/Tools.sh"
      ;;

    *"Käivita MarkuStation"*)
      exec "$HOME/.mas/Markuse asjad/MarkuStation2"
      ;;
    *"Käivita Pidu"*)
      exec "$HOME/.mas/Markuse asjad/Pidu!"
      ;;
    *"Taaskäivita Windowsisse"*)
      xdg-terminal-exec sudo efibootmgr -o 0000,0002 && sudo reboot now
      ;;
    *"Lae töölauaikoonid uuesti"*)
      eww close desktop; eww close logo; eww open logo; eww open desktop
      ;;
    *"Tuled kustu"*)
      killall openrgb; openrgb --mode direct --color 000000 2>/dev/null >/dev/null & disown
      ;;
    *"Tuled põlema"*)
      killall openrgb; openrgb --startminimized </dev/null 2>/dev/null & disown
      ;;
    *)
      # Anything else returns to the main menu.
      show_main_menu
      ;;
  esac
}
'''
      # Insert our function into upstream script text.
      s = s[:insert_point+3] + custom_fn + s[insert_point+3:]

# -----------------------------
# 4) Wrap Omarchy System menu shutdown/reboot tokens
# -----------------------------
# Omarchy uses tokens like "omarchy-cmd-shutdown" (not always literal commands).
# We replace those tokens so they go through your ACTION wrapper first.
def wrap_token(token: str, replacement: str):
  global s
  # Negative lookbehind tries to avoid double-wrapping.
  pat = rf'(?  s = re.sub(pat, replacement, s)'

wrap_token("omarchy-cmd-shutdown", f"{ACTION} shutdown")
wrap_token("omarchy-cmd-reboot",   f"{ACTION} reboot")

# -----------------------------
# 5) Safety net: wrap any systemctl poweroff/reboot/halt
# -----------------------------
# If upstream ever directly calls systemctl poweroff/reboot/halt,
# we wrap it too: ACTION -- systemctl ...
def wrap_cmd(pattern, repl):
  global s
  s = re.sub(pattern, repl, s, flags=re.M)

wrap_cmd(
  rf'(^|[;&\(\)\n]\s*)(?!{re.escape(ACTION)}\s+--\s+)((?:/usr/bin/)?systemctl\b[^\n;&\)]*\b(?:poweroff|reboot|halt)\b[^\n;&\)]*)',
  rf'\1{ACTION} -- \2'
)

# Marker to confirm patch success (used by the bash wrapper below).
if "OMARCHY_INTEGRATSIOON_PATCH_MARKER" not in s and "show_integratsioon_menu()" in s:
  s += "\n# OMARCHY_INTEGRATSIOON_PATCH_MARKER\n"

# Write patched script out.
open(out_path, "w", encoding="utf-8").write(s)