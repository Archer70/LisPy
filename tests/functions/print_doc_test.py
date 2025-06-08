# tests/functions/print_doc_test.py
import unittest
from io import StringIO
import sys

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class PrintDocFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        # Capture stdout for testing print output
        self.captured_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.captured_output

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.original_stdout

    def test_print_doc_with_string(self):
        """Test (print-doc \"hello\") prints hello."""
        result = run_lispy_string('(print-doc "Hello, World!")', self.env)
        self.assertIsNone(result)  # print-doc returns nil
        output = self.captured_output.getvalue()
        self.assertEqual(output.strip(), "Hello, World!")

    def test_print_doc_with_doc_result(self):
        """Test (print-doc (doc +)) prints documentation."""
        result = run_lispy_string("(print-doc (doc +))", self.env)
        self.assertIsNone(result)  # print-doc returns nil
        output = self.captured_output.getvalue()
        self.assertIn("Function: +", output)
        self.assertIn("Arguments:", output)
        self.assertIn("Examples:", output)

    def test_print_doc_with_abs_documentation(self):
        """Test (print-doc (doc abs)) prints abs documentation."""
        result = run_lispy_string("(print-doc (doc abs))", self.env)
        self.assertIsNone(result)  # print-doc returns nil
        output = self.captured_output.getvalue()
        self.assertIn("Function: abs", output)
        self.assertIn("absolute value", output)

    def test_print_doc_no_args(self):
        """Test (print-doc) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(print-doc)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'print-doc' expects 1 argument, got 0.")

    def test_print_doc_too_many_args(self):
        """Test (print-doc \"a\" \"b\") raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(print-doc "a" "b")', self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'print-doc' expects 1 argument, got 2.")

    def test_print_doc_with_non_string(self):
        """Test (print-doc 42) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(print-doc 42)", self.env)
        self.assertIn("Error in 'print-doc'", str(cm.exception))
        self.assertIn("Unable to find documentation", str(cm.exception))

    def test_print_doc_with_nil(self):
        """Test (print-doc nil) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(print-doc nil)", self.env)
        self.assertIn("Error in 'print-doc'", str(cm.exception))
        self.assertIn("Unable to find documentation", str(cm.exception))

    def test_print_doc_with_function_directly(self):
        """Test (print-doc +) prints documentation directly."""
        result = run_lispy_string("(print-doc +)", self.env)
        self.assertIsNone(result)  # print-doc returns nil
        output = self.captured_output.getvalue()
        self.assertIn("Function: +", output)
        self.assertIn("Arguments:", output)
        self.assertIn("Examples:", output)

    def test_print_doc_with_abs_function_directly(self):
        """Test (print-doc abs) prints abs documentation directly."""
        result = run_lispy_string("(print-doc abs)", self.env)
        self.assertIsNone(result)  # print-doc returns nil
        output = self.captured_output.getvalue()
        self.assertIn("Function: abs", output)
        self.assertIn("absolute value", output)

    def test_print_doc_with_undocumented_function_directly(self):
        """Test (print-doc my-test-fn) with undocumented user-defined function."""
        # Define a user function that won't have documentation
        run_lispy_string("(define my-test-fn (fn [x] (+ x 1)))", self.env)
        result = run_lispy_string("(print-doc my-test-fn)", self.env)
        self.assertIsNone(result)  # print-doc returns nil
        output = self.captured_output.getvalue()
        self.assertIn("No documentation available", output)

    def test_print_doc_convenience_vs_chained(self):
        """Test that (print-doc +) produces same output as (print-doc (doc +))."""
        # Capture output from direct function call
        result1 = run_lispy_string("(print-doc +)", self.env)
        direct_output = self.captured_output.getvalue()
        
        # Reset captured output
        self.captured_output.truncate(0)
        self.captured_output.seek(0)
        
        # Capture output from chained call
        result2 = run_lispy_string("(print-doc (doc +))", self.env)
        chained_output = self.captured_output.getvalue()
        
        # Both should return nil
        self.assertIsNone(result1)
        self.assertIsNone(result2)
        
        # Both should produce identical output
        self.assertEqual(direct_output, chained_output)


if __name__ == '__main__':
    unittest.main() 