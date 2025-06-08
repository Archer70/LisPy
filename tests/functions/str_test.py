import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.types import LispyList, Vector, Symbol


class StrFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_str_integer(self):
        """Test (str 42) returns "42"."""
        result = run_lispy_string("(str 42)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "42")

    def test_str_negative_integer(self):
        """Test (str -123) returns "-123"."""
        result = run_lispy_string("(str -123)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "-123")

    def test_str_float(self):
        """Test (str 3.14) returns "3.14"."""
        result = run_lispy_string("(str 3.14)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "3.14")

    def test_str_negative_float(self):
        """Test (str -2.5) returns "-2.5"."""
        result = run_lispy_string("(str -2.5)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "-2.5")

    def test_str_true(self):
        """Test (str true) returns "true"."""
        result = run_lispy_string("(str true)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "true")

    def test_str_false(self):
        """Test (str false) returns "false"."""
        result = run_lispy_string("(str false)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "false")

    def test_str_nil(self):
        """Test (str nil) returns "nil"."""
        result = run_lispy_string("(str nil)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "nil")

    def test_str_string_passthrough(self):
        """Test (str "hello") returns "hello" unchanged."""
        result = run_lispy_string('(str "hello")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "hello")

    def test_str_empty_string(self):
        """Test (str "") returns "" unchanged."""
        result = run_lispy_string('(str "")', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

    def test_str_symbol(self):
        """Test (str 'symbol) returns "symbol"."""
        result = run_lispy_string("(str 'symbol)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "symbol")

    def test_str_keyword_symbol(self):
        """Test (str ':keyword) returns ":keyword"."""
        result = run_lispy_string("(str ':keyword)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, ":keyword")

    def test_str_vector(self):
        """Test (str [1 2 3]) returns vector representation."""
        result = run_lispy_string("(str [1 2 3])", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "[1 2 3]")

    def test_str_empty_vector(self):
        """Test (str []) returns "[]"."""
        result = run_lispy_string("(str [])", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "[]")

    def test_str_list(self):
        """Test (str '(1 2 3)) returns list representation."""
        result = run_lispy_string("(str '(1 2 3))", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "(1 2 3)")

    def test_str_empty_list(self):
        """Test (str '()) returns "()"."""
        result = run_lispy_string("(str '())", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "()")

    def test_str_mixed_vector(self):
        """Test str with vector containing mixed types."""
        result = run_lispy_string('(str [1 "hello" true])', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "[1 'hello' True]")

    def test_str_hash_map(self):
        """Test str with hash map."""
        result = run_lispy_string("(str (hash-map ':a 1 ':b 2))", self.env)
        self.assertIsInstance(result, str)
        # Hash map order might vary, so check it contains the expected parts
        self.assertIn(":a", result)
        self.assertIn("1", result)
        self.assertIn(":b", result)
        self.assertIn("2", result)
        self.assertTrue(result.startswith("{"))
        self.assertTrue(result.endswith("}"))

    def test_str_with_variables(self):
        """Test str with variables."""
        run_lispy_string("(define x 42)", self.env)
        run_lispy_string("(define y 'hello)", self.env)
        
        result_x = run_lispy_string("(str x)", self.env)
        result_y = run_lispy_string("(str y)", self.env)
        
        self.assertEqual(result_x, "42")
        self.assertEqual(result_y, "hello")

    def test_str_zero(self):
        """Test (str 0) returns "0"."""
        result = run_lispy_string("(str 0)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "0")

    def test_str_large_number(self):
        """Test str with large numbers."""
        result = run_lispy_string("(str 123456789)", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "123456789")

    # --- Error Handling Tests ---
    def test_str_too_few_args(self):
        """Test str with too few arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(str)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'str' expects 1 argument, got 0.")

    def test_str_too_many_args(self):
        """Test str with too many arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(str 42 43)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'str' expects 1 argument, got 2.")

    # --- Integration Tests ---
    def test_str_with_append(self):
        """Test using str with append for mixed type concatenation."""
        result = run_lispy_string('(append "Number: " (str 42))', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Number: 42")

    def test_str_with_append_multiple_types(self):
        """Test complex string building with str and append."""
        result = run_lispy_string('(append "Value: " (str 3.14) ", Active: " (str true))', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Value: 3.14, Active: true")

    def test_str_with_thread_first(self):
        """Test str used with the -> (thread-first) special form."""
        result = run_lispy_string("(-> 42 (str) (append \" items\"))", self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "42 items")

    def test_str_complex_thread_first(self):
        """Test complex thread-first with str and append."""
        result = run_lispy_string('(-> [1 2 3] (str) (append " is a vector"))', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "[1 2 3] is a vector")

    def test_str_chaining_conversions(self):
        """Test chaining str conversions in thread-first."""
        result = run_lispy_string('(-> true (str) (append " and ") (append (str 42)))', self.env)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "true and 42")


if __name__ == '__main__':
    unittest.main() 