"""Configuration for CrewAI agents."""

from crew_agents.config.llm import get_llm, default_llm, creative_llm, analytical_llm, code_llm

__all__ = [
    "get_llm",
    "default_llm",
    "creative_llm",
    "analytical_llm",
    "code_llm",
]
