import matplotlib.pyplot as plt
import numpy as np
from objects import *

start = 0
end = 100

base = np.linspace(start, end, precision:=1000)

create_option(option_type='call', strike=55, direction='long', quantity=1, price=0)
create_option(option_type='put', strike=45, direction='short', quantity=1, price=0)

# create_asset(direction='long', quantity=100000, price=49)

value = np.zeros(precision)
for asset in assets:
    value += asset.exp_value(base)

fig = plt.figure()
ax = fig.add_subplot()

ax.plot(base, value)
ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks().tolist()])
ax.axhline(0, c='k', lw=1)
ax.grid(which='both')

plt.show()