import warnings
warnings.filterwarnings("error")
# warnings.resetwarnings()

import numpy as np
from scipy.stats import norm

def expir_value(S, K, kind):
    if kind == 'call':
        return np.maximum(S-K, 0)
    elif kind == 'put':
        return np.maximum(K-S, 0)

def get_d1(S0, t, K, r, vol):
         
    return (np.log(S0/K) + (r + (vol**2)/2)*t)/(vol*np.sqrt(t))

def get_d2(t, vol, d1):
    
    return d1 - vol*np.sqrt(t)

def delta(d1, kind):

    if kind == 'call':
        return norm.cdf(d1)
    elif kind == 'put':
        return norm.cdf(d1) - 1

def gamma(S0, t, vol, d1):

    return norm.pdf(d1)/(S0*vol*np.sqrt(t))

def vega(S0, t, d1):

    return S0 * norm.pdf(d1) * np.sqrt(t)
    
def theta(S0, t, K, r, vol, d1, d2, kind):

    if kind == 'call':
        return -S0*norm.pdf(d1)*vol/(2*np.sqrt(t)) - r*K*np.exp(-r*t)*norm.cdf(d2)
    elif kind == 'put':
        return -S0*norm.pdf(d1)*vol/(2*np.sqrt(t)) + r*K*np.exp(-r*t)*norm.cdf(-d2)

def rho(t, K, r, d2, kind):

    if kind == 'call':
        return K*t*np.exp(-r*t)*norm.cdf(d2)
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

