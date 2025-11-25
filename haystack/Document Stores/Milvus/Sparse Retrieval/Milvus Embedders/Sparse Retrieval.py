"""
Works only for Milvus server modeg
"""

from haystack import Document, Pipeline
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy

from milvus_haystack import MilvusDocumentStore, MilvusSparseEmbeddingRetriever
from milvus_haystack.function import BM25BuiltInFunction

document_store = MilvusDocumentStore(
    connection_args={"uri": "./milvus.db"},
    sparse_vector_field="sparse_vector",
    text_field="text",
    builtin_function=[
        BM25BuiltInFunction(
            input_field_names="text", output_field_names="sparse_vector"
        )
    ], drop_old=True,
)
documents = [
    Document(content="My name is Wolfgang and I live in Berlin"),
    Document(content="I saw a black horse running"),
    Document(content="Germany has many big cities"),
    Document(content="full text search is supported by Milvus."),
]
writer = DocumentWriter(document_store=document_store)
indexing_pipeline = Pipeline()
indexing_pipeline.add_component("writer", writer)
indexing_pipeline.run({"writer": {"documents": documents}})

retrieval_pipeline = Pipeline()
retrieval_pipeline.add_component("sparse_retriever", MilvusSparseEmbeddingRetriever(document_store))
query = "who supports full text search?"
result = retrieval_pipeline.run({"sparse_retriever": {"query_text": query}})
print(result["sparse_retriever"]["documents"][0])