import unittest
from lispy.types import LispyList, Symbol
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class KeysFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_keys_on_map(self):
        """Test (keys {:a 1 :b 2}) returns a list of keys, e.g., (:a :b) or (:b :a)."""
        run_lispy_string("(define my-map {:a 1 :b 2 :c 3})", self.env)
        lispy_code = "(keys my-map)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertIsInstance(result, LispyList)
        self.assertCountEqual(result, [Symbol(":a"), Symbol(":b"), Symbol(":c")])

    def test_keys_on_empty_map(self):
        """Test (keys {}) returns an empty list '()."""
        lispy_code = "(keys {})"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([]))

    def test_keys_on_nil_map(self):
        """Test (keys nil) returns an empty list '()."""
        lispy_code = "(keys nil)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([]))

    # Error handling tests
    def test_keys_no_args(self):
        """Test (keys) raises SyntaxError."""
        lispy_code = "(keys)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'keys' expects 1 argument (a map), got 0."
        )

    def test_keys_too_many_args(self):
        """Test (keys {} {}) raises SyntaxError."""
        lispy_code = "(keys {} {})"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'keys' expects 1 argument (a map), got 2."
        )

    def test_keys_wrong_arg_type(self):
        """Test (keys '(1 2)) raises TypeError."""
        lispy_code = "(keys '(1 2))"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'keys' expects a map or nil, got <class 'lispy.types.LispyList'>.",
        )


if __name__ == "__main__":
    unittest.main()
