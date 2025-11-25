"""Unit tests for CrewAI crews

Testing patterns follow CrewAI best practices:
- Unit tests mock Task.execute_sync to avoid actual LLM calls
- Import tests verify module structure without instantiation
- State tests validate Pydantic models
"""

import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from pathlib import Path


class TestLLMConfig:
    """Test LLM configuration"""

    def test_get_llm_returns_none_without_api_key(self):
        """Test that get_llm returns None when API key is not set"""
        with patch.dict("os.environ", {}, clear=True):
            from crew_agents.config.llm import get_llm

            llm = get_llm()
            assert llm is None

    def test_default_model_is_openrouter_auto(self):
        """Test that the default model is openrouter/auto"""
        from crew_agents.config.llm import DEFAULT_MODEL

        assert DEFAULT_MODEL == "openrouter/auto"

    def test_models_dict_contains_expected_models(self):
        """Test that MODELS dict contains expected model aliases"""
        from crew_agents.config.llm import MODELS

        assert "auto" in MODELS
        assert "deepseek-r1" in MODELS
        assert "claude-sonnet" in MODELS
        assert "gpt-4o" in MODELS
        assert "gemini-flash" in MODELS


class TestCrewImports:
    """Test that all crews can be imported"""

    def test_import_world_design_crew(self):
        """Test WorldDesignCrew can be imported"""
        from crew_agents.crews.world_design.world_design_crew import WorldDesignCrew

        assert WorldDesignCrew is not None

    def test_import_creature_design_crew(self):
        """Test CreatureDesignCrew can be imported"""
        from crew_agents.crews.creature_design.creature_design_crew import (
            CreatureDesignCrew,
        )

        assert CreatureDesignCrew is not None

    def test_import_gameplay_design_crew(self):
        """Test GameplayDesignCrew can be imported"""
        from crew_agents.crews.gameplay_design.gameplay_design_crew import (
            GameplayDesignCrew,
        )

        assert GameplayDesignCrew is not None

    def test_import_ecs_implementation_crew(self):
        """Test ECSImplementationCrew can be imported"""
        from crew_agents.crews.ecs_implementation.ecs_crew import ECSImplementationCrew

        assert ECSImplementationCrew is not None

    def test_import_rendering_crew(self):
        """Test RenderingCrew can be imported"""
        from crew_agents.crews.rendering.rendering_crew import RenderingCrew

        assert RenderingCrew is not None

    def test_import_asset_pipeline_crew(self):
        """Test AssetPipelineCrew can be imported"""
        from crew_agents.crews.asset_pipeline.asset_crew import AssetPipelineCrew

        assert AssetPipelineCrew is not None

    def test_import_qa_validation_crew(self):
        """Test QAValidationCrew can be imported"""
        from crew_agents.crews.qa_validation.qa_crew import QAValidationCrew

        assert QAValidationCrew is not None


class TestFlowImports:
    """Test that all flows can be imported"""

    def test_import_game_design_flow(self):
        """Test GameDesignFlow can be imported"""
        from crew_agents.flows.game_design_flow import GameDesignFlow

        assert GameDesignFlow is not None

    def test_import_implementation_flow(self):
        """Test ImplementationFlow can be imported"""
        from crew_agents.flows.implementation_flow import ImplementationFlow

        assert ImplementationFlow is not None

    def test_import_asset_generation_flow(self):
        """Test AssetGenerationFlow can be imported"""
        from crew_agents.flows.asset_generation_flow import AssetGenerationFlow

        assert AssetGenerationFlow is not None


class TestFlowState:
    """Test flow state management"""

    def test_design_state_has_required_fields(self):
        """Test DesignState has all required fields"""
        from crew_agents.flows.game_design_flow import DesignState

        state = DesignState()
        assert hasattr(state, "world_design")
        assert hasattr(state, "creature_design")
        assert hasattr(state, "gameplay_design")
        assert hasattr(state, "world_approved")
        assert hasattr(state, "max_retries")

    def test_implementation_state_has_required_fields(self):
        """Test ImplementationState has all required fields"""
        from crew_agents.flows.implementation_flow import ImplementationState

        state = ImplementationState()
        assert hasattr(state, "world_design")
        assert hasattr(state, "ecs_components")
        assert hasattr(state, "ecs_systems")
        assert hasattr(state, "rendering_code")

    def test_asset_state_has_required_fields(self):
        """Test AssetState has all required fields"""
        from crew_agents.flows.asset_generation_flow import AssetState

        state = AssetState()
        assert hasattr(state, "creature_design")
        assert hasattr(state, "asset_specs")
        assert hasattr(state, "approved_assets")
        assert hasattr(state, "rejected_assets")


class TestCrewAgentsClass:
    """Test the CrewAgents wrapper class"""

    def test_crew_agents_init_with_default_path(self):
        """Test CrewAgents initializes with default config path"""
        from crew_agents.crew import CrewAgents, get_crewbase_path

        agent = CrewAgents()
        assert agent.config_path == get_crewbase_path()

    def test_crew_agents_init_with_custom_path(self):
        """Test CrewAgents accepts custom config path"""
        from crew_agents.crew import CrewAgents

        custom_path = Path("/tmp/custom_config.yaml")
        agent = CrewAgents(config_path=custom_path)
        assert agent.config_path == custom_path

    def test_kickoff_does_not_mutate_inputs(self):
        """Test that kickoff() does not modify the original inputs dict"""
        from crew_agents.crew import CrewAgents

        # Create mock crew that returns immediately
        with patch("crew_agents.crew.Crew") as MockCrew:
            mock_crew_instance = MagicMock()
            mock_crew_instance.tasks = []
            mock_crew_instance.kickoff.return_value = "result"
            MockCrew.from_yaml.return_value = mock_crew_instance

            agent = CrewAgents()
            original_inputs = {"task": "some_task", "key": "value"}
            inputs_copy = original_inputs.copy()

            # Even though kickoff fails (no tasks), inputs should not be mutated
            try:
                agent.kickoff(inputs=original_inputs)
            except ValueError:
                pass  # Expected - no matching tasks

            # Original dict should be unchanged
            assert original_inputs == inputs_copy

    def test_kickoff_async_does_not_mutate_inputs(self):
        """Test that kickoff_async() does not modify the original inputs dict"""
        from crew_agents.crew import CrewAgents

        with patch("crew_agents.crew.Crew") as MockCrew:
            mock_crew_instance = MagicMock()
            mock_crew_instance.tasks = []
            mock_crew_instance.kickoff_async.return_value = "async_result"
            MockCrew.from_yaml.return_value = mock_crew_instance

            agent = CrewAgents()
            original_inputs = {"task": "some_task", "another": "param"}
            inputs_copy = original_inputs.copy()

            try:
                agent.kickoff_async(inputs=original_inputs)
            except ValueError:
                pass  # Expected - no matching tasks

            # Original dict should be unchanged
            assert original_inputs == inputs_copy

    def test_get_crew_for_task_raises_on_unknown_task(self):
        """Test that _get_crew_for_task raises ValueError for unknown task"""
        from crew_agents.crew import CrewAgents

        with patch("crew_agents.crew.Crew") as MockCrew:
            mock_task = MagicMock()
            mock_task.name = "existing_task"

            mock_crew_instance = MagicMock()
            mock_crew_instance.tasks = [mock_task]
            MockCrew.from_yaml.return_value = mock_crew_instance

            agent = CrewAgents()

            with pytest.raises(ValueError) as exc_info:
                agent._get_crew_for_task("nonexistent_task")

            assert "nonexistent_task" in str(exc_info.value)
            assert "Available:" in str(exc_info.value)

    def test_get_crew_for_task_returns_cached_crew_when_no_filter(self):
        """Test that _get_crew_for_task returns cached crew when no task filter"""
        from crew_agents.crew import CrewAgents

        with patch("crew_agents.crew.Crew") as MockCrew:
            mock_crew_instance = MagicMock()
            MockCrew.from_yaml.return_value = mock_crew_instance

            agent = CrewAgents()

            # First call creates the crew
            crew1 = agent._get_crew_for_task(None)
            # Second call should return same instance (cached)
            crew2 = agent._get_crew_for_task(None)

            assert crew1 is crew2
            # from_yaml should only be called once for cached access
            assert MockCrew.from_yaml.call_count == 1


class TestStandaloneKickoffFunction:
    """Test the standalone kickoff function"""

    def test_kickoff_function_does_not_mutate_inputs(self):
        """Test that standalone kickoff() function doesn't mutate inputs"""
        from crew_agents.crew import kickoff

        with patch("crew_agents.crew.Crew") as MockCrew:
            mock_crew_instance = MagicMock()
            mock_crew_instance.tasks = []
            mock_crew_instance.kickoff.return_value = "result"
            MockCrew.from_yaml.return_value = mock_crew_instance

            with patch("crew_agents.crew.load_crewbase"):
                original_inputs = {"task": "test_task", "data": "important"}
                inputs_copy = original_inputs.copy()

                # Task filtering will result in empty tasks, but inputs should stay intact
                try:
                    kickoff(inputs=original_inputs)
                except Exception:
                    pass

                assert original_inputs == inputs_copy

    def test_kickoff_filters_task_correctly(self):
        """Test that kickoff correctly filters to specified task"""
        from crew_agents.crew import kickoff

        with patch("crew_agents.crew.Crew") as MockCrew:
            mock_task_1 = MagicMock()
            mock_task_1.name = "task_one"
            mock_task_2 = MagicMock()
            mock_task_2.name = "task_two"

            mock_crew_instance = MagicMock()
            mock_crew_instance.tasks = [mock_task_1, mock_task_2]
            mock_crew_instance.kickoff.return_value = "result"
            MockCrew.from_yaml.return_value = mock_crew_instance

            with patch("crew_agents.crew.load_crewbase"):
                kickoff(inputs={"task": "task_one"})

                # Verify crew tasks were filtered
                assert mock_crew_instance.tasks == [mock_task_1]

    def test_kickoff_raises_for_unknown_task(self):
        """Test that kickoff raises ValueError for unknown task name"""
        from crew_agents.crew import kickoff

        with patch("crew_agents.crew.Crew") as MockCrew:
            mock_task = MagicMock()
            mock_task.name = "existing_task"

            mock_crew_instance = MagicMock()
            mock_crew_instance.tasks = [mock_task]
            MockCrew.from_yaml.return_value = mock_crew_instance

            with patch("crew_agents.crew.load_crewbase"):
                with pytest.raises(ValueError) as exc_info:
                    kickoff(inputs={"task": "nonexistent"})

                assert "nonexistent" in str(exc_info.value)
