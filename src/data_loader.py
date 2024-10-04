import os
from typing import List
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

# function for loading the relevant documents and ensure right file extension
def load_documents(folder_path: str, file_extensions: List[str]) -> List[Document]:
    documents = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext in file_extensions:
                try:
                    if ext == '.pdf':
                        loader = PyPDFLoader(file_path)
                    else:
                        loader = TextLoader(file_path)
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata['source'] = file_path  # Add source to metadata
                    documents.extend(docs)
                except Exception as e:
                    print(f"Could not load {file_path}: {e}")
    return documents


# function for splitting docs into configured chunk sizes
def split_documents(documents: List[Document], chunk_size: int, chunk_overlap: int) -> List[Document]:
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs