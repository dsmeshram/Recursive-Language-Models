# RLM SDK Examples

This directory contains example scripts demonstrating how to use the RLM SDK.

## Examples

### 1. Basic Usage (`basic_usage.py`)

Simple example showing how to query a document:

```python
from rlm_sdk import RLMClient

# Initialize client
client = RLMClient()

# Load a document
client.load_document_from_file("sample_document.txt")

# Ask a question
answer = client.query("What is the main topic of this document?")
print(answer)
```

### 2. Multiple Queries (`multiple_queries.py`)

Example showing how to ask multiple questions about the same document:

```python
from rlm_sdk import RLMClient

client = RLMClient()
client.load_document_from_file("research_paper.txt")

questions = [
    "What is the main hypothesis?",
    "What methodology was used?",
    "What are the key findings?"
]

for question in questions:
    print(f"\nQ: {question}")
    answer = client.query(question, verbose=True)
    print(f"A: {answer}\n")
```

### 3. Custom Document Processing (`custom_processing.py`)

Example with custom document handling:

```python
from rlm_sdk import RLMClient, RLMDocument

# Create custom document
content = """Your document content here..."""
doc = RLMDocument(content, name="Custom Doc")

# Initialize and query
client = RLMClient(model="gpt-4o")
client.load_document(doc)
answer = client.query("Summarize this document")
print(answer)
```

### 4. Quick Query (`quick_usage.py`)

One-liner for simple use cases:

```python
from rlm_sdk import quick_query

answer = quick_query("document.txt", "What is this about?")
print(answer)
```

## Running Examples

```bash
# Basic usage
python examples/basic_usage.py

# Multiple queries
python examples/multiple_queries.py

# Custom processing
python examples/custom_processing.py

# Quick usage
python examples/quick_usage.py
```

## Notes

- Make sure to set your `OPENAI_API_KEY` environment variable
- Prepare sample documents before running examples
- Use `verbose=True` to see the tool calling process
