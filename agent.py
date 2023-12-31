import numpy as np
import pandas as pd
from resource import Resource
from resource_dict import resource_dict
from map import Map
from model import Linear_QNet, QTrainer
from collections import deque
import random
import torch
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
TOTAL_HRS = 24

class Agent:
    def __init__(self, name = 'Alex', age = 20, location = (0,0), efficiency = 1, map = None) -> None:
        self.name = name
        self.age = age
        self.map = map
        self.hp = 100 - max((20 - self.age), 0) * 5 - max((self.age - 50), 0) * 5
        self.location = location
        self.efficiency = efficiency
        self.product = {resource_name:0 for resource_name in resource_dict.keys()}
        self.utilities = 0
        self.hrs_spent = 0
        self.last_movement = None
        self.last_action = None

        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(10, 256, 9)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def describe(self, map = None):
        print('The agent {} is {} years old, with {:.2f} hp {:.2f} utilities, and is at {}'.format(self.name, self.age, self.hp, self.utilities, self.location))
        print('{} has:'.format(self.name))
        if len(self.product) > 0:
            for resource, units in self.product.items():
                print('{} {:.2f}'.format(resource, units))
        else:
            print('nothing')

        if map is not None:
            print('{} is at:'.format(self.name))
            map.print_map([self.location])
    
    def act(self, model_action):
        if model_action[0] == 1:
            reward = self.move_location((0,1), self.map)
        elif model_action[1] == 1:
            reward = self.move_location((1,0), self.map)
        elif model_action[2] == 1:
            reward = self.move_location((0,-1), self.map)
        elif model_action[3] == 1:
            reward = self.move_location((-1,0), self.map)
        elif model_action[4] == 1:
            reward = self.produce_local(self.map)
        elif model_action[5] == 1:
            reward = self.cook()
        elif model_action[6] == 1:
            reward = self.consume('apple')
        elif model_action[7] == 1:
            reward = self.consume('fish')
        elif model_action[8] == 1:
            reward = self.consume('cooked fish')
        self.hrs_spent += 1
        game_over = (self.hp == 0) or (self.hrs_spent == TOTAL_HRS)

        return reward, game_over, self.utilities

    def reset(self):
        self.hp = 100 - max((20 - self.age), 0) * 5 - max((self.age - 50), 0) * 5
        self.location = (0, 0)
        self.product = {resource_name:0 for resource_name in resource_dict.keys()}
        self.utilities = 0
        self.hrs_spent = 0
        self.last_movement = None
        self.last_action = None

    def produce_resource(self, resource, map = None):
        try:
            if not resource_dict[resource].recipe.requires_location or (map != None and resource == map.map[self.location[0]][self.location[1]]):
                for i in range(len(resource_dict[resource].recipe.inputs)):
                    input_resource = resource_dict[resource].recipe.inputs[i]
                    input_resource_units = resource_dict[resource].recipe.input_units[i]
                    assert self.product[input_resource] >= input_resource_units
                    self.product[input_resource] -= input_resource_units
                self.product[resource] = self.product.get(resource, 0) + self.efficiency * resource_dict[resource].recipe.output_units
                self.last_action = 'produce'
                print('{} spent {} hrs and produced {} {}'.format(self.name, resource_dict[resource].recipe.time, resource_dict[resource].recipe.output_units, resource))
            else:
                print('{} could not produce {}'.format(self.name, resource))
        except:
            print('{} could not produce {}'.format(self.name, resource))

        return -0.05

    def produce_local(self, map):
        return self.produce_resource(map.map[self.location[0]][self.location[1]], map)

    def cook(self):
        return self.produce_resource('cooked fish')
    
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
            self.last_action = 'trade'
        except Exception as e:
            print('{} could not trade'.format(self.name))
        return 0

    def consume(self, resource):
        if self.product[resource] >= 1:
            self.utilities += resource_dict[resource].consumption_utility
            self.hp += resource_dict[resource].health_points
            self.product[resource] -= 1
            self.last_action = 'eat'
            print('{} ate {}'.format(self.name, resource))
        else:
            print('{} could not eat {}'.format(self.name, resource))
        return resource_dict[resource].consumption_utility

    def product_decay(self):
        if len(self.product) > 0:
            for resource, units in self.product.items():
                self.product[resource] *= units.decay

    def move_location(self, step, map):
        try:
            assert abs(sum(step)) == 1
            assert self.location[0] + step[0] >= 0 and self.location[0] + step[0] < map.width
            assert self.location[1] + step[1] >= 0 and self.location[1] + step[1] < map.length
            old_location = self.location
            self.location = (self.location[0] + step[0], self.location[1] + step[1])
            self.last_movement = step
            self.last_action = 'move'
            print('{} moved from {} to {}'.format(self.name, old_location, self.location))
        except:
            print('{} could not move {} from {}'.format(self.name, step, self.location))
        return -0.05

    def get_available_actions(self):
        action_availability = []
        # move actions
        if self.location[1] == self.map.width - 1 or self.last_movement == (0,-1):
            action_availability.append(-100)
        else:
            action_availability.append(1)
        if self.location[0] == self.map.length - 1 or self.last_movement == (-1,0):
            action_availability.append(-100)
        else:
            action_availability.append(1)
        if self.location[1] == 0 or self.last_movement == (0,1):
            action_availability.append(-100)
        else:
            action_availability.append(1)
        if self.location[0] == 0 or self.last_movement == (1,0):
            action_availability.append(-100)
        else:
            action_availability.append(1)

        # produce actions
        if self.map.map[self.location[0]][self.location[1]] not in resource_dict.keys():
            action_availability.append(-100)
        else:
            action_availability.append(1)
        if self.product['fish'] < 2 or self.product['wood'] < 1:
            action_availability.append(-100)
        else:
            action_availability.append(1)  
        
        #consume
        if self.product['apple'] < 1 or self.last_action == 'move':
            action_availability.append(-100)
        else:
            action_availability.append(1)
        if self.product['fish'] < 1 or self.last_action == 'move':
            action_availability.append(-100)
        else:
            action_availability.append(1)
        if self.product['cooked fish'] < 1 or self.last_action == 'move':
            action_availability.append(-100)
        else:
            action_availability.append(1)     

        return action_availability  
    

    def get_state(self):

        state = [
            # location
            self.location[0],
            self.location[1],

            # product
            self.product['apple'],
            self.product['fish'],
            self.product['wood'],
            self.product['cooked fish'],

            # health
            self.hp,

            # last action
            self.last_action == 'move',
            self.last_action == 'eat',
            self.last_action == 'produce'
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        available_actions = np.array(self.get_available_actions())
        self.epsilon = 100 - self.n_games
        final_move = [0,0,0,0,0,0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            r = np.random.uniform(size=9)
            # move = random.randint(0, 8)
            available_r = np.array([r[i] * available_actions[i] for i in range(len(r))])
            move = np.argmax(available_r)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            # import pdb
            # pdb.set_trace()
            available_prediction = torch.add(prediction, torch.tensor(available_actions))
            # print(prediction)
            # print(available_prediction)
            # available_prediction = [prediction[i] * available_actions[i] for i in range(len(prediction))]
            move = torch.argmax(available_prediction).item()
            # print(move)
            # import pdb
            # pdb.set_trace()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    map = Map(2,2)
    map.populate_resources(['fish','apple','water','wood'],[(0,0),(0,1),(1,0),(1,1)])
    agent = Agent(map = map)

    while agent.n_games <= 400:
        # get old state
        state_old = agent.get_state()

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = agent.act(final_move)
        state_new = agent.get_state()

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            print('###########one day done############')
            # train long memory, plot result
            agent.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    # map = Map(2,2)
    # map.populate_resources(['fish','apple','water','wood'],[(0,0),(0,1),(1,0),(1,1)])
    # a = Agent(map = map)
    # a.describe(map = map)
    # print(a.get_available_actions())
    # a.move_location(step = (0, 1), map = map)
    # print(a.get_available_actions())
    # a.describe(map = map)
    # a.produce_resource('apple', map)
    # a.move_location(step = (1,0), map = map)
    # print(a.get_available_actions())
    # a.produce_resource('wood', map)
    # a.move_location(step = (-1,0), map = map)
    # a.move_location(step = (0,-1), map = map)
    # a.produce_resource('fish', map)
    # a.produce_resource('fish', map)
    # a.produce_resource('cooked fish')
    # a.produce_resource('fish', map)
    # a.trade(['apple'], [5], ['cooked fish','fish'], [1,1])
    # a.consume('apple')
    # a.move_location(step = (1,0), map = map)
    # a.describe(map = map)
    train()