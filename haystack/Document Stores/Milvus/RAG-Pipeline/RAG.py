import glob
import os

from haystack.utils import Secret

from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack import Pipeline
from haystack.components.converters import TextFileToDocument
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.utils.hf import HFGenerationAPIType

from milvus_haystack import MilvusDocumentStore
from milvus_haystack.milvus_embedding_retriever import MilvusEmbeddingRetriever

prompt_template = """Answer the following query based on the provided context. If the context does
                     not include an answer, reply with 'I don't know'.\n
                     Query: {{query}}
                     Documents:
                     {% for doc in documents %}
                        {{ doc.content }}
                     {% endfor %}
                     Answer: """

llm = HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN"))

document_store = MilvusDocumentStore(
    connection_args={"uri": "./milvus.db"},
)

rag_pipeline = Pipeline()
rag_pipeline.add_component("prompt_builder", ChatPromptBuilder([ChatMessage.from_user(prompt_template)]))
rag_pipeline.add_component('retriever', MilvusEmbeddingRetriever(document_store=document_store, top_k=3))
rag_pipeline.add_component("text_embedder", SentenceTransformersTextEmbedder())
rag_pipeline.add_component("llm", llm)

rag_pipeline.connect("prompt_builder.prompt", "llm.messages")
rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
rag_pipeline.connect('retriever', 'prompt_builder')
rag_pipeline.connect("prompt_builder.prompt", "llm.messages")

question = "How to rename a commit?"
messages = [ChatMessage.from_user(prompt_template)]
results = rag_pipeline.run({"text_embedder": {"text": question}, "prompt_builder": {"query": question}})

print('RAG answer:', results["llm"]["replies"][0].text)