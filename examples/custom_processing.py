"""
Custom Processing Example
Shows advanced usage with custom document handling and settings.
"""

from rlm_sdk import RLMClient, RLMDocument
import os

def main():
    # Load document from file
    legal_document = """
    SOFTWARE LICENSE AGREEMENT
    
    This Agreement is entered into on January 24, 2026.
    
    1. GRANT OF LICENSE
    Subject to the terms of this Agreement, Licensor grants to Licensee a
    non-exclusive, non-transferable license to use the Software.
    
    2. RESTRICTIONS
    Licensee shall not:
    a) Reverse engineer, decompile, or disassemble the Software
    b) Rent, lease, or lend the Software
    c) Remove any proprietary notices from the Software
    
    3. TERM AND TERMINATION
    This Agreement is effective until terminated. Licensor may terminate this
    Agreement if Licensee breaches any terms.
    
    4. WARRANTY DISCLAIMER
    THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
    
    5. LIMITATION OF LIABILITY
    IN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY DAMAGES ARISING FROM THE USE
    OF THE SOFTWARE.
    """
    
    # Create a custom RLMDocument
    doc = RLMDocument(legal_document, name="License_Agreement")
    
    # Initialize client with custom settings
    client = RLMClient(
        model="gpt-4o-mini",  # Specify model
        max_iterations=15      # Allow more iterations if needed
    )
    
    # Load the custom document
    client.load_document(doc)
    
    # Get document information
    info = client.get_document_info()
    print("Document Information:")
    print(f"  Name: {info['name']}")
    print(f"  Length: {info['length']} characters")
    print(f"  Lines: {info['lines']}")
    print("\n" + "="*60 + "\n")
    
    # Custom system message for legal analysis
    custom_system_message = """You are a legal document analyzer. 
    You cannot see the full document. Use the 'search' and 'peek' tools to 
    examine the document and provide accurate legal information. 
    Be precise and cite specific sections when possible."""
    
    # Query with custom system message
    questions = [
        "What are the main restrictions on the licensee?",
        "What happens if the licensee breaches the agreement?",
        "Is there any warranty provided?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question}")
        answer = client.query(
            question,
            system_message=custom_system_message,
            verbose=False
        )
        print(f"Answer: {answer}\n")
        print("-"*60 + "\n")
    
    # Demonstrate direct document methods
    print("Direct Document Search:")
    search_results = doc.search(r"shall not", max_hits=5)
    print(f"Found {len(search_results)} occurrences of 'shall not'")
    
    if search_results:
        # Peek around the first occurrence
        first_hit = search_results[0]
        context = doc.peek(first_hit['start'] - 50, first_hit['end'] + 100)
        print(f"\nContext around first occurrence:")
        print(f"'{context['text']}'")

if __name__ == "__main__":
    main()
