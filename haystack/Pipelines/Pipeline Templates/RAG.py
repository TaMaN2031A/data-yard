from haystack import Pipeline, PredefinedPipeline
from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.utils import Secret
from haystack.utils.hf import HFGenerationAPIType

pipeline = Pipeline.from_template(PredefinedPipeline.RAG)
print(
    pipeline.to_dict()
)
llm = HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN"))
pipeline.remove_component('llm')
pipeline.add_component('llm', llm)
pipeline.connect('prompt_builder', 'llm')
print(pipeline.to_dict())
