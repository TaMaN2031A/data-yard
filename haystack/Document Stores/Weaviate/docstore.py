from haystack_integrations.document_stores.weaviate import WeaviateDocumentStore
from weaviate.embedded import EmbeddedOptions
from haystack import Document

doc_store = WeaviateDocumentStore(embedded_options=EmbeddedOptions())

doc_store.write_documents([
    Document("This is first"),
    Document("This is second"),
])

print(doc_store.count_documents())