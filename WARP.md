# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Runtime and dependencies

- This is a small Python 3 project that trains a Deep Q-Learning agent in a simple grid-based economy.
- External Python packages inferred from imports:
  - `numpy`
  - `pandas`
  - `torch`
  - `matplotlib`
  - `ipython`
- A minimal way to install dependencies in a fresh environment is:
  - `pip install numpy pandas torch matplotlib ipython`

## Common commands

All commands below are intended to be run from the repository root.

- Train the economic agent with the default environment and hyperparameters:
  - `python agent.py`
- Visualize the resource map and how agents are rendered on it (manual demo):
  - `python map.py`
- Quick checks for the resource and recipe domain objects (run their small demos):
  - `python resource_recipe.py`
  - `python resource.py`

Notes:
- There is currently no automated test suite or linting configuration in this repository; there are no standard commands like `pytest` or `ruff` wired up.
- Model checkpoints are saved under the `model/` directory by `Linear_QNet.save` in `model.py` (e.g. `model/model_new.pth`).

## High-level architecture

### Overview

The codebase implements a single-agent reinforcement-learning environment where an agent moves on a 2D grid, gathers and transforms resources (fish, apples, wood, cooked fish), and learns a policy using a Deep Q-Network (DQN). The environment dynamics, economic objects, and learning logic are split across a few focused modules.

### Modules and responsibilities

- `agent.py`
  - Defines the central `Agent` class, which combines:
    - Domain state: age, hit points (`hp`), current grid `location`, production inventory (`product`), and accumulated `utilities`.
    - Environment interaction: movement, production, trade, and consumption, using the recipes defined in `resource_dict.py`.
    - Reinforcement learning state: replay `memory`, exploration parameter `epsilon`, discount factor `gamma`, and a `Linear_QNet` model with its `QTrainer`.
  - Implements the action space via a 9-dimensional one-hot `model_action` vector covering: 4 moves, 2 production actions (`produce_local`, `cook`), and 3 consumption actions (`consume` for different resources).
  - `get_state()` encodes the environment into a numeric vector (location, inventory levels, hp, and last action type) that is fed into the DQN.
  - `get_available_actions()` masks out invalid or undesirable actions (e.g., moving off the map, producing where no resource exists, consuming when inventory is empty) by assigning large negative values that are added to the network’s Q-values.
  - `train_short_memory` and `train_long_memory` wrap `QTrainer.train_step` for on-policy and replay-batch updates.
  - The top-level `train()` function orchestrates training:
    - Builds a `Map`, populates resources in fixed locations, and instantiates an `Agent` bound to that map.
    - For each time step, obtains the current state, selects an action (epsilon-greedy over masked Q-values), applies it via `act`, and records the transition into replay memory.
    - On episode end (`done` when hp is 0 or daily hours exhausted), runs replay training, tracks the best score, saves improved models, and updates live training plots via `helper.plot`.
    - `if __name__ == "__main__":` in this file calls `train()` and is the primary entrypoint.

- `map.py`
  - Defines the `Map` class, modeling a 2D grid of fixed size (`width`, `length`).
  - `populate_resources` assigns a resource name (e.g., `'fish'`, `'apple'`, `'wood'`) to specific grid coordinates; these resource names must match keys in `resource_dict.resource_dict`.
  - `print_map` renders the grid with simple ASCII art, optionally marking agent locations with a `*`. This is used for debugging and visualization in interactive demos.

- `resource.py`, `resource_recipe.py`, and `resource_dict.py`
  - `resource_recipe.py` defines `Recipe`, which encodes the production technology for a resource:
    - Time required, input resource names and amounts, output resource and quantity, and whether production requires being at a specific map location.
  - `resource.py` defines `Resource`, which couples consumption utility, decay rate, health effects, and a `Recipe` object.
  - `resource_dict.py` builds the global `resource_dict` mapping string names (e.g. `'apple'`, `'fish'`, `'wood'`, `'cooked fish'`) to `Resource` instances with associated `Recipe`s.
  - The `Agent` relies heavily on `resource_dict` for:
    - Determining rewards and health changes on `consume`.
    - Determining production feasibility and outputs in `produce_resource` / `produce_local` / `cook`.

- `model.py`
  - Wraps the PyTorch DQN implementation used by the agent.
  - `Linear_QNet` is a simple two-layer fully connected network: `input_size -> hidden_size -> output_size`, with ReLU between layers.
  - `Linear_QNet.save` saves the model weights to `./model/<file_name>` and creates the `model/` directory if it does not exist.
  - `QTrainer` encapsulates the Adam optimizer and MSE loss, and implements `train_step`, which performs the standard DQN target update:
    - Computes Q-values for current and next states.
    - For each transition in the batch, sets the target for the taken action to `reward` or `reward + gamma * max_a' Q(next_state, a')` if the transition is not terminal.

- `helper.py`
  - Provides a single `plot(scores, mean_scores)` function that uses Matplotlib and IPython display to render live plots of training progress (per-episode scores and running mean scores) during `agent.train()`.

### How pieces fit together

- Environment setup:
  - `Map` defines the spatial layout and which resources are available at each grid cell.
  - `resource_dict` defines what each named resource is worth (utility, health) and how it can be produced (recipes).
- Agent and learning loop:
  - `Agent` keeps track of inventory, health, and location, and uses `Map` and `resource_dict` to determine which actions are available and what outcomes they produce.
  - The DQN (`Linear_QNet` + `QTrainer`) learns to map `Agent.get_state()` vectors to Q-values over the 9 discrete actions, with invalid actions discouraged via `get_available_actions` masking.
  - Training via `agent.train()` is episodic over simulated "days" (`TOTAL_HRS`), with experience replay and model checkpointing.

These relationships are important when modifying the project: changes to resource names, recipes, or map layout must stay consistent across `resource_dict.py`, `map.py`, and the features/actions encoded in `Agent.get_state` and `Agent.get_available_actions`.