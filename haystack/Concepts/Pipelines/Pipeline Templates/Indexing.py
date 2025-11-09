from haystack import Pipeline, PredefinedPipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder

pipeline = Pipeline.from_template(PredefinedPipeline.INDEXING)
pipeline.remove_component('embedder')
docs_embedder = SentenceTransformersDocumentEmbedder()
pipeline.add_component('embedder', docs_embedder)
pipeline.connect('splitter.documents', 'embedder.documents')
#pipeline.connect('embedder.documents', 'writer.documents')
result = pipeline.run({"converter": {"sources": [r"dummy.txt"]}})