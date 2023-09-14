import numpy as np
import pandas as pd

class Agent:
    def __init__(self, name = 'Alex', age = 20, location = (0,0)) -> None:
        self.name = name
        self.age = age
        self.hp = 100 - max((20 - self.age), 0) * 5 - max((self.age - 50), 0) * 5
        self.location = location
    
    def describe(self):
        print('The agent {} is {} years old, with {:.2f} hp, and is at {}'.format(self.name, self.age, self.hp, self.location))




a = Agent()
a.describe()