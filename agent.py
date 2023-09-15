import numpy as np
import pandas as pd
from resource import Resource
from resource_dict import resource_dict

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
        print('{} has:'.format(self.name))
        if len(self.product) > 0:
            for resource, units in self.product.items():
                print('{} {:.2f}'.format(resource, units))
        else:
            print('nothing')

    def produce_resource(self, resource):
        for i in range(len(resource_dict[resource].recipe.inputs)):
            input_resource = resource_dict[resource].recipe.inputs[i]
            input_resource_units = resource_dict[resource].recipe.input_units[i]
            assert self.product[input_resource] >= input_resource_units
            self.product[input_resource] -= input_resource_units
        self.product[resource] = self.product.get(resource, 0) + self.efficiency * resource_dict[resource].recipe.output_units
        print('{} spent {} hrs and produced {} {}'.format(self.name, resource_dict[resource].recipe.time, resource_dict[resource].recipe.output_units, resource))

    def trade(self, inflows, inflow_units, outflows, outflow_units):
        assert len(inflows) == len(inflow_units)
        assert len(outflows) == len(outflow_units)
        
        for i in range(len(outflows)):
            assert self.product[outflows[0]] >= outflow_units[i]
            self.product[outflows[i]] = self.product.get(outflows[0], 0) - outflow_units[i]

        for i in range(len(inflows)):
            self.product[inflows[i]] = self.product.get(inflows[i], 0) + inflow_units[i]
        
        print('{} traded: '.format(self.name))
        for i in range(len(outflows)):
            print(outflows[i], outflow_units[i])
        print('for: ')
        for i in range(len(inflows)):
            print(inflows[i], inflow_units[i])

    


if __name__ == "__main__":
    a = Agent()
    a.describe()
    a.produce_resource('wood')
    a.produce_resource('fish')
    a.produce_resource('fish')
    a.produce_resource('cooked fish')
    a.produce_resource('fish')
    a.trade(['apple'], [5], ['cooked fish','fish'], [1,1])
    a.describe()