"""Unit tests for Text3DService"""
import pytest
from unittest.mock import Mock
import httpx
from mesh_toolkit.services.text3d_service import Text3DService
from mesh_toolkit.api.base_client import BaseHttpClient
from mesh_toolkit.persistence.repository import TaskRepository
from mesh_toolkit.persistence.schemas import TaskSubmission, TaskStatus


class TestText3DService:
    """Test Text3DService webhook submission"""
    
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
        repo.compute_spec_hash.return_value = "hash123"
        return repo
    
    @pytest.fixture
    def service(self, mock_client, mock_repository):
        """Create Text3DService with mocked dependencies"""
        return Text3DService(mock_client, mock_repository)
    
    def test_submit_task_basic_payload(self, service, mock_client, mock_repository):
        """Test submit_task builds correct payload with defaults"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"result": "task_123"}
        mock_client.request.return_value = mock_response
        
        submission = service.submit_task(
            species="otter",
            prompt="test otter",
            callback_url="http://example.com/webhook",
            art_style="sculpture"
        )
        
        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        
        assert call_args[0] == ("POST", "text-to-3d")
        assert call_args[1]["api_version"] == "v2"
        
        payload = call_args[1]["json"]
        assert payload["mode"] == "preview"
        assert payload["prompt"] == "test otter"
        assert payload["art_style"] == "sculpture"
        assert payload["model_version"] == "latest"
        assert payload["negative_prompt"] == ""
        assert payload["enable_pbr"] is True
        assert payload["ai_model"] == "meshy-4"
        assert payload["topology"] == "quad"
        assert payload["callback_url"] == "http://example.com/webhook"
        assert payload["should_remesh"] is True
        
        mock_repository.record_task_submission.assert_called_once()
        recorded_submission = mock_repository.record_task_submission.call_args[0][0]
        assert isinstance(recorded_submission, TaskSubmission)
        assert recorded_submission.task_id == "task_123"
        assert recorded_submission.species == "otter"
        assert recorded_submission.service == "text3d"
        assert recorded_submission.status == TaskStatus.PENDING
        assert recorded_submission.callback_url == "http://example.com/webhook"
        
        assert submission.task_id == "task_123"
        assert submission.species == "otter"
        assert submission.service == "text3d"
        assert submission.status == TaskStatus.PENDING
        assert submission.spec_hash == "hash123"
    
    def test_submit_task_with_optional_params(self, service, mock_client, mock_repository):
        """Test submit_task with all optional parameters"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"result": "task_456"}
        mock_client.request.return_value = mock_response
        
        submission = service.submit_task(
            species="otter",
            prompt="custom prompt",
            callback_url="http://test.com/cb",
            art_style="realistic",
            model_version="v3.5",
            negative_prompt="bad quality",
            enable_pbr=False,
            enable_retexture=False,
            seed=12345
        )
        
        payload = mock_client.request.call_args[1]["json"]
        assert payload["art_style"] == "realistic"
        assert payload["model_version"] == "v3.5"
        assert payload["negative_prompt"] == "bad quality"
        assert payload["enable_pbr"] is False
        assert payload["seed"] == 12345
        assert "should_remesh" not in payload
        
        assert submission.task_id == "task_456"
        mock_repository.record_task_submission.assert_called_once()
    
    def test_submit_task_seed_optional(self, service, mock_client, mock_repository):
        """Test seed parameter is optional"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"result": "task_789"}
        mock_client.request.return_value = mock_response
        
        submission = service.submit_task(
            species="otter",
            prompt="test",
            callback_url="http://test.com/cb",
            seed=None
        )
        
        payload = mock_client.request.call_args[1]["json"]
        assert "seed" not in payload
        assert submission.task_id == "task_789"
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
                prompt="invalid",
                callback_url="http://test.com/cb"
            )
    
    def test_refine_task(self, service, mock_client, mock_repository):
        """Test refine_task creates refinement submission"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"result": "refine_task_999"}
        mock_client.request.return_value = mock_response
        
        submission = service.refine_task(
            species="otter",
            task_id="preview_task_123",
            callback_url="http://test.com/refine_cb"
        )
        
        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        assert call_args[0] == ("POST", "text-to-3d/preview_task_123/refine")
        assert call_args[1]["api_version"] == "v2"
        assert call_args[1]["json"]["callback_url"] == "http://test.com/refine_cb"
        
        assert submission.task_id == "refine_task_999"
        assert submission.species == "otter"
        assert submission.service == "text3d_refine"
        assert submission.status == TaskStatus.PENDING
        assert submission.spec_hash == "hash123"
        
        mock_repository.record_task_submission.assert_called_once()
