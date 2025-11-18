
from pathlib import Path
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, DirectoryReadTool

@CrewBase
class RivermarshCrew:
    """Rivermarsh Game Development Crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        # MCP tools will be loaded from .mcp.json automatically by CrewAI
        self.file_read_tool = FileReadTool()
        self.directory_read_tool = DirectoryReadTool()
    
    @agent
    def project_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['project_manager'],
            tools=[self.file_read_tool, self.directory_read_tool],
            verbose=True
        )
    
    @agent
    def technical_director(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_director'],
            tools=[self.file_read_tool, self.directory_read_tool],
            verbose=True,
            allow_delegation=True
        )
    
    @agent
    def ecs_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['ecs_architect'],
            tools=[self.file_read_tool, self.directory_read_tool],
            verbose=True
        )
    
    @agent
    def yuka_ai_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['yuka_ai_engineer'],
            tools=[self.file_read_tool],
            verbose=True
        )
    
    @agent
    def rendering_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['rendering_engineer'],
            tools=[self.file_read_tool],
            verbose=True
        )
    
    @agent
    def technical_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_writer'],
            tools=[self.file_read_tool, self.directory_read_tool],
            verbose=True
        )
    
    @task
    def context_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['context_analysis'],
            agent=self.project_manager()
        )
    
    @task
    def ecs_data_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['ecs_data_design'],
            agent=self.ecs_architect()
        )
    
    @task
    def context_recording_task(self) -> Task:
        return Task(
            config=self.tasks_config['context_recording'],
            agent=self.technical_writer()
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Rivermarsh crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.technical_director(),
            verbose=True,
            memory=True
        )
