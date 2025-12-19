from langchain_ollama import OllamaEmbeddings 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma 
import pandas as pd
import os
from tqdm import tqdm

df = pd.read_csv("data/processed/cat_articles.csv")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

documents = []
metadata = []

for _, row in tqdm(df.iterrows(), total=len(df)):
    if pd.isna(row['content']):
        continue
        
    chunks = text_splitter.split_text(row['content'])
    for chunk in chunks:
        documents.append(chunk)
        metadata.append({
            "title": row['title'],
            "url": row['url']
        })

os.makedirs("data/vectorstore", exist_ok=True)
vector_db = Chroma.from_texts(
    texts=documents,
    embedding=OllamaEmbeddings(model="nomic-embed-text"), 
    persist_directory="data/vectorstore",
    metadatas=metadata
)

print(f"Created vector store with {len(documents)} documents.")