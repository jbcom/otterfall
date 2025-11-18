"""Knowledge store adapter using SQLite"""

import sqlite3
import time
import json
from pathlib import Path
from typing import Any, Optional, Dict, List
from datetime import datetime
from .base import BaseToolAdapter, ToolResult, ToolError


class KnowledgeAdapter(BaseToolAdapter):
    """Production knowledge store using SQLite"""
    
    def __init__(self, db_path: Path = Path("data/knowledge.db"), **kwargs):
        super().__init__(**kwargs)
        self.db_path = db_path
        
        # Create database directory
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Create knowledge table if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    metadata TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_updated_at ON knowledge(updated_at)")
            conn.commit()
    
    def validate_input(
        self,
        action: str,
        key: Optional[str] = None,
        value: Optional[Any] = None,
        **kwargs
    ) -> None:
        """Validate knowledge store operation"""
        allowed_actions = ["store", "retrieve", "delete", "list", "search"]
        if action not in allowed_actions:
            raise ToolError(f"Action '{action}' not allowed. Allowed: {allowed_actions}")
        
        if action in ["store", "retrieve", "delete"]:
            if not key or not key.strip():
                raise ToolError(f"key required for {action} action")
            
            # Validate key size
            if len(key) > 256:
                raise ToolError("key too long (max 256 characters)")
        
        if action == "store":
            if value is None:
                raise ToolError("value required for store action")
            
            # Validate value size (1MB limit)
            value_str = json.dumps(value) if not isinstance(value, str) else value
            if len(value_str) > 1_000_000:
                raise ToolError("value too large (max 1MB)")
    
    def execute(
        self,
        action: str,
        key: Optional[str] = None,
        value: Optional[Any] = None,
        metadata: Optional[Dict] = None,
        **kwargs
    ) -> ToolResult:
        """
        Execute knowledge store operation
        
        Args:
            action: Operation to perform (store, retrieve, delete, list, search)
            key: Knowledge key
            value: Value to store
            metadata: Optional metadata dict
        
        Returns:
            ToolResult with operation result
        """
        start_time = time.time()
        
        try:
            self.validate_input(action=action, key=key, value=value)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                
                if action == "store":
                    # Serialize value
                    value_str = json.dumps(value) if not isinstance(value, str) else value
                    metadata_str = json.dumps(metadata) if metadata else None
                    now = datetime.utcnow().isoformat()
                    
                    # UPSERT
                    conn.execute("""
                        INSERT INTO knowledge (key, value, metadata, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?)
                        ON CONFLICT(key) DO UPDATE SET
                            value = excluded.value,
                            metadata = excluded.metadata,
                            updated_at = excluded.updated_at
                    """, (key, value_str, metadata_str, now, now))
                    
                    conn.commit()
                    
                    return self._create_result(
                        success=True,
                        data={"key": key, "size": len(value_str)},
                        message=f"Stored knowledge: {key}",
                        execution_time_ms=(time.time() - start_time) * 1000
                    )
                
                elif action == "retrieve":
                    cursor = conn.execute(
                        "SELECT * FROM knowledge WHERE key = ?",
                        (key,)
                    )
                    row = cursor.fetchone()
                    
                    if row:
                        # Try to parse value as JSON
                        try:
                            value = json.loads(row["value"])
                        except json.JSONDecodeError:
                            value = row["value"]
                        
                        # Try to parse metadata
                        metadata = None
                        if row["metadata"]:
                            try:
                                metadata = json.loads(row["metadata"])
                            except json.JSONDecodeError:
                                pass
                        
                        data = {
                            "key": row["key"],
                            "value": value,
                            "metadata": metadata,
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"]
                        }
                        
                        return self._create_result(
                            success=True,
                            data=data,
                            message=f"Retrieved knowledge: {key}",
                            execution_time_ms=(time.time() - start_time) * 1000
                        )
                    else:
                        return self._create_result(
                            success=False,
                            data=None,
                            message=f"Knowledge not found: {key}",
                            execution_time_ms=(time.time() - start_time) * 1000
                        )
                
                elif action == "delete":
                    cursor = conn.execute(
                        "DELETE FROM knowledge WHERE key = ?",
                        (key,)
                    )
                    conn.commit()
                    
                    if cursor.rowcount > 0:
                        return self._create_result(
                            success=True,
                            data={"deleted": True},
                            message=f"Deleted knowledge: {key}",
                            execution_time_ms=(time.time() - start_time) * 1000
                        )
                    else:
                        return self._create_result(
                            success=False,
                            data={"deleted": False},
                            message=f"Knowledge not found: {key}",
                            execution_time_ms=(time.time() - start_time) * 1000
                        )
                
                elif action == "list":
                    cursor = conn.execute(
                        "SELECT key, created_at, updated_at FROM knowledge ORDER BY updated_at DESC LIMIT 100"
                    )
                    rows = cursor.fetchall()
                    
                    data = {
                        "keys": [{
                            "key": row["key"],
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"]
                        } for row in rows],
                        "count": len(rows)
                    }
                    
                    return self._create_result(
                        success=True,
                        data=data,
                        message=f"Listed {len(rows)} knowledge entries",
                        execution_time_ms=(time.time() - start_time) * 1000
                    )
                
                elif action == "search":
                    search_term = kwargs.get("search_term", "")
                    if not search_term:
                        raise ToolError("search_term required for search action")
                    
                    cursor = conn.execute(
                        "SELECT key FROM knowledge WHERE key LIKE ? OR value LIKE ? LIMIT 50",
                        (f"%{search_term}%", f"%{search_term}%")
                    )
                    rows = cursor.fetchall()
                    
                    data = {
                        "matches": [row["key"] for row in rows],
                        "count": len(rows)
                    }
                    
                    return self._create_result(
                        success=True,
                        data=data,
                        message=f"Found {len(rows)} matches for '{search_term}'",
                        execution_time_ms=(time.time() - start_time) * 1000
                    )
                
                else:
                    raise ToolError(f"Action '{action}' not implemented")
        
        except sqlite3.Error as e:
            raise ToolError(f"Database error: {e}")
        except Exception as e:
            raise ToolError(f"Knowledge store operation failed: {e}")
