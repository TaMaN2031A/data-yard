from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack import Document
document_store = InMemoryDocumentStore()
document_store = DocumentWriter(
    document_store=document_store,
    policy=DuplicatePolicy.SKIP
)