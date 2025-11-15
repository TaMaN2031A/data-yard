from haystack import Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack import Pipeline
from haystack.utils.auth import Secret
from couchbase_haystack import CouchbaseSearchDocumentStore, CouchbasePasswordAuthenticator

documents = [Document(content="This is document 1"), Document(content="This is document 2")]

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

embedder = SentenceTransformersDocumentEmbedder()
document_writer = DocumentWriter(
    document_store=document_store,
)

indexing_pipeline = Pipeline()
indexing_pipeline.add_component(instance=embedder, name="embedder")
indexing_pipeline.add_component(instance=document_writer, name="writer")

indexing_pipeline.connect("embedder", "writer")

indexing_pipeline.run({"embedder": {"documents": documents}})