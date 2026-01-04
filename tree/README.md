# Tree: Parallel Agent Development Workspace

This directory is a workspace for multiple agents to work on different updates in parallel before merging back to the main codebase.

## Purpose

The `/tree` folder enables:
- **Parallel development** - Multiple agents work on different features simultaneously
- **Isolated experimentation** - Test changes without affecting main codebase
- **Controlled merging** - Review and integrate changes selectively
- **Version tracking** - Keep history of different approaches

## Directory Structure

```
tree/
├── README.md              # This file
├── phase2-state-expansion/   # Enhanced state representation (10→25 dims)
├── phase2-reward-integration/ # Integrate reward calculators into agent
├── phase2-validation/     # Optimal policy validation
├── advanced-rewards/      # New reward function experiments
├── multi-agent/           # Multi-agent extensions
└── experiments/           # One-off experiments and prototypes
```

## Workflow

### 1. Start a New Workstream

```bash
# Create a new workstream directory
mkdir tree/<workstream-name>

# Copy relevant files from main codebase
cp <files> tree/<workstream-name>/

# Create a WORKSTREAM.md to track goals and progress
```

### 2. Develop in Isolation

Each workstream should have:
- **WORKSTREAM.md** - Goals, approach, progress, findings
- **Modified files** - Only the files being changed
- **Test scripts** - Validation code specific to this workstream
- **Notes** - Insights, issues, decisions made

### 3. Merge Back to Main

When a workstream is ready:

```bash
# Review changes
cd tree/<workstream-name>
diff <file> ../../<file>

# Copy approved changes back to main codebase
cp <approved-files> ../..

# Update main documentation
# Create git commit in main repo
# Archive or remove workstream directory
```

## Active Workstreams

| Workstream | Owner | Status | Goal |
|------------|-------|--------|------|
| phase2-state-expansion | TBD | Not started | Expand state from 10→25 dimensions |
| phase2-reward-integration | TBD | Not started | Use reward calculators in agent.act() |
| phase2-validation | TBD | Not started | Implement optimal policy validation |

## Best Practices

### File Organization
- Keep workstream directories focused on ONE specific goal
- Document all assumptions and decisions in WORKSTREAM.md
- Include example commands to test changes

### Code Changes
- Minimize dependencies between workstreams
- Maintain backward compatibility when possible
- Add inline comments explaining non-obvious changes

### Testing
- Test changes in isolation before merging
- Compare metrics before/after to validate improvements
- Document performance impacts

### Merging
- Review all diffs carefully before copying to main
- Update main documentation to reflect merged changes
- Test integrated system after each merge
- Create atomic git commits per workstream

## Example: Creating a New Workstream

```bash
# 1. Create workstream directory
mkdir tree/my-experiment

# 2. Copy base files
cp agent.py tree/my-experiment/
cp model.py tree/my-experiment/

# 3. Create workstream doc
cat > tree/my-experiment/WORKSTREAM.md << 'EOF'
# My Experiment

## Goal
Test if larger hidden layer improves learning

## Approach
- Change model from (10, 256, 9) to (10, 512, 9)
- Train on simple_2x2 for 400 episodes
- Compare final utilities to baseline

## Status
[ ] Modify model.py
[ ] Run training
[ ] Analyze results
[ ] Decision: merge or discard

## Findings
TBD
EOF

# 4. Make changes
cd tree/my-experiment
# ... edit files ...

# 5. Test
python agent.py

# 6. Merge if successful
cp model.py ../..
git add model.py
git commit -m "Increase hidden layer size to 512"
```

## Gitignore Note

The `/tree` directory is **tracked in git** to enable collaboration, but individual experiment runs within workstreams should use their own `runs/` subdirectories (which are ignored).

## Questions?

See the main project README.md or ask the current session owner.
