import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# initialise the model selected
def initialize_model(model_name: str = 'all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    return model

# create the embeddings
def create_embeddings(model, docs):
    contents = []
    sources = []
    embeddings = []
    for doc in tqdm(docs, desc="Creating embeddings"):
        text = doc.page_content
        source = doc.metadata.get('source', 'Unknown')
        embedding = model.encode(text).astype(np.float32)
        contents.append(text)
        sources.append(source)
        embeddings.append(embedding)
    return contents, sources, embeddings