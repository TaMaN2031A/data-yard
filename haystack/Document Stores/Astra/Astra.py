from haystack import Document
from haystack_integrations.document_stores.astra import AstraDocumentStore

document_store = AstraDocumentStore()

document_store.write_documents([
    Document(content="This is first"),
    Document(content="This is second")
    ])
print(document_store.count_documents())