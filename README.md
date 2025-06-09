# Soreq - Your enterprise's knowledge-base AI agent

<img width="571" alt="Image" src="https://github.com/user-attachments/assets/7f3889f1-a0b0-492d-9e90-8d8d78c44525" />

Soreq is an AI agent designed to help enterprises manage and utilize their knowledge base effectively. It can answer questions, provide insights, and assist in decision-making by leveraging the information stored within the organization's knowledge base.

## Features
- **Q&A over documentation**: Ask questions and get answers based on code project's documentation.

## **Getting Started**

### 📦 Installation
1. Install Python 3.11 or later. (https://www.python.org/downloads/)
2. Install `uv` package manager (https://docs.astral.sh/uv/getting-started/installation/)
    - For Linux and MacOS, you can use the following command:
       ```bash
       curl -LsSf https://astral.sh/uv/install.sh | sh
       ```
    - For Windows, you can use the following command:
       ```bash
       powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
       ```
3. Install `Ollama` and download the required models:
    - Follow the instructions at [Ollama Installation](https://ollama.com).
    - Download the models:
      ```bash
      ollama pull llama3.1:8b
      ollama pull mxbai-embed-large
      ```
4. Clone the project repository and navigate to the project directory.
    ```bash
   git clone https://github.com/barvhaim/soreq.git
   cd soreq
    ```
5. Configure the `.env` file based on `.env.sample` file.
    ```bash
    cp .env.sample .env
    ```
   
    - `DOCS_FOLDER_PATH` = The path to your code project's documentation folder.
    - `LLM_PROVIDER` = The LLM provider to use (e.g., `ollama`).
    - `MODEL_NAME` = The name of the model to use (e.g., `llama3.1:8b`).
    - `EMBEDDING_MODEL_NAME` = The name of the embedding model to use (e.g., `mxbai-embed-large`).

### Usage
1. Run the application:
    ```bash
    uv run streamlit run ui.py
    ```
2. Soreq will start a Streamlit application, which you can access in your web browser at [http://localhost:8501](http://localhost:8501).