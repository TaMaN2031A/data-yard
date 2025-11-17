from datetime import timedelta

from couchbase.logic.n1ql import QueryScanConsistency
from couchbase_haystack import CouchbaseQueryDocumentStore, CouchbasePasswordAuthenticator, QueryVectorSearchType, \
    CouchbaseQueryOptions, CouchbaseQueryEmbeddingRetriever
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.utils import Secret
from haystack import Document, Pipeline
from haystack.components.converters import DocumentWriter

document_store = CouchbaseQueryDocumentStore(
    cluster_connection_string=Secret.from_env_var("CB_CONNECTION_STRING"),
    authenticator=CouchbasePasswordAuthenticator(
        username=Secret.from_env_var("CB_USERNAME"),
        password=Secret.from_env_var("CB_PASSWORD"),
    ),
    bucket="haystack_bucket_name",
    scope="_default",
    collection="_default",
    search_type=QueryVectorSearchType.ANN,
    similarity="L2",
    nprobes=10,
    query_options=CouchbaseQueryOptions(timeout=timedelta(seconds=300), scan_consistency=QueryScanConsistency.REQUEST_PLUS)
)

r = CouchbaseQueryEmbeddingRetriever(document_store=document_store)
e = SentenceTransformersTextEmbedder()
p = Pipeline()
p.add_component("embedder", e)
p.add_component("retriever", r)
p.connect("embedder.embedding", "retriever.query_embedding")

query = "who is jon snow's father?"

results = p.run({"text": query})

print(results)
