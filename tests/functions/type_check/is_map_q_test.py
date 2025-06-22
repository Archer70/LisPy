# tests/functions/map_q_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class IsMapQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_map_q_empty_map(self):
        """Test (is-map? {}) returns true."""
        self.assertTrue(run_lispy_string("(is-map? {})", self.env))

    def test_map_q_map_with_elements(self):
        """Test (is-map? {:a 1 :b 2}) returns true."""
        self.assertTrue(run_lispy_string("(is-map? {:a 1 :b 2})", self.env))

    def test_map_q_hash_map_function_result(self):
        """Test (is-map? (hash-map 'a 1 'b 2)) returns true."""
        self.assertTrue(run_lispy_string("(is-map? (hash-map 'a 1 'b 2))", self.env))

    def test_map_q_nested_map(self):
        """Test (is-map? {:a {:b 2} :c 3}) returns true."""
        self.assertTrue(run_lispy_string("(is-map? {:a {:b 2} :c 3})", self.env))

    def test_map_q_map_with_mixed_types(self):
        """Test (is-map? {:a 1 :b \"hello\" :c true :d nil}) returns true."""
        self.assertTrue(
            run_lispy_string('(is-map? {:a 1 :b "hello" :c true :d nil})', self.env)
        )

    def test_map_q_map_with_collections(self):
        """Test (is-map? {:list '(1 2) :vector [3 4]}) returns true."""
        self.assertTrue(
            run_lispy_string("(is-map? {:list '(1 2) :vector [3 4]})", self.env)
        )

    def test_map_q_vector(self):
        """Test (is-map? [1 2 3]) returns false."""
        self.assertFalse(run_lispy_string("(is-map? [1 2 3])", self.env))

    def test_map_q_list(self):
        """Test (is-map? '(1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is-map? '(1 2 3))", self.env))

    def test_map_q_string(self):
        """Test (is-map? \"hello\") returns false."""
        self.assertFalse(run_lispy_string('(is-map? "hello")', self.env))

    def test_map_q_number(self):
        """Test (is-map? 42) returns false."""
        self.assertFalse(run_lispy_string("(is-map? 42)", self.env))

    def test_map_q_boolean_true(self):
        """Test (is-map? true) returns false."""
        self.assertFalse(run_lispy_string("(is-map? true)", self.env))

    def test_map_q_boolean_false(self):
        """Test (is-map? false) returns false."""
        self.assertFalse(run_lispy_string("(is-map? false)", self.env))

    def test_map_q_nil(self):
        """Test (is-map? nil) returns false."""
        self.assertFalse(run_lispy_string("(is-map? nil)", self.env))

    def test_map_q_symbol(self):
        """Test (is-map? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is-map? 'x)", self.env))

    def test_map_q_no_args(self):
        """Test (is-map?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-map?)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-map?' expects 1 argument, got 0."
        )

    def test_map_q_too_many_args(self):
        """Test (is-map? {} {}) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-map? {} {})", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-map?' expects 1 argument, got 2."
        )


if __name__ == "__main__":
    unittest.main()
