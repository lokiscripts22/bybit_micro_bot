import ccxt

API_KEY = "gVoGfxgyIKLCKhVLA0"
API_SECRET = "ajmFZexUoBdLEbxlUE7GUKuKjmCtevcKJsf8"

exchange = ccxt.bybit({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "enableRateLimit": True,
    "options": {"defaultType": "linear"}
})

SYMBOL = "BTC/USDT"

USDT_PER_TRADE = 10

def set_symbol(symbol):
    global SYMBOL
    SYMBOL = symbol

def set_leverage(leverage):
    try:
        exchange.private_post_position_leverage_save({
            "symbol": SYMBOL.replace("/", ""),
            "buy_leverage": leverage,
            "sell_leverage": leverage
        })
    except Exception as e:
        print(f"[ERROR] Failed to set leverage: {e}")

def get_balance():
    try:
        bal = exchange.fetch_balance({"accountType": "UNIFIED"})
        return float(bal["total"].get("USDT", 0))
    except:
        return 0

def get_price():
    try:
        return exchange.fetch_ticker(SYMBOL)["last"]
    except:
        return 0

def get_orderbook():
    try:
        return exchange.fetch_order_book(SYMBOL, limit=25)
    except:
        return {"bids":[], "asks":[]}

def open_position(side, leverage):
    set_leverage(leverage)
    price = get_price()
    qty = round((USDT_PER_TRADE * leverage) / price, 6)
    try:
        order = exchange.create_order(SYMBOL, "market", side, qty)
    except:
        order = None
    return qty, price, order

def close_position(position):
    side = "sell" if position["side"] == "buy" else "buy"
    try:
        exchange.create_order(SYMBOL, "market", side, position["qty"])
    except:
        pass

