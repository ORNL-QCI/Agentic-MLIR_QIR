"""Configuration management for MLIR to QIR translator."""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Configuration
    LLM_PROVIDER: str = Field(default="ollama", description="LLM provider (ollama, huggingface)")
    LLM_MODEL: str = Field(default="llama3.1:8b-instruct", description="LLM model name")
    LLM_TEMPERATURE: float = Field(default=0.1, description="LLM temperature for generation")
    LLM_BASE_URL: str = Field(default="http://localhost:11434", description="Ollama base URL")
    LLM_MAX_TOKENS: int = Field(default=4000, description="Maximum tokens for LLM generation")

    # RAG Configuration
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="HuggingFace embedding model"
    )
    CHUNK_SIZE: int = Field(default=1000, description="Text chunk size for RAG")
    CHUNK_OVERLAP: int = Field(default=200, description="Chunk overlap size")
    RAG_TOP_K: int = Field(default=5, description="Number of documents to retrieve")
    CHROMADB_PATH: str = Field(default="data/chromadb", description="ChromaDB storage path")

    # Verification Thresholds
    GATE_COUNT_TOLERANCE: float = Field(default=0.0, description="Gate count tolerance (0.0 = exact match)")
    DEPTH_TOLERANCE: int = Field(default=1, description="Circuit depth tolerance")
    SIMULATION_SIMILARITY_THRESHOLD: float = Field(
        default=0.95,
        description="Minimum similarity for simulation verification"
    )
    SIMULATION_SHOTS: int = Field(default=1000, description="Number of shots for quantum simulation")

    # Agent Configuration
    MAX_ITERATIONS: int = Field(default=3, description="Maximum refinement iterations")
    AGENT_VERBOSE: bool = Field(default=True, description="Enable verbose agent logging")
    ENABLE_MEMORY: bool = Field(default=True, description="Enable agent memory")

    # Dialect Configuration
    DEFAULT_DIALECT: str = Field(default="auto", description="Default MLIR dialect (auto, catalyst, quake)")

    # Backend Configuration
    QIR_RUNNER_PATH: Optional[str] = Field(default=None, description="Path to qir-runner executable")
    CATALYST_CLI_PATH: Optional[str] = Field(default=None, description="Path to catalyst-cli")
    ENABLE_QISKIT: bool = Field(default=True, description="Enable Qiskit simulator")
    ENABLE_CIRQ: bool = Field(default=False, description="Enable Cirq simulator")

    # HuggingFace (optional for some embeddings)
    HUGGINGFACE_TOKEN: Optional[str] = Field(default=None, description="HuggingFace API token")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_DIR: str = Field(default="logs", description="Log directory")
    ENABLE_FILE_LOGGING: bool = Field(default=True, description="Enable file logging")

    # Cache
    ENABLE_CACHE: bool = Field(default=True, description="Enable translation caching")
    CACHE_DIR: str = Field(default="data/cache", description="Cache directory")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
