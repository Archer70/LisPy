import unittest
import sys

from lispy.evaluator import evaluate
from lispy.functions import global_env
from lispy.environment import Environment
from lispy.types import Symbol
from lispy.exceptions import EvaluationError


class TailCallOptimizationTest(unittest.TestCase):
    """Test tail call optimization functionality."""

    def setUp(self):
        self.env = Environment(outer=global_env)

    def test_simple_tail_recursive_countdown(self):
        """Test a simple tail-recursive countdown function."""
        # Define countdown function
        countdown_fn = [
            Symbol("define"), Symbol("countdown"),
            [Symbol("fn"), [Symbol("n")],
             [Symbol("if"), [Symbol("<="), Symbol("n"), 0],
              Symbol("n"),
              [Symbol("countdown"), [Symbol("-"), Symbol("n"), 1]]]]
        ]
        
        evaluate(countdown_fn, self.env)
        
        # Test with small values
        result = evaluate([Symbol("countdown"), 5], self.env)
        self.assertEqual(result, 0)
        
        result = evaluate([Symbol("countdown"), 10], self.env)
        self.assertEqual(result, 0)

    def test_deep_tail_recursion(self):
        """Test that tail recursion can handle deep calls without stack overflow."""
        # Define countdown function
        countdown_fn = [
            Symbol("define"), Symbol("countdown"),
            [Symbol("fn"), [Symbol("n")],
             [Symbol("if"), [Symbol("<="), Symbol("n"), 0],
              Symbol("n"),
              [Symbol("countdown"), [Symbol("-"), Symbol("n"), 1]]]]
        ]
        
        evaluate(countdown_fn, self.env)
        
        # Test with values that would normally cause stack overflow
        # This should work with TCO but fail without it
        result = evaluate([Symbol("countdown"), 2000], self.env)
        self.assertEqual(result, 0)
        
        result = evaluate([Symbol("countdown"), 5000], self.env)
        self.assertEqual(result, 0)

    def test_tail_recursive_factorial(self):
        """Test tail-recursive factorial function."""
        # Define tail-recursive factorial helper
        factorial_tail_fn = [
            Symbol("define"), Symbol("factorial-tail"),
            [Symbol("fn"), [Symbol("n"), Symbol("acc")],
             [Symbol("if"), [Symbol("<="), Symbol("n"), 1],
              Symbol("acc"),
              [Symbol("factorial-tail"), [Symbol("-"), Symbol("n"), 1], [Symbol("*"), Symbol("n"), Symbol("acc")]]]]
        ]
        
        # Define wrapper factorial function
        factorial_fn = [
            Symbol("define"), Symbol("factorial"),
            [Symbol("fn"), [Symbol("n")],
             [Symbol("factorial-tail"), Symbol("n"), 1]]
        ]
        
        evaluate(factorial_tail_fn, self.env)
        evaluate(factorial_fn, self.env)
        
        # Test factorial calculations
        self.assertEqual(evaluate([Symbol("factorial"), 0], self.env), 1)
        self.assertEqual(evaluate([Symbol("factorial"), 1], self.env), 1)
        self.assertEqual(evaluate([Symbol("factorial"), 5], self.env), 120)
        self.assertEqual(evaluate([Symbol("factorial"), 10], self.env), 3628800)
        
        # Test with larger values that would cause stack overflow without TCO
        result = evaluate([Symbol("factorial"), 100], self.env)
        # Just check it's a very large number (factorial of 100)
        self.assertGreater(result, 10**150)

    def test_non_tail_recursion_still_works(self):
        """Test that non-tail recursive functions still work (but aren't optimized)."""
        # Define regular (non-tail) recursive factorial
        factorial_fn = [
            Symbol("define"), Symbol("factorial-regular"),
            [Symbol("fn"), [Symbol("n")],
             [Symbol("if"), [Symbol("<="), Symbol("n"), 1],
              1,
              [Symbol("*"), Symbol("n"), [Symbol("factorial-regular"), [Symbol("-"), Symbol("n"), 1]]]]]
        ]
        
        evaluate(factorial_fn, self.env)
        
        # Test with small values (large values would still cause stack overflow)
        self.assertEqual(evaluate([Symbol("factorial-regular"), 0], self.env), 1)
        self.assertEqual(evaluate([Symbol("factorial-regular"), 1], self.env), 1)
        self.assertEqual(evaluate([Symbol("factorial-regular"), 5], self.env), 120)

    def test_tail_call_in_if_branches(self):
        """Test that tail calls work in both branches of if statements."""
        # Define a function that has tail calls in both if branches
        even_odd_fn = [
            Symbol("define"), Symbol("is-even"),
            [Symbol("fn"), [Symbol("n")],
             [Symbol("if"), [Symbol("="), Symbol("n"), 0],
              True,
              [Symbol("if"), [Symbol("="), Symbol("n"), 1],
               False,
               [Symbol("is-even"), [Symbol("-"), Symbol("n"), 2]]]]]
        ]
        
        evaluate(even_odd_fn, self.env)
        
        # Test even/odd detection
        self.assertEqual(evaluate([Symbol("is-even"), 0], self.env), True)
        self.assertEqual(evaluate([Symbol("is-even"), 1], self.env), False)
        self.assertEqual(evaluate([Symbol("is-even"), 4], self.env), True)
        self.assertEqual(evaluate([Symbol("is-even"), 5], self.env), False)
        
        # Test with large values
        self.assertEqual(evaluate([Symbol("is-even"), 1000], self.env), True)
        self.assertEqual(evaluate([Symbol("is-even"), 1001], self.env), False)

    def test_mutual_recursion_not_optimized(self):
        """Test that mutual recursion works but isn't optimized (for now)."""
        # Define mutually recursive even/odd functions
        is_even_fn = [
            Symbol("define"), Symbol("is-even-mutual"),
            [Symbol("fn"), [Symbol("n")],
             [Symbol("if"), [Symbol("="), Symbol("n"), 0],
              True,
              [Symbol("is-odd-mutual"), [Symbol("-"), Symbol("n"), 1]]]]
        ]
        
        is_odd_fn = [
            Symbol("define"), Symbol("is-odd-mutual"),
            [Symbol("fn"), [Symbol("n")],
             [Symbol("if"), [Symbol("="), Symbol("n"), 0],
              False,
              [Symbol("is-even-mutual"), [Symbol("-"), Symbol("n"), 1]]]]
        ]
        
        evaluate(is_even_fn, self.env)
        evaluate(is_odd_fn, self.env)
        
        # Test with small values (large values might cause stack overflow)
        self.assertEqual(evaluate([Symbol("is-even-mutual"), 0], self.env), True)
        self.assertEqual(evaluate([Symbol("is-even-mutual"), 1], self.env), False)
        self.assertEqual(evaluate([Symbol("is-even-mutual"), 4], self.env), True)
        self.assertEqual(evaluate([Symbol("is-odd-mutual"), 3], self.env), True)
        self.assertEqual(evaluate([Symbol("is-odd-mutual"), 4], self.env), False)

    def test_tail_call_with_multiple_parameters(self):
        """Test tail calls with functions that have multiple parameters."""
        # Define a tail-recursive sum function that adds two numbers by counting
        sum_by_counting_fn = [
            Symbol("define"), Symbol("sum-by-counting"),
            [Symbol("fn"), [Symbol("a"), Symbol("b")],
             [Symbol("if"), [Symbol("="), Symbol("b"), 0],
              Symbol("a"),
              [Symbol("sum-by-counting"), [Symbol("+"), Symbol("a"), 1], [Symbol("-"), Symbol("b"), 1]]]]
        ]
        
        evaluate(sum_by_counting_fn, self.env)
        
        # Test sum calculations
        self.assertEqual(evaluate([Symbol("sum-by-counting"), 5, 3], self.env), 8)
        self.assertEqual(evaluate([Symbol("sum-by-counting"), 10, 7], self.env), 17)
        self.assertEqual(evaluate([Symbol("sum-by-counting"), 0, 5], self.env), 5)
        
        # Test with larger values to ensure TCO works
        self.assertEqual(evaluate([Symbol("sum-by-counting"), 100, 1000], self.env), 1100)

    def test_non_recursive_functions_unaffected(self):
        """Test that non-recursive functions work normally."""
        # Define a simple non-recursive function
        add_fn = [
            Symbol("define"), Symbol("add-two"),
            [Symbol("fn"), [Symbol("x")],
             [Symbol("+"), Symbol("x"), 2]]
        ]
        
        evaluate(add_fn, self.env)
        
        self.assertEqual(evaluate([Symbol("add-two"), 5], self.env), 7)
        self.assertEqual(evaluate([Symbol("add-two"), 10], self.env), 12)


if __name__ == '__main__':
    unittest.main() 