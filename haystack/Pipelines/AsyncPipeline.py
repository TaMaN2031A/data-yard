import asyncio
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

embed_docs = SentenceTransformersDocumentEmbedder()
embed_docs.warm_up()
embeddings = embed_docs.run(documents=documents)

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
hybrid_rag_retrieval.add_component("prompt_builder", ChatPromptBuilder(template=prompt_template, required_variables="*"))
hybrid_rag_retrieval.add_component("llm", HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN")))

hybrid_rag_retrieval.connect("text_embedder.embedding", "embedding_retriever.query_embedding")
hybrid_rag_retrieval.connect("bm25_retriever.documents", "document_joiner.documents")
hybrid_rag_retrieval.connect("embedding_retriever.documents", "document_joiner.documents")
hybrid_rag_retrieval.connect("document_joiner.documents", "prompt_builder.documents")
hybrid_rag_retrieval.connect("prompt_builder.prompt", "llm.messages")

question = "Which pyramid is neither the smallest nor the biggest?"
data = {
    "prompt_builder": {"query": question},
    "text_embedder": {"text": question},
    "bm25_retriever": {"query": question},
}

async def process_results():
    async for partial_output in hybrid_rag_retrieval.run_async_generator(
            data=data,
            include_outputs_from={"document_joiner", "llm"}
    ):
        # Each partial_output contains the results from a completed component
        if "document_joiner" in partial_output:
            print("Retrieved documents:", len(partial_output["document_joiner"]["documents"]))
        if "llm" in partial_output:
            print("Generated answer:", partial_output["llm"]["replies"][0])

asyncio.run(process_results())