import tkinter as tk
from datetime import datetime

BG = "#0e1116"
CARD = "#161b22"
FG = "#e6edf3"
SUB = "#9da7b3"
ACCENT = "#2ea043"      # live
MUTED = "#8b949e"       # timetabled
FONT = ("Arial", 16)
FONT_SM = ("Arial", 12)
FONT_MONO = ("DejaVu Sans Mono", 16)

class BusTrackerApp:
    def __init__(self, root, service, url, refresh_ms=30_000):
        self.root = root
        self.service = service
        self.url = url
        self.refresh_ms = refresh_ms

        self.root.geometry("480x320")
        self.root.configure(bg=BG)

        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=10, pady=(10, 6))

        # 🕒 Replace title with current time
        self.clock_lbl = tk.Label(header, text="", fg=FG, bg=BG, font=("Arial", 18, "bold"))
        self.clock_lbl.pack(side="left")

        self.updated_lbl = tk.Label(header, text="Updated —", fg=SUB, bg=BG, font=FONT_SM)
        self.updated_lbl.pack(side="right")

        # Card container
        self.card = tk.Frame(self.root, bg=CARD, bd=0, highlightthickness=0)
        self.card.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Rows holder
        self.rows = tk.Frame(self.card, bg=CARD)
        self.rows.pack(fill="both", expand=True, padx=12, pady=12)

        self.update_clock()
        self.update_times()

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_lbl.config(text=now)
        self.root.after(1000, self.update_clock)

    def set_updated(self):
        self.updated_lbl.config(text=f"Updated {datetime.now().strftime('%H:%M:%S')}")

    def clear_rows(self):
        for w in self.rows.winfo_children():
            w.destroy()

    def add_row(self, left, right, live=False, alt=False):
        row_bg = CARD if not alt else "#1b2230"
        f = tk.Frame(self.rows, bg=row_bg)
        f.pack(fill="x", pady=2)

        left_lbl = tk.Label(f, text=left, fg=FG, bg=row_bg, font=FONT_MONO, anchor="w")
        left_lbl.pack(side="left")

        color = ACCENT if live else MUTED
        right_lbl = tk.Label(f, text=right, fg=color, bg=row_bg, font=FONT_MONO, anchor="e")
        right_lbl.pack(side="right")

    def render(self, times):
        self.clear_rows()
        if not times:
            self.add_row("No data", "", live=False)
            return
        for i, t in enumerate(times[:8]):  # cap rows to fit
            left = f"{t.number:<4} {t.name}"
            right = t.scheduled_time
            self.add_row(left, right, live=(not t.is_timetabled), alt=(i % 2 == 1))

    def update_times(self):
        try:
            times = self.service.get_times(self.url)
            self.render(times)
            self.set_updated()
        except Exception as e:
            self.clear_rows()
            err = tk.Label(self.rows, text=f"Error: {e}", fg="#ff6b6b", bg=CARD, font=FONT)
            err.pack()
        self.root.after(self.refresh_ms, self.update_times)
