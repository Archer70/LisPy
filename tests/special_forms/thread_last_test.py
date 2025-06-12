"""
Tests for the thread-last (->>)  special form.

Thread-last threads values as the LAST argument to each function in the pipeline.
"""

import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.types import Vector


class ThreadLastTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

        # Helper functions for testing
        run_lispy_string("(define double (fn [x] (* x 2)))", self.env)
        run_lispy_string("(define add5 (fn [x] (+ x 5)))", self.env)
        run_lispy_string("(define subtract-from (fn [a b] (- a b)))", self.env)
        run_lispy_string("(define divide-by (fn [a b] (/ a b)))", self.env)
        # Create a string concatenation helper using Python's string concatenation
        self.env.store["py-str-concat"] = lambda args, env: args[0] + args[1]
        run_lispy_string("(define str-concat (fn [a b] (py-str-concat a b)))", self.env)

        # Multi-argument functions for comprehensive testing
        run_lispy_string("(define three-arg-sum (fn [a b c] (+ a b c)))", self.env)
        run_lispy_string("(define multiply-three (fn [a b c] (* a b c)))", self.env)

    def test_thread_last_simple_chain(self):
        """Test basic thread-last chaining with single-argument functions."""
        # (->> 10 double add5) => (add5 (double 10)) => (add5 20) => 25
        result = run_lispy_string("(->> 10 double add5)", self.env)
        self.assertEqual(result, 25)

    def test_thread_last_arithmetic_sequence(self):
        """Test thread-last with arithmetic operations as last argument."""
        # (->> 100 (- 10) (* 2)) => (* 2 (- 10 100)) => (* 2 -90) => -180
        result = run_lispy_string("(->> 100 (- 10) (* 2))", self.env)
        self.assertEqual(result, -180)

        # Different order: (->> 10 (- 100) (* 2)) => (* 2 (- 100 10)) => (* 2 90) => 180
        result = run_lispy_string("(->> 10 (- 100) (* 2))", self.env)
        self.assertEqual(result, 180)

    def test_thread_last_with_vectors(self):
        """Test thread-last with vector operations."""
        # Since conj expects (conj collection item), we need collection first, item second
        # In thread-last, the value becomes the LAST argument
        # (->> 3 (conj [1 2])) => (conj [1 2] 3) => [1 2 3]
        result = run_lispy_string("(->> 3 (conj [1 2]))", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3]))

        # Chain multiple conj operations
        # (->> 4 (conj [1 2 3]) (conj [0])) => (conj [0] (conj [1 2 3] 4)) => (conj [0] [1 2 3 4]) => [0 [1 2 3 4]]
        result = run_lispy_string("(->> 4 (conj [1 2 3]) (conj [0]))", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([0, Vector([1, 2, 3, 4])]))

    def test_thread_last_with_lists(self):
        """Test thread-last with list processing."""
        # (->> '(1 2 3) (cons 0)) => (cons 0 '(1 2 3)) => [0, 1, 2, 3] (as regular Python list)
        result = run_lispy_string("(->> '(1 2 3) (cons 0))", self.env)
        self.assertIsInstance(result, list)  # cons returns a regular Python list
        self.assertEqual(result, [0, 1, 2, 3])

    def test_thread_last_string_operations(self):
        """Test thread-last with string operations."""
        # (->> "world" (str-concat "hello ")) => (str-concat "hello " "world") => "hello world"
        result = run_lispy_string('(->> "world" (str-concat "hello "))', self.env)
        self.assertEqual(result, "hello world")

    def test_thread_last_multi_argument_functions(self):
        """Test thread-last with functions that take multiple arguments."""
        # (->> 10 (three-arg-sum 1 2)) => (three-arg-sum 1 2 10) => 13
        result = run_lispy_string("(->> 10 (three-arg-sum 1 2))", self.env)
        self.assertEqual(result, 13)

        # (->> 5 (multiply-three 2 3)) => (multiply-three 2 3 5) => 30
        result = run_lispy_string("(->> 5 (multiply-three 2 3))", self.env)
        self.assertEqual(result, 30)

    def test_thread_last_longer_pipeline(self):
        """Test thread-last with a longer pipeline."""
        # (->> 1 (+ 2) (* 3) (- 10) (/ 2))
        # => (/ 2 (- 10 (* 3 (+ 2 1))))
        # => (/ 2 (- 10 (* 3 3)))
        # => (/ 2 (- 10 9))
        # => (/ 2 1) => 2
        result = run_lispy_string("(->> 1 (+ 2) (* 3) (- 10) (/ 2))", self.env)
        self.assertEqual(result, 2)

    def test_thread_last_with_nested_data(self):
        """Test thread-last preserving nested data structures."""
        # Create nested vector and process it
        # (->> [5 6] (conj [[1 2] [3 4]])) => (conj [[1 2] [3 4]] [5 6])
        result = run_lispy_string("(->> [5 6] (conj [[1 2] [3 4]]))", self.env)
        expected = Vector([Vector([1, 2]), Vector([3, 4]), Vector([5, 6])])
        self.assertEqual(result, expected)

    def test_thread_last_single_step(self):
        """Test thread-last with just one step."""
        # (->> 5 double) => (double 5) => 10
        result = run_lispy_string("(->> 5 double)", self.env)
        self.assertEqual(result, 10)

    def test_thread_last_just_initial_value(self):
        """Test thread-last with just an initial value (no pipeline steps)."""
        # (->> 42) => 42
        result = run_lispy_string("(->> 42)", self.env)
        self.assertEqual(result, 42)

    def test_thread_last_with_complex_expressions(self):
        """Test thread-last where initial value is a complex expression."""
        # (->> (+ 1 2 3) double) => (double (+ 1 2 3)) => (double 6) => 12
        result = run_lispy_string("(->> (+ 1 2 3) double)", self.env)
        self.assertEqual(result, 12)

    def test_thread_last_comparison_with_thread_first(self):
        """Test the difference between thread-first and thread-last."""
        # Thread-first: (-> 10 (- 5)) => (- 10 5) => 5
        result_first = run_lispy_string("(-> 10 (- 5))", self.env)
        self.assertEqual(result_first, 5)

        # Thread-last: (->> 10 (- 5)) => (- 5 10) => -5
        result_last = run_lispy_string("(->> 10 (- 5))", self.env)
        self.assertEqual(result_last, -5)

    def test_thread_last_with_filter_and_map_like_operations(self):
        """Test thread-last with data processing pipelines."""
        # Test with vector concatenation - more realistic for thread-last
        # (->> [4 5] (concat [1 2 3])) => (concat [1 2 3] [4 5]) => [1 2 3 4 5]
        result = run_lispy_string("(->> [4 5] (concat [1 2 3]))", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3, 4, 5]))

        # Chain concat operations
        # (->> [7 8] (concat [4 5 6]) (concat [1 2 3]))
        # => (concat [1 2 3] (concat [4 5 6] [7 8]))
        # => (concat [1 2 3] [4 5 6 7 8]) => [1 2 3 4 5 6 7 8]
        result = run_lispy_string(
            "(->> [7 8] (concat [4 5 6]) (concat [1 2 3]))", self.env
        )
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3, 4, 5, 6, 7, 8]))

    # --- Error Handling Tests ---
    def test_thread_last_no_initial_value(self):
        """Test thread-last with no arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(->>) ", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: '->>' special form expects at least an initial value.",
        )

    def test_thread_last_empty_list_in_pipeline(self):
        """Test thread-last with empty list in pipeline."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(->> 5 ())", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: Invalid empty list () found in '->>' pipeline.",
        )

    def test_thread_last_invalid_form_in_pipeline(self):
        """Test thread-last with invalid form in pipeline."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(->> 5 123)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Invalid form in '->>' pipeline. Expected function or (function ...), got <class 'int'>: 123",
        )

    def test_thread_last_undefined_function(self):
        """Test thread-last with undefined function in pipeline."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(->> 5 undefined-function)", self.env)
        self.assertEqual(str(cm.exception), "Unbound symbol: undefined-function")

    def test_thread_last_arity_error_propagation(self):
        """Test that arity errors in pipeline functions are properly propagated."""
        # three-arg-sum expects 3 args, but with thread-last it gets: (three-arg-sum 1 5) - only 2 args
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(->> 5 (three-arg-sum 1))", self.env)
        # The actual error message will depend on three-arg-sum's arity checking
        self.assertIn("expects 3 arguments", str(cm.exception))

    def test_thread_last_preserves_list_structure(self):
        """Test that thread-last properly preserves and protects list structures."""
        # Create a list and thread it through operations
        # (->> '(1 2 3) (cons 0) (cons -1))
        # => (cons -1 (cons 0 '(1 2 3)))
        # => (cons -1 [0, 1, 2, 3])  # cons prepends to list
        # => [-1, 0, 1, 2, 3]        # cons flattens, doesn't nest
        result = run_lispy_string("(->> '(1 2 3) (cons 0) (cons -1))", self.env)
        self.assertIsInstance(result, list)  # cons returns regular Python list
        expected = [-1, 0, 1, 2, 3]  # cons flattens the structure
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
