"""Unit tests for CrewAI crews"""

import pytest
from unittest.mock import patch, MagicMock


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
