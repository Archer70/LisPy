import sys
import unittest
from io import StringIO

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class PrintFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        # Capture stdout for testing
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held

    def test_print_single_string(self):
        result = run_lispy_string('(print "Hello")', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "Hello")
        self.assertIsNone(result)

    def test_print_multiple_strings(self):
        result = run_lispy_string('(print "Hello" "World")', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "Hello World")
        self.assertIsNone(result)

    # def test_print_numbers(self):
    #     result = run_lispy_string('(print 42 3.14)', self.env)
    #     output = sys.stdout.getvalue()
    #     self.assertEqual(output, "42 3.14")
    #     self.assertIsNone(result)

    def test_print_mixed_types(self):
        result = run_lispy_string('(print "Number:" 42 "Boolean:" true)', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "Number: 42 Boolean: true")
        self.assertIsNone(result)

    def test_print_booleans(self):
        result = run_lispy_string("(print true false)", self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "true false")
        self.assertIsNone(result)

    def test_print_nil(self):
        result = run_lispy_string("(print nil)", self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "nil")
        self.assertIsNone(result)

    def test_print_vector(self):
        result = run_lispy_string("(print [1 2 3])", self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "[1 2 3]")
        self.assertIsNone(result)

    def test_print_hash_map(self):
        result = run_lispy_string('(print {:name "Alice" :age 30})', self.env)
        output = sys.stdout.getvalue()
        # Hash map output may vary in order, so just check it contains expected parts
        self.assertIn("name", output)
        self.assertIn("Alice", output)
        self.assertIn("age", output)
        self.assertIn("30", output)
        self.assertIsNone(result)

    def test_print_no_arguments(self):
        result = run_lispy_string("(print)", self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "")
        self.assertIsNone(result)

    def test_print_no_newline(self):
        # Test that print doesn't add a newline
        run_lispy_string('(print "Hello")', self.env)
        run_lispy_string('(print "World")', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "HelloWorld")


if __name__ == "__main__":
    unittest.main()
