"""
LLM Configuration for CrewAI agents.

Uses OpenRouter with automatic model selection.
See: https://docs.crewai.com/concepts/llms#openrouter
"""

import os
from crewai import LLM


def get_llm(model: str = "openrouter/auto") -> LLM:
    """
    Get configured LLM instance for CrewAI agents.
    
    Args:
        model: Model identifier. Defaults to openrouter/auto which
               automatically selects the best model for the task.
               
    Available models via OpenRouter:
        - openrouter/auto (recommended - auto-selects best model)
        - openrouter/anthropic/claude-3.5-sonnet
        - openrouter/openai/gpt-4o
        - openrouter/google/gemini-pro-1.5
        
    Returns:
        Configured LLM instance
    """
    return LLM(
        model=model,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )


# Default LLM instance using auto-routing
default_llm = get_llm("openrouter/auto")

# Specialized LLMs for specific tasks (if needed)
creative_llm = get_llm("openrouter/auto")  # Could use claude for creative tasks
analytical_llm = get_llm("openrouter/auto")  # Could use gpt-4o for analysis
code_llm = get_llm("openrouter/auto")  # Could use claude for code generation
