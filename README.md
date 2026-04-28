<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-brightgreen.svg" alt="Cross-platform">
  <img src="https://img.shields.io/badge/Type-Wallpaper-orange.svg" alt="Wallpaper">
</p>

<p align="center">
  <i>"时间从来不语，却回答了所有问题。"</i>
</p>

---

## 🕐 时间倒计时壁纸 · Time Countdown Wallpaper

一个让你每天都能**看见时间流逝**的桌面壁纸。

左边是**退休倒计时**——提醒你工作不是全部，自由在等你。
右边是**生命倒计时**——以 100 岁为刻度，看清生命的进度条。

> 不是为了制造焦虑，而是为了**珍惜当下**。

### ✨ 效果预览

```
┌──────────────────────────────────────────────┐
│                                              │
│    退 休 倒 计 时          生 命 倒 计 时    │
│                                              │
│    24 : 158 : 15 : 42 : 37    61 : 072 : 08 : 15 : 51 │
│     年    天   时   分   秒      年    天   时   分   秒  │
│                                              │
│    ████████░░░░░░░░ 52.3%    ██████░░░░░░░░ 38.7%   │
│    退休进度                 生命进度                 │
│                                              │
│  出生 1987-10-26  年龄 38.xxxx 岁  百岁 2087-10-26  │
└──────────────────────────────────────────────┘
```

- 🔵 冷蓝色退休倒计时 — 冷静、期待
- 🟠 暖橙色生命倒计时 — 警示、珍视
- 📊 实时进度条 + 秒级刷新年龄
- 🌌 深空科技感背景 + 扫描线效果

### 🚀 快速开始

#### 方式一：Lively Wallpaper（推荐）

1. 下载 [Lively Wallpaper](https://www.rocksdanister.com/lively/)（免费，Microsoft Store 有）
2. 下载 `index.html`，放到固定位置（如 `D:\wallpapers\`）
3. Lively → 点 `+` → 选择 `index.html`
4. 右键壁纸 → 自定义 → 显示模式选 **「每屏幕独立」**（双屏镜像）

#### 方式二：Python 独立运行

```bash
pip install screeninfo
python time-countdown-wallpaper.py
```
按 `Esc` 退出，`F11` 全屏。

### 🔧 自定义

编辑 `index.html` 顶部日期：

```javascript
var BIRTH  = new Date('1987-10-26T00:00:00+08:00');  // 你的生日
var RETIRE = new Date('2050-10-26T00:00:00+08:00');   // 退休日期
var DEATH  = new Date('2087-10-26T00:00:00+08:00');   // 目标寿命
```

### 📄 License

MIT — 随意使用、修改、分享。

---

<p align="center">
  <sub>⚡ 每一天，都在倒计时。别等了。</sub>
</p>
