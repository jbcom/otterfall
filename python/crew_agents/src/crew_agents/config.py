
"""Pydantic configuration schemas for CrewAI agents and tasks"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, field_validator


class AgentConfig(BaseModel):
    """Agent configuration schema"""
    role: str
    goal: str
    backstory: str
    verbose: bool = True
    allow_delegation: bool = False
    max_iter: int = 25
    max_reasoning_attempts: Optional[int] = None
    
    @field_validator('role', 'goal', 'backstory')
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class TaskConfig(BaseModel):
    """Task configuration schema"""
    description: str
    expected_output: str
    agent: str  # Agent name reference
    
    @field_validator('description', 'expected_output')
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class MCPServerConfig(BaseModel):
    """MCP server configuration schema"""
    command: str
    args: List[str]
    env: Optional[Dict[str, str]] = None
    
    @field_validator('command')
    @classmethod
    def validate_command(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Command cannot be empty")
        return v.strip()


class CrewConfig(BaseModel):
    """Complete crew configuration"""
    agents: Dict[str, AgentConfig]
    tasks: Dict[str, TaskConfig]
    mcp_servers: Dict[str, MCPServerConfig]
    
    @field_validator('agents')
    @classmethod
    def validate_agents(cls, v: Dict[str, AgentConfig]) -> Dict[str, AgentConfig]:
        if not v:
            raise ValueError("At least one agent must be configured")
        return v
    
    @field_validator('tasks')
    @classmethod
    def validate_tasks(cls, v: Dict[str, TaskConfig]) -> Dict[str, TaskConfig]:
        if not v:
            raise ValueError("At least one task must be configured")
        return v


def load_crew_config(
    agents_path: str = "crew_config/agents.yaml",
    tasks_path: str = "crew_config/tasks.yaml",
    mcp_path: str = "crew_config/mcp_servers.json"
) -> CrewConfig:
    """Load and validate complete crew configuration"""
    import yaml
    import json
    
    with open(agents_path) as f:
        agents_data = yaml.safe_load(f)
    
    with open(tasks_path) as f:
        tasks_data = yaml.safe_load(f)
    
    with open(mcp_path) as f:
        mcp_data = json.load(f)
    
    return CrewConfig(
        agents={k: AgentConfig(**v) for k, v in agents_data.items()},
        tasks={k: TaskConfig(**v) for k, v in tasks_data.items()},
        mcp_servers={k: MCPServerConfig(**v) for k, v in mcp_data['mcpServers'].items()}
    )
