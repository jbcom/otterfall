"""Production-grade tool adapters for CrewAI agents"""

from .base import BaseToolAdapter, ToolResult, ToolError
from .git_adapter import GitAdapter
from .github_adapter import GitHubAdapter
from .vite_adapter import ViteAdapter
from .playwright_adapter import PlaywrightAdapter
from .database_adapter import DatabaseAdapter
from .filesystem_adapter import FilesystemAdapter
from .knowledge_adapter import KnowledgeAdapter
from .docs_adapter import DocsAdapter

__all__ = [
    "BaseToolAdapter",
    "ToolResult",
    "ToolError",
    "GitAdapter",
    "GitHubAdapter",
    "ViteAdapter",
    "PlaywrightAdapter",
    "DatabaseAdapter",
    "FilesystemAdapter",
    "KnowledgeAdapter",
    "DocsAdapter",
]
