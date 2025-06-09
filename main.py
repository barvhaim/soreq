import logging
import os
from dotenv import load_dotenv
from src.vector_db import get_vector_db
from src.indexer.markdown_indexer import MarkdownIndexer
from src.retriever.markdown_retriever import MarkdownRetriever
from src.augmentation.markdown_augmenter import MarkdownAugmenter

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    md_docs_folder_path = os.getenv("DOCS_FOLDER_PATH")
    vector_db = get_vector_db()
    logger.info(f"Vector database initialized: {vector_db}")

    indexer = MarkdownIndexer(docs_folder_path=md_docs_folder_path, vector_db=vector_db)
    indexer.index()

    query = "How to update the swagger?"

    retriever = MarkdownRetriever()
    context = retriever.retrieve(query=query, k=2)

    logger.info(f"Retrieved context for query '{query}': {len(context)}")

    augmenter = MarkdownAugmenter()
    result = augmenter.augment(query=query, context=context)

    logger.info(f"Augmentation result: {result}")


if __name__ == "__main__":
    main()
