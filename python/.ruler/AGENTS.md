
# Python Backend Development Standards

## Project Structure

```
python/
├── mesh_toolkit/          # Meshy API client library
│   └── src/mesh_toolkit/
│       ├── api/           # HTTP client
│       ├── services/      # Business logic
│       ├── persistence/   # Database & file storage
│       └── webhooks/      # Webhook handlers
├── crew_agents/           # CrewAI orchestration
│   └── src/crew_agents/
│       └── adapters/      # MCP tool adapters
└── tests/
    ├── unit/              # Fast, mocked tests
    └── integration/       # Real API calls (VCR)
```

## Testing Standards

### VCR for Expensive APIs
```python
import pytest

@pytest.mark.vcr()
def test_meshy_text3d_creates_otter():
    """VCR records on first run, replays after"""
    client = MeshyClient(api_key="test")
    task_id = client.create_text3d(prompt="otter")
    assert task_id.startswith("018")
```

See [testing_conventions.md](./testing_conventions.md) for details.

## Type Hints Required

```python
# ✅ Good
def process_webhook(
    payload: WebhookPayload,
    repository: AssetRepository
) -> WebhookResult:
    ...

# ❌ Bad
def process_webhook(payload, repository):
    ...
```

## Error Handling

### Use Result Types
```python
from typing import TypedDict

class Success(TypedDict):
    ok: Literal[True]
    value: T

class Failure(TypedDict):
    ok: Literal[False]
    error: Exception

Result = Success | Failure
```

## CrewAI Standards

See [crew_agents/.ruler/workflow_configuration.md](../crew_agents/.ruler/workflow_configuration.md) for agent hierarchy and MCP tool access patterns.
