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
import time


import json
import sys
from threading import Thread
import sys

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Crazy_bot:
    def __init__(self):
        sys.setrecursionlimit(10000000)
        self.currency = "USDCAD"
        self.balance = 0
        self.profits = 0
        self.pri_stop_loss_price = 0
        self.pri_take_profit_price = 0
        self.lot_size = 0.01
        self.no_of_orders_open = 0
        self.order_type = 0
        self.number_of_orders_completed = 0
        self.secondary_stop_loss_price = 0
        self.primary_buying_price = 0
        self.secondary_trade = 0
        self.secondary_take_profit_price = 0
        self.secondary_type_of_order = 0
        self.primary_order_state = 0
        self.initiate_secondary_first_trade = 1  # cheks whether we should buy/sell secondry trade similar to the pri trade
        self.initiate_secondary_second_trade = 0  # above but for sec trade
        self.similar_to_primary_order = 0
        self.primary_order_type = 0
        self.done_first_order = 0
        self.status_checked = 1

    def initiate_bot(self):
        # Initiates the bot
        login = 6056739
        password = 'Gichengo@254'
        server = 'OANDA-OGM MT5 Demo'
        print('Initializing and login in hold on..')
        print()

        if not mt.initialize(login=login, server=server, password=password):
            print("initialize() failed, error code =", mt.last_error())
            quit()
        print('Meta trader initialized')
        print()
        self.done_first_order = 0
        self.no_of_orders_open = 0
        self.is_pri_order = 0
        self.create_order()

    def calculate_next_move(self):
        account_info = mt.account_info()
        self.balance = account_info.balance
        print("meta trader logged in, your current balance is : ", self.balance)
        print()
        start = input('choose 0 to buy and 1 to sell : ')
        print()
        self.order_type = float(start)
        self.primary_order_type = float(start)
        self.done_first_order += 1
        self.is_pri_order = 0
        self.create_order()

    def check_if_its_pri_order(self):
        self.status_checked = 0
        # check if its a primary order
        if self.primary_order_state == 0:
            price = mt.symbol_info_tick(self.currency).ask
            print("its a pri order...")
            print()
            print("current price is: ", price)
            print()
            
            self.primary_order_state = 1
            self.primary_order_type = self.order_type
            self.primary_buying_price = price
            if self.order_type == 0:
                self.pri_stop_loss_price = float(price - 0.002)
                self.pri_take_profit_price = float(price + 0.006)
            else:
                self.pri_stop_loss_price = float(price + 0.002)
                self.pri_take_profit_price = float(price - 0.006)
                self.create_order()
        else:
            print("Its a secondary order...")
            print()
            self.its_a_secondary_order()

    def its_a_secondary_order(self):
        if self.no_of_orders_open < 2:
            # shows that this is the first secondary order
            price = mt.symbol_info_tick(self.currency).ask
            if self.order_type == 0:
                self.secondary_stop_loss_price = float(0.000)
                self.secondary_take_profit_price = float(price + 0.006)
            else:
                self.secondary_stop_loss_price = float(0.000)
                self.secondary_take_profit_price = float(price - 0.006)
                self.create_order()
        else:
            self.check_whether_is_similar_to_pri_trade()

    def check_whether_is_similar_to_pri_trade(self):
        # check if its a trade similar to the first trade
        if self.similar_to_primary_order == 0:
            print("Order is similar to pri order...")
            print()
            self.secondary_take_profit_price = self.pri_take_profit_price
            self.create_order()
        else:
            print("Order aint similar to Pri Order")
            self.secondary_take_profit_price = self.secondary_take_profit_price
            self.create_order()

    def create_order(self):
        # creating our first order

        if self.done_first_order == 0:
            print()
            self.calculate_next_move()
            print('placing order now')
        else:
            print('the journey has just begun')
        if self.status_checked == 1:
            self.check_if_its_pri_order()
        else:
            self.status_checked = 1 
            self.number_of_orders_completed += 1
            self.no_of_orders_open += 1
            lotage = float(format(self.lot_size, '.2f'))
            print("The orders lotage is : ", lotage, "SL : ", self.pri_stop_loss_price if self.is_pri_order == 0 else float(self.secondary_stop_loss_price),
                  "and TP : ", self.pri_take_profit_price if self.is_pri_order == 0 else self.secondary_take_profit_price)

            order = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.currency,
                "volume": lotage,
                "type": mt5.ORDER_TYPE_BUY if self.order_type == 0 else mt5.ORDER_TYPE_SELL,
                "price": mt.symbol_info_tick(self.currency).ask,
                "sl": self.pri_stop_loss_price if self.is_pri_order == 0 else float(self.secondary_stop_loss_price),
                "tp": self.pri_take_profit_price if self.is_pri_order == 0 else self.secondary_take_profit_price,
                "deviation": 20,
                "magic": int(datetime.now().timestamp()),
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result = mt5.order_send(order)
            # check the execution result
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("4. order_send failed, retcode={}".format(result.retcode))
                print("   result", result)
            else:
                
                print("position #{} closed, {}".format(self.number_of_orders_completed, result))
                print()
                print("Moving to check order state...")
                print()
                self.is_pri_order = 1
            self.check_orders_state()
        #        print("4. position #{} closed, {}".format(self.number_of_orders_completed, result))
                # request the result as a dictionary and display it element by element
     #           result_dict = result._asdict()
      #          for field in result_dict.keys():
       #             print("   {}={}".format(field, result_dict[field]))
                    # if this is a trading request structure, display it element by element as well
       #             if field == "request":
       #                 traderequest_dict = result_dict[field]._asdict()
       #                 for tradereq_filed in traderequest_dict:
       #                     print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
            

    

    def check_orders_state(self):
        time.sleep(0.2)
        # checks whether there is a change in the open orders in mt5 and compares it to the local runing orders
        print("inside the check order state function ..")
        print()
        try:
            print("Inside the get order try loop")
            orders = mt.positions_total()
            if orders <= 0:
                print("No orders found")
                orders = mt.positions_total()
            else:
                print("Your orders are: ", orders)            
        except None as e:
            print("found none trying again")
            orders = mt.orders_get(symbol=self.currency)
            print("Your orders are: ", orders)
        #orders = len(orders)
        if orders < self.no_of_orders_open:
            print("the orders are less, moving to close all open orders ...")
            print()
            self.get_all_open_orders_details()
        else:
            print("going to check if price has changed from the pri order buying price")
            self.check_buying_price()

    def get_all_open_orders_details(self):
        print("inside the closing orders funtion")
        print()
        self.primary_order_state, self.initiate_secondary_second_trade, self.initiate_secondary_first_trade = 0,0,1 
#        if self.primary_order_state == 1:
#            self.primary_order_state -= 1
#        else:
#            pass
#       if self.initiate_secondary_second_trade == 1:
#           self.initiate_secondary_second_trade -= 1
#       else:
#           pass
#       if self.initiate_secondary_first_trade == 0:
#           self.initiate_secondary_first_trade += 1
#       else:
#           pass
        self.lot_size=0.01
        # this will get all the open order details and close them all
        

        positions = mt.positions_get(symbol=self.currency)
        if positions == None:
            print("No positions on",self.currency, "error code={}".format(mt5.last_error()))
        elif len(positions) > 0:
            print("Total positions on ",self.currency,"= : ", len(positions))
                # display all open positions
            for position in positions:
                print("going to the close order funtion now for position: ")
                self.close_orders(positions, position)
                
           
            self.initiate_secondary_first_trade = 1
            self.primary_order_type = 0
            # starting the process and sending mail with profit details
            print("starting the threading process")
            t1 = Thread(target=self.create_order())
            t2 = Thread(target=self.send_mail())
            t1.start()
            t2.start()
            
            
            

        else:
            mt.shutdown()
            quit()
            print("Orders not found")
    def close_orders(self, positions, position):
        print("inside closing position funtion")
        lst = list(positions)
        position_id = position[0]  # get the ticket number
        symbol = position[16]
        action = position[5]
        lot = position[9]
        deviation = 20
        ea_magic_number = position[6]
        sl = position[11]
        tp = position[12]
        mt.Close(symbol=symbol, ticket= position_id)
        print("Closing position with ticket number :", position_id, "ea_magic_number : ", ea_magic_number)
        print(position)
        if(action == 0):
            print("ORDER OF SALE - CLOSING")
            price = mt.symbol_info_tick(symbol).bid
           
        else:
            print("PURCHASE ORDER - CLOSING")
            price = mt.symbol_info_tick(symbol).ask
        
            # check the execution result
        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.currency,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL if action == 0 else mt5.ORDER_TYPE_BUY,
            "position": position_id,
            "price": mt.symbol_info_tick(self.currency).bid if action == 0 else mt.symbol_info_tick(self.currency).ask,
           # "sl": float(sl),
           # "tp": float(tp),
            "deviation": 20,
            "magic": ea_magic_number,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(order)
            
        print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,dict));
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(" order_send failed")
            print("   result",result)
            mt.shutdown()
            quit()
        else:
            print("4. position #{} closed, {}".format(position_id,result))
        
        

    def send_mail(self):
        print("sending mail")
        account_info = mt.account_info()
        new_balance = account_info.balance
        profit = new_balance - self.balance
        self.profits += profit

        
        port = 587
        smtp_server = "smtp.gmail.com"
        sender_email = "academicdons@gmail.com"
        receiver_email = "gichengo.wangui29@gmail.com"
        password = "Academicdons@254"
        message = """\
                    Subject: Hi there
                    How are you?
                   The bot has closed several orders with a profit of """, profit, """
                The account balance is now """, self.balance, """"
                    This message is sent from Python."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

        
        print("mail sent")



    def check_buying_price(self):
        print("WE are now checking price deviation with reference to the original buying price")
        print()
        try:
            print("Inside the get price try loop")
            price = mt.symbol_info_tick(self.currency).ask
        except None as e:
            print("found none trying again")
            price = mt.symbol_info_tick(self.currency).ask
            print("Your orders are: ", orders)
        print("current price is:", price)


        if self.primary_order_type == 0:
            if price > self.primary_buying_price:
                print()
                print("Primary order is a buy order and the price is above primary buying price")
                print()
                print("proceeding to check_sec_primary_trade_true")
                self.check_sec_primary_trade_true(price)
            elif price < self.primary_buying_price:
                print("Primary order is a buy order and the price is below primary buying price")
                print()
                print("proceeding to check_if_its_passed_primary_SL")
                self.check_if_its_passed_primary_SL(price)
            else:
                self.check_orders_state()
        else:
            if price < self.primary_buying_price:
                print("Primary order is a sell order and the price is below primary buying price")
                print()
                print("proceeding to check_sec_primary_trade_true")
                self.check_sec_primary_trade_true(price)
            elif price > self.primary_buying_price:
                print("Primary order is a sell order and the price is above primary buying price")
                print()
                print("proceeding to check_if_its_passed_primary_SL")
                self.check_if_its_passed_primary_SL(price)
            else:
                self.check_orders_state()

    def check_sec_primary_trade_true(self, price):
        if self.initiate_secondary_first_trade == 0:
            self.initiate_secondary_first_trade, self.initiate_secondary_second_trade, self.similar_to_primary_order  = 1,0,0
            
            if self.order_type == 0:
                self.order_type += 1
            else:
                self.order_type -= 1
            print("Secondary Pri Trade is true.. Proceeding to place it..")
            lot = self.lot_size
            self.lot_size = lot * float(1.5)
            self.create_order()
        else:
            print("Secondary Pri trading is false proceeding to check order state")
            self.check_orders_state()

    def check_if_its_passed_primary_SL(self, price):
        print()
        print("In the check_if_its_passed_primary_SL funtion")
        if self.primary_order_type == 0:
            # checks the type of our primary order
            if price < self.pri_stop_loss_price:
                print()
                print("Pri order is Buy and price is below pri SL price")
                print()
                self.initiate_secondary_first_trade = 0
                
                self.similar_to_primary_order = 0
                
                
                self.order_type = 1
                
                lot = self.lot_size
                self.lot_size = lot * float(1.5)
                print("changed lot size to: ", self.lot_size, "and creating a new order")
                print()
                self.create_order()
            else:
                print("Pri order is Buy and price is above pri SL price.. proceeding to check_orders_state")
                self.check_orders_state()
        else:
            if price > self.pri_stop_loss_price:
                self.initiate_secondary_first_trade =0
                print("Pri order is Sell and price is above pri SL price")
                print()
                
                self.similar_to_primary_order = 1
                
                self.initiate_secondary_second_trade = 1
                
                
                self.order_type =0
                
                lot = self.lot_size
                self.lot_size = lot * float(1.5)
                print("changed lot size to: ", self.lot_size, "and creating a new order")
                self.create_order()
            else:
                print("Pri order is Sell and price is below pri SL price.. proceeding to check_orders_state")
                self.check_orders_state()


if __name__ == '__main__':
    print('Please wait ..')
    ed = Crazy_bot()
    ed.initiate_bot()
