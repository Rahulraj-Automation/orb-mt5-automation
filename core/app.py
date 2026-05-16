from flask import Flask, request
import MetaTrader5 as mt5

# START FLASK
app = Flask(__name__)

# CONNECT MT5
mt5.initialize()

@app.route('/webhook', methods=['POST'])
def webhook():

    # RECEIVE JSON
    data = request.json

    print("Received Alert:")
    print(data)

    # CLOSE ALL POSITIONS
    if data["action"] == "close_all":

        positions = mt5.positions_get()

        if positions:
            for position in positions:

                symbol = position.symbol
                volume = position.volume
                ticket = position.ticket

                tick = mt5.symbol_info_tick(symbol)

                if position.type == mt5.POSITION_TYPE_BUY:
                    order_type = mt5.ORDER_TYPE_SELL
                    price = tick.bid
                else:
                    order_type = mt5.ORDER_TYPE_BUY
                    price = tick.ask

                close_request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": volume,
                    "type": order_type,
                    "position": ticket,
                    "price": price,
                    "deviation": 20,
                    "magic": 123456,
                    "comment": "Close All",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_FOK,
                }

                result = mt5.order_send(close_request)

                print(result)

        return "Closed All Positions"

    # EXTRACT VALUES
    symbol = data["symbol"]
    action = data["action"]

    volume = float(data["qty"])
    sl = float(data["sl"])
    tp = float(data["tp"])

    # ENABLE SYMBOL
    mt5.symbol_select(symbol, True)

    # GET PRICES
    ask_price = mt5.symbol_info_tick(symbol).ask
    bid_price = mt5.symbol_info_tick(symbol).bid

    # BUY ORDER
    if action == "buy":

        request_order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": ask_price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 123456,
            "comment": "ORB Buy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request_order)

        print(result)

    # SELL ORDER
    elif action == "sell":

        request_order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": bid_price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 123456,
            "comment": "ORB Sell",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request_order)

        print(result)

    return "Trade Executed"

# RUN FLASK
app.run(host='0.0.0.0', port=5000)