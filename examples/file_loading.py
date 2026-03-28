"""
File Loading Example
Demonstrates different ways to load documents from files.
"""

from rlm_sdk import RLMClient, RLMDocument
import os

def create_sample_files():
    """Create sample files for demonstration."""
    files = {
        "sample1.txt": """
        Introduction to Python
        
        Python is a high-level, interpreted programming language known for its
        simplicity and readability. Created by Guido van Rossum in 1991.
        
        Key Features:
        - Easy to learn and use
        - Extensive standard library
        - Large community support
        - Cross-platform compatibility
        """,
        
        "sample2.txt": """
        Recipe: Chocolate Chip Cookies
        
        Ingredients:
        - 2 cups all-purpose flour
        - 1 cup butter, softened
        - 3/4 cup sugar
        - 2 eggs
        - 1 tsp vanilla extract
        - 2 cups chocolate chips
        
        Instructions:
        1. Preheat oven to 375°F
        2. Mix butter and sugar until creamy
        3. Add eggs and vanilla
        4. Gradually blend in flour
        5. Stir in chocolate chips
        6. Bake for 10-12 minutes
        """
    }
    
    for filename, content in files.items():
        with open(filename, "w") as f:
            f.write(content)
    
    return list(files.keys())

def main():
    # Create sample files
    files = create_sample_files()
    print("Created sample files:", files)
    print("\n" + "="*60 + "\n")
    
    try:
        # Method 1: Using RLMClient.load_document_from_file()
        print("METHOD 1: Direct file loading with client")
        print("-"*60)
        client1 = RLMClient()
        client1.load_document_from_file("sample1.txt")
        
        answer1 = client1.query("Who created Python and when?")
        print(f"Answer: {answer1}\n")
        
        # Method 2: Using RLMDocument.from_file()
        print("METHOD 2: Loading through RLMDocument")
        print("-"*60)
        doc2 = RLMDocument.from_file("sample2.txt")
        
        client2 = RLMClient()
        client2.load_document(doc2)
        
        answer2 = client2.query("What temperature should the oven be?")
        print(f"Answer: {answer2}\n")
        
        # Method 3: Switching documents
        print("METHOD 3: Switching between documents")
        print("-"*60)
        client3 = RLMClient()
        
        # Load first document
        client3.load_document_from_file("sample1.txt")
        print(f"Loaded: {client3.get_document_info()['name']}")
        answer3a = client3.query("What is Python?")
        print(f"Answer: {answer3a}\n")
        
        # Switch to second document
        client3.load_document_from_file("sample2.txt")
        print(f"Switched to: {client3.get_document_info()['name']}")
        answer3b = client3.query("What are the ingredients?")
        print(f"Answer: {answer3b}\n")
        
    finally:
        # Cleanup
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        print("\nCleaned up sample files")

if __name__ == "__main__":
    main()
