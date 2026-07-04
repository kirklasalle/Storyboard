try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

from typing import List, Dict, Any, Optional
import os

class MemoryService:
    def __init__(self, persist_directory: str = "./backend/vector_store"):
        if not CHROMA_AVAILABLE:
            print("Warning: chromadb not installed. MemoryService will be disabled.")
            self.collection = None
            return
            
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.text_ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="project_memory",
            embedding_function=self.text_ef
        )

    def add_item(self, id: str, content: str, metadata: Dict[str, Any]):
        if not self.collection:
            return
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[id]
        )

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        if not self.collection:
            return []
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
