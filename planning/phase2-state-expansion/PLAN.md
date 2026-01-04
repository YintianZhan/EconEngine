# Phase 2: State Expansion Workstream

## Goal
Expand agent state representation from 10 to 25+ dimensions to enable better economic decision-making.

## Current State (10 dimensions)
From `agent.py:get_state()`:
```python
[
    location_x,      # 0
    location_y,      # 1
    fish,            # 2
    apple,           # 3
    wood,            # 4
    cooked_fish,     # 5
    hp,              # 6
    age,             # 7
    last_action,     # 8
    reward           # 9
]
```

## Target State (25+ dimensions)

### New Features to Add
1. **Time remaining** - Episodes have fixed length, crucial for planning
2. **Spatial distances** - Distance to each resource type
3. **Resource availability** - Which resources are at current location
4. **Production feasibility** - Can cook fish here? Have ingredients?
5. **Consumption efficiency** - Time until next hp loss
6. **Inventory capacity** - Total items vs max capacity
7. **Recent action history** - Last N actions (for pattern detection)

### Proposed Layout (25 dims)
```python
[
    # Location (2)
    location_x,
    location_y,

    # Inventory (4)
    fish,
    apple,
    wood,
    cooked_fish,

    # Health & Time (3)
    hp,
    age,
    time_remaining,  # NEW: episode_length - age

    # Spatial awareness (8)
    dist_to_fish_x,      # NEW
    dist_to_fish_y,      # NEW
    dist_to_apple_x,     # NEW
    dist_to_apple_y,     # NEW
    dist_to_wood_x,      # NEW
    dist_to_wood_y,      # NEW
    steps_to_nearest_food,  # NEW
    steps_to_cooking_spot,  # NEW

    # Production context (4)
    can_cook_fish,       # NEW: binary flag
    has_fish_ingredients,# NEW: binary flag
    at_resource_location,# NEW: binary flag
    resource_here_type,  # NEW: 0=none, 1=fish, 2=apple, 3=wood

    # Action context (4)
    last_action,
    last_reward,
    consecutive_moves,   # NEW: count of sequential move actions
    inventory_total,     # NEW: sum of all items
]
```

## Tasks

- [ ] Modify `Agent.__init__()` to track episode_length
- [ ] Create `Agent.get_enhanced_state()` with new features
- [ ] Add helper methods: `_calculate_distances()`, `_check_production_feasibility()`
- [ ] Update `Linear_QNet` input size from 10 to 25 in `model.py`
- [ ] Test state encoding with assertions
- [ ] Train on simple_2x2 and compare to baseline
- [ ] Document performance impact

## Testing Plan

1. **Unit test**: Verify state vector has 25 elements
2. **Sanity test**: Check distance calculations are correct
3. **Integration test**: Train for 100 episodes, ensure no crashes
4. **Performance test**: Compare learning curve to 10-dim baseline

## Success Metrics

- State vector is 25 dimensions
- All features are normalized to [0, 1] or [-1, 1]
- No NaN or Inf values in state
- Training speed impact < 20%
- Learning performance ≥ baseline (may improve later with reward integration)

## Dependencies

- None (independent workstream)

## Merge Checklist

Before merging to main:
- [ ] All tests pass
- [ ] Code is documented
- [ ] Performance impact acceptable
- [ ] Backward compatibility maintained (old `get_state()` still works)
- [ ] Update CLAUDE.md with new state layout

## Notes

- Keep old `get_state()` for backward compatibility
- Consider making state features configurable via environment config
- May need to adjust learning rate or model architecture after expansion
