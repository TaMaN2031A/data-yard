from haystack import Document
from haystack.components.converters import OutputAdapter

adapter = OutputAdapter(template="{{ document[0].content }}",
                        output_type=str)
input_data = {"document": [Document(content="Test content")]}
expected_output = {"output": "Test content"}

assert adapter.run(**input_data) == expected_output