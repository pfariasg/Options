import sys
sys.path.insert(1, '//'.join((sys.path[0]).split('\\')[:-1]))

from giraldi_pricing import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

if __name__ == '__main__':

    # calculates european call and put gammas and speeds (DgammaDspot) accross variable times and moneyness states

    # 1: option delta, gamma and speed in relation to moneyness (S0/K-1 for calls, 1-S0/K for puts, x axis)
    # 2: option gamma (y axis) in relation to moneyness (x axis) for four different times to expiration (0.1, 0.5, 1 and 2 monsths to expiration)
    # 3: option gamma (y axis) in relation to time to expiration (t, x axis) for 5% OTM, ATM and 5% ITM options
    # 4: option gamma (z axis) in relation to moneyness (x axis) and time to expiration (t, y axis)
    # 5: option gamma (z axis) in relation to moneyness (x axis) and time to expiration (t, y axis) for large t, showing explosive gamma at very small moneyness and very large t

    kind = 'call'

    fixed_S0 = 90 # S0 and K must be between 0.00000001 and 100
    fixed_t = 3/12
    fixed_K = 80
    fixed_r = 0.05
    fixed_vol = 0.20

    p = 200 # recommended: 200, computational time grows in p^2

    ##############################################################################

    # option price for different volatilities

    S0  = np.linspace(fixed_S0*.5, fixed_S0*1.5, p)

    fig, ax = plt.subplots()

    ax.set_ylabel('price', fontsize=16)
    ax.yaxis.set_label_coords(-0.075,.5)
    ax.yaxis.set_tick_params(labelsize=16)

    ax.axhline(0, c='k')
    ax.axvline(0, c='k')
    
    if kind == 'call':
        axis =  100*(S0/fixed_K-1)
    if kind == 'put':
        axis = -100*(S0/fixed_K-1)
        ax.invert_xaxis()

    vols = [0.01 + i*0.25 for i in range(5)]
    for i, vol in enumerate(vols):
        d1 = get_d1(S0, fixed_t, fixed_K, fixed_r, vol)
        d2 = get_d2(fixed_t, vol, d1)

        if i == 0:
            lns  = ax.plot(axis, expir_value(S0, fixed_K, kind), lw=2, c='black'   , label='expiration value')
            lns += ax.plot(axis,       price(S0, fixed_t, fixed_K, fixed_r, d1, d2, kind), lw=2, label=f'vol: {int((vol)*100)}%'           )
        else:
            lns += ax.plot(axis,       price(S0, fixed_t, fixed_K, fixed_r, d1, d2, kind), lw=2, label=f'vol: {int((vol-0.01)*100)}%'           )

    # lns0 = ax.plot(axis, expir_value(S0,          fixed_K,                  kind), lw=2, c='tab:red'   , label='expiration value')
    # lns1 = ax.plot(axis,       price(S0, fixed_t, fixed_K, fixed_r, d1, d2, kind), lw=2, c='tab:blue'  , label='price'           )
    # lns2 = ax.plot(axis,       delta(                               d1,     kind), lw=2, c='tab:orange', label='delta'           )

    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, fontsize=16, framealpha=1)

    ax.set_xlabel('moneyness', fontsize=16)
    ax.xaxis.set_tick_params(labelsize=16)
    ax.set_title(f'long {kind} (t={fixed_t*12} months, K={fixed_K}, r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    ax.grid(alpha=0.5)

    del lns, labs, S0, axis, d1, d2, vols, i, vol

    plt.show()

    ##############################################################################

    # option vega and gamma for different moneyness states

    S0  = np.linspace(fixed_S0*.5, fixed_S0*1.5, p)

    fig, ax0 = plt.subplots()

    ax0.set_ylabel('vega', fontsize=16)
    ax0.yaxis.set_label_coords(-0.075,.5)
    ax0.yaxis.set_tick_params(labelsize=16)

    ax1 = ax0.twinx()
    ax1.set_ylabel('gamma', fontsize=16, rotation=-90)
    ax1.yaxis.set_label_coords(1.075,.5)
    ax1.yaxis.set_tick_params(labelsize=16)

    ax0.axhline(0, c='k')
    ax0.axvline(0, c='k')
    
    if kind == 'call':
        axis =  100*(S0/fixed_K-1)
    if kind == 'put':
        axis = -100*(S0/fixed_K-1)
        ax0.invert_xaxis()

    d1 = get_d1(S0, fixed_t, fixed_K, fixed_r, fixed_vol)
    lns  = ax0.plot(axis,  vega(S0, fixed_t  ,            d1), lw=2, c='tab:blue'  , label= f'vega (t={fixed_t*12} months)')
    lns += ax1.plot(axis, gamma(S0, fixed_t  , fixed_vol, d1), lw=2, c='tab:orange', label=f'gamma (t={fixed_t*12} months)')
    lns += ax0.plot(axis,  vega(S0, fixed_t/2,            d1), lw=2, c='tab:cyan'  , label= f'vega (t={fixed_t/2*12} months)')
    lns += ax1.plot(axis, gamma(S0, fixed_t/2, fixed_vol, d1), lw=2, c='tab:red'   , label=f'gamma (t={fixed_t/2*12} months)')

    labs = [l.get_label() for l in lns]
    ax0.legend(lns, labs, fontsize=16, loc=2, framealpha=1)

    ax0.set_xlabel('moneyness', fontsize=16)
    ax0.xaxis.set_tick_params(labelsize=16)
    ax0.set_title(f'long {kind} (r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
    ax0.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    ax0.grid(alpha=0.5)

    del S0, axis, d1, lns, labs

    plt.show()

    ##############################################################################

    # option vega, different times

    S0  = np.linspace(fixed_S0*.5, fixed_S0*1.5, p)

    fig, ax = plt.subplots()

    ax.yaxis.set_label_coords(-0.1,.5)    

    colors = {'tab:blue': .1/12, 'tab:orange': 0.5/12, 'tab:green': 1/12, 'tab:red': 2/12}
    lns = 0
    for i, c in enumerate(colors):
        t = colors[c]

        d1 = get_d1(S0, t, fixed_K, fixed_r, fixed_vol)
        if i == 0:
            if kind == 'call':
                lns = ax.plot(axis:= 100*(S0/fixed_K-1), vega(S0, t, d1), lw=2, c=c  , label=f't={t*12} months')
            elif kind == 'put':
                lns = ax.plot(axis:=-100*(S0/fixed_K-1), vega(S0, t, d1), lw=2, c=c  , label=f't={t*12} months')
                ax.invert_xaxis()
        else:
            lns += ax.plot(axis, vega(S0, t, d1), lw=2, c=c  , label=f't={t*12} months')

    ax.axhline(0, c='k')
    ax.axvline(0, c='k')

    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, fontsize=16, loc=2, framealpha=1)

    ax.set_xlabel('moneyness', fontsize=16)
    ax.set_ylabel('option vega', fontsize=16)
    ax.set_title(f'long {kind} (r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)

    ax.grid(alpha=0.5)
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())

    del axis, S0, colors, i, c, d1, lns, labs

    plt.show()

    ##############################################################################

    # different moneyness accross time

    t = np.linspace(.1/360,2/12,1000)
    moneyness_chg = 0.05

    fig, ax = plt.subplots()

    for i in range(3):
        S0_loop = fixed_S0 * ((1-moneyness_chg) + i*moneyness_chg)
        d1 = get_d1(S0_loop, t, fixed_K, fixed_r, fixed_vol)

        ax.plot(t*12, vega(S0_loop, t, d1), lw=2)

    ax.set_title(f'{kind} vega accross time', fontsize=24)

    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.set_xlabel('time to expiration (months)', fontsize=16)
    ax.set_ylabel('vega', fontsize=16)

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

    # X = S0, Y = t, Z = vega, c = vanna

    S0 = np.linspace(fixed_K*.75, fixed_K*1.25, p)
    t = np.linspace(1/360, 2/12, p)

    S0_grid, t_grid = np.meshgrid(S0, t)
    zvega = np.array([vega(x, y, get_d1(x, y, fixed_K, fixed_r, fixed_vol)) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    zvega = zvega.reshape(S0_grid.shape)

    zvanna = np.array([vanna(fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol), get_d2(y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol))) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    zvanna = zvanna.reshape(S0_grid.shape)

    m = plt.cm.ScalarMappable()
    fcolors = m.to_rgba(zvanna)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    if kind == 'call':
        ax.plot_surface( 100*(S0_grid/fixed_K-1), t_grid*12, zvega, facecolors=fcolors)
    elif kind == 'put':
        ax.plot_surface(-100*(S0_grid/fixed_K-1), t_grid*12, zvega, facecolors=fcolors)
        ax.invert_xaxis()
        
    ax.set_title(f'{kind} vega for r = {fixed_r*100}%, vol = {fixed_vol*100}%', fontsize=24)
    ax.set_xlabel('moneyness')
    ax.set_ylabel('time to expiration (months)')
    ax.set_zlabel('vega')
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    fig.colorbar(m, ax=ax, label='vanna')

    ax.grid(alpha=0.5)

    del S0, t, S0_grid, t_grid, m, fcolors, zvanna, zvega

    plt.show()

    ##############################################################################

    # X = S0, Y = t, Z = vega, c = vanna

    S0 = np.linspace(fixed_K*.75, fixed_K*1.25, p)
    t = np.linspace(1/360, 6/12, p)

    S0_grid, t_grid = np.meshgrid(S0, t)
    zvomma = np.array([vomma(
        fixed_vol, 
        get_d1(x, y, fixed_K, fixed_r, fixed_vol),
        get_d2(y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol)),
        vega(x, y, get_d1(x, y, fixed_K, fixed_r, fixed_vol))
    ) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    zvomma = zvomma.reshape(S0_grid.shape)

    # zvanna = np.array([vanna(fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol), get_d2(y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol))) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    # zvanna = zvanna.reshape(S0_grid.shape)

    # m = plt.cm.ScalarMappable()
    # fcolors = m.to_rgba(zvanna)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    if kind == 'call':
        ax.plot_wireframe( 100*(S0_grid/fixed_K-1), t_grid*12, zvomma, color='black')
    elif kind == 'put':
        ax.plot_wireframe(-100*(S0_grid/fixed_K-1), t_grid*12, zvomma, color='black')
        ax.invert_xaxis()
    
    ax.set_title(f'{kind} vomma for r = {fixed_r*100}%, vol = {fixed_vol*100}%', fontsize=24)
    ax.set_xlabel('moneyness')
    ax.set_ylabel('time to expiration (months)')
    ax.set_zlabel('vomma')
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    # fig.colorbar(m, ax=ax, label='vanna')

    ax.grid(alpha=0.5)

    del S0, t, S0_grid, t_grid, zvomma

    plt.show()
