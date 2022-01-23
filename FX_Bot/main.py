import bot
import MetaTrader5 as mt5

# creating the bot
b = bot.Bot(0.01, 60*50, "EURUSD")

# login into mt5
login = 6056739
password = 'Gichengo@254'
server = 'OANDA-OGM MT5 Demo'

if not mt5.initialize(login=login, server=server, password=password):
    print("initialize() failed, error code =", mt5.last_error())
    quit()
print('Meta trader initialized')

b.thread_candle()
b.thread_RSI()
b.thread_orders()
b.wait()
