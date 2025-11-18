"""Pytest fixtures for webhook recording infrastructure"""
import os
import time
import threading
from pathlib import Path
from contextlib import contextmanager

import pytest
import uvicorn
from pyngrok import ngrok


@contextmanager
def webhook_server(port: int = 8000):
    """Context manager to run webhook server"""
    from python.tests.integration.webhook_server.app import app
    
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    
    time.sleep(1)
    
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        thread.join(timeout=5)


@contextmanager
def ngrok_tunnel(port: int = 8000):
    """Context manager to create ngrok tunnel"""
    tunnel = ngrok.connect(port, "http")
    public_url = tunnel.public_url
    
    print(f"[NGROK] Tunnel opened: {public_url}")
    
    try:
        yield public_url
    finally:
        ngrok.disconnect(public_url)
        print(f"[NGROK] Tunnel closed: {public_url}")


@pytest.fixture
def webhook_recorder(request):
    """Fixture for webhook recording mode
    
    Usage in test:
        @pytest.mark.record_webhook
        def test_something(webhook_recorder):
            callback_url = webhook_recorder.get_callback_url("otter", "text3d")
            # Submit task with callback_url
            # Wait for webhook
            payload = webhook_recorder.get_payload("otter", "text3d", task_id)
    """
    record_mode = request.config.getoption("--record-webhooks", default=False)
    
    if not record_mode:
        pytest.skip("Webhook recording disabled, use --record-webhooks to enable")
    
    port = 8000
    
    with webhook_server(port) as local_url:
        with ngrok_tunnel(port) as public_url:
            yield WebhookRecorder(public_url)


class WebhookRecorder:
    """Helper for webhook recording"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.storage_dir = Path(__file__).parent.parent / "cassettes" / "webhooks"
    
    def get_callback_url(self, species: str, task_type: str) -> str:
        """Get callback URL for Meshy"""
        return f"{self.base_url}/webhook/{species}/{task_type}"
    
    def get_payload(self, species: str, task_type: str, task_id: str, timeout: int = 300) -> dict:
        """Wait for and retrieve webhook payload"""
        storage_file = self.storage_dir / f"{species}_{task_type}_{task_id}.json"
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if storage_file.exists():
                import json
                return json.loads(storage_file.read_text())
            time.sleep(2)
        
        raise TimeoutError(f"Webhook not received within {timeout}s for {task_id}")


def pytest_addoption(parser):
    """Add pytest command-line options"""
    parser.addoption(
        "--record-webhooks",
        action="store_true",
        default=False,
        help="Enable webhook recording mode (requires ngrok)"
    )
