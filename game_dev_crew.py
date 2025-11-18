#!/usr/bin/env python3
"""
Rivermarsh Game Development Crew
Hierarchical AI team for orchestrating game development tasks
"""

import os
from crewai import Agent, Crew, Process, Task
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import yaml


def load_yaml(filepath):
    """Load YAML configuration file"""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def create_agent(name, config, llm):
    """Create a CrewAI agent from configuration"""
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        llm=llm,
        verbose=True,
        allow_delegation=False  # Specialists don't delegate
    )


def create_task(name, config, agents_map):
    """Create a CrewAI task from configuration"""
    agent = agents_map[config['agent']]
    
    # Build context list from referenced tasks
    context_tasks = []
    if 'context' in config:
        for context_task_name in config['context']:
            if context_task_name in tasks_map:
                context_tasks.append(tasks_map[context_task_name])
    
    return Task(
        description=config['description'],
        expected_output=config['expected_output'],
        agent=agent,
        context=context_tasks if context_tasks else None
    )


# Load configurations
agents_config = load_yaml('crew_config/agents.yaml')
tasks_config = load_yaml('crew_config/tasks.yaml')

# Initialize LLMs
# Use Anthropic Claude for specialized agents (better at code)
claude = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=os.getenv('ANTHROPIC_API_KEY')
)

# Use OpenAI for manager (required by CrewAI hierarchical process)
gpt4 = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv('OPENAI_API_KEY')
)

# Create agents
agents_map = {
    name: create_agent(name, config, claude)
    for name, config in agents_config.items()
}

# Create tasks (need to build in order due to context dependencies)
tasks_map = {}
for name, config in tasks_config.items():
    tasks_map[name] = create_task(name, config, agents_map)

# Assemble crew with hierarchical process
crew = Crew(
    agents=list(agents_map.values()),
    tasks=list(tasks_map.values()),
    process=Process.hierarchical,
    manager_llm=gpt4,  # Manager coordinates the workflow
    memory=True,  # Enable cross-task memory
    verbose=True
)


def main():
    """Run the game development crew"""
    print("=" * 80)
    print("🎮 RIVERMARSH GAME DEVELOPMENT CREW")
    print("=" * 80)
    print("\nStarting hierarchical workflow...")
    print("Manager: GPT-4 (coordinates specialists)")
    print("Specialists: Claude Sonnet 3.5 (ECS, AI, Systems, QA, Architecture)")
    print("\nTasks:")
    for i, task_name in enumerate(tasks_config.keys(), 1):
        print(f"  {i}. {task_name}")
    print("\n" + "=" * 80 + "\n")
    
    # Kickoff the crew
    result = crew.kickoff()
    
    print("\n" + "=" * 80)
    print("✅ CREW EXECUTION COMPLETE")
    print("=" * 80)
    print("\nFinal Output:")
    print(result)
    
    # Save result to file
    with open('crew_output/final_report.md', 'w') as f:
        f.write("# Rivermarsh Game Development Crew - Final Report\n\n")
        f.write(str(result))
    
    print("\n📄 Report saved to: crew_output/final_report.md")


if __name__ == "__main__":
    main()
