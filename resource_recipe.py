import numpy as np

class Recipe:
    def __init__(self, time, inputs, input_units, output, output_units, requires_location = False) -> None:
        assert len(inputs) == len(input_units)
        self.time = time
        self.inputs = inputs
        self.input_units = input_units
        self.output = output
        self.output_units = output_units
        self.requires_location = requires_location

    def describe(self):
        print('time:')
        print('{:.2f} hrs'.format(self.time))
        print('inputs:')
        for i in range(len(self.inputs)):
            print(self.inputs[i], self.input_units[i])
        print('outputs:')
        print(self.output, self.output_units)

if __name__ == "__main__":
    recipe = Recipe(time = 0.5, inputs = ['wood','fish'], input_units = [1,2], output = 'cooked food', output_units = 1)
    recipe.describe()
    
