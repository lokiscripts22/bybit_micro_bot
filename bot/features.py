import numpy as np

def orderbook_imbalance(orderbook, depth=10):
    bids = orderbook.get("bids", [])[:depth]
    asks = orderbook.get("asks", [])[:depth]

    bid_vol = sum(b[1] for b in bids) if bids else 0
    ask_vol = sum(a[1] for a in asks) if asks else 0

    if bid_vol + ask_vol == 0:
        return 0
    return (bid_vol - ask_vol) / (bid_vol + ask_vol)

def momentum(prices, lookback=6):
    if len(prices) < lookback:
        return 0
    return prices[-1] - prices[-lookback]

def volatility(prices, lookback=20):
    if len(prices) < lookback:
        return 0
    return np.std(prices[-lookback:])

def trend_strength(prices, lookback=50):
    if len(prices) < lookback:
        return 0
    return prices[-1] - prices[-lookback]
