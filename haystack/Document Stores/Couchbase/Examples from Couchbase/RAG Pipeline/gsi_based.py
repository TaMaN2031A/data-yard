from multiprocessing.connection import answer_challenge

from couchbase.options import KnownConfigProfiles
from haystack import GeneratedAnswer, Pipeline
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.utils import Secret

from couchbase_haystack import (
    CouchbaseClusterOptions,
    CouchbasePasswordAuthenticator,
    CouchbaseQueryDocumentStore,
    CouchbaseQueryEmbeddingRetriever,
    QueryVectorSearchType,
)

document_store = CouchbaseQueryDocumentStore(
    cluster_connection_string=Secret.from_env_var("CB_CONNECTION_STRING"),
    authenticator=CouchbasePasswordAuthenticator(
        username=Secret.from_env_var("CB_USERNAME"),
        password=Secret.from_env_var("CB_PASSWORD"),
    ),
    bucket="haystack_bucket_name",
    scope="_default",
    collection="_default",
    search_type=QueryVectorSearchType.ANN,
    similarity="L2",
    nprobes=10
)
# Build a RAG pipeline with a Retriever to get relevant documents to the query and a HuggingFaceTGIGenerator
# interacting with LLMs using a custom prompt.
prompt_template = """
Given these documents, answer the question.\nDocuments:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}

\nQuestion: {{question}}
\nAnswer:
"""
rag_pipeline = Pipeline()
rag_pipeline.add_component(
    "query_embedder",
    SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2", progress_bar=False),
)
rag_pipeline.add_component("retriever", CouchbaseQueryEmbeddingRetriever(document_store=document_store))
rag_pipeline.add_component("prompt_builder", PromptBuilder(template=prompt_template))
rag_pipeline.add_component(
    "llm",
    HuggingFaceAPIGenerator(
        api_type="serverless_inference_api",
        api_params={"model": "mistralai/Mistral-7B-v0.1"},
    ),
)
rag_pipeline.add_component("answer_builder", AnswerBuilder())

rag_pipeline.connect("query_embedder", "retriever.query_embedding")
rag_pipeline.connect("retriever.documents", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder.prompt", "llm.prompt")
rag_pipeline.connect("llm.replies", "answer_builder.replies")
rag_pipeline.connect("llm.meta", "answer_builder.meta")
rag_pipeline.connect("retriever", "answer_builder.documents")

# Ask a question on the data you just added.
question = "Who created the Dothraki vocabulary?"
result = rag_pipeline.run(
    {
        "query_embedder": {"text": question},
        "retriever": {"top_k": 3},
        "prompt_builder": {"question": question},
        "answer_builder": {"query": question},
    }
)

# For details, like which documents were used to generate the answer, look into the GeneratedAnswer object
answer: GeneratedAnswer = result["answer_builder"]["answers"][0]

# ruff: noqa: T201
print("Query: ", answer.query)
print("Answer: ", answer.data)
print("== Sources:")
for doc in answer.documents:
    print("-> ", doc.meta["file_path"])