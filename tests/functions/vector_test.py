import unittest

from lispy.types import Vector
from lispy.functions import create_global_env
from lispy.lexer import tokenize
from lispy.parser import parse
from lispy.evaluator import evaluate
from lispy.exceptions import EvaluationError


class VectorFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_vector_fn_empty(self):
        """Test (vector) creates an empty vector."""
        lispy_code = "(vector)"
        ast = parse(tokenize(lispy_code))
        result = evaluate(ast, self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, Vector([]))

    def test_vector_fn_with_numbers(self):
        """Test (vector 1 2 3) creates a vector of numbers."""
        lispy_code = "(vector 1 2 3)"
        ast = parse(tokenize(lispy_code))
        result = evaluate(ast, self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 2, 3]))

    def test_vector_fn_with_mixed_types(self):
        """Test (vector 1 \"two\" true nil) creates a vector of mixed types."""
        lispy_code = '(vector 1 "two" true nil)'
        ast = parse(tokenize(lispy_code))
        result = evaluate(ast, self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, "two", True, None]))

    def test_vector_fn_with_nested_structure(self):
        """Test (vector 1 (vector 2 3) 4) creates a nested vector."""
        lispy_code = "(vector 1 (vector 2 3) 4)"
        ast = parse(tokenize(lispy_code))
        result = evaluate(ast, self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, Vector([2, 3]), 4]))

    def test_vector_fn_evaluates_arguments(self):
        """Test that arguments to (vector ...) are evaluated."""
        evaluate(parse(tokenize("(define x 10)")), self.env)
        lispy_code = "(vector x (+ 1 2) (vector (* 2 3)))"
        ast = parse(tokenize(lispy_code))
        result = evaluate(ast, self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([10, 3, Vector([6])]))


if __name__ == '__main__':
    unittest.main() 