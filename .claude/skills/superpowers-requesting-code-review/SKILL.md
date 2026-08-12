---
name: superpowers-requesting-code-review
description: "CRITICAL: MUST request code review BEFORE any commit. Prepares code for review with comprehensive context and documentation. Use whenever code is ready to be committed or merged."
---

# Requesting Code Review Skill

**Purpose:** Prepare and request code review before commits.

## CRITICAL RULE

**NEVER commit without code review. ALWAYS prepare code for review first.**

## Review Request Flow

```
Prepare code → Document changes → Create review request → Wait for review → Address feedback → THEN commit
```

## Preparing Code for Review

### Step 1: Self-Review

Before requesting review:

```markdown
1. Read all changed files
2. Check for obvious issues
3. Verify tests pass
4. Check code style
```

### Step 2: Document Changes

Create change documentation:

```markdown
## Changes Made

### [File 1]
- [What changed]
- [Why it changed]

### [File 2]
- [What changed]
- [Why it changed]
```

### Step 3: Run All Checks

```markdown
- [ ] All tests pass
- [ ] No lint errors
- [ ] No type errors
- [ ] Code formatted
```

## Creating Review Request

### Review Request Template

```markdown
## Code Review Request

### Summary
[Brief description of changes]

### Changes
- [Change 1]
- [Change 2]
- [Change 3]

### Testing
- [How changes were tested]
- [Test results]

### Notes for Reviewer
- [Any specific concerns]
- [Areas to focus on]
- [Known limitations]
```

### What to Include

```markdown
1. **Context** - Why changes were made
2. **Changes** - What was changed
3. **Testing** - How changes were verified
4. **Concerns** - Any worries or questions
```

## Review Documentation

### Change Log

```markdown
## Change Log

### Added
- [New features/files]

### Modified
- [Changed files]

### Removed
- [Deleted files]
```

### Test Results

```markdown
## Test Results

### Unit Tests
- [Test suite results]

### Integration Tests
- [Integration test results]

### Manual Testing
- [Manual verification steps]
```

## Addressing Review Feedback

### Step 1: Understand Feedback

```markdown
1. Read all feedback carefully
2. Ask questions if unclear
3. Understand the concern
4. Plan the fix
```

### Step 2: Make Changes

```markdown
1. Address each feedback item
2. Make necessary changes
3. Run tests again
4. Update documentation
```

### Step 3: Respond to Feedback

```markdown
## Feedback Response

### [Feedback Item 1]
- **Action:** [What was done]
- **Result:** [Outcome]

### [Feedback Item 2]
- **Action:** [What was done]
- **Result:** [Outcome]
```

## Review Checklist

Before submitting for review:

- [ ] Self-review completed
- [ ] All tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] Change summary written
- [ ] Review request created

## After Review Approval

Only after review is approved:

1. **Commit changes** - With proper commit message
2. **Push to remote** - If applicable
3. **Update plan** - Mark step complete
4. **Document** - Add completion notes

## Common Review Issues

### Code Quality
- Inconsistent style
- Missing error handling
- Poor naming
- Duplicated code

### Testing
- Missing tests
- Incomplete coverage
- Flaky tests
- Missing edge cases

### Documentation
- Missing comments
- Outdated docs
- Unclear explanations
- Missing context

## Review Best Practices

✅ **Do:**
- Self-review first
- Document changes clearly
- Run all checks
- Address feedback promptly

❌ **Don't:**
- Skip self-review
- Submit without tests
- Ignore feedback
- Rush through review
