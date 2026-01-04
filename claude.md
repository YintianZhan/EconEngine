# EconEngine Project Reference

## Project Overview

EconEngine is a reinforcement learning project that trains a Deep Q-Learning (DQN) agent in a simple grid-based economy. The agent learns to navigate a 2D grid, gather resources (fish, apples, wood), transform them through production (e.g., cooking fish), and consume them to maximize utility while maintaining health.

## Tech Stack

- **Language**: Python 3
- **Dependencies**:
  - `numpy` - numerical operations
  - `pandas` - data handling
  - `torch` - PyTorch for DQN implementation
  - `matplotlib` - visualization and plotting
  - `ipython` - interactive display support

## Setup

Install dependencies:
```bash
pip install numpy pandas torch matplotlib ipython
```

## Common Commands

Run from repository root:

- **Train the agent**: `python agent.py`
- **Visualize the map**: `python map.py`
- **Test resource/recipe objects**: `python resource_recipe.py` or `python resource.py`

**Note**: No automated test suite or linting is currently configured.

## Architecture

### Core Modules

#### `agent.py` (Main Entry Point)
- **Agent class**: Manages state (age, hp, location, inventory, utilities) and RL components (memory, epsilon, model)
- **Action space**: 9 discrete actions (4 moves, 2 production, 3 consumption)
- **State encoding**: `get_state()` returns numeric vector of location, inventory, hp, last action
- **Action masking**: `get_available_actions()` prevents invalid actions (off-grid moves, empty inventory consumption)
- **Training loop**: `train()` orchestrates episodes, experience replay, model saving
- Run with: `if __name__ == "__main__": train()`

#### `map.py`
- **Map class**: 2D grid with fixed width/length
- `populate_resources`: Assigns resource names to grid coordinates
- `print_map`: ASCII visualization with agent markers
- Resource names must match `resource_dict` keys

#### `resource.py`, `resource_recipe.py`, `resource_dict.py`
- **Recipe**: Production technology (time, inputs, outputs, location requirements)
- **Resource**: Consumption utility, decay, health effects, associated recipe
- **resource_dict**: Global mapping of resource names to Resource instances
  - Keys: `'fish'`, `'apple'`, `'wood'`, `'cooked fish'`
  - Used by Agent for rewards, health changes, production feasibility

#### `model.py`
- **Linear_QNet**: 2-layer fully connected network (input → hidden → output) with ReLU
- **QTrainer**: Adam optimizer + MSE loss, implements DQN target updates
- Models saved to `./model/` directory (e.g., `model/model_new.pth`)

#### `helper.py`
- `plot(scores, mean_scores)`: Live matplotlib plots of training progress

### Data Flow

1. **Environment**: Map defines spatial layout, resource_dict defines economic rules
2. **Agent**: Tracks state, queries Map and resource_dict for available actions
3. **DQN**: Learns state → Q-values mapping with invalid action masking
4. **Training**: Episodic learning with experience replay, model checkpointing on improvement

### Important Consistency Requirements

When modifying the project, ensure consistency across:
- Resource names in `resource_dict.py`
- Map layout in `map.py`
- State features in `Agent.get_state()`
- Action masks in `Agent.get_available_actions()`

## File Structure

```
.
├── agent.py              # Main training loop and Agent class
├── map.py                # Grid environment
├── resource.py           # Resource class definition
├── resource_recipe.py    # Recipe class definition
├── resource_dict.py      # Global resource configuration
├── model.py              # DQN network and trainer
├── helper.py             # Plotting utilities
└── model/                # Saved model checkpoints
    └── model_new.pth
```

## Current State

- Recent commits focused on action limiting and training improvements
- Git branch: `main`
- Untracked files: `.DS_Store`, `WARP.md`
