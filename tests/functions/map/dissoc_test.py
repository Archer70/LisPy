import unittest

from lispy.types import Symbol
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class DissocFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        # self.map_abc = {Symbol(":a"): 1, Symbol(":b"): 2, Symbol(":c"): 3} # Defined in tests using Lispy syntax

    def test_dissoc_from_existing_map_one_key(self):
        """Test (dissoc {:a 1 :b 2} :b) returns {:a 1}."""
        run_lispy_string("(define my-map {:a 1 :b 2})", self.env)
        lispy_code = "(dissoc my-map ':b)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, {Symbol(":a"): 1})

    def test_dissoc_from_existing_map_multiple_keys(self):
        """Test (dissoc {:a 1 :b 2 :c 3} :b :c) returns {:a 1}."""
        run_lispy_string("(define my-map {:a 1 :b 2 :c 3})", self.env)
        lispy_code = "(dissoc my-map ':b ':c)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, {Symbol(":a"): 1})

    def test_dissoc_non_existent_key(self):
        """Test (dissoc {:a 1} :c) returns {:a 1}."""
        run_lispy_string("(define my-map {:a 1})", self.env)
        lispy_code = "(dissoc my-map ':c)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, {Symbol(":a"): 1})

    def test_dissoc_from_empty_map(self):
        """Test (dissoc {} :a) returns {}."""
        lispy_code = "(dissoc {} ':a)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, {})

    def test_dissoc_original_map_unchanged(self):
        """Test dissoc does not modify the original map."""
        run_lispy_string("(define orig-map {:a 1 :b 2})", self.env)
        run_lispy_string("(dissoc orig-map ':b)", self.env)
        original_map_val = run_lispy_string("orig-map", self.env)
        self.assertEqual(original_map_val, {Symbol(":a"): 1, Symbol(":b"): 2})

    def test_dissoc_with_nil_map(self):
        """Test (dissoc nil :a) returns nil."""
        lispy_code = "(dissoc nil ':a)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsNone(result)

    def test_dissoc_no_keys_specified(self):
        """Test (dissoc {:a 1}) returns {:a 1} (no keys to dissoc)."""
        run_lispy_string("(define my-map {:a 1})", self.env)
        lispy_code = "(dissoc my-map)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, {Symbol(":a"): 1})

    def test_dissoc_evaluated_symbol_keys(self):
        """Test dissoc works with keys that are evaluated symbols."""
        run_lispy_string("(define my-map {:a 1 :b 2 :c 3})", self.env)
        run_lispy_string("(define key-to-remove ':b)", self.env)
        lispy_code = "(dissoc my-map key-to-remove ':c)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, {Symbol(":a"): 1})

    # Error handling tests
    def test_dissoc_no_args(self):
        """Test (dissoc) raises SyntaxError."""
        lispy_code = "(dissoc)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'dissoc' expects at least 1 argument (map), got 0.",
        )

    def test_dissoc_map_arg_not_map_or_nil(self):
        """Test (dissoc '(1 2) :a) raises TypeError."""
        lispy_code = "(dissoc '(1 2) ':a)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: First argument to 'dissoc' must be a map or nil, got <class 'lispy.types.LispyList'>.",
        )

    def test_dissoc_key_not_symbol(self):
        """Test (dissoc {:a 1} 1) raises TypeError (key must be a symbol)."""
        lispy_code = "(dissoc {:a 1} 1)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Keys to 'dissoc' must be symbols, got <class 'int'>.",
        )


if __name__ == "__main__":
    unittest.main()
