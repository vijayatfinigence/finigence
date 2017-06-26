# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 17:54:18 2017

@author: vijayp
"""
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
import logging
import logging.handlers


class Account:
    
    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance
        
    def withdraw(self, amount):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        if (amount > self.balance):
           raise RuntimeError('Amount greater than available balance.')
        self.balance = self.balance - amount
        #Log print ("Withdrawing amount : " + str(amount) + " and balance is:"  + str(self.balance))
        return self.balance

    def deposit(self, amount):
        """Return the balance remaining after depositing *amount*
        dollars."""
        self.balance = self.balance + amount
        #print ("depositing  amount : " + str(amount) + " and balance is:"  + str(self.balance))
        return self.balance 
    
    def getBalance(self):
        #print ("Balance  amount : " + str(self.balance) )
        return self.balance

class TradeJournal:
    def __init__(self,name,data):
        self.name=name
        self.data = pd.DataFrame(data,columns=['Name','Date','OrderType','Ticker','Price','Shares','Amount','pandl','pandlPercent','BuyDate','DaysInTrade','BeginingBalance','EndingBalance'])
   
    def enterTrade(self,rownumber,name,orderType,date,symbol,units,unitPrice,beginBalance,endBalance):
        amount = units*unitPrice
        if (orderType=='Sell') & (symbol!='CASH'):
            pandl = amount-self.getAmount(symbol)
            #print (pandl)
            pandlPercent = 100.00*(pandl/self.getAmount(symbol))
            #print ('pandlPercent:' +str(pandlPercent))
            BuyDate =self.getDate(symbol)
            DaysInTrade=(date-BuyDate).days
        else:
            pandl=0
            pandlPercent = pandl 
            BuyDate = date
            DaysInTrade=""
        d = {'Name': name,'Date': date,'OrderType': orderType,'Ticker': symbol,'Price': unitPrice,'Shares': units,'Amount': amount,'pandl': pandl,'pandlPercent': pandlPercent,'BuyDate': BuyDate,'DaysInTrade':DaysInTrade,'BeginingBalance':beginBalance,'EndingBalance': endBalance }
        #print(name,orderType,date,symbol,units,unitPrice,amount)
        tempFrame = pd.DataFrame(data=d,index={rownumber})        
        self.data= self.data.append(other=tempFrame) 
        self.data.reset_index()
        #print (self.data)
   
    def getDate(self,ticker):
        #if len(self.data['Shares'][ self['Ticker']==ticker])>=1:
        df = self.data[ (self.data['Ticker']==ticker) &(self.data['OrderType']=='Buy') ]
        buyDate=df['Date'][-1:]
        return buyDate.iloc[0]
        
    def getTradeLedger(self):
        return self.data
    
    def getShares(self,ticker):
        #if len(self.data['Shares'][ self['Ticker']==ticker])>=1:
        df = self.data[ self.data['Ticker']==ticker]
        shares=df['Shares'][-1:]
        #print (shares.iloc[0])
        return shares.iloc[0]
    def getAmount(self,ticker):
        #if len(self.data['Shares'][ self['Ticker']==ticker])>=1:
        df = self.data[ (self.data['Ticker']==ticker) &(self.data['OrderType']=='Buy') ]
        amount=df['Amount'][-1:]
        return amount.iloc[0]

def generate_trade(pf,trade_data):
    #safe_asset,trade_data,ticker,strategy,,slow_signal,threshold,startingCapital
    safe_asset=pf['Safe Asset']
    ticker=pf['Risk Asset']   
    dataFileName =  pf['Id'] +"_trade_data.csv"
    if pf['writeFile']:
       trade_data.to_csv(dataFileName,index=False)
    rownumber = 0
    accountName = pf['Id']       
    """ Open trading account with starting balance and name of account
    """
    tradingAccount = Account(name=pf['Id'],balance=pf['Starting Capital']);
    #print ('Balance is ' + str(tradingAccount.getBalance()))
    #tradingAccount.deposit(startingCash) 
    rownumber=0
    journal = TradeJournal(accountName,pd.DataFrame())                           
    for index,row in trade_data.iterrows():
        rownumber =rownumber+1  
        safePrice=row['Safe_Price']
        tradePrice=row['Trade_Price']
        date=row['Trade_Date']
        signal=row['signal']
        #sell  = pd.DataFrame()        
        if (rownumber==1):            
            if (signal ==-1):
                """ first sell signal, no risk assetst to sell.
                    buy safe assets
                """                                
                price=safePrice
                """ Account 
                """
                beginingBalance=tradingAccount.getBalance()
                shares=int(tradingAccount.getBalance()/price) 
                #print ('Signal:' + str(signal), 'Buy=' +str(rownumber), date , safe_asset, safePrice, price, shares)                
                tradingAccount.withdraw(price*shares)               
                endingBalance=tradingAccount.getBalance()
                """ Trade
                """
                journal.enterTrade(rownumber,accountName,'Buy',date,safe_asset,shares,price,beginingBalance,endingBalance)              
            else:                    
                price=tradePrice                            
                """ Account 
                """
                #shares=pd.to_numeric(tradingAccount.getBalance()/price,downcast='integer')
                beginingBalance=tradingAccount.getBalance()
                shares=int(tradingAccount.getBalance()/price)
                #print ('Signal:' + str(signal),'Buy'+str(rownumber),date , ticker, tradePrice, price, shares)                
                tradingAccount.withdraw(price*shares)
                endingBalance=tradingAccount.getBalance()
                """ Trade
                """
                journal.enterTrade(rownumber,accountName,'Buy',date,ticker,shares,price,beginingBalance,endingBalance)
        else:                    
            if (signal ==-1):                
                price=tradePrice                
                shares=journal.getShares(ticker)
                """ Account
                """
                beginingBalance=tradingAccount.getBalance()
                tradingAccount.deposit(price*shares)   
                endingBalance=tradingAccount.getBalance()
                """ Enter trade
                """
                journal.enterTrade(rownumber,accountName,'Sell',date,ticker,shares,price,beginingBalance,endingBalance)
                #print ('Signal:' + str(signal),'Sell'+str(rownumber),date , ticker, tradePrice, price, shares)                
                            
                price=safePrice
                #shares=pd.to_numeric(tradingAccount.getBalance()/price,downcast='integer')
                """ Account
                """
                beginingBalance=tradingAccount.getBalance()
                shares=int(tradingAccount.getBalance()/price)
                #print ('Signal:' + str(signal),'Buy'+str(rownumber),date , safe_asset,safePrice, price, shares)
                tradingAccount.withdraw(price*shares) 
                endingBalance=tradingAccount.getBalance()                              
                """ Trade
                """
                journal.enterTrade(rownumber,accountName,'Buy',date,safe_asset,shares,price,beginingBalance,endingBalance)
            else:                
                 price=safePrice
                 shares=journal.getShares(safe_asset) 
                 #print ('Signal:' + str(signal),'Sell'+str(rownumber),date , safe_asset,safePrice, price, shares)                   
                 """ Account
                 """
                 beginingBalance=tradingAccount.getBalance()
                 tradingAccount.deposit(price*shares) 
                 endingBalance=tradingAccount.getBalance()
                 """ Trade
                 """
                 journal.enterTrade(rownumber,accountName,'Sell',date,safe_asset,shares,price,beginingBalance,endingBalance)
                                
                 price=tradePrice
                 #shares=pd.to_numeric(tradingAccount.getBalance()/price,downcast='integer') 
                 """ Account
                 """
                 beginingBalance=tradingAccount.getBalance()
                 shares=int(tradingAccount.getBalance()/price) 
                 #print ('Signal:' + str(signal),'Buy'+str(rownumber),date , ticker, tradePrice,  price, shares)
                 tradingAccount.withdraw(shares*price) 
                 endingBalance=tradingAccount.getBalance()
                 """ Trade
                 """
                 journal.enterTrade(rownumber,accountName,'Buy',date,ticker,shares,price,beginingBalance,endingBalance)                                
                 #print (sell)                                    
    #journal.getTradeLedger().to_csv('trade_ledger.csv')
    return journal.getTradeLedger()
    #print('Balance:' + str(tradingAccount.getBalance()) )