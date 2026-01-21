"""
controls.py

Bot control panel for Tkinter GUI.

Features:
- Start / Stop buttons
- Mode toggle (LEARNING / LIVE)
- Optional sliders synced with Settings: Leverage, Risk %, Trailing Stop
"""

import tkinter as tk
from tkinter import ttk


class Controls:
    def __init__(self, master, start_callback=None, stop_callback=None, mode_callback=None, settings=None):
        """
        Initialize the Controls panel.

        Args:
            master: Parent Tkinter frame
            start_callback: function() called when Start is pressed
            stop_callback: function() called when Stop is pressed
            mode_callback: function(mode) called when mode changes
            settings: Settings object (optional, to sync sliders)
        """
        self.master = tk.Frame(master, bg="#121212", bd=2, relief=tk.RIDGE)
        self.master.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.mode_callback = mode_callback
        self.settings = settings

        # ── Start / Stop Buttons ──
        self.start_btn = tk.Button(self.master, text="▶ Start Bot", fg="white", bg="#33aa33",
                                   command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_btn = tk.Button(self.master, text="⏹ Stop Bot", fg="white", bg="#aa3333",
                                  command=self.stop)
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # ── Mode Toggle ──
        self.mode_var = tk.StringVar(value=self.settings.get("default_mode") if self.settings else "LEARNING")
        self.mode_toggle = ttk.Combobox(
            self.master, textvariable=self.mode_var,
            values=["LEARNING", "LIVE"], state="readonly"
        )
        self.mode_toggle.pack(side=tk.LEFT, padx=10)
        self.mode_toggle.bind("<<ComboboxSelected>>", self.change_mode)

        # ── Optional Sliders from Settings ──
        if self.settings:
            self.create_leverage_slider()
            self.create_risk_slider()
            self.create_trailing_slider()

    # ── Start / Stop Methods ──
    def start(self):
        """Call start callback and update button color."""
        if callable(self.start_callback):
            self.start_callback()
        self.start_btn.config(bg="#22cc22")

    def stop(self):
        """Call stop callback and reset button color."""
        if callable(self.stop_callback):
            self.stop_callback()
        self.start_btn.config(bg="#33aa33")

    # ── Mode Toggle Method ──
    def change_mode(self, event=None):
        """Call mode callback when mode is changed."""
        mode = self.mode_var.get()
        if callable(self.mode_callback):
            self.mode_callback(mode)

    # ── Sliders ──
    def create_leverage_slider(self):
        tk.Label(self.master, text="Max Leverage", fg="white", bg="#121212").pack(side=tk.LEFT, padx=5)
        self.leverage_var = tk.IntVar(value=self.settings.get("max_leverage"))
        self.leverage_slider = tk.Scale(
            self.master, from_=1, to=150, orient=tk.HORIZONTAL,
            variable=self.leverage_var, length=150,
            bg="#121212", fg="white", troughcolor="#333333",
            command=lambda x: self.settings.update_setting("max_leverage", self.leverage_var.get())
        )
        self.leverage_slider.pack(side=tk.LEFT, padx=5)

    def create_risk_slider(self):
        tk.Label(self.master, text="Risk %", fg="white", bg="#121212").pack(side=tk.LEFT, padx=5)
        self.risk_var = tk.DoubleVar(value=self.settings.get("risk_percent"))
        self.risk_slider = tk.Scale(
            self.master, from_=0.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL,
            variable=self.risk_var, length=150,
            bg="#121212", fg="white", troughcolor="#333333",
            command=lambda x: self.settings.update_setting("risk_percent", self.risk_var.get())
        )
        self.risk_slider.pack(side=tk.LEFT, padx=5)

    def create_trailing_slider(self):
        tk.Label(self.master, text="Trailing Stop ($)", fg="white", bg="#121212").pack(side=tk.LEFT, padx=5)
        self.trail_var = tk.DoubleVar(value=self.settings.get("trailing_stop"))
        self.trail_slider = tk.Scale(
            self.master, from_=0.05, to=1.0, resolution=0.01, orient=tk.HORIZONTAL,
            variable=self.trail_var, length=150,
            bg="#121212", fg="white", troughcolor="#333333",
            command=lambda x: self.settings.update_setting("trailing_stop", self.trail_var.get())
        )
        self.trail_slider.pack(side=tk.LEFT, padx=5)

