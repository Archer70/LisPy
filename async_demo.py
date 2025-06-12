#!/usr/bin/env python3
"""
LisPy Async Functionality Demo
==============================

This script demonstrates the new async functionality in LisPy, including:
- Promise creation and execution
- Async/await syntax
- Async function definitions
- Error handling with promises
"""

from lispy.utils import run_lispy_string
from lispy.functions import global_env


def demo_section(title):
    """Print a demo section header."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")


def run_demo(description, code):
    """Run a demo with description and code."""
    print(f"\n{description}:")
    print(f"Code: {code}")
    try:
        result = run_lispy_string(code, global_env)
        print(f"Result: {result}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    print("LisPy Async Functionality Demo")
    print("===============================")

    demo_section("1. Basic Promise Operations")

    # Test promise creation
    run_demo("Creating a simple promise", "(promise (fn [] (+ 10 20)))")

    # Test resolve
    run_demo("Creating a resolved promise", "(resolve 42)")

    # Test reject
    run_demo("Creating a rejected promise", '(reject "Something went wrong")')

    demo_section("2. Async/Await Operations")

    # Test basic async/await
    run_demo("Basic async/await with resolved promise", "(async (await (resolve 100)))")

    # Test async/await with promise
    run_demo(
        "Async/await with promise computation",
        "(async (await (promise (fn [] (* 7 8)))))",
    )

    # Test async/await with complex computation
    run_demo(
        "Async/await with complex computation",
        "(async (await (promise (fn [] (reduce [1 2 3 4 5] + 0)))))",
    )

    demo_section("3. Async Function Definitions")

    # Define an async function
    run_demo("Defining an async function", "(defn-async compute-square [x] (* x x))")

    # Call the async function
    run_demo("Calling async function (returns promise)", "(compute-square 9)")

    # Use async function with await
    run_demo("Using async function with await", "(async (await (compute-square 12)))")

    # Define a more complex async function
    run_demo(
        "Defining complex async function",
        "(defn-async fibonacci [n] (if (<= n 1) n (+ (await (fibonacci (- n 1))) (await (fibonacci (- n 2))))))",
    )

    # Note: The fibonacci example above would cause infinite recursion in practice
    # Let's use a simpler example
    run_demo(
        "Defining async function with multiple operations",
        "(defn-async process-data [x y] (let [sum (+ x y)] (* sum 2)))",
    )

    run_demo("Using complex async function", "(async (await (process-data 5 7)))")

    demo_section("4. Error Handling")

    # Test error handling with try/catch (if available)
    try:
        run_demo("Handling rejected promise", '(async (await (reject "Test error")))')
    except Exception as e:
        print(f"Expected error caught: {e}")

    demo_section("5. Practical Examples")

    # Simulate async I/O operation
    run_demo(
        "Simulating async file operation",
        '(async (await (promise (fn [] (str "File contents: Hello, World!")))))',
    )

    # Chain multiple async operations
    run_demo(
        "Chaining async operations",
        """(async 
             (let [data (await (promise (fn [] [1 2 3 4 5])))]
               (await (promise (fn [] (count data))))))""",
    )

    # Multiple async functions working together
    run_demo("Multiple async functions", """(defn-async double-async [x] (* x 2))""")

    run_demo(
        "Using multiple async functions together",
        """(async 
             (let [a (await (double-async 5))
                   b (await (double-async 10))]
               (+ a b)))""",
    )

    demo_section("6. Documentation")

    # Show documentation for async functions
    print("\nPromise function documentation:")
    result = run_lispy_string("(doc promise)", global_env)
    print(result[:200] + "..." if len(result) > 200 else result)

    print("\nResolve function documentation:")
    result = run_lispy_string("(doc resolve)", global_env)
    print(result[:200] + "..." if len(result) > 200 else result)

    print("\nReject function documentation:")
    result = run_lispy_string("(doc reject)", global_env)
    print(result[:200] + "..." if len(result) > 200 else result)

    demo_section("Summary")
    print("""
LisPy now supports full async programming with:

✓ Promise creation with (promise function)
✓ Immediate resolution/rejection with (resolve value) and (reject error)
✓ Async contexts with (async body)
✓ Promise waiting with (await promise)
✓ Async function definitions with (defn-async name [params] body...)
✓ Full error handling and propagation
✓ Integration with existing LisPy functions
✓ Complete documentation support

This enables powerful asynchronous programming patterns while maintaining
LisPy's functional programming philosophy!
    """)


if __name__ == "__main__":
    main()
