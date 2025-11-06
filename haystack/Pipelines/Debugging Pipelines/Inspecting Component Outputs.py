from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.components.builders.chat_prompt_builder import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack.utils.hf import HFGenerationAPIType
from haystack.dataclasses.breakpoints import Breakpoint
from haystack.core.errors import BreakpointException

# Documents
documents = [Document(content="Joe lives in Berlin"), Document(content="Joe is a software engineer")]

break_point = Breakpoint(
    component_name="llm",
    visit_count=0,
    snapshot_file_path=r"C:\Users\20106\PycharmProjects\Data-Science\haystack\Pipelines\Debugging Pipelines"
)

# Define prompt template
prompt_template = [
    ChatMessage.from_system("You are a helpful assistant."),
    ChatMessage.from_user(
        "Given these documents, answer the question.\nDocuments:\n"
        "{% for doc in documents %}{{ doc.content }}{% endfor %}\n"
        "Question: {{query}}\nAnswer:"
    )
]

# Define pipeline
p = Pipeline()
p.add_component(instance=ChatPromptBuilder(template=prompt_template, required_variables={"query", "documents"}), name="prompt_builder")
p.add_component(instance=HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN")), name="llm")
p.connect("prompt_builder", "llm.messages")

# Define question
question = "Where does Joe live?"

# Execute pipeline
try:
    result = p.run({"prompt_builder": {"documents": documents, "query": question}},
               include_outputs_from="prompt_builder")
    # Print result
    print(result)
except BreakpointException as e:
    print(f"Breakpoint triggered at component: {e.component}")
    print(f"Component inputs: {e.inputs}")
    print(f"Pipeline results so far: {e.results}")