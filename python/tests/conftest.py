"""Pytest configuration and shared fixtures"""
import os
import json
import pytest
import tempfile
import shutil
from pathlib import Path
from mesh_toolkit.persistence.repository import TaskRepository
from mesh_toolkit.webhooks.handler import WebhookHandler
from mesh_toolkit.webhooks.schemas import MeshyWebhookPayload

# Only load integration fixtures if pyngrok is available
try:
    import pyngrok  # noqa: F401
    pytest_plugins = ["tests.integration.webhook_server.fixtures"]
except ImportError:
    pytest_plugins = []


@pytest.fixture(scope="session")
def vcr_config():
    """Configure pytest-vcr for recording HTTP interactions"""
    return {
        "filter_headers": ["authorization"],
        "record_mode": "once",
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "cassette_library_dir": "tests/integration/cassettes",
    }


@pytest.fixture(scope="session")
def meshy_api_key():
    """Get Meshy API key from environment"""
    api_key = os.getenv("MESHY_API_KEY")
    if not api_key:
        pytest.skip("MESHY_API_KEY not set")
    return api_key


@pytest.fixture(scope="session")
def glb_fixtures_dir():
    """Directory for GLB fixtures"""
    fixtures_dir = Path("tests/integration/fixtures/glb")
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    return fixtures_dir


@pytest.fixture(scope="session")
def webhook_fixtures_dir():
    """Directory for webhook payload fixtures"""
    fixtures_dir = Path("tests/integration/fixtures/webhooks")
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    return fixtures_dir


@pytest.fixture
def test_repository():
    """Create a temporary test repository"""
    temp_dir = tempfile.mkdtemp()
    repository = TaskRepository(base_path=temp_dir)
    yield repository
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def webhook_payload_loader(webhook_fixtures_dir):
    """Load webhook payload fixtures from JSON files"""
    def load_payload(filename: str) -> MeshyWebhookPayload:
        payload_path = webhook_fixtures_dir / filename
        with open(payload_path, 'r') as f:
            data = json.load(f)
        return MeshyWebhookPayload(**data)
    return load_payload


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "record_webhook: Tests that record real webhooks from Meshy API"
    )
    config.addinivalue_line(
        "markers", "webhook_integration: Webhook-based integration tests"
    )
