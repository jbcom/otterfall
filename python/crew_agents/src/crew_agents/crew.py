
#!/usr/bin/env python
"""
Rivermarsh CrewAI Entry Point

This file is the standard CrewAI entry point that `crewai run` expects.
It loads configuration from crewbase.yaml and executes the crew.
"""

from crewai import Crew
from crewai.flow import Flow
import yaml
from pathlib import Path


def load_crewbase():
    """Load crewbase.yaml configuration."""
    crewbase_path = Path(__file__).parent.parent.parent / "crewbase.yaml"
    with open(crewbase_path) as f:
        return yaml.safe_load(f)


def kickoff(inputs: dict = None):
    """
    Main entry point for crewai run.
    
    Args:
        inputs: Optional dict with:
            - task: Specific task name to run
            - All other task inputs from crewbase.yaml
    """
    config = load_crewbase()
    
    # CrewAI will automatically load agents/tasks from crewbase.yaml
    # The MCP tools are declared in crewbase.yaml using mcp:// syntax
    crew = Crew.from_yaml(str(Path(__file__).parent.parent.parent / "crewbase.yaml"))
    
    # If specific task requested, filter to that task
    if inputs and "task" in inputs:
        task_name = inputs["task"]
        crew.tasks = [t for t in crew.tasks if t.name == task_name]
        if not crew.tasks:
            raise ValueError(f"Task '{task_name}' not found in crewbase.yaml")
    
    return crew.kickoff(inputs=inputs)


def train(n_iterations: int = 5, inputs: dict = None):
    """Train the crew using memory/learning features."""
    config = load_crewbase()
    crew = Crew.from_yaml(str(Path(__file__).parent.parent.parent / "crewbase.yaml"))
    
    crew.train(n_iterations=n_iterations, inputs=inputs)


if __name__ == "__main__":
    # For direct execution
    kickoff()
