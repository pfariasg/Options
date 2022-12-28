import numpy as np
import pandas as pd
from loguru import logger

class Option:
    def __init__(self, option_type, strike, direction, quantity, price, exotic):
        self.option_type = option_type
        self.strike = strike
        self.direction = direction
        self.quantity = quantity
        self.price = price
        self.exotic = exotic

        if self.exotic != False:
            raise NotImplementedError(f'Option type not implemented: {exotic}')

    def exp_value(self, base):
                
        if self.option_type == 'call':
            if self.direction == 'long':
                return self.quantity * (np.maximum(base - self.strike, 0) - self.price)
            elif self.direction == 'short':
                return self.quantity * (- (np.maximum(base - self.strike, 0) - self.price))
        
        elif self.option_type == 'put':
            if self.direction == 'long':
                return self.quantity * (np.maximum(self.strike - base, 0) - self.price)
            elif self.direction == 'short':
                return self.quantity * (- (np.maximum(self.strike - base, 0) - self.price))
    
class Asset:
    def __init__(self, direction, quantity, price):
        # self.current_price = current_price
        self.direction = direction
        self.quantity = quantity
        self.price = price
    
    def exp_value(self, base):      
        if self.direction == 'long':
            return self.quantity * (base - self.price)
        elif self.direction == 'short':
            return self.quantity * (- (base - self.price))

def create_option(option_type, strike, direction, quantity, price=0, exotic=False):
    x = Option(option_type, strike, direction, quantity, price, exotic)
    assets.append(x)

    return x

def create_asset(direction, quantity, price):
    x = Asset(direction, quantity, price)
    assets.append(x)

    return x

assets = []