#!/usr/bin/env python3
"""
RLM SDK Demo
A simple demonstration of the RLM SDK capabilities.
Run this to see the SDK in action!
demo
"""

import sys

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_section(text):
    print(f"\n{text}")
    print("-"*70)

def main():
    try:
        from pyrlmlite import RLMClient, quick_query
    except ImportError:
        print("ERROR: Could not import rlm_sdk")
        print("Make sure rlm_sdk.py is in the current directory or Python path")
        sys.exit(1)
    
    print_header("🚀 RLM SDK Demo")
    
    # Sample document
    sample_doc = """
    The Future of Artificial Intelligence
    
    Introduction:
    Artificial Intelligence (AI) is revolutionizing how we live and work. 
    This document explores three key areas where AI is making the biggest impact.
    
    1. Healthcare
    AI is transforming healthcare through:
    - Disease diagnosis using medical imaging
    - Drug discovery and development
    - Personalized treatment plans
    - Predictive analytics for patient outcomes
    
    2. Transportation
    Autonomous vehicles are becoming a reality:
    - Self-driving cars reduce accidents
    - Optimized traffic flow in smart cities
    - Delivery drones for logistics
    - AI-powered navigation systems
    
    3. Education
    AI is personalizing learning experiences:
    - Adaptive learning platforms
    - Automated grading and feedback
    - Virtual tutors available 24/7
    - Early identification of learning difficulties
    
    Conclusion:
    AI's impact will continue to grow, transforming industries and creating
    new opportunities while also raising important ethical questions about
    privacy, bias, and the future of work.
    
    Published: January 2026
    Author: AI Research Lab
    """
    
    print("Demo Document: 'The Future of Artificial Intelligence'")
    print(f"Document length: {len(sample_doc)} characters\n")
    
    # Demo 1: Basic Usage
    print_section("DEMO 1: Basic Query")
    
    client = RLMClient()
    client.load_document_from_text(sample_doc, "AI_Future")
    
    question1 = "What are the three key areas mentioned?"
    print(f"Question: {question1}\n")
    
    answer1 = client.query(question1)
    print(f"Answer: {answer1}")
    
    # Demo 2: Multiple Queries
    print_section("DEMO 2: Multiple Questions")
    
    questions = [
        "How is AI transforming healthcare?",
        "What year was this published?"
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. Question: {q}")
        answer = client.query(q)
        print(f"   Answer: {answer}")
    
    # Demo 3: Verbose Mode
    print_section("DEMO 3: Verbose Mode (see tool calls)")
    
    question3 = "Who is the author?"
    print(f"Question: {question3}\n")
    
    answer3 = client.query(question3, verbose=True)
    print(f"\n→ Final Answer: {answer3}")
    
    # Demo 4: Quick Query
    print_section("DEMO 4: Quick Query (one-liner)")
    
    # Create a temp file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(sample_doc)
        temp_file = f.name
    
    try:
        print("Using quick_query() function...")
        answer4 = quick_query(temp_file, "What ethical questions does AI raise?")
        print(f"\nAnswer: {answer4}")
    finally:
        import os
        os.unlink(temp_file)
    
    # Demo 5: Document Info
    print_section("DEMO 5: Document Information")
    
    info = client.get_document_info()
    print(f"Document Name: {info['name']}")
    print(f"Length: {info['length']} characters")
    print(f"Lines: {info['lines']}")
    
    # Summary
    print_header("✅ Demo Complete!")
    print("You've seen:")
    print("  ✓ Basic query")
    print("  ✓ Multiple questions")
    print("  ✓ Verbose mode (tool calling)")
    print("  ✓ Quick query function")
    print("  ✓ Document information\n")
    
    print("Next steps:")
    print("  1. Check out examples/ directory for more examples")
    print("  2. Read QUICKSTART.md for a tutorial")
    print("  3. See API.md for complete documentation")
    print("  4. Read INTEGRATION.md for integration patterns\n")
    
    print("Ready to build amazing document Q&A apps! 🎉\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        print("\nMake sure you have:")
        print("  1. Set OPENAI_API_KEY environment variable")
        print("  2. Installed openai package: pip install openai")
        sys.exit(1)
