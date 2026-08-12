---
name: superpowers-dispatching-parallel-agents
description: "Dispatch multiple independent agents in parallel for faster execution. Use when you have multiple independent tasks that can be executed simultaneously."
---

# Dispatching Parallel Agents Skill

**Purpose:** Execute multiple independent tasks in parallel.

## When to Use

- Multiple independent tasks exist
- Parallel execution would speed up work
- Tasks don't depend on each other
- Resources are available

## Parallel Dispatch Flow

```
Identify parallel tasks → Prepare tasks → Dispatch agents → Monitor → Collect results → Integrate
```

## Step 1: Identify Parallel Tasks

### Analyze Dependencies

```markdown
Task Dependencies:

Task A: No dependencies
Task B: No dependencies
Task C: Depends on A
Task D: Depends on B

Parallel Groups:
- Group 1: A, B (parallel)
- Group 2: C, D (after Group 1)
```

### Verify Independence

```markdown
For each task pair, verify:
- [ ] No shared state
- [ ] No file conflicts
- [ ] No dependency
- [ ] Can run simultaneously
```

## Step 2: Prepare Tasks

### Task Description Template

```markdown
## Task: [Task Name]

### Objective
[What needs to be accomplished]

### Context
[Background information]

### Requirements
1. [Requirement 1]
2. [Requirement 2]

### Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Constraints
- [Limitations]
```

### Include All Context

```markdown
Each task must include:
- Complete context
- All dependencies
- Success criteria
- Constraints
- Expected output format
```

## Step 3: Dispatch Agents

### Dispatch Strategy

```markdown
1. Create task descriptions
2. Spawn agents for each task
3. Provide all necessary context
4. Set clear expectations
```

### Agent Communication

```markdown
To Agent:
- Clear task description
- All context needed
- Success criteria
- Output format

From Agent:
- Task result
- Success/failure status
- Any issues encountered
```

## Step 4: Monitor Progress

### Track Agent Status

```markdown
Agent Status:

Agent 1: Task A - In Progress
Agent 2: Task B - Complete
Agent 3: Task C - Waiting (depends on A)
Agent 4: Task D - Waiting (depends on B)
```

### Handle Issues

```markdown
If agent fails:
1. Capture error details
2. Analyze root cause
3. Retry OR escalate
4. Update other agents if needed
```

## Step 5: Collect Results

### Gather Outputs

```markdown
1. Collect all agent results
2. Verify success criteria met
3. Check for errors
4. Validate output format
```

### Verify Completion

```markdown
For each task:
- [ ] Success criteria met
- [ ] Output valid
- [ ] No errors
- [ ] Ready for integration
```

## Step 6: Integrate Results

### Combine Results

```markdown
1. Merge outputs
2. Resolve conflicts
3. Run integration tests
4. Verify overall result
```

### Final Verification

```markdown
- [ ] All tasks complete
- [ ] Results integrated
- [ ] Tests pass
- [ ] Requirements met
```

## Parallel Execution Patterns

### Pattern 1: Fan-Out/Fan-In

```markdown
Fan-Out:
- Task A → Agent 1
- Task B → Agent 2
- Task C → Agent 3

Fan-In:
- Collect results from all agents
- Integrate into final result
```

### Pattern 2: Pipeline

```markdown
Stage 1: Task A, B, C (parallel)
Stage 2: Task D (after A, B, C)
Stage 3: Task E (after D)
```

### Pattern 3: Map-Reduce

```markdown
Map:
- Split work into chunks
- Process each chunk in parallel

Reduce:
- Combine results
- Produce final output
```

## Best Practices

✅ **Do:**
- Verify task independence
- Include all context
- Set clear success criteria
- Monitor progress

✅ **Do:**
- Handle failures gracefully
- Collect all results
- Integrate carefully
- Verify final result

❌ **Don't:**
- Dispatch dependent tasks
- Assume agent knows context
- Ignore failures
- Rush integration

## When NOT to Use Parallel Agents

❌ **Don't use when:**
- Tasks are sequential
- Dependencies exist
- Coordination overhead high
- Simple, single-step work

✅ **Use when:**
- Tasks are independent
- Parallel execution beneficial
- Tasks are complex enough
- Resources available
