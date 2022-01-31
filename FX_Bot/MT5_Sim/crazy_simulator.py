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

import json
import sys
from threading import Thread


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Crazy_bot:
    def __init__(self):
        self.currency = "USDCAD"
        self.balance = 0
        self.profits = 0
        self.pri_stop_loss_price = 0
        self.pri_take_profit_price = 0
        self.lot_size = 0.01
        self.no_of_orders_open = 0
        self.order_type = 0
        self.number_of_orders_completed = 0
        self.primary_buying_price = 0
        self.secondary_trade = 0
        self.secondary_take_profit_price = 0
        self.secondary_type_of_order = 0
        self.primary_order_state = 0
        self.initiate_secondary_first_trade = 0  # cheks whether we should buy/sell secondry trade similar to the pri trade
        self.initiate_secondary_second_trade = 0  # above but for sec trade
        self.similar_to_primary_order = 0
        self.primary_order_type = 0
        self.done_first_order = 0

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
        self.create_order()

    def calculate_next_move(self):
        account_info = mt.account_info()
        self.balance = account_info.balance
        start = input('choose 0 to buy and 1 to sell : ')
        print()
        self.order_type = float(start)
        self.done_first_order += 1
        self.create_order()

    def check_if_its_pri_order(self):
        # check if its a primary order
        if self.primary_order_state == 0:
            price = mt.symbol_info_tick(self.currency).ask
            self.primary_buying_price = price
            if self.order_type == 0:
                self.pri_stop_loss_price = float(price - 0.002)
                self.pri_take_profit_price = float(price + 0.006)
                if self.primary_order_type == 1:
                    self.primary_order_type -= 1
                else:
                    pass

            else:
                self.pri_stop_loss_price = float(price + 0.002)
                self.pri_take_profit_price = float(price - 0.006)
                if self.primary_order_type == 0:
                    self.primary_order_type += 1
                else:
                    pass
                self.create_order()
        else:
            self.its_a_secondary_order()

    def its_a_secondary_order(self):
        if self.no_of_orders_open < 2:
            # shows that this is the first secondary order
            price = mt.symbol_info_tick(self.currency).ask
            if self.order_type == 0:
                self.secondary_take_profit_price = float(price - 0.002)
                self.secondary_take_profit_price = float(price + 0.006)
            else:
                self.secondary_take_profit_price = float(price + 0.002)
                self.secondary_take_profit_price = float(price - 0.006)
                self.create_order()
        else:
            self.check_whether_is_similar_to_pri_trade()

    def check_whether_is_similar_to_pri_trade(self):
        # check if its a trade similar to the first trade
        if self.similar_to_primary_order == 0:
            self.secondary_take_profit_price = self.pri_take_profit_price
            self.create_order()
        else:
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

        self.number_of_orders_completed += 1
        self.no_of_orders_open += 1
        lotage = float(format(self.lot_size, '.2f'))

        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.currency,
            "volume": lotage,
            "type": mt5.ORDER_TYPE_BUY if self.order_type == 0 else mt5.ORDER_TYPE_SELL,
            "price": mt.symbol_info_tick(self.currency).ask,
            # "sl": self.stop_loss_price,
            "tp": self.pri_take_profit_price if self.primary_order_state == 0 else self.secondary_take_profit_price,
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
            print("4. position #{} closed, {}".format(self.number_of_orders_completed, result))
            # request the result as a dictionary and display it element by element
            result_dict = result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # if this is a trading request structure, display it element by element as well
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
        self.check_orders_state()

    def check_orders_state(self):
        # checks whether there is a change in the open orders in mt5 and compares it to the local runing orders
        orders = mt.orders_get()
        orders = len(orders)
        if orders < self.no_of_orders_open:
            self.get_all_open_orders_details()
        else:
            self.check_buying_price()

    def get_all_open_orders_details(self):
        if self.primary_order_state == 1:
            self.primary_order_state -= 1
        else:
            pass
        if self.initiate_secondary_second_trade == 1:
            self.initiate_secondary_second_trade -= 1
        else:
            pass
        if self.initiate_secondary_first_trade == 0:
            self.initiate_secondary_first_trade += 1
        else:
            pass
        self.lot_size=0
        # this will get all the open order details and close them all
        orders = mt.orders_total()
        if orders > 0:
            print("Total orders=", orders)
            symbol = self.currency
            symbol_info = mt.symbol_info(symbol)

            positions = mt.positions_get(symbol=symbol)
            if positions == None:
                print("No positions on",self.currency, "error code={}".format(mt5.last_error()))
            elif len(positions) > 0:
                print("Total positions on ",self.currency,"= : ", len(positions))
                # display all open positions
                for position in positions:
                    print(position)
                    lst = list(positions)
                    ticket_no = lst[0][0]  # get the ticket number
                    mt.Close(symbol, ticket= ticket_no)

                # starting the process and sending mail with profit details
                t1 = Thread(target=self.create_order())
                t2 = Thread(target=self.send_mail())
                t1.start()
                t2.start()
        else:
            mt.shutdown()
            quit()
            print("Orders not found")

    def send_mail(self):

        account_info = mt.account_info()
        new_balance = account_info.balance
        profit = new_balance - self.balance
        self.profits += profit

        sender_email = "academicdons@gmail.com"
        receiver_email = "gichengo.wangui29@gmail.com"
        password = "Academicdons@254"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Profit Report"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message

        html = """\
        <html>
          <body>
            <p>Hi,<br>
               How are you?<br>
               The bot has closed several orders with a profit of """, profit, """
                The account balance is now """, self.balance, """"
            </p>
          </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        print("mail sent")



    def check_buying_price(self):
        price = mt.symbol_info_tick(self.currency).ask

        if self.primary_order_type == 0:
            if price > self.primary_buying_price:
                self.check_sec_primary_trade_true(price)
            elif price < self.primary_buying_price:
                self.check_if_its_passed_primary_SL(price)
            else:
                self.check_orders_state()
        else:
            if price < self.primary_buying_price:
                self.check_sec_primary_trade_true(price)
            elif price > self.primary_buying_price:
                self.check_if_its_passed_primary_SL(price)
            else:
                self.check_orders_state()

    def check_sec_primary_trade_true(self, price):
        if self.initiate_secondary_first_trade == 0:

            if self.initiate_secondary_first_trade == 0:
                self.initiate_secondary_first_trade += 1
            else:
                pass
            if self.initiate_secondary_second_trade == 1:
                self.initiate_secondary_second_trade -= 1
            else:
                pass
            if self.similar_to_primary_order == 1:
                self.similar_to_primary_order -= 1
            else:
                pass
            if self.order_type == 0:
                self.order_type += 1
            else:
                self.order_type -= 1
            lot = self.lot_size
            self.lot_size = lot * 1.5
            self.create_order()
        else:
            self.check_orders_state()

    def check_if_its_passed_primary_SL(self, price):

        if self.primary_order_type == 0:
            # checks the type of our primary order
            if price < self.pri_stop_loss_price:
                if self.initiate_secondary_first_trade == 1:
                    self.initiate_secondary_first_trade -= 1
                else:
                    pass
                if self.similar_to_primary_order == 0:
                    self.similar_to_primary_order += 1
                else:
                    pass
                if self.initiate_secondary_second_trade == 0:
                    self.initiate_secondary_second_trade += 1
                else:
                    pass
                if self.order_type == 0:
                    self.order_type += 1
                else:
                    pass
                lot = self.lot_size
                self.lot_size = lot * 1.5
                self.create_order()
            else:
                self.check_orders_state()
        else:
            if price > self.pri_stop_loss_price:
                if self.initiate_secondary_first_trade == 1:
                    self.initiate_secondary_first_trade -= 1
                else:
                    pass
                if self.similar_to_primary_order == 0:
                    self.similar_to_primary_order += 1
                else:
                    pass
                if self.initiate_secondary_second_trade == 0:
                    self.initiate_secondary_second_trade += 1
                else:
                    pass
                if self.order_type == 1:
                    self.order_type -= 1
                else:
                    pass
                lot = self.lot_size
                self.lot_size = lot * 1.5
                self.create_order()
            else:
                self.check_orders_state()


if __name__ == '__main__':
    print('Please wait ..')
    ed = Crazy_bot()
    ed.initiate_bot()
