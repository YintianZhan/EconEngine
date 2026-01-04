# Phase 2: Validation Workstream

## Goal
Implement optimal policy validation to verify agents learn economically rational behaviors.

## Motivation

We need to know if agents are learning **optimal** economic behaviors, not just improving over random play.

**Key Questions:**
- Does the agent learn to cook fish instead of eating raw?
- Does it maximize utility given time constraints?
- Does it discover the optimal production sequence?

## Approach

Create analytical optimal policies for simple environments and compare learned behavior.

## Tasks

### 1. Implement Optimal Policy Calculator

Create `validation/optimal_policy.py`:

```python
class OptimalPolicy:
    """Calculate analytically optimal behavior for simple environments."""

    def calculate_optimal_utility(self, env_config):
        """Return maximum possible utility for environment."""
        pass

    def calculate_optimal_actions(self, env_config):
        """Return optimal action sequence."""
        pass

    def score_agent_behavior(self, agent_actions, optimal_actions):
        """Compare agent to optimal, return 0-1 score."""
        pass
```

### 2. Define Optimal Solutions

For `simple_fish_cooking` environment (2x2 grid, 50 steps):

**Optimal Strategy:**
```
1. Move to fish (0,0) - 1 step
2. Gather fish - 1 step
3. Move to wood (1,1) - 2 steps
4. Gather wood - 1 step
5. Cook fish - 3 steps (assumes cooking time = 3)
6. Consume cooked fish - 1 step
   Utility = 2.0 (cooked fish utility)
7. Repeat as time allows
```

**Expected Optimal Utility:** ~15.0 (depends on episode length)

**Target:** Agent should achieve ≥90% of optimal (≥13.5)

### 3. Create Validation Tests

```python
def test_simple_fish_cooking_optimal():
    """Verify agent learns to cook fish."""
    env = get_preset_config('simple_fish_cooking')

    # Calculate analytical optimal
    optimal = OptimalPolicy()
    max_utility = optimal.calculate_optimal_utility(env)

    # Train agent
    agent = train_agent(env, episodes=1000)

    # Evaluate agent
    agent_utility = evaluate_agent(agent, env, episodes=100)

    # Assert performance
    assert agent_utility >= 0.9 * max_utility
    assert agent.learned_to_cook_fish()  # Custom check
```

### 4. Add Behavior Checks

Beyond utility, check if agent learned specific behaviors:

```python
def learned_to_cook_fish(agent, episodes=100):
    """Check if agent cooks fish instead of eating raw."""
    cook_count = 0
    raw_count = 0

    for _ in range(episodes):
        # Run episode, count cook vs eat-raw actions
        # ...

    return cook_count > raw_count * 2  # Cooks at least 2x more than eats raw
```

## Environments to Validate

1. **simple_2x2** (baseline)
   - Optimal: Gather + consume, no production needed
   - Expected utility: ~10-12

2. **simple_fish_cooking** (production chain)
   - Optimal: Gather fish + wood → cook → consume
   - Expected utility: ~15.0

3. **Future: moderate_5x5**
   - Complex production chains
   - Multiple optimal strategies

## Task List

- [ ] Create `validation/optimal_policy.py`
- [ ] Implement `calculate_optimal_utility()` for simple_fish_cooking
- [ ] Implement `calculate_optimal_actions()` for simple_fish_cooking
- [ ] Create `validation/tests.py` with validation suite
- [ ] Add `learned_to_cook_fish()` behavior check
- [ ] Add `prefers_high_value_resources()` check
- [ ] Document expected vs actual utilities
- [ ] Create visualization comparing optimal vs learned

## Success Metrics

For simple_fish_cooking environment:
- Agent achieves ≥90% of analytical optimal utility
- Agent cooks fish ≥80% of the time (vs eating raw)
- Agent's action sequence resembles optimal sequence

## Testing Plan

1. **Analytical verification**: Hand-calculate optimal for simple_fish_cooking
2. **Agent training**: Train for 1000 episodes with OpportunityCostReward
3. **Evaluation**: Run 100 test episodes, measure utilities
4. **Behavior analysis**: Check if cooking occurs, action patterns

## Dependencies

- **Recommended**: phase2-state-expansion (for better learning)
- **Recommended**: phase2-reward-integration (for OpportunityCostReward)
- Can work with current baseline but may not pass validation

## Merge Checklist

- [ ] Optimal policies documented for each environment
- [ ] Validation tests pass for simple_fish_cooking
- [ ] Behavior checks implemented
- [ ] Visualization of optimal vs learned
- [ ] Documentation updated

## Notes

- Start with simple_fish_cooking (easiest to solve)
- If agent fails validation, this guides Phase 2 improvements
- Optimal policy can be used to generate training demonstrations (future)
- Consider adding "curriculum learning" if agent struggles
