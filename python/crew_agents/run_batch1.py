#!/usr/bin/env python3
"""
Rivermarsh Batch 1: ECS Schemas + DFU Analysis
Kick off parallel development of foundation systems
"""

import os
import sys
import yaml
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from crew_agents.config import AgentConfig, TaskConfig, MCPServerConfig
from crew_agents.__main__ import create_openrouter_llm, create_mcp_tools, filter_tools

print("=" * 70)
print("🚀 RIVERMARSH BATCH 1: FOUNDATION SYSTEMS")
print("=" * 70)
print("\nTasks:")
print("  1. ECS Component Schemas (TypeScript)")
print("  2. Daggerfall Unity Data Analysis (Python)")
print("\nExecution: Parallel via OpenRouter")
print("=" * 70 + "\n")

def load_batch1_config():
    """Load Batch 1 configuration"""
    # Get workspace root (2 levels up from this file)
    workspace_root = Path(__file__).parent.parent.parent
    config_dir = workspace_root / "crew_config"
    
    # Load agents
    with open(config_dir / "agents.yaml", 'r') as f:
        agents_data = yaml.safe_load(f)
    
    # Load Batch 1 tasks
    with open(config_dir / "tasks_batch1.yaml", 'r') as f:
        tasks_data = yaml.safe_load(f)
    
    agents = {name: AgentConfig(**config) for name, config in agents_data.items()}
    tasks = {name: TaskConfig(**config) for name, config in tasks_data.items()}
    
    return agents, tasks

def main():
    """Execute Batch 1"""
    try:
        # 1. Load configuration
        print("📋 Loading Batch 1 configuration...")
        agents_config, tasks_config = load_batch1_config()
        print(f"✓ Loaded {len(agents_config)} agents")
        print(f"✓ Loaded {len(tasks_config)} tasks\n")
        
        # 2. Setup LLM using OpenRouter via environment variables
        print("🤖 Setting up OpenRouter LLM...")
        llm = create_openrouter_llm()  # Sets env vars, returns None for auto-detect
        print("✓ OpenRouter configured\n")
        
        # 3. Create tools
        print("🔧 Creating MCP tools...")
        tools_list = create_mcp_tools()
        print(f"✓ Created {len(tools_list)} tools\n")
        
        # 4. Create agents
        print("👥 Creating specialized agents...")
        
        # ECS Architect
        ecs_tools = filter_tools(tools_list, ['read', 'write', 'file', 'docs', 'list'])
        ecs_agent = Agent(
            role=agents_config['ecs_architect'].role,
            goal=agents_config['ecs_architect'].goal,
            backstory=agents_config['ecs_architect'].backstory,
            verbose=agents_config['ecs_architect'].verbose,
            allow_delegation=agents_config['ecs_architect'].allow_delegation,
            llm=llm,
            tools=ecs_tools,
        )
        print(f"  ✓ ECS Architect ({len(ecs_tools)} tools)")
        
        # DFU Analyst
        dfu_tools = filter_tools(tools_list, ['read', 'write', 'file', 'docs', 'knowledge', 'list'])
        dfu_agent = Agent(
            role=agents_config['dfu_analyst'].role,
            goal=agents_config['dfu_analyst'].goal,
            backstory=agents_config['dfu_analyst'].backstory,
            verbose=agents_config['dfu_analyst'].verbose,
            allow_delegation=agents_config['dfu_analyst'].allow_delegation,
            llm=llm,
            tools=dfu_tools,
        )
        print(f"  ✓ DFU Analyst ({len(dfu_tools)} tools)")
        
        # Technical Director (Manager)
        manager_agent = Agent(
            role=agents_config['technical_director'].role,
            goal=agents_config['technical_director'].goal,
            backstory=agents_config['technical_director'].backstory,
            verbose=agents_config['technical_director'].verbose,
            allow_delegation=agents_config['technical_director'].allow_delegation,
            llm=llm,
            tools=tools_list,  # Manager gets all tools
        )
        print(f"  ✓ Technical Director (Manager, {len(tools_list)} tools)\n")
        
        # 5. Create tasks
        print("📝 Creating tasks...")
        
        task_ecs = Task(
            description=tasks_config['ecs_component_schemas'].description,
            expected_output=tasks_config['ecs_component_schemas'].expected_output,
        )
        print("  ✓ ECS Component Schemas task")
        
        task_dfu = Task(
            description=tasks_config['dfu_data_analysis'].description,
            expected_output=tasks_config['dfu_data_analysis'].expected_output,
        )
        print("  ✓ DFU Data Analysis task\n")
        
        # 6. Assemble crew
        print("🎯 Assembling Batch 1 crew...")
        crew = Crew(
            agents=[ecs_agent, dfu_agent],
            tasks=[task_ecs, task_dfu],
            manager_agent=manager_agent,
            process=Process.hierarchical,
            planning=True,
            verbose=True,
        )
        print("✓ Crew assembled (2 workers + 1 manager)\n")
        
        # 7. Execute
        print("=" * 70)
        print("🚀 STARTING BATCH 1 EXECUTION")
        print("=" * 70 + "\n")
        
        result = crew.kickoff()
        
        print("\n" + "=" * 70)
        print("✅ BATCH 1 COMPLETE")
        print("=" * 70)
        print("\nResult:", result)
        
        print("\n📦 Deliverables:")
        print("  - shared/backend/ecs_world/")
        print("  - shared/backend/dfu_analysis/")
        print("\nNext: Agent reviews and integrates into frontend prototypes")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
