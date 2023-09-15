import numpy as np
from resource_recipe import Recipe

class Resource:
    def __init__(self, name, consumption_utility, decay, recipe) -> None:
        self.name = name
        self.consumption_utility = consumption_utility
        self.decay = decay
        self.recipe = recipe
        
if __name__ == "__main__":
    r = Resource('apple', 1, 0.8, None)