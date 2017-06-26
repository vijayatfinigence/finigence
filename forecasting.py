
# coding: utf-8

# ## Monte Carlo - Forecasting Stock Prices - Part I

# *Suggested Answers follow (usually there are multiple ways to solve a problem in Python).*

# Download the data for Microsoft (‘MSFT’) from Yahoo Finance for the period ‘2000-1-1’ until today.

import numpy as np  
import pandas as pd  
#from pandas_datareader import data as wb  
from finigence import data
import matplotlib.pyplot as plt  
from scipy.stats import norm

get_ipython().magic('matplotlib inline')

ticker = 'MSFT' 
data = pd.DataFrame()
start=""
end=""
prices = data.load_data(data_folder,"MSFT","csv","MSFT",start,end)


# Use the .pct_change() method to obtain the log returns of Microsoft for the designated period.

log_returns = np.log(1 + prices['Adj Close'].pct_change())


log_returns.tail()


data.plot(figsize=(10, 6));

log_returns.plot(figsize = (10, 6))


# Assign the mean value of the log returns to a variable, called “U”, and their variance to a variable, called “var”. 


u = log_returns.mean()
print('Mu=',u)

var = log_returns.var()
print('Variance=',var)


# Calculate the drift, using the following formula: 
# 
# $$
# drift = u - \frac{1}{2} \cdot var
# $$

drift = u - (0.5 * var)
print ('Drift=',drift)


# Store the standard deviation of the log returns in a variable, called “stdev”.

stdev = log_returns.std()
print('Standard Deviation=',stdev)