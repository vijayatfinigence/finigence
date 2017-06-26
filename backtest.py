# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 07:24:25 2017

@author: vijayp
"""
import pandas as pd
from finigence import data,plots,trade_signals,trade,analyze
#from logutil import Logutil as lu


def backtest(pf,logger):
    data_folder = r'C:\Users\vijayp\Documents\Python Scripts\finigence\data\\'
    logger.info('filePrefix='+pf['Id'])
    logger.info('startDate='+ str(pf['Start Date']))
    logger.info('endDate='+ str( pf['End Date']) )
    #threshold=0.93
    """ fast
    load_data(data_folder,file,source,ticker,start,end):
    """
    
    fast = data.load_data(data_folder,pf['Fast Signal'],'csv',pf['Fast Signal'],pf['Start Date'], pf['End Date'] )
    del fast['Open']
    del fast['High']
    del fast['Low']
    #del fast['Ticker']
    fast['Date']=pd.to_datetime(fast['Date'])
    fast.rename(columns={'Close': 'f'},inplace=True)
    
    """ slow
    """
    slow = data.load_data(data_folder,pf['Slow Signal'],'csv',pf['Slow Signal'],pf['Start Date'], pf['End Date'])
    del slow['Open']
    del slow['High']
    del slow['Low']
    #del slow['Ticker']
    slow['Date']=pd.to_datetime(slow['Date'])
    
    slow.rename(columns={'Close': 's'},inplace=True)
    #print (fast.info())
    #print (slow.info())
    
    """ generate signals
    """
    fast_slow = trade_signals.signal_gen(fast,slow,pf)
    if pf['writeFile']:
       fast_slow.to_csv(pf['Id']+'_fast_slow.csv')

    """ check tail risk
    """
    #tail = data.load_data('csv',pf['Tail Risk'],pf['Start Date'], pf['End Date'])
    #tail.rename(columns=)
    
    #print (fast_slow.info())
    
    """  data for the assets
    """
    risk_asset1 = data.load_data(data_folder,pf['Risk Asset'],'csv',pf['Risk Asset'],fast_slow['Date'].iloc[0],pf['End Date'])
    risk_asset1['Date']=pd.to_datetime(risk_asset1['Date'])
    risk_asset1 = risk_asset1 [ risk_asset1['Date']>=fast_slow['Date'].iloc[0]]
    risk_asset1.rename(columns={'Date':'Trade_Date','Adj Close': 'Trade_Price'},inplace=True)
    
    buyAndHoldPandL=risk_asset1['Trade_Price'].iat[-1]*int (pf['Starting Capital']/risk_asset1['Trade_Price'].iat[0]) - ( int (pf['Starting Capital']/risk_asset1['Trade_Price'].iat[0]) * risk_asset1['Trade_Price'].iat[0])
    #print (risk_asset1.tail(10))   
    """ safe asset - usually cash
    """
    #safe_ticker='CASH'
    safe_asset1 = data.load_data(data_folder,pf['Safe Asset'],'csv',pf['Safe Asset'],fast_slow['Date'].iloc[0],pf['End Date'])
    safe_asset1['Date']=pd.to_datetime(safe_asset1['Date'])
    safe_asset1 = safe_asset1 [ safe_asset1['Date']>=fast_slow['Date'].iloc[0]]
    safe_asset1.rename(columns={'Date':'Trade_Date','Adj Close': 'Safe_Price'},inplace=True)    
    #print (safe_asset1.tail(10))   
    """ combine signals and assets to trade
        Risk asset
    """
    fast_slow=fast_slow.merge(risk_asset1,how='inner',on='Trade_Date')
    fast_slow['ticker']=pf['Risk Asset']            
    fast_slow['strategy']=pf['Strategy']                                 
    fast_slow['threshold']=pf['Threshold'] 
    #fast_slow.to_csv(ticker+'_fast_slow.csv',index=False)             
    """ safe asset - now merge in to signal+risk
    """
    fast_slow=fast_slow.merge(safe_asset1,how='inner',on='Trade_Date')
    fast_slow['safe_ticker']=pf['Safe Asset'] 
    # write to file
    fast_slow['fast_slow_signal']=pf['Fast Signal']+'_'+pf['Slow Signal'] 
    #fast_slow.to_csv(ticker+'_'+safe_ticker+'_fast_slow.csv',index=False)
    
     
    
    """ signal to positions
    """
    positions = trade.generate_trade(pf=pf,trade_data=fast_slow)
    if pf['writeFile']:
       positions.to_csv(pf['Id']+'_trade_ledger.csv',index=False)
    
    """ Analyse
    """  
    if (len(positions)>2) and (len(positions[ (positions.OrderType=='Sell') &  (positions.Ticker!='CASH')  ])>2) :
       return analyze.run_metrics(pf, positions[ (positions.OrderType=='Sell') &  (positions.Ticker!='CASH')  ],buyAndHoldPandL,False)
    else:
        return analyze.run_metrics(pf, positions,buyAndHoldPandL,True)
        
    #asset = data.load_data('yahoo','SPY',fast_slow['Date'][0],endDate)
    #print (asset.info())
    
