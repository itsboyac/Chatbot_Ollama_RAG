import streamlit as st
"""
This script implements a Streamlit-based Q&A application about cats using a Retrieval-Augmented Generation (RAG) approach. 
It integrates the following components:
1. **Streamlit**: Provides the user interface for the application.
2. **LangChain Ollama**: Used for embeddings and language model (LLM) functionalities.
3. **Chroma**: A vector database for storing and retrieving document embeddings.
Key Functionalities:
- **Resource Loading**: The `load_resources` function initializes and caches the embeddings, vector database, and language model.
- **Document Retrieval**: The `get_sources` function retrieves the top 3 most relevant documents from the vector database based on the user's query and formats their metadata as sources.
- **Prompt Template**: A predefined template is used to structure the context and question for the language model.
- **RAG Chain**: A pipeline that retrieves relevant documents, formats them, applies the prompt template, and generates an answer using the language model.
- **User Interaction**: The app allows users to input questions about cats via a chat interface. The system responds with an answer and displays the sources used to generate the response.
The application is designed to provide accurate and contextually relevant answers about cats, leveraging the power of embeddings, vector search, and a language model.
"""
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
st.title("🐱 Cat Q&A")

@st.cache_resource
def load_resources():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_db = Chroma(persist_directory="data/vectorstore", embedding_function=embeddings)
    llm = OllamaLLM(model="llama3.2")
    return embeddings, vector_db, llm
embeddings, vector_db, llm = load_resources()

def get_sources(query):
    docs = vector_db.similarity_search(query, k=3)
    sources = []
    for doc in docs:
        sources.append(f"- {doc.metadata.get('title')} ({doc.metadata.get('url')})")
    return "\n".join(set(sources)) 


template = """Use the following pieces of context to answer the question. 
{context}
Question: {question}
Answer:"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": vector_db.as_retriever() | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


query = st.chat_input("Ask a question about cats.", accept_file=False)

if query:
    with st.chat_message("user"):
        st.markdown(query)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = rag_chain.invoke(query)
            sources = get_sources(query)
            st.markdown(answer)
            st.info(f"Sources:\n{sources}")

