from haystack_integrations.document_stores.opensearch import OpenSearchDocumentStore
from haystack import Document

document_store = OpenSearchDocumentStore(hosts="http://localhost:9200",
                                         use_ssl=True, verify_ssl=False, http_auth=("admin", "admin"))
document_store.write_documents([
    Document(content="This is first"),
    Document(content="This is second"),
])

print(document_store.count_documents())