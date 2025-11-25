from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack_integrations.components.embedders.fastembed import (
FastembedSparseDocumentEmbedder,
FastembedSparseTextEmbedder
)

from milvus_haystack import MilvusDocumentStore, MilvusHybridRetriever

document_store = MilvusDocumentStore(
    connection_args={"uri": "./milvus.db"},
    drop_old=True,
    sparse_vector_field="sparse_vector",
)

documents = [
    Document(content="My name is Wolfgang and I live in Berlin"),
    Document(content="I saw a black horse running"),
    Document(content="Germany has many big cities"),
    Document(content="full text search is supported by Milvus."),
]

writer = DocumentWriter(document_store=document_store)

indexing_pipeline = Pipeline()
indexing_pipeline.add_component('sparse_doc_embedder', FastembedSparseDocumentEmbedder())
indexing_pipeline.add_component('dense_doc_embedder', SentenceTransformersDocumentEmbedder())
indexing_pipeline.add_component('writer', writer)
indexing_pipeline.connect('sparse_doc_embedder', "dense_doc_embedder")
indexing_pipeline.connect('dense_doc_embedder', "writer")

indexing_pipeline.run({"sparse_doc_embedder": {"documents": documents}})


retrieval_pipeline = Pipeline()
retrieval_pipeline.add_component("sparse_text_embedder",
                                FastembedSparseTextEmbedder())

retrieval_pipeline.add_component("dense_text_embedder", SentenceTransformersTextEmbedder())
retrieval_pipeline.add_component(
    "retriever",
    MilvusHybridRetriever(
        document_store=document_store,
        # reranker=WeightedRanker(0.5, 0.5),  # Default is RRFRanker()
    )
)

retrieval_pipeline.connect("sparse_text_embedder.sparse_embedding", "retriever.query_sparse_embedding")
retrieval_pipeline.connect("dense_text_embedder.embedding", "retriever.query_embedding")

question = "who supports full text search?"

results = retrieval_pipeline.run(
    {"dense_text_embedder": {"text": question},
     "sparse_text_embedder": {"text": question}}
)

print(results["retriever"]["documents"][0])
