from typing import List

from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.utils.auth import Secret
from couchbase_haystack.document_stores import CouchbaseSearchDocumentStore, CouchbasePasswordAuthenticator
from couchbase_haystack.components.retrievers import CouchbaseSearchEmbeddingRetriever

document_store = CouchbaseSearchDocumentStore(
    cluster_connection_string=Secret.from_env_var("CB_CONNECTION_STRING"),
    authenticator=CouchbasePasswordAuthenticator(
        username=Secret.from_env_var("CB_USERNAME"),
        password=Secret.from_env_var("CB_PASSWORD"),
    ),
    bucket="haystack_bucket_name",
    scope="_default",
    collection="_default",
    vector_search_index="vector_search_index"
)

documents = [
    Document(content="Alice has been living in New York City for the past 5 years.", meta={"num_of_years": 5, "city": "New York"}),
    Document(content="John moved to Los Angeles 2 years ago and loves the sunny weather.", meta={"num_of_years": 2, "city": "Los Angeles"}),
]

document_embedder = SentenceTransformersDocumentEmbedder()
document_embedder.warm_up()
documents_with_embedding = document_embedder.run(documents)

#document_store.write_documents(documents_with_embedding.get("documents"))
print("Number of documents written: ", document_store.count_documents())

pipeline = Pipeline()
pipeline.add_component("text_embedder", SentenceTransformersTextEmbedder())
pipeline.add_component("retriever", CouchbaseSearchEmbeddingRetriever(document_store=document_store))
pipeline.connect("text_embedder.embedding", "retriever.query_embedding")

result = pipeline.run(
    data={
        "text_embedder": {"text": "What cities do Alice live in?"}
        , "retriever": {
            "top_k": 5
        }
    }
)
print(result)
documents: List[Document] = result["retriever"]["documents"]
print(documents)