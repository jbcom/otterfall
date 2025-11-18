"""Vite dev server adapter"""

import subprocess
import time
import signal
import psutil
from pathlib import Path
from typing import Optional
from .base import BaseToolAdapter, ToolResult, ToolError


class ViteAdapter(BaseToolAdapter):
    """Production Vite dev server adapter with process management"""
    
    def __init__(self, project_root: Path = Path("."), **kwargs):
        super().__init__(**kwargs)
        self.project_root = project_root
        self.pid_file = project_root / ".vite_pid"
    
    def validate_input(self, action: str, **kwargs) -> None:
        """Validate Vite action"""
        allowed_actions = ["start", "stop", "status", "restart"]
        if action not in allowed_actions:
            raise ToolError(f"Action '{action}' not allowed. Allowed: {allowed_actions}")
    
    def _get_running_pid(self) -> Optional[int]:
        """Get PID of running Vite server if it exists"""
        if not self.pid_file.exists():
            return None
        
        try:
            pid = int(self.pid_file.read_text().strip())
            # Check if process is actually running
            if psutil.pid_exists(pid):
                proc = psutil.Process(pid)
                # Verify it's a node/vite process
                if "node" in proc.name().lower() or "vite" in ' '.join(proc.cmdline()).lower():
                    return pid
            # Stale PID file
            self.pid_file.unlink()
            return None
        except (ValueError, psutil.NoSuchProcess):
            return None
    
    def execute(self, action: str, **kwargs) -> ToolResult:
        """
        Execute Vite server action
        
        Args:
            action: One of 'start', 'stop', 'status', 'restart'
        
        Returns:
            ToolResult with action status
        """
        start_time = time.time()
        
        try:
            self.validate_input(action=action)
            
            if action == "status":
                pid = self._get_running_pid()
                execution_time = (time.time() - start_time) * 1000
                
                if pid:
                    proc = psutil.Process(pid)
                    return self._create_result(
                        success=True,
                        data={"running": True, "pid": pid, "status": proc.status()},
                        message=f"Vite server running (PID: {pid})",
                        execution_time_ms=execution_time
                    )
                else:
                    return self._create_result(
                        success=True,
                        data={"running": False},
                        message="Vite server not running",
                        execution_time_ms=execution_time
                    )
            
            elif action == "start":
                existing_pid = self._get_running_pid()
                if existing_pid:
                    return self._create_result(
                        success=False,
                        data={"pid": existing_pid},
                        message=f"Vite server already running (PID: {existing_pid})",
                        execution_time_ms=(time.time() - start_time) * 1000
                    )
                
                self.logger.info("Starting Vite dev server...")
                
                # Start vite in background
                process = subprocess.Popen(
                    ["npm", "run", "dev"],
                    cwd=self.project_root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True  # Detach from current session
                )
                
                # Save PID
                self.pid_file.write_text(str(process.pid))
                
                # Give it a moment to start
                time.sleep(2)
                
                execution_time = (time.time() - start_time) * 1000
                
                if psutil.pid_exists(process.pid):
                    return self._create_result(
                        success=True,
                        data={"pid": process.pid},
                        message=f"Vite server started (PID: {process.pid})",
                        execution_time_ms=execution_time
                    )
                else:
                    return self._create_result(
                        success=False,
                        data=None,
                        message="Vite server failed to start",
                        execution_time_ms=execution_time
                    )
            
            elif action == "stop":
                pid = self._get_running_pid()
                if not pid:
                    return self._create_result(
                        success=True,
                        data=None,
                        message="Vite server not running",
                        execution_time_ms=(time.time() - start_time) * 1000
                    )
                
                self.logger.info(f"Stopping Vite server (PID: {pid})...")
                
                try:
                    proc = psutil.Process(pid)
                    proc.terminate()  # SIGTERM
                    
                    # Wait up to 5 seconds for graceful shutdown
                    try:
                        proc.wait(timeout=5)
                    except psutil.TimeoutExpired:
                        # Force kill
                        proc.kill()  # SIGKILL
                        proc.wait()
                    
                    # Remove PID file
                    if self.pid_file.exists():
                        self.pid_file.unlink()
                    
                    execution_time = (time.time() - start_time) * 1000
                    
                    return self._create_result(
                        success=True,
                        data=None,
                        message=f"Vite server stopped (PID: {pid})",
                        execution_time_ms=execution_time
                    )
                
                except psutil.NoSuchProcess:
                    return self._create_result(
                        success=True,
                        data=None,
                        message="Vite server already stopped",
                        execution_time_ms=(time.time() - start_time) * 1000
                    )
            
            elif action == "restart":
                # Stop then start
                stop_result = self.execute(action="stop")
                time.sleep(1)
                start_result = self.execute(action="start")
                
                return self._create_result(
                    success=start_result.success,
                    data=start_result.data,
                    message=f"Vite server restarted: {start_result.message}",
                    execution_time_ms=(time.time() - start_time) * 1000
                )
            
            else:
                raise ToolError(f"Action '{action}' not implemented")
        
        except Exception as e:
            raise ToolError(f"Vite operation failed: {e}")
