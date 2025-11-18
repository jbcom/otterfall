"""Base adapter interface for CrewAI tools with structured results and error handling"""

from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime
import logging


@dataclass
class ToolResult:
    """Structured result from tool execution"""
    success: bool
    data: Any
    message: str
    timestamp: datetime
    execution_time_ms: Optional[float] = None
    
    def to_string(self) -> str:
        """Convert result to string for CrewAI tool return"""
        if self.success:
            return f"✓ {self.message}\n{self.data}"
        else:
            return f"✗ {self.message}\nError: {self.data}"


class ToolError(Exception):
    """Base exception for tool execution errors"""
    pass


class BaseToolAdapter:
    """Base class for all tool adapters with common functionality"""
    
    def __init__(self, timeout: int = 30, logger: Optional[logging.Logger] = None):
        """
        Initialize adapter with common settings
        
        Args:
            timeout: Maximum execution time in seconds
            logger: Custom logger instance (creates default if None)
        """
        self.timeout = timeout
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    def validate_input(self, **kwargs) -> None:
        """
        Validate input parameters before execution
        
        Args:
            **kwargs: Parameters to validate
        
        Raises:
            ToolError: If validation fails
        """
        raise NotImplementedError("Subclasses must implement validate_input")
    
    def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with validated inputs
        
        Args:
            **kwargs: Tool-specific parameters
        
        Returns:
            ToolResult with success status and data
        
        Raises:
            ToolError: If execution fails
        """
        raise NotImplementedError("Subclasses must implement execute")
    
    def _create_result(
        self,
        success: bool,
        data: Any,
        message: str,
        execution_time_ms: Optional[float] = None
    ) -> ToolResult:
        """Helper to create standardized ToolResult"""
        return ToolResult(
            success=success,
            data=data,
            message=message,
            timestamp=datetime.utcnow(),
            execution_time_ms=execution_time_ms
        )
