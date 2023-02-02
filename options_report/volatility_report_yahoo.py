import sys
sys.path.insert(1, '//'.join((sys.path[0]).split('\\')[:-1]))

import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from giraldi_pricing import *

if __name__ == '__main__':
    ticker = yf.Ticker('AAPL')

    S0 = ticker.history(period='1d')['Close'].values[0]

    # print(ticker.option_chain().calls)
    # ticker.option_chain().calls.to_clipboard()
    # sys.exit()
    # print(ticker.options)

    for i, expiration in enumerate(ticker.options):

        chain = ticker.option_chain(date=expiration)

        calls = chain.calls
        calls = calls.loc[:, ['strike', 'lastPrice', 'openInterest']]
        calls.columns = ['strike', 'price', 'open_interest']
        
        calls['exp'] = datetime.datetime.strptime(expiration, '%Y-%m-%d')
        calls['kind'] = 'call'

        if i == 0:
            df = calls.copy()
        else:
            df = pd.concat([df, calls], axis=0, ignore_index=True)

        puts = chain.puts
        puts = puts.loc[:, ['strike', 'lastPrice', 'openInterest']]
        puts.columns = ['strike', 'price', 'open_interest']
        puts['exp'] = datetime.datetime.strptime(expiration, '%Y-%m-%d')
        puts['kind'] = 'put'

        df = pd.concat([df, puts], axis=0, ignore_index=True)      

        # print(f'{expiration} done. {i+1}/{len(ticker.options)}')

    df = df[df.open_interest > 1000]
    df = df.iloc[-10:, :]

    df['time'] = (df['exp'] - datetime.datetime.now()) / datetime.timedelta(days=365)
    df['r'] = 0.05 # r not implemented
    
    df['vol']   = df.apply(lambda x: implied_vol(x['price'], S0, x['time'], x['strike'], x['r'],                             x['kind']), axis=1)
    df['d1']    = df.apply(lambda x:       get_d1(           S0, x['time'], x['strike'], x['r'], x['vol']                             ), axis=1)
    df['d2']    = df.apply(lambda x:       get_d2(               x['time'],                      x['vol'], x['d1']                    ), axis=1)
    
    df['delta'] = df.apply(lambda x:       delta(                                                          x['d1'],          x['kind']), axis=1)
    df['gamma'] = df.apply(lambda x:       gamma(            S0, x['time'],                      x['vol'], x['d1']                    ), axis=1)
    df['vega']  = df.apply(lambda x:        vega(            S0, x['time'],                                x['d1']                    ), axis=1)
    df['theta'] = df.apply(lambda x:       theta(            S0, x['time'], x['strike'], x['r'], x['vol'], x['d1'], x['d2'], x['kind']), axis=1)
    df['rho']   = df.apply(lambda x:         rho(                x['time'], x['strike'], x['r'],                    x['d2'], x['kind']), axis=1)
        
    df = df[['exp', 'price', 'time', 'strike', 'r', 'vol', 'kind', 'd1', 'd2', 'delta', 'gamma', 'vega', 'theta', 'rho']]

    print(df)
    df.head().to_clipboard()

