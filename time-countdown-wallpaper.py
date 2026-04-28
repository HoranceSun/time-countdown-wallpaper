"""
Time Countdown Wallpaper — Python Standalone Version
双屏扩展模式 | 退休倒计时 + 生命倒计时

使用方法：
  pip install screeninfo
  python time-countdown-wallpaper.py

或打包为 exe：
  pip install pyinstaller
  pyinstaller --onefile --noconsole time-countdown-wallpaper.py
"""

import tkinter as tk
import math
import time
from datetime import datetime, timedelta
from threading import Thread, Event

try:
    from screeninfo import get_monitors
    HAS_SCREENINFO = True
except ImportError:
    HAS_SCREENINFO = False

# ═══════════════════════════════════════════════
# Dates
# ═══════════════════════════════════════════════
BIRTH = datetime(1987, 10, 26)
RETIRE = datetime(2050, 10, 26)  # 63岁，延迟退休
DEATH = datetime(2087, 10, 26)   # 100岁目标
TOTAL_LIFE_DAYS = (DEATH - BIRTH).days

# ═══════════════════════════════════════════════
# Colors — Tech Dark Theme
# ═══════════════════════════════════════════════
BG_DEEP = "#080d18"
RETIRE_COLOR = "#64b5f6"
RETIRE_DIM = "#1a6b8a"
LIFE_COLOR = "#fb923c"
LIFE_DIM = "#c2410c"
TEXT_PRIMARY = "#e8ecf1"
TEXT_SECONDARY = "#8899aa"
TEXT_MUTED = "#556677"
BAR_RETIRE = "#1e88e5"
BAR_LIFE = "#f59e0b"


def get_screen_geometry():
    """Get the combined virtual screen geometry for all monitors."""
    if HAS_SCREENINFO:
        monitors = get_monitors()
        if not monitors:
            return 1920, 1080, 0, 0
        # Find bounding box
        x_min = min(m.x for m in monitors)
        y_min = min(m.y for m in monitors)
        x_max = max(m.x + m.width for m in monitors)
        y_max = max(m.y + m.height for m in monitors)
        return x_max - x_min, y_max - y_min, x_min, y_min
    else:
        # Fallback: try tkinter
        root = tk.Tk()
        root.withdraw()
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        root.destroy()
        return w, h, 0, 0


def countdown_parts(ms):
    """Break milliseconds into years/days/hours/minutes/seconds."""
    if ms <= 0:
        return 0, 0, 0, 0, 0, 0
    total_sec = int(ms / 1000)
    s = total_sec % 60
    total_min = total_sec // 60
    m = total_min % 60
    total_hr = total_min // 60
    h = total_hr % 24
    total_days = total_hr // 24
    y = int(total_days / 365.25)
    d = int(total_days - y * 365.25)
    return y, d, h, m, s, total_days


class CountdownWallpaper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Time Countdown Wallpaper")
        self.root.configure(bg=BG_DEEP)

        # Get screen geometry
        w, h, x, y = get_screen_geometry()
        self.w = w
        self.h = h
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # Make it a borderless, always-on-bottom window (wallpaper behavior)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', False)
        self.root.wm_attributes('-transparentcolor', BG_DEEP)  # pseudo-transparency
        try:
            self.root.attributes('-alpha', 1.0)
        except:
            pass

        # Full-screen canvas
        self.canvas = tk.Canvas(
            self.root, width=w, height=h,
            bg=BG_DEEP, highlightthickness=0, bd=0
        )
        self.canvas.pack(fill='both', expand=True)

        # Bind Escape to exit
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.bind('<F11>', self.toggle_fullscreen)

        self.running = True
        self._stop_event = Event()

        self.draw_background()
        self._elements = {}
        self.create_elements()

        # Start update loop
        self.update_loop()

    def draw_background(self):
        """Draw gradient + grid background."""
        w, h = self.w, self.h
        canvas = self.canvas

        # Simple gradient approximation with rectangles
        steps = 40
        for i in range(steps):
            t = i / steps
            # Blend deep blue to slightly lighter
            r = int(8 + t * 7)
            g = int(13 + t * 10)
            b = int(24 + t * 6)
            color = f'#{r:02x}{g:02x}{b:02x}'
            y0 = int(h * i / steps)
            y1 = int(h * (i + 1) / steps) + 1
            canvas.create_rectangle(0, y0, w, y1, fill=color, outline='')

        # Grid lines (very subtle)
        grid_size = 80
        for x in range(0, w, grid_size):
            canvas.create_line(x, 0, x, h, fill='#ffffff05', width=1)
        for y in range(0, h, grid_size):
            canvas.create_line(0, y, w, y, fill='#ffffff05', width=1)

        # Accent gradient ellipses
        cx1 = int(w * 0.2)
        canvas.create_oval(
            cx1-400, h//2-300, cx1+400, h//2+300,
            fill='', outline='#0d47a108', width=2
        )
        cx2 = int(w * 0.8)
        canvas.create_oval(
            cx2-350, h//2-250, cx2+350, h//2+250,
            fill='', outline='#c2410c08', width=2
        )

    def create_elements(self):
        """Create all text elements."""
        w, h = self.w, self.h
        canvas = self.canvas

        # Font sizes scale with screen
        title_size = max(14, int(h * 0.022))
        number_size = max(24, int(h * 0.10))
        label_size = max(10, int(h * 0.015))
        sep_size = max(14, int(h * 0.05))
        secondary_size = max(10, int(h * 0.013))

        pad_x = int(w * 0.05)
        half_w = w // 2
        center_y = int(h * 0.38)
        bar_y = int(h * 0.78)

        # ── Retirement Panel (left half) ──
        rx = half_w // 2
        e = {}

        e['ret_title'] = canvas.create_text(
            rx, center_y - 70, text='退 休 倒 计 时',
            fill=RETIRE_DIM, font=('Microsoft YaHei', title_size, 'bold'),
            anchor='center'
        )
        e['ret_sub'] = canvas.create_text(
            rx, center_y - 40,
            text='2050-10-26 · 63 岁退休',
            fill=TEXT_MUTED, font=('Microsoft YaHei', secondary_size),
            anchor='center'
        )
        # Countdown row
        e['ret_nums'] = canvas.create_text(
            rx, center_y + 30, text='-- : -- : -- : -- : --',
            fill=RETIRE_COLOR, font=('Consolas', number_size, 'bold'),
            anchor='center'
        )
        e['ret_labels'] = canvas.create_text(
            rx, center_y + 30 + number_size // 2 + 15,
            text='年     天     时     分     秒',
            fill=TEXT_SECONDARY, font=('Microsoft YaHei', label_size),
            anchor='center'
        )

        # ── Life Panel (right half) ──
        lx = half_w + half_w // 2
        e['life_title'] = canvas.create_text(
            lx, center_y - 70, text='生 命 倒 计 时',
            fill=LIFE_DIM, font=('Microsoft YaHei', title_size, 'bold'),
            anchor='center'
        )
        e['life_sub'] = canvas.create_text(
            lx, center_y - 40,
            text='2087-10-26 · 100 岁目标',
            fill=TEXT_MUTED, font=('Microsoft YaHei', secondary_size),
            anchor='center'
        )
        e['life_nums'] = canvas.create_text(
            lx, center_y + 30, text='-- : -- : -- : -- : --',
            fill=LIFE_COLOR, font=('Consolas', number_size, 'bold'),
            anchor='center'
        )
        e['life_labels'] = canvas.create_text(
            lx, center_y + 30 + number_size // 2 + 15,
            text='年     天     时     分     秒',
            fill=TEXT_SECONDARY, font=('Microsoft YaHei', label_size),
            anchor='center'
        )

        # ── Progress bars ──
        bar_w = int(w * 0.35)
        bar_h = 8
        bar1_y = bar_y
        bar2_y = bar_y + 35

        # Retirement bar
        e['bar1_label'] = canvas.create_text(
            pad_x, bar1_y + bar_h // 2, text='退休进度',
            fill=TEXT_SECONDARY, font=('Microsoft YaHei', label_size),
            anchor='w'
        )
        e['bar1_bg'] = canvas.create_rectangle(
            pad_x + 100, bar1_y, pad_x + 100 + bar_w, bar1_y + bar_h,
            fill='#ffffff08', outline=''
        )
        e['bar1_fill'] = canvas.create_rectangle(
            pad_x + 100, bar1_y, pad_x + 100, bar1_y + bar_h,
            fill=BAR_RETIRE, outline=''
        )
        e['bar1_pct'] = canvas.create_text(
            pad_x + 120 + bar_w, bar1_y + bar_h // 2,
            text='0%', fill=TEXT_SECONDARY,
            font=('Consolas', label_size), anchor='w'
        )

        # Life bar
        e['bar2_label'] = canvas.create_text(
            pad_x, bar2_y + bar_h // 2, text='生命进度',
            fill=TEXT_SECONDARY, font=('Microsoft YaHei', label_size),
            anchor='w'
        )
        e['bar2_bg'] = canvas.create_rectangle(
            pad_x + 100, bar2_y, pad_x + 100 + bar_w, bar2_y + bar_h,
            fill='#ffffff08', outline=''
        )
        e['bar2_fill'] = canvas.create_rectangle(
            pad_x + 100, bar2_y, pad_x + 100, bar2_y + bar_h,
            fill=BAR_LIFE, outline=''
        )
        e['bar2_pct'] = canvas.create_text(
            pad_x + 120 + bar_w, bar2_y + bar_h // 2,
            text='0%', fill=TEXT_SECONDARY,
            font=('Consolas', label_size), anchor='w'
        )

        # ── Status bar at bottom ──
        status_y = int(h * 0.92)
        status_font = ('Microsoft YaHei', max(9, int(h * 0.012)))
        e['status'] = canvas.create_text(
            w // 2, status_y,
            text='出生 1987-10-26  |  当前年龄 --  |  退休 63 岁  |  目标 100 岁',
            fill=TEXT_MUTED, font=status_font, anchor='center'
        )

        self._elements = e
        self._layout = {
            'bar1_x': pad_x + 100, 'bar_w': bar_w,
            'bar1_y': bar1_y, 'bar2_y': bar2_y, 'bar_h': bar_h,
        }

    def update_loop(self):
        """Update countdowns ~1/sec."""
        if not self.running:
            return

        now = datetime.now()
        e = self._elements
        L = self._layout

        # Retirement countdown
        to_retire = (RETIRE - now).total_seconds() * 1000
        ry, rd, rh, rm, rs, rd_total = countdown_parts(max(0, to_retire))
        retire_str = f'{ry:02d} : {rd:03d} : {rh:02d} : {rm:02d} : {rs:02d}'
        self.canvas.itemconfig(e['ret_nums'], text=retire_str)

        # Life countdown
        to_death = (DEATH - now).total_seconds() * 1000
        ly, ld, lh, lm, ls, ld_total = countdown_parts(max(0, to_death))
        life_str = f'{ly:02d} : {ld:03d} : {lh:02d} : {lm:02d} : {ls:02d}'
        self.canvas.itemconfig(e['life_nums'], text=life_str)

        # Subtitles
        self.canvas.itemconfig(
            e['ret_sub'],
            text=f'2050-10-26 · 63 岁退休 · 剩余 {rd_total:,} 天'
        )
        self.canvas.itemconfig(
            e['life_sub'],
            text=f'2087-10-26 · 100 岁目标 · 剩余 {ld_total:,} 天'
        )

        # Progress bars
        life_lived = (now - BIRTH).total_seconds()
        retire_total = (RETIRE - BIRTH).total_seconds()
        life_total = (DEATH - BIRTH).total_seconds()

        retire_pct = min(100, life_lived / retire_total * 100)
        life_pct = min(100, life_lived / life_total * 100)

        fill1_w = int(L['bar_w'] * retire_pct / 100)
        fill2_w = int(L['bar_w'] * life_pct / 100)

        self.canvas.coords(
            e['bar1_fill'],
            L['bar1_x'], L['bar1_y'],
            L['bar1_x'] + fill1_w, L['bar1_y'] + L['bar_h']
        )
        self.canvas.coords(
            e['bar2_fill'],
            L['bar2_x'], L['bar2_y'],
            L['bar2_x'] + fill2_w, L['bar2_y'] + L['bar_h']
        )
        self.canvas.itemconfig(e['bar1_pct'], text=f'{retire_pct:.1f}%')
        self.canvas.itemconfig(e['bar2_pct'], text=f'{life_pct:.1f}%')

        # Current age
        age_years = (now - BIRTH).total_seconds() / (365.25 * 86400)
        self.canvas.itemconfig(
            e['status'],
            text=f'出生 1987-10-26  |  当前年龄 {age_years:.8f} 岁  |  '
                 f'退休 63 岁 · 倒计时 {rd_total:,} 天  |  '
                 f'目标 100 岁 · 剩余 {ld_total:,} 天'
        )

        self.root.after(1000, self.update_loop)

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode."""
        try:
            self.root.attributes('-fullscreen',
                not self.root.attributes('-fullscreen'))
        except:
            pass

    def run(self):
        """Start the wallpaper."""
        self.root.mainloop()


if __name__ == '__main__':
    app = CountdownWallpaper()
    app.run()
