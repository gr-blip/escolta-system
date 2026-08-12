---
name: superpowers-verification-before-completion
description: "ALWAYS verify before marking work complete. Comprehensive verification checklist to ensure quality. Use when work appears complete and before requesting review or merging."
---

# Verification Before Completion Skill

**Purpose:** Verify work is truly complete before marking done.

## CRITICAL RULE

**NEVER mark work complete without verification. ALWAYS run full checklist.**

## Verification Flow

```
Run tests → Check quality → Verify requirements → Document → THEN mark complete
```

## Verification Checklist

### 1. Code Quality

```markdown
- [ ] Code follows style guidelines
- [ ] No lint errors
- [ ] No type errors
- [ ] Consistent naming
- [ ] Proper comments
```

### 2. Testing

```markdown
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Edge cases tested
- [ ] Error handling tested
- [ ] Coverage acceptable
```

### 3. Functionality

```markdown
- [ ] All requirements met
- [ ] All features work
- [ ] All bugs fixed
- [ ] No regressions
- [ ] Performance acceptable
```

### 4. Documentation

```markdown
- [ ] Code commented
- [ ] README updated
- [ ] API docs updated
- [ ] CHANGELOG updated
- [ ] Examples provided
```

### 5. Security

```markdown
- [ ] No security vulnerabilities
- [ ] Input validation
- [ ] Authentication checks
- [ ] Authorization checks
- [ ] Data protection
```

### 6. Performance

```markdown
- [ ] No performance regressions
- [ ] Efficient algorithms
- [ ] Proper caching
- [ ] Resource management
- [ ] Scalability considered
```

## Running Verification

### Step 1: Run All Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# All tests with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

### Step 2: Run Quality Checks

```bash
# Linting
flake8 src/ tests/

# Type checking
mypy src/

# Formatting
black --check src/ tests/
```

### Step 3: Manual Verification

```markdown
1. Test main user flows
2. Test edge cases
3. Test error scenarios
4. Test performance
```

## Verification Report

### Report Template

```markdown
## Verification Report

### Summary
[Brief overview]

### Test Results
- Unit Tests: [X/X passed]
- Integration Tests: [X/X passed]
- Coverage: [X%]

### Quality Checks
- Lint: [Pass/Fail]
- Types: [Pass/Fail]
- Format: [Pass/Fail]

### Manual Testing
- [Test 1]: [Pass/Fail]
- [Test 2]: [Pass/Fail]

### Issues Found
- [Issue 1]: [Description]
- [Issue 2]: [Description]

### Conclusion
[Ready/Not Ready for completion]
```

## Common Verification Issues

### Issue: Tests Failing

```markdown
1. Identify failing tests
2. Analyze failures
3. Fix issues
4. Re-run tests
```

### Issue: Low Coverage

```markdown
1. Identify uncovered code
2. Write additional tests
3. Focus on critical paths
4. Re-check coverage
```

### Issue: Lint Errors

```markdown
1. Run linter
2. Fix errors
3. Re-run linter
4. Verify clean
```

## Verification Best Practices

✅ **Do:**
- Run all checks
- Test thoroughly
- Document results
- Fix all issues

❌ **Don't:**
- Skip tests
- Ignore warnings
- Rush verification
- Mark incomplete

## When Verification Fails

### If Issues Found

```markdown
1. Document issues
2. Prioritize fixes
3. Fix critical first
4. Re-verify
5. Update report
```

### If Not Ready

```markdown
1. List remaining work
2. Estimate effort
3. Plan completion
4. Communicate status
```

## Completion Criteria

Work is complete when:

```markdown
- [ ] All tests pass
- [ ] All checks pass
- [ ] All requirements met
- [ ] Documentation complete
- [ ] No known issues
- [ ] Review approved
```

## After Verification

### If Verification Passes

```markdown
1. Mark work complete
2. Request review
3. Prepare for merge
4. Clean up
```

### If Verification Fails

```markdown
1. Document failures
2. Fix issues
3. Re-verify
4. Update status
```

## Verification Tools

### Test Runners

```bash
# pytest
pytest tests/ -v

# Jest
npm test

# Go test
go test ./...
```

### Quality Tools

```bash
# Linters
flake8, eslint, golint

# Type checkers
mypy, tsc, go vet

# Formatters
black, prettier, gofmt
```

### Coverage Tools

```bash
# Python
pytest --cov=src

# JavaScript
npm test -- --coverage

# Go
go test -cover
```

## Verification Checklist Summary

Before marking complete:

- [ ] All tests pass
- [ ] All quality checks pass
- [ ] All requirements met
- [ ] Documentation complete
- [ ] No known issues
- [ ] Ready for review
- [ ] Ready for merge
