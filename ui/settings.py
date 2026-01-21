"""
settings.py

A GUI panel for configuring Spot Bot settings using Tkinter.

Features:
- Adjustable starting balance, trade size, max leverage, and risk per trade
- Trailing stop, default mode, and trading symbol selection
- Optional callback function for dynamic updates
"""

import tkinter as tk
from tkinter import ttk


class Settings:
    def __init__(self, master, update_callback=None):
        """
        Initialize the settings panel.

        Args:
            master: Parent Tkinter frame or Toplevel
            update_callback: Optional function called when a setting changes
        """
        self.master = tk.Frame(master, bg="#121212", bd=2, relief=tk.RIDGE)
        self.master.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.update_callback = update_callback

        # Internal settings storage with defaults
        self.settings = {
            "balance": 1000.0,
            "usdt_per_trade": 10.0,
            "max_leverage": 10,
            "risk_percent": 1.0,
            "trailing_stop": 0.15,
            "default_mode": "LEARNING",
            "symbol": "BTC/USDT"
        }

        # Create UI controls
        self.create_balance_setting()
        self.create_trade_setting()
        self.create_leverage_setting()
        self.create_risk_setting()
        self.create_trailing_stop_setting()
        self.create_mode_setting()
        self.create_symbol_setting()

    # ── Individual setting creation ──
    def create_balance_setting(self):
        """Create a slider to adjust starting balance."""
        tk.Label(self.master, text="Starting Balance (USDT)", fg="white", bg="#121212").pack(pady=3)
        self.balance_var = tk.DoubleVar(value=self.settings["balance"])
        slider = tk.Scale(self.master, from_=100, to=100000, resolution=50, orient=tk.HORIZONTAL,
                          variable=self.balance_var, length=200, bg="#121212", fg="white", troughcolor="#333333",
                          command=lambda x: self.update_setting("balance", self.balance_var.get()))
        slider.pack(pady=3)

    def create_trade_setting(self):
        """Create a slider to adjust USDT per trade."""
        tk.Label(self.master, text="USDT per Trade", fg="white", bg="#121212").pack(pady=3)
        self.usdt_var = tk.DoubleVar(value=self.settings["usdt_per_trade"])
        slider = tk.Scale(self.master, from_=1, to=500, resolution=1, orient=tk.HORIZONTAL,
                          variable=self.usdt_var, length=200, bg="#121212", fg="white", troughcolor="#333333",
                          command=lambda x: self.update_setting("usdt_per_trade", self.usdt_var.get()))
        slider.pack(pady=3)

    def create_leverage_setting(self):
        """Create a slider to adjust maximum leverage."""
        tk.Label(self.master, text="Max Leverage", fg="white", bg="#121212").pack(pady=3)
        self.leverage_var = tk.IntVar(value=self.settings["max_leverage"])
        slider = tk.Scale(self.master, from_=1, to=150, orient=tk.HORIZONTAL,
                          variable=self.leverage_var, length=200, bg="#121212", fg="white", troughcolor="#333333",
                          command=lambda x: self.update_setting("max_leverage", self.leverage_var.get()))
        slider.pack(pady=3)

    def create_risk_setting(self):
        """Create a slider to adjust risk percentage per trade."""
        tk.Label(self.master, text="Risk % per Trade", fg="white", bg="#121212").pack(pady=3)
        self.risk_var = tk.DoubleVar(value=self.settings["risk_percent"])
        slider = tk.Scale(self.master, from_=0.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL,
                          variable=self.risk_var, length=200, bg="#121212", fg="white", troughcolor="#333333",
                          command=lambda x: self.update_setting("risk_percent", self.risk_var.get()))
        slider.pack(pady=3)

    def create_trailing_stop_setting(self):
        """Create a slider to adjust trailing stop."""
        tk.Label(self.master, text="Trailing Stop ($)", fg="white", bg="#121212").pack(pady=3)
        self.trail_var = tk.DoubleVar(value=self.settings["trailing_stop"])
        slider = tk.Scale(self.master, from_=0.05, to=1.0, resolution=0.01, orient=tk.HORIZONTAL,
                          variable=self.trail_var, length=200, bg="#121212", fg="white", troughcolor="#333333",
                          command=lambda x: self.update_setting("trailing_stop", self.trail_var.get()))
        slider.pack(pady=3)

    def create_mode_setting(self):
        """Create a dropdown to select default mode (LEARNING or LIVE)."""
        tk.Label(self.master, text="Default Mode", fg="white", bg="#121212").pack(pady=3)
        self.mode_var = tk.StringVar(value=self.settings["default_mode"])
        menu = ttk.Combobox(self.master, textvariable=self.mode_var, values=["LEARNING", "LIVE"], state="readonly")
        menu.pack(pady=3)
        menu.bind("<<ComboboxSelected>>", lambda e: self.update_setting("default_mode", self.mode_var.get()))

    def create_symbol_setting(self):
        """Create a dropdown to select trading symbol."""
        tk.Label(self.master, text="Trading Symbol", fg="white", bg="#121212").pack(pady=3)
        self.symbol_var = tk.StringVar(value=self.settings["symbol"])
        menu = ttk.Combobox(self.master, textvariable=self.symbol_var,
                            values=["BTC/USDT", "ETH/USDT"], state="readonly")
        menu.pack(pady=3)
        menu.bind("<<ComboboxSelected>>", lambda e: self.update_setting("symbol", self.symbol_var.get()))

    # ── Update Methods ──
    def update_setting(self, key, value):
        """Update a setting and call the callback if provided."""
        self.settings[key] = value
        if callable(self.update_callback):
            self.update_callback(key, value)

    def get(self, key):
        """Get the current value of a setting."""
        return self.settings.get(key)

