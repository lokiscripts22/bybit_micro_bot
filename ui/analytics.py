import tkinter as tk
from tkinter import ttk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Analytics:
    def __init__(self, master):
        """
        master: parent frame or Toplevel
        """
        self.master = tk.Frame(master, bg="#121212", bd=2, relief=tk.RIDGE)
        self.master.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ── Trade History Table ──
        self.table = ttk.Treeview(self.master, columns=("Entry", "Exit", "Side", "Qty", "PnL", "Confidence", "Live"), show="headings")
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, anchor=tk.CENTER, width=80)
        self.table.pack(fill=tk.BOTH, expand=True, pady=5)

        # Dark theme colors
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background="#1E1E1E", foreground="white", fieldbackground="#1E1E1E")
        style.configure("Treeview.Heading", background="#333333", foreground="white")

        # ── Performance Stats ──
        stats_frame = tk.Frame(self.master, bg="#121212")
        stats_frame.pack(fill=tk.X, pady=5)
        self.total_pnl_label = tk.Label(stats_frame, text="Total PnL: 0", fg="lime", bg="#121212")
        self.total_pnl_label.pack(side=tk.LEFT, padx=5)
        self.win_rate_label = tk.Label(stats_frame, text="Win Rate: 0%", fg="cyan", bg="#121212")
        self.win_rate_label.pack(side=tk.LEFT, padx=5)
        self.avg_pnl_label = tk.Label(stats_frame, text="Avg PnL: 0", fg="yellow", bg="#121212")
        self.avg_pnl_label.pack(side=tk.LEFT, padx=5)
        self.max_drawdown_label = tk.Label(stats_frame, text="Max Drawdown: 0", fg="red", bg="#121212")
        self.max_drawdown_label.pack(side=tk.LEFT, padx=5)

        # ── Performance Graph ──
        self.fig, self.ax = plt.subplots(figsize=(5,3))
        self.ax.set_facecolor("#121212")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.set_title("Cumulative PnL", color="white")
        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Internal storage
        self.trades = pd.DataFrame(columns=["entry", "exit", "side", "qty", "pnl", "confidence", "live"])
        self.cum_pnl = []

    # ── Add trade record ──
    def add_trade(self, trade):
        """
        trade: dict with keys ['entry','exit','side','qty','pnl','confidence','live']
        """
        self.trades = pd.concat([self.trades, pd.DataFrame([trade])], ignore_index=True)
        self.table.insert("", tk.END, values=(
            trade["entry"], trade["exit"], trade["side"], trade["qty"],
            round(trade["pnl"],2), trade["confidence"], "LIVE" if trade["live"] else "SIM"
        ))
        self.update_stats()
        self.update_graph()

    # ── Update stats labels ──
    def update_stats(self):
        if self.trades.empty:
            return
        total_pnl = self.trades["pnl"].sum()
        wins = len(self.trades[self.trades["pnl"] > 0])
        total = len(self.trades)
        win_rate = (wins / total) * 100 if total > 0 else 0
        avg_pnl = self.trades["pnl"].mean()
        drawdown = (self.trades["pnl"].cumsum().min())

        self.total_pnl_label.config(text=f"Total PnL: {round(total_pnl,2)}")
        self.win_rate_label.config(text=f"Win Rate: {round(win_rate,1)}%")
        self.avg_pnl_label.config(text=f"Avg PnL: {round(avg_pnl,2)}")
        self.max_drawdown_label.config(text=f"Max Drawdown: {round(abs(drawdown),2)}")

    # ── Update cumulative PnL graph ──
    def update_graph(self):
        if self.trades.empty:
            return
        self.ax.clear()
        cum_pnl = self.trades["pnl"].cumsum()
        self.ax.plot(cum_pnl, color="lime" if cum_pnl.iloc[-1] >= 0 else "red")
        self.ax.set_facecolor("#121212")
        self.ax.set_title("Cumulative PnL", color="white")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.canvas.draw()
