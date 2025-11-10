from haystack.dataclasses import ChatMessage, ImageContent

capybara_image_url = (
    "https://cdn.pixabay.com/photo/2017/04/24/11/05/capybara-2252556_960_720.jpg"
)

image_content = ImageContent.from_url(url=capybara_image_url, detail="low")
user_message = ChatMessage.from_user(
    content_parts=[
        "What does the image show?",
        image_content
    ]
)

print(user_message)
print(user_message.text)
print(user_message.texts)
print(user_message.image)