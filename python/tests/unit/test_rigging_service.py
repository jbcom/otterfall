"""Unit tests for RiggingService"""
import pytest
from unittest.mock import Mock
import httpx
from mesh_toolkit.services.rigging_service import RiggingService
from mesh_toolkit.api.base_client import BaseHttpClient
from mesh_toolkit.persistence.repository import TaskRepository
from mesh_toolkit.persistence.schemas import TaskSubmission, TaskStatus


class TestRiggingService:
    """Test RiggingService webhook submission"""
    
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
        repo.compute_spec_hash.return_value = "spec_hash_456"
        return repo
    
    @pytest.fixture
    def service(self, mock_client, mock_repository):
        """Create RiggingService with mocked dependencies"""
        return RiggingService(mock_client, mock_repository)
    
    def test_submit_task_payload(self, service, mock_client, mock_repository):
        """Test submit_task builds correct payload"""
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = {"result": "rig_task_123"}
        mock_client.request.return_value = mock_response
        
        submission = service.submit_task(
            species="otter",
            model_id="model_456",
            callback_url="http://example.com/webhook"
        )
        
        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        
        assert call_args[0] == ("POST", "rigging")
        assert call_args[1]["api_version"] == "v1"
        
        payload = call_args[1]["json"]
        assert payload["model_id"] == "model_456"
        assert payload["callback_url"] == "http://example.com/webhook"
        
        mock_repository.record_task_submission.assert_called_once()
        recorded_submission = mock_repository.record_task_submission.call_args[0][0]
        assert isinstance(recorded_submission, TaskSubmission)
        assert recorded_submission.task_id == "rig_task_123"
        assert recorded_submission.species == "otter"
        assert recorded_submission.service == "rigging"
        assert recorded_submission.status == TaskStatus.PENDING
        assert recorded_submission.spec_hash == "spec_hash_456"
        
        assert submission.task_id == "rig_task_123"
        assert submission.species == "otter"
        assert submission.service == "rigging"
        assert submission.status == TaskStatus.PENDING
    
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
                model_id="invalid_model",
                callback_url="http://test.com/cb"
            )
