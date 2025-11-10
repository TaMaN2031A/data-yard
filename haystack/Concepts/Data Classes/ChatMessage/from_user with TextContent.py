from haystack.dataclasses import ChatMessage

user_message = ChatMessage.from_user('What is the capital of Australia?')

print(user_message)
print(user_message.text)
print(user_message.texts)
