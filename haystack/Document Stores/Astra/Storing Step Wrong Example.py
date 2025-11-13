import logging

from haystack import Document, Pipeline

from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy

from haystack_integrations.document_stores.astra import AstraDocumentStore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"

# embedding_dim is the number of dimensions the embedding model supports.
document_store = AstraDocumentStore(
    astra_collection="dummy",
    duplicates_policy=DuplicatePolicy.SKIP,
    embedding_dim=384,
)


# Add Documents
documents = [
    Document(content="There are over 7,000 languages spoken around the world today."),
    Document(
        content="Elephants have been observed to behave in a way that indicates"
        " a high level of self-awareness, such as recognizing themselves in mirrors."
    ),
    Document(
        content="In certain parts of the world, like the Maldives, Puerto Rico, "
        "and San Diego, you can witness the phenomenon of bioluminescent waves."
    ),
]
index_pipeline = Pipeline()
index_pipeline.add_component(
    instance=SentenceTransformersDocumentEmbedder(model=embedding_model_name),
    name="embedder",
)
index_pipeline.add_component(instance=DocumentWriter(document_store=document_store, policy=DuplicatePolicy.SKIP), name="writer")
index_pipeline.connect("embedder.documents", "writer.documents")

index_pipeline.run({"embedder": {"documents": documents}})

print(document_store.count_documents())
