import MetaTrader5 as mt
import MetaTrader5 as mt5
import pandas as pd
import plotly.express as px
from datetime import *
import threading
from time import *
from decimal import *
import time
import sys

# make sure the trade server is enabled in MT% terminal
# trade type o for buying 1 for selling
print("""

dP     dP                 dP          oo                       888888ba             dP   dP                         
88     88                 88                                   88    `8b            88   88                         
88aaaaa88a .d8888b. .d888b88 .d8888b. dP 88d888b. .d8888b.    a88aaaa8P' dP    dP d8888P 88d888b. .d8888b. 88d888b. 
88     88  88ooood8 88'  `88 88'  `88 88 88'  `88 88'  `88     88        88    88   88   88'  `88 88'  `88 88'  `88 
88     88  88.  ... 88.  .88 88.  .88 88 88    88 88.  .88     88        88.  .88   88   88    88 88.  .88 88    88 
dP     dP  `88888P' `88888P8 `8888P88 dP dP    dP `8888P88     dP        `8888P88   dP   dP    dP `88888P' dP    dP 
                                    8                    8                      8
                              d8888P               d8888P                 d8888P

                              
                                             888888ba             dP                                                                    
                                             88    `8b            88                                                                    
                                            a88aaaa8P' .d8888b. d8888P                                                                  
                                             88   `8b. 88'  `88   88                                                                    
                                             88    .88 88.  .88   88                                                                    
                                             88888888P `88888P'   dP                                                                    
                                                                                          
        """)
print('Initializing and login in hold on..')
print()
print()
type_input = input('select trade to state 0 for buying and 1 for selling: ')
trade_type = int(type_input)

print()
lotage = input('enter your desired lot size where 0.01 equals $1000: ')
lotage = float(lotage)

#print()
#TAKEPROFIT = input('enter your desired Take Profit size in points ie 100: ')
#TAKEPROFIT = float(TAKEPROFIT)

#print()
#STOPLOSS = input('enter your desired Stop Loss size in points ie 50: ')
#STOPLOSS = float(STOPLOSS)
    

trade_type = trade_type
no_of_orders = 0
currency = "USDCAD"
tp = 0
current_price = 0
sl = 0
order_id = 0
position = 0
balance = 0
profitable_trades = 0
lost_trade = 0
#TAKEPRofit = TAKEPROFIT
#STOPLoss = STOPLOSS
lotage = lotage



def check_state_of_last_order():
    global no_of_orders
    global currency
    global tp
    global sl
    global trade_type
    global position
    global profitable_trades
    global order_id
    global lost_trade
    global current_price
    global balance
    
    currency = currency
    order_id = order_id
    print("checking state of last order")
    account_info = mt.account_info()
    from_date = datetime(2022, 1, 24)
    to_date = datetime.now()
    
    #getting last closed order now
    print("the last orders Id is: ", order_id)
    last_order = mt.history_orders_get(ticket = order_id)
    last_order = last_order[0]
    currency_price = last_order[19]
    print("Current price is: ", currency_price)
    balance = balance
    balance_After_trade = account_info.balance
    profit = balance_After_trade - balance
    balance = balance_After_trade
    
    if profit > 0:
        profitable_trades += 1
        
        print("Your trade profit is: ", profit)

        if trade_type == 0:
            print("Your previous trade was a buy trade")
            place_an_order()
        else:
            print("Your previous trade was a sell trade")
            place_an_order()
        
    elif profit == 0:
        print("Your trade did not affect the balance ")
        place_an_order()
    else:
        lost_trade += 1
        print("Your trade losss is: ", profit)
        if trade_type == 0:
            print("Your previous trade was a buy trade")
            trade_type+=1
            if trade_type ==0:
                print("DID NOT CHANGE TYPE TO SELL")
                mt.shutdown()
            else:
                pass
            print("Changed the trade type to sell for the next order")
            place_an_order()
            
        else:
            print("Your previous trade was a sell trade")
            trade_type-=1
            if trade_type == 1:
                print("DID NOT CHANGE TYPE TO Buy")
                mt.shutdown()
            else:
                pass
            print("changed trade type to buy for the next order")
            place_an_order()
    


def check_order_state():
    global no_of_orders
    global currency
    global tp
    global sl
    global trade_type
    global position
    global order_id
    currency = currency
    order_id = order_id

    orders = mt.positions_total()
    no_of_orders = no_of_orders
    try:
        if orders == 1:
            time.sleep(5)
            checking_manual_loop()
            
        else:
            print('order', no_of_orders, "completed successfully")
            check_state_of_last_order()
    except RecursionError as re:
        check_order_state()

def checking_manual_loop():
    check_order_state()

        


def get_price():
    threading.Timer(0.1, get_price).start()
    global selling_price
    global buying_price
    buying_price = mt.symbol_info_tick("USDCAD").ask
    selling_price = mt.symbol_info_tick("USDCAD").bid
    print('The asking and bidding price is', buying_price, 'and', selling_price, 'as at: ', datetime.now())


def place_an_order():
    global no_of_orders
    global tp
    global sl
    global trade_type
    global position
    global balance
    global TAKEPRofit
    global STOPLoss
    global lotage
    
    

    no_of_orders = no_of_orders
    if no_of_orders == 0:
        print()
        
        print('placing order now')
        no_of_orders += 1
    else:
        no_of_orders += 1
        print('an order found')
        pass
    
    
    

    market = "USDCAD"
    print()
    
    lotage = lotage

    trade_type = trade_type

    point = mt5.symbol_info(market).point
    price = mt5.symbol_info_tick(market).ask
    print("price right now is: ", price)

    if trade_type == 0:
        print('its a buy order')
        sl = price - 40 * point
        tp = price + 80 * point
    else:
        print("Its a sell order")
        sl = price + 40 * point
        tp = price - 80 * point
    print('Your sl and tp are :', sl, 'and', tp)

    deviation = 20

    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": market,
        "volume": lotage,
        "type": mt5.ORDER_TYPE_BUY if trade_type == 0 else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price + 40 * point if trade_type ==1 else price - 40 * point,
        "tp": price - 80 * point if trade_type ==1 else price + 80 * point,
        "deviation": 20,
        "magic":  int(datetime.now().timestamp()),
        "comment": "st_1_min_mod_3",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
            }

    # Sending the buy
    result = mt5.order_send(request)
    global order_id
    order_id = result[2]
    position += 1
    #    print(
    #        "[Thread - orders] 1. order_send(): by {} {} lots at {} with deviation={} points".format(market, lotage, price,
    #                                                                                                     deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("[Thread - orders] Failed operation: retcode={}".format(result.retcode))
        return None
    print('order', no_of_orders, "is still running, Please hold on")

    check_order_state()


def init_bot():
    global no_of_orders
    global balance
    no_of_orders = 0
    path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"  # path of terminal64.exe

    login = 6056739
    password = 'Gichengo@254'
    server = 'OANDA-OGM MT5 Demo'
    

    if not mt.initialize(path, login = login, server = server, password = password):
        print("initialize() failed, error code =", mt.last_error())
        quit()
    print('Meta trader initialized')
    
    account_info = mt.account_info()
    balance = account_info.balance
    print("The account balance is:", balance,"as at: ", datetime.now())
    place_an_order()


if __name__ == '__main__':
    print('Please wait ..')
    init_bot()
