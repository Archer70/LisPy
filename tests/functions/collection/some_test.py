# tests/functions/some_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class SomeFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_some_with_builtin_predicate_found(self):
        """Test (some [1 "hello" 3] is_number?) returns true."""
        result = run_lispy_string('(some [1 "hello" 3] is_number?)', self.env)
        self.assertTrue(result)

    def test_some_with_builtin_predicate_not_found(self):
        """Test (some ["hello" "world"] is_number?) returns nil."""
        result = run_lispy_string('(some ["hello" "world"] is_number?)', self.env)
        self.assertIsNone(result)

    def test_some_with_user_defined_predicate_found(self):
        """Test some with user-defined predicate that finds a match."""
        run_lispy_string("(define positive? (fn [x] (> x 0)))", self.env)
        result = run_lispy_string("(some [-1 0 5 -3] positive?)", self.env)
        self.assertTrue(result)

    def test_some_with_user_defined_predicate_not_found(self):
        """Test some with user-defined predicate that finds no match."""
        run_lispy_string("(define positive? (fn [x] (> x 0)))", self.env)
        result = run_lispy_string("(some [-1 -2 -3] positive?)", self.env)
        self.assertIsNone(result)

    def test_some_returns_first_truthy_value(self):
        """Test that some returns the first truthy value, not just true."""
        run_lispy_string("(define return-self (fn [x] x))", self.env)
        result = run_lispy_string("(some [nil false 42 100] return-self)", self.env)
        self.assertEqual(result, 42)

    def test_some_with_comparison_functions(self):
        """Test some with comparison built-in functions."""
        # Test with > function - create a partially applied function first
        run_lispy_string("(define greater-than-5? (fn [x] (> x 5)))", self.env)
        result = run_lispy_string("(some [1 2 3 10 4] greater-than-5?)", self.env)
        self.assertTrue(result)

        result = run_lispy_string("(some [1 2 3 4] greater-than-5?)", self.env)
        self.assertIsNone(result)

    def test_some_with_empty_list(self):
        """Test (some '() is_number?) returns nil."""
        result = run_lispy_string("(some '() is_number?)", self.env)
        self.assertIsNone(result)

    def test_some_with_empty_vector(self):
        """Test (some [] is_number?) returns nil."""
        result = run_lispy_string("(some [] is_number?)", self.env)
        self.assertIsNone(result)

    def test_some_with_list(self):
        """Test some works with lists."""
        result = run_lispy_string('(some \'(1 2 "found" 4) is_string?)', self.env)
        self.assertTrue(result)

    def test_some_with_vector(self):
        """Test some works with vectors."""
        result = run_lispy_string('(some [1 2 "found" 4] is_string?)', self.env)
        self.assertTrue(result)

    def test_some_with_mixed_types(self):
        """Test some with various mixed data types."""
        result = run_lispy_string(
            '(some [1 "hello" true {:a 1}] is_boolean?)', self.env
        )
        self.assertTrue(result)

        result = run_lispy_string('(some [1 "hello" true {:a 1}] is_map?)', self.env)
        # is_map? returns True when it finds a map, not the map itself
        self.assertTrue(result)

    def test_some_preserves_predicate_return_value(self):
        """Test that some preserves the actual return value of the predicate."""
        run_lispy_string(
            "(define return-double (fn [x] (if (is_number? x) (* x 2) false)))",
            self.env,
        )
        result = run_lispy_string('(some ["hello" 5 "world"] return-double)', self.env)
        self.assertEqual(result, 10)  # 5 * 2

    def test_some_with_false_and_nil_values(self):
        """Test some correctly handles false and nil as falsy values."""
        run_lispy_string("(define return-value (fn [x] x))", self.env)
        result = run_lispy_string('(some [false nil 0 ""] return-value)', self.env)
        self.assertEqual(result, 0)  # First truthy value

    def test_some_short_circuits(self):
        """Test that some short-circuits and doesn't evaluate remaining elements."""
        # Test short-circuiting by checking that some stops at first truthy result
        run_lispy_string("(define check-value (fn [x] (if (= x 3) x false)))", self.env)

        result = run_lispy_string("(some [1 2 3 4 5] check-value)", self.env)
        self.assertEqual(result, 3)  # Should return 3 (the first truthy result)

        # Test that some stops early - if it didn't short circuit, this would cause an error
        # because the last element would cause a division by zero
        run_lispy_string(
            "(define safe-check (fn [x] (if (= x 3) true (if (= x 0) (/ 1 x) false))))",
            self.env,
        )
        result = run_lispy_string("(some [1 2 3 0] safe-check)", self.env)
        self.assertTrue(result)  # Should find 3 before reaching 0

    def test_some_with_nested_collections(self):
        """Test some with nested data structures."""
        run_lispy_string("(define has-nested-list? (fn [x] (is_list? x)))", self.env)
        result = run_lispy_string(
            '(some [1 "hello" \'(1 2 3) {:a 1}] has-nested-list?)', self.env
        )
        self.assertTrue(result)

    def test_some_no_args(self):
        """Test (some) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(some)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'some' expects 2 arguments, got 0."
        )

    def test_some_one_arg(self):
        """Test (some [1 2]) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(some [1 2])", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'some' expects 2 arguments, got 1."
        )

    def test_some_too_many_args(self):
        """Test (some [1 2] is_number? [3 4]) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(some [1 2] is_number? [3 4])", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'some' expects 2 arguments, got 3."
        )

    def test_some_non_function_predicate(self):
        """Test some with non-function predicate raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(some [1 2 3] 42)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Second argument to 'some' must be a function, got <class 'int'>.",
        )

    def test_some_non_collection(self):
        """Test some with non-collection raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(some 42 is_number?)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: First argument to 'some' must be a list or vector, got <class 'int'>.",
        )

    def test_some_predicate_wrong_arity(self):
        """Test some with predicate that expects wrong number of arguments."""
        run_lispy_string("(define bad-predicate (fn [x y] (+ x y)))", self.env)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(some [1 2 3] bad-predicate)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Predicate function expects 1 argument, got 2.",
        )

    def test_some_with_string_collection(self):
        """Test some with string as collection raises an error (strings aren't supported)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(some "hello" is_number?)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: First argument to 'some' must be a list or vector, got <class 'str'>.",
        )

    def test_some_with_map_collection(self):
        """Test some with map as collection raises an error (maps aren't supported as sequences)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(some {:a 1 :b 2} is_number?)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: First argument to 'some' must be a list or vector, got <class 'dict'>.",
        )

    def test_some_functional_composition(self):
        """Test some can be used in functional composition."""
        run_lispy_string(
            "(define has-positive? (fn [coll] (some coll (fn [x] (> x 0)))))", self.env
        )

        result = run_lispy_string("(has-positive? [-1 -2 3])", self.env)
        self.assertTrue(result)

        result = run_lispy_string("(has-positive? [-1 -2 -3])", self.env)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
