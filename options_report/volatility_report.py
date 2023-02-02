import sys
sys.path.insert(1, '//'.join((sys.path[0]).split('\\')[:-1]))

import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from giraldi_pricing import *
import yfinance as yf

if __name__ == '__main__': 
    ticker = 'AAPL'

    df = pd.read_csv(r'options report/apple_options.csv')
    df = df.iloc[:, :7]
    
    # filter out ticker
    df = df.loc[df['act_symbol']==ticker]
    df.drop('act_symbol', axis=1, inplace=True)
    
    # general formatting
    df['call_put'] = df['call_put'].str.lower()
    df['date'] = pd.to_datetime(df['date'])
    df['expiration'] = pd.to_datetime(df['expiration'])
    
    df.rename({'call_put': 'kind', 'expiration': 'exp'}, axis=1, inplace=True)
    df['price'] = df[['bid','ask']].mean(axis=1)
    df.drop(['bid', 'ask'], axis=1, inplace=True)
    
    # add S0 column
    S0 = yf.download(ticker, start="2019-01-01")
    S0.reset_index(inplace=True)
    
    S0 = S0.loc[:, ['Date', 'Adj Close']]
    S0.columns = ['date', 'S0']
    
    S0['date'] = pd.to_datetime(pd.to_datetime(S0['date']).dt.date)
    df = df.merge(S0, how='left', on='date')
    del S0
    
    # create ticker
    df['ticker'] = df.apply(lambda x: f'''{x['kind'][0].upper()}_{ticker}_{round(x['strike'], 1)}_{pd.to_datetime(x['exp']).strftime('%d-%b-%Y')}''', axis=1)
    
    # add time column
    df['time'] = (df['exp'] - df['date']) / datetime.timedelta(days=365)
    
    # add risk-free rate (not implemented)
    df['r'] = 0.02
    
    df.fillna(method='ffill', inplace=True)
    df.dropna(inplace=True)
    
    # df = df[df['kind']=='call']
    df = df.iloc[-10:]
    
    df['vol']   = df.apply(lambda x: implied_vol(x['price'], x['S0'], x['time'], x['strike'], x['r'],                             x['kind']), axis=1)
    df['d1']    = df.apply(lambda x:       get_d1(           x['S0'], x['time'], x['strike'], x['r'], x['vol']                             ), axis=1)
    df['d2']    = df.apply(lambda x:       get_d2(                    x['time'],                      x['vol'], x['d1']                    ), axis=1)
    
    df['delta'] = df.apply(lambda x:       delta(                                                               x['d1'],          x['kind']), axis=1)
    df['gamma'] = df.apply(lambda x:       gamma(            x['S0'], x['time'],                      x['vol'], x['d1']                    ), axis=1)
    df['vega']  = df.apply(lambda x:        vega(            x['S0'], x['time'],                                x['d1']                    ), axis=1)
    df['theta'] = df.apply(lambda x:       theta(            x['S0'], x['time'], x['strike'], x['r'], x['vol'], x['d1'], x['d2'], x['kind']), axis=1)
    df['rho']   = df.apply(lambda x:         rho(                     x['time'], x['strike'], x['r'],                    x['d2'], x['kind']), axis=1)
    
    df = df[['date', 'ticker', 'exp', 'price', 'S0', 'time', 'strike', 'r', 'vol', 'kind', 'd1', 'd2', 'delta', 'gamma', 'vega', 'theta', 'rho']]
    
    print(df)
    df.head().to_clipboard()
    sys.exit()