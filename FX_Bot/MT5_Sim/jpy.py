from json import loads
import os
import pickle
from collections import OrderedDict
import pandas as pd
import re
from Hedging_simulator import *

#def tick_ohcl():
#    filename = 'ohcl_data.json'
#    if not os.path.exists(filename):
#        return False
#    dbfile = open('data_file', 'rb')
#    db = pickle.load(dbfile)
#    closes = db['close']
#    return closes
#    for close in closes:
#       print(close)
        
#def time_ohcl():
 #   filename = 'ohcl_data.json'
 #   if not os.path.exists(filename):
 #       return False
 #   dbfile = open('data_file', 'rb')
 #   db = pickle.load(dbfile)
 #   time = db['time']
 #  for time in closes:
 #       print(time)
def orders():
    dbfile = open('orders_data', 'rb')
    db = pickle.load(dbfile)
    lossess = db
    df = pd.DataFrame(db)
    for col in df:
       print(df.order.SL)
       
orders()
                    


