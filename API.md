# RLM SDK API Documentation

Complete API reference for the RLM SDK.

## Table of Contents

- [RLMClient](#rlmclient)
- [RLMDocument](#rlmdocument)
- [Convenience Functions](#convenience-functions)

---

## RLMClient

The main client class for interacting with the Recursive Language Model.

### Constructor

```python
RLMClient(api_key=None, model="gpt-4o-mini", max_iterations=10)
```

**Parameters:**
- `api_key` (str, optional): OpenAI API key. If not provided, uses `OPENAI_API_KEY` environment variable.
- `model` (str): OpenAI model to use. Default: `"gpt-4o-mini"`
- `max_iterations` (int): Maximum number of tool-calling iterations. Default: `10`

**Example:**
```python
client = RLMClient()  # Use defaults
# or
client = RLMClient(
    api_key="sk-...",
    model="gpt-4o",
    max_iterations=15
)
```

---

### Methods

#### `load_document(document)`

Load an RLMDocument for querying.

**Parameters:**
- `document` (RLMDocument): The document to load

**Example:**
```python
doc = RLMDocument("content", "name")
client.load_document(doc)
```

---

#### `load_document_from_file(filepath, encoding="utf-8")`

Load a document directly from a file.

**Parameters:**
- `filepath` (str): Path to the document file
- `encoding` (str): File encoding. Default: `"utf-8"`

**Example:**
```python
client.load_document_from_file("document.txt")
```

---

#### `load_document_from_text(text, name="document")`

Load a document from a text string.

**Parameters:**
- `text` (str): The document text
- `name` (str): A name for the document. Default: `"document"`

**Example:**
```python
client.load_document_from_text("Document content...", "MyDoc")
```

---

#### `query(question, system_message=None, verbose=False)`

Query the loaded document with a question.

**Parameters:**
- `question` (str): The question to ask
- `system_message` (str, optional): Custom system message for the AI
- `verbose` (bool): Print debug information. Default: `False`

**Returns:**
- `str`: The AI's answer

**Raises:**
- `ValueError`: If no document is loaded

**Example:**
```python
answer = client.query("What is the main topic?")
# or with custom system message
answer = client.query(
    "Summarize the key points",
    system_message="You are a technical writer.",
    verbose=True
)
```

---

#### `get_document_info()`

Get information about the currently loaded document.

**Returns:**
- `dict`: Document information with keys:
  - `loaded` (bool): Whether a document is loaded
  - `name` (str): Document name (if loaded)
  - `length` (int): Document length in characters (if loaded)
  - `lines` (int): Number of lines (if loaded)

**Example:**
```python
info = client.get_document_info()
print(f"Document: {info['name']}, {info['length']} chars")
```

---

## RLMDocument

Represents a document that can be queried by the RLM.

### Constructor

```python
RLMDocument(content, name="document")
```

**Parameters:**
- `content` (str): The text content of the document
- `name` (str): A name for the document. Default: `"document"`

**Example:**
```python
doc = RLMDocument("Document text here", "MyDocument")
```

---

### Class Methods

#### `from_file(filepath, encoding="utf-8")`

Load a document from a file.

**Parameters:**
- `filepath` (str): Path to the document file
- `encoding` (str): File encoding. Default: `"utf-8"`

**Returns:**
- `RLMDocument`: New document instance

**Example:**
```python
doc = RLMDocument.from_file("document.txt")
```

---

### Instance Methods

#### `search(pattern, max_hits=10, flags=re.IGNORECASE)`

Search for a regex pattern in the document.

**Parameters:**
- `pattern` (str): Regular expression pattern
- `max_hits` (int): Maximum number of matches. Default: `10`
- `flags` (int): Regex flags. Default: `re.IGNORECASE`

**Returns:**
- `list[dict]`: List of hits with `start` and `end` offsets

**Example:**
```python
hits = doc.search(r"chapter \d+", max_hits=5)
for hit in hits:
    print(f"Found at {hit['start']}-{hit['end']}")
```

---

#### `peek(start, end)`

Retrieve a substring from the document.

**Parameters:**
- `start` (int): Starting byte offset
- `end` (int): Ending byte offset

**Returns:**
- `dict`: Dictionary with:
  - `text` (str): The extracted text
  - `start` (int): Actual start position (bounded)
  - `end` (int): Actual end position (bounded)

**Example:**
```python
snippet = doc.peek(0, 100)
print(snippet['text'])
```

---

### Properties

- `content` (str): The full document text
- `name` (str): The document name
- `length` (int): The document length in characters

---

## Convenience Functions

### `quick_query(document_path, question, api_key=None, verbose=False)`

Quick function to query a document without setting up the client manually.

**Parameters:**
- `document_path` (str): Path to the document file
- `question` (str): Question to ask
- `api_key` (str, optional): OpenAI API key
- `verbose` (bool): Print debug information. Default: `False`

**Returns:**
- `str`: The answer

**Example:**
```python
from rlm_sdk import quick_query

answer = quick_query("doc.txt", "What is this about?")
print(answer)
```

---

## Error Handling

### Common Errors

#### `ValueError: No document loaded`
**Cause:** Attempting to query before loading a document  
**Solution:** Call `load_document()` or related methods first

```python
client = RLMClient()
client.load_document_from_file("doc.txt")  # Must load first
answer = client.query("Question?")
```

#### `openai.OpenAIError: API key not found`
**Cause:** OpenAI API key not set  
**Solution:** Set the `OPENAI_API_KEY` environment variable or pass it to the constructor

```python
# Option 1: Environment variable
import os
os.environ["OPENAI_API_KEY"] = "sk-..."

# Option 2: Constructor
client = RLMClient(api_key="sk-...")
```

#### `FileNotFoundError`
**Cause:** Document file doesn't exist  
**Solution:** Check the file path

```python
import os
if os.path.exists("doc.txt"):
    client.load_document_from_file("doc.txt")
```

---

## Advanced Usage

### Custom Tool Execution

The SDK internally uses two tools:

1. **search**: Finds regex patterns in the document
2. **peek**: Retrieves document sections

These are automatically handled, but you can use the document methods directly:

```python
doc = RLMDocument.from_file("doc.txt")

# Direct search
results = doc.search(r"important.*topic")

# Direct peek
text = doc.peek(100, 500)
```

### Multiple Documents

To query multiple documents, simply switch documents:

```python
client = RLMClient()

# Query first document
client.load_document_from_file("doc1.txt")
answer1 = client.query("Question about doc1?")

# Switch to second document
client.load_document_from_file("doc2.txt")
answer2 = client.query("Question about doc2?")
```

### Custom System Messages

Customize the AI's behavior with system messages:

```python
legal_system_msg = """You are a legal expert. 
Analyze documents carefully and cite specific sections."""

client.query(
    "What are the termination clauses?",
    system_message=legal_system_msg
)
```

### Verbose Mode

Enable verbose mode to see the tool-calling process:

```python
answer = client.query("Question?", verbose=True)
# Output:
# [RLM] Querying document 'doc.txt' (length: 5000 chars)
# [RLM] Question: Question?
# [RLM] Tool call: search({'pattern': '...'})
# [RLM] Tool result: {'hits': [...]}
# [RLM] Tool call: peek({'start': 100, 'end': 500})
# [RLM] Tool result: {'text': '...'}
# [RLM] Completed in 2 iteration(s)
```

---

## Best Practices

### 1. Document Size
- Works best with documents up to several MB
- For very large documents, consider chunking or pre-processing

### 2. Question Formulation
- Be specific in your questions
- The AI will search for relevant information
- Multiple questions can be more efficient than one complex question

### 3. System Messages
- Use custom system messages for domain-specific queries
- Examples: legal analysis, technical documentation, code review

### 4. Error Handling
```python
try:
    client = RLMClient()
    client.load_document_from_file("doc.txt")
    answer = client.query("Question?")
except FileNotFoundError:
    print("Document not found")
except ValueError as e:
    print(f"Error: {e}")
```

### 5. Resource Management
- The client can be reused for multiple queries
- Switch documents by calling `load_document()` again
- No need to recreate the client for each query

---

## Performance Tips

1. **Reuse client instances**: Create once, query multiple times
2. **Batch questions**: Ask multiple questions about the same document
3. **Use appropriate models**: `gpt-4o-mini` is faster and cheaper
4. **Adjust max_iterations**: Increase for complex documents
5. **Enable verbose mode during development**: Understand tool usage patterns

---

## Version History

- **v0.1.0** (2026-01-24): Initial release
  - Basic RLM functionality
  - Document loading and querying
  - Search and peek tools
  - Example scripts

---

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/damodharm10/RLM
- Issues: https://github.com/damodharm10/RLM/issues

---

*Last updated: January 24, 2026*
