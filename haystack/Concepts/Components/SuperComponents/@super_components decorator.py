"""
The new simplified method of creating a super components
As simple as decrating a class that contains self.pipeline
"""
from haystack import super_component, Pipeline, Document
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.joiners import DocumentJoiner
from haystack.components.retrievers import InMemoryEmbeddingRetriever, InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore

from datasets import load_dataset

@super_component
class HybridRetriever:
    def __init__(self, document_store: InMemoryDocumentStore,
                 embedder_model: str = "BAAI/bge-small-en-v1.5"):
        embedding_retriever = InMemoryEmbeddingRetriever(document_store)
        bm25_retriever = InMemoryBM25Retriever(document_store)
        text_embedder = SentenceTransformersTextEmbedder(embedder_model)
        document_joiner = DocumentJoiner()

        self.pipeline = Pipeline()
        self.pipeline.add_component("text_embedder", text_embedder)
        self.pipeline.add_component("embedding_retriever", embedding_retriever)
        self.pipeline.add_component("bm25_retriever", bm25_retriever)
        self.pipeline.add_component("document_joiner", document_joiner)

        self.pipeline.connect("text_embedder", "embedding_retriever")
        self.pipeline.connect("bm25_retriever", "document_joiner")
        self.pipeline.connect("embedding_retriever", "document_joiner")

dataset = load_dataset("HaystackBot/medrag-pubmed-chunk-with-embeddings", split="train")

docs = [Document(content=doc["contents"], embedding=doc["embedding"]) for doc in dataset]
document_store = InMemoryDocumentStore()
document_store.write_documents(docs)

query = "What treatments are available for chronic bronchitis?"

result = HybridRetriever(document_store).run(text=query, query=query)
print(result)