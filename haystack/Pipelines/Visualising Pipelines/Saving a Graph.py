"""
pipeline لو عايز تعرف المدخلات اللي محتاج تديها ل
وانت بترانه
"""
from haystack import AsyncPipeline, Document
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from haystack.components.retrievers import InMemoryEmbeddingRetriever, InMemoryBM25Retriever
from haystack.components.joiners import DocumentJoiner
from haystack.components.builders import ChatPromptBuilder
from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.utils import Secret
from haystack.utils.hf import HFGenerationAPIType
documents = [
    Document(content='Khufu is the largest Pyramid.'),
    Document(content='Arjen Robben is a fascinating player.'),
    Document(content='Khafre is the middle pyramid.'),
    Document(content='People should drink between three and five letters of water daily.'),
    Document(content='PSG won the champions league last year.'),
    Document(content='Menkaure is the smallest pyramid.'),
    Document(content='Population of China is 1.4 billion.'),
]

docs_embedder = SentenceTransformersDocumentEmbedder()
docs_embedder.warm_up()
embeddings = docs_embedder.run(documents=documents)

document_store = InMemoryDocumentStore()
document_store.write_documents(embeddings["documents"])

prompt_template = [
    ChatMessage.from_system(
        '''
        You are a precise, factual QA assistant.
        According to the following documents:
        {% for document in documents %}
        {{document.content}}
        {% endfor %}

        If an answer cannot be deduced from the documents, say "I don't know based on these documents".

        When answering:
        - be concise
        - write the documents that support your answer

        Answer the given question
        '''
    ),
    ChatMessage.from_user(
        '''
        {{query}}
        '''
    ),
    ChatMessage.from_system("Answer:")
]

hybrid_rag_retrieval = AsyncPipeline()
hybrid_rag_retrieval.add_component("text_embedder", SentenceTransformersTextEmbedder())
hybrid_rag_retrieval.add_component("embedding_retriever", InMemoryEmbeddingRetriever(document_store=document_store))
hybrid_rag_retrieval.add_component("bm25_retriever", InMemoryBM25Retriever(document_store=document_store))
hybrid_rag_retrieval.add_component("document_joiner", DocumentJoiner())
hybrid_rag_retrieval.add_component("prompt_builder",
                                   ChatPromptBuilder(template=prompt_template, required_variables="*"))
hybrid_rag_retrieval.add_component("llm",
                                   HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                                               api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                                                           "provider": "together"},
                                                               token=Secret.from_env_var("HF_TOKEN")))

hybrid_rag_retrieval.connect("text_embedder.embedding", "embedding_retriever.query_embedding")
hybrid_rag_retrieval.connect("bm25_retriever.documents", "document_joiner.documents")
hybrid_rag_retrieval.connect("embedding_retriever.documents", "document_joiner.documents")
hybrid_rag_retrieval.connect("document_joiner.documents", "prompt_builder.documents")
hybrid_rag_retrieval.connect("prompt_builder.prompt", "llm.messages")

hybrid_rag_retrieval.draw(path='hybrid_rag_retrieval.png')