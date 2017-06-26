# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 11:32:56 2017

@author: vijayp
"""
import pandas as pd
from dateutil.relativedelta import relativedelta
import math

def zerometrics(pf):
    metrics = pd.DataFrame.from_dict({ 
                 'identifier' : { 
                    'id': pf['Id'],
                    'Risk Asset': pf['Risk Asset'] ,                           
                    'Safe Asset': pf['Safe Asset'] ,
                    'Begining Balance': pf['Starting Capital'] ,
                    'Ending Balance': 0 ,                      
                    'Fast Signal': pf['Fast Signal'] ,
                    'Slow Signal': pf['Slow Signal'] ,                
                    #'High/Threshold/Low Bands': pf['lowerBand']/pf['Threshold']/pf['higherBand'] ,
                    'Start Date': "",
                    'End Date': "",
                    'Total Trades': 0 , 
                    'Number of Equity Trades': 0,
                    'Number of Bond Trades': 0,
                    'Average Days in Trade': 0,                                
                    'winrate': 0 , 
                    'Average Gain': 0,
                    'Max Gain': 0, 
                    'Average Loss': 0,
                    'Max Loss': 0,
                    'payoff': 0,
                    'pandl': 0,
                    'pandl from safe asset': 0,
                    'pandl from risk asset': 0,
                    'EV': 0,                   
                    'Win%': 0,
                    'Loss%': 0,
                    'pf':pf, 
                    'maxdd': 0,
                    'buyAndHoldProfit': 0,
                    'ExcessOverBuyAndHoldProfit': 0,
                    'CAGR %': 0 }  
                }, orient='index')     
    return metrics;


def cagr (starting_balance, ending_balance, num_of_years):
    if (starting_balance==0):
        starting_balance=1
    if float(num_of_years) ==0:
        return 0
    if (ending_balance==0):
        return 0    
    return ( ((ending_balance/starting_balance)**(1/float(num_of_years))) -1)*100

def run_metrics(pf,positions,buyAndHoldPandL,noMetrics):
    
    if noMetrics:
        return zerometrics(pf)
    
    trades=positions
    print (pf['Safe Asset'], str(pf['Starting Capital']), pf['Risk Asset'])
    winrate = float(sum(trades['pandl'] > 0)) / len(trades['pandl'])
    win_percent = 100*float(trades[trades['pandl']>0]['pandl'].count())/len(trades)
    loss_percent = 100*float(trades[trades['pandl']<0]['pandl'].count())/len(trades)
    
    average_gain  = trades[trades['pandl']>0]['pandl'].mean()
    average_loss = trades[trades['pandl']<0]['pandl'].mean()
    max_gain = trades[trades['pandl']>0]['pandl'].max()
    max_loss =  trades[trades['pandl']<0]['pandl'].min() # yes min loss is max number
    #pf = PF = abs(trades['pandl'][trades['pandl'] > 0].sum() / trades['pandl'][trades['pandl'] < 0].sum())
    maxdd = (trades['pandl'].cumsum().expanding().max() - trades['pandl'].cumsum()).max()
    expectency_value = (average_gain*win_percent ) +(average_loss* loss_percent)

    #payoff = average_gain/-average_loss    
    payoff = trades['pandl'][trades['pandl'] > 0].mean() / -trades['pandl'][trades['pandl'] < 0].mean()
    pandl = round(trades['pandl'].sum(),2)
    pandlequity = round(trades['pandl'][ trades['Ticker']==pf['Risk Asset'] ].sum(),2)
    pandlbonds = round(trades['pandl'][ trades['Ticker']==pf['Safe Asset'] ].sum(),2)
    numberOfEquityTrades = len(trades['Date'][ trades['Ticker']==pf['Risk Asset'] ])
    numberOfBondTrades = len(trades['Date'][ trades['Ticker']==pf['Safe Asset'] ])

    difference_in_years = relativedelta(trades['Date'].max(), trades['BuyDate'].min()).years
    days_in_trade = trades['DaysInTrade'].mean()  
                                 
    endingBalance=trades['EndingBalance'].iloc[len(trades)-1] 
    print ("endingBalance:"+ str(endingBalance) + "/" + str(difference_in_years) )  
    beginingBalance=pf['Starting Capital']                                   
    #cagr = (endingBalance/beginingBalance)**(1/float(difference_in_years))) -1)*100
    #max_drawdown = 
    excessReturnsOverBH = round(trades['pandl'].sum(),2) -round(buyAndHoldPandL,2) 
    metrics = pd.DataFrame.from_dict({ 
                 'identifier' : { 
                    'id': pf['Id'],
                    'Risk Asset': pf['Risk Asset'] ,                           
                    'Safe Asset': pf['Safe Asset'] ,
                    'Begining Balance': pf['Starting Capital'] ,
                    'Ending Balance': endingBalance ,                      
                    'Fast Signal': pf['Fast Signal'] ,
                    'Slow Signal': pf['Slow Signal'] ,                
                    'Threshold': pf['Threshold'] ,
                    'Start Date': trades['Date'].min(),
                    'End Date': trades['Date'].max(),
                    'Total Trades':len(trades) , 
                    'Number of Equity Trades': numberOfEquityTrades,
                    'Number of Bond Trades': numberOfBondTrades,
                    'Average Days in Trade': days_in_trade,                                
                    'winrate': winrate , 
                    'Average Gain': average_gain,
                    'Max Gain': max_gain, 
                    'Average Loss': average_loss,
                    'Max Loss': max_loss,
                    'payoff': payoff,
                    'pandl':pandl ,
                    'pandl from safe asset':pandlbonds  ,
                    'pandl from risk asset':pandlequity ,
                    'EV':expectency_value,                    
                    'Win%':win_percent,
                    'Loss%': loss_percent,
                    'pf':pf, 
                    'maxdd':maxdd,
                    'buyAndHoldProfit':buyAndHoldPandL,
                    'ExcessOverBuyAndHoldProfit': excessReturnsOverBH,
                    'CAGR %': cagr(beginingBalance,endingBalance,difference_in_years) }  
                }, orient='index')      
    
    print (metrics[['EV','Average Gain','Win%','Loss%','Average Loss','pandl','payoff','maxdd']])                   
    return metrics     
    