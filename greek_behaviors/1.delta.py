import sys
sys.path.insert(1, '//'.join((sys.path[0]).split('\\')[:-1]))

from giraldi_pricing import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

if __name__ == '__main__':
    # calculates european call and put deltas is relation to fixed and variable parameters. It displays the following graphs:

    # 1: option price (before and at expiration, y1 axis) and option delta (y2) in relation to stock price (S0, x axis)
    # 2: option delta (y axis) in relation to stock price (S0, x axis) for four different times to expiration (0.1, 0.5, 1 and 2 monsths to expiration)
    # 3: option delta (y axis) in relation to time to expiration (t, x axis) for 5% OTM, ATM and 5% ITM options
    # 4: option delta (z axis) in relation to stock price (S0, x axis) and time to expiration (t, y axis)

    # fixed inputs are used as constant variables

    kind = 'put' # call or put

    fixed_S0 = 50 
    fixed_t = 1/12
    fixed_K = 50
    fixed_r = 0.05
    fixed_vol = 0.3

    p = 200 # recommended: 200, computational time grows in p^2

    # K   = np.linspace(   40,    60, p) # not implemented
    # r   = np.linspace(    0,   0.2, p) # not implemented
    # vol = np.linspace(    0,     1, p) # not implemented

    ##############################################################################

    ### option price, delta and gamma

    S0 = np.linspace(fixed_K*.75, fixed_K*1.25, p)

    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    
    d1 = get_d1(S0, fixed_t, fixed_K, fixed_r, fixed_vol)
    d2 = get_d2(fixed_t, fixed_vol, d1)

    ax.axhline(0, c='k')

    if kind == 'call':
        axis =  100*(S0/fixed_K-1)
    elif kind == 'put':
        axis = -100*(S0/fixed_K-1)
        ax.invert_xaxis()
        
    lns0 =  ax.plot(axis, expir_value(S0,          fixed_K,                  kind), lw=2, c='tab:red'   , label='expiration value')
    lns1 =  ax.plot(axis,       price(S0, fixed_t, fixed_K, fixed_r, d1, d2, kind), lw=2, c='tab:blue'  , label='price'           )
    lns2 = ax2.plot(axis,       delta(                               d1,     kind), lw=2, c='tab:orange', label='delta'           )

    # plotting

    lns = lns0 + lns1 + lns2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, fontsize=16, loc=6, framealpha=1)

    ax.set_title(f'long {kind} (t={fixed_t*12} months, r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
    ax.set_xlabel(   'moneyness', fontsize=16              )
    ax.set_ylabel('option price', fontsize=16              )
    ax2.set_ylabel(      'delta', fontsize=16, rotation=-90)
    ax.xaxis.set_tick_params( labelsize=16)
    ax.yaxis.set_tick_params( labelsize=16)
    ax2.yaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_label_coords(-0.05, .5)
    ax2.yaxis.set_label_coords(1.05, .5)
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())

    ax.grid(alpha=0.5)

    # if kind == 'put':
    #     ax.invert_xaxis()
        # ax2.invert_xaxis()

    del S0, d1, d2, lns0, lns1, lns2, lns, labs

    plt.show()

    ##############################################################################

    ### option price and delta, different times

    S0 = np.linspace(fixed_K*.75, fixed_K*1.25, p)

    fig, ax = plt.subplots()

    ax.axhline(0, c='k')
    if kind == 'call':
        ax.axhline(1, c='k')
    elif kind == 'put':
        ax.axhline(-1, c='k')
        ax.invert_xaxis()


    colors = {'tab:blue': 0.1/12, 'tab:orange': 0.5/12, 'tab:green': 1/12, 'tab:red': 2/12}
    lns = 0
    for i, c in enumerate(colors):
        t = colors[c]

        d1 = get_d1(S0, t, fixed_K, fixed_r, fixed_vol)
        if i == 0:
            if kind == 'call':
                lns = ax.plot(axis:= 100*(S0/fixed_K-1), delta(d1, kind), lw=2, c=c  , label=f't={t*12} months')
            elif kind == 'put':
                lns = ax.plot(axis:=-100*(S0/fixed_K-1), delta(d1, kind), lw=2, c=c  , label=f't={t*12} months')
                
        else:
            lns += ax.plot(axis, delta(d1, kind), lw=2, c=c  , label=f't={t*12} months')

    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, fontsize=16, loc=2, framealpha=1)

    ax.set_title(f'long {kind} (K={fixed_K}, r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
    ax.set_xlabel('moneyness', fontsize=16)
    ax.set_ylabel('delta', fontsize=16)
    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_label_coords(-0.1,.5)
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())

    ax.grid(alpha=0.5)

    del S0, colors, lns, labs

    plt.show()

    ##############################################################################

    # different moneyness accross time

    t = np.linspace(.00001/360,2/12,p)
    moneyness_chg = 0.05

    fig, ax = plt.subplots()

    for i in range(3):
        S0_loop = fixed_S0 * ((1-moneyness_chg) + i*moneyness_chg)
        d1 = get_d1(S0_loop, t, fixed_K, fixed_r, fixed_vol)
        ax.plot(t*12, delta(d1, kind), lw=2)

    ax.set_title(f'{kind} delta accross time', fontsize=24)

    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.set_xlabel('time to expiration (months)', fontsize=16)
    ax.set_ylabel('delta', fontsize=16)
    ax.invert_xaxis()
    ax.grid(alpha=0.5)

    states = [f'{moneyness_chg*100}% out of the money', 'on the money', f'{moneyness_chg*100}% in the money']
    if kind == 'put':
        states.reverse()
    ax.legend(states, fontsize=16)

    del S0_loop, i, t, states, moneyness_chg

    plt.show()

    ##############################################################################

    # X = S0, Y = t, Z = delta, c = gamma

    S0 = np.linspace(fixed_K*.75, fixed_K*1.25, p)
    t = np.linspace(1/360, 2/12, p)

    S0_grid, t_grid = np.meshgrid(S0, t)
    zdelta = np.array([delta(get_d1(x, y, fixed_K, fixed_r, fixed_vol), kind) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    zdelta = zdelta.reshape(S0_grid.shape)

    zgamma = np.array([gamma(x, y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol)) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    zgamma = zgamma.reshape(S0_grid.shape)

    m = plt.cm.ScalarMappable()
    fcolors = m.to_rgba(zgamma)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    if kind == 'call':
        ax.plot_surface( 100*(S0_grid/fixed_K-1), t_grid*12, zdelta, facecolors=fcolors)
    elif kind == 'put':
        ax.invert_xaxis()
        ax.plot_surface(-100*(S0_grid/fixed_K-1), t_grid*12, zdelta, facecolors=fcolors)
        
    ax.set_title(f'{kind} delta for r = {fixed_r*100}%, vol = {fixed_vol*100}%', fontsize=24)
    ax.set_xlabel('moneyness')
    ax.set_ylabel('time to expiration (months)')
    ax.set_zlabel('delta')
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    fig.colorbar(m, ax=ax, label='gamma')

    ax.grid(alpha=0.5)

    del S0, t, S0_grid, t_grid, m, fcolors, zgamma, zdelta

    plt.show()