import os
from getpass import getpass
from typing import List

from haystack import logging, Document, Pipeline
from haystack.components.agents import Agent
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack.tools.from_function import tool
from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.utils import Secret
from haystack.utils.hf import HFGenerationAPIType
from haystack_integrations.components.connectors.github import GitHubIssueViewer
from haystack_integrations.tools.github import GitHubRepoViewerTool
from haystack_integrations.prompts.github import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

issue_viewer = GitHubIssueViewer()
print(issue_viewer.run(url="https://github.com/deepset-ai/haystack/issues/8903")["documents"])
github_repo_viewer_tool = GitHubRepoViewerTool()

@tool
def write_github_comment(comment: str) -> str:
    """
    Use this to create a comment on GitHub once you finished your exploration.
    """
    return comment

chat_generator = HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN"))

issue_resolver_agent = Agent(
    chat_generator=chat_generator,
    system_prompt=SYSTEM_PROMPT,
    tools=[github_repo_viewer_tool, write_github_comment],
    exit_conditions=["write_github_comment"],
    state_schema={"documents": {"type": List[Document]}}
)

issue_template = """
{% for document in documents %}
{% if loop.index == 1 %}
**Title: {{ document.meta.title }}**
{% endif %}
<issue-comment>
{{document.content}}
</issue-comment>
{% endfor %}
"""

issue_builder = ChatPromptBuilder(template=[ChatMessage.from_user(issue_template)], required_variables="*")

issue_resolver = Pipeline()
issue_resolver.add_component('issue_viewer', issue_viewer)
issue_resolver.add_component('issue_builder', issue_builder)
issue_resolver.add_component('issue_resolver_agent', issue_resolver_agent)


issue_resolver.connect("issue_viewer.documents", "issue_builder.documents")
issue_resolver.connect("issue_builder.prompt", "issue_resolver_agent.messages")

issue_url = "https://github.com/deepset-ai/haystack-core-integrations/issues/1819"
result = issue_resolver.run({"url": issue_url})
print(result)