import orders
import time
import MetaTrader5 as mt5

login = 6056739
password = 'Gichengo@254'
server = 'OANDA-OGM MT5 Demo'

if not mt5.initialize(login=login, server=server, password=password):
    print("initialize() failed, error code =", mt5.last_error())
    quit()
print('Meta trader test order initialized')

orders.STOPLOSS = 100
orders.TAKEPROFIT = 500
orders.open_position("EURUSD", 0.01, "buy")
time.sleep(5)

orders.open_position("EURGBP", 0.01, "sell")