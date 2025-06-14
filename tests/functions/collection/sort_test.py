import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.types import Vector


class SortFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_sort_empty_vector(self):
        """Test (sort []) returns []."""
        result = run_lispy_string("(sort [])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_sort_single_element(self):
        """Test (sort [42]) returns [42]."""
        result = run_lispy_string("(sort [42])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([42]))

    def test_sort_numbers_ascending(self):
        """Test (sort [3 1 4 1 5]) sorts numbers in ascending order."""
        result = run_lispy_string("(sort [3 1 4 1 5])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 1, 3, 4, 5]))

    def test_sort_numbers_already_sorted(self):
        """Test (sort [1 2 3 4 5]) returns [1 2 3 4 5]."""
        result = run_lispy_string("(sort [1 2 3 4 5])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3, 4, 5]))

    def test_sort_numbers_reverse_order(self):
        """Test (sort [5 4 3 2 1]) returns [1 2 3 4 5]."""
        result = run_lispy_string("(sort [5 4 3 2 1])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3, 4, 5]))

    def test_sort_strings(self):
        """Test (sort [\"zebra\" \"apple\" \"banana\"]) sorts strings alphabetically."""
        result = run_lispy_string('(sort ["zebra" "apple" "banana"])', self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector(["apple", "banana", "zebra"]))

    def test_sort_mixed_numbers_floats(self):
        """Test (sort [3.14 2 1.5 4]) sorts mixed numbers and floats."""
        result = run_lispy_string("(sort [3.14 2 1.5 4])", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1.5, 2, 3.14, 4]))

    def test_sort_with_custom_comparison_function(self):
        """Test sort with a custom comparison function for descending order."""
        run_lispy_string("(define desc (fn [a b] (> a b)))", self.env)
        result = run_lispy_string("(sort [1 3 2 5 4] desc)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([5, 4, 3, 2, 1]))

    def test_sort_with_custom_comparison_numeric(self):
        """Test sort with a custom comparison function returning numeric values."""
        run_lispy_string("(define numeric-desc (fn [a b] (- b a)))", self.env)
        result = run_lispy_string("(sort [1 3 2 5 4] numeric-desc)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([5, 4, 3, 2, 1]))

    def test_sort_with_absolute_value_comparison(self):
        """Test sort with custom comparison based on absolute values."""
        run_lispy_string(
            "(define abs-compare (fn [a b] (< (abs a) (abs b))))", self.env
        )
        # Define abs function for the test
        self.env.define("abs", lambda args, env: abs(args[0]))
        result = run_lispy_string("(sort [-3 1 -2 4 -1] abs-compare)", self.env)
        self.assertIsInstance(result, Vector)
        # Should be sorted by absolute value: [1, -1, -2, -3, 4]
        self.assertEqual(result, Vector([1, -1, -2, -3, 4]))

    def test_sort_original_vector_unchanged(self):
        """Test that sort does not mutate the original vector."""
        run_lispy_string("(define my-vec [3 1 4 1 5])", self.env)
        run_lispy_string("(sort my-vec)", self.env)
        original_vec = run_lispy_string("my-vec", self.env)
        self.assertIsInstance(original_vec, Vector)
        self.assertEqual(original_vec, Vector([3, 1, 4, 1, 5]))

    # --- Argument Validation Tests ---
    def test_sort_too_few_args(self):
        """Test sort with too few arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(sort)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'sort' expects 1 or 2 arguments, got 0."
        )

    def test_sort_too_many_args(self):
        """Test sort with too many arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(sort [1 2 3] + 'extra)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'sort' expects 1 or 2 arguments, got 3."
        )

    def test_sort_invalid_collection_type(self):
        """Test sort with invalid collection type."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(sort "not-a-vector")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'sort' first argument must be a vector, got <class 'str'>.",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(sort 123)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'sort' first argument must be a vector, got <class 'int'>.",
        )

    def test_sort_invalid_comparison_function(self):
        """Test sort with invalid comparison function."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(sort [1 2 3] 123)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Second argument to 'sort' must be a procedure, got <class 'int'>.",
        )

    def test_sort_comparison_function_wrong_arity(self):
        """Test sort with comparison function that has wrong arity."""
        run_lispy_string("(define wrong-arity (fn [x] true))", self.env)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(sort [1 2 3] wrong-arity)", self.env)
        self.assertEqual(
            str(cm.exception),
            "Comparison function <UserDefinedFunction params:(x)> passed to 'sort' expects 2 arguments, got 1.",
        )

    def test_sort_comparison_function_invalid_return(self):
        """Test sort with comparison function that returns invalid type."""
        run_lispy_string('(define bad-return (fn [a b] "not-a-number"))', self.env)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(sort [1 2 3] bad-return)", self.env)
        self.assertEqual(
            str(cm.exception),
            "Comparison function must return a number or boolean, got <class 'str'>.",
        )

    def test_sort_with_thread_first(self):
        """Test sort used with the -> (thread-first) macro."""
        result = run_lispy_string("(-> [3 1 4 1 5] sort)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 1, 3, 4, 5]))

        run_lispy_string("(define desc (fn [a b] (> a b)))", self.env)
        result = run_lispy_string("(-> [3 1 4 1 5] (sort desc))", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([5, 4, 3, 1, 1]))


if __name__ == "__main__":
    unittest.main()
