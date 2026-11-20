# 兼容性

## 支持的系统

- Omarchy 4.x（Hyprland 配置为 Lua 格式，Omarchy 自带界面程序：任务栏、菜单、启动器、通知）。旧版 Omarchy（Waybar + `hyprland.conf`）不支持，安装程序会提示先更新。
- Wayland + Hyprland，就是 Omarchy 默认的环境。

Aero7 没有依赖 Waybar：Omarchy 4 已经不用 Waybar，任务栏是 Omarchy 自己的界面程序，Aero7 通过主题的 `shell.toml` 和 `omarchy bar` 命令给它换外观。

## 显卡

| 显卡 | 建议档位 |
|---|---|
| Intel 集成显卡（近几年） | `full` |
| 老 Intel 集成显卡、虚拟机 | `light` 或 `solid` |
| NVIDIA 独立显卡 | `full`；卡顿或闪烁时用 `light` |
| Intel + NVIDIA 混合显卡 | `full`；用电池时可以 `light` |
| 软件渲染（没有显卡加速） | Omarchy 本身会关掉模糊；Aero7 自动只保留颜色 |

模糊是最吃显卡的效果，`light` 把模糊减半、只算一遍，`solid` 完全关掉。三档都只用 Hyprland 自己的合成效果，不另外跑合成器，也没有常驻进程，不占 CPU。

## 高分辨率和多显示器

- 壁纸是 3840×2160，在 1080p、1440p、4K 屏幕上都清楚；`wallpapers/` 里另有 1920×1080 和 2560×1440 版本。
- `aero7 scale` 只改文字大小（用 Omarchy 自带的 `omarchy display text size`），不改显示器缩放。需要整体放大，按 `SUPER + /`。
- 多显示器：任务栏位置和玻璃效果由 Omarchy 统一管理，每个屏幕都一样。

## 测试情况

- 在模拟的 Omarchy 环境里自动测试：安装、三档效果、改设置、Hyprland 报错时自动退回不透明、缩放、重装不覆盖备份、恢复、卸载，共 30 项。
- 生成的 Hyprland 设置逐项对照 Hyprland 源代码里的设置名，三档都没有不存在的设置。
- 主题用 Omarchy 自己的模板程序生成全部 24 个应用配色文件，没有遗漏。
- 所有文字颜色按 WCAG 2.2 计算对比度：正文 13.6:1；玻璃任务栏上的白字在最暗和最亮的壁纸上分别为 11.9:1 和 4.9:1。
- 还没有在真实的 Omarchy 电脑上看过实际画面，欢迎截图反馈。
