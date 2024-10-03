# main.py

import sys
import os
import yaml
from src import data_loader, embedding, database, query

def main():
    # load config
    config_path = os.path.join('configs', 'config.yaml')
    if not os.path.isfile(config_path):
        print(f"Configuration file not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # read configs with defaults
    folder_path = config.get('data_folder')
    db_file = config.get('db_file', 'documents.db')
    model_name = config.get('model_name', 'all-MiniLM-L6-v2')
    chunk_size = config.get('chunk_size', 1000)
    chunk_overlap = config.get('chunk_overlap', 100)
    file_extensions = config.get('file_extensions', ['.txt', '.md', '.py', '.json', '.csv', '.pdf'])
    k = config.get('k', 3)

    print(f"Using embedding model: {model_name}")
    print(f"Supported file extensions: {file_extensions}")
    print(f"Number of results to retrieve (k): {k}")

    if not folder_path:
        print("Error: 'data_folder' not set in config.yaml.")
        sys.exit(1)

    # check if data folder exists
    if not os.path.isdir(folder_path):
        print(f"Invalid data folder path: {folder_path}")
        sys.exit(1)

    # load docs
    print("Loading documents...")
    documents = data_loader.load_documents(folder_path, file_extensions)
    if not documents:
        print("No valid documents found in the specified folder.")
        sys.exit(1)

    # split documents into chunks
    print("Splitting documents into chunks...")
    docs = data_loader.split_documents(documents, chunk_size, chunk_overlap)

    # initialize embedding model
    model = embedding.initialize_model(model_name)

    # create embeddings
    contents, sources, embeddings = embedding.create_embeddings(model, docs)

    # initialize database
    db = database.initialize_database(db_file, embedding_dim=embeddings[0].shape[0])

    # insert data into database
    database.insert_data(db, contents, sources, embeddings)

    print("Setup complete. You can now query your documents.")

    # prompt user for query
    while True:
        query_text = input("\nEnter your question (or 'exit' to quit): ").strip()
        if query_text.lower() == 'exit':
            break

        # query the database
        results = query.query_database(db, model, query_text, k=k)

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