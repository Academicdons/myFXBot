import MetaTrader5 as mt
import pandas as pd
import plotly.express as px
from datetime import datetime



# make sure the trade server is enabled in MT% terminal

path = "C:\Program Files\Mozilla Firefox\Firefox.exe" #path of Firefox.exe

login = 6056739
password = 'E2wcETta'
server = 'OANDA-OGM MT5 Demo'

print('Initializing and login_in in hold on..')
print()
if not mt5.initialize(path, login=login, server=server, password=password):
    print("initialize() failed, error code =", mt5.last_error())
    quit()
print('Meta trader initialized')


# get all account info

account_info = mt.account_info()
print('Your account information is as follows: ', account_info)

# getting specific account data
login_number = account_info.login
balance = account_info.balance
equity = account_info.equity

print('your login number is: ', login_number)
print()
print('Your account balance is: ', balance)
print()
print('Your account equity is: ', equity)
print()

# get number of symbols with symbols tools

nump_symbols = mt.symbols_total()
print('The total number of symbols available is: ', nump_symbols)

# get all symbols and specofocations
# symbols = mt.symbols_get()


# get all symbols and their specification ie EUR/USD

symbol_info = mt.symbol_info("EURUSD")._asdict()
print()
print('info for EURO/USD:', symbol_info)

# get current symbol price

symbol_price = mt.symbol_info_tick("EURUSD")._asdict
print()
print("current symbole price is:", symbol_price)

# OHLC_DATA

ohlc_Data = pd.DataFrame(mt.copy_ticks_range("EURUSD",
                                             datetime(2021, 10, 4),
                                             datetime.now(),
                                             mt.COPY_TICKS_ALL
                                             ))

fig = px.line(tick_data, xmtick_data['time'], y=[tick_data['bid'], tick_data['ask']])
fig.show()
