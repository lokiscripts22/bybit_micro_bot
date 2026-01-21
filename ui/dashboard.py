"""
dashboard.py

A Tkinter-based dashboard for visualizing live trading data.

Features:
- Candlestick chart plotting using mplfinance
- Trend and confidence meters
- Live updating loop for price data
"""

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from threading import Thread
import time

# Import your trading data functions
from bot.trader import get_price, get_orderbook


class Dashboard:
    def __init__(self, master):
        """
        Initialize the Dashboard GUI.

        Args:
            master: Parent Tkinter frame or window
        """
        self.master = master
        self.frame = tk.Frame(master, bg="#1E1E1E", bd=2, relief=tk.RIDGE)

        # ── Candlestick Figure ──
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_facecolor("#121212")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # ── Trend / Confidence meters ──
        self.trend_var = tk.DoubleVar(value=50)
        self.confidence_var = tk.DoubleVar(value=50)
        self.trend_meter = tk.Scale(
            self.frame, from_=0, to=100, variable=self.trend_var,
            orient=tk.VERTICAL, length=150, fg="white",
            troughcolor="#333333", bg="#121212", label="Trend"
        )
        self.trend_meter.pack(side=tk.LEFT, padx=5)

        self.confidence_meter = tk.Scale(
            self.frame, from_=0, to=100, variable=self.confidence_var,
            orient=tk.VERTICAL, length=150, fg="white",
            troughcolor="#333333", bg="#121212", label="Confidence"
        )
        self.confidence_meter.pack(side=tk.LEFT, padx=5)

        # ── Chart Data Storage ──
        self.prices = []
        self.running = False

    # ── Start / Stop ──
    def start(self, symbol="BTC/USDT", timeframe="1m", update_interval=2):
        """
        Start the dashboard update loop.

        Args:
            symbol: Trading symbol to track
            timeframe: Timeframe for charting
            update_interval: Seconds between updates
        """
        self.running = True
        Thread(target=self.update_loop, args=(symbol, timeframe, update_interval), daemon=True).start()

    def stop(self):
        """Stop the dashboard update loop."""
        self.running = False

    # ── Update Loop ──
    def update_loop(self, symbol, timeframe, interval):
        """Main loop that fetches price data, updates meters, and redraws the chart."""
        while self.running:
            try:
                price = get_price()
                self.prices.append(price)
                self.update_meters()
                self.plot_chart()
            except Exception as e:
                print(f"[ERROR] Dashboard update: {e}")
            time.sleep(interval)

    # ── Trend & Confidence ──
    def update_meters(self):
        """Update the trend and confidence meters based on price changes."""
        if len(self.prices) < 2:
            return
        delta = self.prices[-1] - self.prices[-2]
        trend = min(max(50 + delta * 50, 0), 100)
        confidence = min(max(50 + abs(delta) * 50, 0), 100)
        self.trend_var.set(trend)
        self.confidence_var.set(confidence)

    # ── Plotting ──
    def plot_chart(self):
        """Plot candlestick chart from collected prices using mplfinance."""
        if len(self.prices) < 10:
            return
        self.ax.clear()
        df = pd.DataFrame({"close": self.prices})
        df.index = pd.date_range(end=pd.Timestamp.now(), periods=len(df), freq='S')
        mpf.plot(df, type='candle', style='charles', ax=self.ax, volume=False, show_nontrading=True)
        self.canvas.draw()

