# Webhook Recording Infrastructure

## Overview

This infrastructure enables proper integration testing of the Meshy SDK's webhook-based architecture by recording real webhook payloads from actual Meshy API calls.

## Architecture

```
┌─────────────┐                    ┌──────────────┐
│             │  1. create_task    │              │
│   pytest    ├───────────────────>│  Meshy API   │
│             │   (w/ callback)    │              │
└──────┬──────┘                    └──────┬───────┘
       │                                  │
       │  4. assert                       │ 2. webhook
       │     payload                      │    POST
       │                                  │
       v                                  v
┌─────────────┐                    ┌──────────────┐
│  Webhook    │<───────────────────│    ngrok     │
│  Storage    │  3. save payload   │   tunnel     │
└─────────────┘                    └──────┬───────┘
                                          │
                                          v
                                   ┌──────────────┐
                                   │   FastAPI    │
                                   │   Receiver   │
                                   └──────────────┘
```

## Components

### 1. FastAPI Webhook Receiver (`app.py`)
- Receives POST requests from Meshy
- Stores payload + headers to JSON files
- Endpoint pattern: `/webhook/{species}/{task_type}`

### 2. Pytest Fixtures (`fixtures.py`)
- `webhook_recorder`: Main fixture for recording mode
- `webhook_server()`: Context manager for local FastAPI server
- `ngrok_tunnel()`: Context manager for public tunnel

### 3. Webhook Storage
- Location: `tests/integration/cassettes/webhooks/`
- Filename pattern: `{species}_{task_type}_{task_id}.json`
- Contents: Full webhook payload + headers + timestamp

## Usage

### Recording Mode (Real API Calls)

```bash
# Set Meshy API key
export MESHY_API_KEY="your_key_here"

# Run tests in recording mode
cd python
uv run pytest tests/integration/test_otter_pipeline.py \
    --record-webhooks \
    --record-mode=new_episodes
```

**What happens:**
1. Test starts local webhook server on port 8000
2. Creates ngrok tunnel to expose localhost
3. Submits real Meshy task with ngrok callback URL
4. Waits for webhook from Meshy (up to 5 minutes)
5. Saves webhook payload to `cassettes/webhooks/`
6. pytest-vcr records HTTP traffic to cassettes
7. Test continues with recorded data

### Replay Mode (No API Calls)

```bash
# Run tests with recorded data
cd python
uv run pytest tests/integration/test_otter_pipeline.py
```

**What happens:**
1. pytest-vcr replays HTTP cassettes (no real API calls)
2. Test loads pre-recorded webhook payloads from JSON
3. Feeds webhook to WebhookHandler
4. Validates repository state + artifact downloads

## Example Test

```python
import pytest
from mesh_toolkit.services.text3d_service import Text3DService

@pytest.mark.vcr()
@pytest.mark.record_webhook
def test_text3d_with_webhook(
    base_client,
    test_repository,
    webhook_recorder,
    vcr_cassette
):
    """Test text-to-3d with real webhook"""
    service = Text3DService(base_client, test_repository)
    
    # Get callback URL from recorder
    callback_url = webhook_recorder.get_callback_url("otter", "text3d")
    
    # Submit task (recorded by VCR)
    submission = service.submit_task(
        species="otter",
        prompt="Cute otter character, sculpture style",
        callback_url=callback_url
    )
    
    # Wait for webhook (only in record mode)
    webhook_payload = webhook_recorder.get_payload(
        "otter", 
        "text3d", 
        submission.task_id,
        timeout=300  # 5 minutes max
    )
    
    # Validate webhook
    assert webhook_payload["status"] == "SUCCEEDED"
    assert webhook_payload["task_id"] == submission.task_id
    assert "model_urls" in webhook_payload
```

## Workflow

### First Time (Recording)

1. Install ngrok: `brew install ngrok` (or download from ngrok.com)
2. Set MESHY_API_KEY environment variable
3. Run with `--record-webhooks --record-mode=new_episodes`
4. Tests will:
   - Make real API calls (cost credits)
   - Wait for real webhooks
   - Save everything for replay

### Subsequent Runs (Replay)

1. Run normal pytest (no flags)
2. Tests use recorded data
3. No API calls, no waiting, instant results

## Files Generated

### VCR Cassettes
- `cassettes/test_otter_pipeline/test_text3d_with_webhook.yaml`
- Contains HTTP request/response to Meshy API

### Webhook Payloads
- `cassettes/webhooks/otter_text3d_{task_id}.json`
- Contains webhook payload + headers from Meshy

## Limitations

- Requires ngrok for recording mode
- Recording mode costs Meshy API credits
- Webhooks can take 2-5 minutes to arrive
- ngrok free tier has connection limits

## Pytest Markers

```python
@pytest.mark.vcr()              # Use pytest-vcr cassettes
@pytest.mark.record_webhook     # Enable webhook recording
@pytest.mark.webhook_integration # Mark as webhook integration test
@pytest.mark.polling_integration # Mark as polling fallback test
```

## Configuration

Add to `pytest.ini`:

```ini
[pytest]
markers =
    record_webhook: Tests that record real webhooks
    webhook_integration: Webhook-based integration tests
    polling_integration: Polling-based integration tests
```
