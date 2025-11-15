from couchbase_haystack import CouchbaseSearchDocumentStore, CouchbasePasswordAuthenticator
from haystack.utils.auth import Secret
from haystack import Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder

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

documents = [Document(content="Alice has been living in New York City for the past 5 years.")]

document_embedder = SentenceTransformersDocumentEmbedder()
document_embedder.warm_up()
documents_with_embeddings = document_embedder.run(documents)
document_store.write_documents(documents_with_embeddings.get("documents"))
