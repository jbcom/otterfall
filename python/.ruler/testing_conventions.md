
# Python Testing Conventions

## Test Organization

```
tests/
├── unit/              # Fast, isolated tests with mocks
├── integration/       # Real API calls with VCR cassettes
└── conftest.py        # Shared fixtures
```

## VCR Recording Strategy

- Use `pytest-vcr` for expensive API calls (Meshy)
- Record once, replay for free
- Cassettes stored in `tests/integration/cassettes/`
- Download artifacts to `tests/integration/fixtures/`

## Test Naming

```python
# Good
def test_text3d_service_creates_task_with_valid_spec():
    pass

# Bad
def test_stuff():
    pass
```

## Assertion Style

Use descriptive assertions with context:

```python
assert result.status == TaskStatus.SUCCEEDED, \
    f"Expected SUCCEEDED but got {result.status}"
```
