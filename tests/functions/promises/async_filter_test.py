"""
Tests for async-filter function - concurrent async filtering.

Tests cover:
- Basic filtering with sync predicates
- Async predicates with promises
- Mixed sync/async predicates
- Error handling and fail-fast behavior
- Empty collections
- Thread-first compatibility
- Performance characteristics
- Edge cases
"""

import time
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.types import Vector
from lispy.utils import run_lispy_string


class TestAsyncFilter(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_empty_collection(self):
        """Test async-filter with empty collection."""
        result = run_lispy_string("(await (async-filter [] (fn [x] true)))", self.env)
        self.assertEqual(result, Vector([]))

    def test_sync_predicate_all_true(self):
        """Test async-filter with sync predicate that returns true for all."""
        result = run_lispy_string(
            "(await (async-filter [1 2 3] (fn [x] true)))", self.env
        )
        self.assertEqual(result, Vector([1, 2, 3]))

    def test_sync_predicate_all_false(self):
        """Test async-filter with sync predicate that returns false for all."""
        result = run_lispy_string(
            "(await (async-filter [1 2 3] (fn [x] false)))", self.env
        )
        self.assertEqual(result, Vector([]))

    def test_sync_predicate_selective(self):
        """Test async-filter with sync predicate that filters selectively."""
        result = run_lispy_string(
            "(await (async-filter [1 2 3 4 5] (fn [x] (> x 3))))", self.env
        )
        self.assertEqual(result, Vector([4, 5]))

    def test_async_predicate_all_true(self):
        """Test async-filter with async predicate that returns true for all."""
        result = run_lispy_string(
            "(await (async-filter [1 2 3] (fn [x] (resolve true))))", self.env
        )
        self.assertEqual(result, Vector([1, 2, 3]))

    def test_async_predicate_all_false(self):
        """Test async-filter with async predicate that returns false for all."""
        result = run_lispy_string(
            "(await (async-filter [1 2 3] (fn [x] (resolve false))))", self.env
        )
        self.assertEqual(result, Vector([]))

    def test_async_predicate_selective(self):
        """Test async-filter with async predicate that filters selectively."""
        result = run_lispy_string(
            """
            (await (async-filter [1 2 3 4 5] 
                                 (fn [x] (resolve (> x 3)))))
        """,
            self.env,
        )
        self.assertEqual(result, Vector([4, 5]))

    def test_mixed_sync_async_predicates(self):
        """Test async-filter with mixed sync and async predicates."""
        # This test uses a predicate that returns sync for some values, async for others
        result = run_lispy_string(
            """
            (await (async-filter [1 2 3 4] 
                                 (fn [x] 
                                   (if (< x 3)
                                     (> x 1)  ; sync: true for 2, false for 1
                                     (resolve (> x 3))))))  ; async: true for 4, false for 3
        """,
            self.env,
        )
        self.assertEqual(result, Vector([2, 4]))

    def test_concurrent_execution(self):
        """Test that predicates execute concurrently, not sequentially."""
        start_time = time.time()
        result = run_lispy_string(
            """
            (await (async-filter [1 2 3] 
                                 (fn [x] (-> (timeout 100 true)))))
        """,
            self.env,
        )
        end_time = time.time()

        # Should take ~100ms (concurrent) not ~300ms (sequential)
        elapsed = (end_time - start_time) * 1000
        self.assertLess(elapsed, 200, "Predicates should execute concurrently")
        self.assertEqual(result, Vector([1, 2, 3]))

    def test_order_preservation(self):
        """Test that results maintain original order regardless of completion order."""
        result = run_lispy_string(
            """
            (await (async-filter [1 2 3 4 5] 
                                 (fn [x] 
                                   (-> (timeout (if (= x 3) 10 50) true)))))
        """,
            self.env,
        )
        self.assertEqual(result, Vector([1, 2, 3, 4, 5]))

    def test_error_handling_fail_fast(self):
        """Test that async-filter fails fast when any predicate throws."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(
                """
                (await (async-filter [1 2 3] 
                                     (fn [x] 
                                       (if (= x 2) 
                                         (reject "predicate error")
                                         true))))
            """,
                self.env,
            )
        self.assertIn("predicate error", str(cm.exception))

    def test_thread_first_compatibility(self):
        """Test async-filter works with thread-first operator."""
        result = run_lispy_string(
            """
            (-> [1 2 3 4 5 6]
                (async-filter (fn [x] (= 0 (% x 2))))  ; even numbers
                (await))
        """,
            self.env,
        )
        self.assertEqual(result, Vector([2, 4, 6]))

    def test_chaining_with_promise_then(self):
        """Test async-filter can be chained with promise-then."""
        result = run_lispy_string(
            """
            (-> (async-filter [1 2 3 4 5] (fn [x] (> x 2)))
                (promise-then (fn [filtered] (count filtered)))
                (await))
        """,
            self.env,
        )
        self.assertEqual(result, 3)  # [3, 4, 5] has count 3

    def test_truthy_falsy_values(self):
        """Test async-filter handles truthy/falsy values correctly."""
        result = run_lispy_string(
            """
            (await (async-filter [1 2 3 4] 
                                 (fn [x] 
                                   (cond 
                                     (= x 1) nil      ; falsy
                                     (= x 2) false    ; falsy
                                     (= x 3) 0        ; falsy in LisPy
                                     (= x 4) "truthy" ; truthy
                                     :else true))))
        """,
            self.env,
        )
        self.assertEqual(result, Vector([4]))

    def test_performance_large_collection(self):
        """Test async-filter performance with larger collection."""
        start_time = time.time()
        result = run_lispy_string(
            """
            (await (async-filter (range 100) 
                                 (fn [x] (-> (timeout 1 (= 0 (% x 10)))))))
        """,
            self.env,
        )
        end_time = time.time()

        # Should complete in reasonable time (concurrent execution)
        elapsed = (end_time - start_time) * 1000
        self.assertLess(elapsed, 500, "Should handle large collections efficiently")

        # Should filter to multiples of 10: [0, 10, 20, ..., 90]
        expected = Vector([i for i in range(0, 100, 10)])
        self.assertEqual(result, expected)

    def test_argument_validation(self):
        """Test async-filter argument validation."""
        # Wrong number of arguments
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(async-filter [1 2 3])", self.env)
        self.assertIn("expects 2 arguments", str(cm.exception))

        # Non-collection first argument
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(async-filter 42 (fn [x] true))", self.env)
        self.assertIn("expects a vector or list", str(cm.exception))

        # Non-function second argument
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(async-filter [1 2 3] 42)", self.env)
        self.assertIn("expects a function", str(cm.exception))

    def test_predicate_arity_validation(self):
        """Test that predicate function must take exactly 1 argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(await (async-filter [1 2 3] (fn [] true)))", self.env)
        self.assertIn("expects 1 argument", str(cm.exception))

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(await (async-filter [1 2 3] (fn [x y] true)))", self.env)
        self.assertIn("expects 1 argument", str(cm.exception))

    def test_complex_filtering_logic(self):
        """Test async-filter with complex predicate logic."""
        result = run_lispy_string(
            """
            (await (async-filter (range 1 21)  ; 1 to 20
                                 (fn [x] 
                                   (-> (timeout 10 x)
                                       (promise-then (fn [n] 
                                         (and (> n 5) 
                                              (< n 15) 
                                              (= 0 (% n 3)))))))))
        """,
            self.env,
        )
        # Numbers between 5 and 15 that are divisible by 3: [6, 9, 12]
        self.assertEqual(result, Vector([6, 9, 12]))

    def test_nested_async_operations(self):
        """Test async-filter with nested async operations in predicate."""
        result = run_lispy_string(
            """
            (await (async-filter [1 2 3 4 5] 
                                 (fn [x] 
                                   (-> (timeout 10 (* x 2))
                                       (promise-then (fn [doubled] 
                                         (-> (timeout 10 (> doubled 6)))))))))
        """,
            self.env,
        )
        # x * 2 > 6 means x > 3, so [4, 5]
        self.assertEqual(result, Vector([4, 5]))


if __name__ == "__main__":
    unittest.main()
