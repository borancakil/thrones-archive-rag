import os
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

DATA_PATH = "books"
CHROMA_PATH = "chroma"

def generate_data_store():
    load_dotenv()
    if os.path.exists(CHROMA_PATH):
        print(f"Chroma database already exists at '{CHROMA_PATH}'. Skipping build.")
        return

    print("Chroma database not found. Building now...")
    
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} documents.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    
    if chunks:
        print("Example chunk:")
        print(chunks[0].page_content[:200], "...\n")
        print("Metadata:", chunks[0].metadata)

    embeddings = OpenAIEmbeddings()
    
    db = Chroma.from_documents(
        chunks, 
        embeddings, 
        persist_directory=CHROMA_PATH
    )
    print(f"✅ Saved {len(chunks)} chunks to Chroma at '{CHROMA_PATH}'.")

if __name__ == "__main__":
    generate_data_store()
