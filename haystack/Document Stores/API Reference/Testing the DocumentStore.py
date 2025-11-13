# Import dependencies
from haystack import Document, Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever

# Creating Documents
documents = [
    Document(content='Khufu is the largest Pyramid.'),
    Document(content='Arjen Robben is a fascinating player.'),
    Document(content='Khafre is the middle pyramid.'),
    Document(content='People should drink between three and five liters of water daily.'),
    Document(content='PSG won the champions league last year.'),
    Document(content='Menkaure is the smallest pyramid.'),
    Document(content='Population of China is 1.4 billion.'),
]
embed_docs = SentenceTransformersDocumentEmbedder()
embed_docs.warm_up()
embeddings = embed_docs.run(documents=documents)
# Initialize components
document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")
#text_embedder = SentenceTransformersTextEmbedder()
retriever = InMemoryEmbeddingRetriever(document_store=document_store)

print(embeddings["documents"])
# Adding documents to document store
document_store.write_documents(embeddings["documents"])

# Create the pipeline
query_pipeline = Pipeline()

# Add components
#query_pipeline.add_component("text_embedder", text_embedder)
query_pipeline.add_component("retriever", retriever)

# Connect components
#query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")

# Run the pipeline
query = "Who is a fascinating player?"
embeddings = [0. for _ in range(768)]
print(all(isinstance(x, float) for x in embeddings))
embeddings[1] = 10000000000000
print(all(isinstance(x, float) for x in embeddings))
result = query_pipeline.run({"retriever": {"query_embedding": embeddings}})
print(result)
