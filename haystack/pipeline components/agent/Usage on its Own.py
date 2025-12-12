from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.utils import Secret
from haystack.utils.hf import HFGenerationAPIType
from haystack.tools.tool import Tool
from haystack.components.agents import Agent
from typing import List
from haystack.dataclasses import ChatMessage

def calculate(expression: str) -> dict:
    try:
        result = eval(expression, {"__builtins__": {}})
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

calulator_tool = Tool(
    name="calculator",
    description="A tool to calculate a number",
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Math expression to evaluate",
            },
        },
        "required": ["expression"],
    },
    function=calculate,
    outputs_to_state={"calc_result": {"source": "result"}},
)

agent = Agent(
    chat_generator=HuggingFaceAPIChatGenerator(api_type=HFGenerationAPIType.SERVERLESS_INFERENCE_API,
                                  api_params={"model": "Qwen/Qwen2.5-7B-Instruct",
                                             "provider": "together"},
                                  token=Secret.from_env_var("HF_TOKEN")),
    tools=[calulator_tool],
    exit_conditions=["calculator"],
    state_schema={
        "calc_result": {"type": int},
    }
)

agent.warm_up()
response = agent.run(messages=[ChatMessage.from_user("What is 7 * (4 + 2)?")])

print(response["messages"])
print("Calc Result: ", response.get("calc_result"))