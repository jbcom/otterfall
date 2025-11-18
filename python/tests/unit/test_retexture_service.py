"""Unit tests for RetextureService"""
import pytest
from unittest.mock import Mock
import httpx
from mesh_toolkit.services.retexture_service import RetextureService
from mesh_toolkit.api.base_client import BaseHttpClient
from mesh_toolkit.persistence.repository import TaskRepository
from mesh_toolkit.persistence.schemas import TaskSubmission, TaskStatus


class TestRetextureService:
    """Test RetextureService webhook submission"""
    
    @pytest.fixture
    def mock_client(self, mocker):
        """Mock BaseHttpClient"""
        mocker.patch.dict("os.environ", {"MESHY_API_KEY": "test_key"})
        client = Mock(spec=BaseHttpClient)
        return client
    
    @pytest.fixture
    def mock_repository(self, mocker):
        """Mock TaskRepository"""
        repo = Mock(spec=TaskRepository)
        repo.compute_spec_hash.return_value = "hash456"
        return repo
    
    @pytest.fixture
    def service(self, mock_client, mock_repository):
        """Create RetextureService with mocked dependencies"""
        return RetextureService(mock_client, mock_repository)
    
    def test_submit_task_basic_payload(self, service, mock_client, mock_repository):
        """Test submit_task builds correct payload with defaults"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"result": "retex_task_123"}
        mock_client.request.return_value = mock_response
        
        submission = service.submit_task(
            species="otter",
            model_id="model_456",
            prompt="grey fur texture",
            callback_url="http://example.com/webhook"
        )
        
        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        
        assert call_args[0] == ("POST", "retexture")
        assert call_args[1]["api_version"] == "v1"
        
        payload = call_args[1]["json"]
        assert payload["model_id"] == "model_456"
        assert payload["prompt"] == "grey fur texture"
        assert payload["art_style"] == "realistic"
        assert payload["negative_prompt"] == ""
        assert payload["enable_pbr"] is True
        assert payload["resolution"] == "1024"
        assert payload["ai_model"] == "meshy-4"
        assert payload["callback_url"] == "http://example.com/webhook"
        
        mock_repository.record_task_submission.assert_called_once()
        recorded_submission = mock_repository.record_task_submission.call_args[0][0]
        assert isinstance(recorded_submission, TaskSubmission)
        assert recorded_submission.task_id == "retex_task_123"
        assert recorded_submission.species == "otter"
        assert recorded_submission.service == "retexture"
        assert recorded_submission.status == TaskStatus.PENDING
        assert recorded_submission.spec_hash == "hash456"
        
        assert submission.task_id == "retex_task_123"
        assert submission.species == "otter"
        assert submission.service == "retexture"
        assert submission.status == TaskStatus.PENDING
    
    def test_submit_task_with_optional_params(self, service, mock_client, mock_repository):
        """Test submit_task with all optional parameters"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"result": "retex_task_789"}
        mock_client.request.return_value = mock_response
        
        submission = service.submit_task(
            species="otter",
            model_id="model_999",
            prompt="metallic surface",
            callback_url="http://test.com/cb",
            art_style="cartoon",
            negative_prompt="rusty, old",
            enable_pbr=False,
            resolution="2048",
            seed=54321
        )
        
        payload = mock_client.request.call_args[1]["json"]
        assert payload["art_style"] == "cartoon"
        assert payload["negative_prompt"] == "rusty, old"
        assert payload["enable_pbr"] is False
        assert payload["resolution"] == "2048"
        assert payload["seed"] == 54321
        
        assert submission.task_id == "retex_task_789"
        mock_repository.record_task_submission.assert_called_once()
    
    def test_submit_task_seed_optional(self, service, mock_client, mock_repository):
        """Test seed parameter is optional"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"result": "retex_no_seed"}
        mock_client.request.return_value = mock_response
        
        submission = service.submit_task(
            species="otter",
            model_id="model_123",
            prompt="test texture",
            callback_url="http://test.com/cb",
            seed=None
        )
        
        payload = mock_client.request.call_args[1]["json"]
        assert "seed" not in payload
        assert submission.task_id == "retex_no_seed"
        mock_repository.record_task_submission.assert_called_once()
    
    def test_submit_task_http_error_propagates(self, service, mock_client):
        """Test HTTP errors from client are propagated"""
        mock_client.request.side_effect = httpx.HTTPStatusError(
            "Bad Request",
            request=Mock(),
            response=Mock(status_code=400)
        )
        
        with pytest.raises(httpx.HTTPStatusError):
            service.submit_task(
                species="otter",
                model_id="invalid",
                prompt="test",
                callback_url="http://test.com/cb"
            )
