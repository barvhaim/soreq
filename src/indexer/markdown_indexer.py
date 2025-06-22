from typing import List, Optional
import logging
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from src.embeddings import get_embeddings_client

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarkdownIndexer:
    def __init__(self, docs_folder_path: str, vector_db: FAISS = None):
        self.docs_folder_path = docs_folder_path
        self.vector_db = vector_db

    def _load_documents(self, file_extension: str = ".md") -> List[Document]:
        docs = []
        for root, _, files in os.walk(self.docs_folder_path):
            for file in files:
                if file.endswith(file_extension):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        metadata = {
                            "source": file_path,
                            "filename": os.path.basename(file_path),
                        }

                        doc = Document(page_content=content, metadata=metadata)
                        docs.append(doc)
                    except Exception as e:
                        logger.error(f"Error loading document {file_path}: {e}")

        logger.info(f"Loaded {len(docs)} documents from {self.docs_folder_path}")
        return docs

    def index(self) -> Optional[str]:
        if not self.vector_db:
            raise ValueError("Vector database is not initialized.")

        docs = self._load_documents(file_extension=".md")

        headers_to_split_on = [
            ("#", "h1"),
            ("##", "h2"),
        ]
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            return_each_line=False,
            strip_headers=False,
        )

        chunks = []
        for doc in docs:
            doc_chunks = splitter.split_text(doc.page_content)
            for doc_chunk in doc_chunks:
                doc_chunk.metadata = {
                    **doc_chunk.metadata,
                    "source": doc.metadata["source"],
                    "filename": doc.metadata["filename"],
                }

            chunks.extend(doc_chunks)

        logger.info(f"Loaded {len(chunks)} document chunks")

        vector_store = self.vector_db.from_documents(
            documents=chunks,
            embedding=get_embeddings_client(),
        )

        vector_store.save_local(
            os.getenv("VECTOR_DB_PERSIST_DIRECTORY_MD", "md_faiss_db")
        )

        return f"Indexed {len(docs)} documents from {self.docs_folder_path} into {len(chunks)} chunks and saved to vector store."
