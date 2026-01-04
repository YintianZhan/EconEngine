# Advanced Rewards Workstream

## Goal
Experiment with novel reward functions beyond SimpleUtilityReward and OpportunityCostReward.

## Motivation

Current reward functions may not capture all economic learning objectives. This workstream explores:
- Alternative reward formulations
- Curriculum learning approaches
- Auxiliary rewards for exploration
- Multi-objective reward combinations

## Potential Reward Functions

### 1. Intrinsic Curiosity Reward
```python
class CuriosityReward(BaseReward):
    """Bonus for discovering new state-action combinations."""

    def calculate(self, context):
        base_reward = simple_utility(context)

        # Bonus for novel behaviors
        state_action = (context['state'], context['action'])
        if state_action not in self.seen_combinations:
            curiosity_bonus = 0.1
            self.seen_combinations.add(state_action)
        else:
            curiosity_bonus = 0.0

        return base_reward + curiosity_bonus
```

**Hypothesis**: Helps agent explore production chains it might not discover naturally.

### 2. Efficiency Reward
```python
class EfficiencyReward(BaseReward):
    """Penalize wasteful actions, reward efficient paths."""

    def calculate(self, context):
        base_reward = simple_utility(context)

        # Penalize inefficient movement
        if context['action'] in [0,1,2,3]:  # Movement
            optimal_dist = manhattan_distance(
                context['location'],
                nearest_valuable_resource()
            )
            actual_dist = context['steps_taken']
            efficiency_penalty = -0.01 * (actual_dist - optimal_dist)
        else:
            efficiency_penalty = 0

        return base_reward + efficiency_penalty
```

**Hypothesis**: Encourages optimal navigation and resource gathering.

### 3. Planning Horizon Reward
```python
class PlanningHorizonReward(BaseReward):
    """Reward based on future value, not just immediate utility."""

    def calculate(self, context):
        immediate = simple_utility(context)

        # Estimate future value of current inventory
        future_value = self._estimate_production_potential(
            context['inventory'],
            context['time_remaining']
        )

        # Discount future value
        gamma = 0.95
        return immediate + gamma * future_value
```

**Hypothesis**: Helps agent value intermediate goods (wood) that enable future production.

### 4. Multi-Objective Reward
```python
class MultiObjectiveReward(BaseReward):
    """Combine multiple objectives with learnable weights."""

    def __init__(self):
        self.objectives = {
            'utility': SimpleUtilityReward(),
            'efficiency': EfficiencyReward(),
            'exploration': CuriosityReward(),
        }
        self.weights = {'utility': 0.7, 'efficiency': 0.2, 'exploration': 0.1}

    def calculate(self, context):
        total = 0
        for name, reward_fn in self.objectives.items():
            total += self.weights[name] * reward_fn.calculate(context)
        return total
```

**Hypothesis**: Balanced approach captures multiple aspects of good economic behavior.

### 5. Curriculum Reward
```python
class CurriculumReward(BaseReward):
    """Gradually shift from exploration to exploitation."""

    def __init__(self):
        self.episode = 0
        self.exploration_reward = CuriosityReward()
        self.utility_reward = SimpleUtilityReward()

    def calculate(self, context):
        # Early: mostly exploration
        # Late: mostly utility maximization
        exploration_weight = max(0, 1 - self.episode / 500)
        utility_weight = 1 - exploration_weight

        exploration = self.exploration_reward.calculate(context)
        utility = self.utility_reward.calculate(context)

        return exploration_weight * exploration + utility_weight * utility
```

**Hypothesis**: Structured learning progression improves final performance.

## Experiments to Run

### Experiment 1: Curiosity Bonus
- Train with CuriosityReward on simple_fish_cooking
- Measure: Does agent discover cooking faster?
- Compare: Baseline vs curiosity-enhanced

### Experiment 2: Efficiency Penalties
- Train with EfficiencyReward on simple_fish_cooking
- Measure: Steps to achieve same utility
- Compare: Baseline vs efficiency-optimized

### Experiment 3: Multi-Objective
- Train with MultiObjectiveReward, sweep weight combinations
- Measure: Utility, efficiency, exploration diversity
- Find: Pareto-optimal weight settings

### Experiment 4: Curriculum Learning
- Train with CurriculumReward
- Measure: Learning speed, final performance
- Compare: Curriculum vs static rewards

## Task List

- [ ] Implement CuriosityReward
- [ ] Implement EfficiencyReward
- [ ] Implement PlanningHorizonReward
- [ ] Implement MultiObjectiveReward
- [ ] Implement CurriculumReward
- [ ] Create experiment runner script
- [ ] Run experiments on simple_fish_cooking
- [ ] Analyze results, create comparison plots
- [ ] Document findings

## Success Metrics

For each reward function:
- Final utility vs baseline
- Learning speed (episodes to 90% performance)
- Behavior quality (cooking frequency, efficiency)
- Robustness (performance variance across runs)

## Testing Plan

For each new reward function:
1. Unit test: Verify reward calculation logic
2. Sanity test: Rewards have reasonable magnitude
3. Training test: Agent improves over time
4. Comparison test: Compare to baseline

## Dependencies

- None (independent experiments)
- Optional: phase2-reward-integration (for easier integration)

## Merge Checklist

Only merge if:
- [ ] New reward function outperforms baseline
- [ ] Well-documented and tested
- [ ] Adds clear value to the project
- [ ] Code follows project structure (in `rewards/` module)

Otherwise, keep as experimental archive.

## Notes

- This is an **experimental** workstream - not all ideas will work
- Document negative results too (what didn't work and why)
- Some ideas may need state expansion to work well
- Consider publishing findings as research notes
