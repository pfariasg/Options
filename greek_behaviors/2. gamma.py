# incomplete

import sys
sys.path.insert(1, '//'.join((sys.path[0]).split('\\')[:-1]))

from giraldi_pricing import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

if __name__ == '__main__':

    kind = 'put'

    fixed_S0 = 50 
    fixed_t = 1/12
    fixed_K = 50
    fixed_r = .05
    fixed_vol = 0.3

    # variable inputs are used to calculate a whole axis of values

    p = 200 # recommended: 200, computational time grows in p^2

    # K   = np.linspace(   40,    60, p) # not implemented
    # r   = np.linspace(    0,   0.2, p) # not implemented
    # vol = np.linspace(    0,     1, p) # not implemented

    ##############################################################################

    # option delta, gamma and speed

    S0  = np.linspace(.0001, 100, p)

    fig, ax0 = plt.subplots()

    ax0.set_ylabel('delta', fontsize=16, color='tab:blue')
    ax0.yaxis.set_label_coords(-0.075,.5)
    ax0.yaxis.set_tick_params(labelsize=16)
    ax0.tick_params(axis='y', colors='tab:blue')

    ax1 = ax0.twinx()
    ax1.set_ylabel('gamma', fontsize=16, rotation=-90, color='tab:orange')
    ax1.yaxis.set_label_coords(1.075,.5)
    ax1.yaxis.set_tick_params(labelsize=16)
    ax1.tick_params(axis='y', colors='tab:orange')

    ax2 = ax0.twinx()
    ax2.set_ylabel('speed', fontsize=16, rotation=-90, color='tab:red')
    ax2.yaxis.set_label_coords(1.100,.5)
    ax2.yaxis.set_tick_params(labelsize=16)
    ax2.tick_params(axis='y', colors='tab:red')

    ax0.axhline(0, c='k')
    ax0.axvline(0, c='k')
    
    if kind == 'call':
        axis =  100*(S0/fixed_K-1)
    if kind == 'put':
        axis = -100*(S0/fixed_K-1)
        ax0.invert_xaxis()

    d1 = get_d1(S0, fixed_t, fixed_K, fixed_r, fixed_vol)

    lns0 = ax0.plot(axis,         delta(                        d1,         kind), lw=2, c='tab:blue'  , label='delta')
    lns1 = ax1.plot(axis, _gamma:=gamma(S0, fixed_t, fixed_vol, d1              ), lw=2, c='tab:orange', label='gamma')
    lns2 = ax2.plot(axis,         speed(S0, fixed_t, fixed_vol, d1, _gamma      ), lw=2, c='tab:red'   , label='speed')

    lns = lns0 + lns1 + lns2
    labs = [l.get_label() for l in lns]
    ax0.legend(lns, labs, fontsize=16, loc=2, framealpha=1)

    ax0.set_xlabel('moneyness', fontsize=16)
    ax0.xaxis.set_tick_params(labelsize=16)
    ax0.set_title(f'long {kind} (t={fixed_t*12} months, K={fixed_K}, r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
    ax0.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    ax0.grid(alpha=0.5)

    del lns0, lns1, lns, labs, S0, _gamma, axis, d1

    plt.show()

    ##############################################################################

    # option gamma, different times

    S0  = np.linspace(.0001, 100, p)

    fig, ax = plt.subplots()

    ax.yaxis.set_label_coords(-0.1,.5)    

    colors = {'tab:blue': 0.1/12, 'tab:orange': 0.5/12, 'tab:green': 1/12, 'tab:red': 2/12}
    lns = 0
    for i, c in enumerate(colors):
        t = colors[c]

        d1 = get_d1(S0, t, fixed_K, fixed_r, fixed_vol)
        if i == 0:
            if kind == 'call':
                lns = ax.plot(axis:= 100*(S0/fixed_K-1), gamma(S0, t, fixed_vol, d1), lw=2, c=c  , label=f't={t*12} months')
            elif kind == 'put':
                lns = ax.plot(axis:=-100*(S0/fixed_K-1), gamma(S0, t, fixed_vol, d1), lw=2, c=c  , label=f't={t*12} months')
                ax0.invert_xaxis()
        else:
            lns += ax.plot(axis, gamma(S0, t, fixed_vol, d1), lw=2, c=c  , label=f't={t*12} months')

    ax.axhline(0, c='k')
    ax.axvline(0, c='k')

    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, fontsize=16, loc=2, framealpha=1)

    ax.set_xlabel('moneyness', fontsize=16)
    ax.set_ylabel('option gamma', fontsize=16)
    ax.set_title(f'long {kind} (K={fixed_K}, r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)

    ax.grid(alpha=0.5)
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())

    del axis, S0, colors, i, c, d1, lns, labs

    plt.show()

    ##############################################################################

    # different moneyness accross time

    t = np.linspace(1/360,2/12,1000)
    moneyness_chg = 0.05

    fig, ax = plt.subplots()

    for i in range(3):
        S0_loop = fixed_S0 * ((1-moneyness_chg) + i*moneyness_chg)
        d1 = get_d1(S0_loop, t, fixed_K, fixed_r, fixed_vol)

        ax.plot(t*12, gamma(S0_loop, t, fixed_vol, d1), lw=2)

    ax.set_title(f'{kind} gamma accross time', fontsize=24)

    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.set_xlabel('time to expiration (months)', fontsize=16)
    ax.set_ylabel('gamma', fontsize=16)

    ax.set_xlim(0,2)
    ax.invert_xaxis()
    ax.grid(alpha=0.5)

    states = [f'{moneyness_chg*100}% out of the money', 'on the money', f'{moneyness_chg*100}% in the money']
    if kind == 'put':
        states.reverse()
    ax.legend(states, fontsize=16)

    del S0_loop, i, states, moneyness_chg, t

    plt.show()

    ##############################################################################

    # X = S0, Y = t, Z = gamma, c = dgamma

    ## add gamma incline as color

    S0  = np.linspace(.75*50, 1.25*50, p) # restricted underlying price range due to gamma acceleration, starting at zero will cause an infinite division error
    t   = np.linspace(7/360, 2/12, p)

    S0_grid, t_grid = np.meshgrid(S0, t)

    # change zdelta to zgamma, zgamma to zdgamma

    zgamma = np.array([gamma(x, y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol)) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    zgamma = zgamma.reshape(S0_grid.shape)

    zspeed = np.array([speed(x, y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol), gamma(x, y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol))) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    zspeed = zspeed.reshape(S0_grid.shape)

    m = plt.cm.ScalarMappable(cmap='viridis')
    fcolors = m.to_rgba(abs(zspeed))

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    if kind == 'call':
        axis =  100*(S0_grid/fixed_K - 1)
    if kind == 'put':
        axis = -100*(S0_grid/fixed_K - 1)
        ax.invert_xaxis()

    ax.plot_surface(axis, t_grid*12, zgamma, facecolors=fcolors)
    ax.set_xlabel('moneyness')
    ax.set_ylabel('time to expiration (months)')
    ax.set_zlabel('gamma')

    ax.set_title(f'{kind} gamma for r = {fixed_r*100}%, vol = {fixed_vol*100}%', fontsize=24)
    fig.colorbar(m, ax=ax, label='absolute speed')

    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    ax.grid(alpha=0.5)

    del m, fcolors, zgamma, zspeed, S0_grid, t_grid, axis

    plt.show()

    ##############################################################################

    # X = S0, Y = t, Z = gamma, c = dgamma

    ## add gamma incline as color

    S0  = np.linspace(5, 100, p*5) # restricted underlying price range due to gamma acceleration, starting at zero will cause an infinite division error
    t   = np.linspace(60/360, 240/12, p*5)

    S0_grid, t_grid = np.meshgrid(S0, t)

    # change zdelta to zgamma, zgamma to zdgamma

    zgamma = np.array([gamma(x, y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol)) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    zgamma = zgamma.reshape(S0_grid.shape)

    zspeed = np.array([speed(x, y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol), gamma(x, y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol))) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    zspeed = zspeed.reshape(S0_grid.shape)

    m = plt.cm.ScalarMappable(cmap='viridis')
    fcolors = m.to_rgba(abs(zspeed))

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    if kind == 'call':
        axis =  100*(S0_grid/fixed_K - 1)
    if kind == 'put':
        axis = -100*(S0_grid/fixed_K - 1)
        ax.invert_xaxis()

    ax.plot_surface(axis, t_grid*12, zgamma, facecolors=fcolors)
    ax.set_xlabel('moneyness')
    ax.set_ylabel('time to expiration (months)')
    ax.set_zlabel('gamma')

    ax.set_title(f'{kind} gamma for r = {fixed_r*100}%, vol = {fixed_vol*100}%', fontsize=24)
    fig.colorbar(m, ax=ax, label='absolute speed')

    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    ax.grid(alpha=0.5)

    del m, fcolors, zgamma, zspeed, S0_grid, t_grid, axis

    plt.show()