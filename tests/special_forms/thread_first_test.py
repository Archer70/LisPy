import unittest

from lispy.types import Vector
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError


# Helper Python function for string-append for testing purposes
def _py_string_append(args):
    if not all(isinstance(arg, str) for arg in args):
        raise EvaluationError("TypeError: string-append expects all arguments to be strings.")
    if len(args) == 0:
        return ""
    return "".join(args)

class ThreadFirstTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        # Define some simple functions for testing the pipeline
        run_lispy_string("(define add1 (fn [x] (+ x 1)))", self.env)
        run_lispy_string("(define mul2 (fn [x] (* x 2)))", self.env)
        # Register our Python helper for string-append
        self.env.define("string-append", _py_string_append)
        run_lispy_string("(define str-concat (fn [s1 s2] (string-append s1 s2)))", self.env)
        run_lispy_string("(define wrap-in-list (fn [x] (list x)))", self.env)
        run_lispy_string("(define to-vector (fn [x y] (vector x y)))", self.env)

    def test_basic_pipeline(self):
        """Test (-> initial-value func1 func2)"""
        # (-> 5 add1 mul2)  => (mul2 (add1 5)) => (mul2 6) => 12
        result = run_lispy_string("(-> 5 add1 mul2)", self.env)
        self.assertEqual(result, 12)

    def test_pipeline_with_initial_value_only(self):
        """Test (-> initial-value) returns initial-value."""
        result = run_lispy_string("(-> 100)", self.env)
        self.assertEqual(result, 100)

    def test_pipeline_with_functions_taking_more_args(self):
        """Test (-> initial-value (func arg2) func2)"""
        # (-> 3 (to-vector 4)) means (vector 3 4) -> [3 4]
        result = run_lispy_string("(-> 3 (to-vector 4))", self.env)
        self.assertEqual(result, Vector([3, 4]))

    def test_pipeline_with_function_symbol_and_list_form(self):
        """Test (-> initial-value func-symbol (list-form arg2))"""
        # (-> 5 add1 (to-vector 10))
        # => (to-vector (add1 5) 10) => (to-vector 6 10) => [6 10]
        result = run_lispy_string("(-> 5 add1 (to-vector 10))", self.env)
        self.assertEqual(result, Vector([6, 10]))

    def test_empty_pipeline_error(self):
        """Test (->) raises SyntaxError."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(->)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: '->' special form expects at least an initial value.")

    def test_invalid_form_in_pipeline(self):
        """Test (-> initial-value 123) where 123 is not a function or list."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(-> 5 123)", self.env)
        self.assertTrue("Invalid form in '->' pipeline" in str(cm.exception))

    def test_pipeline_with_string_concat_function(self):
        """Test piping through str-concat which uses string-append."""
        result = run_lispy_string('(-> "hello" (str-concat "-") (str-concat "world"))', self.env)
        self.assertEqual(result, "hello-world")

if __name__ == '__main__':
    unittest.main() 