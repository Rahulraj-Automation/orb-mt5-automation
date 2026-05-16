import MetaTrader5 as mt5

# connect to MT5
mt5.initialize()

# get account info
account = mt5.account_info()

print(account)