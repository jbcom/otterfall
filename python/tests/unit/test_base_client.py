"""Unit tests for BaseHttpClient"""
import pytest
from unittest.mock import Mock, patch
import httpx
import tenacity
from mesh_toolkit.api.base_client import BaseHttpClient, RateLimitError


class TestBaseHttpClient:
    """Test BaseHttpClient retry and rate limit logic"""
    
    def test_initialization(self, mocker):
        """Test client initialization with API key"""
        mocker.patch.dict("os.environ", {"MESHY_API_KEY": "test_key"})
        client = BaseHttpClient()
        assert client.api_key == "test_key"
        assert client.timeout == 300.0
    
    def test_initialization_no_key_raises(self, mocker):
        """Test initialization fails without API key"""
        mocker.patch.dict("os.environ", {}, clear=True)
        with pytest.raises(ValueError, match="MESHY_API_KEY not set"):
            BaseHttpClient()
    
    def test_headers_include_auth(self, mocker):
        """Test headers include authorization token"""
        mocker.patch.dict("os.environ", {"MESHY_API_KEY": "test_key"})
        client = BaseHttpClient()
        headers = client._headers()
        assert headers["Authorization"] == "Bearer test_key"
        assert headers["Content-Type"] == "application/json"
    
    def test_successful_request(self, mocker):
        """Test successful HTTP request"""
        mocker.patch.dict("os.environ", {"MESHY_API_KEY": "test_key"})
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "task_id"}
        
        mock_client = mocker.patch.object(httpx.Client, "request", return_value=mock_response)
        
        client = BaseHttpClient()
        response = client.request("GET", "test-endpoint")
        
        assert response.status_code == 200
        assert response.json() == {"result": "task_id"}
    
    def test_rate_limit_with_retry_after(self, mocker):
        """Test 429 handling with Retry-After header"""
        mocker.patch.dict("os.environ", {"MESHY_API_KEY": "test_key"})
        mocker.patch("time.sleep")  # Mock sleep to speed up test
        
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 429
        mock_response.headers = {"retry-after": "2"}
        
        mocker.patch.object(httpx.Client, "request", return_value=mock_response)
        
        client = BaseHttpClient()
        
        with pytest.raises(tenacity.RetryError) as exc_info:
            client.request("GET", "test-endpoint")
        
        # Verify the original exception was RateLimitError
        assert isinstance(exc_info.value.last_attempt.exception(), RateLimitError)
        assert "Rate limit exceeded" in str(exc_info.value.last_attempt.exception())
    
    def test_server_error_retries(self, mocker):
        """Test 5xx errors trigger retries"""
        mocker.patch.dict("os.environ", {"MESHY_API_KEY": "test_key"})
        mocker.patch("time.sleep")
        
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 500
        
        mocker.patch.object(httpx.Client, "request", return_value=mock_response)
        
        client = BaseHttpClient()
        
        with pytest.raises(tenacity.RetryError) as exc_info:
            client.request("GET", "test-endpoint")
        
        # Verify the original exception was RateLimitError
        assert isinstance(exc_info.value.last_attempt.exception(), RateLimitError)
        assert "Server error 500" in str(exc_info.value.last_attempt.exception())
    
    def test_4xx_errors_no_retry(self, mocker):
        """Test 4xx errors fail immediately without retry"""
        mocker.patch.dict("os.environ", {"MESHY_API_KEY": "test_key"})
        
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request", request=Mock(), response=mock_response
        )
        
        mocker.patch.object(httpx.Client, "request", return_value=mock_response)
        
        client = BaseHttpClient()
        
        with pytest.raises(httpx.HTTPStatusError):
            client.request("GET", "test-endpoint")
