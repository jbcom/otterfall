"""Filesystem adapter with sandboxing"""

import time
from pathlib import Path
from typing import Optional
from .base import BaseToolAdapter, ToolResult, ToolError


class FilesystemAdapter(BaseToolAdapter):
    """Production filesystem adapter with path sandboxing"""
    
    def __init__(self, sandbox_root: Path = Path("."), **kwargs):
        super().__init__(**kwargs)
        self.sandbox_root = sandbox_root.resolve()
    
    def _validate_path(self, filepath: str) -> Path:
        """Validate path is within sandbox and doesn't escape"""
        path = Path(filepath)
        
        # Reject absolute paths
        if path.is_absolute():
            raise ToolError(f"Absolute paths not allowed: {filepath}")
        
        # Resolve relative to sandbox
        full_path = (self.sandbox_root / path).resolve()
        
        # Ensure it's within sandbox
        try:
            full_path.relative_to(self.sandbox_root)
        except ValueError:
            raise ToolError(f"Path escapes sandbox: {filepath}")
        
        return full_path
    
    def validate_input(self, filepath: str, action: str, **kwargs) -> None:
        """Validate filesystem operation"""
        allowed_actions = ["read", "write", "exists", "list"]
        if action not in allowed_actions:
            raise ToolError(f"Action '{action}' not allowed. Allowed: {allowed_actions}")
        
        if not filepath or not filepath.strip():
            raise ToolError("filepath cannot be empty")
        
        # Validate path
        self._validate_path(filepath)
    
    def execute(
        self,
        action: str,
        filepath: str,
        content: Optional[str] = None,
        binary: bool = False,
        create_parents: bool = False,
        **kwargs
    ) -> ToolResult:
        """
        Execute filesystem operation
        
        Args:
            action: Operation to perform (read, write, exists, list)
            filepath: Path to file (relative to sandbox)
            content: Content to write (for write action)
            binary: Read/write in binary mode
            create_parents: Create parent directories if they don't exist
        
        Returns:
            ToolResult with operation result
        """
        start_time = time.time()
        
        try:
            self.validate_input(filepath=filepath, action=action)
            full_path = self._validate_path(filepath)
            
            if action == "read":
                if not full_path.exists():
                    return self._create_result(
                        success=False,
                        data=None,
                        message=f"File not found: {filepath}",
                        execution_time_ms=(time.time() - start_time) * 1000
                    )
                
                if binary:
                    data = full_path.read_bytes()
                    message = f"Read {len(data)} bytes from {filepath}"
                else:
                    try:
                        data = full_path.read_text(encoding='utf-8')
                        message = f"Read {len(data)} characters from {filepath}"
                    except UnicodeDecodeError:
                        return self._create_result(
                            success=False,
                            data=None,
                            message=f"File encoding error (not UTF-8): {filepath}",
                            execution_time_ms=(time.time() - start_time) * 1000
                        )
                
                return self._create_result(
                    success=True,
                    data=data,
                    message=message,
                    execution_time_ms=(time.time() - start_time) * 1000
                )
            
            elif action == "write":
                if content is None:
                    raise ToolError("content parameter required for write action")
                
                # Create parent directories if requested
                if create_parents:
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Atomic write using temporary file
                temp_path = full_path.with_suffix(full_path.suffix + '.tmp')
                
                try:
                    if binary:
                        temp_path.write_bytes(content)
                    else:
                        temp_path.write_text(content, encoding='utf-8')
                    
                    # Atomic replace
                    temp_path.replace(full_path)
                    
                    message = f"Wrote to {filepath}"
                    data = {"path": str(filepath), "size": full_path.stat().st_size}
                    
                    return self._create_result(
                        success=True,
                        data=data,
                        message=message,
                        execution_time_ms=(time.time() - start_time) * 1000
                    )
                finally:
                    # Clean up temp file if it still exists
                    if temp_path.exists():
                        temp_path.unlink()
            
            elif action == "exists":
                exists = full_path.exists()
                data = {
                    "exists": exists,
                    "is_file": full_path.is_file() if exists else False,
                    "is_dir": full_path.is_dir() if exists else False
                }
                
                return self._create_result(
                    success=True,
                    data=data,
                    message=f"Path {'exists' if exists else 'does not exist'}: {filepath}",
                    execution_time_ms=(time.time() - start_time) * 1000
                )
            
            elif action == "list":
                if not full_path.exists():
                    return self._create_result(
                        success=False,
                        data=None,
                        message=f"Directory not found: {filepath}",
                        execution_time_ms=(time.time() - start_time) * 1000
                    )
                
                if not full_path.is_dir():
                    return self._create_result(
                        success=False,
                        data=None,
                        message=f"Not a directory: {filepath}",
                        execution_time_ms=(time.time() - start_time) * 1000
                    )
                
                entries = []
                for entry in full_path.iterdir():
                    entries.append({
                        "name": entry.name,
                        "is_file": entry.is_file(),
                        "is_dir": entry.is_dir()
                    })
                
                return self._create_result(
                    success=True,
                    data={"entries": entries, "count": len(entries)},
                    message=f"Listed {len(entries)} entries in {filepath}",
                    execution_time_ms=(time.time() - start_time) * 1000
                )
            
            else:
                raise ToolError(f"Action '{action}' not implemented")
        
        except PermissionError as e:
            raise ToolError(f"Permission denied: {e}")
        except OSError as e:
            raise ToolError(f"Filesystem error: {e}")
        except Exception as e:
            raise ToolError(f"Filesystem operation failed: {e}")
