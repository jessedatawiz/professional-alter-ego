from pathlib import Path

from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


class KnowledgeBase:

    def __init__(
        self,
        docs_dir: str,
        qdrant_path: str,
        collection_name: str,
        embedding_model: str,
        top_k: int = 4,
        rebuild: bool = False,
    ):
        self.top_k = top_k
        Settings.embed_model = OpenAIEmbedding(model=embedding_model)
        Settings.llm = None

        Path(qdrant_path).mkdir(parents=True, exist_ok=True)
        client = QdrantClient(path=qdrant_path)

        if rebuild and client.collection_exists(collection_name):
            client.delete_collection(collection_name)

        vector_store = QdrantVectorStore(
            client=client, collection_name=collection_name
        )
        self.index = self._build_or_load(vector_store, client, collection_name, docs_dir)

    def _build_or_load(self, vector_store, client, collection_name, docs_dir):
        has_data = (
            client.collection_exists(collection_name)
            and client.count(collection_name).count > 0
        )
        if has_data:
            return VectorStoreIndex.from_vector_store(vector_store)

        documents = SimpleDirectoryReader(docs_dir).load_data()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )

    def retrieve(self, query: str, top_k: int | None = None) -> str:
        retriever = self.index.as_retriever(
            similarity_top_k=top_k or self.top_k
        )
        nodes = retriever.retrieve(query)
        return "\n\n---\n\n".join(node.get_content() for node in nodes)
