# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 13:13:17 2017

@author: vijayp
parameters: threshold :- IVTS slope of 1-month Vol (VIX) and 3-month Vol (VXV)
Buy=Cover=1
Sell=Short=-1
Hold=0
Contrarian: Does opposite. i.e. flip the signs on Buy, Sell. Therefore, buy = -1, Sell = 1

"""

import pandas as pd
import numpy as np



def signal_gen(fast,slow,pf):
    threshold=pf['Threshold']
    smooth=pf['Signal Smoothing']
    contrarian=pf['Contrarian']
    buyOnWeakness=pf['buyOnWeakness']
    buy = 1
    sell = -1
    if contrarian:
       buy = -1
       sell = 1
    fast_slow=pd.DataFrame()    
    fast_slow = fast.merge(slow,how='inner',on='Date')
    fast_slow['fs_ratio'] = np.round(fast_slow['f']/fast_slow['s'],decimals=2,out=None)
    fast_slow['fs_ratio5'] =  np.round(fast_slow['fs_ratio'].rolling(window=5,center=False).mean(),decimals=2,out=None)
    #print(fast_slow[['Date','f','s','fs_ratio','fs_ratio5']])
    """ Threshold implementation to generate signals.
    LT or EQ - Buy
    GT - Sell
    """
    if buyOnWeakness:
        fast_slow['Buy_Sell_Smooth'] = np.where ( fast_slow['fs_ratio5']>threshold,buy,sell )
        fast_slow['Buy_Sell'] = np.where ( fast_slow['fs_ratio']>threshold,buy,sell )
    else:
        fast_slow['Buy_Sell_Smooth'] = np.where ( fast_slow['fs_ratio5']<=threshold,buy,sell )
        fast_slow['Buy_Sell'] = np.where ( fast_slow['fs_ratio']<=threshold,buy,sell )
    """ if signal remains in the same zone...continue holding i.e. zero
    """
    fast_slow['signal'] = np.where (fast_slow['Buy_Sell']==fast_slow['Buy_Sell'].shift(1),0,fast_slow['Buy_Sell'])
    fast_slow['smooth_signal'] = np.where (fast_slow['Buy_Sell_Smooth']==fast_slow['Buy_Sell_Smooth'].shift(1),0,fast_slow['Buy_Sell_Smooth'])
    """ we usually buy/sell the next day after signal or at the time of close
    """
    fast_slow['Trade_Date'] = fast_slow['Date'].shift(-1) # trade on next day before Market close.
    
   
    if pf['writeFile']:
       fast_slow.to_csv(pf['Id']+'_fast_slow_series.csv',index=False)
    if (smooth):
       fast_slow= fast_slow[ fast_slow['smooth_signal']!=0]  # remove any no action/signal. 0 - no trades/hold.
    else:
         fast_slow= fast_slow[ fast_slow['signal']!=0]  # remove any no action/signal. 0 - no trades/hold.
    return fast_slow

def signals_from_vix(fast_slow,pf):
    threshold=pf['Threshold']  #normally 1
    smooth=pf['Signal Smoothing']
    contrarian=pf['Contrarian']
    buyOnWeakness=pf['buyOnWeakness']
    buy = 1
    sell = -1
    if contrarian:
       buy = -1
       sell = 1
    fast_slow['fs_ratio'] = np.round(fast_slow['f']/fast_slow['s'],decimals=2,out=None)
    fast_slow['fs_ratio5'] =  np.round(fast_slow['fs_ratio'].rolling(window=5,center=False).mean(),decimals=2,out=None)
    #print(fast_slow[['Date','f','s','fs_ratio','fs_ratio5']])
    """ Threshold implementation to generate signals.
    LT or EQ - Buy
    GT - Sell
    """
    if buyOnWeakness:
        fast_slow['Buy_Sell_Smooth'] = np.where ( fast_slow['fs_ratio5']>threshold,buy,sell )
        fast_slow['Buy_Sell'] = np.where ( fast_slow['fs_ratio']>threshold,buy,sell )
    else:
        fast_slow['Buy_Sell_Smooth'] = np.where ( fast_slow['fs_ratio5']<=threshold,buy,sell )
        fast_slow['Buy_Sell'] = np.where ( fast_slow['fs_ratio']<=threshold,buy,sell )
    """ if signal remains in the same zone...continue holding i.e. zero
    """
    fast_slow['signal'] = np.where (fast_slow['Buy_Sell']==fast_slow['Buy_Sell'].shift(1),0,fast_slow['Buy_Sell'])
    fast_slow['smooth_signal'] = np.where (fast_slow['Buy_Sell_Smooth']==fast_slow['Buy_Sell_Smooth'].shift(1),0,fast_slow['Buy_Sell_Smooth'])
    """ we usually buy/sell the next day after signal or at the time of close
    """
    fast_slow['Trade_Date'] = fast_slow['Date'].shift(-1) # trade on next day before Market close.
    
   
    if pf['writeFile']:
       fast_slow.to_csv(pf['Id']+'_fast_slow_series.csv',index=False)
    if (smooth):
       fast_slow= fast_slow[ fast_slow['smooth_signal']!=0]  # remove any no action/signal. 0 - no trades/hold.
    else:
         fast_slow= fast_slow[ fast_slow['signal']!=0]  # remove any no action/signal. 0 - no trades/hold.
    return fast_slow


def signal_gen_from_macd(fast_slow,pf):
    threshold=pf['Threshold']
    smooth=pf['Signal Smoothing']
    contrarian=pf['Contrarian']
    buyOnWeakness=pf['buyOnWeakness']
    buy = 1
    sell = -1
    hold=0
    if contrarian:
       buy = -1
       sell = 1
       
    #fast_slow=pd.DataFrame()    
    """go long when slow_macd crosses over its signal and fast_macd crosses over its signal   
     Threshold implementation to generate signals.    
    """
    if (pf['use2Signals']):
        fast_slow['Buy_Sell'] = np.where ( (fast_slow['Fast']>0) & (fast_slow['Slow']>0),buy, sell )
    else:
        fast_slow['Buy_Sell'] = np.where ( fast_slow['Slow']>0,buy, sell )
    
    """ if signal remains in the same zone...continue holding i.e. zero
    """
    fast_slow['signal'] = np.where (fast_slow['Buy_Sell']==fast_slow['Buy_Sell'].shift(1),hold,fast_slow['Buy_Sell'])
    """ we usually buy/sell the next day after signal or at the time of close
    """
    fast_slow['Trade_Date'] = fast_slow['Date'].shift(-1) # trade on next day before Market close.   
   
    if pf['writeFile']:
       fast_slow.to_csv(pf['Id']+'_fast_slow_series.csv',index=False)
    fast_slow= fast_slow[ fast_slow['signal']!=0]  # remove any no action/signal. 0 - no trades/hold.
    return fast_slow