import os
import sys
import sqlite3
import sqlite_vec
import struct
import numpy as np
from tqdm import tqdm
from typing import List
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer

def serialize(vector: List[float]) -> bytes:
    """Serializes a list or numpy array of floats into a compact "raw bytes" format."""
    return struct.pack(f"{len(vector)}f", *vector)

def deserialize(blob: bytes) -> List[float]:
    """Deserializes bytes back into a list of floats."""
    return list(struct.unpack(f"{len(blob)//4}f", blob))

def load_documents(folder_path):
    documents = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            # Only process text files; you can expand this to other types as needed
            if filename.lower().endswith(('.txt', '.md', '.py', '.json', '.csv')):
                try:
                    loader = TextLoader(file_path)
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata['source'] = file_path  # Add source to metadata
                    documents.extend(docs)
                except Exception as e:
                    print(f"Could not load {file_path}: {e}")
    return documents

def main():
    # Get folder path from user
    folder_path = input("Enter the folder path containing documents: ").strip()
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        sys.exit(1)

    # Load documents
    print("Loading documents...")
    documents = load_documents(folder_path)
    if not documents:
        print("No valid documents found in the specified folder.")
        sys.exit(1)

    # Split documents into chunks
    print("Splitting documents into chunks...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Prepare data for database insertion
    contents = []
    sources = []
    embeddings = []
    print("Creating embeddings...")
    for doc in tqdm(docs):
        text = doc.page_content
        source = doc.metadata.get('source', 'Unknown')
        embedding = model.encode(text).astype(np.float32)
        contents.append(text)
        sources.append(source)
        embeddings.append(serialize(embedding))

    # Initialize SQLite database with sqlite-vec
    db = sqlite3.connect('documents.db')
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)

    # Drop existing tables (optional)
    db.execute("DROP TABLE IF EXISTS documents;")
    db.execute("DROP TABLE IF EXISTS vec_documents;")

    # Create tables
    db.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            content TEXT,
            source TEXT
        );
    """)

    # Specify FLOAT[384] to match the 384-dimensional embedding size
    db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_documents USING vec0(
            id INTEGER PRIMARY KEY,
            content_embedding FLOAT[384]
        );
    """)

    # Insert data into tables
    print("Inserting data into database...")
    with db:
        for idx, (content, source, embedding) in enumerate(zip(contents, sources, embeddings)):
            db.execute("INSERT INTO documents(id, content, source) VALUES(?, ?, ?)", (idx, content, source))
            db.execute("INSERT INTO vec_documents(id, content_embedding) VALUES(?, ?)", (idx, embedding))

    print("Setup complete. You can now query your documents.")

    # Prompt user for query
    while True:
        query = input("\nEnter your question (or 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            break

        # Compute embedding for the query
        query_embedding = model.encode(query).astype(np.float32)
        query_embedding_serialized = serialize(query_embedding)

        # Retrieve similar documents
        results = db.execute("""
            SELECT
                documents.id,
                distance,
                content,
                source
            FROM vec_documents
            LEFT JOIN documents ON documents.id = vec_documents.id
            WHERE content_embedding MATCH ?
                             AND k = 3
            ORDER BY distance LIMIT 5;
        """, (query_embedding_serialized,)).fetchall()

        if results:
            for result in results:
                doc_id, distance, content, source = result
                print(f"\nFound in: {source}")
                print(f"Similarity Score: {distance}")
                print(f"Content Snippet:\n{content[:500]}")
                print("-" * 50)
        else:
            print("No relevant documents found.")

    db.close()

if __name__ == "__main__":
    main()