# Phase 2: Reward Integration Workstream

## Goal
Integrate modular reward calculators into `agent.act()` to replace hardcoded reward logic.

## Current Problem

From `agent.py:act()` around line 200-250:
```python
# Hardcoded reward calculation
reward = -0.05  # Fixed penalty per step

# Production action
if action == 4 or action == 5:
    # ... production logic ...
    reward = 0  # Hardcoded

# Consumption action
if action == 6 or action == 7 or action == 8:
    # ... consumption logic ...
    reward = resource.consumption_utility  # From resource dict
```

This prevents using the sophisticated reward calculators built in Phase 1:
- `SimpleUtilityReward` (baseline)
- `OpportunityCostReward` (advanced)

## Target Architecture

```python
# In Agent.__init__()
def __init__(self, map, location, reward_calculator=None):
    # ...
    self.reward_calculator = reward_calculator or SimpleUtilityReward()

# In Agent.act()
def act(self, action):
    # ... execute action ...

    # Calculate reward using pluggable calculator
    reward_context = {
        'action': action,
        'old_state': old_state,
        'new_state': self.get_state(),
        'inventory_change': {...},
        'hp_change': hp_delta,
        'production_occurred': did_produce,
        'consumption_occurred': did_consume,
        'resource_consumed': resource_name,
    }

    reward = self.reward_calculator.calculate(reward_context)

    # ... rest of logic ...
```

## Tasks

- [ ] Add `reward_calculator` parameter to `Agent.__init__()`
- [ ] Refactor `Agent.act()` to build reward_context dict
- [ ] Replace hardcoded rewards with `reward_calculator.calculate(context)`
- [ ] Ensure backward compatibility (default to SimpleUtilityReward)
- [ ] Update `train()` to accept reward_calculator parameter
- [ ] Update `train_with_config()` to pass reward_calculator to Agent
- [ ] Test with both SimpleUtilityReward and OpportunityCostReward
- [ ] Validate rewards match expected values

## Implementation Notes

### Reward Context Structure

```python
{
    'action': int,                    # 0-8
    'old_location': (x, y),
    'new_location': (x, y),
    'old_inventory': {...},
    'new_inventory': {...},
    'inventory_change': {...},        # delta
    'old_hp': int,
    'new_hp': int,
    'hp_change': int,                 # delta
    'age': int,
    'time_remaining': int,
    'action_succeeded': bool,         # False if invalid action
    'production_occurred': bool,
    'production_type': str or None,   # 'cooked_fish', etc.
    'consumption_occurred': bool,
    'resource_consumed': str or None, # 'fish', 'apple', etc.
    'consumption_utility': float,     # base utility from resource
}
```

### Backward Compatibility

Old code:
```python
agent = Agent(map=my_map, location=(0,0))
```

New code:
```python
# Default behavior (same as before)
agent = Agent(map=my_map, location=(0,0))

# With custom reward calculator
from rewards import OpportunityCostReward
reward_calc = OpportunityCostReward(opportunity_cost_weight=0.3)
agent = Agent(map=my_map, location=(0,0), reward_calculator=reward_calc)
```

## Testing Plan

1. **Unit tests**:
   - Verify SimpleUtilityReward produces same rewards as old hardcoded logic
   - Verify OpportunityCostReward produces different rewards

2. **Integration test**:
   - Train agent with SimpleUtilityReward, compare metrics to baseline
   - Train agent with OpportunityCostReward, verify different behavior

3. **Regression test**:
   - Old code path (no reward_calculator param) still works
   - Utilities match baseline

## Success Metrics

- Agent can use any reward calculator
- SimpleUtilityReward matches old behavior (within 1% utility)
- OpportunityCostReward produces measurably different behavior
- Code is cleaner (no hardcoded reward values in agent.py)
- Backward compatible

## Dependencies

- Optional: Depends on phase2-state-expansion for full context (time_remaining, distances)
- Can be done independently with current 10-dim state

## Merge Checklist

- [ ] All tests pass
- [ ] Backward compatibility verified
- [ ] Documentation updated
- [ ] train() and train_with_config() both support reward_calculator
- [ ] Example usage in QUICKSTART.md

## Notes

- Start with SimpleUtilityReward to ensure backward compatibility
- OpportunityCostReward may need state expansion features to work well
- Consider logging reward breakdown to metrics for visualization
