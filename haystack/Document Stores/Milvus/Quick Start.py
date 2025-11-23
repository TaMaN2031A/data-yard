from haystack import Document
from milvus_haystack import MilvusDocumentStore

document_store = MilvusDocumentStore(
    connection_args={"uri": "./milvus.db"},
    drop_old=True
)
