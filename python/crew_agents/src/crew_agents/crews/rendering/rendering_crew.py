"""
Rendering Crew - Builds visual systems.

This crew implements:
- React Three Fiber scenes
- GLSL shaders
- Post-processing effects
- Performance optimization for mobile
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crew_agents.config.llm import default_llm


@CrewBase
class RenderingCrew:
    """
    Rendering Crew for Rivermarsh.
    
    Creates beautiful, performant visuals that run at 60fps on mobile.
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def shader_engineer(self) -> Agent:
        """GLSL shader development."""
        return Agent(
            config=self.agents_config["shader_engineer"],
            llm=default_llm,
            verbose=True,
        )

    @agent
    def r3f_specialist(self) -> Agent:
        """React Three Fiber implementation."""
        return Agent(
            config=self.agents_config["r3f_specialist"],
            llm=default_llm,
            verbose=True,
        )

    @agent
    def performance_engineer(self) -> Agent:
        """Mobile optimization."""
        return Agent(
            config=self.agents_config["performance_engineer"],
            llm=default_llm,
            verbose=True,
        )

    @task
    def create_water_shader(self) -> Task:
        """Create water/marsh shader."""
        return Task(
            config=self.tasks_config["create_water_shader"],
        )

    @task
    def build_terrain_system(self) -> Task:
        """Build procedural terrain."""
        return Task(
            config=self.tasks_config["build_terrain_system"],
        )

    @task
    def optimize_rendering(self) -> Task:
        """Optimize for 60fps mobile."""
        return Task(
            config=self.tasks_config["optimize_rendering"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Rendering Crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
