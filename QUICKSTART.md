# Quick Start Guide

Get started with RLM SDK in 5 minutes!

## Step 1: Install

```bash
pip install openai
```

## Step 2: Set API Key

```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Step 3: Run Your First Query

Create a file `my_first_rlm.py`:

```python
from rlm_sdk import RLMClient

# Initialize
client = RLMClient()

# Create a sample document
text = """
Welcome to RLM!

RLM (Recursive Language Model) helps you query large documents
efficiently. Instead of sending the entire document to the AI, it uses
tools to search and retrieve only relevant parts.

Key benefits:
- Reduces token usage
- Handles large documents
- More cost-effective
- Faster responses
"""

# Load document
client.load_document_from_text(text, "intro")

# Ask a question
answer = client.query("What are the key benefits of RLM?")
print(answer)
```

Run it:

```bash
python my_first_rlm.py
```

## Step 4: Try with Your Own Document

```python
from rlm_sdk import quick_query

# One-liner to query any document
answer = quick_query("your_document.txt", "What is this about?")
print(answer)
```

## Next Steps

- Check out the `examples/` directory for more examples
- Read the full README for advanced features
- Customize the system message for specific use cases

## Troubleshooting

**Problem**: `openai.OpenAIError: API key not found`
**Solution**: Make sure you've set the OPENAI_API_KEY environment variable

**Problem**: `ValueError: No document loaded`
**Solution**: Call `client.load_document()` before `client.query()`

**Problem**: Verbose output shows many tool calls
**Solution**: This is normal! The model is searching and reading the document

## Common Patterns

### Pattern 1: Single Question
```python
from rlm_sdk import quick_query
answer = quick_query("doc.txt", "What is the main point?")
```

### Pattern 2: Multiple Questions
```python
from rlm_sdk import RLMClient

client = RLMClient()
client.load_document_from_file("doc.txt")

for question in ["Q1?", "Q2?", "Q3?"]:
    print(client.query(question))
```

### Pattern 3: Multiple Documents
```python
from rlm_sdk import RLMClient

client = RLMClient()

# Query first document
client.load_document_from_file("doc1.txt")
answer1 = client.query("Question about doc1?")

# Switch to second document
client.load_document_from_file("doc2.txt")
answer2 = client.query("Question about doc2?")
```

### Pattern 4: Custom System Message
```python
from rlm_sdk import RLMClient

client = RLMClient()
client.load_document_from_file("legal_doc.txt")

answer = client.query(
    "What are the terms?",
    system_message="You are a legal expert. Analyze this document carefully."
)
```

Happy querying! 🚀
