from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.document_stores.types import DuplicatePolicy
from haystack.utils import Secret
from haystack.utils.hf import HFGenerationAPIType
from haystack_integrations.components.retrievers.astra import AstraEmbeddingRetriever
from haystack_integrations.document_stores.astra import AstraDocumentStore

prompt_template = [
    ChatMessage.from_system(
        '''
        You are a precise, factual QA assistant.
        According to the following documents:
        {% for document in documents %}
        {{document.content}}
        {% endfor %}

        Answer the given question
        '''
    ),
    ChatMessage.from_user(
        '''
        {{question}}
        '''
    ),
    ChatMessage.from_system("Answer:")
]
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
document_store = AstraDocumentStore(
    collection_name="cook_book",
    duplicates_policy=DuplicatePolicy.SKIP,
    embedding_dimension=384
)

rag_pipeline = Pipeline()
rag_pipeline.add_component(instance=SentenceTransformersTextEmbedder(model=embedding_model_name),
                           name="embedder")
rag_pipeline.add_component(instance=AstraEmbeddingRetriever(document_store=document_store), name="retriever")
rag_pipeline.add_component(instance=ChatPromptBuilder(template=prompt_template, required_variables="*"), name="prompt_builder")
rag_pipeline.add_component(instance=HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN")), name="llm")
rag_pipeline.add_component(instance=AnswerBuilder(), name='answer_builder')
rag_pipeline.connect("embedder", "retriever")
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")
rag_pipeline.connect("llm.replies", "answer_builder.replies")
rag_pipeline.connect("retriever", "answer_builder.documents")
rag_pipeline.draw(path="rag_pipeline.png") # issue


question = "How many language are there in the world today?"
result = rag_pipeline.run(
    {
        "embedder": {"text": question},
        "retriever": {"top_k": 2},
        "prompt_builder": {"question": question},
        "answer_builder": {"query": question},
    }
)

print(result)