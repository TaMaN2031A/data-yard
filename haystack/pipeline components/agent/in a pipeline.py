from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.utils import Secret
from haystack.utils.hf import HFGenerationAPIType
from haystack.components.agents import Agent
from haystack.core.pipeline import Pipeline
from haystack.components.builders.chat_prompt_builder import ChatPromptBuilder
from haystack.components.converters.html import HTMLToDocument
from haystack.components.fetchers.link_content import LinkContentFetcher
from haystack.tools import tool
from haystack.document_stores.in_memory import InMemoryDocumentStore
from typing import Optional
from haystack.dataclasses import ChatMessage, Document

document_store = InMemoryDocumentStore()

@tool
def add_database_tool(name: str, surname: str, job_title:Optional[str],
                      other: Optional[str]):
    """Use this tool to add names to the database with information about them"""
    document_store.write_documents([Document(content=name + " " + surname + " " + (job_title or ""), meta={"other":other})])
    return

database_assistant = Agent(
    chat_generator=HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN")),
    tools=[add_database_tool],
    system_prompt="""
    You are a database assistant.
    Your task is to extract the names of people mentioned in the given context and add them to a knowledge base, 
    along with additional relevant information about them that can be extracted from the context.
    Do not use you own knowledge, stay grounded to the given context.
    Do not ask the user for confirmation. Instead, automatically update the knowledge base and return a brief summary 
    of the people added, including the information stored for each.
    """,
    exit_conditions=["text"],
    max_agent_steps=100,
    raise_on_tool_invocation_failure=False
)

extraction_agent = Pipeline()
extraction_agent.add_component("fetcher", LinkContentFetcher())
extraction_agent.add_component("converter", HTMLToDocument())
extraction_agent.add_component("builder", ChatPromptBuilder(
    template=[ChatMessage.from_user("""
        {% for doc in docs %}
        {{ doc.content|default|truncate(25000) }}
        {% endfor %}
        """)],
    required_variables=["docs"]
))
extraction_agent.add_component("database_agent", database_assistant)

extraction_agent.connect('fetcher.streams', 'converter.sources')
extraction_agent.connect('converter.documents', 'builder.docs')
extraction_agent.connect('builder', 'database_agent')

agent_op = extraction_agent.run({"fetcher": {"urls": ["https://en.wikipedia.org/wiki/Deepset"]}})

print(agent_op["database_agent"]["messages"][-1].text)

"https://haystack.deepset.ai/release-notes/v2.20.0"