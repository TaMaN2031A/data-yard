from haystack import Pipeline
from haystack.utils import Secret
from haystack.utils.hf import HFGenerationAPIType
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses.chat_message import ChatMessage
from haystack_integrations.document_stores.chroma import ChromaDocumentStore

prompt = """
Answer the query based on the provided context.
If the context does not contain the answer, say 'Answer not found'.
Context:
{% for doc in documents %}
  {{ doc.content }}
{% endfor %}
query: {{query}}
Answer:
"""

template = [ChatMessage.from_user(prompt)]
prompt_builder = ChatPromptBuilder(template)
document_store = ChromaDocumentStore()

llm = HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN"))
retriever = ChromaQueryTextRetriever(document_store)

pipeline = Pipeline()
pipeline.add_component("retriever", retriever)
pipeline.add_component("prompt_builder", prompt_builder)
pipeline.add_component("llm", llm)

pipeline.connect("retriever.documents", "prompt_builder.documents")
pipeline.connect("prompt_builder", "llm")

query = "Should I write documentation for my plugin?"
result = pipeline.run({"retriever": {"query": query, "top_k": 3},
                    "prompt_builder": {"query": query}})
print(result)