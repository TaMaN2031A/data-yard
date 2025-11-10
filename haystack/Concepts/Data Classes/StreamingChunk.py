from haystack.dataclasses.streaming_chunk import StreamingChunk, ComponentInfo, ToolCallDelta
#https://docs.haystack.deepset.ai/docs/data-classes#example-2

# Basic text chunk
chunk = StreamingChunk(
    content="Hello world",
    start=True,
    meta={"model": "gpt-3.5-turbo"}
)

# Tool call chunk
tool_chunk = StreamingChunk(
    content='',
    tool_calls=[ToolCallDelta(index=0, tool_name="calculator", arguments='{"operation": "add", "a": 2, "b": 3}')],
    index=0,
    start=False,
    finish_reason="tool_calls"
)