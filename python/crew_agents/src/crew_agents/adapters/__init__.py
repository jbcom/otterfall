"""
DEPRECATED: MCP Tool Adapters for CrewAI

CrewAI now has native MCP integration via MCPTool.from_server().
These adapters are no longer needed and will be removed in a future version.

See: python/crew_agents/src/crew_agents/__main__.py for new implementation
"""

# Legacy imports for backwards compatibility
from .git_adapter import GitAdapter
from .github_adapter import GitHubAdapter
from .vite_adapter import ViteAdapter
from .playwright_adapter import PlaywrightAdapter
from .conport_adapter import ConPortAdapter
from .filesystem_adapter import FilesystemAdapter
from .knowledge_adapter import KnowledgeAdapter
from .docs_adapter import DocsAdapter

__all__ = [
    "GitAdapter",
    "GitHubAdapter",
    "ViteAdapter",
    "PlaywrightAdapter",
    "ConPortAdapter",
    "FilesystemAdapter",
    "KnowledgeAdapter",
    "DocsAdapter",
]