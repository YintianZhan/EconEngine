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

# New modular components
from environments import load_environment, get_preset_config
from rewards import SimpleUtilityReward, OpportunityCostReward
from metrics import MetricCollector, MetricLogger

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


def train_with_config(config_path=None,
                      reward_type='simple',
                      experiment_name=None,
                      save_metrics=True,
                      verbose=True,
                      num_training_episodes=400,
                      num_test_episodes=100):
    """
    Train agent using configuration-driven approach.

    Args:
        config_path: Path to environment YAML config, or preset name (e.g., 'simple_2x2')
        reward_type: 'simple' or 'opportunity_cost'
        experiment_name: Name for logging (default: auto-generated)
        save_metrics: Whether to save metrics to disk
        verbose: Print progress messages
        num_training_episodes: Number of training episodes (default: 400)
        num_test_episodes: Number of test episodes (default: 100)

    Returns:
        Dict with training results and paths to logs
    """
    # Load environment configuration
    if config_path is None:
        config_path = 'simple_2x2'  # Default to baseline

    try:
        # Try loading as preset first
        if not config_path.endswith('.yaml'):
            env_config = get_preset_config(config_path)
        else:
            env_config = load_environment(config_path)
    except FileNotFoundError:
        print(f"Config '{config_path}' not found, using simple_2x2 baseline")
        env_config = get_preset_config('simple_2x2')

    if verbose:
        print(f"Loaded environment: {env_config}")

    # Create reward calculator
    if reward_type == 'simple':
        reward_calc = SimpleUtilityReward()
    elif reward_type == 'opportunity_cost':
        reward_calc = OpportunityCostReward()
    else:
        raise ValueError(f"Unknown reward type: {reward_type}")

    if verbose:
        print(f"Using reward calculator: {reward_calc}")

    # Initialize metrics collection
    metrics = MetricCollector()
    logger = MetricLogger(experiment_name=experiment_name) if save_metrics else None

    if logger and verbose:
        print(f"Logging to: {logger.get_log_dir()}")

    # Save configuration
    if logger:
        config_dict = {
            'environment': env_config.name,
            'grid_size': env_config.grid_size,
            'episode_length': env_config.episode_length,
            'reward_type': reward_type,
            'reward_config': reward_calc.get_config(),
            'max_games': env_config.resources.get('max_games', 400) if hasattr(env_config.resources, 'get') else 400,
        }
        logger.log_config(config_dict)

    # Create map from config
    map_obj = Map(*env_config.grid_size)

    resource_locations = env_config.get_resource_locations()
    resource_names = list(resource_locations.keys())
    resource_coords = [locs[0] for locs in resource_locations.values()]  # Take first location for each

    map_obj.populate_resources(resource_names, resource_coords)

    # Create agent
    agent_start = env_config.agent_start
    agent = Agent(map=map_obj, location=agent_start)

    # Training loop
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    max_games = num_training_episodes

    if verbose:
        print(f"Starting training for {max_games} episodes...")

    while agent.n_games < max_games:
        metrics.reset_episode()

        # Episode loop
        while True:
            # Get old state
            state_old = agent.get_state()

            # Get move
            final_move = agent.get_action(state_old)

            # Perform move and get new state
            reward, done, score = agent.act(final_move)
            state_new = agent.get_state()

            # Log step metrics
            agent_data = {
                'location': agent.location,
                'inventory': agent.product.copy(),
                'hp': agent.hp,
                'utilities': agent.utilities,
            }
            metrics.log_step(
                step=agent.hrs_spent,
                state=state_old,
                action=final_move,
                reward=reward,
                next_state=state_new,
                done=done,
                agent_data=agent_data
            )

            # Train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)

            # Remember
            agent.remember(state_old, final_move, reward, state_new, done)

            if done:
                break

        # Episode ended
        if verbose:
            print(f'Episode {agent.n_games + 1} complete: score={score:.2f}, steps={agent.hrs_spent}')

        # Finalize episode metrics
        episode_summary = metrics.end_episode(agent.n_games)

        # Log to disk
        if logger:
            logger.log_episode(episode_summary, include_steps=(agent.n_games % 10 == 0))

        # Train long memory, plot result
        agent.reset()
        agent.n_games += 1
        agent.train_long_memory()

        if score > record:
            record = score
            agent.model.save()
            if verbose:
                print(f'New record: {record:.2f}')

        if verbose and agent.n_games % 10 == 0:
            print(f'Game {agent.n_games} | Score: {score:.2f} | Record: {record:.2f}')

        plot_scores.append(score)
        total_score += score
        mean_score = total_score / agent.n_games
        plot_mean_scores.append(mean_score)
        plot(plot_scores, plot_mean_scores)

    # Training complete - now run test episodes
    if verbose:
        print("\n" + "="*50)
        print("Training Complete! Starting Test Phase...")
        print(f"Running {num_test_episodes} test episodes (no learning, pure exploitation)")
        print("="*50)

    test_scores = []
    agent.epsilon = 0  # No exploration during test

    for test_episode in range(num_test_episodes):
        agent.reset()
        metrics.reset_episode()

        while True:
            state_old = agent.get_state()
            final_move = agent.get_action(state_old)
            reward, done, score = agent.act(final_move)
            state_new = agent.get_state()

            # Log metrics but don't train
            agent_data = {
                'location': agent.location,
                'inventory': agent.product.copy(),
                'hp': agent.hp,
                'utilities': agent.utilities,
            }
            metrics.log_step(
                step=agent.hrs_spent,
                state=state_old,
                action=final_move,
                reward=reward,
                next_state=state_new,
                done=done,
                agent_data=agent_data
            )

            if done:
                break

        # Log test episode with special marker
        episode_summary = metrics.end_episode(max_games + test_episode)
        episode_summary['is_test'] = True  # Mark as test episode

        if logger:
            logger.log_episode(episode_summary, include_steps=(test_episode % 10 == 0))

        test_scores.append(score)

        if verbose and (test_episode + 1) % 20 == 0:
            print(f'Test Episode {test_episode + 1}/100 | Score: {score:.2f} | Mean: {np.mean(test_scores):.2f}')

    # Test phase complete
    if verbose:
        print("\n" + "="*50)
        print("Test Phase Complete!")
        print(f"Test Mean Score: {np.mean(test_scores):.2f} ± {np.std(test_scores):.2f}")
        print(f"Test Max Score: {max(test_scores):.2f}")
        print(f"Training Mean Score: {mean_score:.2f}")
        print("="*50)

    # Create comprehensive summary
    training_summary = metrics.get_training_summary()
    training_summary['final_record'] = record
    training_summary['final_mean_score'] = mean_score
    training_summary['test_mean_score'] = float(np.mean(test_scores))
    training_summary['test_std_score'] = float(np.std(test_scores))
    training_summary['test_max_score'] = float(max(test_scores))
    training_summary['test_scores'] = test_scores

    if logger:
        logger.log_training_summary(training_summary)

    if verbose:
        print("\n" + "="*50)
        print("Training + Test Complete!")
        print(f"Training Record: {record:.2f}")
        print(f"Training Mean: {mean_score:.2f}")
        print(f"Test Mean: {np.mean(test_scores):.2f}")
        if logger:
            print(f"Logs saved to: {logger.get_log_dir()}")
        print("="*50)

    return {
        'scores': plot_scores,
        'mean_scores': plot_mean_scores,
        'record': record,
        'training_summary': training_summary,
        'log_dir': logger.get_log_dir() if logger else None,
    }


if __name__ == "__main__":
    import sys

    # Choose training mode
    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == '--old':
            # Use original training function (for comparison)
            print("Running original training function...")
            train()

        elif mode == '--config':
            # Use new config-driven training
            config = sys.argv[2] if len(sys.argv) > 2 else 'simple_2x2'
            reward = sys.argv[3] if len(sys.argv) > 3 else 'simple'
            num_train = int(sys.argv[4]) if len(sys.argv) > 4 else 400
            num_test = int(sys.argv[5]) if len(sys.argv) > 5 else 100
            print(f"Running config-driven training: config={config}, reward={reward}, train_episodes={num_train}, test_episodes={num_test}")
            train_with_config(config_path=config, reward_type=reward, num_training_episodes=num_train, num_test_episodes=num_test)

        else:
            print("Unknown mode. Use --old or --config")
            sys.exit(1)
    else:
        # Default: use new config-driven training with simple_2x2 baseline
        print("Running config-driven training (default: simple_2x2, simple reward)")
        print("Use: python agent.py --old  # for original training")
        print("Use: python agent.py --config <config> <reward_type>  # for custom config")
        print()
        train_with_config(config_path='simple_2x2', reward_type='simple')