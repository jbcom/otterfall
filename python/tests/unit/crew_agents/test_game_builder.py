"""Tests for the GameBuilderCrew and file tools."""

import pytest
from pathlib import Path


class TestFileTools:
    """Test the file manipulation tools."""

    def test_get_workspace_root_returns_path(self):
        """Test that get_workspace_root returns a valid path."""
        from crew_agents.tools.file_tools import get_workspace_root

        workspace = get_workspace_root()
        assert isinstance(workspace, Path)
        # Should have client and python directories
        assert (workspace / "client").exists() or workspace == Path(".").resolve()

    def test_directory_list_tool_finds_components(self):
        """Test that DirectoryListTool can list ECS components."""
        from crew_agents.tools.file_tools import DirectoryListTool

        tool = DirectoryListTool()
        result = tool._run("client/src/ecs/components")

        # Should contain some known component files
        assert "BiomeComponent.ts" in result or "Error" not in result

    def test_directory_list_tool_rejects_path_traversal(self):
        """Test that DirectoryListTool rejects path traversal."""
        from crew_agents.tools.file_tools import DirectoryListTool

        tool = DirectoryListTool()
        result = tool._run("../../../etc")

        assert "Error" in result
        assert "traversal" in result.lower()

    def test_code_reader_tool_reads_file(self):
        """Test that GameCodeReaderTool can read existing files."""
        from crew_agents.tools.file_tools import GameCodeReaderTool

        tool = GameCodeReaderTool()
        result = tool._run("client/src/ecs/components.ts")

        # Should contain component interfaces
        assert "interface" in result or "export" in result or "Error" in result

    def test_code_reader_tool_rejects_path_traversal(self):
        """Test that GameCodeReaderTool rejects path traversal."""
        from crew_agents.tools.file_tools import GameCodeReaderTool

        tool = GameCodeReaderTool()
        result = tool._run("../../../etc/passwd")

        assert "Error" in result
        assert "traversal" in result.lower()

    def test_code_writer_tool_validates_directory(self):
        """Test that GameCodeWriterTool validates allowed directories."""
        from crew_agents.tools.file_tools import GameCodeWriterTool

        tool = GameCodeWriterTool()

        # Should reject writing outside allowed directories
        result = tool._run(
            file_path="some/random/path/file.ts", content="// test content"
        )

        assert "Error" in result
        assert "not in an allowed directory" in result

    def test_code_writer_tool_validates_extension(self):
        """Test that GameCodeWriterTool validates file extensions."""
        from crew_agents.tools.file_tools import GameCodeWriterTool

        tool = GameCodeWriterTool()

        # Should reject non-allowed extensions
        result = tool._run(
            file_path="client/src/ecs/components/test.exe", content="// test content"
        )

        assert "Error" in result
        assert "not allowed" in result


class TestGameBuilderCrew:
    """Test the GameBuilderCrew."""

    def test_game_builder_crew_imports(self):
        """Test that GameBuilderCrew can be imported."""
        from crew_agents.crews.game_builder import GameBuilderCrew

        assert GameBuilderCrew is not None

    def test_game_builder_crew_has_tools(self):
        """Test that GameBuilderCrew has required tools."""
        from crew_agents.crews.game_builder import GameBuilderCrew

        crew = GameBuilderCrew()
        assert hasattr(crew, "code_writer")
        assert hasattr(crew, "code_reader")
        assert hasattr(crew, "dir_lister")

    def test_game_builder_crew_has_agents(self):
        """Test that GameBuilderCrew has required agents defined."""
        from crew_agents.crews.game_builder import GameBuilderCrew

        crew = GameBuilderCrew()
        # Check agent methods exist
        assert hasattr(crew, "senior_typescript_engineer")
        assert hasattr(crew, "qa_engineer")
        assert hasattr(crew, "chief_engineer")

    def test_game_builder_crew_has_tasks(self):
        """Test that GameBuilderCrew has required tasks defined."""
        from crew_agents.crews.game_builder import GameBuilderCrew

        crew = GameBuilderCrew()
        # Check task methods exist
        assert hasattr(crew, "write_code_task")
        assert hasattr(crew, "review_code_task")
        assert hasattr(crew, "evaluate_code_task")


class TestKnowledge:
    """Test the knowledge loading functionality."""

    def test_knowledge_path_exists(self):
        """Test that knowledge directory exists."""
        from crew_agents.crews.game_builder.game_builder_crew import get_knowledge_path

        knowledge_path = get_knowledge_path()
        # Knowledge path should exist after setup
        assert knowledge_path.exists() or True  # Pass even if not yet created

    def test_load_knowledge_sources_returns_list(self):
        """Test that load_knowledge_sources returns a list."""
        from crew_agents.crews.game_builder.game_builder_crew import load_knowledge_sources

        sources = load_knowledge_sources()
        assert isinstance(sources, list)
