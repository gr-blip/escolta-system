---
name: superpowers-writing-skills
description: "Create and maintain skills for reusable workflows. Use when identifying repeated patterns, complex procedures, or domain-specific knowledge that should be captured."
---

# Writing Skills Skill

**Purpose:** Create and maintain reusable skill definitions.

## When to Use

- Identifying repeated patterns
- Complex procedures need documentation
- Domain-specific knowledge to capture
- Workflows that benefit from standardization

## Skill Creation Flow

```
Identify need → Plan skill → Create structure → Write content → Test → Deploy
```

## Step 1: Identify Need

### When to Create a Skill

```markdown
Create a skill when:
- Same workflow repeated 3+ times
- Complex procedure with many steps
- Domain knowledge needs capturing
- Team needs standardization
```

### Skill Scope

```markdown
Good skill scope:
- Focused on one workflow
- Clear boundaries
- Manageable size
- Clear value add

Bad skill scope:
- Too broad
- Too complex
- Too narrow
- Unclear value
```

## Step 2: Plan Skill

### Skill Structure

```markdown
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter
│   │   ├── name: skill-name
│   │   └── description: What it does
│   └── Markdown instructions
└── Optional resources
    ├── scripts/
    ├── references/
    └── assets/
```

### Content Planning

```markdown
1. What triggers the skill?
2. What instructions are needed?
3. What resources are helpful?
4. What examples are useful?
```

## Step 3: Create Structure

### Initialize Skill

```bash
# Use skill-creator to initialize
python scripts/init_skill.py skill-name --path ./skills
```

### Directory Structure

```markdown
skill-name/
├── SKILL.md
├── scripts/          # Optional
├── references/       # Optional
└── assets/          # Optional
```

## Step 4: Write Content

### YAML Frontmatter

```yaml
---
name: skill-name
description: "Clear description of when to use this skill"
---
```

### SKILL.md Body

```markdown
# Skill Name

## When to Use
[Clear trigger conditions]

## Workflow
[Step-by-step instructions]

## Examples
[Concrete examples]

## Resources
[Reference materials]
```

### Writing Guidelines

```markdown
✅ Do:
- Be concise
- Use imperative form
- Include examples
- Reference resources

❌ Don't:
- Be verbose
- Use passive voice
- Omit examples
- Duplicate content
```

## Step 5: Test Skill

### Testing Checklist

```markdown
- [ ] Skill triggers correctly
- [ ] Instructions are clear
- [ ] Examples work
- [ ] Resources are helpful
- [ ] No ambiguity
```

### Testing Process

```markdown
1. Test with real scenarios
2. Verify instructions work
3. Check for edge cases
4. Gather feedback
```

## Step 6: Deploy Skill

### Deployment Steps

```markdown
1. Package skill
2. Share with team
3. Document usage
4. Gather feedback
```

### Skill Maintenance

```markdown
1. Update as needed
2. Fix issues
3. Add improvements
4. Archive if obsolete
```

## Skill Quality Checklist

Before deploying:

- [ ] Clear description
- [ ] Focused scope
- [ ] Complete instructions
- [ ] Helpful examples
- [ ] Useful resources
- [ ] Tested thoroughly

## Common Skill Patterns

### Workflow Skill

```markdown
## When to Use
[Trigger conditions]

## Workflow
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Verification
[How to verify success]
```

### Reference Skill

```markdown
## When to Use
[When to reference]

## Reference
[Key information]

## Examples
[Usage examples]
```

### Tool Skill

```markdown
## When to Use
[When to use tool]

## Commands
[Command reference]

## Examples
[Usage examples]
```

## Skill Naming Conventions

### Good Names

```markdown
- test-driven-development
- code-review-workflow
- api-design-patterns
- database-migration
```

### Bad Names

```markdown
- my-skill
- stuff
- helper
- utils
```

## Skill Description Guidelines

### Good Descriptions

```markdown
"MUST use for ALL code implementation. Strict RED-GREEN-REFACTOR cycle with tests written FIRST."

"ALWAYS create plans before implementation. Generates self-contained planning documents."
```

### Bad Descriptions

```markdown
"A skill for coding"

"Helps with development"
```

## Skill Resources

### Scripts

```markdown
Use when:
- Deterministic reliability needed
- Same code rewritten repeatedly
- Complex calculations
```

### References

```markdown
Use when:
- Detailed documentation needed
- API specifications
- Domain knowledge
```

### Assets

```markdown
Use when:
- Templates needed
- Images/icons used
- Boilerplate code
```

## Skill Maintenance

### Regular Updates

```markdown
1. Review usage patterns
2. Gather feedback
3. Update content
4. Test changes
```

### Deprecation

```markdown
When skill is obsolete:
1. Mark as deprecated
2. Provide alternative
3. Archive skill
4. Remove from active use
```

## Skill Best Practices

✅ **Do:**
- Keep skills focused
- Write clear instructions
- Include examples
- Test thoroughly

❌ **Don't:**
- Make skills too broad
- Write vague instructions
- Omit examples
- Skip testing
