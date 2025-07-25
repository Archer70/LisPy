# tests/functions/doc_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


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
        """Test (doc 'doc) returns documentation for doc function itself."""
        result = run_lispy_string("(doc 'doc)", self.env)
        self.assertIsInstance(result, str)
        self.assertIn("Function: doc", result)
        self.assertIn("(doc 'symbol-name)", result)

    def test_doc_with_special_form(self):
        """Test (doc 'and) returns documentation for and special form."""
        result = run_lispy_string("(doc 'and)", self.env)
        self.assertIsInstance(result, str)
        self.assertIn("Special Form: and", result)
        self.assertIn("(and expr1 expr2 ...)", result)
        self.assertIn("short-circuiting", result)

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

    def test_doc_with_quoted_function(self):
        """Test (doc '+) works with quoted function names."""
        result = run_lispy_string("(doc '+)", self.env)
        self.assertIsInstance(result, str)
        self.assertIn("Function: +", result)
        self.assertIn("(+ number1 number2 ...)", result)

    def test_doc_consistency_both_forms_work(self):
        """Test that both (doc +) and (doc '+) work for functions."""
        # Test unquoted form
        result_unquoted = run_lispy_string("(doc abs)", self.env)
        # Test quoted form
        result_quoted = run_lispy_string("(doc 'abs)", self.env)

        # Both should return the same documentation
        self.assertEqual(result_unquoted, result_quoted)
        self.assertIn("Function: abs", result_unquoted)


if __name__ == "__main__":
    unittest.main()
