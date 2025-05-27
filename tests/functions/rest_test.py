import unittest

from lispy.types import LispyList, Vector
from lispy.functions import create_global_env
from lispy.lexer import tokenize
from lispy.parser import parse
from lispy.evaluator import evaluate
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class RestFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_rest_on_list(self):
        """Test (rest '(1 2 3)) returns (2 3)."""
        lispy_code = "(rest '(1 2 3))"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([2, 3]))

    def test_rest_on_vector(self):
        """Test (rest [10 20 30]) returns [20 30]."""
        lispy_code = "(rest [10 20 30])"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, Vector([20, 30]))

    def test_rest_on_empty_list(self):
        """Test (rest '()) returns '()."""
        lispy_code = "(rest '())"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([]))

    def test_rest_on_empty_vector(self):
        """Test (rest []) returns []."""
        lispy_code = "(rest [])"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, Vector([]))

    def test_rest_on_list_with_one_element(self):
        """Test (rest '(99)) returns '()."""
        lispy_code = "(rest '(99))"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([]))

    def test_rest_on_vector_with_one_element(self):
        """Test (rest [77]) returns []."""
        lispy_code = "(rest [77])"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, Vector([]))

    def test_rest_on_nil(self):
        """Test (rest nil) returns '()."""
        lispy_code = "(rest nil)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([]))

    def test_rest_wrong_type(self):
        """Test (rest {:a 1}) raises TypeError."""
        lispy_code = "(rest {:a 1})"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'rest' expects a list, vector, or nil, got <class 'dict'>.")

    def test_rest_too_many_args(self):
        """Test (rest '(1 2) '(3 4)) raises SyntaxError."""
        lispy_code = "(rest '(1 2) '(3 4))"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'rest' expects 1 argument, got 2.")

    def test_rest_no_args(self):
        """Test (rest) raises SyntaxError."""
        lispy_code = "(rest)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'rest' expects 1 argument, got 0.")

    def test_rest_on_string_error(self):
        """Test (rest \"hello\") raises TypeError."""
        lispy_code = '(rest "hello")'
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'rest' expects a list, vector, or nil, got <class 'str'>.")


if __name__ == '__main__':
    unittest.main() 