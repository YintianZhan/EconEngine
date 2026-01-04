# Phase 1 Testing Guide

Quick guide to test Phase 1 implementation and the Streamlit dashboard.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Core: numpy, pandas, torch, matplotlib, ipython
- New: pyyaml, tqdm, streamlit, plotly

## Step 2: Quick Training Test (5 minutes)

Run a short training session to generate test data:

```bash
python agent.py
```

**What happens:**
1. Loads `simple_2x2` environment config
2. Creates agent with SimpleUtilityReward
3. Trains for 400 episodes (takes ~3-5 minutes)
4. Saves metrics to `runs/experiment_<timestamp>/`
5. Shows real-time matplotlib plot

**Expected output:**
```
Running config-driven training (default: simple_2x2, simple reward)
Use: python agent.py --old  # for original training
Use: python agent.py --config <config> <reward_type>  # for custom config

Loaded environment: EnvironmentConfig(name='simple_2x2_baseline', grid=(2, 2), episode_length=24)
Using reward calculator: SimpleUtilityReward(config={})
Logging to: /Users/.../runs/experiment_20260103_...
Starting training for 400 episodes...
Episode 1 complete: score=5.45, steps=24
Episode 2 complete: score=6.20, steps=24
...
```

## Step 3: Launch Dashboard

```bash
streamlit run streamlit_dashboard.py
```

**What happens:**
1. Dashboard opens at http://localhost:8501
2. Automatically detects experiments in `runs/`
3. Loads most recent experiment by default

**Expected dashboard features:**
- Training Progress: utility curve showing learning
- Episode Analysis: action distributions, inventory plots, spatial heatmap
- Statistics: mean/max utilities, learning phases
- Episode Replay: step-by-step visualization

## Step 4: Explore the Dashboard

### Test Training Progress Tab

1. ✅ See utility curve increasing over episodes
2. ✅ Moving average shows learning trend
3. ✅ Summary stats show max/mean utilities

### Test Episode Analysis Tab

1. ✅ Select different episodes from dropdown
2. ✅ Action distribution pie chart shows what agent does
3. ✅ Inventory trajectory shows resource gathering
4. ✅ Spatial heatmap shows where agent moves
5. ✅ Try comparing Episode 0 (early) vs Episode 390 (late)

### Test Episode Replay Tab

1. ✅ Select Episode 0, 10, 20, or 30 (has detailed steps)
2. ✅ Use slider to step through episode
3. ✅ See action taken, reward, inventory at each step

## Step 5: Validation Checks

### Module Imports ✅

```bash
python3 -c "
from environments import get_preset_config
from rewards import SimpleUtilityReward
from metrics import MetricCollector
print('✅ All modules import successfully')
"
```

### Config Loading ✅

```bash
python3 -c "
from environments import get_preset_config
config = get_preset_config('simple_2x2')
print(f'✅ Config loaded: {config}')
print(f'   Grid: {config.grid_size}')
print(f'   Resources: {list(config.resources.keys())}')
"
```

### Metrics Logging ✅

```bash
ls runs/experiment_*/
# Should show: config.json  episodes.jsonl  steps.jsonl  summary.json
```

### Backward Compatibility ✅

```bash
# Test old training function still works
python agent.py --old
```

## Common Issues

### ImportError: No module named 'streamlit'

**Solution:**
```bash
pip install streamlit plotly
```

### ImportError: No module named 'yaml'

**Solution:**
```bash
pip install pyyaml
```

### Dashboard shows "No experiments found"

**Solution:**
- Run training first: `python agent.py`
- Check `runs/` directory exists
- Verify files in `runs/experiment_*/`

### Episode Replay shows "No step data available"

**Solution:**
- Steps are only logged every 10 episodes
- Select episodes 0, 10, 20, 30, etc.
- This is by design to save disk space

## Expected Behavior (Baseline)

With the current simple reward structure, you should see:

**Early Episodes (0-100):**
- Random exploration
- Low utilities (< 5)
- No clear action patterns

**Mid Episodes (100-300):**
- Learning basic behaviors
- Utilities increase to 8-12
- Some production actions learned

**Late Episodes (300-400):**
- More stable performance
- Utilities 10-15
- Agent finds some productive strategies

**Note:** The agent might NOT learn optimal cooking behavior with simple rewards. This is expected! Phase 2 will introduce opportunity-cost aware rewards that incentivize production chains.

## Success Criteria for Phase 1

✅ **Architecture:**
- [x] Config-driven environment loading
- [x] Modular reward system
- [x] Metrics collection and logging
- [x] Backward compatible with old code

✅ **Dashboard:**
- [x] Training progress visualization
- [x] Action distribution analysis
- [x] Inventory trajectory tracking
- [x] Spatial heatmap
- [x] Episode replay

✅ **Data Pipeline:**
- [x] YAML configs load correctly
- [x] Metrics saved to JSON Lines
- [x] Dashboard reads logged data
- [x] Multiple experiments supported

## What's Next: Phase 2

Once Phase 1 is validated, we'll move to Phase 2:

1. **Enhanced State Representation**
   - Expand from 10 to 25 dimensions
   - Add time_remaining, spatial distances
   - Enable planning and lookahead

2. **Opportunity-Cost Rewards**
   - Integrate OpportunityCostReward calculator
   - Reward production chains (not just consumption)
   - Variable time costs for different actions

3. **Validation Environment**
   - Train on simple_fish_cooking.yaml
   - Target: ≥90% of optimal utility
   - Verify agent learns to cook fish

4. **Dashboard Enhancements**
   - Reward breakdown visualization
   - Q-value evolution tracking
   - Compare simple vs opportunity-cost rewards

---

**Ready to test? Run:**
```bash
pip install -r requirements.txt
python agent.py
streamlit run streamlit_dashboard.py
```

**Enjoy watching your agent learn! 🎉**
