---
name: superpowers-using-git-worktrees
description: "Create isolated git worktrees for all non-trivial work. Provides clean workspace without stashing or losing state. Use when starting new features, fixing bugs, or any work that benefits from isolation."
---

# Using Git Worktrees Skill

**Purpose:** Create isolated workspaces for clean development.

## When to Use

- Starting new feature work
- Fixing bugs
- Experimenting with changes
- Working on multiple tasks
- Need clean workspace

## CRITICAL RULE

**ALWAYS use git worktrees for non-trivial work. NEVER work directly on main branch.**

## Worktree Flow

```
Identify work → Create worktree → Work in isolation → Commit → Push → Clean up
```

## Step 1: Identify Work

### Determine Work Type

```markdown
Work Types:
- Feature: New functionality
- Bugfix: Fixing issues
- Experiment: Trying something
- Refactor: Improving code
```

### Name the Branch

```markdown
Branch Naming:
- feature/description
- bugfix/description
- experiment/description
- refactor/description

Examples:
- feature/user-authentication
- bugfix/login-error
- experiment/new-architecture
- refactor/cleanup-utils
```

## Step 2: Create Worktree

### Create Branch and Worktree

```bash
# Create new branch
git branch feature/my-feature

# Create worktree
git worktree add ../project-feature-my-feature feature/my-feature

# Navigate to worktree
cd ../project-feature-my-feature
```

### Verify Worktree

```bash
# List worktrees
git worktree list

# Check current branch
git branch --show-current
```

## Step 3: Work in Isolation

### Development Workflow

```markdown
1. Make changes in worktree
2. Test changes
3. Commit frequently
4. Push when ready
```

### Commit Guidelines

```bash
# Stage changes
git add .

# Commit with message
git commit -m "feat: add user authentication"

# Push to remote
git push origin feature/my-feature
```

## Step 4: Clean Up

### After Work Complete

```bash
# Navigate back to main project
cd ../project

# Remove worktree
git worktree remove ../project-feature-my-feature

# Delete branch (if merged)
git branch -d feature/my-feature
```

### Worktree Management

```bash
# List all worktrees
git worktree list

# Remove worktree
git worktree remove <path>

# Prune stale worktrees
git worktree prune
```

## Worktree Best Practices

### Naming Conventions

```markdown
Directory Naming:
- ../project-feature-name
- ../project-bugfix-name
- ../project-experiment-name

Branch Naming:
- feature/name
- bugfix/name
- experiment/name
```

### Location Guidelines

```markdown
Worktree Location:
- Same parent directory as main project
- Clear naming convention
- Easy to find and manage

Example:
~/projects/
├── project/           # Main worktree
├── project-feature-a/ # Feature worktree
└── project-bugfix-b/  # Bugfix worktree
```

## Common Worktree Scenarios

### Scenario 1: New Feature

```bash
# Create feature worktree
git worktree add ../project-feature-auth feature/user-auth

# Work on feature
cd ../project-feature-auth
# ... make changes ...
git commit -m "feat: add authentication"
git push origin feature/user-auth

# Clean up
cd ../project
git worktree remove ../project-feature-auth
```

### Scenario 2: Bug Fix

```bash
# Create bugfix worktree
git worktree add ../project-bugfix-login bugfix/login-error

# Fix the bug
cd ../project-bugfix-login
# ... fix bug ...
git commit -m "fix: resolve login error"
git push origin bugfix/login-error

# Clean up
cd ../project
git worktree remove ../project-bugfix-login
```

### Scenario 3: Experiment

```bash
# Create experiment worktree
git worktree add ../project-experiment-newarch experiment/new-architecture

# Try something
cd ../project-experiment-newarch
# ... experiment ...
git commit -m "experiment: try new architecture"

# If successful, merge
# If not, just delete worktree
cd ../project
git worktree remove ../project-experiment-newarch
```

## Worktree Benefits

✅ **Isolation**
- Changes don't affect main project
- Clean workspace for each task
- No stashing needed

✅ **Parallel Work**
- Multiple features simultaneously
- Easy context switching
- No branch switching

✅ **Safety**
- Main project stays clean
- Easy to discard experiments
- No accidental commits

## Worktree Limitations

❌ **Disk Space**
- Each worktree uses space
- Multiple copies of repo

❌ **Management**
- Need to track worktrees
- Need to clean up

❌ **Confusion**
- Can get lost in worktrees
- Need clear naming

## When NOT to Use Worktrees

❌ **Don't use when:**
- Quick one-line fix
- Very small change
- Just trying something quick
- Disk space limited

✅ **Use when:**
- Non-trivial work
- Need isolation
- Multiple tasks
- Experimenting

## Worktree Commands Reference

```bash
# Create worktree
git worktree add <path> <branch>

# List worktrees
git worktree list

# Remove worktree
git worktree remove <path>

# Prune stale worktrees
git worktree prune
```
