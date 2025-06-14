# tests/functions/doc_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class DocFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_doc_with_add_function(self):
        """Test (doc +) returns documentation for add function."""
        result = run_lispy_string("(doc +)", self.env)
        self.assertIsInstance(result, str)
        self.assertIn("Function: +", result)
        self.assertIn("Arguments:", result)
        self.assertIn("Examples:", result)

    def test_doc_with_abs_function(self):
        """Test (doc abs) returns documentation for abs function."""
        result = run_lispy_string("(doc abs)", self.env)
        self.assertIsInstance(result, str)
        self.assertIn("Function: abs", result)
        self.assertIn("(abs number)", result)
        self.assertIn("absolute value", result)

    def test_doc_with_doc_function(self):
        """Test (doc doc) returns documentation for doc function itself."""
        result = run_lispy_string("(doc doc)", self.env)
        self.assertIsInstance(result, str)
        self.assertIn("Function: doc", result)
        self.assertIn("(doc function)", result)

    def test_doc_with_undocumented_function(self):
        """Test doc with a function that has no documentation."""
        # Define a user function that won't have documentation
        run_lispy_string("(define my-test-fn (fn [x] (+ x 1)))", self.env)
        result = run_lispy_string("(doc my-test-fn)", self.env)
        self.assertIsInstance(result, str)
        self.assertIn("No documentation available", result)

    def test_doc_no_args(self):
        """Test (doc) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(doc)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'doc' expects 1 argument, got 0."
        )

    def test_doc_too_many_args(self):
        """Test (doc + abs) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(doc + abs)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'doc' expects 1 argument, got 2."
        )

    def test_doc_with_non_function(self):
        """Test doc with non-function argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(doc 42)", self.env)
        self.assertIn("Unable to find documentation", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
