from haystack_integrations.document_stores.mongodb_atlas import MongoDBAtlasDocumentStore

## Initialize the document store
document_store = MongoDBAtlasDocumentStore(
    database_name="haystack_test",
    collection_name="test_collection",
    vector_search_index="embedding_index",
  	full_text_search_index="search_index",
)