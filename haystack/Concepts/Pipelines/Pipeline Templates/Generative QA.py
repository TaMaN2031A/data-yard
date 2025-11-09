from haystack import Pipeline, PredefinedPipeline
from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.utils import Secret
from haystack.utils.hf import HFGenerationAPIType

pipeline = Pipeline.from_template(PredefinedPipeline.GENERATIVE_QA)
print(
    pipeline.to_dict()
)
llm = HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN"))
pipeline.remove_component('generator')
pipeline.add_component('generator', llm)
pipeline.connect('prompt_builder', 'generator')
pipeline.run({"prompt_builder":{"question":"Where is Rome?"}})