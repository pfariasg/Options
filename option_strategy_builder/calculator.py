import matplotlib.pyplot as plt
import numpy as np
from objects import *

start = 0
end = 100

base = np.linspace(start, end, precision:=100000)

# create_option(option_type='call', strike=95, direction='long', quantity=1, price=11.55)
# create_option(option_type='call', strike=84, direction='short', quantity=1, price=16.1)
# create_option(option_type='put', strike=83, direction='short', quantity=1, price=11.65)
# create_option(option_type='put', strike=45, direction='long', quantity=1, price=1.63)

# create_option(option_type='put', strike=75, direction='short', quantity=1, price=8.85)
# create_option(option_type='call', strike=90, direction='short', quantity=1, price=13.42)
# create_option(option_type='call', strike=95, direction='long', quantity=1, price=11.05)

create_option(option_type='call', strike=45, direction='long', quantity=1, price=0)
create_option(option_type='call', strike=55, direction='short', quantity=1, price=0)
# create_option(option_type='call', strike=55, direction='long', quantity=1, price=0)


# create_asset(direction='short', quantity=1, price=84)

value = np.zeros(precision)
for asset in assets:
    value += asset.exp_value(base)

# value /= 5

fig = plt.figure()
ax = fig.add_subplot()


# ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks().tolist()])
ax.axhline(0, c='k', lw=1)
ax.plot(base, value, lw=2.5, c='k')
ax.grid(which='both')
ax.set_xlabel('St')
ax.set_ylabel('CS(K=50,∆K=5,t=0)')
# ax.set_ylabel('c(K=50,t=0) ')
ax.set_title('call spread')


plt.show()