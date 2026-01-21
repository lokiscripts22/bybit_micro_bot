"""
trade_panel.py

A GUI panel for displaying live trading information for the Spot Bot.

Features:
- Shows current position, entry price, leverage, PnL, trailing stop, and cooldown
- Updates dynamically with color-coded PnL and trailing stop status
"""

import tkinter as tk


class TradePanel:
    def __init__(self, master, settings=None):
        """
        Initialize the trading panel GUI.

        Args:
            master: parent Tkinter frame
            settings: optional settings object for default values
        """
        self.master = tk.Frame(master, bg="#121212", bd=2, relief=tk.RIDGE)
        self.master.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        self.settings = settings

        # Labels
        self.position_label = tk.Label(
            self.master, text="Position: NONE", fg="white", bg="#121212",
            font=("Arial", 12, "bold")
        )
        self.position_label.pack(pady=5)

        self.entry_label = tk.Label(self.master, text="Entry Price: 0.0", fg="white", bg="#121212")
        self.entry_label.pack(pady=5)

        self.leverage_label = tk.Label(self.master, text="Leverage: 0x", fg="white", bg="#121212")
        self.leverage_label.pack(pady=5)

        self.pnl_label = tk.Label(self.master, text="PnL: 0.0", fg="white", bg="#121212")
        self.pnl_label.pack(pady=5)

        self.trail_label = tk.Label(self.master, text="Trailing Stop: OFF", fg="white", bg="#121212")
        self.trail_label.pack(pady=5)

        self.cooldown_label = tk.Label(self.master, text="Cooldown: 0", fg="white", bg="#121212")
        self.cooldown_label.pack(pady=5)

        # For dynamic PnL coloring
        self.current_pnl = 0.0

    # ── Update Methods ──
    def update_position(self, position):
        self.position_label.config(
            text=f"Position: {position.upper() if position else 'NONE'}"
        )

    def update_entry(self, price):
        self.entry_label.config(
            text=f"Entry Price: {price:.2f}" if price else "Entry Price: 0.0"
        )

    def update_leverage(self, leverage):
        self.leverage_label.config(
            text=f"Leverage: {leverage}x" if leverage else "Leverage: 0x"
        )

    def update_pnl(self, pnl):
        self.current_pnl = pnl
        color = "lime" if pnl > 0 else "red" if pnl < 0 else "white"
        self.pnl_label.config(text=f"PnL: {pnl:.2f}", fg=color)

    def update_trailing(self, active):
        text = "ON" if active else "OFF"
        color = "lime" if active else "white"
        self.trail_label.config(text=f"Trailing Stop: {text}", fg=color)

    def update_cooldown(self, cooldown):
        self.cooldown_label.config(text=f"Cooldown: {cooldown}")

    # ── Batch Update ──
    def update_all(self, state):
        """
        Update all labels based on a state dictionary.

        Args:
            state (dict): Expected keys:
                - position
                - entry_price
                - leverage
                - pnl
                - trail_stop
                - cooldown
        """
        self.update_position(state.get("position"))
        self.update_entry(state.get("entry_price", 0.0))
        self.update_leverage(state.get("leverage", 0))
        self.update_pnl(state.get("pnl", 0.0))
        self.update_trailing(state.get("trail_stop") is not None)
        self.update_cooldown(state.get("cooldown", 0))

