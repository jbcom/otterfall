"""
LLM Configuration for CrewAI agents.

Uses OpenRouter with automatic model selection.
See: https://docs.crewai.com/en/concepts/llms#open-router
"""

import os
from typing import Any, Optional

# Default model - openrouter/auto automatically selects best model
DEFAULT_MODEL = "openrouter/auto"

# Alternative models available via OpenRouter
MODELS = {
    "auto": "openrouter/auto",
    "deepseek-r1": "openrouter/deepseek/deepseek-r1",
    "deepseek-chat": "openrouter/deepseek/deepseek-chat",
    "claude-sonnet": "openrouter/anthropic/claude-3.5-sonnet",
    "gpt-4o": "openrouter/openai/gpt-4o",
    "gemini-flash": "openrouter/google/gemini-2.0-flash",
}


def get_llm(model: str = DEFAULT_MODEL, temperature: float = 0.7) -> Optional[Any]:
    """
    Get configured LLM instance for CrewAI agents.

    Args:
        model: Model identifier. Defaults to openrouter/auto which
               automatically selects the best model for the task.
        temperature: Sampling temperature (0.0-1.0). Lower = more focused,
                    higher = more creative.

    Available models via OpenRouter:
        - openrouter/auto (recommended - auto-selects best model)
        - openrouter/deepseek/deepseek-r1 (reasoning model)
        - openrouter/deepseek/deepseek-chat (chat model)
        - openrouter/anthropic/claude-3.5-sonnet
        - openrouter/openai/gpt-4o
        - openrouter/google/gemini-2.0-flash

    Returns:
        Configured LLM instance, or None if API key not set

    Note:
        Returns None if OPENROUTER_API_KEY is not set, allowing
        the code to be imported without the API key present.
        When None is returned, CrewAI will fall back to its default LLM.

    Example:
        >>> llm = get_llm()  # Uses openrouter/auto
        >>> llm = get_llm("openrouter/anthropic/claude-3.5-sonnet", temperature=0.3)
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
        temperature=temperature,
    )


def get_llm_or_raise(model: str = DEFAULT_MODEL, temperature: float = 0.7) -> Any:
    """
    Get configured LLM instance, raising if API key not set.

    Use this when you need to ensure an LLM is available.

    Args:
        model: Model identifier (see get_llm for options)
        temperature: Sampling temperature (0.0-1.0)

    Returns:
        Configured LLM instance

    Raises:
        ValueError: If OPENROUTER_API_KEY is not set
    """
    llm = get_llm(model, temperature)
    if llm is None:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable must be set. "
            "Get your key at https://openrouter.ai/"
        )
    return llm


# Convenience functions for specific use cases
def get_reasoning_llm() -> Optional[Any]:
    """Get LLM optimized for complex reasoning tasks."""
    return get_llm(MODELS["deepseek-r1"], temperature=0.3)


def get_creative_llm() -> Optional[Any]:
    """Get LLM optimized for creative tasks."""
    return get_llm(MODELS["auto"], temperature=0.8)


def get_code_llm() -> Optional[Any]:
    """Get LLM optimized for code generation."""
    return get_llm(MODELS["auto"], temperature=0.2)
