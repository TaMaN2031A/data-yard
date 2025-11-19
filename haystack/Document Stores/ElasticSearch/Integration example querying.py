from haystack_integrations.document_stores.elasticsearch import ElasticsearchDocumentStore
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.components.retrievers.elasticsearch import ElasticsearchEmbeddingRetriever

document_store = ElasticsearchDocumentStore(hosts = "http://localhost:9200")

retriever = ElasticsearchEmbeddingRetriever(document_store=document_store)
text_embedder = SentenceTransformersTextEmbedder()

q = Pipeline()
q.add_component("text_embedder", text_embedder)
q.add_component("retriever", retriever)
q.connect("text_embedder.embedding", "retriever.query_embedding")

result = q.run({"text_embedder": {"text": "couchabse"}})
print(result)
