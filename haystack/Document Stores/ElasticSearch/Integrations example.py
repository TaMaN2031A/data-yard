from haystack_experimental.components.embedders.types import DocumentEmbedder
from haystack_integrations.document_stores.elasticsearch import ElasticsearchDocumentStore
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.converters import TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter

document_store = ElasticsearchDocumentStore(hosts="http://localhost:9200")
converter = TextFileToDocument()
splitter = DocumentSplitter()
doc_embedder = SentenceTransformersDocumentEmbedder()
writer = DocumentWriter(document_store=document_store)

indexing_pipeline = Pipeline()
indexing_pipeline.add_component('converter', converter)
indexing_pipeline.add_component('splitter', splitter)
indexing_pipeline.add_component('embedder', doc_embedder)
indexing_pipeline.add_component('writer', writer)

indexing_pipeline.connect('converter', 'splitter')
indexing_pipeline.connect('splitter', 'embedder')
indexing_pipeline.connect('embedder', 'writer')

indexing_pipeline.run({"converter": {"sources": ["../_Metadata/Document Stores Backends Summary.txt"]}})