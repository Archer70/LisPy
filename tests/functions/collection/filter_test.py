import unittest

from lispy.exceptions import ArityError, EvaluationError
from lispy.functions import create_global_env
from lispy.types import LispyList, Vector
from lispy.utils import run_lispy_string


class FilterFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        run_lispy_string("(define even? (fn [x] (= (% x 2) 0)))", self.env)
        run_lispy_string("(define odd? (fn [x] (not (= (% x 2) 0))))", self.env)

        self.env.store["py-is-number?"] = lambda args, env: isinstance(
            args[0], (int, float)
        )
        run_lispy_string("(define is-number? (fn [x] (py-is-number? x)))", self.env)

        self.env.store["py-is-string?"] = lambda args, env: isinstance(args[0], str)
        run_lispy_string("(define is-string? (fn [x] (py-is-string? x)))", self.env)

        run_lispy_string("(define always-true (fn [x] true))", self.env)
        run_lispy_string("(define always-false (fn [x] false))", self.env)

        # For arity testing of the predicate
        run_lispy_string("(define zero-arg-pred (fn [] true))", self.env)
        run_lispy_string("(define two-arg-pred (fn [a b] true))", self.env)

    def test_filter_empty_vector(self):
        """Test (filter odd? []) returns []."""
        result = run_lispy_string("(filter [] odd?)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_filter_empty_list(self):
        """Test (filter odd? '()) returns '()."""
        result = run_lispy_string("(filter '() odd?)", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([]))

    def test_filter_vector_keep_some_odd(self):
        """Test (filter [1 2 3 4 5] odd?) returns [1 3 5]."""
        result = run_lispy_string("(filter [1 2 3 4 5] odd?)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 3, 5]))

    def test_filter_list_keep_some_even(self):
        """Test (filter '(1 2 3 4 5) even?) returns (2 4)."""
        result = run_lispy_string("(filter '(1 2 3 4 5) even?)", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([2, 4]))

    def test_filter_vector_keep_all(self):
        """Test (filter [1 2 3] always-true) returns [1 2 3]."""
        result = run_lispy_string("(filter [1 2 3] always-true)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3]))

    def test_filter_list_keep_all_numbers(self):
        """Test (filter '(1 2.0 3) is-number?) returns (1 2.0 3)."""
        result = run_lispy_string("(filter '(1 2.0 3) is-number?)", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([1, 2.0, 3]))

    def test_filter_vector_keep_none(self):
        """Test (filter [1 2 3] always-false) returns []."""
        result = run_lispy_string("(filter [1 2 3] always-false)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_filter_list_keep_none_strings(self):
        """Test (filter '(1 2 3) is-string?) returns '()."""
        result = run_lispy_string("(filter '(1 2 3) is-string?)", self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList([]))

    def test_filter_mixed_collection_vector(self):
        """Test filtering a mixed vector, result is a vector."""
        lispy_code = '(filter [1 "a" 2.0 "b" 3] is-number?)'
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2.0, 3]))

    def test_filter_mixed_collection_list(self):
        """Test filtering a mixed list, result is a list."""
        lispy_code = '(filter \'(1 "a" 2.0 "b" 3) is-string?)'
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, LispyList)
        self.assertEqual(result, LispyList(["a", "b"]))

    def test_filter_original_collection_unchanged(self):
        """Test that filter does not mutate the original collection."""
        run_lispy_string("(define my-vec [10 20 30 40])", self.env)
        run_lispy_string("(filter my-vec even?)", self.env)
        original_vec = run_lispy_string("my-vec", self.env)
        self.assertIsInstance(original_vec, Vector)
        self.assertEqual(original_vec, Vector([10, 20, 30, 40]))

    # --- Argument Validation Tests ---
    def test_filter_too_few_args(self):
        """Test filter with too few arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(filter)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'filter' expects 2 arguments, got 0."
        )
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(filter [])", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'filter' expects 2 arguments, got 1."
        )

    def test_filter_too_many_args(self):
        """Test filter with too many arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(filter [] odd? 'extra)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'filter' expects 2 arguments, got 3."
        )

    def test_filter_collection_not_list_or_vector(self):
        """Test filter when collection is not a list or vector."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(filter "abc" odd?)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: First argument to 'filter' must be a list or vector, got <class 'str'>.",
        )
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(filter 123 odd?)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: First argument to 'filter' must be a list or vector, got <class 'int'>.",
        )

    def test_filter_predicate_not_callable(self):
        """Test filter when the predicate argument is not callable."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(filter [1 2 3] 123)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Second argument to 'filter' must be a procedure, got <class 'int'>.",
        )

    # --- Predicate Arity Tests ---
    def test_filter_pred_arity_zero(self):
        """Test filter when the predicate expects 0 arguments."""
        with self.assertRaises(ArityError) as cm:
            run_lispy_string("(filter [1 2] zero-arg-pred)", self.env)
        self.assertEqual(
            str(cm.exception),
            "Procedure <UserDefinedFunction params:()> passed to 'filter' expects 1 argument, got 0.",
        )

    def test_filter_pred_arity_two(self):
        """Test filter when the predicate expects 2 arguments."""
        with self.assertRaises(ArityError) as cm:
            run_lispy_string("(filter [1 2] two-arg-pred)", self.env)
        self.assertEqual(
            str(cm.exception),
            "Procedure <UserDefinedFunction params:(a, b)> passed to 'filter' expects 1 argument, got 2.",
        )

    def test_filter_with_thread_first(self):
        """Test filter used with the -> (thread-first) special form."""
        result = run_lispy_string("(-> [1 2 3 4 5] (filter odd?))", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 3, 5]))

        result_list = run_lispy_string("(-> '(1 2 3 4 5) (filter even?))", self.env)
        self.assertIsInstance(result_list, LispyList)
        self.assertEqual(result_list, LispyList([2, 4]))


if __name__ == "__main__":
    unittest.main()
