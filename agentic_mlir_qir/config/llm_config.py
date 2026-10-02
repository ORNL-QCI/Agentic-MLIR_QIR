"""LLM model configuration and management."""

import os
from typing import Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ModelInfo:
    """Information about an LLM model."""
    size: str
    quantization: str
    vram: str
    quality: str
    speed: str
    recommended_for: str
    ollama_name: str                    # Ollama pull name (empty string for API models)
    provider: str = "ollama"            # "ollama" | "openai" | "huggingface"
    api_key_env: str = ""               # env var holding the API key (API models only)
    free_tier: bool = False             # whether a free tier is available
    litellm_model: str = ""             # litellm model string (defaults to ollama_name)

    def get_litellm_model(self) -> str:
        """Return the litellm model identifier used by crewai LLM."""
        if self.litellm_model:
            return self.litellm_model
        if self.provider == "ollama":
            return f"ollama/{self.ollama_name}"
        if self.provider == "huggingface":
            return f"huggingface/{self.ollama_name}"  # ollama_name holds the HF model ID
        return self.ollama_name  # fallback


class LLMConfig:
    """Configuration for available LLM models."""

    MODELS: Dict[str, ModelInfo] = {
        # ── Local Ollama models ───────────────────────────────────────────────
        'llama3.1-70b-q4': ModelInfo(
            size='70B',
            quantization='4-bit',
            vram='~40GB',
            quality='excellent',
            speed='medium',
            recommended_for='production',
            ollama_name='llama3.1:70b-instruct-q4_K_M',
            provider='ollama',
        ),
        'llama3.1-8b': ModelInfo(
            size='8B',
            quantization='none',
            vram='~8GB',
            quality='good',
            speed='fast',
            recommended_for='development, testing',
            ollama_name='llama3.1:8b',
            provider='ollama',
        ),
        'gemma4-31b': ModelInfo(
            size='31B',
            quantization='4-bit',
            vram='~20GB',
            quality='excellent',
            speed='medium',
            recommended_for='local Path 3 repair testing without HuggingFace credits',
            ollama_name='gemma4:31b-it-q4_K_M',
            provider='ollama',
        ),
        'codellama-13b': ModelInfo(
            size='13B',
            quantization='none',
            vram='~13GB',
            quality='very good',
            speed='medium',
            recommended_for='code-heavy tasks',
            ollama_name='codellama:13b-instruct',
            provider='ollama',
        ),
        'codellama-34b-q4': ModelInfo(
            size='34B',
            quantization='4-bit',
            vram='~20GB',
            quality='excellent',
            speed='medium-slow',
            recommended_for='complex code translation',
            ollama_name='codellama:34b-instruct-q4_K_M',
            provider='ollama',
        ),

        # ── HuggingFace Inference API (free HF token, no local GPU needed) ───
        # Get a free token at: https://huggingface.co/settings/tokens
        # export HF_TOKEN=hf_...
        'gpt-oss-20b': ModelInfo(
            size='20B',
            quantization='none',
            vram='cloud',
            quality='very good',
            speed='fast',
            recommended_for='translation, verification (open-weight, Apache 2.0, free HF token)',
            ollama_name='openai/gpt-oss-20b',   # HF model ID stored in ollama_name field
            provider='huggingface',
            api_key_env='HF_TOKEN',
            free_tier=True,
        ),

        # Llama 3.1 8B via the HuggingFace Inference API (no local Ollama).
        # NOTE: meta-llama models are GATED — before this key works you must
        # (1) accept Meta's license on the model page
        #     https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct and
        # (2) be granted access on the HF account tied to your HF_TOKEN.
        # Serverless/free hosting is not guaranteed (HF routes through
        # Inference Providers and may charge); for a guaranteed-free portable
        # model prefer 'gpt-oss-20b'.
        'llama3.1-8b-hf': ModelInfo(
            size='8B',
            quantization='none',
            vram='cloud',
            quality='good',
            speed='fast',
            recommended_for='portable agentic path without Ollama (gated model; requires HF access approval)',
            ollama_name='meta-llama/Llama-3.1-8B-Instruct',  # HF model ID
            provider='huggingface',
            api_key_env='HF_TOKEN',
            free_tier=False,
        ),

        # Google Gemma 4 (latest Gemma; flagship 31B dense instruct) via the
        # HuggingFace Inference API — no local Ollama.
        # Open-weight (Apache 2.0), NOT gated — no license acceptance or access
        # approval needed. Free serverless hosting is still not guaranteed (HF
        # routes through Inference Providers and may charge).
        'gemma4-31b-hf': ModelInfo(
            size='31B',
            quantization='none',
            vram='cloud',
            quality='excellent',
            speed='medium',
            recommended_for='portable agentic path without Ollama (open-weight Apache 2.0, not gated)',
            ollama_name='google/gemma-4-31B-it',  # HF model ID
            provider='huggingface',
            api_key_env='HF_TOKEN',
            free_tier=False,
        ),
    }

    # ── Default model for the agentic route ──────────────────────────────────
    # Preference order, strongest first. ``resolve_default_model`` walks this
    # chain and returns the first entry whose credentials are present, so the
    # UI never opens on a model the environment cannot reach.
    DEFAULT_MODEL: str = 'gemma4-31b-hf'
    DEFAULT_MODEL_CHAIN: tuple[str, ...] = (
        'gemma4-31b-hf',   # 31B, HuggingFace  — needs HF_TOKEN
        'gpt-oss-20b',     # 20B, HuggingFace  — needs HF_TOKEN, free tier
        'llama3.1-8b',     #  8B, local Ollama — no credentials
    )

    @classmethod
    def has_credentials(cls, model_key: str) -> bool:
        """Return True if the env var this model needs is set.

        Offline check only: it confirms credentials exist, not that the
        provider is currently serving the model. Ollama models need no
        credentials and always pass.
        """
        info = cls.MODELS.get(model_key)
        if info is None:
            return False
        if not info.api_key_env:
            return True
        return bool(os.environ.get(info.api_key_env))

    @classmethod
    def resolve_default_model(cls) -> str:
        """Return the first model in DEFAULT_MODEL_CHAIN with credentials set."""
        for key in cls.DEFAULT_MODEL_CHAIN:
            if cls.has_credentials(key):
                return key
        return cls.DEFAULT_MODEL

    @classmethod
    def get_model_info(cls, model_key: str) -> Optional[ModelInfo]:
        return cls.MODELS.get(model_key)

    @classmethod
    def get_ollama_model_name(cls, model_key: str) -> str:
        """Return Ollama pull name (for Ollama models only)."""
        model_info = cls.MODELS.get(model_key)
        if model_info and model_info.provider == "ollama":
            return model_info.ollama_name
        return model_key

    @classmethod
    def get_litellm_model(cls, model_key: str) -> str:
        """Return the litellm model string used by crewai LLM."""
        model_info = cls.MODELS.get(model_key)
        if model_info:
            return model_info.get_litellm_model()
        return model_key

    @classmethod
    def is_ollama_model(cls, model_key: str) -> bool:
        info = cls.MODELS.get(model_key)
        return info is None or info.provider == "ollama"

    @classmethod
    def estimate_vram(cls, model_key: str) -> str:
        model_info = cls.MODELS.get(model_key)
        return model_info.vram if model_info else "Unknown"

    @classmethod
    def get_recommended_models(cls, purpose: str = 'development') -> list[str]:
        return [
            key for key, info in cls.MODELS.items()
            if purpose.lower() in info.recommended_for.lower()
        ]

    @classmethod
    def list_all_models(cls) -> Dict[str, ModelInfo]:
        return cls.MODELS
