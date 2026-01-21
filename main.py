import tkinter as tk
from ui.app import App
from bot.brain import Brain
from bot.trader import get_price, get_orderbook, get_balance, open_position, close_position
from threading import Thread
import time

# ── Launcher ──
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bybit Smart Micro Bot - Final Product")
    root.geometry("1200x720")
    root.configure(bg="#121212")

    # ── Brain / Bot instance ──
    brain = Brain()

    # ── Trade callback for replay / simulation ──
    def trade_callback(state):
        """
        Called by replay_window for each historical candle.
        Simulates trading decisions based on brain logic.
        """
        action = brain.decide(state)
        state["action"] = action
        # Save simulated trade if exit
        if action == "exit" and state.get("position"):
            pnl = (state["price"] - state["entry_price"]) * state["qty"]
            if state["position"] == "sell":
                pnl *= -1
            trade_data = {
                "side": state["position"],
                "entry": state["entry_price"],
                "exit": state["price"],
                "pnl": pnl,
                "confidence": 100,  # placeholder, can be calculated
                "live": False
            }
            brain.save_trade(trade_data)

    # ── App / UI ──
    app = App(root, brain, trade_callback)

    # ── Start Tkinter mainloop ──
    root.mainloop()

