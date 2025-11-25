"""
File manipulation tools for CrewAI agents.

These tools enable agents to read and write code to specific directories
in the Rivermarsh game codebase.
"""

import os
from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


def get_workspace_root() -> Path:
    """Get the workspace root directory."""
    # Navigate up from this file to find the workspace root
    current = Path(__file__).resolve()
    # Go up: tools -> crew_agents -> src -> crew_agents -> python -> workspace
    for _ in range(6):
        current = current.parent
        if (current / "client").exists() and (current / "python").exists():
            return current
    # Fallback to environment variable or current directory
    return Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()


# Allowed directories for writing
ALLOWED_WRITE_DIRS = [
    "client/src/ecs/components",
    "client/src/ecs/entities",
    "client/src/ecs/systems",
    "client/src/components",
    "client/src/lib/stores",
    "shared/contracts",
    "shared/backend/ecs_world",
]

# Allowed file extensions
ALLOWED_EXTENSIONS = {".ts", ".tsx", ".json", ".md"}


class WriteFileInput(BaseModel):
    """Input schema for GameCodeWriterTool."""

    file_path: str = Field(
        description="Relative path from workspace root (e.g., 'client/src/ecs/components/NewComponent.ts')"
    )
    content: str = Field(description="The TypeScript/TSX code content to write")


class GameCodeWriterTool(BaseTool):
    """
    Tool for writing code files to the Rivermarsh game codebase.

    This tool is restricted to specific directories to ensure agents
    only modify appropriate parts of the codebase.
    """

    name: str = "Write Game Code File"
    description: str = """
    Write a code file to the Rivermarsh game codebase.
    
    ALLOWED DIRECTORIES:
    - client/src/ecs/components - ECS component definitions
    - client/src/ecs/entities - Entity factory functions
    - client/src/ecs/systems - ECS systems
    - client/src/components - React Three Fiber components
    - client/src/lib/stores - Zustand stores
    - shared/contracts - TypeScript contracts
    - shared/backend/ecs_world - Backend ECS code
    
    ALLOWED EXTENSIONS: .ts, .tsx, .json, .md
    
    Example:
        file_path: "client/src/ecs/components/QuestComponent.ts"
        content: "export interface QuestComponent { ... }"
    """
    args_schema: Type[BaseModel] = WriteFileInput

    def _run(self, file_path: str, content: str) -> str:
        """Write the file content to the specified path."""
        try:
            # Validate path
            clean_path = file_path.strip().replace("\\", "/")

            # Check for path traversal
            if ".." in clean_path or clean_path.startswith("/"):
                return f"Error: Invalid path '{clean_path}'. Path traversal not allowed."

            # Check allowed directories
            is_allowed = any(
                clean_path.startswith(allowed_dir) for allowed_dir in ALLOWED_WRITE_DIRS
            )
            if not is_allowed:
                return f"Error: Path '{clean_path}' is not in an allowed directory. Allowed: {ALLOWED_WRITE_DIRS}"

            # Check extension
            ext = Path(clean_path).suffix.lower()
            if ext not in ALLOWED_EXTENSIONS:
                return f"Error: Extension '{ext}' not allowed. Allowed: {ALLOWED_EXTENSIONS}"

            # Construct full path
            workspace_root = get_workspace_root()
            full_path = workspace_root / clean_path

            # Create parent directories
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

            return f"Successfully wrote {len(content)} bytes to {clean_path}"

        except PermissionError:
            return f"Error: Permission denied writing to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"


class ReadFileInput(BaseModel):
    """Input schema for GameCodeReaderTool."""

    file_path: str = Field(
        description="Relative path from workspace root (e.g., 'client/src/ecs/components.ts')"
    )


class GameCodeReaderTool(BaseTool):
    """
    Tool for reading code files from the Rivermarsh game codebase.

    Use this to understand existing patterns before writing new code.
    """

    name: str = "Read Game Code File"
    description: str = """
    Read a code file from the Rivermarsh game codebase.
    
    Use this tool to:
    - Understand existing patterns
    - See how similar components are structured
    - Check imports and dependencies
    
    Example:
        file_path: "client/src/ecs/components.ts"
    """
    args_schema: Type[BaseModel] = ReadFileInput

    def _run(self, file_path: str) -> str:
        """Read the file content from the specified path."""
        try:
            clean_path = file_path.strip().replace("\\", "/")

            if ".." in clean_path:
                return f"Error: Path traversal not allowed in '{clean_path}'"

            workspace_root = get_workspace_root()
            full_path = workspace_root / clean_path

            if not full_path.exists():
                return f"Error: File not found: {clean_path}"

            if not full_path.is_file():
                return f"Error: Path is not a file: {clean_path}"

            # Limit file size
            if full_path.stat().st_size > 100_000:  # 100KB limit
                return f"Error: File too large (>{100_000} bytes)"

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            return content

        except PermissionError:
            return f"Error: Permission denied reading {file_path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"


class ListDirInput(BaseModel):
    """Input schema for DirectoryListTool."""

    directory: str = Field(
        description="Relative directory path from workspace root (e.g., 'client/src/ecs')"
    )


class DirectoryListTool(BaseTool):
    """
    Tool for listing files in a directory.

    Use this to discover existing files and understand project structure.
    """

    name: str = "List Directory Contents"
    description: str = """
    List files and subdirectories in a directory.
    
    Use this to:
    - Discover existing components
    - Understand project structure
    - Find files to read or reference
    
    Example:
        directory: "client/src/ecs/components"
    """
    args_schema: Type[BaseModel] = ListDirInput

    def _run(self, directory: str) -> str:
        """List directory contents."""
        try:
            clean_path = directory.strip().replace("\\", "/")

            if ".." in clean_path:
                return "Error: Path traversal not allowed"

            workspace_root = get_workspace_root()
            full_path = workspace_root / clean_path

            if not full_path.exists():
                return f"Error: Directory not found: {clean_path}"

            if not full_path.is_dir():
                return f"Error: Path is not a directory: {clean_path}"

            entries = []
            for entry in sorted(full_path.iterdir()):
                if entry.name.startswith("."):
                    continue
                prefix = "📁" if entry.is_dir() else "📄"
                entries.append(f"{prefix} {entry.name}")

            if not entries:
                return f"Directory {clean_path} is empty"

            return f"Contents of {clean_path}:\n" + "\n".join(entries)

        except PermissionError:
            return f"Error: Permission denied accessing {directory}"
        except Exception as e:
            return f"Error listing directory: {str(e)}"
