# Parallel Development Workflow with Git Worktrees

This guide explains how to use git worktrees to enable multiple Claude Code agents to work on different features simultaneously.

## Quick Start

```bash
# 1. See available worktrees
cd ~/Documents/projects/EconEngine
git worktree list

# 2. Terminal 1: Work on state expansion
cd ~/Documents/projects/EconEngine-state-expansion
claude
# Agent: "Read planning/phase2-state-expansion/PLAN.md and implement it"

# 3. Terminal 2: Work on reward integration
cd ~/Documents/projects/EconEngine-reward-integration
claude
# Agent: "Read planning/phase2-reward-integration/PLAN.md and implement it"

# 4. Terminal 3: Merge completed work
cd ~/Documents/projects/EconEngine
claude
# You: "Merge the phase2-state-expansion branch into main"
```

## Architecture Overview

### Directory Structure

```
~/Documents/projects/
├── EconEngine/                     # Main repo (main branch)
│   ├── planning/                   # Planning docs (accessible from all worktrees)
│   │   ├── phase2-state-expansion/
│   │   ├── phase2-reward-integration/
│   │   └── phase2-validation/
│   ├── agent.py
│   ├── model.py
│   └── ... (all main codebase files)
│
├── EconEngine-state-expansion/     # Worktree (phase2-state-expansion branch)
│   ├── planning/                   # Same planning docs (shared via git)
│   ├── agent.py                    # Can be modified independently
│   └── ...
│
├── EconEngine-reward-integration/  # Worktree (phase2-reward-integration branch)
│   └── ...
│
└── EconEngine-validation/          # Worktree (phase2-validation branch)
    └── ...
```

### Available Worktrees

| Directory | Branch | Purpose |
|-----------|--------|---------|
| `EconEngine` | `main` | Main codebase, coordination, merging |
| `EconEngine-state-expansion` | `phase2-state-expansion` | Expand state 10→25 dims |
| `EconEngine-reward-integration` | `phase2-reward-integration` | Integrate reward calculators |
| `EconEngine-validation` | `phase2-validation` | Optimal policy validation |
| `EconEngine-advanced-rewards` | `advanced-rewards` | Experimental rewards |
| `EconEngine-multi-agent` | `multi-agent` | Multi-agent extensions |

## Workflow Steps

### 1. Setup (Already Done!)

The worktrees have been created for you. To see them:

```bash
cd ~/Documents/projects/EconEngine
git worktree list
```

### 2. Start Parallel Work

Open multiple terminal windows/tabs:

**Terminal 1: State Expansion**
```bash
cd ~/Documents/projects/EconEngine-state-expansion
claude
```

> **Prompt**: "Read planning/phase2-state-expansion/PLAN.md and implement the state expansion feature. Commit your changes when done."

**Terminal 2: Reward Integration**
```bash
cd ~/Documents/projects/EconEngine-reward-integration
claude
```

> **Prompt**: "Read planning/phase2-reward-integration/PLAN.md and integrate the reward calculators into agent.act(). Commit when done."

**Terminal 3: Validation**
```bash
cd ~/Documents/projects/EconEngine-validation
claude
```

> **Prompt**: "Read planning/phase2-validation/PLAN.md and implement optimal policy validation. Commit when done."

Each agent works independently in its own worktree without interfering with others!

### 3. Monitor Progress

Check on agents anytime:

```bash
# See what each worktree is doing
cd ~/Documents/projects/EconEngine
git worktree list

# Check commits in each branch
git log phase2-state-expansion --oneline -5
git log phase2-reward-integration --oneline -5
git log phase2-validation --oneline -5
```

### 4. Merge Completed Work

When an agent finishes, merge its branch back to main:

**Terminal 4: Main Coordination**
```bash
cd ~/Documents/projects/EconEngine
claude
```

> **Prompt**: "Review the changes in the phase2-state-expansion branch and merge it into main. Handle any conflicts."

Or manually:
```bash
cd ~/Documents/projects/EconEngine
git checkout main

# Review changes
git diff main..phase2-state-expansion

# Merge
git merge phase2-state-expansion

# If conflicts, resolve them
# Then:
git add .
git commit
git push origin main
```

### 5. Sync Worktrees After Merge

After merging to main, update other worktrees:

```bash
# In each worktree that needs the merged changes
cd ~/Documents/projects/EconEngine-reward-integration
git merge main  # Merge main into this branch

cd ~/Documents/projects/EconEngine-validation
git merge main  # Merge main into this branch
```

This brings the latest changes from main into the feature branches.

## Key Concepts

### What Are Worktrees?

Git worktrees let you check out multiple branches simultaneously in different directories.

**Without worktrees:**
```bash
git checkout phase2-state-expansion  # Switches entire repo
# Can't work on phase2-reward-integration at same time
```

**With worktrees:**
```bash
cd ~/Documents/projects/EconEngine-state-expansion      # On phase2-state-expansion
cd ~/Documents/projects/EconEngine-reward-integration   # On phase2-reward-integration
# Both can be worked on simultaneously!
```

### Planning Folder

The `/planning` folder contains design docs and is accessible from all worktrees:

```bash
# In main repo
cat ~/Documents/projects/EconEngine/planning/phase2-state-expansion/PLAN.md

# In worktree (same file!)
cat ~/Documents/projects/EconEngine-state-expansion/planning/phase2-state-expansion/PLAN.md
```

**Important**: Planning docs are tracked in git, so changes to planning docs are shared across all worktrees after committing.

### Branch Independence

Each worktree works on its own branch:
- Changes in `EconEngine-state-expansion` don't affect `EconEngine-reward-integration`
- Each agent commits to its own branch
- Merging to main integrates changes

## Common Tasks

### Adding a New Worktree

```bash
cd ~/Documents/projects/EconEngine

# Create branch
git branch my-new-feature

# Create worktree
git worktree add ~/Documents/projects/EconEngine-my-feature my-new-feature
```

### Removing a Worktree

When work is done and merged:

```bash
cd ~/Documents/projects/EconEngine

# Remove worktree
git worktree remove ~/Documents/projects/EconEngine-state-expansion

# Optionally delete branch (if merged)
git branch -d phase2-state-expansion

# Or force delete if not merged
git branch -D phase2-state-expansion
```

### Checking Worktree Status

```bash
cd ~/Documents/projects/EconEngine

# List all worktrees
git worktree list

# See detailed status
git branch -vv
```

### Handling Merge Conflicts

When merging branches that modified the same files:

```bash
cd ~/Documents/projects/EconEngine
git checkout main
git merge phase2-state-expansion

# If conflicts:
# Git will mark conflict sections in files

# Option 1: Ask Claude to resolve
claude
# "Resolve the merge conflicts in agent.py and model.py"

# Option 2: Manual resolution
# Edit conflicted files, then:
git add .
git commit
```

## Example: Complete Parallel Workflow

### Scenario
Three agents work on Phase 2 features simultaneously.

**Day 1: Setup**
```bash
# You (in main terminal)
cd ~/Documents/projects/EconEngine
git worktree list  # Verify all worktrees exist
```

**Day 1-3: Parallel Development**

Terminal 1 (State Expansion Agent):
```bash
cd ~/Documents/projects/EconEngine-state-expansion
claude
# Agent works for 3 days, makes 15 commits
```

Terminal 2 (Reward Integration Agent):
```bash
cd ~/Documents/projects/EconEngine-reward-integration
claude
# Agent works for 2 days, makes 8 commits
```

Terminal 3 (Validation Agent):
```bash
cd ~/Documents/projects/EconEngine-validation
claude
# Agent works for 2 days, makes 6 commits
```

**Day 3: First Merge (Reward Integration)**
```bash
# Reward integration finishes first
cd ~/Documents/projects/EconEngine
git merge phase2-reward-integration
git push origin main

# Update other branches with the merge
cd ~/Documents/projects/EconEngine-state-expansion
git merge main  # Get reward integration changes

cd ~/Documents/projects/EconEngine-validation
git merge main  # Get reward integration changes
```

**Day 4: Second Merge (State Expansion)**
```bash
cd ~/Documents/projects/EconEngine
git merge phase2-state-expansion
# Conflicts with reward integration!

# Resolve conflicts with Claude
claude
# "Resolve merge conflicts between state expansion and reward integration"

git push origin main
```

**Day 5: Final Merge (Validation)**
```bash
cd ~/Documents/projects/EconEngine-validation
git merge main  # Get latest main changes

cd ~/Documents/projects/EconEngine
git merge phase2-validation
git push origin main

# Phase 2 complete!
```

## Tips & Best Practices

### 1. Keep Main Clean
- Only merge tested, working code into main
- Use the main repo for coordination, not development

### 2. Commit Often in Worktrees
- Each agent should commit frequently
- Small commits are easier to review and merge

### 3. Communicate Merge Order
- If features depend on each other, merge in order:
  1. `phase2-state-expansion` (no dependencies)
  2. `phase2-reward-integration` (may need new state features)
  3. `phase2-validation` (needs both above)

### 4. Test Before Merging
- Run tests in the worktree before merging to main
- Validate that changes work as expected

### 5. Document in Planning Folder
- Agents should update planning docs with findings
- Add NOTES.md files with implementation insights

### 6. Handle Conflicts Promptly
- When conflicts arise, resolve them immediately
- Don't let conflicts accumulate

### 7. Clean Up Finished Worktrees
- Remove worktrees when work is merged
- Keeps the workspace clean and clear

## Troubleshooting

### "worktree already exists"
```bash
# List worktrees
git worktree list

# Remove stale worktree
git worktree remove <path>

# Or prune (clean up deleted worktrees)
git worktree prune
```

### "cannot merge unrelated histories"
```bash
# Ensure both branches share common ancestor
git merge-base main phase2-state-expansion

# If no common ancestor, branches were created incorrectly
# Recreate the branch from main:
git checkout main
git branch -D phase2-state-expansion
git branch phase2-state-expansion
```

### "modified files in working directory"
```bash
# Commit or stash changes before switching branches
cd ~/Documents/projects/EconEngine-state-expansion
git status
git add .
git commit -m "WIP: Save current progress"
```

### Worktree is locked
```bash
# Unlock worktree
git worktree unlock <path>
```

## See Also

- `/planning/README.md` - Planning documentation overview
- `/planning/phase2-state-expansion/PLAN.md` - State expansion design
- `/planning/phase2-reward-integration/PLAN.md` - Reward integration design
- `/planning/phase2-validation/PLAN.md` - Validation design
- `/README.md` - Project overview
- `/QUICKSTART.md` - Getting started guide

## Advanced: Git Worktree Commands Reference

```bash
# Create worktree
git worktree add <path> <branch>

# Create worktree with new branch
git worktree add -b <new-branch> <path>

# List worktrees
git worktree list

# Remove worktree
git worktree remove <path>

# Prune stale worktrees
git worktree prune

# Move worktree
git worktree move <source> <destination>

# Lock/unlock worktree
git worktree lock <path>
git worktree unlock <path>
```

---

**You're all set!** Open multiple terminals, navigate to different worktree directories, start Claude Code sessions, and let multiple agents work in parallel. Happy coding! 🚀
