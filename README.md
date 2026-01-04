# EconEngine: Economic Learning Research Platform

A reinforcement learning platform for studying whether agents can learn economic behaviors that rational agents understand immediately.

## 🎯 Research Goals

**Primary Question:** Can RL agents learn optimal economic behaviors through experience?

**Phase 1 (Single-Agent):**
- Learn **opportunity costs** and **optimal resource allocation**
- Discover **production chains** and value creation (gather → process → consume)
- Validate with **simple and moderate** complexity environments

**Phase 2 (Multi-Agent - Future):**
- Learn **comparative advantage** and **specialization**
- Discover **market dynamics** and **price discovery**

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train an agent (400 episodes, ~5 minutes)
python agent.py

# 3. Visualize results in interactive dashboard
streamlit run streamlit_dashboard.py
```

**See `QUICKSTART.md` for detailed guide.**

## 📊 Interactive Dashboard

Real-time visualization of agent learning:

- **Training Progress** - Utility curves, learning trends
- **Episode Analysis** - Action distributions, inventory trajectories, spatial heatmaps
- **Statistics** - Learning progression (early vs mid vs late)
- **Episode Replay** - Step-by-step visualization of agent decisions

**See `DASHBOARD_README.md` for usage guide.**

## 🏗️ Architecture

### Modular Design (Phase 1 Complete ✅)

```
EconEngine/
├── agent.py              # RL agent with DQN
├── map.py                # 2D grid environment
├── resource_dict.py      # Economic resources & recipes
├── model.py              # PyTorch DQN
│
├── environments/         # Config-driven environments
│   ├── environment_config.py
│   └── configs/
│       ├── simple_2x2.yaml
│       └── simple_fish_cooking.yaml
│
├── rewards/              # Pluggable reward calculators
│   ├── base_reward.py
│   └── reward_components.py
│       - SimpleUtilityReward
│       - OpportunityCostReward
│
├── metrics/              # Data collection & logging
│   ├── metric_collector.py
│   └── metric_logger.py
│
└── streamlit_dashboard.py  # Interactive visualization
```

### Key Features

✅ **Config-driven environments** - YAML-based, easy to create new economies
✅ **Modular rewards** - Swap reward functions to test different learning objectives
✅ **Comprehensive metrics** - JSON Lines logging for analysis
✅ **Interactive dashboard** - Real-time visualization with Streamlit
✅ **Backward compatible** - Original training code still works

## 📚 Documentation

| File | Description |
|------|-------------|
| `QUICKSTART.md` | Get started in 5 minutes |
| `DASHBOARD_README.md` | Dashboard features and usage |
| `TEST_PHASE1.md` | Comprehensive testing guide |
| `PHASE1_COMPLETE.md` | Phase 1 implementation details |
| `claude.md` | Architecture reference for Claude sessions |
| `WARP.md` | Original project reference |

## 🧪 Example: Training on Simple Environment

```bash
# Train with simple utility rewards (baseline)
python agent.py --config simple_2x2 simple

# Train with opportunity-cost aware rewards (Phase 2)
python agent.py --config simple_fish_cooking opportunity_cost
```

**Environment:** 2x2 grid with fish, apple, wood resources
**Optimal Strategy:** Gather fish + wood → cook → consume cooked fish
**Expected Outcome:** Agent should learn production chains yield higher utility

## 📈 Current State (Phase 1)

### What Works

✅ Modular architecture (environments, rewards, metrics)
✅ Config-driven environment creation
✅ Comprehensive metrics logging
✅ Interactive Streamlit dashboard
✅ Backward compatible with original code

### What's Next (Phase 2)

⏳ Enhanced state representation (10 → 25 dimensions)
⏳ Integrate opportunity-cost reward calculator
⏳ Validate optimal learning on simple_fish_cooking
⏳ Reward breakdown visualization

### Future (Phase 3+)

🔮 Rich visualization dashboard (Q-values, reward components)
🔮 Moderate 5x5 environment with complex production chains
🔮 Multi-agent support
🔮 Comparative advantage and market dynamics

## 🔬 Research Workflow

1. **Design Environment** - Create YAML config with resources and recipes
2. **Choose Reward** - Select reward calculator (simple vs opportunity-cost)
3. **Train Agent** - Run `python agent.py --config <env> <reward>`
4. **Analyze Results** - Use dashboard to understand what agent learned
5. **Iterate** - Adjust rewards/environment based on insights

## 🛠️ Tech Stack

- **Python 3** - Core language
- **PyTorch** - Deep Q-Network (DQN)
- **NumPy/Pandas** - Numerical operations and data handling
- **Streamlit** - Interactive dashboard
- **Plotly** - Interactive visualizations
- **YAML** - Configuration files

## 📦 Installation

### Requirements

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- numpy >= 1.24.0
- pandas >= 2.0.0
- torch >= 2.0.0
- matplotlib >= 3.7.0

**New (Phase 1):**
- pyyaml >= 6.0 (config parsing)
- tqdm >= 4.65.0 (progress bars)
- streamlit >= 1.28.0 (dashboard)
- plotly >= 5.14.0 (visualizations)

## 📊 Example Results

With simple rewards (Phase 1 baseline):
- Agents learn basic navigation and resource gathering
- Utilities increase from ~5 (early) to ~10-15 (late)
- May NOT learn optimal cooking (expected - needs better rewards!)

With opportunity-cost rewards (Phase 2):
- Agents should learn production chains
- Expected utilities: ≥90% of analytical optimal
- Should prefer cooked fish over raw fish

## 🤝 Contributing

This is a research project. Key areas for contribution:

1. **New Environments** - Create YAML configs for different economies
2. **Reward Functions** - Implement new reward calculators
3. **Visualizations** - Add dashboard components
4. **Multi-Agent** - Extend to multiple agents (Phase 2)

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

Built with Claude Code for economic learning research.

## 📞 Contact

[Add your contact information]

---

**Status:** Phase 1 Complete ✅

**Next:** Phase 2 - Enhanced Learning Signals

**Get Started:** `python agent.py && streamlit run streamlit_dashboard.py`
