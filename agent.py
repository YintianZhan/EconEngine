import numpy as np
import pandas as pd
from resource import Resource
from resource_dict import *

class Agent:
    def __init__(self, name = 'Alex', age = 20, location = (0,0), efficiency = 1) -> None:
        self.name = name
        self.age = age
        self.hp = 100 - max((20 - self.age), 0) * 5 - max((self.age - 50), 0) * 5
        self.location = location
        self.efficiency = efficiency
        self.product = {}
        self.utilities = 0

    
    def describe(self):
        print('The agent {} is {} years old, with {:.2f} hp, and is at {}'.format(self.name, self.age, self.hp, self.location))

    def produce_resource(self, resource):
        for i in range(len(resources[resource].recipe.inputs)):
            input_resource = resources[resource].recipe.inputs[i]
            input_resource_units = resources[resource].recipe.input_units[i]
            assert self.product[input_resource] > input_resource_units
            self.product[input_resource] -= input_resource_units

        self.product[resource] = self.product.get(resource, 0) + self.efficiency * resources[resource].output_per_hour
        print('{} produced {} {}'.format(self.name, ))

    


if __name__ == "__main__":
    a = Agent()
    a.describe()