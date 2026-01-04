# Experiments: One-Off Prototypes

## Purpose

This directory is for **quick experiments and prototypes** that don't fit into other workstreams.

Use this space for:
- Testing wild ideas
- Reproducing bugs in isolation
- Prototyping features before committing to a workstream
- Benchmarking performance
- Learning experiments

## Guidelines

### File Naming
Use descriptive names with dates:
```
2026-01-04_larger_hidden_layer/
2026-01-05_double_learning_rate/
2026-01-10_test_curriculum_bug/
```

### Documentation
Each experiment should have a brief README:
```markdown
# Experiment: [Name]

**Date**: 2026-01-04
**Goal**: Test if larger hidden layer improves learning
**Result**: No significant improvement, slight slowdown
**Decision**: Do not merge
```

### Cleanup
Archive or delete experiments after:
- Findings are documented
- Code is merged (if successful)
- 30 days of inactivity (if inconclusive)

## Example Experiments

### Performance Tuning
```
experiments/2026-01-04_batch_size_sweep/
├── README.md
├── agent_modified.py
├── results.csv
└── plots/
```

Test: Batch sizes [500, 1000, 2000, 4000]
Result: 1000 optimal, 2000 slightly worse, 4000 much worse

### Bug Reproduction
```
experiments/2026-01-05_nan_in_q_values/
├── README.md
├── minimal_repro.py
└── debug_output.txt
```

Bug: Q-values become NaN after ~300 episodes
Cause: Gradient explosion from large rewards
Fix: Clip rewards to [-10, 10]

### Architecture Exploration
```
experiments/2026-01-06_dueling_dqn/
├── README.md
├── dueling_model.py
├── train_dueling.py
└── comparison_plots/
```

Test: Dueling DQN vs standard DQN
Result: 15% improvement in sample efficiency
Decision: Create separate workstream to integrate

## Current Experiments

| Date | Name | Status | Outcome |
|------|------|--------|---------|
| - | - | - | - |

## Tips

- Keep experiments small and focused
- Document negative results (what didn't work)
- If experiment succeeds, graduate to a proper workstream
- If experiment fails, document why for future reference
- Use git branches for experiments that might break things

## Quick Experiment Template

```bash
# Create experiment directory
mkdir experiments/$(date +%Y-%m-%d)_my_experiment
cd experiments/$(date +%Y-%m-%d)_my_experiment

# Create README
cat > README.md << 'EOF'
# Experiment: [Name]

**Date**: $(date +%Y-%m-%d)
**Goal**:
**Hypothesis**:
**Method**:
**Result**: TBD
**Decision**: TBD

## Files
-

## Commands
```bash

```

## Notes
EOF

# Copy baseline files
cp ../../agent.py .
# ... make changes ...

# Run experiment
python agent.py

# Document results in README.md
```

## Archive

Completed experiments are moved to `experiments/archive/` after 30 days.
