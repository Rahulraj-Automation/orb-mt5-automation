import MetaTrader5 as mt5

# CONNECT TO MT5
mt5.initialize()

# SYMBOL
symbol = "EURUSD"

# ENABLE SYMBOL
mt5.symbol_select(symbol, True)

# GET CURRENT ASK PRICE
price = mt5.symbol_info_tick(symbol).ask

# ORDER REQUEST
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": 0.01,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "deviation": 20,
    "magic": 123456,
    "comment": "Python Buy Test",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_FOK,
}

# SEND ORDER
result = mt5.order_send(request)

# PRINT RESULT
print(result)