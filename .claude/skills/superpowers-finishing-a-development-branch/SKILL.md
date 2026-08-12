---
name: superpowers-finishing-a-development-branch
description: "Complete development branches properly with verification, testing, and documentation. Use when a feature or fix is complete and ready to merge."
---

# Finishing a Development Branch Skill

**Purpose:** Properly complete and merge development branches.

## When to Use

- Feature is complete
- Bug fix is done
- Work is ready to merge
- Need to clean up branches

## CRITICAL RULES

1. **Verify all tests pass** - No merging with failures
2. **Run full test suite** - Not just related tests
3. **Update documentation** - Keep docs current
4. **Clean up worktree** - Remove when done

## Branch Completion Flow

```
Verify complete → Run tests → Update docs → Request review → Merge → Clean up
```

## Step 1: Verify Completion

### Check Requirements

```markdown
- [ ] All requirements met
- [ ] All tasks complete
- [ ] No known issues
- [ ] Ready for review
```

### Self-Review

```markdown
1. Review all changes
2. Check for completeness
3. Verify quality
4. Ensure consistency
```

## Step 2: Run Tests

### Test Execution

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run linting
flake8 src/ tests/

# Run type checking
mypy src/
```

### Test Checklist

```markdown
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] No lint errors
- [ ] No type errors
- [ ] Coverage acceptable
```

## Step 3: Update Documentation

### Documentation Updates

```markdown
- [ ] README updated (if needed)
- [ ] API docs updated (if needed)
- [ ] CHANGELOG updated
- [ ] Comments added/updated
```

### Change Documentation

```markdown
## Changes

### Added
- [New features]

### Modified
- [Changed functionality]

### Fixed
- [Bug fixes]
```

## Step 4: Request Review

### Prepare Review Request

```markdown
## Review Request

### Summary
[What was done]

### Changes
- [Change 1]
- [Change 2]

### Testing
[How it was tested]

### Notes
[Any concerns]
```

### Review Checklist

```markdown
- [ ] Self-review done
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Ready for review
```

## Step 5: Merge

### Merge Process

```bash
# Ensure you're on the branch
git checkout feature/my-feature

# Pull latest changes
git pull origin feature/my-feature

# Switch to main
git checkout main

# Pull latest main
git pull origin main

# Merge the branch
git merge feature/my-feature

# Push merged changes
git push origin main
```

### Merge Commit Message

```bash
git commit -m "feat: add user authentication

- Added login/logout functionality
- Added user registration
- Added password reset
- Added session management

Closes #123"
```

## Step 6: Clean Up

### Local Cleanup

```bash
# Delete local branch
git branch -d feature/my-feature

# Remove worktree
git worktree remove ../project-feature-my-feature
```

### Remote Cleanup

```bash
# Delete remote branch
git push origin --delete feature/my-feature
```

### Verify Cleanup

```bash
# List branches
git branch -a

# List worktrees
git worktree list
```

## Merge Strategies

### Feature Branch

```bash
# Squash merge for clean history
git merge --squash feature/my-feature
git commit -m "feat: add feature"
```

### Bugfix Branch

```bash
# Regular merge for bugfixes
git merge bugfix/my-fix
```

### Long-Running Branch

```bash
# Merge with merge commit
git merge --no-ff feature/my-feature
```

## Post-Merge Tasks

### Verification

```markdown
- [ ] Main branch builds
- [ ] Tests pass on main
- [ ] Deployment works
- [ ] No regressions
```

### Documentation

```markdown
- [ ] Update release notes
- [ ] Notify team
- [ ] Update project board
- [ ] Close related issues
```

## Common Merge Issues

### Merge Conflicts

```bash
# If conflicts occur
git merge feature/my-feature
# Resolve conflicts
git add .
git commit -m "merge: resolve conflicts"
```

### Failed Merge

```bash
# If merge fails
git merge --abort
# Fix issues
git merge feature/my-feature
```

## Branch Completion Checklist

Before considering branch complete:

- [ ] All code changes complete
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Review approved
- [ ] Merged to main
- [ ] Branch deleted
- [ ] Worktree removed
- [ ] Remote branch deleted

## When to NOT Merge

❌ **Don't merge when:**
- Tests failing
- Incomplete implementation
- Unresolved review comments
- Known issues exist

✅ **Merge when:**
- All tests pass
- Review approved
- Documentation complete
- Ready for production
