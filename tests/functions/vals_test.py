import unittest

from lispy.types import LispyList
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class ValsFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_vals_on_map(self):
        """Test (vals {:a 1 :b 2 :c 3}) returns a list of values, e.g., (1 2 3) in some order."""
        run_lispy_string("(define my-map {:a 1 :b 2 :c 3})", self.env)
        lispy_code = "(vals my-map)"
        result = run_lispy_string(lispy_code, self.env)

        self.assertIsInstance(result, LispyList)
        self.assertEqual(len(result), 3)
        # Convert to set for order-independent comparison of elements if values are simple and hashable
        # If values can be complex (e.g., lists, other maps), use a Counter or sort if order is defined.
        expected_values = {1, 2, 3}
        # To handle potential unhashable types in result if values could be lists/maps:
        # self.assertEqual(sorted(map(repr, result)), sorted(map(repr, list(expected_values))))
        self.assertEqual(set(result), expected_values)

    def test_vals_on_empty_map(self):
        """Test (vals {}) returns an empty list '()."""
        lispy_code = "(vals {})"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([]))

    def test_vals_on_nil_map(self):
        """Test (vals nil) returns an empty list '()."""
        lispy_code = "(vals nil)"
        result = run_lispy_string(lispy_code, self.env)
        self.assertEqual(result, LispyList([]))

    # Error handling tests
    def test_vals_wrong_arg_type(self):
        """Test (vals '(1 2)) raises TypeError."""
        lispy_code = "(vals '(1 2))"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'vals' expects a map or nil, got <class 'lispy.types.LispyList'>.",
        )

    def test_vals_too_many_args(self):
        """Test (vals {} {}) raises SyntaxError."""
        lispy_code = "(vals {} {})"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'vals' expects 1 argument (a map), got 2."
        )

    def test_vals_no_args(self):
        """Test (vals) raises SyntaxError."""
        lispy_code = "(vals)"
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(lispy_code, self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'vals' expects 1 argument (a map), got 0."
        )


if __name__ == "__main__":
    unittest.main()
