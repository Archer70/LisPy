import unittest

from lispy.types import Symbol
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class AssocFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        # self.empty_map = {} # Not used directly, can be removed or kept if planning future use
        # self.map1 = {Symbol("a"): 1, Symbol("b"): 2} # Not used directly

    def test_assoc_empty_map_one_pair(self):
        """Test (assoc {} :c 3) returns {:c 3}."""
        lispy_code = "(assoc {} ':c 3)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, {Symbol(":c"): 3})

    def test_assoc_existing_map_new_key(self):
        """Test (assoc {:a 1 :b 2} :c 3) returns {:a 1 :b 2 :c 3}."""
        run_lispy_string("(define my-map {:a 1 :b 2})", self.env)
        lispy_code = "(assoc my-map ':c 3)"
        result = run_lispy_string(lispy_code, self.env)
        expected = {Symbol(":a"): 1, Symbol(":b"): 2, Symbol(":c"): 3}
        self.assertEqual(result, expected)

    def test_assoc_existing_map_update_key(self):
        """Test (assoc {:a 1 :b 2} :b 20) returns {:a 1 :b 20}."""
        run_lispy_string("(define my-map {:a 1 :b 2})", self.env)
        lispy_code = "(assoc my-map ':b 20)"
        result = run_lispy_string(lispy_code, self.env)
        expected = {Symbol(":a"): 1, Symbol(":b"): 20}
        self.assertEqual(result, expected)

    def test_assoc_multiple_pairs(self):
        """Test (assoc {} :x 10 :y 20) returns {:x 10 :y 20}."""
        lispy_code = "(assoc {} ':x 10 ':y 20)"
        result = run_lispy_string(lispy_code, self.env)
        expected = {Symbol(":x"): 10, Symbol(":y"): 20}
        self.assertEqual(result, expected)

    def test_assoc_multiple_pairs_update_and_add(self):
        """Test (assoc {:a 1} :a 10 :b 20) returns {:a 10 :b 20}."""
        run_lispy_string("(define my-map {:a 1})", self.env)
        lispy_code = "(assoc my-map ':a 10 ':b 20)"
        result = run_lispy_string(lispy_code, self.env)
        expected = {Symbol(":a"): 10, Symbol(":b"): 20}
        self.assertEqual(result, expected)

    def test_assoc_original_map_unchanged(self):
        """Test assoc does not modify the original map."""
        run_lispy_string("(define orig-map {:a 1})", self.env)
        run_lispy_string("(assoc orig-map ':b 2)", self.env)
        original_map_val = run_lispy_string("orig-map", self.env)
        self.assertEqual(original_map_val, {Symbol(":a"): 1})

    def test_assoc_with_nil_map(self):
        """Test (assoc nil :a 1) returns {:a 1}."""
        lispy_code = "(assoc nil ':a 1)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, {Symbol(":a"): 1})

    def test_assoc_keys_are_symbols(self):
        """Test keys are stored as Symbols if they are parsed as symbols."""
        run_lispy_string("(define mykey ':some-val)", self.env)
        lispy_code = "(assoc {} ':mykey 100 mykey 200)"
        result = run_lispy_string(lispy_code, self.env)
        expected = {Symbol(":mykey"): 100, Symbol(":some-val"): 200}
        self.assertEqual(result, expected)
        self.assertIsInstance(list(result.keys())[0], Symbol)
        self.assertIsInstance(list(result.keys())[1], Symbol)

    # Error handling tests
    def test_assoc_no_pairs(self):
        """Test (assoc {}) raises SyntaxError."""
        lispy_code = "(assoc {})"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'assoc' expects at least 3 arguments (map, key, value), got 1.",
        )

    def test_assoc_odd_number_of_key_value_args(self):
        """Test (assoc {} :a) raises SyntaxError due to insufficient arguments."""
        lispy_code = "(assoc {} ':a)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'assoc' expects at least 3 arguments (map, key, value), got 2.",
        )

    def test_assoc_map_arg_not_map_or_nil(self):
        """Test (assoc '(1 2) :a 1) raises TypeError."""
        lispy_code = "(assoc '(1 2) ':a 1)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: First argument to 'assoc' must be a map or nil, got <class 'lispy.types.LispyList'>.",
        )

    def test_assoc_key_not_symbol(self):
        """Test (assoc {} 1 2) raises TypeError (key must be a symbol)."""
        lispy_code = "(assoc {} 1 2)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Map keys in 'assoc' must be symbols, got <class 'int'>.",
        )


if __name__ == "__main__":
    unittest.main()
