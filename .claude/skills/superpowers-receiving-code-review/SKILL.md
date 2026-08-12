---
name: superpowers-receiving-code-review
description: "Handle code review feedback properly. Use when receiving review comments and need to address feedback systematically."
---

# Receiving Code Review Skill

**Purpose:** Handle code review feedback systematically.

## When to Use

- Receiving review comments
- Need to address feedback
- Updating code based on review
- Responding to reviewer questions

## Review Response Flow

```
Read feedback → Understand concerns → Plan changes → Make changes → Respond → Re-request review
```

## Step 1: Read Feedback

### Understand All Comments

```markdown
1. Read all comments carefully
2. Note specific concerns
3. Identify patterns
4. Prioritize by importance
```

### Categorize Feedback

```markdown
Categories:
- **Must Fix** - Critical issues
- **Should Fix** - Important improvements
- **Consider** - Suggestions
- **Question** - Clarifications needed
```

## Step 2: Understand Concerns

### Analyze Each Comment

```markdown
For each comment:
1. What is the concern?
2. Why is it important?
3. What is the expected change?
4. How to address it?
```

### Ask for Clarification

```markdown
If unclear:
1. Ask specific questions
2. Provide context
3. Suggest alternatives
4. Wait for response
```

## Step 3: Plan Changes

### Create Action Plan

```markdown
## Action Plan

### [Comment 1]
- **Concern:** [What reviewer said]
- **Action:** [What you'll do]
- **Priority:** High/Medium/Low

### [Comment 2]
- **Concern:** [What reviewer said]
- **Action:** [What you'll do]
- **Priority:** High/Medium/Low
```

### Estimate Effort

```markdown
For each action:
- Time required
- Complexity
- Dependencies
- Risk level
```

## Step 4: Make Changes

### Implement Fixes

```markdown
1. Address each comment
2. Make minimal changes
3. Test each change
4. Update documentation
```

### Test Changes

```markdown
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing done
- [ ] No regressions
```

## Step 5: Respond to Feedback

### Response Template

```markdown
## Feedback Response

### [Comment 1]
- **Action:** [What was done]
- **Result:** [Outcome]
- **Notes:** [Any additional context]

### [Comment 2]
- **Action:** [What was done]
- **Result:** [Outcome]
- **Notes:** [Any additional context]
```

### Response Best Practices

```markdown
✅ Do:
- Be specific about changes
- Reference code changes
- Explain reasoning
- Thank reviewer

❌ Don't:
- Be defensive
- Ignore comments
- Make excuses
- Rush responses
```

## Step 6: Re-request Review

### Prepare for Re-review

```markdown
- [ ] All comments addressed
- [ ] All changes tested
- [ ] Documentation updated
- [ ] Response written
```

### Re-review Request

```markdown
## Re-review Request

### Summary
[What was changed]

### Changes Made
- [Change 1]
- [Change 2]

### Comments Addressed
- [Comment 1] - [Resolution]
- [Comment 2] - [Resolution]

### Notes
[Any additional context]
```

## Handling Different Feedback Types

### Critical Issues

```markdown
Reviewer: "This will cause a data leak"

Response:
1. Acknowledge severity
2. Fix immediately
3. Add tests
4. Document fix
```

### Style Issues

```markdown
Reviewer: "Inconsistent naming"

Response:
1. Fix naming
2. Update related code
3. Run linter
4. Note for future
```

### Questions

```markdown
Reviewer: "Why did you do it this way?"

Response:
1. Explain reasoning
2. Provide context
3. Consider alternatives
4. Discuss tradeoffs
```

### Suggestions

```markdown
Reviewer: "Consider using X instead"

Response:
1. Evaluate suggestion
2. Explain decision
3. Implement if better
4. Thank reviewer
```

## Common Review Scenarios

### Scenario 1: Multiple Issues

```markdown
1. Prioritize by severity
2. Fix critical first
3. Address all issues
4. Test thoroughly
```

### Scenario 2: Disagreement

```markdown
1. Understand reviewer's perspective
2. Explain your reasoning
3. Discuss alternatives
4. Reach consensus
```

### Scenario 3: Complex Changes

```markdown
1. Break into smaller changes
2. Address incrementally
3. Test each change
4. Update reviewer
```

## Review Response Checklist

Before re-requesting review:

- [ ] All comments read
- [ ] All concerns understood
- [ ] All changes made
- [ ] All changes tested
- [ ] All responses written
- [ ] Documentation updated

## When Review Takes Long

### If Review is Delayed

```markdown
1. Follow up politely
2. Provide context
3. Offer to help
4. Be patient
```

### If Reviewer is Unavailable

```markdown
1. Request new reviewer
2. Provide context
3. Share previous feedback
4. Continue work
```

## Learning from Reviews

### Track Patterns

```markdown
Common feedback patterns:
- [Pattern 1]
- [Pattern 2]
- [Pattern 3]
```

### Improve Skills

```markdown
Based on feedback:
1. Learn new patterns
2. Update coding style
3. Improve testing
4. Share knowledge
```
