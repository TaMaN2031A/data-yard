from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.dataclasses import Document
from haystack.dataclasses.chat_message import ChatMessage
from haystack.components.builders import ChatPromptBuilder
from haystack import Pipeline, SuperComponent
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.utils import Secret
from haystack.utils.hf import HFGenerationAPIType

document_store = InMemoryDocumentStore()
documents = [
    Document(content="Paris is the capital of France."),
    Document(content="London is the capital of England.")
]
document_store.write_documents(documents)

prompt_template = [
    ChatMessage.from_user(
        '''
        According to the following documents:
        {% for document in documents %}
        {{document.content}}
        {% endfor %}
        Answer the given question: {{query}}
        Answer:
        '''
    )
]

prompt_builder = ChatPromptBuilder(prompt_template=prompt_template,
                                   required_variables="*")

pipeline = Pipeline()
pipeline.add_component("retriever", InMemoryBM25Retriever(document_store=document_store))
pipeline.add_component("prompt_builder", prompt_builder)
pipeline.add_component("llm", HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN")))
pipeline.connect("retriever.documents", "prompt_builder.documents")
pipeline.connect("prompt_builder.prompt", "llm.messages")

wrapper = SuperComponent(
    pipeline=pipeline,
    input_mapping={
        'query': ["retriever.query", "prompt_builder.query"],
    },
    output_mapping={
        "llm.replies": "replies",
        "retriever.documents": "documents",
    }
)

result = wrapper.run(
    query="What is the capital of France?"
)
print(result)