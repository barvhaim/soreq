from typing import List, Dict, Optional
import logging
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.llm import get_chat_llm_client

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarkdownAugmenter:
    def __init__(self):
        self.llm = get_chat_llm_client(
            model_parameters={
                "temperature": 0.05,
                "top_p": 0.5,
                "max_tokens": 1000,
            }
        )

    @staticmethod
    def _build_context(context: List[Dict]) -> str:
        if not context:
            return "No relevant context found."

        context_str = "\n".join(
            [f"{i + 1}. {doc['content']}" for i, doc in enumerate(context)]
        )
        return context_str

    def augment(self, query: str, context: List[Dict]) -> Optional[str]:
        task = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer: """

        prompt = ChatPromptTemplate([("user", task)])

        context_str = self._build_context(context)

        chain = prompt | self.llm | StrOutputParser()

        try:
            result = chain.invoke({"question": query, "context": context_str})
            return result.strip()
        except Exception as e:
            logger.error(f"Error during augmentation: {e}")

        return None
