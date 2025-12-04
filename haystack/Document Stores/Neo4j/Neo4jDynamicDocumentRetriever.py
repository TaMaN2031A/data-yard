from typing import List

from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder

from neo4j_haystack import Neo4jClientConfig, Neo4jDynamicDocumentRetriever

client_config = Neo4jClientConfig(
    url="_",
    username="_",
    password="_",
    database="neo4j",
)

cipher_query = """
    CALL db.index.vector.queryNodes($index, $top_k, $query_embedding)
    YIELD node as doc, score
    MATCH (doc) WHERE doc.release_date = $release_date
    RETURN doc{.*, score}, score
    ORDER BY score DESC LIMIT $top_k
"""
embedders = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
retriever = Neo4jDynamicDocumentRetriever(
    client_config=client_config, runtime_parameters=["query_embedding"],
    doc_node_name="doc",
)

p = Pipeline()
p.add_component("text_embedder", embedders)
p.add_component("retriever", retriever)
p.connect("text_embedder.embedding", "retriever.query_embedding")

result = p.run(
    data={
        "text_embedder": {"text": "What cities do people live in?"},
        "retriever": {
            "query": cipher_query,
            "parameters": {"index": "document-embeddings", "top_k": 5,
                           "release_date": "2018-12-09"},
        }
    }
)

documents: List[Document] = result["retriever"]["documents"]

print(documents)