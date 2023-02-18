import warnings
warnings.filterwarnings("error")
# warnings.resetwarnings()

import numpy as np
from scipy.stats import norm

'''
Symbol list:

v - option price
S0 - current underlying price
t - time to expiration
K - strike
r - risk-free rate
vol - volatility
kind - call or put

d/D - derivative, as in dx/dy 

'''

def expir_value(S0, K, kind):
    # option price at t = 0

    if kind == 'call':
        return np.maximum(S0-K, 0)
    elif kind == 'put':
        return np.maximum(K-S0, 0)

def get_d1(S0, t, K, r, vol):
    # d1 = (log(S0/K) + (r + vol²/2)) / (vol * sqrt(t))     
    return (np.log(S0/K) + (r + (vol**2)/2)*t)/(vol*np.sqrt(t))

def get_d2(t, vol, d1):
    # d2 = d1 - vol * sqrt(t)
    return d1 - vol*np.sqrt(t)

def delta(d1, kind):
    # dv/dS0

    # delta = 0.5: S0 + $1.0 -> v + $0.5 
    if kind == 'call':
        return norm.cdf(d1)
    elif kind == 'put':
        return norm.cdf(d1) - 1

def gamma(S0, t, vol, d1):
    # δ²v/δS0²

    # delta sensitivity to changes in price

    return norm.pdf(d1)/(S0*vol*np.sqrt(t))

def speed(S0, t, vol, d1, gamma):
    # δ³v/δS0³

    # gamma sensitivity to changes in price

    return - gamma * (1 + d1/(vol * np.sqrt(t))) / S0

def vega(S0, t, d1):
    # δv/δvol

    # vega = 18.5: vol + 0.01 -> v + 0.185

    return S0 * norm.pdf(d1) * np.sqrt(t)

def vomma(vol, d1, d2, vega):
    # δvega/δvol, δ²v/δvol²

    # vomma = 92.34: vol + 0.01 -> vega + 0.009234

    return vega * d1 * d2 / vol

def vanna(vol, d1, d2):
    # δdelta/δvol or δvega/δS0 or δ²v/(δS0 δvol)

    # vanna = -1.0008: vol + 0.01 -> delta - 0.010008, 
    # vanna = -1.0008: S0 + $1 -> vega - 0.010008

    return - norm.pdf(d1) * d2 / vol

def DvannaDvol(vol, d1, d2, vanna):
    # δ³v/(δS0 δvol²)

    return vanna * (1/vol) * (d1 * d2 - d1/d2 - 1)

def theta_driftless(S0, t, vol, d1):
    
    return -S0*norm.pdf(d1)*vol/(2*np.sqrt(t))

def theta_yield(t, K, r, d2, kind):

    if kind == 'call':
        return - r * K * np.exp(-r*t) * norm.cdf(d2)
    elif kind == 'put':     
        return + r * K * np.exp(-r*t) * norm.cdf(-d2)

def theta(S0, t, K, r, vol, d1, d2, kind):
    # δv/δt
    return theta_driftless(S0, t, vol, d1) + theta_yield(t, K, r, d2, kind)

def rho(t, K, r, d2, kind):
    # δv/δr

    if kind == 'call':
        return  K*t*np.exp(-r*t)*norm.cdf(d2)
    if kind == 'put':
        return -K*t*np.exp(-r*t)*norm.cdf(-d2)

def price(S0, t, K, r, d1, d2, kind):

    if kind == 'call':
        return S0*norm.cdf(d1) - K * np.exp(-r*t) * norm.cdf(d2)

    elif kind == 'put':
        return K * np.exp(-r*t) * norm.cdf(-d2) - S0*norm.cdf(-d1)

def implied_vol(mkt_price, S0, t, K, r, kind):
    tol = 0.001
    max_iterations = 1000

    # vol = np.sqrt(2*np.pi/t)*mkt_price/S0
    vol = 0.5
    for i in range(max_iterations):
        try:
            d1 = get_d1(S0, t, K, r, vol)
            d2 = get_d2(t, vol, d1)
        except:
            return np.nan
        
        diff = mkt_price - price(S0, t, K, r, d1, d2, kind)

        if abs(diff) < tol:
            # print(f'found on {i}th iteration')
            # print(f'difference is equal to {diff}')
            break
        
        try: 
            d1 = get_d1(S0, t, K, r, vol)
            vol = vol + diff / vega(S0, t, d1)
            
        except:
            return np.nan
    
    return vol

