from typing import List

from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.utils import Secret

from neo4j_haystack import Neo4jEmbeddingRetriever, Neo4jDocumentStore

print(Secret.from_env_var("NEO4J_USERNAME"))
print(Secret.from_env_var("NEO4J_PASSWORD"))

document_store = Neo4jDocumentStore(
    url="_",
    username="_",
    password="_",
    database="neo4j",
    embedding_dim=384,
    embedding_field="embedding",
    index="document-embeddings", # The name of the Vector Index in Neo4j
    node_label="Document", # Providing a label to Neo4j nodes which store Documents
)



print(document_store.count_documents())