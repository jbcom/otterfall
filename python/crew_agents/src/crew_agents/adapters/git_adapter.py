"""Git adapter for repository operations"""

import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any
from .base import BaseToolAdapter, ToolResult, ToolError


class GitAdapter(BaseToolAdapter):
    """Production git adapter with subprocess execution"""
    
    def __init__(self, repo_path: Path = Path("."), **kwargs):
        super().__init__(**kwargs)
        self.repo_path = repo_path
    
    def validate_input(self, command: str = "status", **kwargs) -> None:
        """Validate git command is allowed"""
        allowed_commands = ["status", "log", "diff", "show", "branch", "remote"]
        if command not in allowed_commands:
            raise ToolError(f"Git command '{command}' not allowed. Allowed: {allowed_commands}")
    
    def execute(self, command: str = "status", args: List[str] = None, **kwargs) -> ToolResult:
        """
        Execute git command
        
        Args:
            command: Git subcommand (status, log, diff, etc.)
            args: Additional arguments for the command
        
        Returns:
            ToolResult with git command output
        """
        start_time = time.time()
        
        try:
            self.validate_input(command=command)
            
            cmd_list = ["git", command]
            if args:
                cmd_list.extend(args)
            
            self.logger.info(f"Executing: {' '.join(cmd_list)}")
            
            result = subprocess.run(
                cmd_list,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={"GIT_TERMINAL_PROMPT": "0"}  # Prevent interactive prompts
            )
            
            execution_time = (time.time() - start_time) * 1000
            
            if result.returncode == 0:
                return self._create_result(
                    success=True,
                    data=result.stdout.strip(),
                    message=f"Git {command} completed successfully",
                    execution_time_ms=execution_time
                )
            else:
                return self._create_result(
                    success=False,
                    data=result.stderr.strip(),
                    message=f"Git {command} failed with exit code {result.returncode}",
                    execution_time_ms=execution_time
                )
        
        except subprocess.TimeoutExpired:
            raise ToolError(f"Git command timed out after {self.timeout}s")
        except Exception as e:
            raise ToolError(f"Git command failed: {e}")
