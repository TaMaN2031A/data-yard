from haystack.dataclasses import ChatMessage

assistant_message = ChatMessage.from_assistant('How can I assist you today?')

print(assistant_message)

print(assistant_message.text)

print(assistant_message.texts)