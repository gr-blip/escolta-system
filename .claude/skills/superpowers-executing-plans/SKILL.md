---
name: superpowers-executing-plans
description: "Execute implementation plans in manageable batches. Reads plan documents, executes steps systematically, and tracks progress. Use when working from a plan document to implement features or fixes."
---

# Executing Plans Skill

**Purpose:** Execute implementation plans systematically in batches.

## When to Use

- Working from a plan document
- Implementing multi-step features
- Following a structured approach
- Tracking progress is important

## Execution Flow

```
Read plan → Understand context → Execute steps → Track progress → Verify results → Update plan
```

## Reading Plans

### Step 1: Read Full Plan

```markdown
1. Read entire plan document
2. Understand the goal
3. Note dependencies
4. Identify current status
```

### Step 2: Understand Context

```markdown
1. What exists today
2. What needs to change
3. Why changes are needed
4. How changes fit together
```

### Step 3: Identify Next Steps

```markdown
1. Find current status
2. Identify next incomplete step
3. Check dependencies satisfied
4. Plan execution approach
```

## Executing Steps

### Step Execution Checklist

For each plan step:

```markdown
- [ ] Read step description
- [ ] Understand requirements
- [ ] Check dependencies
- [ ] Execute implementation
- [ ] Verify result
- [ ] Update plan status
```

### Implementation Approach

```markdown
1. **Understand** - What needs to happen
2. **Plan** - How to implement
3. **Implement** - Write the code
4. **Test** - Verify it works
5. **Document** - Update plan
```

## Batch Execution

### What is a Batch?

A batch is a group of related steps that can be executed together:

```markdown
Batch Example:
- Step 1: Create database model
- Step 2: Add migration
- Step 3: Create API endpoint
- Step 4: Add tests

These form a logical batch for "add user feature".
```

### Batch Size Guidelines

```markdown
Small Batch (1-2 steps):
- Simple changes
- Quick iterations
- Low risk

Medium Batch (3-5 steps):
- Feature implementation
- Moderate complexity
- Some dependencies

Large Batch (6+ steps):
- Complex features
- Multiple components
- Higher risk
```

## Progress Tracking

### Updating Plan Status

After each step:

```markdown
1. Mark step as complete
2. Add completion notes
3. Update overall status
4. Note any issues
```

### Status Updates

```markdown
## Status: In Progress

### Completed
- [x] Step 1: Description
- [x] Step 2: Description

### In Progress
- [ ] Step 3: Description

### Remaining
- [ ] Step 4: Description
- [ ] Step 5: Description
```

## Verification

### After Each Step

```markdown
1. Run relevant tests
2. Check for errors
3. Verify behavior
4. Document results
```

### After Each Batch

```markdown
1. Run full test suite
2. Check integration
3. Verify requirements met
4. Update plan status
```

## Handling Issues

### When a Step Fails

```markdown
1. Capture error details
2. Analyze root cause
3. Fix the issue
4. Re-run the step
5. Update plan with notes
```

### When Blocked

```markdown
1. Document the blocker
2. Identify dependencies
3. Work on unblocked steps
4. Escalate if needed
```

## Plan Updates

### During Execution

```markdown
1. Update step status
2. Add implementation notes
3. Document decisions made
4. Track time spent
```

### After Completion

```markdown
1. Mark all steps complete
2. Add completion summary
3. Document lessons learned
4. Archive plan
```

## Execution Best Practices

✅ **Do:**
- Read plan fully before starting
- Execute steps systematically
- Update plan as you go
- Verify each step works

❌ **Don't:**
- Skip steps
- Ignore plan updates
- Rush through steps
- Forget to test

## When Execution Feels Slow

Execution feels slow when:
- Plan is too detailed
- Steps are too small
- Too much verification
- Context switching

Solution:
- Adjust batch size
- Group related steps
- Streamline verification
- Focus on one batch at a time
