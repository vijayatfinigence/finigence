# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 20:14:58 2017

@author: vijayp
1. The Heikin-Ashi Close is simply an average of the open, 
high, low and close for the current period. 

HA-Close = (Open(0) + High(0) + Low(0) + Close(0)) / 4

2. The Heikin-Ashi Open is the average of the prior Heikin-Ashi 
candlestick open plus the close of the prior Heikin-Ashi candlestick. 

HA-Open = (HA-Open(-1) + HA-Close(-1)) / 2 

3. The Heikin-Ashi High is the maximum of three data points: 
the current period's high, the current Heikin-Ashi 
candlestick open or the current Heikin-Ashi candlestick close. 

HA-High = Maximum of the High(0), HA-Open(0) or HA-Close(0) 

4. The Heikin-Ashi low is the minimum of three data points: 
the current period's low, the current Heikin-Ashi 
candlestick open or the current Heikin-Ashi candlestick close.

HA-Low = Minimum of the Low(0), HA-Open(0) or HA-Close(0) 


"""

import pandas as pd
import numpy as np
from finigence import data, trade_signals, trade, analyze
import time
from logutil import Logutil as lu

data_folder = r'C:\Users\vijayp\Documents\Python Scripts\finigence\data\\'
monthly_data_folder = r'C:\Users\vijayp\Documents\Python Scripts\finigence\data\monthly\\'
weekly_data_folder = r'C:\Users\vijayp\Documents\Python Scripts\finigence\data\weekly\\'


tickerList = ["QQQ","SPY","TQQQ","TLT","TMF"]
safeTickerList=["CASH" ]
thresholdList = [0.91]
source="csv"
start=""
end=""
writeFile=True
contrarian=False
buyWeakness=False
startingCapital=10000.00
fast='MACD_3_6_20'
slow='MACD_50_100_9'
strategy='Slingshot'
startDate= "" #datetime.datetime(2016, 1, 1)
endDate= ""
smoothing=False
runTime=time.strftime("%m_%d_%Y_%I%M%S")
use2Signals=False   # use both macd_3_6_20 and macd_50_100_9 or just macd_50_100_9

""" test 
"""
results = pd.DataFrame()
for ticker in tickerList:
    for safe_ticker in safeTickerList:
        for threshold in thresholdList:
            portfolioId= strategy +"_"+fast+"_"+slow+"_"+str(threshold)+ "_"+ ticker+ "_"+safe_ticker+"_"+runTime
            pf = {'Id': portfolioId, 'Strategy': strategy, 'Fast Signal': fast, 'Slow Signal': slow, 'Risk Asset':ticker, 'Safe Asset': safe_ticker, 'Threshold': threshold,'Starting Capital' :startingCapital,'Start Date':startDate, 'End Date': endDate, 'Contrarian':contrarian,'Time Stamp': runTime,'Signal Smoothing': smoothing,'writeFile': writeFile,'buyOnWeakness':buyWeakness, 'use2Signals':use2Signals}
            
            """ read the stock data
            """
            risk_asset = data.load_data('csv',pf['Risk Asset'],startDate,endDate)
            print(risk_asset.info())
            risk_asset.index=risk_asset.Date
            """ Monthly
            """
            risk_asset_monthly=pd.DataFrame()
            #risk_asset_monthly = risk_asset.resample('M', how=ohlc_dict, closed='right', label='right')
            risk_asset_monthly['Open'] = risk_asset['Open'].resample('M').first()
            risk_asset_monthly['High'] = risk_asset['High'].resample('M').max()
            risk_asset_monthly['Low'] = risk_asset['Low'].resample('M').min()
            risk_asset_monthly['Close'] = risk_asset['Close'].resample('M').last()
            risk_asset_monthly['Volume'] = risk_asset['Volume'].resample('M').sum()
            risk_asset_monthly['Adj Close'] = risk_asset['Adj Close'].resample('M').last()
            if  pf['writeFile']:
                risk_asset_monthly.to_csv(monthly_data_folder+ticker+'_monthly.csv',index=True)
            
            """ Weekly
            """
            risk_asset_weekly=pd.DataFrame()
            #risk_asset_monthly = risk_asset.resample('M', how=ohlc_dict, closed='right', label='right')
            risk_asset_weekly['Open'] = risk_asset['Open'].resample('W').first()
            risk_asset_weekly['High'] = risk_asset['High'].resample('W').max()
            risk_asset_weekly['Low'] = risk_asset['Low'].resample('W').min()
            risk_asset_weekly['Close'] = risk_asset['Close'].resample('W').last()
            risk_asset_weekly['Volume'] = risk_asset['Volume'].resample('W').sum()
            risk_asset_weekly['Adj Close'] = risk_asset['Adj Close'].resample('W').last()
            if  pf['writeFile']:
                risk_asset_weekly.to_csv(weekly_data_folder+ticker+'_weekly.csv',index=True)