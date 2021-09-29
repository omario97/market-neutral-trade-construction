# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 19:37:35 2021

@author: omar_
"""

import pandas as pd
import numpy as np 
import yfinance as yf
from sklearn.linear_model import LinearRegression
import time
import datetime as dt

long_stock = input('Which stock stock would you like to go long? ')
short_stock = input('Which stock stock would you like to go short? ')
start_date = input('Choose the start date in format YYYY-MM-DD: ') # get this to 5 years 251*5, fix this.
end_date = dt.datetime.today()
the_interval = "1d"

tickers = ['^GSPC' , long_stock.upper(), short_stock.upper()]

data = yf.download(tickers = tickers, start = start_date, end = end_date,interval = the_interval)['Adj Close'] 
data = data.reindex(columns = tickers) # get this in the right order everytime.

col_names = []
for i in range(1,len(tickers) + 1):
    col = f'return_{tickers[i-1]}'
    data[col] = data.iloc[:,i-1].pct_change()
    col_names.append(col)

data.dropna(inplace = True)
    
# Calc the beta for long stock.

model_1 = LinearRegression(fit_intercept=True)#wrong beta must be arounf 1.2147
model_1.fit(np.array(data[col_names[0]]).reshape(-1,1), np.array(data[col_names[1]]))  #(x,y)

time.sleep(0.5)
print(f'Beta for the long stock with the mkt is: {model_1.coef_}')

# calc the beta for the short stock.
model_2 = LinearRegression()
model_2.fit(np.array(data[col_names[0]]).reshape(-1,1), np.array(data[col_names[2]])) #(x,y)

time.sleep(0.5)
print(f'Beta for the long stock with the mkt is: {model_2.coef_}')

#Store both of the result in an list.
betas = pd.DataFrame([model_1.coef_, model_2.coef_],index = [long_stock,short_stock],
                     columns = ['beta'])
beta_ratio = betas.loc[long_stock] / betas.loc[short_stock]
time.sleep(0.5)
print(f'we have to increase/decrease with: {beta_ratio[0]} in the short positon')
print('makes sense since the long and short has to co-move')

# Gross commit to the trade. Example 10k long and 10k short = 20k Gross used cap.
# do this tomorrow.
# idea, creta e vectors then put in constraint into a dataframe.

stocks = [long_stock , short_stock ]
beta = [model_1.coef_ , model_2.coef_]
beta_target = beta_ratio

gross_limit = float(input('What is the gross limit size for this spread trade in $/NOK? '))
cap_to_long = gross_limit/(1+ beta_target)
cap_to_short = gross_limit - cap_to_long
check_var = cap_to_long + cap_to_short


print('====================================================================')
print(f'To hedge out mkt risk, we have to Long an amount of {cap_to_long[0]} $/NOK')
print(f'To hedge out mkt risk, we have to short an amount of {cap_to_short[0]} $/NOK')

print(f'And adding the long + short you would have gross profit of: {check_var[0]} $/NOK ')
print('====================================================================')

#calc how many shares 

while True:
    try:
        print('Enter 1 if you want to input data yourself or 2 if you want the prices from the data')
        holder = int(input('Press 1 or 2: '))
        if holder == 1 or holder == 2:
            break
        time.sleep(1)
        print('You can only choose from 1 or 2 Genius')
    except Exception as e:
        print(e)

if holder == 1:
    s_0_long = float(input('Input the Share price for long stock: '))
    time.sleep(0.5)
    s_0_Short = float(input('Input the Share price for short stock: '))
    shares_long = (cap_to_long / s_0_long)
    shares_short = (cap_to_short / s_0_Short)
    print('=================================================================')
    print(f'Long {int(shares_long[0])} # of shares at a price of {s_0_long}')
    print(f'Short {int(shares_short[0])} # of shares at a price of {s_0_Short}')
else:
    s_0_long = data[long_stock.upper()][-1]
    time.sleep(0.5)
    s_0_Short = data[short_stock.upper()][-1]
    print(f'The Last price observed in the data for {long_stock} was {s_0_long} at {data.index[-1]} ')
    print(f'The Last price observed in the data for {short_stock} was {s_0_Short} at {data.index[-1]} ')
    time.sleep(1)
    shares_long = (cap_to_long / s_0_long)
    shares_short = (cap_to_short / s_0_Short)
    print('=================================================================')
    print(f'Long {int(shares_long[0])} # of {long_stock} shares at a price of {s_0_long}')
    print(f'Short {int(shares_short[0])} # of {short_stock} shares at a price of {s_0_Short}')
    print('=================================================================')

#create a summary of actions and numbers

from tabulate import tabulate
info = {'Long or short': ['Long', 'Short'],
        'Ticker': [long_stock.upper(), short_stock.upper()],
        'Beta': [betas.loc[long_stock][0], betas.loc[short_stock][0],beta_ratio[0]],
        '$/NOK comitted': [cap_to_long, cap_to_short, check_var[0]],
        'Stock price': [s_0_long ,s_0_Short ],
        'Shares': [shares_long , shares_short]}
print(tabulate(info, headers='keys', tablefmt = 'fancy_grid'))



input('Press any button to exit()')
time.sleep(0.5)



        
        
    


                                    