---
name: superpowers-test-driven-development
description: "MUST use for ALL code implementation. Strict RED-GREEN-REFACTOR cycle with tests written FIRST. No code without tests. Use whenever writing, modifying, or debugging code."
---

# Test-Driven Development Skill

**Purpose:** Write tests FIRST, then implement code to pass them.

## CRITICAL RULES

1. **Tests FIRST, always** - Never write implementation before test
2. **One test at a time** - Focus on single behavior
3. **Minimal implementation** - Write only enough to pass
4. **Refactor safely** - Only when all tests pass
5. **No skipping steps** - Follow RED-GREEN-REFACTOR strictly

## TDD Cycle

### RED: Write a Failing Test

```python
# 1. Write test for desired behavior
def test_new_feature():
    result = my_function(input)
    assert result == expected_output

# 2. Run test - MUST fail
# pytest tests/test_my_function.py -v
```

### GREEN: Make Test Pass

```python
# 3. Write MINIMAL implementation
def my_function(input):
    return expected_output  # Simplest possible

# 4. Run test - MUST pass
# pytest tests/test_my_function.py -v
```

### REFACTOR: Improve Code

```python
# 5. Refactor while tests pass
def my_function(input):
    # Improved implementation
    return result

# 6. Run ALL tests - MUST still pass
# pytest tests/ -v
```

## Test File Organization

```
tests/
├── test_module1.py
├── test_module2.py
└── conftest.py  # Shared fixtures
```

## Writing Good Tests

### Test Naming
```python
def test_[what]_[when]_[expected]():
    # Example:
    def test_calculate_total_with_empty_cart_returns_zero():
        pass
```

### Test Structure
```python
def test_behavior():
    # Arrange - Set up test data
    input_data = setup_test_data()
    
    # Act - Execute the behavior
    result = function_under_test(input_data)
    
    # Assert - Verify the result
    assert result == expected_value
```

### Edge Cases to Test
- Empty inputs
- Null/None values
- Boundary values
- Error conditions
- Concurrent access (if applicable)

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_module.py -v

# Run specific test
pytest tests/test_module.py::test_function -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

## TDD Checklist

Before writing any code:
- [ ] Write failing test
- [ ] Verify test fails (RED)
- [ ] Write minimal implementation
- [ ] Verify test passes (GREEN)
- [ ] Refactor if needed
- [ ] Verify all tests still pass

## Common TDD Mistakes

❌ Writing implementation first
❌ Writing multiple tests at once
❌ Writing too much implementation
❌ Skipping refactor step
❌ Not running tests frequently

## TDD Benefits

- **Confidence** - Tests prove code works
- **Design** - Tests drive better design
- **Documentation** - Tests show how to use code
- **Refactoring** - Tests catch regressions
- **Debugging** - Tests isolate problems

## When TDD Feels Slow

TDD feels slow when:
- Learning new domain
- Dealing with complex setup
- Working with legacy code

Solution:
- Start with simplest test
- Build up complexity gradually
- Use test fixtures for setup
- Refactor tests too
