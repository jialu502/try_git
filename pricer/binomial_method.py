# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:29:49 2020

@author: 98088
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 15:23:12 2020

@author: 98088
"""

import pandas as pd
import numpy as np 
import datetime
stock_price = pd.read_csv('002027.csv',index_col=0)

sample_data = stock_price.loc[:'2019-01-01',:]
r = 0.01
N = 1
R = 0.31
# calibrate parameters
# since we only know data before pricing
ret = sample_data / sample_data.shift(1) -1 
sigma = ret.std() * np.sqrt(252) # annualized standard division
sigma = sigma.iloc[0]
dt = 1 / 252
u = np.exp(sigma * np.sqrt(dt))
d = 1 / u
p = (np.exp(r * dt) - d) / (u - d)

start_time = '2019-01-03'
start_price = stock_price.loc[start_time,'002027.SZ']    
up_knock_out_date = ['2019-02-01','2019-03-04','2019-03-29','2019-04-26','2019-05-31','2019-06-28','2019-07-26',\
                  '2019-08-23','2019-09-20','2019-10-25','2019-11-22','2019-12-27']


start_time = '2019-01-03'
real_data_calander = stock_price.loc[start_time:,:] # only use the trade calander
time_length = len(real_data_calander) 
#generate stock price path
stock_price_path = pd.DataFrame(index=real_data_calander.index,columns = range(time_length))  
stock_price_path.loc[start_time,0] = start_price
for i in range(1,len(stock_price_path)):
    stock_price_path.iloc[i,0:i+1] = start_price * pd.Series([np.power(u,k) * np.power(d,i-k) for k in range(0,i+1)])
#consider only price of the product when knocked out
value_bound = pd.DataFrame(index=stock_price_path.index,columns=stock_price_path.columns)
value_bound.iloc[-1,:] = N * np.minimum(1,stock_price_path.iloc[-1,:] /5.1)
value_bound.index = pd.to_datetime(value_bound.index)
for j in range(len(value_bound)-2,-1,-1):
    value_bound.iloc[j,:j+1] = np.exp(-r * dt) * pd.Series([(p * value_bound.iloc[j+1,k] + (1 - p) * value_bound.iloc[j+1,k+1]) for k in range(j+1)])

#Next we can calulate the SFD500 value
value_option = pd.DataFrame(index=stock_price_path.index,columns=stock_price_path.columns)
value_option.iloc[-1,:] = N * (1 + R * 357 / 365)
value_option.index = pd.to_datetime(value_option.index)
value_option.iloc[-1,:][stock_price_path.iloc[-1,:] > 5.1 * 1.03] = N * (1 + R * (value_option.index[-1]-value_option.index[0]).days / 365)
value_option.iloc[-1,:][stock_price_path.iloc[-1,:] < 5.1 * 0.7] =  N * np.minimum(1,stock_price_path.iloc[-1,:] / 5.1)
for j in range(len(value_option)-2,-1,-1):
    print(j)
    value_option.iloc[j,:j+1] = np.exp(-r * dt) * pd.Series([(p * value_option.iloc[j+1,k] + (1 - p) * value_option.iloc[j+1,k+1]) for k in range(j+1)])
    if datetime.datetime.strftime(value_option.index[j],'%Y-%m-%d') in up_knock_out_date: 
        value_option.iloc[j,:j+1][stock_price_path.iloc[j,:j+1] > 5.1 * 1.03] = N * (1 + R * (value_option.index[j]-value_option.index[0]).days / 365)
    value_option.iloc[j,:j+1][stock_price_path.iloc[j,:j+1] < 5.1 * 0.7] = pd.Series([value_bound.loc[value_option.index[j],:][stock_price_path.iloc[j,:]==price].iloc[0] for price in stock_price_path.iloc[j,:j+1][stock_price_path.iloc[j,:j+1] < 5.1 * 0.7]])

