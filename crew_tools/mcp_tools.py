"""
MCP Tool Wrappers for CrewAI
Exposes all available MCP and Replit tools to CrewAI agents
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Any


class FileReadSchema(BaseModel):
    file_path: str = Field(description="Path to the file to read")
    limit: int = Field(default=500, description="Number of lines to read")


class FileWriteSchema(BaseModel):
    file_path: str = Field(description="Path to the file to write")
    content: str = Field(description="Content to write to the file")


class FileEditSchema(BaseModel):
    file_path: str = Field(description="Path to the file to edit")
    old_string: str = Field(description="Exact text to replace")
    new_string: str = Field(description="New text to insert")


class CodeSearchSchema(BaseModel):
    query: str = Field(description="Natural language question about the codebase")
    search_paths: list[str] = Field(default_factory=list, description="Directories to search in")


class GrepSearchSchema(BaseModel):
    pattern: str = Field(description="Regex pattern to search for")
    path: str = Field(default=".", description="Path to search in")
    type: str = Field(default=None, description="File type filter (e.g., 'ts', 'py')")


class LSPDiagnosticsSchema(BaseModel):
    file_path: str = Field(default=None, description="File path to get diagnostics for")


class BashCommandSchema(BaseModel):
    command: str = Field(description="Bash command to execute")
    description: str = Field(description="Brief description of what the command does")


class FigmaDesignContextSchema(BaseModel):
    nodeId: str = Field(description="Figma node ID (e.g., '1:2')")
    fileKey: str = Field(description="Figma file key")
    clientLanguages: str = Field(default="typescript", description="Programming languages")
    clientFrameworks: str = Field(default="react", description="Frameworks being used")


# Placeholder implementations - these will be called by CrewAI
# The actual tool execution will need to be wired up to Replit's tools

class FileReadTool(BaseTool):
    name: str = "file_read"
    description: str = "Read contents of a file from the codebase. Use for examining code."
    args_schema: type[BaseModel] = FileReadSchema

    def _run(self, file_path: str, limit: int = 500) -> str:
        # This will be implemented by calling actual Replit read tool
        return f"TOOL_CALL:read:{file_path}:{limit}"


class FileWriteTool(BaseTool):
    name: str = "file_write"
    description: str = "Write or overwrite a file in the codebase. Use for creating new files."
    args_schema: type[BaseModel] = FileWriteSchema

    def _run(self, file_path: str, content: str) -> str:
        return f"TOOL_CALL:write:{file_path}:{len(content)}"


class FileEditTool(BaseTool):
    name: str = "file_edit"
    description: str = "Edit a file by replacing exact text. Use for modifying existing code."
    args_schema: type[BaseModel] = FileEditSchema

    def _run(self, file_path: str, old_string: str, new_string: str) -> str:
        return f"TOOL_CALL:edit:{file_path}"


class CodeSearchTool(BaseTool):
    name: str = "code_search"
    description: str = "Search the entire codebase with natural language. Use for finding relevant code."
    args_schema: type[BaseModel] = CodeSearchSchema

    def _run(self, query: str, search_paths: list[str] = None) -> str:
        paths = ",".join(search_paths) if search_paths else "all"
        return f"TOOL_CALL:search_codebase:{query}:{paths}"


class GrepSearchTool(BaseTool):
    name: str = "grep_search"
    description: str = "Search for patterns using regex. Use for finding specific text in files."
    args_schema: type[BaseModel] = GrepSearchSchema

    def _run(self, pattern: str, path: str = ".", type: str = None) -> str:
        return f"TOOL_CALL:grep:{pattern}:{path}:{type or 'all'}"


class LSPDiagnosticsTool(BaseTool):
    name: str = "lsp_diagnostics"
    description: str = "Get TypeScript/Python errors and warnings. Use for code quality checks."
    args_schema: type[BaseModel] = LSPDiagnosticsSchema

    def _run(self, file_path: str = None) -> str:
        return f"TOOL_CALL:lsp:{file_path or 'all'}"


class BashCommandTool(BaseTool):
    name: str = "bash_command"
    description: str = "Execute bash commands. Use for running tests, builds, or system operations."
    args_schema: type[BaseModel] = BashCommandSchema

    def _run(self, command: str, description: str) -> str:
        return f"TOOL_CALL:bash:{command}"


class FigmaDesignTool(BaseTool):
    name: str = "figma_design_context"
    description: str = "Get design context and generated code from Figma. Use for implementing UI from designs."
    args_schema: type[BaseModel] = FigmaDesignContextSchema

    def _run(self, nodeId: str, fileKey: str, clientLanguages: str = "typescript", clientFrameworks: str = "react") -> str:
        return f"TOOL_CALL:figma:{fileKey}:{nodeId}"


# Tool collections by specialty
ECS_ARCHITECT_TOOLS = [CodeSearchTool(), FileReadTool(), LSPDiagnosticsTool()]
YUKA_AI_TOOLS = [CodeSearchTool(), FileReadTool(), FileEditTool(), LSPDiagnosticsTool()]
RENDERING_TOOLS = [CodeSearchTool(), FileReadTool(), FileEditTool(), FigmaDesignTool()]
SYSTEMS_ENGINEER_TOOLS = [CodeSearchTool(), FileReadTool(), FileEditTool(), LSPDiagnosticsTool(), BashCommandTool()]
QA_TESTER_TOOLS = [BashCommandTool(), LSPDiagnosticsTool(), GrepSearchTool(), FileReadTool()]
ALL_TOOLS = [
    FileReadTool(),
    FileWriteTool(),
    FileEditTool(),
    CodeSearchTool(),
    GrepSearchTool(),
    LSPDiagnosticsTool(),
    BashCommandTool(),
    FigmaDesignTool()
]
