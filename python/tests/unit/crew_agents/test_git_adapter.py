"""Unit tests for Git adapter"""

import pytest
from unittest.mock import Mock, patch
import subprocess
from crew_agents.adapters.git_adapter import GitAdapter
from crew_agents.adapters.base import ToolError


class TestGitAdapter:
    """Test Git adapter with mocked subprocess"""
    
    @pytest.fixture
    def adapter(self):
        """Create GitAdapter instance"""
        return GitAdapter()
    
    def test_validate_allowed_command(self, adapter):
        """Test validation allows safe commands"""
        adapter.validate_input(command="status")
        adapter.validate_input(command="log")
        adapter.validate_input(command="diff")
    
    def test_validate_rejects_dangerous_command(self, adapter):
        """Test validation rejects dangerous commands"""
        with pytest.raises(ToolError, match="not allowed"):
            adapter.validate_input(command="push")
        
        with pytest.raises(ToolError, match="not allowed"):
            adapter.validate_input(command="rm")
    
    @patch('subprocess.run')
    def test_execute_status_success(self, mock_run, adapter):
        """Test git status execution with success"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="M file.txt\nA new.txt\n",
            stderr=""
        )
        
        result = adapter.execute(command="status", args=["--short"])
        
        assert result.success is True
        assert "M file.txt" in result.data
        assert "completed successfully" in result.message
        
        # Verify subprocess was called correctly
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["git", "status", "--short"]
    
    @patch('subprocess.run')
    def test_execute_status_failure(self, mock_run, adapter):
        """Test git status execution with failure"""
        mock_run.return_value = Mock(
            returncode=128,
            stdout="",
            stderr="fatal: not a git repository"
        )
        
        result = adapter.execute(command="status")
        
        assert result.success is False
        assert "not a git repository" in result.data
        assert "failed" in result.message
    
    @patch('subprocess.run')
    def test_execute_timeout(self, mock_run, adapter):
        """Test git command timeout handling"""
        mock_run.side_effect = subprocess.TimeoutExpired("git", adapter.timeout)
        
        with pytest.raises(ToolError, match="timed out"):
            adapter.execute(command="status")
    
    @patch('subprocess.run')
    def test_execute_diff_with_file(self, mock_run, adapter):
        """Test git diff for specific file"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="diff --git a/test.py...",
            stderr=""
        )
        
        result = adapter.execute(command="diff", args=["test.py"])
        
        assert result.success is True
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert "test.py" in call_args[0][0]
