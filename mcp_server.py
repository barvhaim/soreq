import logging
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from src.indexer.markdown_indexer import MarkdownIndexer
from src.retriever.markdown_retriever import MarkdownRetriever
from src.augmentation.markdown_augmenter import MarkdownAugmenter
from src.vector_db import get_vector_db

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
mcp = FastMCP("Soreq")


@mcp.tool(
    name="sync_project_docs",
    description="Synchronizes the project documentation with the latest changes.",
)
def sync_project_docs() -> str:
    """
    Synchronizes the project documentation by indexing Markdown files.

    :returns: A message indicating the synchronization status.
    """
    md_docs_folder_path = os.getenv("DOCS_FOLDER_PATH")
    vector_db = get_vector_db()
    logger.info(f"Vector database initialized: {vector_db}")

    indexer = MarkdownIndexer(docs_folder_path=md_docs_folder_path, vector_db=vector_db)
    try:
        return indexer.index()
    except Exception as e:
        return f"Error during project synchronization: {str(e)}"


@mcp.tool(
    name="query_project_docs",
    description="Queries the project documentation.",
)
def query_project_docs(query: str) -> str:
    """
    Queries the project documentation, retrieving relevant context based on the provided query and answers it.

    :param query: The query string to search for in the documentation.
    :returns: A string containing the answer based on the retrieved context.
    """
    if not query:
        return "Query cannot be empty."

    retriever = MarkdownRetriever()
    context = retriever.retrieve(query=query, k=2)

    if not context:
        return f"No relevant context found for query: '{query}'"

    augmenter = MarkdownAugmenter()
    return augmenter.augment(query=query, context=context)


if __name__ == "__main__":
    # mcp.run()
    mcp.run(transport="sse", host="0.0.0.0", port=5555)
