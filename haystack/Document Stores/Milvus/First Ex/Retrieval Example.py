import glob
import os

from haystack import Pipeline
from haystack.components.converters import TextFileToDocument
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter

from milvus_haystack import MilvusDocumentStore
from milvus_haystack.milvus_embedding_retriever import MilvusEmbeddingRetriever

question = "Give me an example of git usage"
document_store = MilvusDocumentStore(
    connection_args={"uri": "./milvus.db"},
)
retrieval = Pipeline()
retrieval.add_component('embedder', SentenceTransformersTextEmbedder())
retrieval.add_component('retriever', MilvusEmbeddingRetriever(document_store=document_store, top_k=3))
retrieval.connect('embedder', 'retriever')

result = retrieval.run({"embedder": {"text": question}})

for doc in result["retriever"]["documents"]:
    print(doc.content)
    print("-" * 10)