from haystack import Pipeline
from couchbase_haystack import CouchbasePasswordAuthenticator, CouchbaseSearchDocumentStore, CouchbaseSearchEmbeddingRetriever
from haystack.utils import Secret
from haystack.components.embedders import SentenceTransformersTextEmbedder

document_store = CouchbaseSearchDocumentStore(
    cluster_connection_string=Secret.from_env_var("CB_CONNECTION_STRING"),
    authenticator=CouchbasePasswordAuthenticator(
        username=Secret.from_env_var("CB_USERNAME"),
        password=Secret.from_env_var("CB_PASSWORD"),
    ),
    bucket="haystack_bucket_name",
    scope="_default",
    collection="VectorSearchIndexingBasedPipeline",
    vector_search_index="vector_search_index",
)

p = Pipeline()
p.add_component('a', SentenceTransformersTextEmbedder())
p.add_component('b', CouchbaseSearchEmbeddingRetriever(document_store=document_store))
p.connect('a.embedding', 'b.query_embedding')

query = "What is the story of A Song of Ice and Fire?"

result = p.run({'a': {"text": query}, 'b': {'top_k': 5}})

print(result)