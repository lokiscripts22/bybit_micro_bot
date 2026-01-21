"""
replay_window.py

A Tkinter-based window for replaying historical trade data (CSV) for backtesting.

Features:
- Load CSV files containing historical prices
- Adjustable replay speed
- Real-time plotting of price data with Matplotlib
- Callback support for simulating trades
"""

import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from threading import Thread
import time


class ReplayWindow:
    def __init__(self, master, trade_callback=None):
        """
        Initialize the Replay/Backtesting window.

        Args:
            master: Parent Tkinter window
            trade_callback: Optional function(bot_state_dict) called on each simulated trade
        """
        self.master = tk.Toplevel(master)
        self.master.title("Replay / Backtesting")
        self.master.geometry("900x600")
        self.master.configure(bg="#121212")

        self.trade_callback = trade_callback
        self.running = False
        self.speed_var = tk.DoubleVar(value=1.0)  # seconds per candle

        self.df = pd.DataFrame()
        self.index = 0

        # ── Load CSV Button ──
        self.load_btn = tk.Button(
            self.master, text="📂 Load CSV", fg="white", bg="#333333",
            command=self.load_csv
        )
        self.load_btn.pack(pady=5)

        # ── Speed Slider ──
        tk.Label(self.master, text="Replay Speed (sec/candle)", fg="white", bg="#121212").pack()
        self.speed_slider = tk.Scale(
            self.master, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL,
            variable=self.speed_var, length=300, bg="#121212", fg="white", troughcolor="#333333"
        )
        self.speed_slider.pack()

        # ── Control Buttons ──
        control_frame = tk.Frame(self.master, bg="#121212")
        control_frame.pack(pady=5)
        tk.Button(control_frame, text="▶ Start Replay", fg="white", bg="#333333", command=self.start).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="⏹ Stop Replay", fg="white", bg="#333333", command=self.stop).grid(row=0, column=1, padx=5)

        # ── Matplotlib Figure ──
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_facecolor("#121212")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ── CSV Handling ──
    def load_csv(self):
        """Prompt user to load a CSV file and initialize the DataFrame."""
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            self.df = pd.read_csv(path)
            if "timestamp" in self.df.columns:
                self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
            else:
                self.df["timestamp"] = pd.RangeIndex(len(self.df))
            self.index = 0
            self.plot_current()
        except Exception as e:
            print(f"[ERROR] Failed to load CSV: {e}")

    # ── Replay Control ──
    def start(self):
        """Start the replay loop in a separate thread."""
        if self.df.empty:
            print("[ERROR] No CSV loaded")
            return
        if self.running:
            return
        self.running = True
        Thread(target=self.run, daemon=True).start()

    def stop(self):
        """Stop the replay loop."""
        self.running = False

    def run(self):
        """Replay loop that updates the chart and calls trade_callback."""
        while self.running and self.index < len(self.df):
            self.plot_current()
            if callable(self.trade_callback):
                state = self.df.iloc[self.index].to_dict()
                self.trade_callback(state)
            self.index += 1
            time.sleep(self.speed_var.get())
        self.running = False

    # ── Plotting ──
    def plot_current(self):
        """Plot the price data up to the current index."""
        self.ax.clear()
        if not self.df.empty:
            df_plot = self.df.iloc[:self.index + 1]
            self.ax.plot(df_plot["close"], color="lime")
            self.ax.set_title("Replay / Backtesting", color="white")
        self.canvas.draw()

