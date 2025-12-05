from haystack.utils import Secret
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from haystack import Document
PG_CONN_STR = "postgresql://postgres:postgres@localhost:5432/postgres"

document_store = PgvectorDocumentStore(
    connection_string=Secret.from_token(PG_CONN_STR),
    embedding_dimension=768,
    vector_function='cosine_similarity',
    recreate_table=True,
    search_strategy="hnsw"
)
print(document_store.connection_string.resolve_value())
document_store.write_documents([
    Document(content='This is first', embedding=[0.1]*768),
    Document(content='This is second', embedding=[0.3]*768),
])

print(document_store.count_documents())