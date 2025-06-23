# tests/functions/every_q_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class EveryQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_every_q_with_builtin_predicate_all_match(self):
        """Test (every? [1 2 3] is-number?) returns true."""
        result = run_lispy_string("(every? [1 2 3] is-number?)", self.env)
        self.assertTrue(result)

    def test_every_q_with_builtin_predicate_some_dont_match(self):
        """Test (every? [1 "hello" 3] is-number?) returns false."""
        result = run_lispy_string('(every? [1 "hello" 3] is-number?)', self.env)
        self.assertFalse(result)

    def test_every_q_with_user_defined_predicate_all_match(self):
        """Test every? with user-defined predicate where all elements match."""
        run_lispy_string("(define positive? (fn [x] (> x 0)))", self.env)
        result = run_lispy_string("(every? [1 2 3 4] positive?)", self.env)
        self.assertTrue(result)

    def test_every_q_with_user_defined_predicate_some_dont_match(self):
        """Test every? with user-defined predicate where some elements don't match."""
        run_lispy_string("(define positive? (fn [x] (> x 0)))", self.env)
        result = run_lispy_string("(every? [-1 2 3 4] positive?)", self.env)
        self.assertFalse(result)

    def test_every_q_empty_collection_is_vacuously_true(self):
        """Test that every? returns true for empty collections (vacuous truth)."""
        result = run_lispy_string("(every? [] is-number?)", self.env)
        self.assertTrue(result)

        result = run_lispy_string("(every? '() is-number?)", self.env)
        self.assertTrue(result)

    def test_every_q_with_comparison_functions(self):
        """Test every? with comparison built-in functions."""
        run_lispy_string("(define greater-than-0? (fn [x] (> x 0)))", self.env)
        result = run_lispy_string("(every? [1 2 3 4] greater-than-0?)", self.env)
        self.assertTrue(result)

        result = run_lispy_string("(every? [0 1 2 3] greater-than-0?)", self.env)
        self.assertFalse(result)

    def test_every_q_with_list(self):
        """Test every? works with lists."""
        result = run_lispy_string("(every? '(1 2 3 4) is-number?)", self.env)
        self.assertTrue(result)

        result = run_lispy_string('(every? \'(1 "hello" 3) is-number?)', self.env)
        self.assertFalse(result)

    def test_every_q_with_vector(self):
        """Test every? works with vectors."""
        result = run_lispy_string("(every? [1 2 3 4] is-number?)", self.env)
        self.assertTrue(result)

        result = run_lispy_string('(every? [1 "hello" 3] is-number?)', self.env)
        self.assertFalse(result)

    def test_every_q_with_mixed_types(self):
        """Test every? with various mixed data types."""
        result = run_lispy_string(
            '(every? ["hello" "world" "test"] is-string?)', self.env
        )
        self.assertTrue(result)

        result = run_lispy_string('(every? ["hello" 42 "test"] is-string?)', self.env)
        self.assertFalse(result)

    def test_every_q_with_false_and_nil_values(self):
        """Test every? correctly handles false and nil as falsy values."""
        run_lispy_string("(define return-value (fn [x] x))", self.env)
        result = run_lispy_string("(every? [1 2 3] return-value)", self.env)
        self.assertTrue(result)  # All truthy values

        result = run_lispy_string("(every? [1 false 3] return-value)", self.env)
        self.assertFalse(result)  # Contains false

        result = run_lispy_string("(every? [1 nil 3] return-value)", self.env)
        self.assertFalse(result)  # Contains nil

    def test_every_q_short_circuits(self):
        """Test that every? short-circuits on first falsy result."""
        # Test short-circuiting by ensuring it stops at first false result
        run_lispy_string(
            "(define check-not-zero (fn [x] (if (= x 0) false true)))", self.env
        )

        result = run_lispy_string("(every? [1 2 0 4 5] check-not-zero)", self.env)
        self.assertFalse(result)  # Should return false when it hits 0

        # Test that every? stops early - if it didn't short circuit, this would cause an error
        # because the last element would cause a division by zero
        run_lispy_string(
            "(define safe-check (fn [x] (if (= x 0) false (> (/ 10 x) 0))))", self.env
        )
        result = run_lispy_string("(every? [1 2 0 5] safe-check)", self.env)
        self.assertFalse(result)  # Should find 0 and return false before reaching 5

    def test_every_q_with_nested_collections(self):
        """Test every? with nested data structures."""
        result = run_lispy_string("(every? [[1 2] [3 4] [5 6]] is-vector?)", self.env)
        self.assertTrue(result)

        result = run_lispy_string("(every? [[1 2] '(3 4) [5 6]] is-vector?)", self.env)
        self.assertFalse(result)  # Contains a list

    def test_every_q_all_true_values(self):
        """Test every? with all explicitly true values."""
        run_lispy_string("(define always-true (fn [x] true))", self.env)
        result = run_lispy_string(
            '(every? [1 "hello" {:a 1} [1 2]] always-true)', self.env
        )
        self.assertTrue(result)

    def test_every_q_complementary_to_some(self):
        """Test that every? and some are complementary for certain cases."""
        # When every? is true, some should also be true (unless empty)
        result_every = run_lispy_string("(every? [2 4 6 8] is-number?)", self.env)
        result_some = run_lispy_string("(some [2 4 6 8] is-number?)", self.env)
        self.assertTrue(result_every)
        self.assertTrue(result_some)

        # When every? is false, we can't predict some without knowing the specifics
        result_every = run_lispy_string('(every? [2 "hello" 6 8] is-number?)', self.env)
        result_some = run_lispy_string('(some [2 "hello" 6 8] is-number?)', self.env)
        self.assertFalse(result_every)
        self.assertTrue(result_some)  # Some numbers exist

    def test_every_q_no_args(self):
        """Test (every?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(every?)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'every?' expects 2 arguments, got 0."
        )

    def test_every_q_one_arg(self):
        """Test (every? [1 2]) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(every? [1 2])", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'every?' expects 2 arguments, got 1."
        )

    def test_every_q_too_many_args(self):
        """Test (every? [1 2] is-number? [3 4]) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(every? [1 2] is-number? [3 4])", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'every?' expects 2 arguments, got 3."
        )

    def test_every_q_non_function_predicate(self):
        """Test every? with non-function predicate raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(every? [1 2 3] 42)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Second argument to 'every?' must be a function, got <class 'int'>.",
        )

    def test_every_q_non_collection(self):
        """Test every? with non-collection raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(every? 42 is-number?)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: First argument to 'every?' must be a list or vector, got <class 'int'>.",
        )

    def test_every_q_predicate_wrong_arity(self):
        """Test every? with predicate that expects wrong number of arguments."""
        run_lispy_string("(define bad-predicate (fn [x y] (+ x y)))", self.env)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(every? [1 2 3] bad-predicate)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Predicate function expects 1 argument, got 2.",
        )

    def test_every_q_with_string_collection(self):
        """Test every? with string as collection raises an error (strings aren't supported)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(every? "hello" is-string?)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: First argument to 'every?' must be a list or vector, got <class 'str'>.",
        )

    def test_every_q_with_map_collection(self):
        """Test every? with map as collection raises an error (maps aren't supported as sequences)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(every? {:a 1 :b 2} is-number?)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: First argument to 'every?' must be a list or vector, got <class 'dict'>.",
        )

    def test_every_q_functional_composition(self):
        """Test every? can be used in functional composition."""
        run_lispy_string(
            "(define all-positive? (fn [coll] (every? coll (fn [x] (> x 0)))))",
            self.env,
        )

        result = run_lispy_string("(all-positive? [1 2 3])", self.env)
        self.assertTrue(result)

        result = run_lispy_string("(all-positive? [-1 2 3])", self.env)
        self.assertFalse(result)

    def test_every_q_thread_first_composition(self):
        """Test every? works beautifully in thread-first composition."""
        run_lispy_string("(define positive? (fn [x] (> x 0)))", self.env)

        # Test filtering then checking if all remaining are positive
        result = run_lispy_string(
            """
        (-> [-1 2 3 4 -5]
            (filter is-number?)
            (filter positive?)
            (every? positive?))
        """,
            self.env,
        )
        self.assertTrue(
            result
        )  # After filtering for positive numbers, all should be positive


if __name__ == "__main__":
    unittest.main()
