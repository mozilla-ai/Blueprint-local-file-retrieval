
import sqlite3
import sqlite_vec
from .utils import serialize

def initialize_database(db_file: str, embedding_dim: int = 384):
    db = sqlite3.connect(db_file)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)

    # drop existing tables (optional) - added as there can be an error if already exists
    db.execute("DROP TABLE IF EXISTS documents;")
    db.execute("DROP TABLE IF EXISTS vec_documents;")

    # create tables
    db.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            content TEXT,
            source TEXT
        );
    """)

    db.execute(f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_documents USING vec0(
            id INTEGER PRIMARY KEY,
            content_embedding FLOAT[{embedding_dim}]
        );
    """)

    return db


def insert_data(db, contents, sources, embeddings):
    print("Inserting data into database...")
    with db:
        for idx, (content, source, embedding) in enumerate(zip(contents, sources, embeddings)):
            db.execute("INSERT INTO documents(id, content, source) VALUES(?, ?, ?)", (idx, content, source))
            db.execute("INSERT INTO vec_documents(id, content_embedding) VALUES(?, ?)", (idx, serialize(embedding)))