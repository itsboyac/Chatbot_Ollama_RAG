# 🐱 Chatbot for Cats Questions! (RAG)

A local Retrieval-Augmented Generation (RAG) chatbot that answers questions about cats using data scraped from *The Conversation*. This project demonstrates how to build a privacy-focused, local AI application using **Ollama**, **LangChain**, **ChromaDB**, and **Streamlit**.

## 📊 Data Source

The data for this project is sourced from **[The Conversation](https://theconversation.com/europe/search?q=cat)**.
- **Source**: Public articles tagged with "cat" from the European edition.
- **Content**: We scrape raw HTML pages, parse them to extract article text and metadata (title, URL), and use this as the knowledge base for the chatbot.

## 🛠️ Project Structure & Scripts

The project is divided into a data processing pipeline and a frontend application.

### 1. Data Collection & Processing
The `src/` directory contains scripts to build the vector database:

- **`src/scrape_data.py`**
  - **Purpose**: Crawls multiple search result pages from *The Conversation* and downloads individual article HTML files.
  - **Output**: Saves raw HTML files to `data/raw/`.

- **`src/parse_data.py`**
  - **Purpose**: Reads the raw HTML files, parses them with BeautifulSoup to extract clean text and titles, and removes duplicates.
  - **Output**: Saves a consolidated CSV file to `data/processed/cat_articles.csv`.

- **`src/clean_then_store.py`**
  - **Purpose**: 
    1. Loads the CSV data.
    2. Splits logic text into smaller chunks (using `RecursiveCharacterTextSplitter`).
    3. Generates embeddings using **Ollama** (`nomic-embed-text`).
    4. Stores the embeddings and metadata in a local **ChromaDB** vector store.
  - **Output**: Creates/Updates the vector store in `data/vectorstore/`.

### 2. Application
- **`src/streamlit.py`**
  - **Purpose**: The main application script. It connects to the existing ChromaDB, sets up the RAG chain with LangChain, and provides a chat interface.
  - **Function**: When you ask a question, it retrieves the most relevant document chunks and uses the **Llama 3.2** model to generate an answer with sources.

## 🧰 Technology Stack

- **[Ollama](https://ollama.com/)**: A robust tool to run open-source LLMs locally. We use it for both the generation model (`llama3.2`) and the embedding model (`nomic-embed-text`).
- **[LangChain](https://www.langchain.com/)**: The framework used to stitch together the retrieval and generation steps. It handles the "RAG" logic.
- **[ChromaDB](https://www.trychroma.com/)**: A fast, open-source embedding database that runs locally (no cloud account required). It stores our "knowledge" about cats.
- **[Streamlit](https://streamlit.io/)**: Turns our Python script into a sharable web app with a chat interface in just a few lines of code.

## 🚀 Installation & Setup

### Prerequisites
1. **Install Ollama**: Download and install from [ollama.com](https://ollama.com/).
2. **Pull Models**: Open your terminal/command prompt and run:
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```
3. **Install Poetry**: This project uses Poetry for dependency management. If you don't have it, install it (or standard pip if you prefer).

### Project Setup
1. Clone this repository.
2. Install dependencies:
   ```bash
   poetry install
   ```
   *Note: If not using Poetry, you can install the packages listed in `pyproject.toml` manually via pip.*

## 🏃 Usage

You can use the included `Makefile` to run steps easily, or run commands directly.

### 1. Build the Database (First Run Only)
If you are running this for the first time, you need to scrape data and build the vector store:

```bash
# Run all data steps in order
make scrape_data
make parse_data
make process_data
```

Or manually:
```bash
poetry run python src/scrape_data.py
poetry run python src/parse_data.py
poetry run python src/clean_then_store.py
```

### 2. Run the Chatbot
To start the web interface:

```bash
# Using Makefile
make app
```

**OR** (Recommended standard command):
```bash
poetry run streamlit run src/streamlit.py
```

Once the command runs, a local URL (usually `http://localhost:8501`) will appear. Open it in your browser to start chatting with the ✨ **Cat Q&A** ✨ bot!
![alt text](image-1.png)

---
*Created for the purpose of demonstrating a local RAG pipeline.*
