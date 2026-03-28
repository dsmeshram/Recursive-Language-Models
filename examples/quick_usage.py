"""
Quick Query Example
Demonstrates the quickest way to query a document using the convenience function.
"""

from rlm_sdk import quick_query
import os

def main():
    # Create a sample document file
    sample_content = """
    Product Manual: SmartHome Hub 3000
    
    Setup Instructions:
    1. Connect the hub to your router using the included ethernet cable
    2. Plug in the power adapter
    3. Download the SmartHome app on your smartphone
    4. Follow the in-app pairing instructions
    
    Features:
    - Voice control with Alexa and Google Assistant
    - Supports up to 100 devices
    - 256-bit encryption for security
    - Automatic firmware updates
    
    Troubleshooting:
    If the hub doesn't connect, try:
    - Restarting your router
    - Ensuring the hub is within 10 feet of the router
    - Checking that your firmware is up to date
    """
    
    # Create a temporary document
    doc_path = "temp_manual.txt"
    with open(doc_path, "w") as f:
        f.write(sample_content)
    
    try:
        print("Using quick_query() for rapid document Q&A\n")
        print("="*60)
        
        # Quick query - one line!
        answer = quick_query(
            doc_path, 
            "What are the setup steps?",
            verbose=True
        )
        
        print("\n" + "="*60)
        print("ANSWER:", answer)
        print("="*60)
        
    finally:
        # Cleanup
        if os.path.exists(doc_path):
            os.remove(doc_path)
            print(f"\nCleaned up temporary file: {doc_path}")

if __name__ == "__main__":
    main()
