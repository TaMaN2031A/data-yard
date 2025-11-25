from haystack import Document, Pipeline
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack_integrations.components.embedders.fastembed import (
FastembedSparseDocumentEmbedder,
FastembedSparseTextEmbedder
)

from milvus_haystack import MilvusDocumentStore, MilvusSparseEmbeddingRetriever

document_store = MilvusDocumentStore(
    connection_args={"uri": "./milvus.db",},
    sparse_vector_field="sparse_vector",
    drop_old=True,
)

documents = [
    Document(content="My name is Wolfgang and I live in Berlin"),
    Document(content="I saw a black horse running"),
    Document(content="Germany has many big cities"),
    Document(content="full text search is supported by Milvus."),
]

sparse_document_embedder = FastembedSparseDocumentEmbedder()
writer = DocumentWriter(document_store)

pipeline = Pipeline()
pipeline.add_component("sparse_document_embedder", sparse_document_embedder)
pipeline.add_component("writer", writer)
pipeline.connect("sparse_document_embedder", "writer")

pipeline.run({"sparse_document_embedder": {"documents": documents}})

retrieval_pipeline = Pipeline()
retrieval_pipeline.add_component("sparse_text_embedder", FastembedSparseTextEmbedder())
retrieval_pipeline.add_component("sparse_retriever", MilvusSparseEmbeddingRetriever(document_store))
retrieval_pipeline.connect("sparse_text_embedder.sparse_embedding", "sparse_retriever.query_sparse_embedding")

query = "who supports full text search?"

results = retrieval_pipeline.run({"sparse_text_embedder": {"text": query}})

print(results)
print(results["sparse_retriever"]["documents"][0])
