#!/usr/bin/env python3
"""
LisPy Test Runner

A centralized script for running tests with various options including coverage reporting,
test filtering, and performance timing.

Usage:
    python bin/test_runner.py --all                    # Run all tests
    python bin/test_runner.py --fast                   # Skip slow tests
    python bin/test_runner.py --coverage               # Generate coverage
    python bin/test_runner.py --functions              # Run function tests
    python bin/test_runner.py --special-forms          # Run special form tests
    python bin/test_runner.py --integration            # Run integration tests
    python bin/test_runner.py --help                   # Show help
"""

import argparse
import os
import sys
import time
import subprocess
import unittest
from pathlib import Path

# Add the project root to the path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ANSI color codes for pretty output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(text, color=Colors.WHITE):
    """Print text with color if terminal supports it."""
    if os.name == 'nt':  # Windows
        print(text)
    else:
        print(f"{color}{text}{Colors.END}")

def print_header(text):
    """Print a section header."""
    print_colored(f"\n🧪 {text}", Colors.BOLD + Colors.CYAN)
    print_colored("=" * (len(text) + 4), Colors.CYAN)

def print_success(text):
    """Print success message."""
    print_colored(f"✅ {text}", Colors.GREEN)

def print_error(text):
    """Print error message."""
    print_colored(f"❌ {text}", Colors.RED)

def print_warning(text):
    """Print warning message."""
    print_colored(f"⚠️  {text}", Colors.YELLOW)

def print_info(text):
    """Print info message."""
    print_colored(f"ℹ️  {text}", Colors.BLUE)

def run_command(command, description="Running command"):
    """Run a command and return the result."""
    print_info(f"{description}: {' '.join(command)}")
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print_success(f"Completed in {duration:.2f}s")
            if result.stdout:
                print(result.stdout)
            return True, result.stdout, result.stderr
        else:
            print_error(f"Failed after {duration:.2f}s (exit code: {result.returncode})")
            if result.stderr:
                print_colored(result.stderr, Colors.RED)
            if result.stdout:
                print(result.stdout)
            return False, result.stdout, result.stderr
            
    except Exception as e:
        print_error(f"Command failed with exception: {e}")
        return False, "", str(e)

def discover_tests(pattern="*_test.py", start_dir="tests"):
    """Discover test files matching the pattern."""
    test_dir = PROJECT_ROOT / start_dir
    if not test_dir.exists():
        print_error(f"Test directory not found: {test_dir}")
        return []
    
    test_files = []
    for test_file in test_dir.rglob(pattern):
        if test_file.is_file():
            relative_path = test_file.relative_to(PROJECT_ROOT)
            test_files.append(str(relative_path))
    
    return sorted(test_files)

def run_tests_basic(test_pattern="*_test.py", test_dir="tests"):
    """Run tests using unittest discovery."""
    print_header(f"Running Tests: {test_pattern}")
    
    command = [
        sys.executable, "-m", "unittest", "discover",
        "-s", test_dir,
        "-p", test_pattern,
        "-v"
    ]
    
    success, stdout, stderr = run_command(command, "Running unittest discovery")
    return success

def run_tests_with_coverage(test_pattern="*_test.py", test_dir="tests", html_report=True):
    """Run tests with coverage reporting."""
    print_header("Running Tests with Coverage")
    
    # Ensure coverage reports directory exists
    coverage_dir = PROJECT_ROOT / "coverage_reports"
    coverage_dir.mkdir(exist_ok=True)
    
    # Run tests with coverage
    command = [
        sys.executable, "-m", "coverage", "run",
        "-m", "unittest", "discover",
        "-s", test_dir,
        "-p", test_pattern,
        "-v"
    ]
    
    success, stdout, stderr = run_command(command, "Running tests with coverage")
    
    if not success:
        return False
    
    # Generate console report
    print_header("Coverage Report")
    command = [sys.executable, "-m", "coverage", "report"]
    run_command(command, "Generating coverage report")
    
    # Generate HTML report if requested
    if html_report:
        print_header("Generating HTML Coverage Report")
        command = [sys.executable, "-m", "coverage", "html"]
        success, stdout, stderr = run_command(command, "Generating HTML report")
        
        if success:
            html_path = coverage_dir / "htmlcov" / "index.html"
            print_success(f"HTML coverage report generated: {html_path}")
            print_info(f"Open in browser: file://{html_path.absolute()}")
    
    return True

def run_category_tests(category):
    """Run tests for a specific category."""
    category_map = {
        'functions': ('tests/functions', '*_test.py'),
        'special-forms': ('tests/special_forms', '*_test.py'),
        'integration': ('tests/integration', '*_test.py'),
        'bdd': ('tests/bdd_features', '*_test.py'),
        'parser': ('tests', 'parser_test.py'),
        'lexer': ('tests', 'lexer_test.py'),
        'evaluator': ('tests', 'evaluator_test.py'),
        'environment': ('tests', 'environment_test.py'),
    }
    
    if category not in category_map:
        print_error(f"Unknown test category: {category}")
        print_info(f"Available categories: {', '.join(category_map.keys())}")
        return False
    
    test_dir, pattern = category_map[category]
    return run_tests_basic(pattern, test_dir)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="LisPy Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bin/test_runner.py --all                    # Run all tests
  python bin/test_runner.py --coverage               # Run with coverage
  python bin/test_runner.py --functions              # Run function tests
  python bin/test_runner.py --special-forms          # Run special form tests
  python bin/test_runner.py --integration            # Run integration tests
  python bin/test_runner.py --fast                   # Skip slow tests (future)
        """
    )
    
    # Test selection options
    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument('--all', action='store_true',
                           help='Run all tests (default)')
    test_group.add_argument('--functions', action='store_true',
                           help='Run function tests only')
    test_group.add_argument('--special-forms', action='store_true',
                           help='Run special form tests only')
    test_group.add_argument('--integration', action='store_true',
                           help='Run integration tests only')
    test_group.add_argument('--bdd', action='store_true',
                           help='Run BDD tests only')
    test_group.add_argument('--parser', action='store_true',
                           help='Run parser tests only')
    test_group.add_argument('--lexer', action='store_true',
                           help='Run lexer tests only')
    test_group.add_argument('--evaluator', action='store_true',
                           help='Run evaluator tests only')
    test_group.add_argument('--environment', action='store_true',
                           help='Run environment tests only')
    
    # Coverage options
    parser.add_argument('--coverage', action='store_true',
                       help='Generate coverage report')
    parser.add_argument('--no-html', action='store_true',
                       help='Skip HTML coverage report generation')
    
    # Performance options (future)
    parser.add_argument('--fast', action='store_true',
                       help='Skip slow tests (placeholder for future use)')
    
    # Output options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Quiet output')
    
    args = parser.parse_args()
    
    # Print header
    print_colored("🧪 LisPy Test Runner", Colors.BOLD + Colors.MAGENTA)
    print_colored("=" * 25, Colors.MAGENTA)
    
    # Determine what to run
    start_time = time.time()
    success = True
    
    if args.fast:
        print_warning("--fast option not yet implemented, running all tests")
    
    # Run the appropriate tests
    if args.functions:
        success = run_category_tests('functions')
    elif args.special_forms:
        success = run_category_tests('special-forms')
    elif args.integration:
        success = run_category_tests('integration')
    elif args.bdd:
        success = run_category_tests('bdd')
    elif args.parser:
        success = run_category_tests('parser')
    elif args.lexer:
        success = run_category_tests('lexer')
    elif args.evaluator:
        success = run_category_tests('evaluator')
    elif args.environment:
        success = run_category_tests('environment')
    elif args.coverage:
        success = run_tests_with_coverage(html_report=not args.no_html)
    else:
        # Default: run all tests
        if args.coverage:
            success = run_tests_with_coverage(html_report=not args.no_html)
        else:
            success = run_tests_basic()
    
    # Print summary
    end_time = time.time()
    total_time = end_time - start_time
    
    print_header("Test Run Summary")
    if success:
        print_success(f"All tests completed successfully in {total_time:.2f}s")
        sys.exit(0)
    else:
        print_error(f"Some tests failed after {total_time:.2f}s")
        sys.exit(1)

if __name__ == '__main__':
    main() 