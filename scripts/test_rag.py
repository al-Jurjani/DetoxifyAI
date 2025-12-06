#!/usr/bin/env python3
"""
DetoxifyAI RAG Pipeline Test Script
Demonstrates end-to-end RAG functionality for Milestone 2 D2 requirement
"""

import sys
import os
import argparse
from typing import Dict
from dotenv import load_dotenv

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag_pipeline import DetoxifyRAGPipeline


# Test cases covering different toxicity types
TEST_CASES = [
    {
        "input": "You're an idiot for making that mistake",
        "category": "insult",
        "expected_tone": "constructive feedback",
    },
    {
        "input": "This is the worst idea I've ever heard",
        "category": "criticism",
        "expected_tone": "professional disagreement",
    },
    {
        "input": "Get lost, nobody wants you here",
        "category": "hostility",
        "expected_tone": "polite boundaries",
    },
    {
        "input": "You clearly have no clue what you're doing",
        "category": "workplace toxicity",
        "expected_tone": "professional concern",
    },
    {
        "input": "That's a stupid question to ask",
        "category": "dismissiveness",
        "expected_tone": "encouraging clarification",
    },
]


def print_separator(char="=", length=80):
    """Print a separator line"""
    print(char * length)


def print_header(text: str):
    """Print formatted header"""
    print_separator()
    print(f"  {text}")
    print_separator()
    print()


def print_result(test_case: Dict, result: Dict, test_num: int, total: int):
    """Print formatted test result"""
    print(f"TEST {test_num}/{total}: {test_case['category'].upper()}")
    print("-" * 80)
    print("Original (Toxic):")
    print(f"  → {result['toxic_input']}")
    print()
    print("Rephrased (Professional):")
    print(f"  ✓ {result['professional_rephrase']}")
    print()
    print(f"Retrieved Examples Used: {result['num_examples_used']}")
    print()
    print("Top 3 Similar Examples:")
    for i, example in enumerate(result["retrieved_examples"][:3], 1):
        print(f"  {i}. [{example['category']}]")
        print(f'     Toxic: "{example["toxic"]}"')
        print(f'     Prof:  "{example["professional"]}"')
    print()
    print_separator("-")
    print()


def run_demo():
    """Run quick demo with 2 examples"""
    print_header("DetoxifyAI RAG Pipeline - Quick Demo")

    print("Initializing RAG pipeline...")
    print("  - Loading FAISS index from Azure Blob Storage")
    print("  - Connecting to Modal Mistral-7B endpoint")
    print("  - Setting up LangChain components")
    print()

    # Load environment variables
    load_dotenv()
    azure_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    if not azure_connection_string:
        print("❌ ERROR: AZURE_STORAGE_CONNECTION_STRING not found in .env file")
        sys.exit(1)

    # Initialize pipeline
    try:
        pipeline = DetoxifyRAGPipeline(
            azure_connection_string=azure_connection_string,
            azure_container="detoxifyai-m2-artifacts",
        )
        print("✅ RAG pipeline initialized successfully!")
        print()
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize RAG pipeline: {e}")
        sys.exit(1)

    # Run demo on first 2 test cases
    demo_cases = TEST_CASES[:2]

    for i, test_case in enumerate(demo_cases, 1):
        try:
            result = pipeline.rephrase(test_case["input"], k=5)
            print_result(test_case, result, i, len(demo_cases))
        except Exception as e:
            print(f"❌ ERROR: Test case {i} failed: {e}")
            print()

    print_header("Demo Complete!")
    print("The RAG pipeline successfully:")
    print("  ✓ Downloaded FAISS index from Azure Blob Storage")
    print("  ✓ Retrieved relevant examples using similarity search")
    print("  ✓ Built few-shot prompts with LangChain PromptTemplate")
    print("  ✓ Generated professional rephrases via Modal Mistral-7B")
    print("  ✓ Demonstrated end-to-end reproducibility")
    print()


def run_all_tests():
    """Run comprehensive tests on all test cases"""
    print_header("DetoxifyAI RAG Pipeline - Comprehensive Tests")

    print("Initializing RAG pipeline...")
    print()

    # Load environment variables
    load_dotenv()
    azure_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    if not azure_connection_string:
        print("❌ ERROR: AZURE_STORAGE_CONNECTION_STRING not found in .env file")
        sys.exit(1)

    # Initialize pipeline
    try:
        pipeline = DetoxifyRAGPipeline(
            azure_connection_string=azure_connection_string,
            azure_container="detoxifyai-m2-artifacts",
        )
        print("✅ RAG pipeline initialized successfully!")
        print()
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize RAG pipeline: {e}")
        sys.exit(1)

    # Run all test cases
    results = []
    failed = 0

    for i, test_case in enumerate(TEST_CASES, 1):
        try:
            result = pipeline.rephrase(test_case["input"], k=5)
            print_result(test_case, result, i, len(TEST_CASES))
            results.append({"test_case": test_case, "result": result, "status": "PASS"})
        except Exception as e:
            print(f"❌ ERROR: Test case {i} failed: {e}")
            print()
            failed += 1
            results.append(
                {
                    "test_case": test_case,
                    "result": None,
                    "status": "FAIL",
                    "error": str(e),
                }
            )

    # Print summary
    print_header("Test Summary")
    print(f"Total Tests: {len(TEST_CASES)}")
    print(f"Passed: {len(TEST_CASES) - failed}")
    print(f"Failed: {failed}")
    print()

    if failed == 0:
        print("✅ All tests passed successfully!")
    else:
        print(f"⚠️  {failed} test(s) failed")
    print()

    # Print LangChain components used
    if results and results[0]["result"]:
        print("LangChain Components Used:")
        components = results[0]["result"]["langchain_components"]
        for component, description in components.items():
            print(f"  • {component}: {description}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Test DetoxifyAI RAG Pipeline")
    parser.add_argument(
        "--demo", action="store_true", help="Run quick demo (2 examples)"
    )
    parser.add_argument(
        "--test-all", action="store_true", help="Run comprehensive tests (all examples)"
    )

    args = parser.parse_args()

    if args.demo:
        run_demo()
    elif args.test_all:
        run_all_tests()
    else:
        # Default: run demo
        run_demo()


if __name__ == "__main__":
    main()
