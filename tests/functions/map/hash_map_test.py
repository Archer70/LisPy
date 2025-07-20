import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.types import Symbol
from lispy.utils import run_lispy_string


class HashMapFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_hash_map_fn_empty(self):
        """Test (hash-map) creates an empty map."""
        lispy_code = "(hash-map)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, {})

    def test_hash_map_fn_simple(self):
        """Test (hash-map ':a 1 ':b 2) creates a map."""
        lispy_code = "(hash-map ':a 1 ':b 2)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, dict)
        expected_map = {Symbol(":a"): 1, Symbol(":b"): 2}
        self.assertEqual(result, expected_map)

    def test_hash_map_fn_mixed_value_types(self):
        """Test (hash-map ':name "LisPy" ':version 0.1 ':active true)"""
        lispy_code = "(hash-map ':name \"LisPy\" ':version 0.1 ':active true)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, dict)
        expected_map = {
            Symbol(":name"): "LisPy",
            Symbol(":version"): 0.1,
            Symbol(":active"): True,
        }
        self.assertEqual(result, expected_map)

    def test_hash_map_fn_evaluates_arguments(self):
        """Test that keys and values to (hash-map ...) are evaluated."""
        run_lispy_string("(define key-a ':key_a)", self.env)
        run_lispy_string("(define val-b 200)", self.env)
        lispy_code = "(hash-map key-a (+ 10 20) ':key_b val-b)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, dict)
        expected_map = {Symbol(":key_a"): 30, Symbol(":key_b"): 200}
        self.assertEqual(result, expected_map)

    def test_hash_map_fn_odd_number_of_args(self):
        """Test (hash-map ':a 1 ':b) raises an error for odd number of args."""
        lispy_code = "(hash-map ':a 1 ':b)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'hash-map' requires an even number of arguments (key-value pairs), got 3.",
        )

    def test_hash_map_fn_string_key(self):
        """Test (hash-map \"key\" 1) works with string keys."""
        lispy_code = '(hash-map "key" 1)'
        result = run_lispy_string(lispy_code, self.env)
        expected = {"key": 1}
        self.assertEqual(result, expected)

    def test_hash_map_fn_evaluated_numeric_key(self):
        """Test hash-map with an evaluated key that is a number."""
        run_lispy_string("(define mykey 123)", self.env)
        lispy_code = '(hash-map mykey "value")'
        result = run_lispy_string(lispy_code, self.env)
        expected = {123: "value"}
        self.assertEqual(result, expected)

    def test_hash_map_fn_invalid_key_type(self):
        """Test hash-map with unsupported key type raises error."""
        # Test with a list as key (not supported)
        lispy_code = '(hash-map (list 1 2) "value")'
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertIn("TypeError", str(cm.exception))
        self.assertIn("'hash-map' keys must be", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
