# EconEngine Interactive Dashboard

Real-time visualization tool for analyzing agent learning behavior, actions, and spatial movement patterns.

## Quick Start

### 1. Install Dependencies

```bash
pip install streamlit plotly pyyaml tqdm
```

### 2. Train an Agent (Generate Data)

Run a quick training session to generate data:

```bash
# Quick test (default: 400 episodes with simple_2x2 environment)
python agent.py
```

This will create logs in `runs/experiment_<timestamp>/` with:
- `config.json` - experiment configuration
- `episodes.jsonl` - episode summaries
- `steps.jsonl` - detailed step data (logged every 10 episodes)
- `summary.json` - training summary (created at end)

### 3. Launch Dashboard

```bash
streamlit run streamlit_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Dashboard Features

### 📈 Training Progress Tab

**Training Curve**
- Line chart showing total utility per episode
- Moving average to see learning trend
- Hover to see exact values

**Summary Statistics**
- Total episodes trained
- Maximum utility achieved
- Mean utility across all episodes
- Final episode utility

### 🎬 Episode Analysis Tab

**Episode Selector**
- Choose any episode to analyze in detail
- Episodes sorted by utility for easy comparison

**Action Distribution**
- Pie chart: what actions the agent took (Move Right, Produce, Cook, etc.)
- Bar chart: action categories (Move, Produce, Consume)
- See if agent learned optimal action patterns

**Inventory Trajectory**
- Line chart showing inventory levels over time
- Track apple, fish, wood, cooked fish quantities
- See production/consumption patterns

**Spatial Heatmap**
- Grid showing where agent spent time
- Darker colors = more time spent
- Understand spatial movement efficiency

### 📊 Statistics Tab

**Overall Statistics**
- Mean, std, max, min utilities
- Total episodes

**Learning Progression**
- Split training into Early, Middle, Late phases
- Compare mean/max utilities across phases
- Verify agent is improving over time

**Training Summary**
- JSON view of complete training metrics

### 🎮 Episode Replay Tab

**Step-by-Step Replay**
- Slider to move through episode step by step
- See action taken, reward received, inventory state
- Track HP and utility changes
- Understand agent decision-making

**Note:** Detailed steps are only logged every 10 episodes (to save disk space). Try selecting episodes 0, 10, 20, 30, etc.

## What to Look For

### Signs of Good Learning

✅ **Utility increasing over time** - training curve slopes upward
✅ **Production chains learned** - agent uses "Cook" action (converts fish → cooked fish)
✅ **Efficient movement** - spatial heatmap shows purposeful paths, not random wandering
✅ **Inventory management** - inventory plot shows gather → produce → consume cycles
✅ **Action balance** - ~50% produce, 25% move, 25% consume (for simple environments)

### Signs of Poor Learning

❌ **Flat or decreasing utility** - agent not learning
❌ **No cooking** - eating raw fish instead of cooked fish (sub-optimal)
❌ **Random movement** - heatmap shows uniform distribution
❌ **Inventory hoarding** - produces but never consumes
❌ **Repetitive actions** - stuck in loops (visible in episode replay)

## Example Analysis Workflow

1. **Training Progress** tab
   - Check if utility is increasing over time
   - Identify the best episode

2. **Episode Analysis** tab
   - Select the best episode
   - Check action distribution: is agent cooking?
   - Check inventory: are there production cycles?
   - Check spatial heatmap: efficient or random?

3. **Compare Early vs Late**
   - Select Episode 0 (early learning)
   - Select Episode 390 (late learning)
   - Compare action distributions and spatial patterns

4. **Episode Replay** (for episodes 0, 10, 20, ...)
   - Step through to see exact decision sequence
   - Understand why certain actions were taken
   - Debug unexpected behaviors

## Troubleshooting

### "No experiments found"
- Run training first: `python agent.py`
- Check that `runs/` directory exists
- Verify `runs/experiment_*/config.json` exists

### "No step data available"
- Steps are only logged every 10 episodes
- Select episodes 0, 10, 20, 30, etc. for replay
- To log more steps, modify `agent.py:466` (change `% 10` to `% 1`)

### Dashboard won't load
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check for errors in terminal
- Try refreshing the browser

## Tips

- **Multiple experiments**: Dashboard automatically lists all experiments in `runs/`
- **Experiment naming**: Pass `experiment_name` to `train_with_config()` for custom names
- **Data persistence**: All data is saved to `runs/`, safe to close dashboard and reopen
- **Performance**: Large experiments (1000+ episodes) may load slowly - be patient!

## Next Steps

After validating Phase 1 works:

1. **Phase 2**: Enhanced state representation (25 dimensions)
2. **Phase 2**: Opportunity-cost aware rewards
3. **Phase 3**: More advanced visualizations (Q-value evolution, etc.)
4. **Phase 4**: Multi-agent support and comparative advantage

---

**Dashboard Features:**
- ✅ Training progress curves
- ✅ Action distribution analysis
- ✅ Inventory trajectory tracking
- ✅ Spatial heatmap visualization
- ✅ Episode-by-episode replay
- ✅ Learning phase comparison
- ✅ Real-time experiment selection

**Enjoy exploring what your agent learns! 🚀**
