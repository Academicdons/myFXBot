from typing import List, Tuple, Dict, Any, Optional

import os
import pickle
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import MetaTrader5 as mt
import MetaTrader5 as mt5
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import jmespath
import json
import sys


class Hedging_simulator:

   def __init__(self):

       self.unit = 'USD'
       self.balance = float(balance)
       self.equity = balance
       self.margin = margin
       self.leverage = leverage
       self.symbol = symbol
       self.identity = 0

   def balance_change(selfs, balance):
       balance = balance

       db = {}
       db['balance'] = balance

       dbfile = open('balance_change', 'wb')

       pickle.dump(db, dbfile)
       dbfile.close()
       
   def balance_change_get(self):
       dbfile = open('balance_change', 'wb')
       dbfile = open('balance_change', 'rb')

       db = pickle.load(dbfile)
       balances = db
       return balances

   def add_profits(self, profit):
       profit = profit

       db = {}
       db['profit'] = profit

       dbfile = open('profit_data', 'ab')

       pickle.dump(db, dbfile)
       dbfile.close()

   def get_profits(self):
       dbfile = open('profit_data', 'wb')
       dbfile = open('profit_data', 'rb')
       db = pickle.load(dbfile)
       profits = db
       return profits
   def add_loss(self, loss):
       loss = loss

       db = {}
       db['loss'] = loss

       dbfile = open('loss_data', 'ab')

       pickle.dump(db, dbfile)
       dbfile.close()

   def get_losses(self):
       dbfile = open('loss_data', 'rb')
       db = pickle.load(dbfile)
       lossess = db
       return lossess


   def save_order(self, order):
       order = order

       db = {}
       db['order'] = order

       dbfile = open('orders_data', 'wb')

       pickle.dump(db, dbfile)
       dbfile.close()


   def orders(self):
       dbfile = open('orders_data', 'rb')
       db = pickle.load(dbfile)
       lossess = db
       return lossess

   def download_data(self):
       print("Downloading ohcl data now. Please wait...")
       global time_frame
       time_frame = time_frame
       data = pd.DataFrame(mt.copy_rates_range(self.symbol, time_frame, datetime(2022, 1, 1), datetime.now()))
       data['time'] = pd.to_datetime(data['time'], unit='s')
       time = data['time']
       print(data['close'])
       close = data['close']

       db = {}
       db['time'] = time
       db['close'] = close

       dbfile = open('data_file', 'ab')

       pickle.dump(db, dbfile)
       dbfile.close()

   def tick_ohcl(self):

       dbfile = open('data_file', 'rb')
       db = pickle.load(dbfile)
       closes = db['close']
       return closes

   def download_datas(self):
       print("Downloading ohcl data now. Please wait...")
       global time_frame
       time_frame = time_frame
       data = mt.copy_rates_range(self.symbol, time_frame, datetime(2022, 1, 1), datetime.now())
       print(data)
       print("Done Downloading saving the data now ..")
       data = pd.DataFrame(data)
       data = data.to_json(indent=2)
       data = '\'' + str(data) + '\''
       print(data)
       self.add_ohcl_data(data)
       print("Done Downloading and saving the ohcl data..")
       return data

   def create_order(self, entry_time, entry_price, exit_time,
                    exit_price, state
                    ):

       global identity
       global order_type
       global STOPLOSS
       global price
       global TAKEPROFIT

       if self.identity == 0:
           print()
           print('placing order now your first order now')
           self.identity += 1
       else:
           self.identity += 1

           pass

       Takeprofit = 0

       Stoploss = 0
       order_type = order_type

       point = mt.symbol_info(self.symbol).point
       print("point is: ", point)
       print('price is:', price)

       if order_type == 0:
           print('its a buy order')
           sl = float(price) - float(0.000300)
           tp = float(price) + float(0.00055)
       else:
           print("Its a sell order")
           sl = float(price) + float(0.00030)
           tp = float(price) - float(0.00055)
       print('Your sl and tp are :', sl, 'and', tp)

       order = {
           "id": identity,
           "type": order_type,
           "symbol": self.symbol,
           "volume": self.leverage,
           "entry_time": entry_price,
           "entry_price": price,
           "exit_time": exit_time,
           "exit_price": exit_price,
           "TP": tp,
           "SL": sl,
           "order_state": state,

       }
       print(order)
       self.save_order(order)
       self.loop_through_ohcl()

   def place_first_order(self):
       global order_type
       global price
       self.identity += 1
       self.download_data()
        

       order_type = order_type

       order_type = input('Open your simulation with: 0 for buy and 1 for sell : ')
       print("You chose,: ", order_type, "as your order opening type")

        
       dbfile = open('data_file', 'rb')
       db = pickle.load(dbfile)
       closes = db['close']
       closes.iloc[::-1]

       price = closes[0]
       price = price
       print("Order starting price is :", price)
       entry_time = datetime.now()

       #       print("the last order was on: ", date_last, "with a price of", price)
       entry_price = price
       exit_time = "N/A"
       exit_price = "N/A"
       state = "open"
       #        print('you are starting with a price of:', price)
       print("going to create your first order")
       self.create_order( entry_price, entry_time, exit_price, exit_time, state)

   def loop_through_ohcl(self):
       global order_type
       print("processing the data")
       
       dbfile = open('data_file', 'rb')
       db = pickle.load(dbfile)
       closes = db['close']
       closes = closes.iloc[::-1]
       data_set = closes
       for data in data_set:
           self.check_order_state(data)
       else:
           print('Finished the simulation')
           self.finish_simulation()

   def check_order_state(self, data):
       global order_type

        
       dbfile = open('orders_data', 'rb')
       db = pickle.load(dbfile)
       last_order = db
       take_profit = last_order['TP']
       stop_loss = last_order['SL']
       price = int(data['close'])
       time = data['time']
       entry_price = last_order['entry_price']

       if order_type == 0:
           print('its a buy order')
           if price > take_profit:
               difference = take_profit - entry_price
               self.calculate_profit(last_order, difference, time, price)
           elif price < stop_loss:
               difference = stop_loss - entry_price
               self.calculate_loss(last_order, difference, time, price)
           else:
               pass

       else:
           print("Its a sell order")
           if price < take_profit:
               difference = take_profit - entry_price
               self.calculate_profit(last_order, difference, time, price)
           elif price > stop_loss:
               difference = stop_loss - entry_price
               self.calculate_loss(last_order, difference, time, price)
           else:
               pass

   def calculate_profit(self, last_order, difference, time, price):
       if self.balance == 0:
           print()
           sys.exit('your balance has been depleted')
       else:
           leverage = self.balance * self.leverage
           profit = difference * leverage
           self.balance = self.balance + profit
           self.add_profit(profit)
           self.update_last_order(self, last_order, time, price)

   def calculate_loss(self, last_order, difference, time, price):
       global order_type

       if self.balance == 0:
           print()
           sys.exit('your balance has been depleted')
       else:
           leverage = self.balance * self.leverage
           loss = difference * leverage
           self.balance = self.balance - loss
           self.add_loss(loss)
           self.update_last_order(self, last_order, time, price)

           if order_type == 0:
               order_type += 1
           else:
               order_type -= 1

   def update_last_order(self, last_order, time, price):
       dbfile = open('orders_data', 'rb')
       db = pickle.load(dbfile)
       last_order = db
       take_profit = last_order['TP']
       stop_loss = last_order['SL']
       id = last_order['id']
       type = last_order['type']
       volume = last_order['volume']
       entry_time = last_order['entry_time']
       entry_price = last_order['entry_price']
       exit_time = datetime.now()
       order_state = "Completed"
       orders.remove(last_order)
       order = {
           "id": id,
           "type": type,
           "symbol": self.symbol,
           "volume": volume,
           "entry_time": entry_time,
           "entry_price": entry_price,
           "exit_time": exit_time,
           "exit_price": price,
           "TP": take_profit,
           "SL": stop_loss,
           "order_state": order_state,

       }
       self.save_order(order)

       balance = {
           'Account_balance': self.balance,
           'time': time
       }
       self.balance_change(balance)
       entry_time = exit_time
       entry_price = price

       self.create_order_inside_a_loop(entry_time, entry_price)

   def create_order_inside_a_loop(self, entry_time, entry_price
                                  ):

       global identity
       global order_type
       global STOPLOSS
       global TAKEPROFIT

       if self.identity == 0:
           print()
           self.place_first_order()
           print('placing order now')
           self.identity += 1
       else:
           self.identity += 1
           pass

       Takeprofit = TAKEPROFIT

       Stoploss = STOPLOSS
       order_type = order_type

       point = 0.00001

       if order_type == 0:
           sl = entry_price - str(0.0003)
           tp = entry_price + str(0.0005)
       else:
           sl = entry_price + str(0.0003)
           tp = entry_price - str(0.0005)
       print('Your sl and tp are :', sl, 'and', tp)

       order = {
           "id": identity,
           "type": order_type,
           "symbol": self.symbol,
           "volume": self.leverage,
           "entry_time": entry_time,
           "entry_price": entry_price,
           "exit_time": "N/A",
           "exit_price": "N/A",
           "TP": Takeprofit,
           "SL": Stoploss,
           "order_state": "Open",

       }
       self.save_order(order)
       self.loop_through_ohcl()

   def create_graph(self):
       balances = self.balance_change_get()

       dbfile = open('data_file', 'rb')
       db = pickle.load(dbfile)
       closes = db['close']
       closes = closes.iloc[::-1]


       dbfile = open('data_file', 'rb')
       db = pickle.load(dbfile)
       time = db['time']
       time = time.iloc[::-1]

       # Create figure with secondary y-axis
       fig = make_subplots(specs=[[{"secondary_y": True}]])

       # Add traces
       fig.add_trace(
           go.Scatter(balances, x=balances['time'], y=int(balances['Account_balance']), name="Balance change"),
           secondary_y=False,
       )

       fig.add_trace(
           go.Scatter(ohcl_data, x=time, y=closes, name="Price change"),
           secondary_y=True,
       )

       # Add figure title
       fig.update_layout(
           title_text="Graph comparing balance with Price Movement"
       )

       # Set x-axis title
       fig.update_xaxes(title_text="time")

       # Set y-axes titles
       fig.update_yaxes(title_text="<b>Balances</b> change", secondary_y=False)
       fig.update_yaxes(title_text="<b>Price</b> change", secondary_y=True)

       fig.show()

   def finish_simulation(self):
       print('Getting the statistics ready')
       balance = self.balance

       # we will now get all the statistics
       orders = self.orders()
       orders_count = len(orders)
       print(" Your Account balance is now :", balance, " After completing :", orders_count, "orders.")
       print()

       profits = self.get_profits()
       profits_count = len(profits)
       largest_profit = max(profits)
       total_profits = sum(profits)
       print("The simulator managed to get :", profits_count, "profitable trades.", )
       print("The most profitable trade made: $", largest_profit, "with all profits adding up to: $", total_profits)

       losses = self.get_losses()
       losses_count = len(losses)
       largest_loss = max(losses)
       total_losses = sum(losses)
       print()
       print("However, the simulator also made :", losses_count)
       print("The biggest loss was: $", largest_loss, "adding up all the lossess to a total of: $", total_losses)
       print()

       success_rate = (profits_count / orders_count) * 100
       fail_rate = (losses_count / orders_count) * 100
       print("The simulator's has a fail rate of: ", fail_rate, "%", "and a success rate of: ", success_rate, "%")
       selection = input("Do You want a graph generated for you 1 for Yes and 2 for NO?")
       if selection == 2:
           pass
       elif selection == 1:
           self.create_graph()
       else:
           print("We are generating a graph coz you don't seem to know what you want, moron!!!")
           self.create_graph()

   def init_bot(self):
       global time_frame

       path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"  # path of terminal64.exe

       login = 6056739
       password = 'Gichengo@254'
       server = 'OANDA-OGM MT5 Demo'

       if not mt.initialize(path, login=login, server=server, password=password):
           print("initialize() failed, error code =", mt.last_error())
           quit()
       print('Meta trader initialized')
       print()

       #       print("Example to use below:")
       #       print(" ie 1 for M1,2 for M5,3 for M15,4 for M30, 5 for H1,6 for H4,7 for D1,8 for W1, and 9 for MN")
       #       time_frame = input('select the timeframe you want to trade in, USE THE EXAMPLE ABOVE OR THE CODE WILL FAIL : ')
       #       print()
       #       print("You have choosen :", time_frame, "time frame")
       #       if time_frame ==1:
       #           time_frame = mt.TIMEFRAME_M1
       #       elif time_frame == 2:
       #           time_frame = mt.TIMEFRAME_M5
       #       elif time_frame == 3 :
       #           time_frame = mt.TIMEFRAME_M15
       #       elif time_frame == 4:
       #           time_frame = mt.TIMEFRAME_M30
       #       elif time_frame == 5 :
       #           time_frame = mt.TIMEFRAME_H1
       #       elif time_frame == 6:
       #           time_frame = mt.TIMEFRAME_H4
       #       elif time_frame == 7 :
       #           time_frame = mt.TIMEFRAME_D1
       #       elif time_frame == 8:
       #           time_frame = mt.TIMEFRAME_W1
       #       elif time_frame == 9 :
       #           time_frame = mt.TIMEFRAME_MN
       #       else:
       #           print("You Moron")
       #          sys.exit('Start again...')
       time_frame = mt.TIMEFRAME_D1
       self.place_first_order()

       print()


if __name__ == '__main__':
   print('Please wait ..')
   balance = float(input('Select your prefered balance: '))
   print()
   leverage = float(input('select your Leverage to use: '))
   print()

   symbol = input('select the currency pair you want to trade in: ')
   print()

   #    from_date = input('select the date you want to start your simulation in ie 2022, 1, 1: ')
   from_date = datetime(2022, 2, 1)
#   print()
 #  TAKEPROFIT = input('enter your desired Take Profit size in points ie 50 for 0.0005: ')
# TAKEPROFIT = float(TAKEPROFIT)
 #  print()
  # STOPLOSS = input('enter your desired Stop Loss size in points ie 50 for 0.0005: ')
  # STOPLOSS = float(STOPLOSS)
   #print()
   identity = 0
   print()
   price = 0
   order_type = 0
   margin = input('enter your desired margin : ')
   print()

   ed = Hedging_simulator()
   ed.init_bot()




