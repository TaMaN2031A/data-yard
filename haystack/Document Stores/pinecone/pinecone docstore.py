from haystack import Document
from haystack_integrations.document_stores.pinecone import PineconeDocumentStore

document_store = PineconeDocumentStore(
    index='default',
    namespace='default',
    dimension=5,
    metric='cosine',
    spec={"serverless": {"region": "us-east-1", "cloud": "aws"}},
)

document_store.write_documents([
    Document(content="This is the first document.", embedding=[0.0]*5),
    Document(content="This is the second document.", embedding=[0.5]*5),
])
print(document_store.count_documents())