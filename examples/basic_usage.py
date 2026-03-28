"""
Basic Usage Example
Shows the simplest way to use the RLM SDK.
"""

from rlm_sdk import RLMClient

def main():
    # Initialize the RLM client
    client = RLMClient()
    
    # Create a sample document
    sample_text = """
    Climate Change Report 2026
    
    Executive Summary:
    Global temperatures have risen by 1.5°C since pre-industrial times.
    This report examines the impacts and potential solutions.
    
    Key Findings:
    1. Arctic ice is melting at an accelerated rate
    2. Sea levels have risen by 20cm in the past century
    3. Extreme weather events have increased by 40%
    
    Recommendations:
    - Transition to renewable energy by 2040
    - Implement carbon capture technology
    - Protect and restore natural ecosystems
    """
    
    # Load the document
    client.load_document_from_text(sample_text, "Climate_Report")
    
    # Check document info
    info = client.get_document_info()
    print(f"Loaded: {info['name']}")
    print(f"Length: {info['length']} characters\n")
    
    # Ask a question
    question = "What are the three key findings mentioned in the report?"
    print(f"Question: {question}\n")
    
    answer = client.query(question, verbose=True)
    
    print("\n" + "="*60)
    print("Answer:")
    print(answer)
    print("="*60)

if __name__ == "__main__":
    main()
