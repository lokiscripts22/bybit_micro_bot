import os
import pandas as pd
from bot.features import orderbook_imbalance, momentum, volatility, trend_strength

BASE_TARGET = 0.50
TRAIL_ACTIVATE = 0.30

def decide(state):
    """
    state keys:
    price, prices, orderbook, position, entry_price,
    pnl, cooldown, time_in_trade, trail_stop, trend_bias
    """

    if state["cooldown"] > 0:
        return "hold"

    vol = volatility(state["prices"])
    dyn_target = BASE_TARGET + vol * 0.25
    soft_stop = -max(0.4, vol * 0.6)

    # ── ENTRY ──
    if state["position"] is None:
        imb = orderbook_imbalance(state["orderbook"])
        mom = momentum(state["prices"])

        if state["trend_bias"] == "up" and imb < 0:
            return "hold"
        if state["trend_bias"] == "down" and imb > 0:
            return "hold"

        if imb > 0.18 and mom > 0:
            return "buy"
        if imb < -0.18 and mom < 0:
            return "sell"
        return "hold"

    # ── TRAILING STOP ──
    if state["pnl"] >= TRAIL_ACTIVATE:
        if state["trail_stop"] is not None:
            if state["pnl"] <= state["trail_stop"]:
                return "exit"

    # ── PROFIT EXIT ──
    if state["pnl"] >= dyn_target:
        return "exit"

    # ── WICK PROTECTION ──
    imb = orderbook_imbalance(state["orderbook"])
    if state["pnl"] < 0:
        if state["position"] == "buy" and imb > -0.1:
            return "hold"
        if state["position"] == "sell" and imb < 0.1:
            return "hold"

    # ── HARD INVALIDATION ──
    if state["pnl"] <= soft_stop and state["time_in_trade"] >= 3:
        return "exit"

    return "hold"

def save_trade(trade):
    os.makedirs("data", exist_ok=True)
    path = "data/trade_history.csv"
    df = pd.DataFrame([trade])
    df.to_csv(path, mode="a", header=not os.path.exists(path), index=False)

