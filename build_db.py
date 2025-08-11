import os
import glob
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
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

    # Hafif loader: 'unstructured' bağımlılığını tetiklememek için md dosyalarını düz metin olarak yükle
    documents: list[Document] = []
    for path in glob.glob(os.path.join(DATA_PATH, "*.md")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append(Document(page_content=text, metadata={"source": os.path.basename(path)}))
        except Exception as e:
            print(f"Warn: could not read {path}: {e}")
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
