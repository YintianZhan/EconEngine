from resource import Resource
from resource_recipe import Recipe

resource_dict = {'apple': Resource(name = 'apple', consumption_utility = 1, decay = 0.8, 
                                   recipe = Recipe(time = 1, 
                                                   inputs = [], 
                                                   input_units = [], 
                                                   output = 'apple', 
                                                   output_units = 2)),
                'fish':   Resource(name = 'fish',  consumption_utility = 0.5, decay = 0.4, 
                                   recipe = Recipe(time = 1, 
                                                   inputs = [], 
                                                   input_units = [], 
                                                   output = 'fish', 
                                                   output_units = 1)),
                'wood':   Resource(name = 'fish',  consumption_utility = 0, decay = 0.95, 
                                   recipe = Recipe(time = 1, 
                                                   inputs = [], 
                                                   input_units = [], 
                                                   output = 'wood', 
                                                   output_units = 2)),
                'cooked fish':   Resource(name = 'cooked fish',  consumption_utility = 2.5, decay = 0.6, 
                                   recipe = Recipe(time = 1, 
                                                   inputs = ['wood','fish'], 
                                                   input_units = [1,2], 
                                                   output = 'cooked fish', 
                                                   output_units = 2)),}

