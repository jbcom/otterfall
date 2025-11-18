
"""ConPort MCP adapter for CrewAI agents"""

from typing import Dict, Any, Optional, List
from .base import BaseToolAdapter, ToolResult, ToolError
import subprocess
import json


class ConPortAdapter(BaseToolAdapter):
    """Adapter for Context Portal MCP server operations"""
    
    def __init__(self):
        super().__init__()
        self.mcp_command = ["uvx", "--from", "context-portal-mcp", "conport-mcp", "--mode", "stdio"]
    
    def _call_mcp(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call ConPort MCP server via stdio"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }
        
        try:
            result = subprocess.run(
                self.mcp_command,
                input=json.dumps(request),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise ToolError(f"MCP command failed: {result.stderr}")
            
            response = json.loads(result.stdout)
            
            if "error" in response:
                raise ToolError(f"MCP error: {response['error']}")
            
            return response.get("result", {})
            
        except subprocess.TimeoutExpired:
            raise ToolError("ConPort MCP timeout")
        except json.JSONDecodeError as e:
            raise ToolError(f"Invalid JSON response: {e}")
    
    def execute(self, action: str, **kwargs) -> ToolResult:
        """
        Execute ConPort action
        
        Actions:
        - get_schema: Get ConPort tool schema
        - get_product_context: Get overall project context
        - get_active_context: Get current working context
        - read_custom_data: Read custom data (category, key)
        - log_decision: Log architectural decision
        - log_progress: Log progress entry
        - update_progress: Update progress status
        - log_pattern: Log system pattern
        - link_items: Link ConPort items
        """
        try:
            if action == "get_schema":
                result = self._call_mcp("list_tools")
                return ToolResult(
                    success=True,
                    message="ConPort schema retrieved",
                    data=result
                )
            
            elif action == "get_product_context":
                result = self._call_mcp("get_product_context")
                return ToolResult(
                    success=True,
                    message="Product context retrieved",
                    data=result
                )
            
            elif action == "get_active_context":
                result = self._call_mcp("get_active_context")
                return ToolResult(
                    success=True,
                    message="Active context retrieved",
                    data=result
                )
            
            elif action == "read_custom_data":
                category = kwargs.get("category")
                key = kwargs.get("key")
                if not category or not key:
                    raise ToolError("category and key required")
                
                result = self._call_mcp("get_custom_data", {
                    "category": category,
                    "key": key
                })
                return ToolResult(
                    success=True,
                    message=f"Custom data retrieved: {category}/{key}",
                    data=result
                )
            
            elif action == "log_decision":
                summary = kwargs.get("summary")
                if not summary:
                    raise ToolError("summary required")
                
                result = self._call_mcp("log_decision", {
                    "summary": summary,
                    "rationale": kwargs.get("rationale"),
                    "implementation_details": kwargs.get("implementation_details"),
                    "tags": kwargs.get("tags", [])
                })
                return ToolResult(
                    success=True,
                    message="Decision logged",
                    data=result
                )
            
            elif action == "log_progress":
                status = kwargs.get("status")
                description = kwargs.get("description")
                if not status or not description:
                    raise ToolError("status and description required")
                
                result = self._call_mcp("log_progress", {
                    "status": status,
                    "description": description,
                    "tags": kwargs.get("tags", [])
                })
                return ToolResult(
                    success=True,
                    message="Progress logged",
                    data=result
                )
            
            else:
                raise ToolError(f"Unknown action: {action}")
                
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"ConPort operation failed: {e}")
