import unittest

from lispy.types import Symbol
from lispy.functions import create_global_env
from lispy.lexer import tokenize
from lispy.parser import parse
from lispy.evaluator import evaluate
from lispy.exceptions import EvaluationError


class HashMapFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_hash_map_fn_empty(self):
        """Test (hash-map) creates an empty map."""
        lispy_code = "(hash-map)"
        ast = parse(tokenize(lispy_code))
        result = evaluate(ast, self.env)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, {})

    def test_hash_map_fn_simple(self):
        """Test (hash-map ':a 1 ':b 2) creates a map."""
        lispy_code = "(hash-map ':a 1 ':b 2)"
        ast = parse(tokenize(lispy_code))
        result = evaluate(ast, self.env)
        self.assertIsInstance(result, dict)
        expected_map = {Symbol(":a"): 1, Symbol(":b"): 2}
        self.assertEqual(result, expected_map)

    def test_hash_map_fn_mixed_value_types(self):
        """Test (hash-map ':name "LisPy" ':version 0.1 ':active true)"""
        lispy_code = "(hash-map ':name \"LisPy\" ':version 0.1 ':active true)"
        ast = parse(tokenize(lispy_code))
        result = evaluate(ast, self.env)
        self.assertIsInstance(result, dict)
        expected_map = {
            Symbol(":name"): "LisPy",
            Symbol(":version"): 0.1,
            Symbol(":active"): True
        }
        self.assertEqual(result, expected_map)

    def test_hash_map_fn_evaluates_arguments(self):
        """Test that keys and values to (hash-map ...) are evaluated."""
        evaluate(parse(tokenize("(define key-a ':key_a)")), self.env)
        evaluate(parse(tokenize("(define val-b 200)")), self.env)
        lispy_code = "(hash-map key-a (+ 10 20) ':key_b val-b)"
        ast = parse(tokenize(lispy_code))
        result = evaluate(ast, self.env)
        self.assertIsInstance(result, dict)
        expected_map = {
            Symbol(":key_a"): 30,
            Symbol(":key_b"): 200
        }
        self.assertEqual(result, expected_map)

    def test_hash_map_fn_odd_number_of_args(self):
        """Test (hash-map ':a 1 ':b) raises an error for odd number of args."""
        lispy_code = "(hash-map ':a 1 ':b)"
        with self.assertRaises(EvaluationError) as cm:
            evaluate(parse(tokenize(lispy_code)), self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'hash-map' requires an even number of arguments (key-value pairs), got 3.")

    def test_hash_map_fn_non_symbol_key(self):
        """Test (hash-map \"key\" 1) raises an error for non-symbol key."""
        lispy_code = '(hash-map "key" 1)'
        # Error caught by hash-map: evaluated args must have symbol keys.
        with self.assertRaises(EvaluationError) as cm:
            evaluate(parse(tokenize(lispy_code)), self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'hash-map' keys must be symbols, got <class 'str'>.")

    def test_hash_map_fn_non_symbol_evaluated_key(self):
        """Test hash-map with an evaluated key that is not a symbol."""
        evaluate(parse(tokenize("(define mykey 123)")), self.env)
        lispy_code = '(hash-map mykey "value")'
        with self.assertRaises(EvaluationError) as cm:
            evaluate(parse(tokenize(lispy_code)), self.env)
        self.assertEqual(str(cm.exception), "TypeError: 'hash-map' keys must be symbols, got <class 'int'>.")


if __name__ == '__main__':
    unittest.main() 