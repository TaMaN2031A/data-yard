from typing import List

from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from neo4j_haystack import Neo4jEmbeddingRetriever, Neo4jDocumentStore

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

documents = [
    Document(content="My name is Morgan and I live in Paris.", meta={"release_date": "2018-12-09"})
]
document_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
document_embedder.warm_up()
documents_with_embeddings = document_embedder.run(documents)

document_store.write_documents(documents_with_embeddings.get("documents"))
print(document_store.count_documents())

p = Pipeline()
p.add_component("text_embedder", SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2"))
p.add_component("retriever", Neo4jEmbeddingRetriever(document_store=document_store))
p.connect("text_embedder.embedding", "retriever.query_embedding")

result = p.run(
    data={
        "text_embedder": {"text": "What cities do people live in?"},
        "retriever": {
            "top_k": 5,
            "filters": {"field": "release_date", "operator": "==", "value": "2018-12-09"},
        }
    }
)

documents: List[Document] = result["retriever"]["documents"]
print(documents)