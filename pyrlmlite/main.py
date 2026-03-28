"""
RLM SDK - Recursive Language Model SDK
A simple SDK for building recursive language models with OpenAI.
"""

import os
import re
import json
from typing import Optional, List, Dict, Any, Callable
from openai import OpenAI


class RLMDocument:
    """Represents a document that can be queried by the RLM."""
    
    def __init__(self, content: str, name: str = "document"):
        """
        Initialize a document.
        
        Args:
            content: The text content of the document
            name: A name for the document (for reference)
        """
        self.content = content
        self.name = name
        self.length = len(content)
    
    @classmethod
    def from_file(cls, filepath: str, encoding: str = "utf-8"):
        """
        Load a document from a file.
        
        Args:
            filepath: Path to the document file
            encoding: File encoding (default: utf-8)
            
        Returns:
            RLMDocument instance
        """
        with open(filepath, "r", encoding=encoding) as f:
            content = f.read()
        name = os.path.basename(filepath)
        return cls(content, name)
    
    def search(self, pattern: str, max_hits: int = 10, flags: int = re.IGNORECASE) -> List[Dict[str, int]]:
        """
        Search for a regex pattern in the document.
        
        Args:
            pattern: Regular expression pattern to search for
            max_hits: Maximum number of matches to return
            flags: Regex flags (default: re.IGNORECASE)
            
        Returns:
            List of dicts with 'start' and 'end' offsets
        """
        hits = []
        for m in re.finditer(pattern, self.content, flags=flags):
            hits.append({"start": m.start(), "end": m.end()})
            if len(hits) >= max_hits:
                break
        return hits
    
    def peek(self, start: int, end: int) -> Dict[str, Any]:
        """
        Retrieve a substring from the document.
        
        Args:
            start: Starting byte offset
            end: Ending byte offset
            
        Returns:
            Dict with 'text', 'start', and 'end'
        """
        start = max(0, start)
        end = min(self.length, end)
        return {
            "text": self.content[start:end],
            "start": start,
            "end": end
        }


class RLMClient:
    """Main client for interacting with the Recursive Language Model."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        max_iterations: int = 10
    ):
        """
        Initialize the RLM client.
        
        Args:
            api_key: OpenAI API key (if not provided, uses OPENAI_API_KEY env var)
            model: OpenAI model to use (default: gpt-4o-mini)
            max_iterations: Maximum number of tool-calling iterations
        """
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.model = model
        self.max_iterations = max_iterations
        self.document: Optional[RLMDocument] = None
        self._tools = self._create_tools()
    
    def _create_tools(self) -> List[Dict[str, Any]]:
        """Create the tool definitions for OpenAI API."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search",
                    "description": "Find locations of a regex/text pattern in the document. Returns start/end offsets.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": "Regular expression pattern to search for"
                            },
                            "max_hits": {
                                "type": "integer",
                                "default": 10,
                                "description": "Maximum number of matches to return"
                            }
                        },
                        "required": ["pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "peek",
                    "description": "Return document substring for [start,end). Keep end-start small (e.g., <= 2000 chars).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "start": {
                                "type": "integer",
                                "description": "Starting byte offset"
                            },
                            "end": {
                                "type": "integer",
                                "description": "Ending byte offset"
                            }
                        },
                        "required": ["start", "end"]
                    }
                }
            }
        ]
    
    def load_document(self, document: RLMDocument):
        """
        Load a document for querying.
        
        Args:
            document: RLMDocument instance to load
        """
        self.document = document
    
    def load_document_from_file(self, filepath: str, encoding: str = "utf-8"):
        """
        Load a document from a file.
        
        Args:
            filepath: Path to the document file
            encoding: File encoding (default: utf-8)
        """
        self.document = RLMDocument.from_file(filepath, encoding)
    
    def load_document_from_text(self, text: str, name: str = "document"):
        """
        Load a document from a text string.
        
        Args:
            text: The document text
            name: A name for the document
        """
        self.document = RLMDocument(text, name)
    
    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool ('search' or 'peek')
            args: Arguments for the tool
            
        Returns:
            Tool execution result
        """
        if not self.document:
            raise ValueError("No document loaded. Use load_document() first.")
        
        if tool_name == "search":
            result = {"hits": self.document.search(**args)}
        elif tool_name == "peek":
            result = self.document.peek(**args)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return result
    
    def query(
        self,
        question: str,
        system_message: Optional[str] = None,
        verbose: bool = False
    ) -> str:
        """
        Query the document with a question.
        
        Args:
            question: The question to ask about the document
            system_message: Custom system message (optional)
            verbose: Print debug information
            
        Returns:
            The model's answer as a string
        """
        if not self.document:
            raise ValueError("No document loaded. Use load_document() first.")
        
        if system_message is None:
            system_message = f"You cannot see the document '{self.document.name}'. Use tools 'search' and 'peek' to inspect the document and answer the user's question."
        
        # Initial request
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
        
        if verbose:
            print(f"[RLM] Querying document '{self.document.name}' (length: {self.document.length} chars)")
            print(f"[RLM] Question: {question}")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self._tools,
            tool_choice="auto"
        )
        
        iterations = 0
        
        # Tool calling loop
        while iterations < self.max_iterations:
            iterations += 1
            message = response.choices[0].message
            
            # Check if we have a final answer
            if not message.tool_calls:
                if verbose:
                    print(f"[RLM] Completed in {iterations} iteration(s)")
                return message.content
            
            # Process tool calls
            messages.append(message)
            
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                if verbose:
                    print(f"[RLM] Tool call: {tool_name}({args})")
                
                # Execute the tool
                result = self._execute_tool(tool_name, args)
                
                if verbose:
                    result_preview = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
                    print(f"[RLM] Tool result: {result_preview}")
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result)
                })
            
            # Continue the conversation
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self._tools,
                tool_choice="auto"
            )
        
        if verbose:
            print(f"[RLM] Warning: Reached max iterations ({self.max_iterations})")
        
        # Return best available answer
        return response.choices[0].message.content or "Unable to complete the query within iteration limit."
    
    def get_document_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded document.
        
        Returns:
            Dict with document information
        """
        if not self.document:
            return {"loaded": False}
        
        return {
            "loaded": True,
            "name": self.document.name,
            "length": self.document.length,
            "lines": self.document.content.count('\n') + 1
        }


# Convenience function for quick usage
def quick_query(document_path: str, question: str, api_key: Optional[str] = None, verbose: bool = False) -> str:
    """
    Quick function to query a document without setting up the client manually.
    
    Args:
        document_path: Path to the document file
        question: Question to ask about the document
        api_key: OpenAI API key (optional)
        verbose: Print debug information
        
    Returns:
        The answer as a string
        
    Example:
        answer = quick_query("my_document.txt", "What is the main topic?")
    """
    client = RLMClient(api_key=api_key)
    client.load_document_from_file(document_path)
    return client.query(question, verbose=verbose)


if __name__ == "__main__":
    # Example usage
    print("RLM SDK - Example Usage\n")
    
    # Create a sample document
    sample_text = """
    Machine Learning Fundamentals
    
    Introduction:
    Machine learning is a subset of artificial intelligence that focuses on 
    developing algorithms that can learn from and make predictions on data.
    
    Key Concepts:
    1. Supervised Learning: Learning from labeled data
    2. Unsupervised Learning: Finding patterns in unlabeled data
    3. Reinforcement Learning: Learning through interaction with an environment
    
    Applications:
    - Image recognition
    - Natural language processing
    - Recommendation systems
    - Autonomous vehicles
    """
    
    # Initialize client
    client = RLMClient()
    client.load_document_from_text(sample_text, "ML_Guide")
    
    # Query the document
    print("Document loaded:", client.get_document_info())
    print("\nAsking: 'What are the three types of learning mentioned?'\n")
    
    answer = client.query(
        "What are the three types of learning mentioned?",
        verbose=True
    )
    
    print("\n" + "="*50)
    print("ANSWER:", answer)
    print("="*50)
