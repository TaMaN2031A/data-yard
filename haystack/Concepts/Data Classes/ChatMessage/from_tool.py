from haystack.dataclasses import ChatMessage, ToolCall

tool_call = ToolCall(tool_name="weather_tool", arguments={"location": "Rome"})
tool_message = (
    ChatMessage.from_tool(tool_result="temparature: 25C",
                          origin=tool_call,
                          error=False))
print(tool_message)
print(tool_message.text)
print(tool_message.texts)
print(tool_message.tool_call)
print(tool_message.tool_calls)
print(tool_message.tool_call_result)
print(tool_message.tool_call_results)
