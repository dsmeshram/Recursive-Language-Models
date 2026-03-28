# RLM SDK - Integration Guide

## What is RLM SDK?

The RLM (Recursive Language Model) SDK is a Python library that makes it easy to query large documents using AI without loading the entire document into the context window. It uses a tool-based approach where the AI can search and peek into documents dynamically.

## Why Use RLM SDK?

✅ **Easy Integration** - Simple API, works out of the box  
✅ **Token Efficient** - Only retrieves relevant document parts  
✅ **Cost Effective** - Reduces API costs significantly  
✅ **Handles Large Docs** - Works with documents exceeding context limits  
✅ **Flexible** - Customizable system messages and settings  

## Installation

```bash
# Clone the repository
git clone https://github.com/damodharm10/RLM.git
cd RLM

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

## Basic Integration

### 1. Import the SDK

```python
from rlm_sdk import RLMClient
```

### 2. Initialize Client

```python
client = RLMClient()
```

### 3. Load a Document

```python
# Option A: From file
client.load_document_from_file("document.txt")

# Option B: From text
text = "Your document content..."
client.load_document_from_text(text, "MyDoc")
```

### 4. Query the Document

```python
answer = client.query("What is the main topic?")
print(answer)
```

## Complete Example

```python
from rlm_sdk import RLMClient

# Initialize
client = RLMClient(model="gpt-4o-mini")

# Load document
client.load_document_from_file("research_paper.pdf.txt")

# Ask multiple questions
questions = [
    "What is the research hypothesis?",
    "What methodology was used?",
    "What are the main findings?"
]

for q in questions:
    print(f"Q: {q}")
    answer = client.query(q)
    print(f"A: {answer}\n")
```

## Integration Patterns

### Pattern 1: Single Question, Single Document

```python
from rlm_sdk import quick_query

# One-liner
answer = quick_query("document.txt", "What is this about?")
```

**Use Case:** Quick queries, scripts, automation

---

### Pattern 2: Multiple Questions, Single Document

```python
from rlm_sdk import RLMClient

client = RLMClient()
client.load_document_from_file("manual.txt")

# Ask multiple questions efficiently
for question in question_list:
    answer = client.query(question)
    process_answer(answer)
```

**Use Case:** Document analysis, Q&A systems

---

### Pattern 3: Multiple Documents

```python
from rlm_sdk import RLMClient

client = RLMClient()

for doc_path in document_list:
    client.load_document_from_file(doc_path)
    info = client.get_document_info()
    
    answer = client.query("Summarize key points")
    save_summary(info['name'], answer)
```

**Use Case:** Batch processing, document comparison

---

### Pattern 4: Custom Domain Expert

```python
from rlm_sdk import RLMClient

client = RLMClient()
client.load_document_from_file("contract.txt")

# Custom system message for legal analysis
legal_system = """You are a legal expert. Analyze contracts carefully, 
cite specific clauses, and identify potential risks."""

answer = client.query(
    "What are the termination conditions?",
    system_message=legal_system
)
```

**Use Case:** Domain-specific analysis (legal, medical, technical)

---

## API Integration Examples

### Flask Web Service

```python
from flask import Flask, request, jsonify
from rlm_sdk import RLMClient

app = Flask(__name__)
client = RLMClient()

@app.route('/load', methods=['POST'])
def load_document():
    doc_path = request.json['document_path']
    client.load_document_from_file(doc_path)
    return jsonify({"status": "loaded", "info": client.get_document_info()})

@app.route('/query', methods=['POST'])
def query_document():
    question = request.json['question']
    answer = client.query(question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Service

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rlm_sdk import RLMClient

app = FastAPI()
client = RLMClient()

class QueryRequest(BaseModel):
    question: str
    document_path: str = None

@app.post("/query")
async def query(req: QueryRequest):
    try:
        if req.document_path:
            client.load_document_from_file(req.document_path)
        
        answer = client.query(req.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### CLI Tool

```python
#!/usr/bin/env python3
import argparse
from rlm_sdk import quick_query

def main():
    parser = argparse.ArgumentParser(description='Query documents with RLM')
    parser.add_argument('document', help='Path to document')
    parser.add_argument('question', help='Question to ask')
    parser.add_argument('-v', '--verbose', action='store_true')
    
    args = parser.parse_args()
    
    answer = quick_query(args.document, args.question, verbose=args.verbose)
    print(answer)

if __name__ == '__main__':
    main()
```

Usage:
```bash
python query_cli.py document.txt "What is the main topic?"
```

---

## Advanced Integration

### Custom Document Processing

```python
from rlm_sdk import RLMDocument, RLMClient

class CustomDocument(RLMDocument):
    def preprocess(self):
        # Custom preprocessing logic
        self.content = self.content.lower()
        return self
    
    def highlight_keywords(self, keywords):
        for keyword in keywords:
            self.content = self.content.replace(
                keyword, 
                f"**{keyword}**"
            )
        return self

# Use custom document
doc = CustomDocument.from_file("doc.txt")
doc.preprocess().highlight_keywords(["important", "critical"])

client = RLMClient()
client.load_document(doc)
```

### Caching Results

```python
from functools import lru_cache
from rlm_sdk import RLMClient

class CachedRLMClient:
    def __init__(self):
        self.client = RLMClient()
    
    @lru_cache(maxsize=128)
    def cached_query(self, doc_path: str, question: str):
        self.client.load_document_from_file(doc_path)
        return self.client.query(question)

# Use cached client
cached_client = CachedRLMClient()
answer1 = cached_client.cached_query("doc.txt", "Question?")  # API call
answer2 = cached_client.cached_query("doc.txt", "Question?")  # From cache
```

### Streaming Responses (Future Feature)

```python
# Planned for future versions
for chunk in client.query_stream("Long question?"):
    print(chunk, end='', flush=True)
```

---

## Configuration Options

### Environment Variables

```bash
# Required
export OPENAI_API_KEY='sk-...'

# Optional
export RLM_DEFAULT_MODEL='gpt-4o-mini'
export RLM_MAX_ITERATIONS='10'
export RLM_VERBOSE='false'
```

### Client Configuration

```python
client = RLMClient(
    api_key="sk-...",           # OpenAI API key
    model="gpt-4o-mini",        # Model to use
    max_iterations=10            # Max tool calling loops
)
```

---

## Error Handling Best Practices

```python
from rlm_sdk import RLMClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_query(doc_path: str, question: str):
    try:
        client = RLMClient()
        client.load_document_from_file(doc_path)
        return client.query(question)
    
    except FileNotFoundError:
        logger.error(f"Document not found: {doc_path}")
        return None
    
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return None
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

---

## Testing Your Integration

```python
import unittest
from rlm_sdk import RLMClient, RLMDocument

class TestRLMIntegration(unittest.TestCase):
    def setUp(self):
        self.client = RLMClient()
        self.test_doc = "Test document content"
    
    def test_load_document(self):
        self.client.load_document_from_text(self.test_doc)
        info = self.client.get_document_info()
        self.assertTrue(info['loaded'])
    
    def test_query(self):
        self.client.load_document_from_text(self.test_doc)
        answer = self.client.query("What is this?")
        self.assertIsInstance(answer, str)
        self.assertGreater(len(answer), 0)

if __name__ == '__main__':
    unittest.main()
```

---

## Performance Considerations

### Token Usage

```python
# Efficient: Specific question
answer = client.query("What is the publication date?")

# Less efficient: Broad question
answer = client.query("Tell me everything about this document")
```

### Model Selection

- **gpt-4o-mini**: Fast, cheap, good for most use cases
- **gpt-4o**: More capable, better for complex analysis
- **gpt-3.5-turbo**: Budget option (may need more iterations)

### Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor

def process_document(doc_path):
    client = RLMClient()
    client.load_document_from_file(doc_path)
    return client.query("Summarize")

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process_document, document_paths)
```

---

## Migration Guide

### From Original Implementation

**Before:**
```python
DOC = open("document.txt").read()
answer = run_rlm("What is this about?")
```

**After:**
```python
from rlm_sdk import quick_query
answer = quick_query("document.txt", "What is this about?")
```

---

## Troubleshooting

### Issue: Slow responses
**Solution:** Use `gpt-4o-mini`, reduce `max_iterations`, or ask more specific questions

### Issue: Incomplete answers
**Solution:** Increase `max_iterations`, enable `verbose=True` to debug

### Issue: High costs
**Solution:** Use `gpt-4o-mini`, cache frequently asked questions

### Issue: Module not found
**Solution:** Ensure `rlm_sdk.py` is in your Python path or install package

---

## Production Checklist

- [ ] API key secured (environment variable or secrets manager)
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Rate limiting considered
- [ ] Document size limits enforced
- [ ] Caching implemented for common queries
- [ ] Monitoring and alerting set up
- [ ] Cost tracking enabled
- [ ] User input validation
- [ ] Timeout handling

---

## Resources

- **Full Documentation**: `README.md`
- **API Reference**: `API.md`
- **Quick Start**: `QUICKSTART.md`
- **Examples**: `examples/` directory
- **Source Code**: `rlm_sdk.py`

---

## Support

- GitHub Issues: https://github.com/damodharm10/RLM/issues
- Discussions: https://github.com/damodharm10/RLM/discussions

---

**Ready to integrate? Start with the Quick Start guide and explore the examples!** 🚀
