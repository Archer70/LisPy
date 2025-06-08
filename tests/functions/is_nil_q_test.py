# tests/functions/nil_q_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class IsNilQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_nil_q_nil(self):
        """Test (is_nil? nil) returns true."""
        self.assertTrue(run_lispy_string("(is_nil? nil)", self.env))

    def test_nil_q_number_zero(self):
        """Test (is_nil? 0) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? 0)", self.env))

    def test_nil_q_number_positive(self):
        """Test (is_nil? 42) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? 42)", self.env))

    def test_nil_q_number_negative(self):
        """Test (is_nil? -17) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? -17)", self.env))

    def test_nil_q_float(self):
        """Test (is_nil? 3.14) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? 3.14)", self.env))

    def test_nil_q_boolean_true(self):
        """Test (is_nil? true) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? true)", self.env))

    def test_nil_q_boolean_false(self):
        """Test (is_nil? false) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? false)", self.env))

    def test_nil_q_string(self):
        """Test (is_nil? \"hello\") returns false."""
        self.assertFalse(run_lispy_string('(is_nil? "hello")', self.env))

    def test_nil_q_empty_string(self):
        """Test (is_nil? \"\") returns false."""
        self.assertFalse(run_lispy_string('(is_nil? "")', self.env))

    def test_nil_q_empty_list(self):
        """Test (is_nil? '()) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? '())", self.env))

    def test_nil_q_list_with_elements(self):
        """Test (is_nil? '(1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? '(1 2 3))", self.env))

    def test_nil_q_empty_vector(self):
        """Test (is_nil? []) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? [])", self.env))

    def test_nil_q_vector_with_elements(self):
        """Test (is_nil? [1 2 3]) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? [1 2 3])", self.env))

    def test_nil_q_empty_map(self):
        """Test (is_nil? {}) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? {})", self.env))

    def test_nil_q_map_with_elements(self):
        """Test (is_nil? {:a 1}) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? {:a 1})", self.env))

    def test_nil_q_symbol(self):
        """Test (is_nil? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is_nil? 'x)", self.env))

    def test_nil_q_function_result_nil(self):
        """Test that is_nil? correctly identifies nil returned from functions."""
        # First test: a function that returns nil
        run_lispy_string("(define get-nil (fn [] nil))", self.env)
        self.assertTrue(run_lispy_string("(is_nil? (get-nil))", self.env))

    def test_nil_q_function_result_not_nil(self):
        """Test that is_nil? correctly identifies non-nil values returned from functions."""
        # Test: a function that returns something other than nil
        run_lispy_string("(define get-value (fn [] 42))", self.env)
        self.assertFalse(run_lispy_string("(is_nil? (get-value))", self.env))

    def test_nil_q_no_args(self):
        """Test (is_nil?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is_nil?)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'is_nil?' expects 1 argument, got 0.")

    def test_nil_q_too_many_args(self):
        """Test (is_nil? nil nil) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is_nil? nil nil)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'is_nil?' expects 1 argument, got 2.")


if __name__ == '__main__':
    unittest.main() 