"""
Multiple Queries Example
Demonstrates asking multiple questions about the same document.
"""

from rlm_sdk import RLMClient

def main():
    # Initialize client
    client = RLMClient()
    
    # Sample document - a research paper abstract
    research_paper = """
    Title: Neural Architecture Search for Large Language Models
    
    Abstract:
    We present a novel approach to neural architecture search (NAS) specifically
    designed for large language models. Our method, called AutoLLM, uses 
    reinforcement learning to discover optimal transformer architectures.
    
    Methodology:
    We employ a two-stage search process:
    1. Macro-search: Determines the overall architecture (layers, dimensions)
    2. Micro-search: Optimizes attention mechanisms and feed-forward networks
    
    Results:
    Our approach achieved a 15% improvement in perplexity compared to baseline
    models while using 30% fewer parameters. Training time was reduced by 40%.
    
    Conclusions:
    AutoLLM demonstrates that automated architecture search can significantly
    improve language model efficiency without sacrificing performance.
    """
    
    # Load document
    client.load_document_from_text(research_paper, "Research_Paper")
    print(f"Document loaded: {client.get_document_info()['name']}\n")
    
    # Multiple questions
    questions = [
        "What is the name of the proposed method?",
        "What are the two stages in the search process?",
        "What were the main improvements achieved?",
        "How much were the parameters reduced by?"
    ]
    
    print("="*70)
    print("ASKING MULTIPLE QUESTIONS ABOUT THE DOCUMENT")
    print("="*70 + "\n")
    
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question}")
        answer = client.query(question)
        print(f"Answer: {answer}\n")
        print("-"*70 + "\n")

if __name__ == "__main__":
    main()
