#!/usr/bin/env python3
"""
Update Test Count in README

This script counts the total number of tests and updates the README.md badge.
Can be run manually or as part of a git hook.

Usage:
    python scripts/update_test_count.py
    python scripts/update_test_count.py --dry-run    # Show what would change
"""

import argparse
import re
import subprocess
import sys
import unittest
from pathlib import Path

# Add the project root to the path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def count_tests():
    """Count the total number of tests in the test suite."""
    # Use unittest's test discovery to find all tests
    loader = unittest.TestLoader()
    start_dir = str(PROJECT_ROOT / 'tests')
    
    try:
        # Discover all test suites
        suite = loader.discover(start_dir, pattern='*_test.py')
        
        # Count total tests recursively
        def count_tests_in_suite(test_suite):
            count = 0
            for test in test_suite:
                if hasattr(test, '_tests'):  # TestSuite
                    count += count_tests_in_suite(test)
                else:  # Individual test case
                    count += 1
            return count
        
        total_tests = count_tests_in_suite(suite)
        return total_tests
        
    except Exception as e:
        print(f"Error counting tests: {e}")
        return None

def update_readme_badge(test_count, dry_run=False):
    """Update the test count badge in README.md."""
    readme_path = PROJECT_ROOT / 'README.md'
    
    if not readme_path.exists():
        print("README.md not found!")
        return False
    
    # Read current README content
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the test badge
    badge_pattern = r'\[\!\[Tests\]\(https://img\.shields\.io/badge/tests-\d+%20passing-green\)\]\(tests/\)'
    new_badge = f'[![Tests](https://img.shields.io/badge/tests-{test_count}%20passing-green)](tests/)'
    
    # Find and replace the badge
    if re.search(badge_pattern, content):
        new_content = re.sub(badge_pattern, new_badge, content)
        
        if dry_run:
            print(f"Would update README.md badge to show {test_count} tests")
            return True
        else:
            # Write the updated content
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated README.md badge to show {test_count} tests")
            return True
    else:
        print("Could not find test badge pattern in README.md")
        return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Update test count in README.md")
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without making changes')
    
    args = parser.parse_args()
    
    print("Counting tests...")
    test_count = count_tests()
    
    if test_count is None:
        print("Failed to count tests")
        sys.exit(1)
    
    print(f"Found {test_count} tests")
    
    # Update the README badge
    success = update_readme_badge(test_count, dry_run=args.dry_run)
    
    if success:
        if not args.dry_run:
            print("README.md updated successfully")
        sys.exit(0)
    else:
        print("Failed to update README.md")
        sys.exit(1)

if __name__ == '__main__':
    main() 