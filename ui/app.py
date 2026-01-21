"""
app.py

Main GUI application for Bybit Smart Micro Bot.

Components:
- Dashboard (charts & trend)
- TradePanel (positions & PnL)
- Controls (start/stop, mode, sliders)
- Terminal (logs)
- Analytics (trade analytics)
- Settings (configurable parameters)
- ReplayWindow (backtesting)
"""

import tkinter as tk
from ui.dashboard import Dashboard
from ui.trade_panel import TradePanel
from ui.controls import Controls
from ui.terminal import Terminal
from ui.analytics import Analytics
from ui.settings import Settings
from ui.replay_window import ReplayWindow


class App:
    def __init__(self, master):
        """
        Initialize main application GUI.
        """
        self.master = master
        master.title("Bybit Smart Micro Bot")
        master.geometry("1400x800")
        master.configure(bg="#121212")

        # ── Components ──
        self.dashboard = Dashboard(master)
        self.trade_panel = TradePanel(master)
        self.settings = Settings(master)
        self.controls = Controls(master, start_callback=self.start_bot,
                                 stop_callback=self.stop_bot, mode_callback=self.toggle_mode,
                                 settings=self.settings)
        self.terminal = Terminal(master)
        self.analytics = Analytics(master)
        self.replay_window = None

        # ── Layout ──
        self.dashboard.frame.place(x=10, y=10, width=800, height=400)
        self.trade_panel.master.place(x=820, y=10, width=560, height=400)
        self.controls.master.place(x=10, y=420, width=1370, height=80)
        self.terminal.frame.place(x=10, y=510, width=1370, height=200)
        self.analytics.frame.place(x=10, y=720, width=1370, height=70)

        # ── State ──
        self.running = False
        self.live = False
        self.symbol = "BTC/USDT"
        self.timeframe = "1m"

    # ── Bot Control Methods ──
    def start_bot(self):
        if not self.running:
            self.running = True
            self.terminal.log("[INFO] Bot started")

    def stop_bot(self):
        if self.running:
            self.running = False
            self.terminal.log("[INFO] Bot stopped")

    def toggle_mode(self, mode=None):
        """
        Switch between LEARNING and LIVE modes.
        """
        if mode:
            self.live = (mode.upper() == "LIVE")
        else:
            self.live = not self.live

        self.terminal.log(f"[INFO] Mode switched to {'LIVE' if self.live else 'LEARNING'}")

    # ── Replay Window ──
    def open_replay(self):
        if self.replay_window is None or not tk.Toplevel.winfo_exists(self.replay_window.master):
            self.replay_window = ReplayWindow(self.master)


