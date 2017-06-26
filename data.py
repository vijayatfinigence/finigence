# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 07:02:54 2017

@author: vijayp

get the data and returns the data
Source of data supported: mysql, csv, yahoo.
1-ticker at a time
Volatility: csv's
stocks/etf's: Yahoo
custom: mysql
bigdata store:?
"""

import pandas as pd
from pandas_datareader import data as web
from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://root:root@localhost/finigence')
#data_folder = r'C:\Users\vijayp\Documents\Python Scripts\finigence\data\\'
#monthly_data_folder = r'C:\Users\vijayp\Documents\Python Scripts\finigence\data\monthly\\'
#weekly_data_folder = r'C:\Users\vijayp\Documents\Python Scripts\finigence\data\weekly\\'

  

def load_data(data_folder,file,source,ticker,start,end):
    """  Loads data from different sources.
    Volatility from CSV's and returns the frames.
    ETF/stocks  from Yahoo
    """
    data = pd.DataFrame()
    adjust_close=False
    if source=="csv":       
       data = pd.read_csv(data_folder+file+".csv",header=0,infer_datetime_format=True, parse_dates=[0],keep_date_col=True)  
       if (start!="") and (end!=""):
           data = data[ (data['Date']>=start) & (data['Date']<=end) ]
       if (start=="") and (end!=""):
          data = data[data['Date']<=end]
       if (start!="") and (end==""):
          data = data[data['Date']>=start]          
       #data.set_index(data['Date'],drop=True,inplace=True,verify_integrity=True)
       #data.drop(['Date'],axis=1,inplace=True)
       #data.drop('Date',axis=1,inplace=True)
       return data
    elif source=="yahoo":
         """ Loads data from Yahoo. After loading it renames columns to shorter
         format, which is what Backtest expects.
         Set `adjust close` to True to correct all fields with with divident info
         provided by Yahoo via Adj Close field.
         Defaults are in place for convenience. """        
         if isinstance(ticker, list):
            return pd.Panel({t: load_from_yahoo(ticker=t, start=start, adjust_close=adjust_close)
            for t in ticker})
         data = web.DataReader(ticker, data_source='yahoo', start=start)
         r = data['Adj Close'] / data['Close']       
         return data



        
        

def get_closing_price(ticker,start):
    """  Loads data from different sources.
    Volatility from CSV's and returns the frames.
    ETF/stocks  from Yahoo
    """    
    if isinstance(start,pd.Series):
       prices=pd.Series()
       #return pd.Series({t: get_closing_price(ticker=ticker,start=t) for t in start })
       for t in start:
           prices=prices.append(get_closing_price(ticker,t))
           #print (prices)
       #df['Trade_Price'] = prices       
       return prices    
    data = web.DataReader(ticker, data_source='yahoo', start=start,end=start)
    return data['Adj Close']
    