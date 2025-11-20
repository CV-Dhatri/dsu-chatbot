import os
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# --- CONFIGURATION ---
# No API key is needed here because we are using free local embeddings!

def main():
    # 1. Load your knowledge base
    print("Loading knowledge base...")
    try:
        loader = TextLoader("knowledge.txt", encoding="utf-8")
        documents = loader.load()
    except Exception as e:
        print(f"Error loading knowledge.txt: {e}")
        return

    # 2. Split the documents into chunks
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    # 3. Create embeddings and store in Chroma
    print("Creating embeddings and storing in vector database...")
    print("(This involves downloading a small model the first time, so please wait...)")
    
    # We use the 'all-MiniLM-L6-v2' model. It's fast, free, and runs on your laptop.
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create the database in the ./db folder
    db = Chroma.from_documents(docs, embedding_function, persist_directory="./db")

    print("--------------------------------------------------")
    print(f"Successfully added {len(docs)} document chunks to the database.")
    print("Your 'brain' is ready! You can now run app.py.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# --- CONFIGURATION ---
# No API key is needed here because we are using free local embeddings!

def main():
    # 1. Load your knowledge base
    print("Loading knowledge base...")
    try:
        loader = TextLoader("knowledge.txt", encoding="utf-8")
        documents = loader.load()
    except Exception as e:
        print(f"Error loading knowledge.txt: {e}")
        return

    # 2. Split the documents into chunks
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    # 3. Create embeddings and store in Chroma
    print("Creating embeddings and storing in vector database...")
    print("(This involves downloading a small model the first time, so please wait...)")
    
    # We use the 'all-MiniLM-L6-v2' model. It's fast, free, and runs on your laptop.
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create the database in the ./db folder
    db = Chroma.from_documents(docs, embedding_function, persist_directory="./db")

    print("--------------------------------------------------")
    print(f"Successfully added {len(docs)} document chunks to the database.")
    print("Your 'brain' is ready! You can now run app.py.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()