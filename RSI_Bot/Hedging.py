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
trade_type = 0
no_of_orders = 0
currency = "USD"
tp = 0
current_price = 0
sl = 0
order_id = 0
position = 0
balance = 0
profitable_trades = 0
lost_trade = 0
TAKEPRofit = 0
STOPLoss = 0
lotage = 0

def place_order_loop():
    global TAKEPRofit
    global STOPLoss
    global lotage
    global trade_type
    global position

    lotage = lotage
    if lotage is None:
        print("no lotage found")
    else:
        print("lotage found to be: ", lotage)
    market = "EURUSD"
    trade_type = trade_type
    TAKEPROFIT = TAKEPRofit
    STOPLOSS = STOPLoss
    prices = mt.symbol_info_tick("EURUSD").ask
    points = mt5.symbol_info(market).point
    #price = current_price
    if price == 0:
        print("no price found")
        mt.shutdown()
    else:
        print("price found to be: ", prices)

    if trade_type == 0:
        print('its a buy order')
        sl = prices - STOPLOSS * points
        tp = prices + TAKEPROFIT * points
    else:
        print("Its a sell order")
        sl = prices + STOPLOSS * points
        tp = prices - TAKEPROFIT * points
    print('Your sl and tp are :', sl, 'and', tp)
    sl = float(sl)
    tp = float(tp)
    lotage = float(lotage)
    deviation = 20
    position = position
    
    operation = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": market,
        "volume": lotage,
        "type": mt5.ORDER_TYPE_BUY if trade_type == 0 else mt5.ORDER_TYPE_SELL,
        "price": prices,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": int(datetime.now().timestamp()),
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Sending the buy
    result = mt5.order_send(operation)
    print(result)
    global order_id
    order_id = result[2]
    position += 1
    #    print(
    #        "[Thread - orders] 1. order_send(): by {} {} lots at {} with deviation={} points".format(market, lotage, price,
    #                                                                                                     deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("failed due to: ", mt.last_error())
        print("[Thread - orders] Failed operation: retcode={}".format(result.retcode))
        
        return None

    check_order_state()


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
    print("your last order is: ", last_order)
    print("Current price is: ", currency_price)

    balance_After_trade = account_info.balance
    profit = balance_After_trade - balance
    
    if profit > 0:
        profitable_trades += 1
        
        print("Your trade profit is: ", profit)

        if trade_type == 0:
            print("Your previous trade was a buy trade")
            print("moving to place order loop")
            place_order_loop()
        else:
            print("Your previous trade was a sell trade")
            print("moving to place order loop")
            place_order_loop()
        
    elif profit == 0:
        print("Your trade did not affect the balance ")
        print("moving to place order loop")
        place_order_loop()
    else:
        lost_trade += 1
        print("Your trade losss is: ", profit)
        if trade_type == 0:
            print("Your previous trade was a buy trade")
            trade_type == 1
            if trade_type ==0:
                print("DID NOT CHANGE TYPE TO SELL")
                mt.shutdown()
            else:
                pass
            print("Changed the trade type to sell for the next order")
            print("moving to place order loop")
            place_order_loop()
            
        else:
            print("Your previous trade was a sell trade")
            trade_type == 0
            if trade_type ==1:
                print("DID NOT CHANGE TYPE TO Buy")
                mt.shutdown()
            else:
                pass
            print("changed trade type to buy for the next order")
            print("moving to place order loop")
            place_order_loop()
    


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
    print('we have ', orders, 'running')
    no_of_orders = no_of_orders
    try:
        if orders == 1:
            print('order', no_of_orders, "is still running, Please hold on")
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
    buying_price = mt.symbol_info_tick("EURUSD").ask
    selling_price = mt.symbol_info_tick("EURUSD").bid
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
    
    account_info = mt.account_info()
    balance = account_info.balance
    print("The account balance is:", balance,"as at: ", datetime.now())

    no_of_orders = no_of_orders
    if no_of_orders == 0:
        print()
        type_input = input('select trade to state 0 for buying and 1 for selling: ')
        trade_type = int(type_input)
        print('placing order now')
        no_of_orders += 1
    else:
        no_of_orders += 1
        print('an order found')
        pass

    TAKEPROFIT = input('enter your desired Take Profit size in points ie 100: ')
    TAKEPROFIT = float(TAKEPROFIT)
    tp = TAKEPROFIT
    TAKEPRofit = TAKEPROFIT
    
    print()
    STOPLOSS = input('enter your desired Stop Loss size in points ie 50: ')
    STOPLOSS = float(STOPLOSS)
    sl = STOPLOSS
    STOPLoss = STOPLOSS
    market = "EURUSD"
    print()
    lotage = input('enter your desired lot size where 0.01 equals $1000: ')
    lotage = float(lotage)
    

    trade_type = trade_type

    point = mt5.symbol_info(market).point
    price = mt5.symbol_info_tick(market).ask

    if trade_type == 0:
        print('its a buy order')
        sl = price - STOPLOSS * point
        tp = price + TAKEPROFIT * point
    else:
        print("Its a sell order")
        sl = price + STOPLOSS * point
        tp = price - TAKEPROFIT * point
    print('Your sl and tp are :', sl, 'and', tp)

    deviation = 20
    position = position

    operation = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": market,
        "volume": lotage,
        "type": mt5.ORDER_TYPE_BUY if trade_type == 0 else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": int(datetime.now().timestamp()),
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Sending the buy
    result = mt5.order_send(operation)
    print(result)
    global order_id
    order_id = result[2]
    position += 1
    #    print(
    #        "[Thread - orders] 1. order_send(): by {} {} lots at {} with deviation={} points".format(market, lotage, price,
    #                                                                                                     deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("[Thread - orders] Failed operation: retcode={}".format(result.retcode))
        return None

    check_order_state()


def init_bot():
    global no_of_orders
    no_of_orders = 0
    path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"  # path of terminal64.exe

    login = 6056739
    password = 'Gichengo@254'
    server = 'OANDA-OGM MT5 Demo'
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

    if not mt.initialize(path, login = login, server = server, password = password):
        print("initialize() failed, error code =", mt.last_error())
        quit()
    print('Meta trader initialized')
    place_an_order()

    # def acc_info():
    #     # get all account info
    #
    #     account_info = mt.account_info()
    #
    #     # getting specific account data
    #     balance = account_info.balance
    #     login_number = account_info.login
    #     equity = account_info.equity
    #
    #
    #     # get number of symbols with symbols tools
    #
    #     nump_symbols = mt.symbols_total()
    #
    #     # get all symbols and specofocations
    #     # symbols = mt.symbols_get()
    #
    #
    #     # get all symbols and their specification ie EUR/USD
    #
    #     symbol_info = mt.symbol_info("EURUSD")._asdict()
    #
    #
    #     # get current symbol price
    #
    #     symbol_price = mt.symbol_info_tick("EURUSD")._asdict()
    #     symbol_price
    #     print()
    #     print("current symbole price is:", symbol_price)

    # OHLC_DATA

    # ohlc_Data = pd.DataFrame(mt.copy_rates_range("EURUSD",
    #                                              mt.TIMEFRAME_D1,
    #                                              datetime(2022, 1, 1),
    #                                             datetime.now(),
    #                                             ))

    # OHLCfig = px.line(ohlc_Data, x=ohlc_Data['time'], y=ohlc_Data['close'])

    # Request tick data

    # tick_data = pd.DataFrame(mt.copy_ticks_range("EURUSD",
    #                                              datetime(2022, 1, 1),
    #                                              datetime.now(),
    #                                              mt.COPY_TICKS_ALL
    #                                              ))
    # tick_fig = px.line(tick_data, x=tick_data['time'], y=[tick_data['bid'],tick_data['ask']])
    # tick_fig.show()
    # print(tick_data)


if __name__ == '__main__':
    print('Please wait ..')
    init_bot()

    #    if trade_type ==0 :
    #
    #        symbol = "EURUSD"
    #        lot = input('enter your desired lot size: ')
    #        lot = float(Decimal(lot))
    #        point = mt.symbol_info(symbol).point
    #        price = mt.symbol_info_tick(symbol).ask
    #        deviation = 20
    #
    #
    #        print('in the buying condition')
    #        buying_price = mt.symbol_info_tick("EURUSD").ask
    #        print()
    #        stop_loss_input = input('Enter your desired stop loss in unit ie 0.0060 for 60 pips:')
    #        print()
    #        take_profit_input = input('Enter your desired rake profit in unit ie 0.0060 for 60 pips:')
    #        stop_loss = Decimal(buying_price)-Decimal(stop_loss_input)
    #       stop_loss = "{:.5f}".format(stop_loss)
    #       stop_loss = float(stop_loss)
    #       take_profit_calc = Decimal(stop_loss_input)*2
    #        take_profit = Decimal(buying_price)+Decimal(take_profit_calc)
    #        take_profit = "{:.5f}".format(take_profit)
    #        take_profit = float(take_profit)
    #        print('your take profit is: ', take_profit, 'and stop loss is: ', stop_loss, 'and a lot size of: ', lot)
    #
    #
    #       request = {
    #          "action": mt.TRADE_ACTION_DEAL,
    #         "symbol": symbol,
    #            "volume": lot,
    #            "type": mt.ORDER_TYPE_BUY,
    #            "price": price,
    #            "sl": stop_loss,
    #            "tp": take_profit,
    #            "deviation": deviation,
    #            "magic": int(datetime.now().timestamp()),
    #            "comment": "python script open",
    #            "type_time": mt.ORDER_TIME_GTC,
    #            "type_filling": mt.ORDER_FILLING_RETURN,
    #        }
    #
    # send a trading request
    #       result = mt.order_send(request)
    #      print(result)
    #
    #
    #
    #
    #
    #
    #  else:
