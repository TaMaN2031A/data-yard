from haystack.dataclasses import ChatMessage, ToolCall

tool_call = ToolCall(tool_name="weather_tool", arguments={"location": "Rome"})

assistant_message = ChatMessage.from_assistant('How is the weather in Rome today?', tool_calls=[tool_call])

print(assistant_message)
print(assistant_message.text)
print(assistant_message.texts)
print(assistant_message.tool_call)
print(assistant_message.tool_calls)
print(assistant_message.tool_call_result)
print(assistant_message.tool_call_results)