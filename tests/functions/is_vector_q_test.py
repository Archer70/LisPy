# tests/functions/vector_q_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class IsVectorQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_vector_q_empty_vector(self):
        """Test (is_vector? []) returns true."""
        self.assertTrue(run_lispy_string("(is_vector? [])", self.env))

    def test_vector_q_vector_with_elements(self):
        """Test (is_vector? [1 2 3]) returns true."""
        self.assertTrue(run_lispy_string("(is_vector? [1 2 3])", self.env))

    def test_vector_q_vector_function_result(self):
        """Test (is_vector? (vector 1 2 3)) returns true."""
        self.assertTrue(run_lispy_string("(is_vector? (vector 1 2 3))", self.env))

    def test_vector_q_nested_vector(self):
        """Test (is_vector? [1 [2 3] 4]) returns true."""
        self.assertTrue(run_lispy_string("(is_vector? [1 [2 3] 4])", self.env))

    def test_vector_q_mixed_types_vector(self):
        """Test (is_vector? [1 \"hello\" true nil]) returns true."""
        self.assertTrue(run_lispy_string("(is_vector? [1 \"hello\" true nil])", self.env))

    def test_vector_q_vector_with_list(self):
        """Test (is_vector? [1 '(2 3) 4]) returns true."""
        self.assertTrue(run_lispy_string("(is_vector? [1 '(2 3) 4])", self.env))

    def test_vector_q_list(self):
        """Test (is_vector? '(1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is_vector? '(1 2 3))", self.env))

    def test_vector_q_empty_list(self):
        """Test (is_vector? '()) returns false."""
        self.assertFalse(run_lispy_string("(is_vector? '())", self.env))

    def test_vector_q_list_function_result(self):
        """Test (is_vector? (list 1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is_vector? (list 1 2 3))", self.env))

    def test_vector_q_string(self):
        """Test (is_vector? \"hello\") returns false."""
        self.assertFalse(run_lispy_string('(is_vector? "hello")', self.env))

    def test_vector_q_number(self):
        """Test (is_vector? 42) returns false."""
        self.assertFalse(run_lispy_string("(is_vector? 42)", self.env))

    def test_vector_q_boolean_true(self):
        """Test (is_vector? true) returns false."""
        self.assertFalse(run_lispy_string("(is_vector? true)", self.env))

    def test_vector_q_boolean_false(self):
        """Test (is_vector? false) returns false."""
        self.assertFalse(run_lispy_string("(is_vector? false)", self.env))

    def test_vector_q_nil(self):
        """Test (is_vector? nil) returns false."""
        self.assertFalse(run_lispy_string("(is_vector? nil)", self.env))

    def test_vector_q_map(self):
        """Test (is_vector? {:a 1}) returns false."""
        self.assertFalse(run_lispy_string("(is_vector? {:a 1})", self.env))

    def test_vector_q_symbol(self):
        """Test (is_vector? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is_vector? 'x)", self.env))

    def test_vector_q_no_args(self):
        """Test (is_vector?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is_vector?)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'is_vector?' expects 1 argument, got 0.")

    def test_vector_q_too_many_args(self):
        """Test (is_vector? [1] [2]) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is_vector? [1] [2])", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'is_vector?' expects 1 argument, got 2.")

    def test_vector_q_vs_list_q_distinction(self):
        """Test that is_vector? and is_list? correctly distinguish between vectors and lists."""
        # Test that is_vector? returns true for vectors but false for lists
        self.assertTrue(run_lispy_string("(is_vector? (vector 1 2 3))", self.env))
        self.assertFalse(run_lispy_string("(is_vector? (list 1 2 3))", self.env))
        
        # Test that is_list? returns true for lists but false for vectors  
        self.assertTrue(run_lispy_string("(is_list? (list 1 2 3))", self.env))
        self.assertFalse(run_lispy_string("(is_list? (vector 1 2 3))", self.env))


if __name__ == '__main__':
    unittest.main() 