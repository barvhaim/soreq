import os
from enum import Enum
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class EmbeddingsProviderType(Enum):
    OLLAMA = "ollama"


EMBEDDINGS_PROVIDER = EmbeddingsProviderType(
    os.getenv("EMBEDDINGS_PROVIDER", EmbeddingsProviderType.OLLAMA.value)
)


def _get_base_llm_settings(model_name: str) -> Dict:
    if EMBEDDINGS_PROVIDER == EmbeddingsProviderType.OLLAMA:
        return {
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            "model": model_name,
        }

    raise ValueError(f"Unsupported embeddings provider: {EMBEDDINGS_PROVIDER}")


def get_embeddings_client() -> Any:
    model_name = os.getenv("EMBEDDING_MODEL_NAME", "mxbai-embed-large")

    if EMBEDDINGS_PROVIDER == EmbeddingsProviderType.OLLAMA:
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(**_get_base_llm_settings(model_name=model_name))

    raise ValueError(f"Unsupported embeddings provider: {EMBEDDINGS_PROVIDER}")
