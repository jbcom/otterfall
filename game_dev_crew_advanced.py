#!/usr/bin/env python3
"""
Rivermarsh Game Development Crew - ADVANCED
Hierarchical AI team with full MCP integration
- Multiple MCP servers (Playwright, Context7, Vite-React, Context-portal)
- OpenRouter support with fallback
- Specialized tool distribution per agent
- Manager-led coordination
"""

import os
import json
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import yaml
from typing import Any


def load_yaml(filepath):
    """Load YAML configuration file"""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def load_mcp_config(filepath='crew_config/mcp_servers.json'):
    """Load MCP server configuration"""
    with open(filepath, 'r') as f:
        config = json.load(f)
    return config['mcpServers']


def create_mcp_server_params():
    """
    Create MCP server parameters for all external servers
    Returns list of StdioServerParameters for MCPServerAdapter
    """
    mcp_config = load_mcp_config()
    server_params = []
    
    for server_name, config in mcp_config.items():
        # Substitute environment variables in env dict
        env = {}
        for key, value in config.get('env', {}).items():
            if value.startswith('${') and value.endswith('}'):
                env_var = value[2:-1]
                env[key] = os.getenv(env_var, '')
            else:
                env[key] = value
        
        # Merge with current environment
        full_env = {**os.environ, **env}
        
        server_params.append(
            StdioServerParameters(
                command=config['command'],
                args=config['args'],
                env=full_env
            )
        )
    
    return server_params


def create_llm(use_openrouter=False):
    """
    Create LLM with fallback support
    Priority: OpenRouter > Anthropic > OpenAI
    """
    if use_openrouter and os.getenv('OPENROUTER_API_KEY'):
        # OpenRouter with auto-routing
        return LLM(
            model="openrouter/auto",
            temperature=0.1,
            max_tokens=4096,
            api_key=os.getenv('OPENROUTER_API_KEY')
        )
    elif os.getenv('ANTHROPIC_API_KEY'):
        return LLM(
            model="claude-3-5-haiku-20241022",
            temperature=0.1,
            max_tokens=4096
        )
    elif os.getenv('OPENAI_API_KEY'):
        return LLM(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=4096
        )
    else:
        raise ValueError("No API keys found! Set OPENROUTER_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY")


def create_agent(name, config, llm, tools=None):
    """Create a CrewAI agent from configuration"""
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        llm=llm,
        tools=tools or [],
        verbose=True,
        allow_delegation=False
    )


def create_task(name, config, agents_map):
    """Create a CrewAI task from configuration"""
    agent = agents_map.get(config.get('agent'))
    
    return Task(
        description=config['description'],
        expected_output=config['expected_output'],
        agent=agent
    )


def main():
    """Run the advanced game development crew with MCP integration"""
    print("=" * 80)
    print("🎮 RIVERMARSH GAME DEVELOPMENT CREW - ADVANCED")
    print("=" * 80)
    print("\nInitializing MCP servers and tools...")
    
    # Load configurations
    agents_config = load_yaml('crew_config/agents.yaml')
    tasks_config = load_yaml('crew_config/tasks.yaml')
    
    # Create LLM (will try OpenRouter first if available)
    use_openrouter = bool(os.getenv('OPENROUTER_API_KEY'))
    llm = create_llm(use_openrouter=use_openrouter)
    
    print(f"\n✓ LLM configured: {'OpenRouter' if use_openrouter else 'Anthropic Claude 3.5 Haiku'}")
    
    # Initialize MCP servers and get aggregated tools
    try:
        server_params_list = create_mcp_server_params()
        print(f"\n✓ MCP server configurations loaded: {len(server_params_list)} servers")
        
        # MCPServerAdapter accepts list of server params
        with MCPServerAdapter(server_params_list) as mcp_tools:  # type: ignore
            # Convert to list if needed
            tools_list = list(mcp_tools) if not isinstance(mcp_tools, list) else mcp_tools
            print(f"\n✓ MCP tools loaded: {len(tools_list)} tools available")
            print("\nAvailable MCP tools:")
            for i, tool in enumerate(tools_list):
                if i >= 10:
                    break
                desc = getattr(tool, 'description', 'No description')[:60]
                print(f"  - {getattr(tool, 'name', 'unnamed')}: {desc}...")
            if len(tools_list) > 10:
                print(f"  ... and {len(tools_list) - 10} more")
            
            # Create agents with specialized tool subsets
            agents_map = {}
            
            # Helper to filter tools by keywords
            def filter_tools(tools_list, keywords, limit=5):
                filtered = []
                for t in tools_list:
                    tool_name = getattr(t, 'name', '').lower()
                    if any(keyword in tool_name for keyword in keywords):
                        filtered.append(t)
                        if len(filtered) >= limit:
                            break
                return filtered
            
            # ECS Architect: Code analysis tools
            ecs_tools = filter_tools(tools_list, ['read', 'search', 'analyze', 'context'])
            agents_map['ecs_architect'] = create_agent(
                'ecs_architect', 
                agents_config['ecs_architect'], 
                llm,
                ecs_tools
            )
            
            # Yuka AI Engineer: Code editing + testing
            yuka_tools = filter_tools(tools_list, ['write', 'edit', 'test', 'run'])
            agents_map['yuka_ai_engineer'] = create_agent(
                'yuka_ai_engineer',
                agents_config['yuka_ai_engineer'],
                llm,
                yuka_tools
            )
            
            # Rendering Engineer: Browser tools + React + Material UI
            rendering_tools = filter_tools(tools_list, ['browser', 'playwright', 'vite', 'react', 'ui', 'mui', 'material'])
            agents_map['rendering_engineer'] = create_agent(
                'rendering_engineer',
                agents_config['rendering_engineer'],
                llm,
                rendering_tools
            )
            
            # Systems Engineer: All tools (first 10)
            max_tools = 10
            systems_tools = list(tools_list[0:max_tools]) if len(tools_list) > max_tools else tools_list
            agents_map['systems_engineer'] = create_agent(
                'systems_engineer',
                agents_config['systems_engineer'],
                llm,
                systems_tools
            )
            
            # QA Tester: Testing + validation tools
            qa_tools = filter_tools(tools_list, ['test', 'validate', 'check', 'lint', 'playwright'])
            agents_map['qa_tester'] = create_agent(
                'qa_tester',
                agents_config['qa_tester'],
                llm,
                qa_tools
            )
            
            # Chief Architect: Documentation + context tools (including conport)
            doc_tools = filter_tools(tools_list, ['doc', 'context', 'conport', 'portal', 'read', 'write'])
            agents_map['chief_architect'] = create_agent(
                'chief_architect',
                agents_config['chief_architect'],
                llm,
                doc_tools
            )
            
            # Create tasks
            tasks_map = {}
            for name, config in tasks_config.items():
                tasks_map[name] = create_task(name, config, agents_map)
            
            print(f"\n✓ Agents created: {len(agents_map)}")
            print(f"✓ Tasks configured: {len(tasks_map)}")
            
            # Assemble crew with hierarchical process
            print("\nAssembling hierarchical crew...")
            crew = Crew(
                agents=list(agents_map.values()),
                tasks=list(tasks_map.values()),
                process=Process.hierarchical,
                manager_llm=llm,  # Manager uses same LLM
                memory=False,
                verbose=True
            )
            
            print("\n" + "=" * 80)
            print("🚀 Starting hierarchical workflow with MCP-enhanced agents")
            print("=" * 80)
            print("\nManager: Coordinates all specialists")
            print("Specialists: Each with specialized MCP tool access")
            print("\nTasks:")
            for i, task_name in enumerate(tasks_config.keys(), 1):
                print(f"  {i}. {task_name}")
            print("\n" + "=" * 80 + "\n")
            
            # Run the crew
            result = crew.kickoff()
            
            print("\n" + "=" * 80)
            print("✅ CREW EXECUTION COMPLETED")
            print("=" * 80)
            print(f"\nFinal Result:\n{result}")
            
            # Save output
            with open('crew_output/final_result.txt', 'w') as f:
                f.write(str(result))
            
            print("\n✓ Output saved to crew_output/final_result.txt")
            
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure all MCP server packages are accessible via npx")
        print("2. Check that required environment variables are set")
        print("3. Verify network connectivity for remote MCP servers")
        raise


if __name__ == "__main__":
    main()
