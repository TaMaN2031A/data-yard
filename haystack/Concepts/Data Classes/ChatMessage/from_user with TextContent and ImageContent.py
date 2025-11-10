
from haystack.dataclasses import ChatMessage, ImageContent

lion_image_url = (
    "https://images.unsplash.com/photo-1546182990-dffeafbe841d?"
	"ixlib=rb-4.0&q=80&w=1080&fit=max"
)

image_content = ImageContent.from_url(lion_image_url, detail="low")

user_message = ChatMessage.from_user(
	content_parts=[
		"What does the image show?",
		image_content
		])

print(user_message)


print(user_message.text)

print(user_message.texts)
