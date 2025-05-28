import unittest
import sys
from io import StringIO

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string

class PrintlnFunctionTest(unittest.TestCase):

    def setUp(self):
        self.env = create_global_env()
        # Capture stdout for testing
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held

    def test_println_single_string(self):
        result = run_lispy_string('(println "Hello")', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "Hello\n")
        self.assertIsNone(result)

    def test_println_multiple_strings(self):
        result = run_lispy_string('(println "Hello" "World")', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "Hello World\n")
        self.assertIsNone(result)

    def test_println_numbers(self):
        result = run_lispy_string('(println 42 3.14)', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "42 3.14\n")
        self.assertIsNone(result)

    def test_println_mixed_types(self):
        result = run_lispy_string('(println "Number:" 42 "Boolean:" true)', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "Number: 42 Boolean: true\n")
        self.assertIsNone(result)

    def test_println_booleans(self):
        result = run_lispy_string('(println true false)', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "true false\n")
        self.assertIsNone(result)

    def test_println_nil(self):
        result = run_lispy_string('(println nil)', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "nil\n")
        self.assertIsNone(result)

    def test_println_vector(self):
        result = run_lispy_string('(println [1 2 3])', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "[1 2 3]\n")
        self.assertIsNone(result)

    def test_println_hash_map(self):
        result = run_lispy_string('(println {:name "Alice" :age 30})', self.env)
        output = sys.stdout.getvalue()
        # Hash map output may vary in order, so just check it contains expected parts
        self.assertIn("name", output)
        self.assertIn("Alice", output)
        self.assertIn("age", output)
        self.assertIn("30", output)
        self.assertTrue(output.endswith("\n"))
        self.assertIsNone(result)

    def test_println_no_arguments(self):
        result = run_lispy_string('(println)', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "\n")
        self.assertIsNone(result)

    def test_println_with_newline(self):
        # Test that println adds a newline
        run_lispy_string('(println "Hello")', self.env)
        run_lispy_string('(println "World")', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "Hello\nWorld\n")

    def test_println_empty_string(self):
        result = run_lispy_string('(println "")', self.env)
        output = sys.stdout.getvalue()
        self.assertEqual(output, "\n")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main() 