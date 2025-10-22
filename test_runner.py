#!/usr/bin/env python3
"""
Simple test runner for ARXML model save tests without pytest dependency.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tests.test_arxml_model_save import TestARXMLModelSave


def run_tests():
    """Run all test methods."""
    test_instance = TestARXMLModelSave()
    test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    print(f"Running {len(test_methods)} tests...")
    print("=" * 50)
    
    for test_method in test_methods:
        print(f"Running {test_method}...", end=" ")
        try:
            getattr(test_instance, test_method)()
            print("PASSED")
            passed += 1
        except Exception as e:
            print(f"FAILED: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)