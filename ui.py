import streamlit as st
from src.retriever.markdown_retriever import MarkdownRetriever
from src.augmentation.markdown_augmenter import MarkdownAugmenter


st.set_page_config(
    page_title="Documentation Q&A",
    page_icon="📚",
    layout="centered",
)

st.title("Documentation Q&A System")
st.markdown(
    """
Ask questions about the documentation and get answers based on the content.
"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


@st.cache_resource
def load_rag():
    """Load the RAG components."""
    return MarkdownRetriever(), MarkdownAugmenter()

retriever, augmenter = load_rag()


def process_query(query) -> str:
    try:
        context = retriever.retrieve(query=query, k=2)
        result = augmenter.augment(query=query, context=context)
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
