import logging
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from src.embeddings import get_embeddings_client

logging.basicConfig(level=logging.INFO)


_index = faiss.IndexFlatL2(len(get_embeddings_client().embed_query("test")))


def get_vector_db() -> FAISS:
    """Initialize and return the FAISS vector database."""
    try:
        return FAISS(
            embedding_function=get_embeddings_client(),
            index=_index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
    except Exception as e:
        logging.error(f"Failed to initialize vector database: {e}")
        raise
