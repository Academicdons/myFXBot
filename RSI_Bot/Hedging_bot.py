import MetaTrader5 as mt
import MetaTrader5 as mt5
import pandas as pd
import plotly.express as px
from datetime import *
import threading
from time import *
from decimal import *
import time
from moving_average import Indicator


# make sure the trade server is enabled in MT% terminal
#trade type o for buying 1 for selling
trade_type = 0
no_of_orders = 0
currency = ["USD"]
tp = 0
sl = 0
order_id = 0
position = 0

def check_order_state():
    global no_of_orders
    global currency
    global tp
    global sl
    global trade_type
    global position
    currency = currency
    
    orders = mt.orders_get()
    orders = len(orders)
    print('we have ', orders, 'running')
    no_of_orders = no_of_orders
    
    if orders>0:
        print('order', no_of_orders, "is still running")
        check_order_state()
        
    else:
        print('order', no_of_orders, "completed successfully")
        position -= 1
        last = mt.positions_get(position = position)
        position += 1
        print(last)
        
        
        

    

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
    no_of_orders = no_of_orders
    symbol = "EURUSD"
    if no_of_orders ==0 :
        print()
        type_input = input('select trade to state 0 for buying and 1 for selling: ')
        trade_type = int(type_input)
        print('placing order now')
        no_of_orders+=1
    else:
        no_of_orders+=1
        print('an order found')
        pass    


        
    TAKEPROFIT = input('enter your desired Take Profit size in points ie 100: ')
    TAKEPROFIT = float(TAKEPROFIT)
    tp = TAKEPROFIT
    print()
    STOPLOSS =  input('enter your desired Stop Loss size in points ie 50: ')
    STOPLOSS = float(STOPLOSS)
    sl = STOPLOSS
    market = "EURUSD"
    print()
    lotage = input('enter your desired lot size where 0.01 equals $1000: ')
    lotage = float(lotage)

    
    trade_type = trade_type

    
    point = mt5.symbol_info(market).point
    price = mt5.symbol_info_tick(market).ask

    if trade_type ==0 :
        print('its a buy order')
        sl = price - STOPLOSS * point
        tp = price + TAKEPROFIT * point
    else:
        print("Its a sell order")
        sl = price + STOPLOSS * point
        tp = price - TAKEPROFIT * point
    print('Your sl and tp are :', sl ,'and', tp)

    deviation = 20
    position = position
       
    operation = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": market,
        "volume": lotage,
        "type": mt5.ORDER_TYPE_BUY if trade_type ==0 else mt5.ORDER_TYPE_SELL,
        "price": price,
        "position": position, 
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
    print(result[2])
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
    path = "C:\Program Files\MetaTrader 5\terminal64.exe" #path of terminal64.exe

    selling_price = 0
    buying_price = 0
        
    login = 6056739
    password = 'Gichengo@254'
    server = 'OANDA-OGM MT5 Demo'
    print("""

                                                                                                                                                                            
                                                                                                                                                                            
        FFFFFFFFFFFFFFFFFFFFFF                                                                                  BBBBBBBBBBBBBBBBB                             tttt          
        F::::::::::::::::::::F                                                                                  B::::::::::::::::B                         ttt:::t          
        F::::::::::::::::::::F                                                                                  B::::::BBBBBB:::::B                        t:::::t          
        FF::::::FFFFFFFFF::::F                                                                                  BB:::::B     B:::::B                       t:::::t          
          F:::::F       FFFFFF   ooooooooooo   rrrrr   rrrrrrrrr       eeeeeeeeeeee    xxxxxxx      xxxxxxx       B::::B     B:::::B   ooooooooooo   ttttttt:::::ttttttt    
          F:::::F              oo:::::::::::oo r::::rrr:::::::::r    ee::::::::::::ee   x:::::x    x:::::x        B::::B     B:::::B oo:::::::::::oo t:::::::::::::::::t    
          F::::::FFFFFFFFFF   o:::::::::::::::or:::::::::::::::::r  e::::::eeeee:::::ee  x:::::x  x:::::x         B::::BBBBBB:::::B o:::::::::::::::ot:::::::::::::::::t    
          F:::::::::::::::F   o:::::ooooo:::::orr::::::rrrrr::::::re::::::e     e:::::e   x:::::xx:::::x          B:::::::::::::BB  o:::::ooooo:::::otttttt:::::::tttttt    
          F:::::::::::::::F   o::::o     o::::o r:::::r     r:::::re:::::::eeeee::::::e    x::::::::::x           B::::BBBBBB:::::B o::::o     o::::o      t:::::t          
          F::::::FFFFFFFFFF   o::::o     o::::o r:::::r     rrrrrrre:::::::::::::::::e      x::::::::x            B::::B     B:::::Bo::::o     o::::o      t:::::t          
          F:::::F             o::::o     o::::o r:::::r            e::::::eeeeeeeeeee       x::::::::x            B::::B     B:::::Bo::::o     o::::o      t:::::t          
          F:::::F             o::::o     o::::o r:::::r            e:::::::e               x::::::::::x           B::::B     B:::::Bo::::o     o::::o      t:::::t    tttttt
        FF:::::::FF           o:::::ooooo:::::o r:::::r            e::::::::e             x:::::xx:::::x        BB:::::BBBBBB::::::Bo:::::ooooo:::::o      t::::::tttt:::::t
        F::::::::FF           o:::::::::::::::o r:::::r             e::::::::eeeeeeee    x:::::x  x:::::x       B:::::::::::::::::B o:::::::::::::::o      tt::::::::::::::t
        F::::::::FF            oo:::::::::::oo  r:::::r              ee:::::::::::::e   x:::::x    x:::::x      B::::::::::::::::B   oo:::::::::::oo         tt:::::::::::tt
        FFFFFFFFFFF              ooooooooooo    rrrrrrr                eeeeeeeeeeeeee  xxxxxxx      xxxxxxx     BBBBBBBBBBBBBBBBB      ooooooooooo             ttttttttttt  
                                                                                                                                                                                                                                                                                                            

        """)
    print('Initializing and login in hold on..')
    print()

    if not mt.initialize(login=login, server=server, password=password):
        print("initialize() failed, error code =", mt.last_error())
        quit()
    print('Meta trader initialized')
    time.sleep(2)
    place_an_order()
        

    def acc_info():
        # get all account info

        account_info = mt.account_info()

        # getting specific account data
        balance = account_info.balance
        login_number = account_info.login
        equity = account_info.equity


        # get number of symbols with symbols tools

        nump_symbols = mt.symbols_total()

        # get all symbols and specofocations
        # symbols = mt.symbols_get()


        # get all symbols and their specification ie EUR/USD

        symbol_info = mt.symbol_info("EURUSD")._asdict()


        # get current symbol price

        symbol_price = mt.symbol_info_tick("EURUSD")._asdict()
        symbol_price
        print()
        print("current symbole price is:", symbol_price)

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
