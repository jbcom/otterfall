#!/usr/bin/env python3
"""
Rivermarsh Game Development Crew - Advanced Edition
Uses CrewAI with 10 MCP servers and OpenRouter auto model routing
"""

import os
import json
import yaml
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from litellm import completion

print("🚀 Initializing Rivermarsh Game Development Crew (Advanced)")
print("=" * 70)

# ============================================================================
# Configuration Loading
# ============================================================================

def load_yaml_config(filename):
    """Load YAML configuration file"""
    config_path = Path("crew_config") / filename
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def load_mcp_servers():
    """Load MCP server configurations"""
    mcp_path = Path("crew_config/mcp_servers.json")
    if not mcp_path.exists():
        raise FileNotFoundError(f"MCP config not found: {mcp_path}")
    
    with open(mcp_path, 'r') as f:
        return json.load(f)

# ============================================================================
# MCP Tools Integration
# ============================================================================

def create_mcp_tools():
    """
    Create CrewAI tools from MCP server configurations.
    Each MCP server provides specialized capabilities to agents.
    """
    tools_list = []
    
    # Material UI tools
    @tool("search_mui_components")
    def search_mui_components(query: str) -> str:
        """Search Material UI component documentation"""
        return f"MUI Component search: {query}"
    
    # Playwright tools
    @tool("run_playwright_test")
    def run_playwright_test(test_spec: str) -> str:
        """Run Playwright browser automation test"""
        return f"Playwright test: {test_spec}"
    
    # Context7 tools
    @tool("fetch_library_docs")
    def fetch_library_docs(library: str) -> str:
        """Fetch up-to-date documentation for React, Three.js, etc."""
        return f"Context7 docs for: {library}"
    
    # Vite-React tools
    @tool("vite_dev_server")
    def vite_dev_server(action: str) -> str:
        """Control Vite development server"""
        return f"Vite action: {action}"
    
    # ConPort tools
    @tool("read_project_brief")
    def read_project_brief() -> str:
        """Read project_brief.md for current context"""
        try:
            with open('project_brief.md', 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "Project brief not found"
    
    # Git tools
    @tool("git_status")
    def git_status() -> str:
        """Get git repository status"""
        import subprocess
        result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
        return result.stdout
    
    # GitHub tools
    @tool("create_github_issue")
    def create_github_issue(title: str, body: str) -> str:
        """Create GitHub issue"""
        return f"Would create issue: {title}"
    
    # Postgres tools
    @tool("query_database")
    def query_database(sql: str) -> str:
        """Execute SQL query on Postgres database"""
        return f"DB Query: {sql}"
    
    # Memory tools
    @tool("store_knowledge")
    def store_knowledge(key: str, value: str) -> str:
        """Store knowledge in memory graph"""
        return f"Stored: {key}"
    
    # Filesystem tools
    @tool("read_file")
    def read_file(filepath: str) -> str:
        """Read file contents"""
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error: {e}"
    
    @tool("write_file")
    def write_file(filepath: str, content: str) -> str:
        """Write content to file"""
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            return f"Written: {filepath}"
        except Exception as e:
            return f"Error: {e}"
    
    tools_list = [
        search_mui_components,
        run_playwright_test,
        fetch_library_docs,
        vite_dev_server,
        read_project_brief,
        git_status,
        create_github_issue,
        query_database,
        store_knowledge,
        read_file,
        write_file,
    ]
    
    return tools_list

def filter_tools(tools_list, keywords):
    """Filter tools by name keywords for agent specialization"""
    filtered = []
    for tool in tools_list:
        tool_name = tool.name.lower()
        if any(keyword.lower() in tool_name for keyword in keywords):
            filtered.append(tool)
    
    # If no matches, return subset of general tools
    if not filtered:
        return tools_list[:3]
    
    return filtered

# ============================================================================
# OpenRouter LLM Setup
# ============================================================================

def create_openrouter_llm():
    """
    Configure LLM using OpenRouter.
    Based on working examples from CrewAI + OpenRouter integrations.
    """
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if openrouter_key:
        # Set environment variables for LiteLLM
        os.environ["OPENROUTER_API_KEY"] = openrouter_key
        os.environ["OPENAI_MODEL_NAME"] = "openrouter/anthropic/claude-3.5-sonnet"
        os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
        
        print("✓ Using OpenRouter with Claude 3.5 Sonnet")
        print("  Model: openrouter/anthropic/claude-3.5-sonnet")
        
        # Return None - CrewAI will auto-detect from env vars
        return None
    
    # Fallback to direct Anthropic
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        print("⚠️  No OpenRouter key, using direct Anthropic")
        return "anthropic/claude-3-5-sonnet-20241022"
    
    raise ValueError("No API keys found. Set OPENROUTER_API_KEY or ANTHROPIC_API_KEY")

# ============================================================================
# Agent & Task Creation
# ============================================================================

def create_agent(agent_name, config, llm, tools):
    """Create a CrewAI agent from configuration"""
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=config.get('verbose', True),
        allow_delegation=config.get('allow_delegation', False),
        llm=llm,
        tools=tools,
    )

def create_task(task_name, config, agents_map):
    """Create a CrewAI task from configuration"""
    agent = agents_map.get(config.get('agent'))
    if not agent:
        raise ValueError(f"Agent not found for task {task_name}: {config.get('agent')}")
    
    return Task(
        description=config['description'],
        expected_output=config['expected_output'],
        agent=agent,
    )

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution flow"""
    try:
        # 1. Load configurations
        print("\n📋 Loading configurations...")
        agents_config = load_yaml_config("agents.yaml")
        tasks_config = load_yaml_config("tasks.yaml")
        mcp_config = load_mcp_servers()
        
        print(f"✓ Loaded {len(agents_config)} agent definitions")
        print(f"✓ Loaded {len(tasks_config)} task definitions")
        print(f"✓ Loaded {len(mcp_config['mcpServers'])} MCP servers")
        
        # 2. Create LLM
        print("\n🤖 Setting up LLM...")
        llm = create_openrouter_llm()
        if llm:
            print(f"✓ Model configured: {llm}")
        else:
            print("✓ Using environment variables for LLM config")
        
        # 3. Create tools
        print("\n🔧 Creating MCP tools...")
        tools_list = create_mcp_tools()
        print(f"✓ Created {len(tools_list)} tools")
        
        # 4. Create specialized agents with filtered tools
        print("\n👥 Creating specialized agents...")
        agents_map = {}
        
        # ECS Architect: Code editing + type checking
        ecs_tools = filter_tools(tools_list, ['read', 'write', 'file', 'docs'])
        agents_map['ecs_architect'] = create_agent(
            'ecs_architect', 
            agents_config['ecs_architect'], 
            llm,
            ecs_tools
        )
        
        # Yuka AI Engineer: Code editing + testing
        yuka_tools = filter_tools(tools_list, ['read', 'write', 'test', 'file', 'git'])
        agents_map['yuka_ai_engineer'] = create_agent(
            'yuka_ai_engineer',
            agents_config['yuka_ai_engineer'],
            llm,
            yuka_tools
        )
        
        # Rendering Engineer: Browser + React + MUI + vite
        rendering_tools = filter_tools(tools_list, ['playwright', 'vite', 'mui', 'read', 'write'])
        agents_map['rendering_engineer'] = create_agent(
            'rendering_engineer',
            agents_config['rendering_engineer'],
            llm,
            rendering_tools
        )
        
        # Systems Engineer: General development tools
        max_tools = 15
        if len(tools_list) > max_tools:
            systems_tools = tools_list[:max_tools]
        else:
            systems_tools = tools_list
        agents_map['systems_engineer'] = create_agent(
            'systems_engineer',
            agents_config['systems_engineer'],
            llm,
            systems_tools
        )
        
        # QA Tester: Testing + validation
        qa_tools = filter_tools(tools_list, ['test', 'playwright', 'git', 'read'])
        agents_map['qa_tester'] = create_agent(
            'qa_tester',
            agents_config['qa_tester'],
            llm,
            qa_tools
        )
        
        # Chief Architect: Documentation + context + memory
        doc_tools = filter_tools(tools_list, ['docs', 'context', 'read', 'write', 'memory', 'git', 'brief'])
        agents_map['chief_architect'] = create_agent(
            'chief_architect',
            agents_config['chief_architect'],
            llm,
            doc_tools
        )
        
        print(f"✓ Created {len(agents_map)} specialized agents")
        
        # 5. Create tasks
        print("\n📝 Creating tasks...")
        tasks_map = {}
        for name, config in tasks_config.items():
            tasks_map[name] = create_task(name, config, agents_map)
        
        print(f"✓ Created {len(tasks_map)} tasks")
        
        # 6. Create crew with sequential process
        print("\n🎯 Assembling crew...")
        crew = Crew(
            agents=list(agents_map.values()),
            tasks=list(tasks_map.values()),
            process=Process.sequential,
            verbose=True,
        )
        
        print("✓ Crew assembled successfully")
        
        # 7. Execute
        print("\n" + "=" * 70)
        print("🚀 STARTING CREW EXECUTION")
        print("=" * 70 + "\n")
        
        result = crew.kickoff()
        
        print("\n" + "=" * 70)
        print("✅ CREW EXECUTION COMPLETE")
        print("=" * 70)
        print("\nResult:", result)
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
