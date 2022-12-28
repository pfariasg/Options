import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import norm

# inputs

kind = 'put'

fixed_S0 = 50
fixed_t = 0.25
fixed_K = 50
fixed_r = 0.05
fixed_vol = 0.3

p = 200

S0  = np.linspace(   40,    60, p)
t   = np.linspace(7/360, 12/12, p)
# K   = np.linspace(   40,    60, p)
# r   = np.linspace(    0,   0.2, p)
# vol = np.linspace(    0,     1, p)

# params

# mpl.style.use('fast')
# mpl.rcParams['path.simplify'] = True
# mpl.rcParams['path.simplify_threshold'] = 1

#

def expir_value(S, K, kind):
    if kind == 'call':
        return np.maximum(S - K, 0)
    elif kind == 'put':
        return np.maximum(K - S, 0)

def get_d1(S0, t, K, r, vol):
    d1 = (np.log(S0/K) + (r+(vol**2)/2)*t)/(vol*np.sqrt(t))
    
    return d1

def get_d2(S0, t, K, r, vol):
    d2 = get_d1(S0, t, K, r, vol) - vol*np.sqrt(t)
    
    return d2

def price(S0, t, K, r, vol, kind):
    d1 = get_d1(S0, t, K, r, vol)
    d2 = get_d2(S0, t, K, r, vol)

    if kind == 'call':
        return S0*norm.cdf(d1) - K * np.exp(-r*t) * norm.cdf(d2)

    elif kind == 'put':
        return K * np.exp(-r*t) * norm.cdf(-d2) - S0*norm.cdf(-d1)        

def delta(S0, t, K, r, vol, kind):
    d1 = get_d1(S0, t, K, r, vol)
    
    if kind == 'call':
        delta = norm.cdf(d1)
    elif kind == 'put':
        delta = norm.cdf(d1)-1

    return delta

def gamma(S0, t, K, r, vol):
    d1 = get_d1(S0, t, K, r, vol)
    gamma = norm.pdf(d1)/(S0*vol*np.sqrt(t))

    return gamma


# X = S0, Y = t, Z = delta, c = gamma
S0_grid, t_grid = np.meshgrid(S0, t)
zdelta = np.array([delta(x, y, fixed_K, fixed_r, fixed_vol, kind) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
zdelta = zdelta.reshape(S0_grid.shape)

zgamma = np.array([gamma(x, y, fixed_K, fixed_r, fixed_vol) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
zgamma = zgamma.reshape(S0_grid.shape)

m = plt.cm.ScalarMappable()
fcolors = m.to_rgba(zgamma)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

ax.plot_surface(S0_grid, t_grid*12, zdelta, facecolors=fcolors)
ax.set_xlabel('stock price')
ax.set_ylabel('time to expiration (months)')
ax.set_zlabel('delta')
ax.set_title(f'{kind} delta for K = {fixed_K}, r = {fixed_r*100}%, vol = {fixed_vol*100}%', fontsize=24)
fig.colorbar(m, label='gamma')
del m, fcolors, zgamma, zdelta, S0_grid, t_grid

ax.grid(alpha=0.5)

plt.show()

# option price and delta

fig, ax = plt.subplots()

ax.yaxis.set_label_coords(-0.1,.5)

lns0 = ax.plot(S0, delta(S0, 0.1/12, fixed_K, fixed_r, fixed_vol, kind), lw=2, c='tab:blue'  , label='t=0.1 months')
lns1 = ax.plot(S0, delta(S0, 0.5/12, fixed_K, fixed_r, fixed_vol, kind), lw=2, c='tab:orange', label='t=0.5 months')
lns2 = ax.plot(S0, delta(S0,   1/12, fixed_K, fixed_r, fixed_vol, kind), lw=2, c='tab:green' , label='t=1.0 months')
lns3 = ax.plot(S0, delta(S0,   2/12, fixed_K, fixed_r, fixed_vol, kind), lw=2, c='tab:red'   , label='t=2.0 months')
ax.axhline(0, c='k')

lns = lns0 + lns1 + lns2 + lns3
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, fontsize=16, loc=2, framealpha=1)

ax.set_xlabel( 'stock price', fontsize=16)
ax.set_ylabel('option delta', fontsize=16)
ax.set_title(f'long {kind} (K={fixed_K}, r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
ax.xaxis.set_tick_params(labelsize=16)
ax.yaxis.set_tick_params(labelsize=16)

ax.grid(alpha=0.5)

plt.show()

# option price and delta

fig, ax = plt.subplots()

ax2 = ax.twinx()
ax2.set_ylabel('delta', fontsize=16, rotation=-90)
ax.yaxis.set_label_coords(-0.05,.5)
ax2.yaxis.set_label_coords(1.05,.5)

lns0 =  ax.plot(S0,       price(S0, fixed_t, fixed_K, fixed_r, fixed_vol, kind), lw=2, c='tab:blue'  , label='price'           )
lns1 = ax2.plot(S0,       delta(S0, fixed_t, fixed_K, fixed_r, fixed_vol, kind), lw=2, c='tab:orange', label='delta'           )
lns2 =  ax.plot(S0, expir_value(S0,          fixed_K,                     kind), lw=2, c='tab:red'   , label='expiration value')
ax.axhline(0, c='k')

lns = lns0 + lns1 + lns2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, fontsize=16, loc=2, framealpha=1)

ax.set_xlabel( 'stock price', fontsize=16)
ax.set_ylabel('option price', fontsize=16)
ax.set_title(f'long {kind} (t={fixed_t*12} months, K={fixed_K}, r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
ax.xaxis.set_tick_params(labelsize=16)
ax.yaxis.set_tick_params(labelsize=16)
ax2.yaxis.set_tick_params(labelsize=16)

ax.grid(alpha=0.5)

plt.show()

# different moneyness accross time

t = np.linspace(0.000001/360,2/12,10000)
moneyness_chg = 0.05

fig, ax = plt.subplots()

for i in range(3):
    S0_loop = fixed_S0 * ((1-moneyness_chg) + i*moneyness_chg)
    ax.plot(t*12, delta(S0_loop, t, fixed_K, fixed_r, fixed_vol, kind), lw=2)
del S0_loop, i

ax.set_title(f'{kind} delta accross time', fontsize=24)

ax.xaxis.set_tick_params(labelsize=16)
ax.yaxis.set_tick_params(labelsize=16)
ax.set_xlabel('time to expiration (months)', fontsize=16)
ax.set_ylabel('delta', fontsize=16)

ax.set_xlim(0,2)
if kind == 'call':
    ax.set_ylim(0,1.1)
elif kind == 'put':
    ax.set_ylim(-1.1,0.1)
    ax.axhline(0, c='k')

ax.invert_xaxis()
ax.grid(alpha=0.5)

states = [f'{moneyness_chg*100}% out of the money', 'on the money', f'{moneyness_chg*100}% in the money']
if kind == 'put':
    states.reverse()
ax.legend(states, fontsize=16)
del states, moneyness_chg

plt.show()