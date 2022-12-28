import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import norm

# inputs

kind = 'call'

S0 = 50
t = 1
K = 50
r = 0.0
vol = 0.3


def get_d1(S0, t, K, r, vol):
    d1 = (np.log(S0/K) + (r+(vol**2)/2)*t)/(vol*np.sqrt(t))
    
    return d1

def delta(S0, t, K, r, vol, kind):
    d1 = get_d1(S0, t, K, r, vol)
    
    if kind == 'call':
        delta = norm.cdf(d1)
    elif kind == 'put':
        delta = norm.cdf(d1)-1

    return delta

delta_c = delta(S0, t, K, r, vol, 'call')
delta_p = delta(S0, t, K, r, vol, 'put')

print(delta_c-delta_p)