# 🎯 Start Here - RLM SDK Complete Guide

Welcome to the RLM (Recursive Language Model) SDK! This guide will help you get started quickly.

## 🚀 What is RLM?

RLM is a Python SDK that lets you query large documents using AI **without loading the entire document** into the AI's context. It's like giving the AI a search tool and letting it find the information it needs!

### Why is this useful?

- 💰 **Saves Money**: Only processes relevant parts of documents
- ⚡ **Faster**: Less data to send = faster responses
- 📚 **Handles Large Docs**: Works with documents larger than AI context limits
- 🎯 **More Accurate**: AI focuses on relevant information

## ⚡ Quick Start (2 minutes)

### 1. Install

```bash
pip install openai
```

### 2. Set API Key

```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 3. Run Demo

```bash
python demo.py
```

### 4. Try Your Own Document

```python
from rlm_sdk import quick_query

answer = quick_query("your_document.txt", "What is this about?")
print(answer)
```

**That's it!** 🎉

## 📖 Documentation Structure

We have organized documentation for different needs:

### 🟢 Beginners Start Here:

1. **[QUICKSTART.md](QUICKSTART.md)** ⭐ (5 min read)
   - Step-by-step tutorial
   - Simple examples
   - Common patterns
   
2. **[examples/](examples/)** ⭐ (Try these!)
   - `basic_usage.py` - Start here
   - `quick_usage.py` - One-liner example
   - `multiple_queries.py` - Multiple questions
   - `file_loading.py` - Loading documents
   - `custom_processing.py` - Advanced usage

3. **[demo.py](demo.py)** ⭐ (Run this!)
   - Interactive demonstration
   - Shows all features

### 🟡 Building Applications:

4. **[README.md](README.md)** (15 min read)
   - Complete overview
   - Architecture explanation
   - All features documented
   
5. **[INTEGRATION.md](INTEGRATION.md)** (20 min read)
   - Integration patterns
   - Flask/FastAPI examples
   - Production tips
   - Best practices

### 🔴 Reference Material:

6. **[API.md](API.md)** (Reference)
   - Complete API documentation
   - Every class, method, function
   - Parameter descriptions
   - Error handling

7. **[PACKAGE_SUMMARY.md](PACKAGE_SUMMARY.md)** (Overview)
   - What's included
   - File structure
   - Technical specs

## 📁 What's in the Package?

```
RLM/
├── 📘 START_HERE.md          ← You are here!
├── 📗 QUICKSTART.md          ← Read this next
├── 📙 README.md              ← Main documentation
├── 📕 API.md                 ← API reference
├── 📓 INTEGRATION.md         ← Integration guide
├── 📔 PACKAGE_SUMMARY.md     ← Package overview
│
├── 🐍 rlm_sdk.py             ← Main SDK code
├── 🎬 demo.py                ← Run this demo!
│
├── 📁 examples/              ← Example scripts
│   ├── basic_usage.py
│   ├── quick_usage.py
│   ├── multiple_queries.py
│   ├── file_loading.py
│   └── custom_processing.py
│
├── ⚙️  setup.py              ← Package installer
├── 📋 requirements.txt       ← Dependencies
├── 📄 LICENSE                ← MIT License
└── 🙈 .gitignore            ← Git ignore file
```

## 🎓 Learning Path

Choose your path based on your goal:

### Path 1: "I just want to try it!" 
⏱️ **5 minutes**

1. Install: `pip install openai`
2. Set key: `export OPENAI_API_KEY='sk-...'`
3. Run: `python demo.py`
4. Try: `python examples/basic_usage.py`

### Path 2: "I want to understand it"
⏱️ **20 minutes**

1. Read: [QUICKSTART.md](QUICKSTART.md)
2. Read: [README.md](README.md) - Overview section
3. Run: All examples in `examples/`
4. Experiment with your own documents

### Path 3: "I want to build with it"
⏱️ **45 minutes**

1. Read: [QUICKSTART.md](QUICKSTART.md)
2. Read: [README.md](README.md) - Complete
3. Read: [INTEGRATION.md](INTEGRATION.md)
4. Bookmark: [API.md](API.md) for reference
5. Build your application!

### Path 4: "I need the full reference"
⏱️ **On-demand**

1. Skim: [README.md](README.md)
2. Reference: [API.md](API.md) as needed
3. Reference: [INTEGRATION.md](INTEGRATION.md) for patterns

## 💻 Common Use Cases

### 1. Document Q&A

```python
from rlm_sdk import RLMClient

client = RLMClient()
client.load_document_from_file("manual.pdf.txt")
answer = client.query("How do I install this?")
print(answer)
```

### 2. Batch Processing

```python
from rlm_sdk import RLMClient

client = RLMClient()

for doc_path in document_list:
    client.load_document_from_file(doc_path)
    summary = client.query("Summarize in 3 sentences")
    save_summary(doc_path, summary)
```

### 3. REST API

```python
from flask import Flask, request, jsonify
from rlm_sdk import RLMClient

app = Flask(__name__)
client = RLMClient()

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    client.load_document_from_file(data['document'])
    answer = client.query(data['question'])
    return jsonify({'answer': answer})
```

### 4. CLI Tool

```bash
# Create query.py
from rlm_sdk import quick_query
import sys
print(quick_query(sys.argv[1], sys.argv[2]))

# Use it
python query.py document.txt "What is this about?"
```

## 🔧 Installation Options

### Option 1: Direct Use (Recommended for trying)

```bash
git clone https://github.com/damodharm10/RLM.git
cd RLM
pip install -r requirements.txt
python demo.py
```

### Option 2: Package Install (Recommended for projects)

```bash
cd RLM
pip install -e .
```

Then use anywhere:
```python
from rlm_sdk import RLMClient
```

## 🎯 Key Concepts

### How it works:

1. **You load a document** into the SDK
2. **You ask a question** about the document
3. **The AI searches** the document for relevant parts
4. **The AI reads** only the relevant parts
5. **The AI answers** your question

### Why this is better:

- ❌ **Traditional**: Send entire 50-page document (expensive, slow)
- ✅ **RLM**: AI searches and reads only relevant 2 pages (cheap, fast)

## 🛠️ Troubleshooting

### Problem: "No module named 'rlm_sdk'"

```bash
# Make sure rlm_sdk.py is in your directory or Python path
# Or install as package:
pip install -e .
```

### Problem: "API key not found"

```bash
# Set environment variable
export OPENAI_API_KEY='sk-...'

# Or pass directly
client = RLMClient(api_key='sk-...')
```

### Problem: "No document loaded"

```python
# Must load document before querying
client = RLMClient()
client.load_document_from_file("doc.txt")  # ← Don't forget this!
answer = client.query("Question?")
```

### Problem: Slow responses

- Use `gpt-4o-mini` instead of `gpt-4o`
- Ask more specific questions
- Enable verbose mode to see what's happening

## 📞 Getting Help

1. **Check the documentation**:
   - [QUICKSTART.md](QUICKSTART.md) for basics
   - [API.md](API.md) for reference
   - [INTEGRATION.md](INTEGRATION.md) for patterns

2. **Run the examples**: `examples/` directory

3. **Run the demo**: `python demo.py`

4. **GitHub Issues**: Report bugs or ask questions

## 🎉 You're Ready!

### Next Steps:

1. ✅ Run `python demo.py`
2. ✅ Read [QUICKSTART.md](QUICKSTART.md)
3. ✅ Try examples in `examples/`
4. ✅ Build something awesome!

## 🌟 Quick Reference Card

```python
# Import
from rlm_sdk import RLMClient, quick_query

# Quick one-liner
answer = quick_query("doc.txt", "Question?")

# Full client
client = RLMClient()
client.load_document_from_file("doc.txt")
answer = client.query("Question?")

# Multiple questions
for q in questions:
    print(client.query(q))

# Verbose mode (see tool calls)
answer = client.query("Question?", verbose=True)

# Document info
info = client.get_document_info()
```

## 📚 Further Reading

- **OpenAI Function Calling**: https://platform.openai.com/docs/guides/function-calling
- **RAG Paper**: https://arxiv.org/abs/2005.11401
- **RLM Research**: https://arxiv.org/html/2512.24601v1

---

## 🚀 Ready to Start?

Choose your next step:

- 🟢 **Beginner**: Run `python demo.py` then read [QUICKSTART.md](QUICKSTART.md)
- 🟡 **Developer**: Read [README.md](README.md) then [INTEGRATION.md](INTEGRATION.md)
- 🔴 **Expert**: Dive into [API.md](API.md) and start building

**Welcome to RLM! Happy coding!** 🎉

---

*Need help? Open an issue on GitHub or check the documentation!*
