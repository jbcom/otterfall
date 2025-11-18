"""Configuration validation using Pydantic schemas"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional
from pathlib import Path
import yaml
import json


class AgentConfig(BaseModel):
    """Agent configuration schema"""
    role: str = Field(..., min_length=1)
    goal: str = Field(..., min_length=1)
    backstory: str = Field(..., min_length=1)
    verbose: bool = True
    allow_delegation: bool = False
    allow_code_execution: bool = True
    memory: bool = True
    reasoning: bool = True
    max_reasoning_attempts: int = Field(default=3, ge=1, le=10)
    max_iter: int = Field(default=25, ge=1, le=100)


class TaskConfig(BaseModel):
    """Task configuration schema"""
    description: str = Field(..., min_length=1)
    expected_output: str = Field(..., min_length=1)
    required_tools: Optional[List[str]] = None
    agent: Optional[str] = None


class MCPServerConfig(BaseModel):
    """MCP server configuration schema"""
    command: str = Field(..., min_length=1)
    args: List[str] = Field(default_factory=list)
    env: Optional[Dict[str, str]] = None


class CrewConfig(BaseModel):
    """Complete crew configuration with all agents, tasks, and servers"""
    agents: Dict[str, AgentConfig]
    tasks: Dict[str, TaskConfig]
    mcp_servers: Dict[str, MCPServerConfig]
    
    @field_validator('agents')
    @classmethod
    def validate_agents(cls, v: Dict[str, AgentConfig]) -> Dict[str, AgentConfig]:
        """Ensure at least one agent is configured"""
        if not v:
            raise ValueError("At least one agent must be configured")
        return v
    
    @field_validator('tasks')
    @classmethod
    def validate_tasks(cls, v: Dict[str, TaskConfig]) -> Dict[str, TaskConfig]:
        """Ensure at least one task is configured"""
        if not v:
            raise ValueError("At least one task must be configured")
        return v


def load_crew_config(config_dir: Path = Path("crew_config")) -> CrewConfig:
    """
    Load and validate complete crew configuration
    
    Args:
        config_dir: Directory containing config files
    
    Returns:
        Validated CrewConfig instance
    
    Raises:
        FileNotFoundError: If config files are missing
        ValueError: If validation fails
    """
    agents_path = config_dir / "agents.yaml"
    tasks_path = config_dir / "tasks.yaml"
    mcp_path = config_dir / "mcp_servers.json"
    
    # Check all files exist
    for path in [agents_path, tasks_path, mcp_path]:
        if not path.exists():
            raise FileNotFoundError(f"Required config file not found: {path}")
    
    # Load YAML files
    with open(agents_path, 'r') as f:
        agents_data = yaml.safe_load(f)
    
    with open(tasks_path, 'r') as f:
        tasks_data = yaml.safe_load(f)
    
    # Load JSON file
    with open(mcp_path, 'r') as f:
        mcp_data = json.load(f)
    
    # Convert to Pydantic models for validation
    agents = {name: AgentConfig(**config) for name, config in agents_data.items()}
    tasks = {name: TaskConfig(**config) for name, config in tasks_data.items()}
    mcp_servers = {name: MCPServerConfig(**config) for name, config in mcp_data['mcpServers'].items()}
    
    return CrewConfig(
        agents=agents,
        tasks=tasks,
        mcp_servers=mcp_servers
    )
