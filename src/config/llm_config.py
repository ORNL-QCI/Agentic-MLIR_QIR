"""LLM model configuration and management."""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class ModelInfo:
    """Information about an LLM model."""
    size: str
    quantization: str
    vram: str
    quality: str
    speed: str
    recommended_for: str
    ollama_name: str


class LLMConfig:
    """Configuration for available LLM models."""

    MODELS: Dict[str, ModelInfo] = {
        # Production model
        'llama3.1-70b-q4': ModelInfo(
            size='70B',
            quantization='4-bit',
            vram='~40GB',
            quality='excellent',
            speed='medium',
            recommended_for='production',
            ollama_name='llama3.1:70b-instruct-q4_K_M'
        ),

        # Development models
        'llama3.1-8b': ModelInfo(
            size='8B',
            quantization='none',
            vram='~8GB',
            quality='good',
            speed='fast',
            recommended_for='development, testing',
            ollama_name='llama3.1:8b-instruct'
        ),

        'codellama-13b': ModelInfo(
            size='13B',
            quantization='none',
            vram='~13GB',
            quality='very good',
            speed='medium',
            recommended_for='code-heavy tasks',
            ollama_name='codellama:13b'
        ),

        'codellama-34b-q4': ModelInfo(
            size='34B',
            quantization='4-bit',
            vram='~20GB',
            quality='excellent',
            speed='medium-slow',
            recommended_for='complex code translation',
            ollama_name='codellama:34b-instruct-q4_K_M'
        ),
    }

    @classmethod
    def get_model_info(cls, model_key: str) -> Optional[ModelInfo]:
        """Get information about a specific model."""
        return cls.MODELS.get(model_key)

    @classmethod
    def get_ollama_model_name(cls, model_key: str) -> str:
        """Convert model key to Ollama pull name."""
        model_info = cls.MODELS.get(model_key)
        if model_info:
            return model_info.ollama_name
        return model_key  # Return as-is if not found

    @classmethod
    def estimate_vram(cls, model_key: str) -> str:
        """Estimate VRAM requirement for a model."""
        model_info = cls.MODELS.get(model_key)
        if model_info:
            return model_info.vram
        return "Unknown"

    @classmethod
    def get_recommended_models(cls, purpose: str = 'development') -> list[str]:
        """Get recommended models for a specific purpose."""
        return [
            key for key, info in cls.MODELS.items()
            if purpose.lower() in info.recommended_for.lower()
        ]

    @classmethod
    def list_all_models(cls) -> Dict[str, ModelInfo]:
        """List all available models with their information."""
        return cls.MODELS
