import logging
import os
from typing import List, Dict, Optional
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from src.embeddings import get_embeddings_client

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarkdownRetriever:
    def __init__(self):
        self.vector_db = self.load_vector_db()

    @staticmethod
    def load_vector_db():
        """Load the FAISS vector database from disk."""
        try:
            embeddings = get_embeddings_client()
            vector_db = FAISS.load_local(
                folder_path=os.getenv("VECTOR_DB_PERSIST_DIRECTORY_MD", "md_faiss_db"),
                embeddings=embeddings,
                allow_dangerous_deserialization=True,
            )
            return vector_db
        except Exception as e:
            logger.error(f"Error loading vector database: {e}")
            return None

    def retrieve(self, query, k=3) -> Optional[List[Dict]]:
        if not self.vector_db:
            raise ValueError("Vector database is not initialized.")

        try:
            docs_and_scores = self.vector_db.similarity_search_with_score(query, k=k)
            if not docs_and_scores:
                logger.warning("No documents found for the query.")
                return None

            results = []
            for doc, score in docs_and_scores:
                results.append(
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "score": score,
                    }
                )
            return results
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return None
