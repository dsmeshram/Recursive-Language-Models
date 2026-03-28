# Recursive Language Model (RLM)

A Python implementation demonstrating how to build a recursive language model using OpenAI's API with function calling capabilities. This pattern allows the model to search and retrieve information from large documents without loading the entire document into the context window.

## Overview

This project implements a **Recursive Language Model (RLM)** that:
- Processes large documents efficiently by using tool-based retrieval
- Enables the model to search and peek into documents dynamically
- Reduces token usage by only loading relevant document sections
- Demonstrates iterative tool calling with OpenAI's API

## How It Works

### Core Concept

Instead of sending an entire large document to the model, this implementation provides the model with two tools:
1. **search**: Find text patterns using regex in the document
2. **peek**: Retrieve specific sections of the document by byte offset

The model autonomously decides when and how to use these tools to answer questions about the document.

### Architecture

```
┌─────────────┐
│   User      │
│  Question   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  run_rlm(question)                  │
│  ┌───────────────────────────────┐  │
│  │ 1. Initial API call           │  │
│  │    with question & tools      │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │ 2. Tool loop                  │  │
│  │    - Model requests tools     │  │
│  │    - Execute search/peek      │  │
│  │    - Send results back        │  │
│  │    - Repeat until answer      │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│  ┌───────────▼───────────────────┐  │
│  │ 3. Return final answer        │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.7+
- OpenAI API key

### Setup

#### Option 1: Install from source

```bash
git clone https://github.com/damodharm10/RLM.git
cd RLM
pip install -e .
```

#### Option 2: Direct installation

```bash
pip install openai
```

### Configure API Key

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or on Windows:
```cmd
set OPENAI_API_KEY=your-api-key-here
```

## Usage

### Using the SDK (Recommended)

The easiest way to use RLM is through the provided SDK:

```python
from rlm_sdk import RLMClient

# Initialize the client
client = RLMClient()

# Load a document
client.load_document_from_file("your_document.txt")

# Ask questions
answer = client.query("What is the main topic of this document?")
print(answer)
```

### Quick Query (One-liner)

For simple use cases:

```python
from rlm_sdk import quick_query

answer = quick_query("document.txt", "Summarize the key points.")
print(answer)
```

### Advanced Usage

```python
from rlm_sdk import RLMClient, RLMDocument

# Initialize with custom settings
client = RLMClient(
    model="gpt-4o-mini",
    max_iterations=15
)

# Load from text
text = "Your document content here..."
client.load_document_from_text(text, name="MyDoc")

# Query with verbose mode to see tool calls
answer = client.query(
    "What are the key findings?",
    verbose=True
)
print(answer)

# Get document info
info = client.get_document_info()
print(f"Document: {info['name']}, Length: {info['length']} chars")
```

### Original Implementation Example

If you prefer the original implementation:

```python
from rlm import run_rlm

# Ask a question about your document
answer = run_rlm("Summarize the key steps in the process described in DOC.")
print(answer)
```

### Complete Implementation

```python
import os, re, json
from openai import OpenAI

client = OpenAI()

# Load your document
DOC = open("big_document.txt", "r", encoding="utf-8").read()

def tool_search(pattern: str, max_hits: int = 10):
    """Search for regex pattern in document."""
    hits = []
    for m in re.finditer(pattern, DOC, flags=re.IGNORECASE):
        hits.append({"start": m.start(), "end": m.end()})
        if len(hits) >= max_hits:
            break
    return {"hits": hits}

def tool_peek(start: int, end: int):
    """Retrieve document section from start to end offset."""
    start = max(0, start)
    end = min(len(DOC), end)
    return {"text": DOC[start:end], "start": start, "end": end}

# Define tools for the model
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Find locations of a regex/text pattern in DOC. Return start/end offsets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "max_hits": {"type": "integer", "default": 10}
                },
                "required": ["pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "peek",
            "description": "Return DOC substring for [start,end). Keep end-start small (e.g., <= 2000 chars).",
            "parameters": {
                "type": "object",
                "properties": {
                    "start": {"type": "integer"},
                    "end": {"type": "integer"}
                },
                "required": ["start", "end"]
            }
        }
    }
]

def run_rlm(question: str):
    """Run recursive language model query."""
    # First request
    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "system",
            "content": "You cannot see DOC. Use tools search/peek to inspect DOC and answer."
        },{
            "role": "user",
            "content": question
        }],
        tools=TOOLS
    )

    # Tool loop
    while True:
        # If model already produced final text, return it
        if getattr(resp, "output_text", None):
            return resp.output_text

        # Otherwise handle tool calls in resp.output
        tool_outputs = []
        for item in resp.output:
            if item.type == "tool_call" and item.tool_name in ("search", "peek"):
                args = json.loads(item.arguments)

                if item.tool_name == "search":
                    result = tool_search(**args)
                else:
                    result = tool_peek(**args)

                tool_outputs.append({
                    "type": "tool_result",
                    "tool_call_id": item.id,
                    "output": json.dumps(result)
                })

        # Send tool results back to model, continue the same response thread
        resp = client.responses.create(
            model="gpt-4.1-mini",
            previous_response_id=resp.id,
            input=tool_outputs,
            tools=TOOLS
        )

# Example usage
print(run_rlm("Summarize the key steps in the process described in DOC."))
```

## Tool Functions

### 1. `search(pattern, max_hits=10)`

Searches the document for a regex pattern.

**Parameters:**
- `pattern` (str): Regular expression pattern to search for
- `max_hits` (int): Maximum number of matches to return (default: 10)

**Returns:**
- Dictionary with list of hits containing start/end offsets

**Example:**
```python
# Model calls: search(pattern="introduction|overview", max_hits=5)
# Returns: {"hits": [{"start": 0, "end": 12}, {"start": 450, "end": 458}]}
```

### 2. `peek(start, end)`

Retrieves a substring from the document.

**Parameters:**
- `start` (int): Starting byte offset
- `end` (int): Ending byte offset

**Returns:**
- Dictionary with the text snippet and actual start/end positions

**Example:**
```python
# Model calls: peek(start=0, end=500)
# Returns: {"text": "Document content...", "start": 0, "end": 500}
```

## Benefits

1. **Token Efficiency**: Only relevant portions of the document are sent to the model
2. **Large Documents**: Handle documents that exceed context window limits
3. **Dynamic Retrieval**: Model decides what information it needs
4. **Cost Effective**: Reduced token usage means lower API costs
5. **Flexible**: Works with any text document format

## Use Cases

- **Document Q&A**: Answer questions about large technical documents, manuals, or reports
- **Legal Document Analysis**: Search and extract information from contracts or legal texts
- **Research Papers**: Summarize or query scientific papers
- **Code Documentation**: Navigate and explain large codebases
- **Knowledge Base**: Build a conversational interface for your documentation

## SDK Features

The RLM SDK provides a simple, intuitive interface for building recursive language model applications:

### Core Classes

- **`RLMClient`**: Main client for querying documents
- **`RLMDocument`**: Document wrapper with search and peek capabilities
- **`quick_query()`**: Convenience function for one-off queries

### Key Methods

```python
# RLMClient methods
client = RLMClient(api_key=None, model="gpt-4o-mini", max_iterations=10)
client.load_document_from_file(filepath)
client.load_document_from_text(text, name)
client.load_document(document)
client.query(question, system_message=None, verbose=False)
client.get_document_info()

# RLMDocument methods
doc = RLMDocument(content, name)
doc = RLMDocument.from_file(filepath, encoding="utf-8")
doc.search(pattern, max_hits=10)
doc.peek(start, end)
```

### Example Usage

See the `examples/` directory for complete examples:

- `basic_usage.py` - Simple document Q&A
- `multiple_queries.py` - Ask multiple questions
- `custom_processing.py` - Advanced customization
- `file_loading.py` - Different file loading methods
- `quick_usage.py` - One-liner usage

## Project Structure

```
RLM/
├── README.md              # This file
├── setup.py              # Package setup
├── rlm_sdk.py            # Main SDK implementation
├── examples/             # Example scripts
│   ├── README.md
│   ├── basic_usage.py
│   ├── multiple_queries.py
│   ├── custom_processing.py
│   ├── file_loading.py
│   └── quick_usage.py
└── tests/                # Unit tests (future)
```

## Limitations

- Requires OpenAI API access and API key
- Document must fit in memory (loaded as string)
- Search uses regex, which has limitations for semantic search
- Tool calling adds latency to responses

## Future Enhancements

- [ ] Add semantic search capabilities with embeddings
- [ ] Support multiple documents
- [ ] Implement caching for frequent queries
- [ ] Add document preprocessing and chunking strategies
- [ ] Support streaming responses
- [ ] Add more sophisticated recursive search strategies (BM25, vector search)

## Documentation

- 📘 **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- 📗 **[API Documentation](API.md)** - Complete API reference
- 📙 **[Integration Guide](INTEGRATION.md)** - Integration patterns and examples
- 📕 **[Package Summary](PACKAGE_SUMMARY.md)** - Complete package overview
- 📂 **[Examples Directory](examples/)** - Working code examples

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this code for your projects.

## References

- [OpenAI Function Calling Documentation](https://platform.openai.com/docs/guides/function-calling)
- [Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401)
- [arXiv Paper: Recursive Language Models](https://arxiv.org/html/2512.24601v1)

---

**Note**: This implementation uses the OpenAI Responses API with `gpt-4.1-mini` model. Make sure to check the current API documentation for the latest model names and API endpoints.