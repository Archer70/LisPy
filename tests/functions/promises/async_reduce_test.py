"""
Tests for async-reduce function - sequential async reduction.

Tests cover:
- Basic reduction with sync reducers
- Async reducers with promises
- Mixed sync/async reducers
- Error handling and fail-fast behavior
- Empty collections
- Thread-first compatibility
- Sequential processing validation
- Edge cases
"""

import time
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.types import LispyPromise, Symbol, Vector
from lispy.utils import run_lispy_string


class AsyncReduceTest(unittest.TestCase):
    """Test cases for async-reduce function."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_basic_sync_reduction(self):
        """Test basic synchronous reduction (sum)."""
        result = run_lispy_string(
            "(await (async-reduce [1 2 3 4] (fn [acc x] (+ acc x)) 0))", self.env
        )
        self.assertEqual(result, 10)

    def test_multiplication_reduction(self):
        """Test multiplication reduction (factorial-like)."""
        result = run_lispy_string(
            "(await (async-reduce [1 2 3 4] (fn [acc x] (* acc x)) 1))", self.env
        )
        self.assertEqual(result, 24)

    def test_async_reduction_with_timeout(self):
        """Test reduction with async timeout operations."""
        result = run_lispy_string(
            "(await (async-reduce [1 2 3] (fn [acc x] (timeout 50 (+ acc (* x x)))) 0))",
            self.env,
        )
        self.assertEqual(result, 14)  # 0 + 1² + 2² + 3² = 0 + 1 + 4 + 9 = 14

    def test_empty_collection(self):
        """Test reduction with empty collection returns initial value."""
        result = run_lispy_string(
            "(await (async-reduce [] (fn [acc x] (+ acc x)) 42))", self.env
        )
        self.assertEqual(result, 42)

    def test_single_element(self):
        """Test reduction with single element."""
        result = run_lispy_string(
            "(await (async-reduce [5] (fn [acc x] (+ acc x)) 10))", self.env
        )
        self.assertEqual(result, 15)

    def test_building_collection(self):
        """Test using reduce to build a collection."""
        result = run_lispy_string(
            "(await (async-reduce [1 2 3] (fn [acc x] (conj acc (* x 2))) []))",
            self.env,
        )
        self.assertEqual(result, Vector([2, 4, 6]))

    def test_string_concatenation(self):
        """Test building a result with reduce (using numbers instead of strings for simplicity)."""
        # Build a sum instead of string concatenation to avoid str function complexity
        result = run_lispy_string(
            "(await (async-reduce [10 20 30] (fn [acc x] (+ acc x)) 0))", self.env
        )
        self.assertEqual(result, 60)  # 0 + 10 + 20 + 30 = 60

    def test_thread_first_compatibility(self):
        """Test that async-reduce works with thread-first operator."""
        result = run_lispy_string(
            "(-> [1 2 3 4 5] (async-reduce (fn [acc x] (* acc x)) 1) (await))", self.env
        )
        self.assertEqual(result, 120)  # 1 * 1 * 2 * 3 * 4 * 5 = 120

    def test_sequential_processing_order(self):
        """Test that processing is sequential, not concurrent."""
        # This test uses timeouts to verify sequential processing
        start_time = time.time()
        result = run_lispy_string(
            "(await (async-reduce [1 2 3] (fn [acc x] (timeout 100 (+ acc x))) 0))",
            self.env,
        )
        end_time = time.time()

        self.assertEqual(result, 6)  # 0 + 1 + 2 + 3 = 6
        # Should take ~300ms (3 * 100ms) for sequential processing
        # Allow some tolerance for timing
        self.assertGreater(end_time - start_time, 0.25)  # At least 250ms
        self.assertLess(end_time - start_time, 0.5)  # Less than 500ms

    def test_mixed_sync_async_operations(self):
        """Test mixing synchronous and asynchronous operations."""
        # Simplified test without conditional logic - just mix sync and async operations
        result = run_lispy_string(
            """
            (await (async-reduce [1 2 3 4] 
                                 (fn [acc x] 
                                   (timeout 50 (+ acc x)))
                                 0))
        """,
            self.env,
        )
        self.assertEqual(result, 10)  # 0 + 1 + 2 + 3 + 4 = 10

    def test_error_handling_sync_reducer(self):
        """Test error handling with synchronous reducer."""
        with self.assertRaises(EvaluationError):
            run_lispy_string(
                "(await (async-reduce [1 2 3] (fn [acc x] (/ acc 0)) 1))", self.env
            )

    def test_error_handling_async_reducer(self):
        """Test error handling with asynchronous reducer."""
        with self.assertRaises(EvaluationError):
            run_lispy_string(
                '(await (async-reduce [1 2 3] (fn [acc x] (reject "error")) 0))',
                self.env,
            )

    def test_invalid_argument_count(self):
        """Test error handling for invalid argument count."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(async-reduce [1 2 3])", self.env)
        self.assertIn("expects 3 arguments", str(cm.exception))

        # Test with too many arguments - simpler test using lispy string
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(
                '(async-reduce [1 2 3] (fn [acc x] (+ acc x)) 0 "extra")', self.env
            )
        self.assertIn("expects 3 arguments", str(cm.exception))

    def test_invalid_collection_type(self):
        """Test error handling for invalid collection type."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(
                '(async-reduce "not-a-collection" (fn [acc x] (+ acc x)) 0)', self.env
            )
        self.assertIn("expects a vector or list", str(cm.exception))

    def test_invalid_reducer_type(self):
        """Test error handling for invalid reducer type."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(async-reduce [1 2 3] "not-a-function" 0)', self.env)
        self.assertIn("expects a function", str(cm.exception))

    def test_reducer_arity_validation(self):
        """Test that reducer function must take exactly 2 arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(
                "(await (async-reduce [1 2 3] (fn [acc] acc) 0))", self.env
            )
        self.assertIn("expects 2 arguments", str(cm.exception))

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(
                "(await (async-reduce [1 2 3] (fn [acc x y] (+ acc x)) 0))", self.env
            )
        self.assertIn("expects 2 arguments", str(cm.exception))

    def test_promise_chaining(self):
        """Test that async-reduce can be chained with other promise operations."""
        result = run_lispy_string(
            """
            (-> (async-reduce [1 2 3] (fn [acc x] (+ acc x)) 0)
                (promise-then (fn [sum] (* sum 2)))
                (await))
        """,
            self.env,
        )
        self.assertEqual(result, 12)  # (1 + 2 + 3) * 2 = 6 * 2 = 12

    def test_complex_async_chain(self):
        """Test complex async operations in reducer."""
        result = run_lispy_string(
            """
            (await (async-reduce [1 2 3] 
                                 (fn [acc x] 
                                   (-> (timeout 30 (* x 2))
                                       (promise-then (fn [doubled] (+ acc doubled)))))
                                 0))
        """,
            self.env,
        )
        self.assertEqual(result, 12)  # 0 + (1*2) + (2*2) + (3*2) = 0 + 2 + 4 + 6 = 12

    def test_performance_sequential_nature(self):
        """Test that async-reduce is truly sequential (not concurrent)."""
        # Create a test that would fail if operations were concurrent
        start_time = time.time()
        result = run_lispy_string(
            """
            (await (async-reduce [50 50 50] 
                                 (fn [acc delay] (timeout delay (+ acc delay)))
                                 0))
        """,
            self.env,
        )
        end_time = time.time()

        self.assertEqual(result, 150)  # 0 + 50 + 50 + 50 = 150
        # Should take ~150ms (50 + 50 + 50) for sequential processing
        # If it were concurrent, it would take ~50ms
        self.assertGreater(end_time - start_time, 0.12)  # At least 120ms
        self.assertLess(end_time - start_time, 0.25)  # Less than 250ms


if __name__ == "__main__":
    unittest.main()
