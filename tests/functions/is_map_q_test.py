# tests/functions/map_q_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class IsMapQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_map_q_empty_map(self):
        """Test (is_map? {}) returns true."""
        self.assertTrue(run_lispy_string("(is_map? {})", self.env))

    def test_map_q_map_with_elements(self):
        """Test (is_map? {:a 1 :b 2}) returns true."""
        self.assertTrue(run_lispy_string("(is_map? {:a 1 :b 2})", self.env))

    def test_map_q_hash_map_function_result(self):
        """Test (is_map? (hash-map 'a 1 'b 2)) returns true."""
        self.assertTrue(run_lispy_string("(is_map? (hash-map 'a 1 'b 2))", self.env))

    def test_map_q_nested_map(self):
        """Test (is_map? {:a {:b 2} :c 3}) returns true."""
        self.assertTrue(run_lispy_string("(is_map? {:a {:b 2} :c 3})", self.env))

    def test_map_q_map_with_mixed_types(self):
        """Test (is_map? {:a 1 :b \"hello\" :c true :d nil}) returns true."""
        self.assertTrue(run_lispy_string("(is_map? {:a 1 :b \"hello\" :c true :d nil})", self.env))

    def test_map_q_map_with_collections(self):
        """Test (is_map? {:list '(1 2) :vector [3 4]}) returns true."""
        self.assertTrue(run_lispy_string("(is_map? {:list '(1 2) :vector [3 4]})", self.env))

    def test_map_q_vector(self):
        """Test (is_map? [1 2 3]) returns false."""
        self.assertFalse(run_lispy_string("(is_map? [1 2 3])", self.env))

    def test_map_q_list(self):
        """Test (is_map? '(1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is_map? '(1 2 3))", self.env))

    def test_map_q_string(self):
        """Test (is_map? \"hello\") returns false."""
        self.assertFalse(run_lispy_string('(is_map? "hello")', self.env))

    def test_map_q_number(self):
        """Test (is_map? 42) returns false."""
        self.assertFalse(run_lispy_string("(is_map? 42)", self.env))

    def test_map_q_boolean_true(self):
        """Test (is_map? true) returns false."""
        self.assertFalse(run_lispy_string("(is_map? true)", self.env))

    def test_map_q_boolean_false(self):
        """Test (is_map? false) returns false."""
        self.assertFalse(run_lispy_string("(is_map? false)", self.env))

    def test_map_q_nil(self):
        """Test (is_map? nil) returns false."""
        self.assertFalse(run_lispy_string("(is_map? nil)", self.env))

    def test_map_q_symbol(self):
        """Test (is_map? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is_map? 'x)", self.env))

    def test_map_q_no_args(self):
        """Test (is_map?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is_map?)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'is_map?' expects 1 argument, got 0.")

    def test_map_q_too_many_args(self):
        """Test (is_map? {} {}) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is_map? {} {})", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'is_map?' expects 1 argument, got 2.")


if __name__ == '__main__':
    unittest.main() 