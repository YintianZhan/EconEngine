import numpy as np
from resource_recipe import Recipe

class Resource:
    def __init__(self, name, consumption_utility, decay, health_points, recipe) -> None:
        self.name = name
        self.consumption_utility = consumption_utility
        self.decay = decay
        self.recipe = recipe
        self.health_points = health_points
        
if __name__ == "__main__":
    r = Resource('apple', 1, 0.8, None)