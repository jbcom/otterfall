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
from crewai.project import CrewBase, agent, task, crew
from crewai.tools import tool

# Import production adapters
from crew_agents.config import load_crew_config
from crew_agents.adapters import (
    GitAdapter,
    GitHubAdapter,
    ViteAdapter,
    PlaywrightAdapter,
    ConPortAdapter,
    FilesystemAdapter,
    KnowledgeAdapter,
    DocsAdapter,
)

print("🚀 Initializing Rivermarsh Game Development Crew (Production)")
print("=" * 70)

# ============================================================================
# Configuration Loading (using validated Pydantic schemas)
# ============================================================================

# ============================================================================
# MCP Tools Integration
# ============================================================================

def create_mcp_tools():
    """
    Create production CrewAI tools using real adapters + ConPort MCP.
    All tools have proper error handling, validation, and logging.
    Adapters are initialized lazily to avoid crashes on missing deps.
    """
    tools_list = []
    
    # Lazy adapter initialization - only create when tool is actually called
    # This prevents crashes if env vars/services aren't available
    _adapters = {}
    
    def _get_adapter(name: str, factory):
        """Lazy adapter initialization"""
        if name not in _adapters:
            try:
                _adapters[name] = factory()
            except Exception as e:
                return None, f"Adapter initialization failed: {e}"
        return _adapters[name], None
    
    # ConPort MCP Tools (Context Portal for RAG)
    @tool("conport_get_schema")
    def conport_get_schema() -> str:
        """Get ConPort schema showing all available tools and their parameters"""
        adapter, error = _get_adapter('conport', ConPortAdapter)
        if error:
            return error
        try:
            result = adapter.execute(action="get_schema")
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    @tool("conport_read_projectbrief")
    def conport_read_projectbrief() -> str:
        """Read projectbrief.md from ConPort custom data (category: 'ProjectBrief', key: 'content')"""
        adapter, error = _get_adapter('conport', ConPortAdapter)
        if error:
            return error
        try:
            result = adapter.execute(
                action="read_custom_data",
                category="ProjectBrief",
                key="content"
            )
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    @tool("conport_get_product_context")
    def conport_get_product_context() -> str:
        """Get overall project goals, features, and architecture from ConPort"""
        adapter, error = _get_adapter('conport', ConPortAdapter)
        if error:
            return error
        try:
            result = adapter.execute(action="get_product_context")
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    @tool("conport_get_active_context")
    def conport_get_active_context() -> str:
        """Get current working focus, recent changes, open issues from ConPort"""
        adapter, error = _get_adapter('conport', ConPortAdapter)
        if error:
            return error
        try:
            result = adapter.execute(action="get_active_context")
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    @tool("conport_log_decision")
    def conport_log_decision(summary: str, rationale: str = None, tags: str = None) -> str:
        """Log architectural or implementation decision to ConPort"""
        adapter, error = _get_adapter('conport', ConPortAdapter)
        if error:
            return error
        try:
            tag_list = [t.strip() for t in tags.split(",")] if tags else []
            result = adapter.execute(
                action="log_decision",
                summary=summary,
                rationale=rationale,
                tags=tag_list
            )
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    @tool("conport_update_progress")
    def conport_update_progress(status: str, description: str) -> str:
        """Update progress entry in ConPort"""
        adapter, error = _get_adapter('conport', ConPortAdapter)
        if error:
            return error
        try:
            result = adapter.execute(
                action="log_progress",
                status=status,
                description=description
            )
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    # Git tools (read-only operations)
    @tool("git_status")
    def git_status() -> str:
        """Get git repository status with changed files"""
        adapter, error = _get_adapter('git', GitAdapter)
        if error:
            return error
        try:
            result = adapter.execute(command="status", args=["--short"])
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    @tool("git_diff")
    def git_diff(filepath: str = None) -> str:
        """Get git diff, optionally for specific file"""
        adapter, error = _get_adapter('git', GitAdapter)
        if error:
            return error
        try:
            args = [filepath] if filepath else []
            result = adapter.execute(command="diff", args=args)
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    # GitHub tools (requires GITHUB_PERSONAL_ACCESS_TOKEN)
    @tool("create_github_issue")
    def create_github_issue(repo: str, title: str, body: str = None) -> str:
        """Create GitHub issue in format owner/repo (requires GitHub token)"""
        adapter, error = _get_adapter('github', GitHubAdapter)
        if error:
            return error
        try:
            result = adapter.execute(
                action="create_issue",
                repo=repo,
                title=title,
                body=body
            )
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    # Vite tools (requires npm/vite setup)
    @tool("vite_dev_server")
    def vite_dev_server(action: str) -> str:
        """Control Vite server: start, stop, status, restart (requires vite setup)"""
        adapter, error = _get_adapter('vite', ViteAdapter)
        if error:
            return error
        try:
            result = adapter.execute(action=action)
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    # Playwright tools (requires playwright installed)
    @tool("run_playwright_test")
    def run_playwright_test(test_spec: str = None) -> str:
        """Run Playwright tests, optionally for specific file/pattern (requires playwright)"""
        adapter, error = _get_adapter('playwright', PlaywrightAdapter)
        if error:
            return error
        try:
            result = adapter.execute(action="test", test_spec=test_spec)
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    # Filesystem tools (sandboxed to project directory)
    @tool("read_file")
    def read_file(filepath: str) -> str:
        """Read file contents (must be within project directory)"""
        adapter, error = _get_adapter('filesystem', FilesystemAdapter)
        if error:
            return error
        try:
            result = adapter.execute(action="read", filepath=filepath)
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    @tool("write_file")
    def write_file(filepath: str, content: str) -> str:
        """Write content to file (creates parent dirs if needed)"""
        adapter, error = _get_adapter('filesystem', FilesystemAdapter)
        if error:
            return error
        try:
            result = adapter.execute(
                action="write",
                filepath=filepath,
                content=content,
                create_parents=True
            )
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    @tool("list_directory")
    def list_directory(filepath: str = ".") -> str:
        """List files and directories"""
        adapter, error = _get_adapter('filesystem', FilesystemAdapter)
        if error:
            return error
        try:
            result = adapter.execute(action="list", filepath=filepath)
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    # Knowledge store tools (persistent SQLite)
    @tool("store_knowledge")
    def store_knowledge(key: str, value: str) -> str:
        """Store knowledge in persistent key-value store"""
        adapter, error = _get_adapter('knowledge', KnowledgeAdapter)
        if error:
            return error
        try:
            result = adapter.execute(action="store", key=key, value=value)
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    @tool("retrieve_knowledge")
    def retrieve_knowledge(key: str) -> str:
        """Retrieve knowledge from store"""
        adapter, error = _get_adapter('knowledge', KnowledgeAdapter)
        if error:
            return error
        try:
            result = adapter.execute(action="retrieve", key=key)
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    # Documentation tools
    @tool("fetch_library_docs")
    def fetch_library_docs(library: str, query: str = None) -> str:
        """Fetch documentation URL for library (react, threejs, r3f, etc.)"""
        adapter, error = _get_adapter('docs', DocsAdapter)
        if error:
            return error
        try:
            result = adapter.execute(library=library, query=query)
            return result.to_string()
        except Exception as e:
            return f"Error: {e}"
    
    tools_list = [
        git_status,
        git_diff,
        create_github_issue,
        vite_dev_server,
        run_playwright_test,
        read_file,
        write_file,
        list_directory,
        store_knowledge,
        retrieve_knowledge,
        fetch_library_docs,
        conport_get_schema,
        conport_read_projectbrief,
        conport_get_product_context,
        conport_get_active_context,
        conport_log_decision,
        conport_update_progress,
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
    """Create a CrewAI agent from Pydantic configuration"""
    return Agent(
        role=config.role,
        goal=config.goal,
        backstory=config.backstory,
        verbose=config.verbose,
        allow_delegation=config.allow_delegation,
        llm=llm,
        tools=tools,
    )

def create_task(task_name, config, agents_map):
    """Create a CrewAI task from Pydantic configuration"""
    # In hierarchical process, tasks don't have pre-assigned agents
    # The manager will delegate to appropriate agents
    return Task(
        description=config.description,
        expected_output=config.expected_output,
    )

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution flow"""
    try:
        # 1. Load and validate configurations
        print("\n📋 Loading and validating configurations...")
        config = load_crew_config()
        
        print(f"✓ Loaded {len(config.agents)} agent definitions")
        print(f"✓ Loaded {len(config.tasks)} task definitions")
        print(f"✓ Loaded {len(config.mcp_servers)} MCP servers")
        print("✓ All configs validated successfully")
        
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
        
        # Project Manager (Alpha): ConPort reading + analysis tools
        pm_tools = filter_tools(tools_list, ['conport', 'read', 'file', 'docs', 'git'])
        agents_map['project_manager'] = create_agent(
            'project_manager',
            config.agents['project_manager'],
            llm,
            pm_tools
        )
        print(f"  ✓ Project Manager (Alpha, {len(pm_tools)} tools)")
        
        # ECS Architect: Code editing + type checking
        ecs_tools = filter_tools(tools_list, ['read', 'write', 'file', 'docs'])
        agents_map['ecs_architect'] = create_agent(
            'ecs_architect', 
            config.agents['ecs_architect'], 
            llm,
            ecs_tools
        )
        
        # Yuka AI Engineer: Code editing + testing
        yuka_tools = filter_tools(tools_list, ['read', 'write', 'test', 'file', 'git'])
        agents_map['yuka_ai_engineer'] = create_agent(
            'yuka_ai_engineer',
            config.agents['yuka_ai_engineer'],
            llm,
            yuka_tools
        )
        
        # Rendering Engineer: Browser + React + MUI + vite
        rendering_tools = filter_tools(tools_list, ['playwright', 'vite', 'mui', 'read', 'write'])
        agents_map['rendering_engineer'] = create_agent(
            'rendering_engineer',
            config.agents['rendering_engineer'],
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
            config.agents['systems_engineer'],
            llm,
            systems_tools
        )
        
        # QA Tester: Testing + validation
        qa_tools = filter_tools(tools_list, ['test', 'playwright', 'git', 'read'])
        agents_map['qa_tester'] = create_agent(
            'qa_tester',
            config.agents['qa_tester'],
            llm,
            qa_tools
        )
        
        # Chief Architect: Documentation + context + memory
        doc_tools = filter_tools(tools_list, ['docs', 'context', 'read', 'write', 'memory', 'git', 'brief'])
        agents_map['chief_architect'] = create_agent(
            'chief_architect',
            config.agents['chief_architect'],
            llm,
            doc_tools
        )
        
        # Technical Writer (Omega): ConPort writing + all context tools
        tw_tools = filter_tools(tools_list, ['conport', 'write', 'file', 'git', 'docs'])
        agents_map['technical_writer'] = create_agent(
            'technical_writer',
            config.agents['technical_writer'],
            llm,
            tw_tools
        )
        print(f"  ✓ Technical Writer (Omega, {len(tw_tools)} tools)")
        
        # Technical Director (Manager): All tools for coordination
        manager_tools = tools_list  # Manager gets all tools
        agents_map['technical_director'] = create_agent(
            'technical_director',
            config.agents['technical_director'],
            llm,
            manager_tools
        )
        
        print(f"✓ Created {len(agents_map)} specialized agents (including manager, alpha, omega)")
        
        # 5. Create tasks
        print("\n📝 Creating tasks...")
        tasks_map = {}
        for name, task_config in config.tasks.items():
            tasks_map[name] = create_task(name, task_config, agents_map)
        
        print(f"✓ Created {len(tasks_map)} tasks")
        
        # 6. Create crew with hierarchical process and manager agent
        print("\n🎯 Assembling crew with hierarchical management...")
        
        # Get manager agent
        manager = agents_map.get('technical_director')
        if not manager:
            raise ValueError("technical_director agent not found")
        
        # Remove manager from worker agents
        worker_agents = [agent for name, agent in agents_map.items() if name != 'technical_director']
        
        crew = Crew(
            agents=worker_agents,
            tasks=list(tasks_map.values()),
            manager_agent=manager,
            process=Process.hierarchical,
            planning=True,  # Enable planning for better task breakdown
            verbose=True,
        )
        
        print(f"✓ Crew assembled: {len(worker_agents)} workers + 1 manager")
        print(f"  Manager: {manager.role}")
        print(f"  Process: Hierarchical (manager delegates tasks)")
        
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
