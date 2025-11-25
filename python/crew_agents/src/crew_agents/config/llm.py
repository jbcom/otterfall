"""
LLM Configuration for CrewAI agents.

Uses OpenRouter with automatic model selection.
See: https://docs.crewai.com/concepts/llms#openrouter
"""

import os
from typing import Optional, Any

# Default model to use with OpenRouter
DEFAULT_MODEL = "openrouter/auto"


def get_llm(model: str = DEFAULT_MODEL) -> Any:
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
        Configured LLM instance, or None if API key not set
        
    Note:
        Returns None if OPENROUTER_API_KEY is not set, allowing
        the code to be imported without the API key present.
    """
    from crewai import LLM
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        # Return None - CrewAI will use its default LLM
        return None
    
    return LLM(
        model=model,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


def get_llm_or_raise(model: str = DEFAULT_MODEL) -> Any:
    """
    Get configured LLM instance, raising if API key not set.
    
    Use this when you need to ensure an LLM is available.
    
    Raises:
        ValueError: If OPENROUTER_API_KEY is not set
    """
    llm = get_llm(model)
    if llm is None:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable must be set. "
            "Get your key at https://openrouter.ai/"
        )
    return llm
