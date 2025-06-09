import os
from enum import Enum
from typing import Dict, Optional, Any
from dotenv import load_dotenv

load_dotenv()


class LLMProviderType(Enum):
    OLLAMA = "ollama"


LLM_PROVIDER = LLMProviderType(os.getenv("LLM_PROVIDER", LLMProviderType.OLLAMA.value))


def _get_base_llm_settings(model_name: str, model_parameters: Optional[Dict]) -> Dict:
    if model_parameters is None:
        model_parameters = {}

    if LLM_PROVIDER == LLMProviderType.OLLAMA:
        parameters = {
            "temperature": model_parameters.get("temperature", 0.05),
            "top_k": model_parameters.get("top_k", 50),
            "top_p": model_parameters.get("top_p", 1.0),
            "num_predict": model_parameters.get("max_tokens", 500),
            "stop": model_parameters.get("stop_sequences", []),
            "repeat_penalty": model_parameters.get("repetition_penalty", 1.0),
        }

        return {
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            "model": model_name,
            **parameters,
        }

    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")


def get_chat_llm_client(
    model_parameters: Optional[Dict] = None,
) -> Any:
    model_name = os.getenv("MODEL_NAME", "llama3.1:8b")

    if LLM_PROVIDER == LLMProviderType.OLLAMA:
        from langchain_ollama import ChatOllama

        return ChatOllama(
            **_get_base_llm_settings(
                model_name=model_name, model_parameters=model_parameters
            )
        )

    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")
