---
name: superpowers-brainstorming
description: "MUST activate before ANY creative, design, or implementation work. Use when starting new features, architectural decisions, UI/UX design, API design, data modeling, or any task without a complete specification. Transforms vague ideas into precise, actionable plans."
---

# Brainstorming Skill

**Purpose:** Refine ideas through questions BEFORE implementation.

## When to Use

- Starting a new feature or project
- Making architectural decisions
- Designing APIs or data models
- User request is vague or incomplete
- Multiple valid approaches exist

## CRITICAL BRAINSTORMING RULES

**When brainstorming/design phase is active:**

1. **DO NOT write code** - Think, question, and discuss
2. **DO NOT create files** - Explore the idea space
3. **DO NOT make implementation decisions** - Consider options
4. **DO ask questions** - About requirements, constraints, and context
5. **DO explore alternatives** - Present different approaches
6. **DO challenge assumptions** - Validate understanding
7. **DO identify gaps** - In requirements or understanding

## Brainstorming Flow

```
User request → Ask clarifying questions → Present options → Get feedback → Refine approach → Document decisions → THEN implement
```

## Question Categories

### Requirements Questions
- What problem does this solve?
- Who are the users?
- What are the success criteria?
- What are the constraints (time, resources, technology)?

### Technical Questions
- What existing systems does this interact with?
- What are the performance requirements?
- What are the security considerations?
- What are the scalability needs?

### Design Questions
- What are the main user flows?
- What are the edge cases?
- What are the error scenarios?
- What are the alternative approaches?

## Brainstorming Completion

Brainstorming is complete when:

1. **All major questions answered** - No critical unknowns remain
2. **Approach agreed upon** - Clear direction established
3. **Constraints understood** - Known limitations documented
4. **Scope defined** - What's in/out is clear

## Documenting Brainstorming Results

After brainstorming, document:

```markdown
## Brainstorming Summary

### Problem Statement
[Clear description of what we're solving]

### Key Decisions
1. [Decision 1] - [Rationale]
2. [Decision 2] - [Rationale]

### Approach
[High-level approach description]

### Open Questions
- [Any remaining questions]

### Next Steps
- [What happens next]
```

## Transitioning to Implementation

After brainstorming:
1. Document the decisions made
2. Create a plan (use `superpowers-writing-plans` skill)
3. Set up git worktree if needed (use `superpowers-using-git-worktrees` skill)
4. Begin implementation with TDD (use `superpowers-test-driven-development` skill)
