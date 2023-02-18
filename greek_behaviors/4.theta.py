import sys
sys.path.insert(1, '//'.join((sys.path[0]).split('\\')[:-1]))

from giraldi_pricing import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

if __name__ == '__main__':
    # calculates european call and put thetas is relation to fixed and variable parameters. It displays the following graphs:

    # 1: option price (y axis) for different moneyness as time passes (x axis)
    # 2: call and put theta (y axis) in relation to moneyness (x axis)
    # 3: theta (y axis) breakdown in driftless theta (function of vol) and yield theta (function of yield)
    # 4: option theta (z axis) in relation to stock price (S0, x axis) and time to expiration (t, y axis)
    # 5: option yield and driftless theta (z axis) in relation to stock price (S0, x axis) and time to expiration (t, y axis)

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

    # price of options with different moneyness accross time

    t = np.linspace(.00001/360,6/12,p)
    moneyness_chg = 0.05

    fig, ax = plt.subplots()
    for i in range(3):
        S0_loop = fixed_S0 * ((1-moneyness_chg) + i*moneyness_chg)
        d1 = get_d1(S0_loop, t, fixed_K, fixed_r, fixed_vol)
        d2 = get_d2(t, fixed_vol, d1)
        ax.plot(t*12, price(S0_loop, t, fixed_K, fixed_r, d1, d2, kind), lw=2)

    ax.set_title(f'{kind} price accross time', fontsize=24)

    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.set_xlabel('time to expiration (months)', fontsize=16)
    ax.set_ylabel('price', fontsize=16)
    ax.invert_xaxis()
    ax.grid(alpha=0.5)

    states = [f'{moneyness_chg*100}% out of the money', 'on the money', f'{moneyness_chg*100}% in the money']
    if kind == 'put':
        states.reverse()
    ax.legend(states, fontsize=16)

    del S0_loop, i, t, states, moneyness_chg

    plt.show()

    ##############################################################################

    ### option theta for call and put

    S0 = np.linspace(fixed_K*.5, fixed_K*1.5, p)

    fig, ax = plt.subplots()
    
    d1 = get_d1(S0, fixed_t, fixed_K, fixed_r, fixed_vol)
    d2 = get_d2(fixed_t, fixed_vol, d1)

    ax.axhline(0, c='k', lw=.75)
    
    
    lns0 = ax.plot(S0, theta(S0, fixed_t, fixed_K, fixed_r, fixed_vol, d1, d2, 'call'), lw=2, c='tab:orange', label='call theta')
    lns1 = ax.plot(S0, theta(S0, fixed_t, fixed_K, fixed_r, fixed_vol, d1, d2, 'put'), lw=2, c='tab:blue', label='put theta')
    ax.axvline(fixed_K, c='k', label='strike')
    # plotting

    lns = lns0 + lns1
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, fontsize=16, loc=6, framealpha=1)

    ax.set_title(f'long call and put (t={fixed_t*12} months, r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
    ax.set_xlabel('underlying price', fontsize=16)
    ax.set_ylabel('option theta', fontsize=16)
    ax.xaxis.set_tick_params( labelsize=16)
    ax.yaxis.set_tick_params( labelsize=16)
    ax.yaxis.set_label_coords(-0.05, .5)

    ax.grid(alpha=0.5)

    del S0, d1, d2, lns, lns0, lns1, labs

    plt.show()

    ##############################################################################

    # option theta breakdown

    S0 = np.linspace(fixed_K*.5, fixed_K*1.5, p)

    fig, ax = plt.subplots()
    
    d1 = get_d1(S0, fixed_t, fixed_K, fixed_r, fixed_vol)
    d2 = get_d2(fixed_t, fixed_vol, d1)

    ax.axhline(0, c='k')

    if kind == 'call':
        axis =  100*(S0/fixed_K-1)
    elif kind == 'put':
        axis = -100*(S0/fixed_K-1)
        ax.invert_xaxis()
        
    lns0 = ax.plot(axis, theta(S0, fixed_t, fixed_K, fixed_r, fixed_vol, d1, d2, kind), lw=2, c='tab:orange', label='theta')
    lns1 = ax.plot(axis, theta_driftless(S0, fixed_t, fixed_vol, d1), lw=2, c='tab:blue', label='driftless theta')
    lns2 = ax.plot(axis, theta_yield(fixed_t, fixed_K, fixed_r, d2, kind), lw=2, c='tab:green', label='yield theta')
    

    # plotting
    lns = lns0 + lns1 + lns2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, fontsize=16, loc=6, framealpha=1)

    ax.set_title(f'long {kind} (t={fixed_t*12} months, r={fixed_r*100}%, vol={fixed_vol*100}%)', fontsize=24)
    ax.set_xlabel(   'moneyness', fontsize=16)
    ax.set_ylabel('option theta', fontsize=16)
    ax.xaxis.set_tick_params( labelsize=16)
    ax.yaxis.set_tick_params( labelsize=16)
    ax.yaxis.set_label_coords(-0.05, .5)
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())

    ax.grid(alpha=0.5)

    del S0, d1, d2, lns, labs

    plt.show()


    ##############################################################################

    # X = S0, Y = t, Z = theta

    S0 = np.linspace(fixed_K*.5, fixed_K*1.5, p)
    t = np.linspace(7/360, 2/12, p)

    S0_grid, t_grid = np.meshgrid(S0, t)
    ztheta = np.array([theta(
        x, y, fixed_K, fixed_r, fixed_vol,
        get_d1(x, y, fixed_K, fixed_r, fixed_vol),
        get_d2(y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol)),
        kind
    ) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    ztheta = ztheta.reshape(S0_grid.shape)

    # zvanna = np.array([vanna(fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol), get_d2(y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol))) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    # zvanna = zvanna.reshape(S0_grid.shape)

    # m = plt.cm.ScalarMappable()
    # fcolors = m.to_rgba(zvanna)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    if kind == 'call':
        ax.plot_wireframe( 100*(S0_grid/fixed_K-1), t_grid*12, ztheta, color='tab:blue', rstride=10, cstride=10)
        ax.plot_surface(   110*(S0_grid/fixed_K-1), t_grid*12, t_grid*0, alpha=.25, color='gray')
    elif kind == 'put':
        ax.plot_wireframe(-100*(S0_grid/fixed_K-1), t_grid*12, ztheta, color='tab:blue', rstride=10, cstride=10)
        ax.plot_surface(  -100*(S0_grid/fixed_K-1), t_grid*12, t_grid*0, alpha=.25, color='gray')
        ax.invert_xaxis()
    
    ax.set_title(f'{kind} theta for r = {fixed_r*100}%, vol = {fixed_vol*100}%', fontsize=24)
    ax.set_xlabel('moneyness')
    ax.set_ylabel('time to expiration (months)')
    ax.set_zlabel('theta')
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    # fig.colorbar(m, ax=ax, label='vanna')

    ax.grid(alpha=0.5)

    del S0, t, S0_grid, t_grid, ztheta

    plt.show()

       ##############################################################################

    # X = S0, Y = t, Z = yield and driftless theta

    S0 = np.linspace(fixed_K*.5, fixed_K*1.5, p)
    t = np.linspace(7/360, 2/12, p)

    S0_grid, t_grid = np.meshgrid(S0, t)
    ztheta_driftless = np.array([theta_driftless(
        x, y, fixed_vol,
        get_d1(x, y, fixed_K, fixed_r, fixed_vol)
    ) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    ztheta_driftless = ztheta_driftless.reshape(S0_grid.shape)

    ztheta_yield = np.array([theta_yield(
        y, fixed_K, fixed_r,
        get_d2(y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol)),
        kind
    ) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    ztheta_yield = ztheta_yield.reshape(S0_grid.shape)

    # zvanna = np.array([vanna(fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol), get_d2(y, fixed_vol, get_d1(x, y, fixed_K, fixed_r, fixed_vol))) for x,y in zip(np.ravel(S0_grid), np.ravel(t_grid))])
    # zvanna = zvanna.reshape(S0_grid.shape)

    # m = plt.cm.ScalarMappable()
    # fcolors = m.to_rgba(zvanna)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    if kind == 'call':
        ax.plot_wireframe( 100*(S0_grid/fixed_K-1), t_grid*12, ztheta_driftless, color='tab:blue', rstride=10, cstride=10, label='theta driftless')
        ax.plot_wireframe( 100*(S0_grid/fixed_K-1), t_grid*12, ztheta_yield, color='tab:orange', rstride=10, cstride=10, label='theta yield')
        ax.plot_surface(   110*(S0_grid/fixed_K-1), t_grid*12, t_grid*0, alpha=.25, color='gray')
    elif kind == 'put':
        ax.plot_wireframe(-100*(S0_grid/fixed_K-1), t_grid*12, ztheta_driftless, color='tab:blue', rstride=10, cstride=10, label='theta driftless')
        ax.plot_wireframe(-100*(S0_grid/fixed_K-1), t_grid*12, ztheta_yield, color='tab:orange', rstride=10, cstride=10, label='theta yield')
        ax.plot_surface(  -110*(S0_grid/fixed_K-1), t_grid*12, t_grid*0, alpha=.25, color='gray')
        ax.invert_xaxis()
    
    ax.legend(fontsize=16, loc=6, framealpha=1)

    ax.set_title(f'{kind} theta for r = {fixed_r*100}%, vol = {fixed_vol*100}%', fontsize=24)
    ax.set_xlabel('moneyness')
    ax.set_ylabel('time to expiration (months)')
    ax.set_zlabel('theta')
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
    # fig.colorbar(m, ax=ax, label='vanna')

    ax.grid(alpha=0.5)

    del S0, t, S0_grid, t_grid, ztheta_driftless, ztheta_yield

    plt.show()