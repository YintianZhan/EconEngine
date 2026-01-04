# Multi-Agent Workstream

## Goal
Extend EconEngine to support multiple agents learning economic interactions: trade, specialization, and comparative advantage.

## Motivation

**Phase 1** focuses on single-agent optimal resource allocation.

**Phase 2+** investigates multi-agent economics:
- Can agents learn to trade?
- Do they discover comparative advantage?
- Can they learn specialization and division of labor?
- Do markets emerge spontaneously?

## Research Questions

1. **Comparative Advantage**: If Agent A is 2x better at fishing and Agent B is 1.5x better at apple-picking, will they specialize and trade?

2. **Price Discovery**: Can agents learn market-clearing prices through interaction?

3. **Cooperation vs Competition**: How do agents balance self-interest with gains from trade?

4. **Communication**: Do agents need explicit communication or can trade emerge from observation?

## Architecture Changes Needed

### 1. Multi-Agent Environment

```python
class MultiAgentMap(Map):
    """Grid environment with multiple agents."""

    def __init__(self, width, length, num_agents=2):
        super().__init__(width, length)
        self.agents = []
        self.agent_locations = {}

    def can_trade(self, agent_a, agent_b):
        """Check if two agents are adjacent."""
        return manhattan_distance(
            self.agent_locations[agent_a],
            self.agent_locations[agent_b]
        ) == 1
```

### 2. Trade Actions

Extend action space from 9 to 15+:
```python
# Original actions (0-8)
# Move: 0-3
# Produce: 4-5
# Consume: 6-8

# New trade actions (9-14)
# Propose trade: 9 (offer fish for apple)
# Accept trade: 10
# Reject trade: 11
# ...
```

### 3. Agent Observation

Each agent observes:
- Own state (as before)
- Other agents' locations (visible)
- Other agents' recent actions (visible)
- Other agents' inventories (visible or hidden?)

### 4. Reward Functions

**Individual Rewards** (self-interested):
```python
reward = own_utility_gained
```

**Social Rewards** (cooperative):
```python
reward = own_utility + alpha * other_agent_utility
```

**Trade Surplus Rewards**:
```python
reward = (own_utility_after - own_utility_before) - opportunity_cost
```

## Implementation Phases

### Phase A: Basic Multi-Agent (No Trade)
- Multiple agents in same environment
- Agents can observe each other
- Independent action selection
- Shared resources (scarcity!)

**Goal**: Learn if agents interfere or cooperate without explicit trade

### Phase B: Simple Trade
- Adjacent agents can exchange items
- Fixed exchange rates (1 fish = 1 apple)
- Agents learn when to trade

**Goal**: Verify agents can learn beneficial trades

### Phase C: Price Discovery
- Agents propose exchange rates
- Negotiation via accept/reject
- Market prices emerge

**Goal**: Learn if agents discover equilibrium prices

### Phase D: Specialization
- Agents have different production efficiencies
- Environment designed to favor specialization
- Measure division of labor

**Goal**: Verify comparative advantage learning

## Example Environment: Trade Island

```yaml
name: trade_island
grid_size: [4, 4]
num_agents: 2

agent_0_start: [0, 0]
agent_0_efficiency:
  fishing: 1.5  # Agent 0 is better at fishing
  apple_picking: 0.8

agent_1_start: [3, 3]
agent_1_efficiency:
  fishing: 0.7
  apple_picking: 1.5  # Agent 1 is better at apples

resources:
  fish:
    locations: [[0, 1], [1, 0]]
  apple:
    locations: [[2, 3], [3, 2]]

optimal_strategy: |
  Agent 0 should specialize in fishing
  Agent 1 should specialize in apples
  Both should trade to maximize utility
```

## Task List

### Phase A: Basic Multi-Agent
- [ ] Create `MultiAgentMap` class
- [ ] Modify `Agent` to handle other agents' presence
- [ ] Create multi-agent training loop
- [ ] Test resource competition
- [ ] Measure interference vs cooperation

### Phase B: Simple Trade
- [ ] Extend action space with trade actions
- [ ] Implement trade execution logic
- [ ] Create trade reward calculator
- [ ] Test on trade_island environment
- [ ] Measure trade frequency and utility gains

### Phase C: Price Discovery
- [ ] Implement negotiation protocol
- [ ] Add price proposal/acceptance actions
- [ ] Track market prices over time
- [ ] Visualize price convergence
- [ ] Compare to theoretical equilibrium

### Phase D: Specialization
- [ ] Add agent-specific production efficiencies
- [ ] Measure specialization index
- [ ] Compare to comparative advantage predictions
- [ ] Visualize division of labor

## Success Metrics

### Phase A
- Agents don't collide (respect locations)
- Agents gather resources (basic functionality works)
- Measure: resource distribution fairness

### Phase B
- Agents initiate trades
- Trades increase total utility
- Measure: trade frequency, mutual benefit

### Phase C
- Prices converge over episodes
- Prices approach theoretical equilibrium
- Measure: price stability, efficiency

### Phase D
- Agents specialize according to comparative advantage
- Specialization index > 0.7 (1.0 = complete specialization)
- Measure: action distribution, utility vs autarky

## Dependencies

- Phase 2 features (state expansion, reward integration)
- Validated single-agent learning (phase2-validation)

## Merge Checklist

Due to complexity, merge incrementally:
- [ ] Phase A: Basic multi-agent environment
- [ ] Phase B: Simple fixed-rate trade
- [ ] Phase C: Price discovery (if successful)
- [ ] Phase D: Specialization (research contribution)

## Notes

- This is **advanced research** - expect challenges
- Multi-agent RL is notoriously difficult
- Start simple (Phase A) and validate before progressing
- Document failures and insights
- May require new algorithms (MADDPG, QMIX, etc.)
- Consider communication channels (cheap talk vs costly signaling)

## Future Directions

- Markets with more than 2 agents
- Money/currency emergence
- Public goods and externalities
- Institutional evolution (property rights, contracts)
