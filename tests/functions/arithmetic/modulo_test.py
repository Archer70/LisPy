import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class ModuloTest(unittest.TestCase):
    """Test the modulo (%) function."""

    def setUp(self):
        """Set up a global environment for the tests."""
        self.env = create_global_env()

    def test_basic_modulo(self):
        """Test basic modulo operations."""
        # Basic positive numbers
        self.assertEqual(run_lispy_string("(% 10 3)", self.env), 1)
        self.assertEqual(run_lispy_string("(% 15 4)", self.env), 3)
        self.assertEqual(run_lispy_string("(% 20 6)", self.env), 2)
        self.assertEqual(run_lispy_string("(% 7 7)", self.env), 0)

        # Even/odd testing
        self.assertEqual(run_lispy_string("(% 8 2)", self.env), 0)  # Even
        self.assertEqual(run_lispy_string("(% 9 2)", self.env), 1)  # Odd
        self.assertEqual(run_lispy_string("(% 100 2)", self.env), 0)  # Even
        self.assertEqual(run_lispy_string("(% 101 2)", self.env), 1)  # Odd

    def test_modulo_with_floats(self):
        """Test modulo with floating point numbers."""
        self.assertAlmostEqual(run_lispy_string("(% 10.5 3)", self.env), 1.5)
        self.assertAlmostEqual(
            run_lispy_string("(% 7.8 2.5)", self.env), 0.3, places=10
        )
        self.assertAlmostEqual(run_lispy_string("(% 15.0 4)", self.env), 3.0)

    def test_modulo_with_negative_numbers(self):
        """Test modulo with negative numbers."""
        # Python's modulo behavior with negative numbers
        self.assertEqual(run_lispy_string("(% -10 3)", self.env), 2)
        self.assertEqual(run_lispy_string("(% 10 -3)", self.env), -2)
        self.assertEqual(run_lispy_string("(% -10 -3)", self.env), -1)

    def test_modulo_multiple_arguments(self):
        """Test modulo with multiple arguments (left-to-right evaluation)."""
        self.assertEqual(run_lispy_string("(% 20 6 3)", self.env), 2)
        self.assertEqual(run_lispy_string("(% 100 7 3)", self.env), 2)
        self.assertEqual(run_lispy_string("(% 50 8 5 2)", self.env), 0)

    def test_modulo_requires_at_least_two_arguments(self):
        """Test that modulo requires at least two arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(%)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: '%' requires at least two arguments."
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(% 5)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: '%' requires at least two arguments."
        )

    def test_modulo_by_zero_error(self):
        """Test that modulo by zero raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(% 10 0)", self.env)
        self.assertEqual(
            str(cm.exception), "ZeroDivisionError: Modulo by zero (argument 2)."
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(% 10 0 3)", self.env)
        self.assertEqual(
            str(cm.exception), "ZeroDivisionError: Modulo by zero (argument 2)."
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(% 10 3 0)", self.env)
        self.assertEqual(
            str(cm.exception), "ZeroDivisionError: Modulo by zero (argument 3)."
        )

    def test_modulo_type_errors(self):
        """Test that modulo raises errors for non-numeric arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(% "10" 3)', self.env)  # String argument
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 1 to '%' must be a number, got str: '10'",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(% 10 "3")', self.env)  # String argument
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 2 to '%' must be a number, got str: '3'",
        )

        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(% 10 3 nil)", self.env)  # nil argument
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 3 to '%' must be a number, got NoneType: 'None'",
        )

    def test_modulo_with_large_numbers(self):
        """Test modulo with large numbers."""
        self.assertEqual(run_lispy_string("(% 1000000 7)", self.env), 1)
        self.assertEqual(run_lispy_string("(% 999999 1000)", self.env), 999)
        self.assertEqual(
            run_lispy_string("(% 123456789 987654)", self.env), 123456789 % 987654
        )

    def test_modulo_preserves_integer_type(self):
        """Test that modulo preserves integer type when possible."""
        result = run_lispy_string("(% 10 3)", self.env)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)

        result = run_lispy_string("(% 10.0 3)", self.env)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)


if __name__ == "__main__":
    unittest.main()
