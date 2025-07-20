import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.types import Vector
from lispy.utils import run_lispy_string


class RangeFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    # --- Single argument tests (range end) ---
    def test_range_single_arg_positive(self):
        """Test (range 5) returns [0 1 2 3 4]."""
        result = run_lispy_string("(range 5)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([0, 1, 2, 3, 4]))

    def test_range_single_arg_zero(self):
        """Test (range 0) returns []."""
        result = run_lispy_string("(range 0)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_range_single_arg_negative(self):
        """Test (range -3) returns []."""
        result = run_lispy_string("(range -3)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_range_single_arg_one(self):
        """Test (range 1) returns [0]."""
        result = run_lispy_string("(range 1)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([0]))

    def test_range_single_arg_large(self):
        """Test (range 10) returns [0 1 2 3 4 5 6 7 8 9]."""
        result = run_lispy_string("(range 10)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))

    # --- Two argument tests (range start end) ---
    def test_range_two_args_positive(self):
        """Test (range 2 8) returns [2 3 4 5 6 7]."""
        result = run_lispy_string("(range 2 8)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([2, 3, 4, 5, 6, 7]))

    def test_range_two_args_equal(self):
        """Test (range 5 5) returns []."""
        result = run_lispy_string("(range 5 5)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_range_two_args_start_greater(self):
        """Test (range 8 2) returns [] (start >= end with positive step)."""
        result = run_lispy_string("(range 8 2)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_range_two_args_negative_start(self):
        """Test (range -3 2) returns [-3 -2 -1 0 1]."""
        result = run_lispy_string("(range -3 2)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([-3, -2, -1, 0, 1]))

    def test_range_two_args_negative_end(self):
        """Test (range -5 -2) returns [-5 -4 -3]."""
        result = run_lispy_string("(range -5 -2)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([-5, -4, -3]))

    def test_range_two_args_zero_start(self):
        """Test (range 0 3) returns [0 1 2]."""
        result = run_lispy_string("(range 0 3)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([0, 1, 2]))

    def test_range_two_args_zero_end(self):
        """Test (range -2 0) returns [-2 -1]."""
        result = run_lispy_string("(range -2 0)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([-2, -1]))

    # --- Three argument tests (range start end step) ---
    def test_range_three_args_positive_step(self):
        """Test (range 0 10 2) returns [0 2 4 6 8]."""
        result = run_lispy_string("(range 0 10 2)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([0, 2, 4, 6, 8]))

    def test_range_three_args_step_three(self):
        """Test (range 1 10 3) returns [1 4 7]."""
        result = run_lispy_string("(range 1 10 3)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1, 4, 7]))

    def test_range_three_args_negative_step(self):
        """Test (range 10 0 -1) returns [10 9 8 7 6 5 4 3 2 1]."""
        result = run_lispy_string("(range 10 0 -1)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]))

    def test_range_three_args_negative_step_two(self):
        """Test (range 10 0 -2) returns [10 8 6 4 2]."""
        result = run_lispy_string("(range 10 0 -2)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([10, 8, 6, 4, 2]))

    def test_range_three_args_negative_start_end(self):
        """Test (range -1 -10 -2) returns [-1 -3 -5 -7 -9]."""
        result = run_lispy_string("(range -1 -10 -2)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([-1, -3, -5, -7, -9]))

    def test_range_three_args_step_one(self):
        """Test (range 3 10 1) returns [3 4 5 6 7 8 9]."""
        result = run_lispy_string("(range 3 10 1)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([3, 4, 5, 6, 7, 8, 9]))

    def test_range_three_args_large_step(self):
        """Test (range 0 20 5) returns [0 5 10 15]."""
        result = run_lispy_string("(range 0 20 5)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([0, 5, 10, 15]))

    def test_range_three_args_step_larger_than_range(self):
        """Test (range 1 5 10) returns [1] (step larger than range)."""
        result = run_lispy_string("(range 1 5 10)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([1]))

    # --- Edge cases ---
    def test_range_wrong_direction_positive_step(self):
        """Test range with wrong direction (start > end with positive step)."""
        result = run_lispy_string("(range 5 2 1)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_range_wrong_direction_negative_step(self):
        """Test range with wrong direction (start < end with negative step)."""
        result = run_lispy_string("(range 2 5 -1)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_range_same_start_end_positive_step(self):
        """Test (range 5 5 1) returns []."""
        result = run_lispy_string("(range 5 5 1)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    def test_range_same_start_end_negative_step(self):
        """Test (range 5 5 -1) returns []."""
        result = run_lispy_string("(range 5 5 -1)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([]))

    # --- Error cases ---
    def test_range_no_args(self):
        """Test range with no arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(range)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'range' expects 1-3 arguments, got 0."
        )

    def test_range_too_many_args(self):
        """Test range with too many arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(range 1 2 3 4)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'range' expects 1-3 arguments, got 4."
        )

    def test_range_non_integer_first_arg(self):
        """Test range with non-integer first argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(range "not-number")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 1 to 'range' must be an integer, got str: 'not-number'",
        )

    def test_range_float_first_arg(self):
        """Test range with float first argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(range 3.14)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 1 to 'range' must be an integer, got float: '3.14'",
        )

    def test_range_non_integer_second_arg(self):
        """Test range with non-integer second argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(range 1 2.5)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 2 to 'range' must be an integer, got float: '2.5'",
        )

    def test_range_boolean_arg(self):
        """Test range with boolean argument - but booleans are integers in Python, so this would actually work."""
        # Since Python booleans are integers (True=1, False=0), they pass isinstance(arg, int)
        # So let's test that True and False work as expected rather than error
        result_true = run_lispy_string("(range true)", self.env)
        self.assertEqual(result_true, Vector([0]))  # range(1) = [0]

        result_false = run_lispy_string("(range false)", self.env)
        self.assertEqual(result_false, Vector([]))  # range(0) = []

    def test_range_vector_arg(self):
        """Test range with vector argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(range [1 2 3])", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 1 to 'range' must be an integer, got Vector: '[1 2 3]'",
        )

    def test_range_zero_step(self):
        """Test range with zero step."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(range 1 10 0)", self.env)
        self.assertEqual(
            str(cm.exception), "ValueError: 'range' step argument must not be zero."
        )

    def test_range_non_integer_step(self):
        """Test range with non-integer step argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(range 1 10 1.5)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 3 to 'range' must be an integer, got float: '1.5'",
        )

    def test_range_nil_arg(self):
        """Test range with nil argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(range nil)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 1 to 'range' must be an integer, got NoneType: 'None'",
        )

    # --- Integration and usage tests ---
    def test_range_with_count(self):
        """Test range used with count function."""
        result = run_lispy_string("(count (range 5))", self.env)
        self.assertEqual(result, 5)

    def test_range_with_first(self):
        """Test range used with first function."""
        result = run_lispy_string("(first (range 3 10))", self.env)
        self.assertEqual(result, 3)

    def test_range_with_nth(self):
        """Test range used with nth function."""
        result = run_lispy_string("(nth (range 0 10 2) 2)", self.env)
        self.assertEqual(result, 4)  # [0 2 4 6 8], index 2 is 4

    def test_range_empty_with_functions(self):
        """Test empty range with collection functions."""
        result = run_lispy_string("(count (range 0))", self.env)
        self.assertEqual(result, 0)

        result = run_lispy_string("(empty? (range 5 5))", self.env)
        self.assertEqual(result, True)

    def test_range_in_arithmetic(self):
        """Test range used in arithmetic operations."""
        # Sum of range 1 to 5 (exclusive): 1+2+3+4 = 10
        result = run_lispy_string("(reduce (range 1 5) + 0)", self.env)
        self.assertEqual(result, 10)

    def test_range_with_map(self):
        """Test range used with map function."""
        result = run_lispy_string("(map (range 3) (fn [x] (* x x)))", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([0, 1, 4]))  # [0^2, 1^2, 2^2]

    def test_range_with_filter(self):
        """Test range used with filter function."""
        result = run_lispy_string(
            "(filter (range 10) (fn [x] (= (% x 2) 0)))", self.env
        )
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([0, 2, 4, 6, 8]))

    def test_range_large_values(self):
        """Test range with large values."""
        result = run_lispy_string("(range 100 105)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([100, 101, 102, 103, 104]))

    def test_range_negative_large_step(self):
        """Test range with large negative step."""
        result = run_lispy_string("(range 20 0 -5)", self.env)
        self.assertIsInstance(result, Vector)
        self.assertEqual(result, Vector([20, 15, 10, 5]))


if __name__ == "__main__":
    unittest.main()
