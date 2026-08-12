---
name: superpowers-systematic-debugging
description: "Use systematic approach for all debugging. No random changes or shotgun debugging. Use when encountering bugs, errors, or unexpected behavior in code."
---

# Systematic Debugging Skill

**Purpose:** Debug systematically, not randomly.

## CRITICAL RULE

**No random changes. Every change must have a hypothesis and verification.**

## Debugging Flow

```
Observe → Hypothesize → Test → Verify → Fix → Learn
```

## Step 1: Observe

### Gather Information

```markdown
1. **What** is happening?
2. **When** does it happen?
3. **Where** does it happen?
4. **How** to reproduce?
5. **What** changed recently?
```

### Reproduce the Issue

```markdown
1. Create minimal reproduction
2. Document exact steps
3. Note expected vs actual
4. Identify patterns
```

## Step 2: Hypothesize

### Form Hypotheses

```markdown
## Hypothesis 1
- **Assumption:** [What you think is wrong]
- **Evidence:** [Why you think this]
- **Test:** [How to verify]

## Hypothesis 2
- **Assumption:** [Alternative explanation]
- **Evidence:** [Supporting evidence]
- **Test:** [How to verify]
```

### Prioritize Hypotheses

```markdown
1. Most likely cause
2. Second most likely
3. Less likely but possible
4. Unlikely but easy to check
```

## Step 3: Test

### Test Each Hypothesis

```markdown
## Testing Hypothesis 1

### Setup
[How to set up the test]

### Execution
[What to run]

### Expected Result
[What should happen if hypothesis is correct]

### Actual Result
[What actually happened]

### Conclusion
[Hypothesis confirmed/rejected]
```

### Testing Tools

```markdown
1. **Print/Log** - Add debug output
2. **Debugger** - Step through code
3. **Tests** - Write specific test
4. **Profiling** - Check performance
```

## Step 4: Verify

### Confirm Root Cause

```markdown
1. Hypothesis confirmed
2. Can reproduce consistently
3. Fix addresses root cause
4. No side effects
```

### Verify Fix

```markdown
1. Apply minimal fix
2. Run reproduction steps
3. Verify issue resolved
4. Run full test suite
```

## Step 5: Fix

### Apply Fix

```markdown
1. Make minimal change
2. Address root cause
3. Don't introduce new issues
4. Document the fix
```

### Test Fix

```markdown
1. Run reproduction steps
2. Run related tests
3. Run full test suite
4. Check for regressions
```

## Step 6: Learn

### Document Learning

```markdown
## Bug Report

### Issue
[What was wrong]

### Root Cause
[Why it happened]

### Fix
[How it was fixed]

### Prevention
[How to prevent in future]
```

### Update Knowledge

```markdown
1. Add to known issues
2. Update documentation
3. Add regression test
4. Share with team
```

## Debugging Tools

### Print Debugging

```python
# Add strategic print statements
print(f"DEBUG: variable = {variable}")
print(f"DEBUG: reached point X")
```

### Debugger

```python
# Use breakpoint()
breakpoint()

# Or pdb
import pdb; pdb.set_trace()
```

### Logging

```python
import logging
logging.debug(f"Variable: {variable}")
logging.info(f"Reached point X")
```

## Common Debugging Mistakes

❌ **Random Changes**
- Changing code without understanding
- Hoping something works
- Not verifying fixes

❌ **Shotgun Debugging**
- Making multiple changes at once
- Not isolating the problem
- Not testing each change

❌ **Skipping Steps**
- Not reproducing first
- Not forming hypotheses
- Not verifying fixes

## Debugging Best Practices

✅ **Do:**
- Reproduce first
- Form hypotheses
- Test each hypothesis
- Verify fixes

✅ **Do:**
- Use systematic approach
- Document findings
- Add regression tests
- Learn from bugs

❌ **Don't:**
- Make random changes
- Skip reproduction
- Assume you know
- Rush to fix

## When Debugging Feels Hard

Debugging feels hard when:
- Can't reproduce
- Complex interactions
- Intermittent issues
- Time pressure

Solution:
- Simplify reproduction
- Isolate components
- Add more logging
- Take breaks
