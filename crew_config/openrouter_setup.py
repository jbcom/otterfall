"""
OpenRouter LLM Setup for CrewAI
Provides flexible model routing with fallback support
"""

import os
from crewai import LLM


def create_openrouter_llm(model: str = "openrouter/auto", temperature: float = 0.1) -> LLM:
    """
    Create OpenRouter LLM instance
    
    Args:
        model: Model identifier (use 'openrouter/auto' for meta-routing)
        temperature: Sampling temperature
    
    Returns:
        Configured LLM instance
    """
    # OpenRouter uses OPENAI_API_KEY env var with special base URL
    # LiteLLM (used by CrewAI) handles this automatically with openrouter/ prefix
    
    return LLM(
        model=model,
        temperature=temperature,
        max_tokens=4096,
        # OpenRouter is accessed via LiteLLM's openrouter/ prefix
        # No need for additional config if OPENAI_API_KEY is set to OpenRouter key
    )


def create_fallback_llm_chain():
    """
    Create fallback chain: OpenRouter -> Anthropic -> OpenAI
    Returns list of LLM configs to try in order
    """
    llms = []
    
    # Try OpenRouter first (if key available)
    if os.getenv('OPENROUTER_API_KEY'):
        llms.append(create_openrouter_llm("openrouter/auto"))
    
    # Fallback to Anthropic
    if os.getenv('ANTHROPIC_API_KEY'):
        llms.append(LLM(model="claude-3-5-haiku-20241022", temperature=0.1))
    
    # Fallback to OpenAI
    if os.getenv('OPENAI_API_KEY'):
        llms.append(LLM(model="gpt-4o-mini", temperature=0.1))
    
    if not llms:
        raise ValueError("No API keys found! Set OPENROUTER_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY")
    
    return llms[0]  # Return first available


# Model presets
FAST_MODEL = "openrouter/anthropic/claude-3-5-haiku"  # Fast, cheap
BALANCED_MODEL = "openrouter/auto"  # Auto-routing to best model
SMART_MODEL = "openrouter/anthropic/claude-3-5-sonnet"  # Stronger reasoning
CODING_MODEL = "openrouter/anthropic/claude-sonnet-4"  # Best for code (if available)
