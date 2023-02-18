import sys
sys.path.insert(1, '//'.join((sys.path[0]).split('\\')[:-1]))

from giraldi_pricing import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

if __name__ == '__main__':

    # calculates european call and put rhos and related derivatives accross variable times and moneyness states

    # 1: option price for different interest rate levels
    # 2: option price as a function of the interest rate
    # 3: option rho (z axis, DvegaDvol) in relation to moneyness (x axis) and time to expiration (t, y axis)

    kind = 'call'

    fixed_S0 = 50 
    fixed_t = 6/12
    fixed_K = 50
    fixed_r = 0.10
    fixed_vol = 0.30

    p = 200 # recommended: 200, computational time grows in p^2

    ##############################################################################

    # options subject to different interest rates

    S0  = np.linspace(fixed_S0*.5, fixed_S0*1.5, p)

    fig, ax = plt.subplots()

    ax.set_ylabel('option price', fontsize=16)
    ax.yaxis.set_label_coords(-0.075,.5)
    ax.yaxis.set_tick_params(labelsize=16)

    ax.axhline(0, c='k')
    ax.axvline(0, c='k')
    
    if kind == 'call':
        axis =  100*(S0/fixed_K-1)
    if kind == 'put':
        axis = -100*(S0/fixed_K-1)
        ax.invert_xaxis()

    rates = [0 + i*0.025 for i in range(5)]
    for i, r in enumerate(rates):
        d1 = get_d1(S0, fixed_t, fixed_K, r, fixed_vol)
        d2 = get_d2(fixed_t, fixed_vol, d1)

        if i == 0:
            lns  = ax.plot(axis, expir_value(S0, fixed_K, kind), lw=2, c='black'   , label='expiration value')

        lns += ax.plot(axis, price(S0, fixed_t, fixed_K, r, d1, d2, kind), lw=2, label=f'r: {int((r)*100)}%')


    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, fontsize=16, framealpha=1)

    ax.set_xlabel('moneyness', fontsize=16)
    ax.xaxis.set_tick_params(labelsize=16)
    ax.set_title(f'long {kind} (t={fixed_t*12} months, K={fixed_K}, r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    ax.grid(alpha=0.5)

    del lns, labs, S0, axis, d1, d2, rates, i, r

    plt.show()

    ##############################################################################

     # different moneyness accross time

    r = np.linspace(0,.15,p)
    moneyness_chg = 0.05

    fig, ax = plt.subplots()

    for i in range(3):
        S0_loop = fixed_S0 * ((1-moneyness_chg) + i*moneyness_chg)
        d1 = get_d1(S0_loop, fixed_t, fixed_K, r, fixed_vol)
        d2 = get_d2(fixed_t, fixed_vol, d1)
        ax.plot(r*100, price(S0_loop, fixed_t, fixed_K, r, d1, d2, kind), lw=2)

    ax.set_title(f'{kind} price accross interest rate levels', fontsize=24)

    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.set_xlabel('interest rate', fontsize=16)
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    ax.set_ylabel('option price', fontsize=16)
    ax.grid(alpha=0.5)

    states = [f'{moneyness_chg*100}% out of the money', 'on the money', f'{moneyness_chg*100}% in the money']
    if kind == 'put':
        states.reverse()
    ax.legend(states, fontsize=16)

    del S0_loop, i, r, states, moneyness_chg

    plt.show()

    ##############################################################################

    # X = S0, Y = t, Z = theta

    S0 = np.linspace(fixed_K*.5, fixed_K*1.5, p)
    t = np.linspace(1/360, 3/12, p)

    S0_grid, t_grid = np.meshgrid(S0, t)
    zrho = np.array([rho(
        y, fixed_K, fixed_r,
        get_d2(y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol)),
        kind
    ) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    zrho = zrho.reshape(S0_grid.shape)

    # zvanna = np.array([vanna(fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol), get_d2(y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol))) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    # zvanna = zvanna.reshape(S0_grid.shape)

    # m = plt.cm.ScalarMappable()
    # fcolors = m.to_rgba(zvanna)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    if kind == 'call':
        ax.plot_wireframe( 100*(S0_grid/fixed_K-1), t_grid*12, zrho, color='tab:blue', rstride=10, cstride=10)
    elif kind == 'put':
        ax.plot_wireframe(-100*(S0_grid/fixed_K-1), t_grid*12, zrho, color='tab:blue', rstride=10, cstride=10)
        ax.invert_xaxis()
    
    ax.set_title(f'{kind} rho for r = {fixed_r*100}%, vol = {fixed_vol*100}%', fontsize=24)
    ax.set_xlabel('moneyness')
    ax.set_ylabel('time to expiration (months)')
    ax.set_zlabel('rho')
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    # fig.colorbar(m, ax=ax, label='vanna')

    ax.grid(alpha=0.5)

    del S0, t, S0_grid, t_grid, zrho

    plt.show()