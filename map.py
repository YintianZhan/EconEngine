import numpy as np
import pandas as pd

class Map:
    def __init__(self, width, length) -> None:
        self.width = width
        self.length = length
        self.map = [[None for j in range(self.width)] for i in range(self.length)]

    def populate_resources(self, resource_list, location_list):
        assert len(resource_list) == len(location_list)
        for i in range(len(resource_list)):
            self.map[location_list[i][0]][location_list[i][1]] = resource_list[i]

    def print_map(self):
        print(self.map)


if __name__ == "__main__":
    map = Map(2,2)
    map.populate_resources(['fish','apple','water','wood'],[(0,0),(0,1),(1,0),(1,1)])
    map.print_map()