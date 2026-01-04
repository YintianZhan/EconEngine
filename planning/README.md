# Planning: Phase 2 Development Roadmap

This directory contains **planning documents and design specifications** for Phase 2 development.

**For actual code work**, use git branches and worktrees (see `/WORKFLOW.md` in project root).

## Purpose

The `/planning` folder provides:
- **Design specifications** for new features
- **Implementation roadmaps** with task breakdowns
- **Success metrics** and validation criteria
- **Dependency tracking** between workstreams
- **Experiment results** and findings documentation

## Directory Structure

```
planning/
├── README.md                      # This file
├── phase2-state-expansion/        # Expand state from 10→25 dimensions
│   └── PLAN.md
├── phase2-reward-integration/     # Integrate reward calculators into agent
│   └── PLAN.md
├── phase2-validation/             # Optimal policy validation
│   └── PLAN.md
├── advanced-rewards/              # Experimental reward functions
│   └── PLAN.md
├── multi-agent/                   # Multi-agent extensions (Phase 3+)
│   └── PLAN.md
└── experiments/                   # Experiment results and analysis
    ├── PLAN.md
    └── archive/                   # Completed experiments
```

## How to Use

### 1. Read the Plan
Before starting work on a feature:
```bash
cat planning/phase2-state-expansion/PLAN.md
```

### 2. Work in Git Branch/Worktree
See `/WORKFLOW.md` for setting up worktrees:
```bash
# Work happens in separate worktree directories, NOT in /planning
cd ~/Documents/projects/EconEngine-state-expansion
# ... implement the plan ...
```

### 3. Document Progress
Planning docs are accessible from all worktrees:
```bash
# In any worktree, you can reference planning docs
cat planning/phase2-state-expansion/PLAN.md

# Add implementation notes
echo "## Progress Update" >> planning/phase2-state-expansion/NOTES.md
```

### 4. Record Experiments
Save experiment results in planning/experiments/:
```bash
planning/experiments/2026-01-04_state_expansion_test/
├── README.md          # Experiment description
├── results.csv        # Metrics
└── plots/             # Visualizations
```

## Active Workstreams (Phase 2)

| Workstream | Status | Branch | Priority | Dependencies |
|------------|--------|--------|----------|--------------|
| phase2-state-expansion | Not started | `phase2-state-expansion` | High | None |
| phase2-reward-integration | Not started | `phase2-reward-integration` | High | None |
| phase2-validation | Not started | `phase2-validation` | High | State expansion (recommended) |
| advanced-rewards | Planning | `advanced-rewards` | Medium | Reward integration |
| multi-agent | Planning | `multi-agent` | Low (Phase 3+) | Phase 2 complete |

## Relationship to Git Workflow

```
planning/                          Git Branches & Worktrees
├── phase2-state-expansion/   →   Branch: phase2-state-expansion
│   └── PLAN.md                    Worktree: ~/Documents/projects/EconEngine-state-expansion/
│
├── phase2-reward-integration/ →  Branch: phase2-reward-integration
│   └── PLAN.md                    Worktree: ~/Documents/projects/EconEngine-reward-integration/
│
└── phase2-validation/        →   Branch: phase2-validation
    └── PLAN.md                    Worktree: ~/Documents/projects/EconEngine-validation/
```

**Planning docs** (this folder) - Design specifications, tracked in git

**Code changes** - Happen in separate worktree directories (see `/WORKFLOW.md`)

## Tips

### Before Starting Work
- Read the PLAN.md for your workstream
- Check dependencies - are prerequisite features done?
- Review success metrics - how will you know it works?

### While Working
- Reference the task checklist in PLAN.md
- Add implementation notes if needed
- Update PLAN.md if you discover better approaches

### After Completing Work
- Document findings and lessons learned
- Update success metrics with actual results
- Archive completed experiments

## See Also

- `/WORKFLOW.md` - Complete git worktree workflow guide (START HERE!)
- `/README.md` - Project overview
- `/PHASE1_COMPLETE.md` - Phase 1 implementation details
- `/QUICKSTART.md` - Getting started guide

---

**Remember**: This is a **planning folder**, not a code workspace. Use git branches and worktrees for actual development!
