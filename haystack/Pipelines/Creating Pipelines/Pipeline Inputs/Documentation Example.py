from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.writers import DocumentWriter

document_store = InMemoryDocumentStore()
fetcher = LinkContentFetcher()
converter = HTMLToDocument()
writer = DocumentWriter(document_store=document_store)

pipeline = Pipeline()
pipeline.add_component(name="fetcher", instance=fetcher)
pipeline.add_component(name="converter", instance=converter)
pipeline.add_component(name="writer", instance=writer)

pipeline.connect("fetcher.streams", "converter.sources")
pipeline.connect("converter.documents", "writer.documents")

#print(pipeline.inputs())
data={
    "fetcher": {"urls": ["https://docs.haystack.deepset.ai/docs/pipelines"]}
}
result = pipeline.run(data=data)
print(result)
print(document_store.filter_documents())