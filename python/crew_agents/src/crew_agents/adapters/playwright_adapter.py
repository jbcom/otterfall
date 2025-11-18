"""Playwright test adapter"""

import subprocess
import time
from pathlib import Path
from typing import Optional, List
from .base import BaseToolAdapter, ToolResult, ToolError


class PlaywrightAdapter(BaseToolAdapter):
    """Production Playwright adapter for browser testing"""
    
    def __init__(self, project_root: Path = Path("."), **kwargs):
        super().__init__(**kwargs)
        self.project_root = project_root
    
    def validate_input(
        self,
        test_spec: Optional[str] = None,
        action: str = "test",
        **kwargs
    ) -> None:
        """Validate Playwright action and test spec"""
        allowed_actions = ["test", "show-report", "codegen"]
        if action not in allowed_actions:
            raise ToolError(f"Action '{action}' not allowed. Allowed: {allowed_actions}")
        
        if action == "test" and test_spec:
            # Validate test spec path is safe
            spec_path = Path(test_spec)
            if spec_path.is_absolute() or ".." in str(spec_path):
                raise ToolError("test_spec must be relative path without '..'")
    
    def execute(
        self,
        action: str = "test",
        test_spec: Optional[str] = None,
        headed: bool = False,
        browser: Optional[str] = None,
        **kwargs
    ) -> ToolResult:
        """
        Execute Playwright command
        
        Args:
            action: Playwright action (test, show-report, codegen)
            test_spec: Test file or pattern to run
            headed: Run in headed mode
            browser: Browser to use (chromium, firefox, webkit)
        
        Returns:
            ToolResult with test results
        """
        start_time = time.time()
        
        try:
            self.validate_input(action=action, test_spec=test_spec)
            
            cmd = ["npx", "playwright", action]
            
            if action == "test":
                if test_spec:
                    cmd.append(test_spec)
                
                if headed:
                    cmd.append("--headed")
                
                if browser:
                    if browser not in ["chromium", "firefox", "webkit"]:
                        raise ToolError(f"Invalid browser: {browser}")
                    cmd.extend(["--browser", browser])
            
            self.logger.info(f"Executing: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            execution_time = (time.time() - start_time) * 1000
            
            # Parse test output for summary
            output = result.stdout + result.stderr
            success = result.returncode == 0
            
            # Extract test summary if available
            summary = self._parse_test_summary(output)
            
            return self._create_result(
                success=success,
                data={
                    "exit_code": result.returncode,
                    "output": output,
                    "summary": summary
                },
                message=f"Playwright {action} {'passed' if success else 'failed'}",
                execution_time_ms=execution_time
            )
        
        except subprocess.TimeoutExpired:
            raise ToolError(f"Playwright command timed out after {self.timeout}s")
        except Exception as e:
            raise ToolError(f"Playwright execution failed: {e}")
    
    def _parse_test_summary(self, output: str) -> dict:
        """Extract test summary from Playwright output"""
        summary = {
            "passed": 0,
            "failed": 0,
            "skipped": 0
        }
        
        # Simple parsing (Playwright output format may vary)
        lines = output.split('\n')
        for line in lines:
            if "passed" in line.lower():
                try:
                    summary["passed"] = int(''.join(filter(str.isdigit, line.split("passed")[0])))
                except:
                    pass
            if "failed" in line.lower():
                try:
                    summary["failed"] = int(''.join(filter(str.isdigit, line.split("failed")[0])))
                except:
                    pass
        
        return summary
