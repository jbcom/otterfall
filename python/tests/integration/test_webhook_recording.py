"""Integration tests with webhook recording

These tests demonstrate proper integration testing with real Meshy API calls
and webhook payloads.

Recording mode (requires ngrok + API key):
    cd python
    export MESHY_API_KEY="your_key_here"
    uv run pytest tests/integration/test_webhook_recording.py \\
        --record-webhooks \\
        --record-mode=new_episodes

Replay mode (uses recorded cassettes):
    cd python
    uv run pytest tests/integration/test_webhook_recording.py
"""
import pytest
from pathlib import Path
from mesh_toolkit.api.base_client import BaseHttpClient
from mesh_toolkit.services.text3d_service import Text3DService
from mesh_toolkit.webhooks.handler import WebhookHandler
from mesh_toolkit.webhooks.schemas import MeshyWebhookPayload


@pytest.mark.webhook_integration
@pytest.mark.vcr()
def test_text3d_with_real_webhook(
    meshy_api_key,
    test_repository,
    webhook_recorder,
    glb_fixtures_dir
):
    """Test text-to-3d with real Meshy webhook
    
    Recording mode:
    - Creates real Meshy task with ngrok callback
    - Waits for real webhook from Meshy
    - Records HTTP traffic + webhook payload
    
    Replay mode:
    - Uses VCR cassette for API calls
    - Loads recorded webhook payload
    - Validates webhook handler logic
    """
    client = BaseHttpClient(api_key=meshy_api_key)
    service = Text3DService(client, test_repository)
    
    callback_url = webhook_recorder.get_callback_url("otter", "text3d")
    
    submission = service.submit_task(
        species="otter",
        prompt="Cute otter character, sculpture style, detailed fur",
        callback_url=callback_url,
        art_style="sculpture",
        model_version="latest",
        enable_pbr=True
    )
    
    assert submission.task_id
    assert submission.species == "otter"
    assert submission.service == "text3d"
    
    webhook_data = webhook_recorder.get_payload(
        "otter",
        "text3d",
        submission.task_id,
        timeout=300
    )
    
    assert webhook_data["status"] == "SUCCEEDED"
    assert webhook_data["task_id"] == submission.task_id
    assert "model_urls" in webhook_data
    assert webhook_data["model_urls"]["glb"]
    
    webhook_payload = MeshyWebhookPayload(**webhook_data)
    handler = WebhookHandler(
        repository=test_repository,
        download_dir=glb_fixtures_dir
    )
    
    response = handler.handle_webhook(webhook_payload)
    
    assert response.status == 200
    assert response.message == "Webhook processed successfully"
    
    glb_path = glb_fixtures_dir / "otter" / "sculptured.glb"
    assert glb_path.exists()
    assert glb_path.stat().st_size > 0


@pytest.mark.webhook_integration
def test_text3d_with_fixture_webhook(
    meshy_api_key,
    test_repository,
    webhook_payload_loader,
    glb_fixtures_dir
):
    """Test text-to-3d with pre-recorded webhook fixture
    
    This test uses a pre-recorded webhook payload fixture
    instead of waiting for a real webhook. Use this pattern
    for unit tests or when webhook recording isn't available.
    """
    webhook_data = webhook_payload_loader("text3d_success.json")
    
    handler = WebhookHandler(
        repository=test_repository,
        download_dir=glb_fixtures_dir
    )
    
    response = handler.handle_webhook(webhook_data)
    
    assert response.status == 200
    assert webhook_data.status == "SUCCEEDED"


