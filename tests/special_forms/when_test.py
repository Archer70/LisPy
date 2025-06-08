import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError


class WhenSpecialFormTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        run_lispy_string("(define x 10)", self.env)
        run_lispy_string("(define y -5)", self.env)
        run_lispy_string("(define z 0)", self.env)

    def test_when_true_condition_single_expression(self):
        """Test when with true condition and single expression."""
        result = run_lispy_string('(when true "executed")', self.env)
        self.assertEqual(result, "executed")

    def test_when_false_condition_single_expression(self):
        """Test when with false condition and single expression."""
        result = run_lispy_string('(when false "not executed")', self.env)
        self.assertIsNone(result)

    def test_when_true_condition_multiple_expressions(self):
        """Test when with true condition and multiple expressions."""
        result = run_lispy_string('''
            (when true
              "first"
              "second"
              "third")
        ''', self.env)
        self.assertEqual(result, "third")  # Returns last expression

    def test_when_false_condition_multiple_expressions(self):
        """Test when with false condition and multiple expressions."""
        result = run_lispy_string('''
            (when false
              "first"
              "second"
              "third")
        ''', self.env)
        self.assertIsNone(result)

    def test_when_with_expression_condition(self):
        """Test when with expression-based condition."""
        result = run_lispy_string('(when (> x 5) "x is big")', self.env)
        self.assertEqual(result, "x is big")

    def test_when_with_false_expression_condition(self):
        """Test when with false expression-based condition."""
        result = run_lispy_string('(when (< x 0) "x is negative")', self.env)
        self.assertIsNone(result)

    def test_when_no_body_expressions_true(self):
        """Test when with no body expressions and true condition."""
        result = run_lispy_string('(when true)', self.env)
        self.assertTrue(result)  # Returns the test value itself

    def test_when_no_body_expressions_false(self):
        """Test when with no body expressions and false condition."""
        result = run_lispy_string('(when false)', self.env)
        self.assertIsNone(result)

    def test_when_with_side_effects(self):
        """Test when with side effects (variable assignments)."""
        run_lispy_string('(define counter 0)', self.env)
        result = run_lispy_string('''
            (when (> x 0)
              (define counter (+ counter 1))
              (define counter (+ counter 10))
              counter)
        ''', self.env)
        
        counter_value = run_lispy_string('counter', self.env)
        self.assertEqual(result, 11)
        self.assertEqual(counter_value, 11)

    def test_when_no_side_effects_action_false(self):
        """Test that when doesn't execute side effects action condition is false."""
        run_lispy_string('(define counter 0)', self.env)
        result = run_lispy_string('''
            (when (< x 0)
              (define counter (+ counter 1))
              (define counter (+ counter 10))
              counter)
        ''', self.env)
        
        counter_value = run_lispy_string('counter', self.env)
        self.assertIsNone(result)
        self.assertEqual(counter_value, 0)  # Counter unchanged

    def test_when_with_complex_expressions(self):
        """Test when with complex expressions in body."""
        result = run_lispy_string('''
            (when (> x 5)
              (+ x 10)
              (* x 2)
              (- x 1))
        ''', self.env)
        self.assertEqual(result, 9)  # Last expression: x - 1 = 10 - 1 = 9

    def test_when_nested_in_function(self):
        """Test when used inside a function definition."""
        run_lispy_string('''
            (define maybe-process 
                (fn [value]
                    (when (> value 0)
                      (define result (* value 2))
                      (+ result 1))))
        ''', self.env)
        
        result1 = run_lispy_string('(maybe-process 5)', self.env)
        result2 = run_lispy_string('(maybe-process -3)', self.env)
        
        self.assertEqual(result1, 11)  # (5 * 2) + 1 = 11
        self.assertIsNone(result2)

    def test_when_with_function_calls(self):
        """Test when with function calls in condition and body."""
        result = run_lispy_string('''
            (when (= (+ 2 3) 5)
              (+ 10 20)
              (* 3 4))
        ''', self.env)
        self.assertEqual(result, 12)

    def test_when_lazy_evaluation(self):
        """Test that when doesn't evaluate body action condition is false."""
        # This would error if division by zero was evaluated
        result = run_lispy_string('''
            (when false
              (/ 1 0)
              "should not execute")
        ''', self.env)
        self.assertIsNone(result)

    def test_when_with_collections(self):
        """Test when with collection predicates."""
        result = run_lispy_string('''
            (when (empty? [])
              "vector is empty"
              "confirmed empty")
        ''', self.env)
        self.assertEqual(result, "confirmed empty")

    def test_when_truthiness_with_numbers(self):
        """Test when truthiness with different values."""
        # Non-zero numbers are truthy
        result1 = run_lispy_string('(when 1 "truthy")', self.env)
        result2 = run_lispy_string('(when 0 "truthy")', self.env)
        result3 = run_lispy_string('(when -1 "truthy")', self.env)
        
        self.assertEqual(result1, "truthy")
        self.assertEqual(result2, "truthy")  # 0 is truthy in this Lisp
        self.assertEqual(result3, "truthy")

    def test_when_truthiness_with_strings(self):
        """Test when truthiness with strings."""
        result1 = run_lispy_string('(when "hello" "truthy")', self.env)
        result2 = run_lispy_string('(when "" "truthy")', self.env)
        
        self.assertEqual(result1, "truthy")
        self.assertEqual(result2, "truthy")  # Empty string is truthy

    def test_when_with_nil_condition(self):
        """Test when with None (nil) condition."""
        # Test with an if expression that returns None action false
        result = run_lispy_string('(when (if false "something") "should not execute")', self.env)
        self.assertIsNone(result)

    # --- Error Handling Tests ---
    def test_when_no_arguments(self):
        """Test when with no arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(when)", self.env)
        self.assertEqual(str(cm.exception), "SyntaxError: 'when' requires at least a test expression.")

    def test_when_with_error_in_condition(self):
        """Test when action an error occurs in the condition."""
        with self.assertRaises(EvaluationError):
            run_lispy_string('(when (/ 1 0) "should not reach")', self.env)

    def test_when_with_error_in_body(self):
        """Test when action an error occurs in the body."""
        with self.assertRaises(EvaluationError):
            run_lispy_string('(when true (/ 1 0))', self.env)

    def test_when_vs_if_comparison(self):
        """Test demonstrating difference between action and if."""
        # when allows multiple expressions naturally
        result_action = run_lispy_string('''
            (when (> x 0)
              (+ x 1)
              (* x 2)
              (- x 3))
        ''', self.env)
        
        # if would need nested structure or function wrapping for multiple expressions
        result_if = run_lispy_string('(if (> x 0) (- x 3))', self.env)
        
        self.assertEqual(result_action, 7)  # x=10, so 10-3=7
        self.assertEqual(result_if, 7)    # Same final result but if can't do multiple expressions


if __name__ == '__main__':
    unittest.main() 