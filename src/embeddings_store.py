from langchain_huggingface import HuggingFaceEmbeddings
from src.config import Config
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_core.documents import Document
from typing import List

def get_embeddings_model():
    return HuggingFaceEmbeddings(model_name=Config.EMBEDDINGS_MODEL)

def create_qdrant_client():
    return QdrantClient(
        url=Config.QDRANT_URL,
        api_key=Config.QDRANT_API_KEY or None
    )

def upsert_documents_to_qdrant(docs: List[Document], collection_name: str = None):
    collection_name = collection_name or Config.QDRANT_COLLECTION_NAME
    # Filter out empty chunks that would cause embedding generation to return []
    non_empty_docs = [d for d in docs if getattr(d, 'page_content', '') and d.page_content.strip()]
    if not non_empty_docs:
        raise ValueError("No textual content found in the uploaded PDF to index.")
    embeddings = get_embeddings_model()
    client = create_qdrant_client()

    # Ensure collection exists with correct vector size
    try:
        client.get_collection(collection_name)
    except Exception:
        vector_dim = len(embeddings.embed_query("dimension_probe"))
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE),
        )
    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )
    vectorstore.add_documents(non_empty_docs)
    return vectorstore

def get_qdrant_vectorstore(collection_name: str = None):
    collection_name = collection_name or Config.QDRANT_COLLECTION_NAME
    embeddings = get_embeddings_model()
    client = create_qdrant_client()

    # Create empty collection if it doesn't exist to avoid 404 on first query
    try:
        client.get_collection(collection_name)
    except Exception:
        vector_dim = len(embeddings.embed_query("dimension_probe"))
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE),
        )

    qdrant = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )
    return qdrant


