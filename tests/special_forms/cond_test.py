import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class CondSpecialFormTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        run_lispy_string("(define x 10)", self.env)
        run_lispy_string("(define y -5)", self.env)
        run_lispy_string("(define z 0)", self.env)

    def test_cond_first_condition_true(self):
        """Test cond action first condition is true."""
        result = run_lispy_string('(cond true "first" false "second")', self.env)
        self.assertEqual(result, "first")

    def test_cond_second_condition_true(self):
        """Test cond action second condition is true."""
        result = run_lispy_string('(cond false "first" true "second")', self.env)
        self.assertEqual(result, "second")

    def test_cond_with_expressions(self):
        """Test cond with expression-based conditions."""
        result = run_lispy_string('(cond (> x 5) "big" (< x 5) "small")', self.env)
        self.assertEqual(result, "big")

    def test_cond_multiple_conditions(self):
        """Test cond with multiple conditions."""
        result = run_lispy_string(
            """
            (cond 
                (< x 0) "negative"
                (= x 0) "zero"
                (> x 0) "positive")
        """,
            self.env,
        )
        self.assertEqual(result, "positive")

    def test_cond_with_negative_number(self):
        """Test cond with negative number variable."""
        result = run_lispy_string(
            """
            (cond 
                (< y 0) "negative"
                (= y 0) "zero"
                (> y 0) "positive")
        """,
            self.env,
        )
        self.assertEqual(result, "negative")

    def test_cond_with_zero(self):
        """Test cond with zero variable."""
        result = run_lispy_string(
            """
            (cond 
                (< z 0) "negative"
                (= z 0) "zero"
                (> z 0) "positive")
        """,
            self.env,
        )
        self.assertEqual(result, "zero")

    def test_cond_no_conditions_match(self):
        """Test cond action no conditions match."""
        result = run_lispy_string('(cond false "first" false "second")', self.env)
        self.assertIsNone(result)

    def test_cond_with_else_condition(self):
        """Test cond with true as final catch-all."""
        result = run_lispy_string(
            """
            (cond 
                (< x -100) "very negative"
                (> x 100) "very positive"
                true "normal range")
        """,
            self.env,
        )
        self.assertEqual(result, "normal range")

    def test_cond_else_not_reached(self):
        """Test cond where catch-all is not reached."""
        result = run_lispy_string(
            """
            (cond 
                (> x 5) "bigger than 5"
                true "5 or less")
        """,
            self.env,
        )
        self.assertEqual(result, "bigger than 5")

    def test_cond_with_function_calls(self):
        """Test cond with function calls in conditions and results."""
        result = run_lispy_string(
            """
            (cond 
                (= (+ 2 3) 6) "wrong math"
                (= (+ 2 3) 5) "correct math")
        """,
            self.env,
        )
        self.assertEqual(result, "correct math")

    def test_cond_lazy_evaluation(self):
        """Test that cond only evaluates conditions until one matches."""
        # This would error if the division by zero was evaluated
        result = run_lispy_string(
            """
            (cond 
                (> x 0) "positive"
                (= (/ 1 0) 1) "this should not evaluate")
        """,
            self.env,
        )
        self.assertEqual(result, "positive")

    def test_cond_lazy_evaluation_results(self):
        """Test that cond only evaluates the result for the matching condition."""
        # Test that the second condition's result is not evaluated
        # by using a function that would cause an error if called
        result = run_lispy_string(
            """
            (cond 
                true "first result"
                false (/ 1 0))
        """,
            self.env,
        )

        self.assertEqual(result, "first result")  # Should not error on division by zero

    def test_cond_returns_complex_expressions(self):
        """Test cond returning complex expressions."""
        result = run_lispy_string(
            """
            (cond 
                (> x 5) (+ x 10)
                (< x 5) (- x 10))
        """,
            self.env,
        )
        self.assertEqual(result, 20)  # x=10, so 10+10=20

    def test_cond_nested_in_function(self):
        """Test cond used inside a function definition."""
        run_lispy_string(
            """
            (define classify 
                (fn [num]
                    (cond 
                        (< num 0) "negative"
                        (= num 0) "zero"
                        (> num 0) "positive")))
        """,
            self.env,
        )

        result1 = run_lispy_string("(classify -3)", self.env)
        result2 = run_lispy_string("(classify 0)", self.env)
        result3 = run_lispy_string("(classify 7)", self.env)

        self.assertEqual(result1, "negative")
        self.assertEqual(result2, "zero")
        self.assertEqual(result3, "positive")

    def test_cond_with_collections(self):
        """Test cond with collection predicates."""
        result = run_lispy_string(
            """
            (cond 
                (empty? []) "empty vector"
                (empty? [1 2]) "non-empty vector"
                true "fallback")
        """,
            self.env,
        )
        self.assertEqual(result, "empty vector")

    # --- Error Handling Tests ---
    def test_cond_no_arguments(self):
        """Test cond with no arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(cond)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'cond' requires at least one test-result pair.",
        )

    def test_cond_odd_number_of_arguments(self):
        """Test cond with odd number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(cond true)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'cond' requires an even number of arguments (test-result pairs).",
        )

    def test_cond_odd_number_multiple_args(self):
        """Test cond with odd number of arguments (multiple)."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(cond true "first" false)', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'cond' requires an even number of arguments (test-result pairs).",
        )

    def test_cond_with_error_in_condition(self):
        """Test cond action an error occurs in a condition."""
        with self.assertRaises(EvaluationError):
            run_lispy_string(
                '(cond (/ 1 0) "should not reach" true "fallback")', self.env
            )

    def test_cond_with_error_in_result(self):
        """Test cond action an error occurs in the result expression."""
        with self.assertRaises(EvaluationError):
            run_lispy_string('(cond true (/ 1 0) false "fallback")', self.env)

    def test_cond_single_pair(self):
        """Test cond with just one test-result pair."""
        result = run_lispy_string('(cond (> x 0) "positive")', self.env)
        self.assertEqual(result, "positive")

    def test_cond_single_pair_no_match(self):
        """Test cond with one pair that doesn't match."""
        result = run_lispy_string('(cond (< x 0) "negative")', self.env)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
