import sys
sys.path.insert(1, '//'.join((sys.path[0]).split('\\')[:-1]))

from giraldi_pricing import *
import numpy as np
import matplotlib.pyplot as plt

# This script calculates european call and put deltas is relation to fixed and variable parameters. It displays the following graphs:

# 1: option price (before and at expiration, y1 axis) and option delta (y2) in relation to stock price (S0, x axis)
# 2: option delta (y axis) in relation to stock price (S0, x axis) for four different times to expiration (0.1, 0.5, 1 and 2 monsths to expiration)
# 3: option delta (y axis) in relation to time to expiration (t, x axis) for 5% OTM, ATM and 5% ITM options
# 4: option delta (z axis) in relation to stock price (S0, x axis) and time to expiration (t, y axis)

# fixed inputs are used as constant variables

kind = 'put' # call or put

fixed_S0 = 50 
fixed_t = 0.25
fixed_K = 50
fixed_r = 0.05
fixed_vol = 0.3

# variable inputs are used to calculate a whole axis of values

p = 50 # recommended: 200, computational time grows in p^2

# np.linspace(start, finish, precision)
S0  = np.linspace(   40,    60, p) # underlying price range, starting at zero will cause an infinite division error
t   = np.linspace(7/360, 12/12, p) # time to expiration. As gamma increases exponentially as the expiration approaches, setting a low start will distort color scales
# K   = np.linspace(   40,    60, p) # not implemented
# r   = np.linspace(    0,   0.2, p) # not implemented
# vol = np.linspace(    0,     1, p) # not implemented

##############################################################################

# option price, delta and gamma

fig, ax = plt.subplots()

ax2 = ax.twinx()
ax2.set_ylabel('delta', fontsize=16, rotation=-90)
ax.yaxis.set_label_coords(-0.05,.5)
ax2.yaxis.set_label_coords(1.05,.5)

lns0 =  ax.plot(S0,       price(S0, fixed_t, fixed_K, fixed_r, get_d1(S0, fixed_t, fixed_K, fixed_r, fixed_vol), get_d2(fixed_t, fixed_vol, get_d1(S0, fixed_t, fixed_K, fixed_r, fixed_vol)), kind), lw=2, c='tab:blue'  , label='price'           )
lns1 = ax2.plot(S0,       delta(                               get_d1(S0, fixed_t, fixed_K, fixed_r, fixed_vol),                                                                               kind), lw=2, c='tab:orange', label='delta'           )
lns2 =  ax.plot(S0, expir_value(S0,          fixed_K,                                                                                                                                          kind), lw=2, c='tab:red'   , label='expiration value')
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

del lns0, lns1, lns2, lns, labs

plt.show()

# option price and delta, different times

fig, ax = plt.subplots()

ax.yaxis.set_label_coords(-0.1,.5)

lns0 = ax.plot(S0, delta(get_d1(S0, 0.1/12, fixed_K, fixed_r, fixed_vol), kind), lw=2, c='tab:blue'  , label='t=0.1 months')
lns1 = ax.plot(S0, delta(get_d1(S0, 0.5/12, fixed_K, fixed_r, fixed_vol), kind), lw=2, c='tab:orange', label='t=0.5 months')
lns2 = ax.plot(S0, delta(get_d1(S0,   1/12, fixed_K, fixed_r, fixed_vol), kind), lw=2, c='tab:green' , label='t=1.0 months')
lns3 = ax.plot(S0, delta(get_d1(S0,   2/12, fixed_K, fixed_r, fixed_vol), kind), lw=2, c='tab:red'   , label='t=2.0 months')
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

del lns0, lns1, lns2, lns3, lns, labs

plt.show()

# different moneyness accross time

t = np.linspace(0.000001/360,2/12,10000)
moneyness_chg = 0.05

fig, ax = plt.subplots()

for i in range(3):
    S0_loop = fixed_S0 * ((1-moneyness_chg) + i*moneyness_chg)
    ax.plot(t*12, delta(get_d1(S0_loop, t, fixed_K, fixed_r, fixed_vol), kind), lw=2)

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

plt.show()

del S0_loop, i, states, moneyness_chg

# X = S0, Y = t, Z = delta, c = gamma
S0_grid, t_grid = np.meshgrid(S0, t)
zdelta = np.array([delta(get_d1(x, y, fixed_K, fixed_r, fixed_vol), kind) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
zdelta = zdelta.reshape(S0_grid.shape)

zgamma = np.array([gamma(x, y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol)) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
zgamma = zgamma.reshape(S0_grid.shape)

m = plt.cm.ScalarMappable()
fcolors = m.to_rgba(zgamma)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

ax.plot_surface(S0_grid, t_grid*12, zdelta, facecolors=fcolors)
ax.set_xlabel('stock price')
ax.set_ylabel('time to expiration (months)')
ax.set_zlabel('delta')
ax.set_title(f'{kind} delta for K = {fixed_K}, r = {fixed_r*100}%, vol = {fixed_vol*100}%', fontsize=24)
fig.colorbar(m, ax=ax, label='gamma')

ax.grid(alpha=0.5)

del m, fcolors, zgamma, zdelta, S0_grid, t_grid

plt.show()