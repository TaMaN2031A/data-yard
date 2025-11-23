import glob
import os

from haystack import Pipeline
from haystack.components.converters import TextFileToDocument
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter

from milvus_haystack import MilvusDocumentStore
from milvus_haystack.milvus_embedding_retriever import MilvusEmbeddingRetriever

current_file_path = "Contribution steps.txt"
file_paths = [current_file_path]
document_store = MilvusDocumentStore(
    connection_args={"uri": "./milvus.db"},
    drop_old=True
)
indexing_pipeline = Pipeline()
indexing_pipeline.add_component('converter', TextFileToDocument())
indexing_pipeline.add_component('splitter', DocumentSplitter())
indexing_pipeline.add_component('embedder', SentenceTransformersDocumentEmbedder())
indexing_pipeline.add_component('writer', DocumentWriter(document_store))
indexing_pipeline.connect('converter', 'splitter')
indexing_pipeline.connect('splitter', 'embedder')
indexing_pipeline.connect('embedder', 'writer')

indexing_pipeline.run({"converter": {"sources": file_paths}})
print("Number of documents:", document_store.count_documents())
