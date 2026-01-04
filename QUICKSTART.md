# EconEngine Quick Start Guide

Get started with Phase 1 in 3 simple steps!

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Train an Agent

```bash
python agent.py
```

This will:
- Load the `simple_2x2` baseline environment
- Train for 400 episodes (~3-5 minutes)
- Save metrics to `runs/experiment_<timestamp>/`
- Show real-time training plot

### Step 3: Visualize Results

```bash
streamlit run streamlit_dashboard.py
```

Dashboard opens at http://localhost:8501

**Features:**
- 📈 Training progress curves
- 🎬 Action distribution analysis
- 📊 Inventory trajectories
- 🗺️ Spatial heatmaps
- 🎮 Step-by-step episode replay

## 📚 Documentation

- **`README.md`** - Project overview
- **`claude.md`** - Architecture reference for Claude sessions
- **`PHASE1_COMPLETE.md`** - Phase 1 implementation details
- **`DASHBOARD_README.md`** - Dashboard usage guide
- **`TEST_PHASE1.md`** - Comprehensive testing guide

## 🎯 What to Explore in Dashboard

### Check Learning Progress
1. Open **Training Progress** tab
2. See if utility increases over episodes
3. Check summary statistics (max, mean utility)

### Analyze Agent Behavior
1. Open **Episode Analysis** tab
2. Select a late episode (e.g., Episode 390)
3. Check action distribution: What does the agent do?
4. Check inventory trajectory: Production cycles?
5. Check spatial heatmap: Efficient or random movement?

### Compare Early vs Late Learning
1. Select Episode 0 (early learning)
2. Note action distribution and spatial pattern
3. Select Episode 390 (late learning)
4. Compare: Did the agent learn better strategies?

### Step Through Episodes
1. Open **Episode Replay** tab
2. Select Episode 0, 10, 20, or 30 (has detailed steps)
3. Use slider to step through each action
4. See reward, inventory, location at each step

## 🔧 Advanced Usage

### Train with Different Configs

```bash
# Original hardcoded training (for comparison)
python agent.py --old

# Custom config and reward type
python agent.py --config simple_fish_cooking opportunity_cost
```

### Available Configs

- `simple_2x2` - Baseline (matches original hardcoded setup)
- `simple_fish_cooking` - Validation environment (tests production chain learning)

### Available Reward Types

- `simple` - Current behavior (consumption utility only)
- `opportunity_cost` - Improved (production rewards, time costs) [Phase 2]

### Experiment Organization

All experiments saved to `runs/<experiment_name>/`:
- `config.json` - Environment and reward configuration
- `episodes.jsonl` - Episode summaries (total utility, actions, etc.)
- `steps.jsonl` - Detailed step data (logged every 10 episodes)
- `summary.json` - Training summary statistics

## 🐛 Troubleshooting

### Dashboard shows "No experiments found"
```bash
# Run training first to generate data
python agent.py
```

### ImportError: No module named 'streamlit'
```bash
pip install streamlit plotly
```

### Episode Replay shows "No step data"
- Steps are only logged every 10 episodes
- Select episodes 0, 10, 20, 30, etc.

## 📊 Expected Results (Phase 1 Baseline)

With simple rewards, the agent will:
- ✅ Learn basic navigation
- ✅ Learn to produce resources
- ✅ Learn to consume for utility
- ⚠️ May NOT learn optimal cooking (this is expected!)

**Why no cooking?**
The simple reward structure doesn't incentivize production chains. Phase 2 will add opportunity-cost aware rewards that make cooking more attractive than eating raw fish.

## 🎓 What's Next: Phase 2

Once you've validated Phase 1 works:

1. **Enhanced State** - Add time_remaining, spatial distances (10 → 25 dimensions)
2. **Better Rewards** - Integrate OpportunityCostReward calculator
3. **Validation** - Train on simple_fish_cooking, verify ≥90% optimal utility
4. **Analysis** - Compare simple vs opportunity_cost reward learning

## 📞 Need Help?

See detailed guides:
- Dashboard: `DASHBOARD_README.md`
- Testing: `TEST_PHASE1.md`
- Architecture: `claude.md`

---

**Phase 1 Status: ✅ Complete**

**Ready to explore? Run:**
```bash
python agent.py
streamlit run streamlit_dashboard.py
```

Enjoy watching your agent learn economics! 🚀
