---
name: superpowers-writing-plans
description: "ALWAYS create plans before implementation. Generates self-contained planning documents with all context needed for successful execution. Use when starting new work, adding features, or before any coding task."
---

# Writing Plans Skill

**Purpose:** Create detailed, self-contained plans BEFORE implementation.

## When to Use

- Before starting any new work
- Before adding new features
- When work is complex or multi-step
- When coordination with other work is needed
- When context needs to be preserved

## Plan Structure

### Header
```markdown
# Plan: [Feature/Task Name]

**Status:** Not Started | In Progress | Complete
**Date:** YYYY-MM-DD
**Author:** [Name]
```

### Context
```markdown
## Context

### Background
[Why this work is needed]

### Current State
[What exists today]

### Goal
[What we're trying to achieve]
```

### Technical Details
```markdown
## Technical Details

### Architecture
[System design decisions]

### Dependencies
[External systems, libraries, APIs]

### Constraints
[Limitations, requirements]
```

### Implementation Steps
```markdown
## Implementation Steps

### Phase 1: [Name]
1. [Step 1]
2. [Step 2]

### Phase 2: [Name]
1. [Step 1]
2. [Step 2]
```

### Testing Strategy
```markdown
## Testing Strategy

### Unit Tests
[What to test]

### Integration Tests
[How to test integrations]

### Manual Testing
[Manual verification steps]
```

### Risks and Mitigations
```markdown
## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | High/Med/Low | [Mitigation] |
```

### Success Criteria
```markdown
## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
```

## Plan Quality Checklist

Before considering a plan complete:

- [ ] Context is clear and complete
- [ ] All dependencies identified
- [ ] Implementation steps are actionable
- [ ] Testing strategy is defined
- [ ] Risks are identified with mitigations
- [ ] Success criteria are measurable

## Plan File Naming

Plans should be stored in a `plans/` directory:

```
plans/
├── 001-feature-name.md
├── 002-another-feature.md
└── 003-bug-fix.md
```

## Using Plans

### Reading a Plan
1. Read the full plan before starting work
2. Understand the context and goals
3. Follow the implementation steps
4. Update status as you progress

### Updating a Plan
1. Update status field as work progresses
2. Add notes about decisions made
3. Document any deviations from the plan
4. Mark steps as complete

### Completing a Plan
1. Verify all success criteria met
2. Run all tests
3. Update status to "Complete"
4. Add completion notes

## Plan Review

Plans should be reviewed for:
- Completeness of context
- Clarity of implementation steps
- Realistic time estimates
- Adequate testing strategy
- Risk identification
