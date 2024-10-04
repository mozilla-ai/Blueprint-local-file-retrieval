from src.utils import serialize
import numpy as np



def query_database(db, model, query: str, k: int = 5):
    # compute embedding for the query
    query_embedding = model.encode(query).astype(np.float32)
    query_embedding_serialized = serialize(query_embedding)

    # retrieve similar documents
    results = db.execute(f"""
        SELECT
            documents.id,
            distance,
            content,
            source
        FROM vec_documents
        LEFT JOIN documents ON documents.id = vec_documents.id
        WHERE content_embedding MATCH ?
            AND k = ?
        ORDER BY distance LIMIT ?;
    """, (query_embedding_serialized, k, k)).fetchall()

    return results