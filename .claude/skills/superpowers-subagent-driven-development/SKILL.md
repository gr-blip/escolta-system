---
name: superpowers-subagent-driven-development
description: "Use subagents to implement plans in isolated environments. Orchestrates multiple agents working in parallel on different parts of a plan. Use when plans have multiple independent steps or when parallel execution would speed up work."
---

# Subagent-Driven Development Skill

**Purpose:** Implement plans using subagents in isolated environments.

## When to Use

- Plan has multiple independent steps
- Parallel execution would speed up work
- Work requires isolation from main environment
- Complex tasks that benefit from focused agents

## Subagent Flow

```
Read plan → Identify parallel work → Spawn subagents → Monitor progress → Collect results → Verify integration
```

## Orchestrating Subagents

### Step 1: Read and Analyze Plan

```markdown
1. Read the full plan document
2. Identify independent steps
3. Determine dependencies between steps
4. Plan parallel execution strategy
```

### Step 2: Prepare Environment

```markdown
1. Create git worktree for isolation
2. Set up necessary dependencies
3. Configure environment variables
4. Prepare test data
```

### Step 3: Spawn Subagents

For each independent step:

```markdown
1. Create focused task description
2. Include all necessary context
3. Define clear success criteria
4. Spawn subagent with task
```

### Step 4: Monitor Progress

```markdown
1. Track subagent status
2. Handle failures gracefully
3. Coordinate dependent work
4. Provide feedback as needed
```

### Step 5: Collect Results

```markdown
1. Gather subagent outputs
2. Verify success criteria met
3. Integrate results
4. Run integration tests
```

## Subagent Task Template

```markdown
## Task: [Task Name]

### Context
[Why this task exists]

### Requirements
1. [Requirement 1]
2. [Requirement 2]

### Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Constraints
- [Constraint 1]
- [Constraint 2]

### Dependencies
- [What this task depends on]
```

## Parallel Execution Strategy

### Identify Parallel Work

```markdown
Plan Steps:
1. Step A (independent)
2. Step B (depends on A)
3. Step C (independent)
4. Step D (depends on B and C)

Parallel Groups:
- Group 1: Step A, Step C (parallel)
- Group 2: Step B (after A)
- Group 3: Step D (after B and C)
```

### Execution Order

```markdown
1. Spawn subagents for Group 1
2. Wait for Group 1 completion
3. Spawn subagent for Group 2
4. Wait for Group 2 completion
5. Spawn subagent for Group 3
6. Wait for Group 3 completion
```

## Subagent Communication

### Sending Tasks

```markdown
1. Clear, focused task description
2. All necessary context included
3. Explicit success criteria
4. No ambiguity in requirements
```

### Receiving Results

```markdown
1. Verify success criteria met
2. Check for errors or warnings
3. Validate output format
4. Integrate into main work
```

## Error Handling

### Subagent Failure

```markdown
1. Capture error details
2. Analyze root cause
3. Retry with fixes OR
4. Escalate to user
```

### Timeout Handling

```markdown
1. Set reasonable timeouts
2. Monitor execution time
3. Cancel stuck subagents
4. Retry with simpler task
```

## Subagent Best Practices

✅ **Do:**
- Give focused, specific tasks
- Include all context needed
- Define clear success criteria
- Handle failures gracefully

❌ **Don't:**
- Give vague or broad tasks
- Assume subagent knows context
- Ignore failures
- Spawn too many at once

## Integration Testing

After all subagents complete:

```markdown
1. Run integration tests
2. Verify all parts work together
3. Check for edge cases
4. Validate overall behavior
```

## When to Use Subagents

✅ **Use when:**
- Multiple independent tasks
- Parallel execution beneficial
- Tasks require isolation
- Complex work can be decomposed

❌ **Don't use when:**
- Tasks are sequential
- Overhead exceeds benefit
- Simple, single-step work
- Tight coordination needed
