# 安装和卸载

## 安装

```bash
curl -fsSL https://raw.githubusercontent.com/Freecode100Year/omarchy-aero7/main/scripts/install.sh | bash
```

或者下载源码后在源码目录里运行 `./scripts/install.sh`（加 `--yes` 跳过确认）。

安装程序按这个顺序做：

1. 检查是不是 Omarchy、有没有 Hyprland，显示两者的版本。
2. 检查 Omarchy 够不够新：需要 `omarchy-bar`、`omarchy-display-text-size`、`omarchy-theme-bg-set` 这几个命令，以及 Lua 格式的 Hyprland 配置。
3. 显示当前的主题、任务栏位置和背景。
4. 列出要修改的地方，等你确认。
5. 下载程序到 `~/.local/share/omarchy-aero7`，命令链接到 `~/.local/bin/aero7`。
6. 备份：当前主题名、任务栏位置和背景、文字大小、壁纸，存到 `~/.local/state/omarchy-aero7/backup/`。以后再装或再应用都不会覆盖这份备份。
7. 把主题复制到 `~/.config/omarchy/themes/aero7`。
8. 检查设置文件。
9. 应用：切换到 aero7 主题，设置壁纸，生成 `~/.local/state/omarchy/toggles/hypr/zz-aero7.lua`（Omarchy 会自动读取这个文件夹），重新载入 Hyprland，把任务栏放到底部、变成玻璃。如果 Hyprland 报告这个文件有错，自动退回不透明档，桌面不会坏。
10. 显示怎么恢复和卸载。

全程用普通用户权限，不用 `sudo`，不覆盖 Omarchy 自己管理的文件，不改 `~/.config/hypr/` 里你自己的文件。

## 恢复

```bash
aero7 restore
```

回到安装前的主题、任务栏位置和背景、文字大小和壁纸，删掉 `zz-aero7.lua`。程序和主题还在，想再用就 `aero7 apply`。

## 卸载

```bash
~/.local/share/omarchy-aero7/scripts/uninstall.sh
```

先恢复，再删掉 Aero7 自己的文件：程序、`~/.config/omarchy/themes/aero7`、`~/.config/omarchy-aero7`、`~/.local/state/omarchy-aero7`、`~/.local/bin/aero7`。你在安装后自己建的其他配置不会被删。

## 其他脚本

| 脚本 | 等于 |
|---|---|
| `scripts/backup.sh` | `aero7 backup`（已经有备份时不覆盖） |
| `scripts/restore.sh` | `aero7 restore` |
| `scripts/validate.sh` | `aero7 validate`：检查设置文件、主题是否安装、Hyprland 有没有报错 |
| `scripts/uninstall.sh` | `aero7 uninstall` |
