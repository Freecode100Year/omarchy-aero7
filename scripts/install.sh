#!/bin/bash
# Omarchy Aero7 installer · 安装
#
#   curl -fsSL https://raw.githubusercontent.com/Freecode100Year/omarchy-aero7/main/scripts/install.sh | bash
#   (GitLab: https://gitlab.com/sj9292008133/omarchy-aero7/-/raw/main/scripts/install.sh)
#   or from a checkout: ./scripts/install.sh [--yes]
#
# Runs as your normal user (no sudo), never overwrites files Omarchy manages, and
# backs up everything it changes first. Undo with: aero7 restore, or uninstall.sh.
set -euo pipefail

REPO_GITHUB="https://github.com/Freecode100Year/omarchy-aero7.git"
REPO_GITLAB="https://gitlab.com/sj9292008133/omarchy-aero7.git"
APP_DIR="$HOME/.local/share/omarchy-aero7"
THEMES_DIR="$HOME/.config/omarchy/themes"
YES=false
[[ ${1:-} == "--yes" || ${1:-} == "-y" ]] && YES=true

say() { printf '\e[34m==>\e[0m %s\n' "$*"; }
fail() { printf '\e[31m错误 Error:\e[0m %s\n' "$*" >&2; exit 1; }

# 1-4: what is this machine, and does it have what Aero7 builds on?
[[ ${AERO7_ALLOW_ROOT:-} == 1 ]] || ((EUID != 0)) || fail "请用普通用户运行，不要用 sudo · run as your normal user, not root"
command -v omarchy-theme-set >/dev/null || fail "这台电脑不是 Omarchy · this is not Omarchy (no omarchy-theme-set)"
command -v hyprctl >/dev/null || fail "没有找到 Hyprland · Hyprland not found"
command -v git >/dev/null || fail "需要 git · git is required"
omarchy_version="$(omarchy-version 2>/dev/null || cat "${OMARCHY_PATH:-/usr/share/omarchy}/version" 2>/dev/null || echo unknown)"
hypr_version="$(hyprctl version 2>/dev/null | head -1 || echo unknown)"
say "Omarchy $omarchy_version · $hypr_version"
for cmd in omarchy-bar omarchy-display-text-size omarchy-theme-bg-set; do
  command -v "$cmd" >/dev/null || fail "这个 Omarchy 版本太旧（没有 $cmd），请先更新 Omarchy · please update Omarchy"
done
[[ -f ${OMARCHY_PATH:-/usr/share/omarchy}/default/hypr/toggles.lua ]] ||
  fail "这个 Omarchy 版本的配置格式不支持（需要 Lua 格式的 Hyprland 配置）· needs Omarchy with Lua Hyprland config"
say "任务栏 bar: $(omarchy-bar position 2>/dev/null)，背景 background: $(omarchy-bar background 2>/dev/null)，当前主题 theme: $(cat "$HOME/.local/state/omarchy/current/theme.name" 2>/dev/null)"

# 5: show what will change, and ask.
cat <<EOF

  将要修改 · Aero7 will:
    + 安装程序      $APP_DIR
    + 安装主题      $THEMES_DIR/aero7
    + 安装图标套装  ~/.config/omarchy/icons/aero7（89 个 Aero 玻璃风格应用图标）
    + 设置文件      ~/.config/omarchy-aero7/aero7.toml
    + 窗口外观      ~/.local/state/omarchy/toggles/hypr/zz-aero7.lua
    ~ 切换主题到 aero7，任务栏移到底部并变成玻璃（用 Omarchy 自带命令）
    · 不改快捷键、不改 ~/.config/hypr 里你的文件、不装系统软件、不用 sudo
    · 先备份当前主题、图标套装、任务栏和文字大小；随时可以 aero7 restore 恢复

EOF
if ! $YES; then
  if [[ -r /dev/tty ]]; then
    read -r -p "  继续安装吗？Continue? [Y/n] " answer </dev/tty
    [[ -z $answer || $answer =~ ^[Yy] ]] || { echo "已取消 cancelled"; exit 0; }
  fi
fi

# Fetch: the checkout this script sits in, or GitHub (GitLab as fallback).
src="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." 2>/dev/null && pwd || true)"
if [[ -n $src && -f $src/bin/aero7 && $src != "$APP_DIR" ]]; then
  say "从本地目录安装 Installing from $src"
  mkdir -p "$APP_DIR"
  cp -a "$src/." "$APP_DIR/"
elif [[ -d $APP_DIR/.git ]]; then
  say "更新 Updating $APP_DIR"
  git -C "$APP_DIR" pull -q --ff-only
else
  say "下载 Downloading"
  rm -rf "$APP_DIR"
  git clone -q --depth 1 "$REPO_GITHUB" "$APP_DIR" 2>/dev/null || git clone -q --depth 1 "$REPO_GITLAB" "$APP_DIR"
fi
chmod +x "$APP_DIR/bin/aero7" "$APP_DIR"/scripts/*.sh
mkdir -p "$HOME/.local/bin"
ln -sfn "$APP_DIR/bin/aero7" "$HOME/.local/bin/aero7"

# 6: back up before touching anything.
"$APP_DIR/bin/aero7" backup

# 7: only theme files — a theme directory of our own.
say "安装主题和图标 Installing the aero7 theme and icon set"
mkdir -p "$THEMES_DIR" "$HOME/.config/omarchy/icons"
rm -rf "${THEMES_DIR:?}/aero7" "$HOME/.config/omarchy/icons/aero7"
cp -r "$APP_DIR/theme/aero7" "$THEMES_DIR/aero7"
cp -r "$APP_DIR/icons/aero7" "$HOME/.config/omarchy/icons/aero7"

# 8-9: check the settings, then apply (apply falls back to the solid level by itself
# if Hyprland rejects the glass settings).
"$APP_DIR/bin/aero7" apply
"$APP_DIR/bin/aero7" validate || true

# 10: how to undo.
cat <<'EOF'

  安装完成 · Installed

  aero7 level light     显卡吃力时换轻玻璃（solid = 不透明）
  aero7 scale 125       界面文字放大到 125%（100 / 125 / 150 / 175 / 200）
  aero7 edit            打开设置文件，改完运行 aero7 apply

  恢复原样 Undo:   aero7 restore
  完全卸载 Remove: ~/.local/share/omarchy-aero7/scripts/uninstall.sh
EOF
