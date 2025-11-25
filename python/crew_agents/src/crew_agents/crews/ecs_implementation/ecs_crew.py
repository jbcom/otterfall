"""
ECS Implementation Crew - Builds the Entity Component System.

This crew implements:
- Miniplex component schemas
- System logic
- Type-safe data contracts
- ECS patterns from .ruler/ecs_patterns.md
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crew_agents.config.llm import default_llm


@CrewBase
class ECSImplementationCrew:
    """
    ECS Implementation Crew for Rivermarsh.
    
    Implements the Entity Component System using Miniplex
    with strict TypeScript typing.
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def ecs_architect(self) -> Agent:
        """Component schema design."""
        return Agent(
            config=self.agents_config["ecs_architect"],
            llm=default_llm,
            verbose=True,
        )

    @agent
    def typescript_engineer(self) -> Agent:
        """TypeScript implementation."""
        return Agent(
            config=self.agents_config["typescript_engineer"],
            llm=default_llm,
            verbose=True,
        )

    @agent
    def systems_engineer(self) -> Agent:
        """System logic implementation."""
        return Agent(
            config=self.agents_config["systems_engineer"],
            llm=default_llm,
            verbose=True,
        )

    @task
    def design_components(self) -> Task:
        """Design component schemas."""
        return Task(
            config=self.tasks_config["design_components"],
        )

    @task
    def implement_components(self) -> Task:
        """Implement TypeScript components."""
        return Task(
            config=self.tasks_config["implement_components"],
        )

    @task
    def implement_systems(self) -> Task:
        """Implement ECS systems."""
        return Task(
            config=self.tasks_config["implement_systems"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ECS Implementation Crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
