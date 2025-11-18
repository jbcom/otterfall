"""PostgreSQL database adapter - DEPRECATED
This adapter is no longer used. The project uses file-based persistence.
See: python/mesh_toolkit/src/mesh_toolkit/persistence/repository.py
"""

import os
import time
import psycopg
from typing import List, Dict, Any, Optional
from .base import BaseToolAdapter, ToolResult, ToolError


class DatabaseAdapter(BaseToolAdapter):
    """Production PostgreSQL adapter with connection pooling"""
    
    def __init__(self, connection_string: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.connection_string = connection_string or os.getenv("DATABASE_URL")
        if not self.connection_string:
            raise ToolError("Database connection string required (DATABASE_URL)")
        
        # Statement timeout in seconds
        self.statement_timeout = 30
        # Max rows to return
        self.max_rows = 1000
    
    def validate_input(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
        allow_mutation: bool = False,
        **kwargs
    ) -> None:
        """Validate SQL query"""
        if not sql or not sql.strip():
            raise ToolError("SQL query cannot be empty")
        
        # Check for dangerous operations if mutations not allowed
        if not allow_mutation:
            sql_upper = sql.upper().strip()
            dangerous_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER", "CREATE"]
            for keyword in dangerous_keywords:
                if sql_upper.startswith(keyword):
                    raise ToolError(
                        f"Mutation operation '{keyword}' not allowed. Set allow_mutation=True"
                    )
    
    def execute(
        self,
        sql: str,
        params: Optional[Dict[str, Any]] = None,
        allow_mutation: bool = False,
        **kwargs
    ) -> ToolResult:
        """
        Execute SQL query on PostgreSQL database
        
        Args:
            sql: SQL query to execute
            params: Query parameters for safe parameterization
            allow_mutation: Allow INSERT/UPDATE/DELETE operations
        
        Returns:
            ToolResult with query results
        """
        start_time = time.time()
        
        try:
            self.validate_input(sql=sql, params=params, allow_mutation=allow_mutation)
            
            self.logger.info(f"Executing SQL: {sql[:100]}...")
            
            with psycopg.connect(self.connection_string) as conn:
                # Set statement timeout
                conn.execute(f"SET statement_timeout TO '{self.statement_timeout}s'")
                
                # Execute query
                cursor = conn.execute(sql, params or {})
                
                # Get results
                if cursor.description:
                    # SELECT query - fetch results
                    rows = cursor.fetchmany(self.max_rows)
                    columns = [desc[0] for desc in cursor.description]
                    
                    data = {
                        "columns": columns,
                        "rows": [dict(zip(columns, row)) for row in rows],
                        "row_count": len(rows),
                        "truncated": len(rows) == self.max_rows
                    }
                    
                    message = f"Query returned {len(rows)} rows"
                    if data["truncated"]:
                        message += f" (truncated at {self.max_rows})"
                else:
                    # Mutation query - get affected rows
                    affected = cursor.rowcount
                    data = {
                        "affected_rows": affected
                    }
                    message = f"Query affected {affected} rows"
                
                conn.commit()
                
                execution_time = (time.time() - start_time) * 1000
                
                return self._create_result(
                    success=True,
                    data=data,
                    message=message,
                    execution_time_ms=execution_time
                )
        
        except psycopg.OperationalError as e:
            raise ToolError(f"Database connection error: {e}")
        except psycopg.ProgrammingError as e:
            raise ToolError(f"SQL syntax error: {e}")
        except psycopg.QueryCanceled as e:
            raise ToolError(f"Query timeout (>{self.statement_timeout}s): {e}")
        except Exception as e:
            raise ToolError(f"Database query failed: {e}")
