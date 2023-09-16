import numpy as np
import pandas as pd
from resource import Resource
from resource_dict import resource_dict
from map import Map

class Agent:
    def __init__(self, name = 'Alex', age = 20, location = (0,0), efficiency = 1) -> None:
        self.name = name
        self.age = age
        self.hp = 100 - max((20 - self.age), 0) * 5 - max((self.age - 50), 0) * 5
        self.location = location
        self.efficiency = efficiency
        self.product = {}
        self.utilities = 0

    def describe(self, map = None):
        print('The agent {} is {} years old, with {:.2f} hp, and is at {}'.format(self.name, self.age, self.hp, self.location))
        print('{} has:'.format(self.name))
        if len(self.product) > 0:
            for resource, units in self.product.items():
                print('{} {:.2f}'.format(resource, units))
        else:
            print('nothing')

        if map is not None:
            print('{} is at:'.format(self.name))
            map.print_map([self.location])

    def produce_resource(self, resource, map = None):
        if resource_dict[resource].recipe.requires_location and map != None and resource == map.map[self.location[0]][self.location[1]]:
            for i in range(len(resource_dict[resource].recipe.inputs)):
                input_resource = resource_dict[resource].recipe.inputs[i]
                input_resource_units = resource_dict[resource].recipe.input_units[i]
                assert self.product[input_resource] >= input_resource_units
                self.product[input_resource] -= input_resource_units
            self.product[resource] = self.product.get(resource, 0) + self.efficiency * resource_dict[resource].recipe.output_units
            print('{} spent {} hrs and produced {} {}'.format(self.name, resource_dict[resource].recipe.time, resource_dict[resource].recipe.output_units, resource))
        else:
            print('{} could not produce {}'.format(self.name, resource))

    def trade(self, inflows, inflow_units, outflows, outflow_units):
        try:
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
        except Exception as e:
            print('{} could not trade'.format(self.name))

    def consume(self, resource):
        if self.product[resource] >= 1:
            self.utilities += resource_dict[resource].consumption_utility
            self.hp += resource_dict[resource].health_points
            self.product[resource] -= 1
        else:
            print('{} could not eat {}'.format(self.name, resource))

    def product_decay(self):
        if len(self.product) > 0:
            for resource, units in self.product.items():
                self.product[resource] *= units.decay

    def act(self):
        pass

    def move_location(self, step, map):
        assert abs(sum(step)) == 1
        assert self.location[0] + step[0] >= 0 and self.location[0] + step[0] < map.width
        assert self.location[1] + step[1] >= 0 and self.location[1] + step[1] < map.length
        old_location = self.location
        self.location = (self.location[0] + step[0], self.location[1] + step[1])
        print('{} moved from {} to {}'.format(self.name, old_location, self.location))

if __name__ == "__main__":
    map = Map(2,2)
    map.populate_resources(['fish','apple','water','wood'],[(0,0),(0,1),(1,0),(1,1)])
    a = Agent()
    a.describe(map = map)
    a.move_location(step = [0,1], map = map)
    a.produce_resource('apple', map)
    a.move_location(step = [1,0], map = map)
    a.produce_resource('wood', map)
    a.move_location(step = [-1,0], map = map)
    a.move_location(step = [0,-1], map = map)
    a.produce_resource('fish', map)
    a.produce_resource('fish', map)
    a.produce_resource('cooked fish')
    a.produce_resource('fish', map)
    a.trade(['apple'], [5], ['cooked fish','fish'], [1,1])
    a.consume('fish')
    a.move_location(step = [1,0], map = map)
    a.describe(map = map)