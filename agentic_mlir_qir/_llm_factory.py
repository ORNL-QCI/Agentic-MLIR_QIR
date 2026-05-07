"""Shared LLM-construction helper used by both ``translate()`` and the CLI.

Keeps the logic for choosing between Ollama (local), HuggingFace, and OpenAI
backends in one place so the public API and CLI cannot drift apart.
"""

from __future__ import annotations

import os


def build_llm(model_key: str):
    """Construct a CrewAI ``LLM`` instance for the given model key.

    Looks up ``model_key`` in :class:`agentic_mlir_qir.config.llm_config.LLMConfig`
    and returns an LLM bound to the right provider (Ollama, HuggingFace, OpenAI).

    Raises
    ------
    ValueError
        Unknown model key.
    RuntimeError
        Required API token missing from the environment, or local Ollama
        server unreachable.
    """
    from .config.llm_config import LLMConfig
    from .config.settings import settings
    from crewai.llm import LLM

    model_info = LLMConfig.get_model_info(model_key)
    if model_info is None:
        raise ValueError(
            f"Unknown model key '{model_key}'. "
            "Use LLMConfig.list_all_models() to see available keys."
        )

    if model_info.provider == "huggingface":
        token = os.environ.get(model_info.api_key_env, "")
        if not token:
            raise RuntimeError(
                f"{model_info.api_key_env} not set. "
                f"Get a free token at https://huggingface.co/settings/tokens "
                f"then: export {model_info.api_key_env}=hf_..."
            )
        return LLM(
            model=model_info.get_litellm_model(),
            api_key=token,
            temperature=settings.LLM_TEMPERATURE,
        )

    if model_info.provider == "openai":
        api_key = os.environ.get(model_info.api_key_env, "")
        if not api_key:
            raise RuntimeError(
                f"API key not found. export {model_info.api_key_env}=<your-key>"
            )
        return LLM(
            model=model_info.get_litellm_model(),
            api_key=api_key,
            temperature=settings.LLM_TEMPERATURE,
        )

    # Ollama (default)
    import ollama as _ollama
    _ollama.list()  # raises ConnectionError if server is down
    return LLM(
        model=LLMConfig.get_litellm_model(model_key),
        base_url=settings.LLM_BASE_URL,
        temperature=settings.LLM_TEMPERATURE,
    )
