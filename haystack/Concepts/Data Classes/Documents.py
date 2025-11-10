from haystack import Document

doc = Document(content="Hello, world!", embedding=[0.1, 0.2, 0.3])
print(doc)