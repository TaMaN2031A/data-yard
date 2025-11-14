from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack import Document

document_store = ChromaDocumentStore()
document_store.write_documents(
    [
        Document(content="This is the first document."),
        Document(content="This is the second document."),
    ]
)
print(document_store.count_documents())