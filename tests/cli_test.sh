#!/bin/bash
# Installs Aero7 into a throwaway HOME against stateful stand-ins for the Omarchy
# commands it uses, then checks apply / levels / scale / fallback / restore /
# uninstall. No desktop needed.   bash tests/cli_test.sh
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
export AERO7_ALLOW_ROOT=1 HOME="$T/home" XDG_STATE_HOME="$T/home/.local/state" OMARCHY_PATH="$T/omarchy"
mkdir -p "$HOME" "$T/bin" "$OMARCHY_PATH/default/hypr" "$T/st"
touch "$OMARCHY_PATH/default/hypr/toggles.lua"
fails=0
S="$T/st" # where the stand-ins keep their state

stub() { printf '#!/bin/bash\n%s\n' "$2" >"$T/bin/$1"; chmod +x "$T/bin/$1"; }
stub omarchy-theme-set "mkdir -p \"\$XDG_STATE_HOME/omarchy/current\"; echo \"\$1\" >\"\$XDG_STATE_HOME/omarchy/current/theme.name\"
  rm -rf \"\$XDG_STATE_HOME/omarchy/current/theme\"; [[ -d \$HOME/.config/omarchy/themes/\$1 ]] && cp -r \"\$HOME/.config/omarchy/themes/\$1\" \"\$XDG_STATE_HOME/omarchy/current/theme\"; true"
stub omarchy-bar "f=$S/bar-\$1; if (( \$# == 1 )); then cat \$f; else echo \"\$2\" >\$f; fi"
stub omarchy-display-text-size "f=$S/text; case \${1:-} in '') if [[ -f \$f ]]; then echo \"text size: \$(cat \$f) px\"; else echo 'text size: 12 (default) px'; fi ;; reset) rm -f \$f ;; *) echo \$1 >\$f ;; esac"
stub omarchy-theme-bg-set "ln -sfn \"\$1\" \"\$XDG_STATE_HOME/omarchy/current/background\""
stub hyprctl "case \$1 in configerrors) cat $S/hypr-errors 2>/dev/null ;; version) echo 'Hyprland 0.99 (stub)' ;; esac; true"
stub omarchy-version "echo 4.0.0-test"
stub omarchy-restart-hyprctl "true"
stub omarchy-notification-send "true"
export PATH="$T/bin:$PATH"

ok() { echo "  ok   $1"; }
bad() { echo "  FAIL $1"; fails=$((fails + 1)); }
check() { if eval "$2"; then ok "$1"; else bad "$1"; fi; }
LOOK="$XDG_STATE_HOME/omarchy/toggles/hypr/zz-aero7.lua"
CFG="$HOME/.config/omarchy-aero7/aero7.toml"
lua_ok() { ! command -v luac5.4 >/dev/null || luac5.4 -p "$LOOK"; }

# The desktop before Aero7.
mkdir -p "$XDG_STATE_HOME/omarchy/current" "$T/walls"
echo catppuccin >"$XDG_STATE_HOME/omarchy/current/theme.name"
echo top >"$S/bar-position"; echo none >"$S/bar-background"; echo 14 >"$S/text"
touch "$T/walls/old.png"; ln -s "$T/walls/old.png" "$XDG_STATE_HOME/omarchy/current/background"

echo "install"
bash "$ROOT/scripts/install.sh" --yes >"$T/install.log" 2>&1 || { bad "install exited non-zero"; cat "$T/install.log"; }
A="$HOME/.local/bin/aero7"
check "aero7 linked" "[[ -x $A ]]"
check "theme installed" "[[ -f $HOME/.config/omarchy/themes/aero7/colors.toml && -f $HOME/.config/omarchy/themes/aero7/shell.toml ]]"
check "backup has old theme / bar / text" "[[ \$(cat $XDG_STATE_HOME/omarchy-aero7/backup/theme) == catppuccin && \$(cat $XDG_STATE_HOME/omarchy-aero7/backup/bar-position) == top && \$(cat $XDG_STATE_HOME/omarchy-aero7/backup/text-size) == 14 ]]"
check "theme switched" "[[ \$(cat $XDG_STATE_HOME/omarchy/current/theme.name) == aero7 ]]"
check "taskbar bottom + glassy" "[[ \$(cat $S/bar-position) == bottom && \$(cat $S/bar-background) == glassy ]]"
check "wallpaper set" "[[ \$(readlink $XDG_STATE_HOME/omarchy/current/background) == *1-aero-blue.webp ]]"
check "look file valid Lua" "lua_ok"
check "full: corners 7, blur on, 3 passes" "grep -q 'rounding = 7' $LOOK && grep -q 'enabled = true,' $LOOK && grep -q 'passes = 3' $LOOK"
check "full: terminals 0.86" "grep -q 'opacity = \"0.86 0.81\"' $LOOK"
check "text size untouched (scale keep)" "[[ \$(cat $S/text) == 14 ]]"

echo "levels"
$A level light >/dev/null; check "light: blur 4, 1 pass, 0.94" "grep -q 'size = 4' $LOOK && grep -q 'passes = 1' $LOOK && grep -q '\"0.94 0.89\"' $LOOK && lua_ok"
$A level solid >/dev/null; check "solid: no blur, opaque, bar opaque" "grep -q 'enabled = false,' $LOOK && grep -q '\"1.0 1.0\"' $LOOK && ! grep -q layer_rule $LOOK && [[ \$(cat $S/bar-background) == opaque ]] && lua_ok"
$A level full >/dev/null; check "back to full" "grep -q 'passes = 3' $LOOK && [[ \$(cat $S/bar-background) == glassy ]]"
$A level shiny >/dev/null 2>&1; check "bad level refused" "grep -q 'level = \"full\"' $CFG"

echo "settings file"
sed -i 's/^corner_radius = 7/corner_radius = 12/; s/^position = "bottom"/position = "left"/' "$CFG"
$A apply >/dev/null; check "edited radius and position applied" "grep -q 'rounding = 12' $LOOK && [[ \$(cat $S/bar-position) == left ]]"
sed -i 's/^opacity = 0.86/opacity = 2/' "$CFG"
$A apply >/dev/null 2>&1; check "invalid opacity rejected, look unchanged" "grep -q 'rounding = 12' $LOOK && ! $A validate >/dev/null 2>&1"
sed -i 's/^opacity = 2/opacity = 0.86/; s/^position = "left"/position = "bottom"/' "$CFG"

echo "fallback"
echo "zz-aero7.lua:12: unknown option" >"$S/hypr-errors"
$A apply >/dev/null 2>&1; check "Hyprland error -> solid level" "grep -q 'level = \"solid\"' $CFG && grep -q '\"1.0 1.0\"' $LOOK"
rm -f "$S/hypr-errors"; $A level full >/dev/null

echo "scale"
$A scale 150 >/dev/null; check "150% -> 18px" "[[ \$(cat $S/text) == 18 ]]"
$A scale 200 >/dev/null; check "200% -> 20px (max)" "[[ \$(cat $S/text) == 20 ]]"
$A scale 130 >/dev/null 2>&1; check "130 refused" "[[ \$(cat $S/text) == 20 ]]"
$A scale 100 >/dev/null; check "100% -> default" "[[ ! -f $S/text ]]"

echo "reinstall keeps the first backup"
bash "$ROOT/scripts/install.sh" --yes >/dev/null 2>&1
check "backup still the pre-Aero7 desktop" "[[ \$(cat $XDG_STATE_HOME/omarchy-aero7/backup/theme) == catppuccin && \$(cat $XDG_STATE_HOME/omarchy-aero7/backup/bar-position) == top ]]"

echo "restore"
$A restore >/dev/null
check "theme back" "[[ \$(cat $XDG_STATE_HOME/omarchy/current/theme.name) == catppuccin ]]"
check "bar back" "[[ \$(cat $S/bar-position) == top && \$(cat $S/bar-background) == none ]]"
check "text size back" "[[ \$(cat $S/text) == 14 ]]"
check "wallpaper back" "[[ \$(readlink $XDG_STATE_HOME/omarchy/current/background) == $T/walls/old.png ]]"
check "look file gone" "[[ ! -f $LOOK ]]"

echo "uninstall"
$A apply >/dev/null
echo "my own setting" >"$HOME/.config/omarchy/themes/my-own-note.txt"
bash "$HOME/.local/share/omarchy-aero7/scripts/uninstall.sh" >/dev/null 2>&1
check "theme, config, program removed" "[[ ! -e $HOME/.config/omarchy/themes/aero7 && ! -e $HOME/.config/omarchy-aero7 && ! -e $HOME/.local/share/omarchy-aero7 && ! -e $HOME/.local/bin/aero7 ]]"
check "desktop restored" "[[ \$(cat $XDG_STATE_HOME/omarchy/current/theme.name) == catppuccin && \$(cat $S/bar-position) == top ]]"
check "user's own files kept" "[[ -f $HOME/.config/omarchy/themes/my-own-note.txt ]]"

echo
if ((fails)); then echo "$fails 项失败 failed"; exit 1; fi
echo "全部通过 all passed"
