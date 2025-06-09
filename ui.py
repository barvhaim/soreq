import os
from dotenv import load_dotenv
import streamlit as st
from src.retriever.markdown_retriever import MarkdownRetriever
from src.augmentation.markdown_augmenter import MarkdownAugmenter
from src.indexer.markdown_indexer import MarkdownIndexer
from src.vector_db import get_vector_db


load_dotenv()

st.set_page_config(
    page_title="Documentation Q&A",
    page_icon="📚",
    layout="centered",
)

MD_DOCS_FOLDER_PATH = os.getenv("DOCS_FOLDER_PATH", "data")


@st.cache_resource
def load_rag():
    """Load the RAG components."""
    return MarkdownRetriever(), MarkdownAugmenter()


with st.sidebar:
    st.header("Settings")

    def refresh_vector_db():
        with st.spinner("Refreshing documents DB..."):
            try:
                vector_db = get_vector_db()
                indexer = MarkdownIndexer(
                    docs_folder_path=MD_DOCS_FOLDER_PATH, vector_db=vector_db
                )
                indexer.index()
                # Clear the cache to reload the retriever with updated index
                load_rag.clear()
                st.success("Documents DB refreshed successfully!")
                return True
            except Exception as e:
                st.error(f"Error refreshing documents DB: {str(e)}")
                return False

    st.text("Using documents from:")
    st.markdown("_" + MD_DOCS_FOLDER_PATH + "_")

    if st.button("Refresh documents DB"):
        refresh_result = refresh_vector_db()

st.title("Soreq: Q&A over documentation")
st.markdown(
    """
    This application uses a Retrieval-Augmented Generation (RAG) approach to answer your queries.
    
    **Note:** Ensure that the documents are indexed before asking questions. You can refresh the index from the sidebar.
"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

retriever, augmenter = load_rag()


def process_query(q: str) -> str:
    try:
        context = retriever.retrieve(query=q, k=1)
        result = augmenter.augment(query=q, context=context)
        return result if result else "No relevant information found."
    except Exception as e:
        return f"An error occurred while processing your query: {e}"


query = st.chat_input("Ask a question about the documentation")
if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        response = process_query(query)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
