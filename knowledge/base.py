import os
from dotenv import load_dotenv
load_dotenv()
from llama_index.core import VectorStoreIndex, Document, StorageContext, load_index_from_storage
from typing import List

class KnowledgeBase:
    def __init__(self, storage_dir: str = "./data/storage"):
        self.storage_dir = storage_dir
        self.index = None
        self._initialize_index()

    def _initialize_index(self):
        if os.path.exists(self.storage_dir):
            storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)
            self.index = load_index_from_storage(storage_context)
        else:
            # Initialize with empty index if no storage exists
            self.index = VectorStoreIndex([])

    def add_documents(self, texts: List[str]):
        documents = [Document(text=t) for t in texts]
        for doc in documents:
            self.index.insert(doc)
        self.index.storage_context.persist(persist_dir=self.storage_dir)

    def query(self, query_str: str, similarity_top_k: int = 3):
        query_engine = self.index.as_query_engine(similarity_top_k=similarity_top_k)
        response = query_engine.query(query_str)
        return str(response)

# Singleton instance for simplicity in this demo
kb = KnowledgeBase()
