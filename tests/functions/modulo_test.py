import unittest
from lispy.functions.modulo import builtin_modulo
from lispy.exceptions import EvaluationError


class ModuloTest(unittest.TestCase):
    """Test the modulo (%) function."""

    def test_basic_modulo(self):
        """Test basic modulo operations."""
        # Basic positive numbers
        self.assertEqual(builtin_modulo([10, 3]), 1)
        self.assertEqual(builtin_modulo([15, 4]), 3)
        self.assertEqual(builtin_modulo([20, 6]), 2)
        self.assertEqual(builtin_modulo([7, 7]), 0)
        
        # Even/odd testing
        self.assertEqual(builtin_modulo([8, 2]), 0)  # Even
        self.assertEqual(builtin_modulo([9, 2]), 1)  # Odd
        self.assertEqual(builtin_modulo([100, 2]), 0)  # Even
        self.assertEqual(builtin_modulo([101, 2]), 1)  # Odd

    def test_modulo_with_floats(self):
        """Test modulo with floating point numbers."""
        self.assertAlmostEqual(builtin_modulo([10.5, 3]), 1.5)
        self.assertAlmostEqual(builtin_modulo([7.8, 2.5]), 0.3, places=10)
        self.assertAlmostEqual(builtin_modulo([15.0, 4]), 3.0)

    def test_modulo_with_negative_numbers(self):
        """Test modulo with negative numbers."""
        # Python's modulo behavior with negative numbers
        self.assertEqual(builtin_modulo([-10, 3]), 2)  # -10 % 3 = 2 in Python
        self.assertEqual(builtin_modulo([10, -3]), -2)  # 10 % -3 = -2 in Python
        self.assertEqual(builtin_modulo([-10, -3]), -1)  # -10 % -3 = -1 in Python

    def test_modulo_multiple_arguments(self):
        """Test modulo with multiple arguments (left-to-right evaluation)."""
        # (% 20 6 3) = (% (% 20 6) 3) = (% 2 3) = 2
        self.assertEqual(builtin_modulo([20, 6, 3]), 2)
        
        # (% 100 7 3) = (% (% 100 7) 3) = (% 2 3) = 2
        self.assertEqual(builtin_modulo([100, 7, 3]), 2)
        
        # (% 50 8 5 2) = (% (% (% 50 8) 5) 2) = (% (% 2 5) 2) = (% 2 2) = 0
        self.assertEqual(builtin_modulo([50, 8, 5, 2]), 0)

    def test_modulo_requires_at_least_two_arguments(self):
        """Test that modulo requires at least two arguments."""
        with self.assertRaises(EvaluationError) as cm:
            builtin_modulo([])
        self.assertEqual(str(cm.exception), "SyntaxError: '%' requires at least two arguments.")
        
        with self.assertRaises(EvaluationError) as cm:
            builtin_modulo([5])
        self.assertEqual(str(cm.exception), "SyntaxError: '%' requires at least two arguments.")

    def test_modulo_by_zero_error(self):
        """Test that modulo by zero raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            builtin_modulo([10, 0])
        self.assertEqual(str(cm.exception), "ZeroDivisionError: Modulo by zero (argument 2).")
        
        # Test with multiple arguments where second is zero
        with self.assertRaises(EvaluationError) as cm:
            builtin_modulo([10, 0, 3])
        self.assertEqual(str(cm.exception), "ZeroDivisionError: Modulo by zero (argument 2).")
        
        # Test with multiple arguments where third is zero
        with self.assertRaises(EvaluationError) as cm:
            builtin_modulo([10, 3, 0])
        self.assertEqual(str(cm.exception), "ZeroDivisionError: Modulo by zero (argument 3).")

    def test_modulo_type_errors(self):
        """Test that modulo raises errors for non-numeric arguments."""
        with self.assertRaises(EvaluationError) as cm:
            builtin_modulo(["10", 3])
        self.assertEqual(str(cm.exception), "TypeError: Argument 1 to '%' must be a number, got str: '10'")
        
        with self.assertRaises(EvaluationError) as cm:
            builtin_modulo([10, "3"])
        self.assertEqual(str(cm.exception), "TypeError: Argument 2 to '%' must be a number, got str: '3'")
        
        with self.assertRaises(EvaluationError) as cm:
            builtin_modulo([10, 3, None])
        self.assertEqual(str(cm.exception), "TypeError: Argument 3 to '%' must be a number, got NoneType: 'None'")

    def test_modulo_with_large_numbers(self):
        """Test modulo with large numbers."""
        self.assertEqual(builtin_modulo([1000000, 7]), 1)
        self.assertEqual(builtin_modulo([999999, 1000]), 999)
        self.assertEqual(builtin_modulo([123456789, 987654]), 123456789 % 987654)

    def test_modulo_preserves_integer_type(self):
        """Test that modulo preserves integer type when possible."""
        result = builtin_modulo([10, 3])
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)
        
        # With floats, result should be float
        result = builtin_modulo([10.0, 3])
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)


if __name__ == '__main__':
    unittest.main() 