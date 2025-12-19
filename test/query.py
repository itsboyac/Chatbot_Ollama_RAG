from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_db = Chroma(persist_directory="data/vectorstore", embedding_function=embeddings)
llm = OllamaLLM(model="llama3.2")

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

query = "How can I help my aging cat?"
print(f"Querying: {query}...\n")
answer = rag_chain.invoke(query)
sources = get_sources(query)

print("--- Response ---")
print(answer)
print("\n--- Source Links ---")
print(sources)