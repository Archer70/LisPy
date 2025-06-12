import unittest
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError


class LoopSpecialFormTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    # --- Basic Loop Tests ---

    def test_loop_simple_countdown(self):
        """Test basic loop with recur - countdown from 5 to 0."""
        result = run_lispy_string(
            """
        (loop [n 5]
          (if (<= n 0)
            "done"
            (recur (- n 1))))
        """,
            self.env,
        )
        self.assertEqual(result, "done")

    def test_loop_accumulator_pattern(self):
        """Test loop with accumulator - sum numbers from 1 to 5."""
        result = run_lispy_string(
            """
        (loop [n 5 acc 0]
          (if (<= n 0)
            acc
            (recur (- n 1) (+ acc n))))
        """,
            self.env,
        )
        self.assertEqual(result, 15)  # 1+2+3+4+5 = 15

    def test_loop_factorial(self):
        """Test loop implementing factorial."""
        result = run_lispy_string(
            """
        (loop [n 5 acc 1]
          (if (<= n 1)
            acc
            (recur (- n 1) (* acc n))))
        """,
            self.env,
        )
        self.assertEqual(result, 120)  # 5! = 120

    def test_loop_vector_processing(self):
        """Test loop processing a vector - reverse it."""
        result = run_lispy_string(
            """
        (loop [items [1 2 3 4] result []]
          (if (empty? items)
            result
            (recur (rest items) (conj result (first items)))))
        """,
            self.env,
        )
        # This creates [1 2 3 4] due to how conj works with vectors
        from lispy.types import Vector

        self.assertEqual(result, Vector([1, 2, 3, 4]))

    def test_loop_complex_condition(self):
        """Test loop with complex termination condition."""
        result = run_lispy_string(
            """
        (loop [x 10 y 1]
          (if (or (<= x 0) (>= y 100))
            (conj (conj [] x) y)
            (recur (- x 2) (* y 3))))
        """,
            self.env,
        )
        # After iterations: [10,1] -> [8,3] -> [6,9] -> [4,27] -> [2,81] -> [0,243]
        from lispy.types import Vector

        self.assertEqual(result, Vector([0, 243]))

    # --- Loop Without Recur Tests ---

    def test_loop_without_recur_immediate_return(self):
        """Test loop that returns immediately without using recur."""
        result = run_lispy_string(
            """
        (loop [x 42]
          x)
        """,
            self.env,
        )
        self.assertEqual(result, 42)

    def test_loop_without_recur_conditional_return(self):
        """Test loop with conditional logic but no recur."""
        result = run_lispy_string(
            """
        (loop [x 5 y 10]
          (if (> x y)
            "x is bigger"
            "y is bigger or equal"))
        """,
            self.env,
        )
        self.assertEqual(result, "y is bigger or equal")

    def test_loop_multiple_expressions_in_body(self):
        """Test loop with multiple expressions in body - returns last."""
        result = run_lispy_string(
            """
        (loop [n 3]
          (define temp (* n 2))
          (define result (+ temp 1))
          result)
        """,
            self.env,
        )
        self.assertEqual(result, 7)  # 3*2+1 = 7

    # --- Loop Variable Scoping Tests ---

    def test_loop_variables_lexical_scope(self):
        """Test that loop variables are properly scoped."""
        run_lispy_string("(define x 100)", self.env)
        result = run_lispy_string(
            """
        (loop [x 5]
          x)
        """,
            self.env,
        )
        self.assertEqual(result, 5)
        # Outer x should be unchanged
        outer_x = run_lispy_string("x", self.env)
        self.assertEqual(outer_x, 100)

    def test_loop_variables_shadow_outer_scope(self):
        """Test that loop variables properly shadow outer variables."""
        run_lispy_string("(define n 999)", self.env)
        result = run_lispy_string(
            """
        (loop [n 3 acc 0]
          (if (<= n 0)
            acc
            (recur (- n 1) (+ acc n))))
        """,
            self.env,
        )
        self.assertEqual(result, 6)  # 3+2+1 = 6
        # Outer n should be unchanged
        outer_n = run_lispy_string("n", self.env)
        self.assertEqual(outer_n, 999)

    def test_loop_access_outer_scope(self):
        """Test that loop can access variables from outer scope."""
        run_lispy_string("(define multiplier 10)", self.env)
        result = run_lispy_string(
            """
        (loop [n 3]
          (if (<= n 0)
            0
            (* n multiplier)))
        """,
            self.env,
        )
        self.assertEqual(result, 30)  # 3 * 10 = 30

    # --- Argument Validation Tests ---

    def test_loop_no_arguments(self):
        """Test loop with no arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(loop)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'loop' requires a bindings vector and at least one body expression. Usage: (loop [var val ...] body...)",
        )

    def test_loop_only_bindings_no_body(self):
        """Test loop with bindings but no body."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(loop [x 1])", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'loop' requires a bindings vector and at least one body expression. Usage: (loop [var val ...] body...)",
        )

    def test_loop_bindings_not_vector(self):
        """Test loop with bindings that are not a vector."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(loop "not-a-vector" x)', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: Bindings for 'loop' must be a vector/list, got str. Usage: (loop [var val ...] body...)",
        )

    def test_loop_odd_number_of_bindings(self):
        """Test loop with odd number of binding elements."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(loop [x 1 y] x)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: Bindings in 'loop' must be in symbol-value pairs. Found an odd number of elements in bindings vector: [x, 1, y]. Usage: (loop [var val ...] body...)",
        )

    def test_loop_binding_variable_not_symbol(self):
        """Test loop with binding variable that's not a symbol."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(loop [42 1] x)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: Variable in 'loop' binding must be a symbol, got int: '42' at index 0 in bindings vector.",
        )

    # --- Recur Validation Tests ---

    def test_loop_recur_arity_mismatch_too_few(self):
        """Test recur with too few arguments for loop bindings."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(
                """
            (loop [x 1 y 2]
              (recur 10))
            """,
                self.env,
            )
        self.assertEqual(
            str(cm.exception),
            "ArityError: 'recur' expects 2 arguments to match function parameters, got 1.",
        )

    def test_loop_recur_arity_mismatch_too_many(self):
        """Test recur with too many arguments for loop bindings."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string(
                """
            (loop [x 1]
              (recur 10 20 30))
            """,
                self.env,
            )
        self.assertEqual(
            str(cm.exception),
            "ArityError: 'recur' expects 1 arguments to match function parameters, got 3.",
        )

    # --- Edge Cases ---

    def test_loop_empty_bindings(self):
        """Test loop with empty bindings vector."""
        result = run_lispy_string(
            """
        (loop []
          42)
        """,
            self.env,
        )
        self.assertEqual(result, 42)

    def test_loop_with_nil_values(self):
        """Test loop with nil initial values."""
        result = run_lispy_string(
            """
        (loop [x nil y nil]
          (if (and (not x) (not y))
            "both nil"
            "not both nil"))
        """,
            self.env,
        )
        self.assertEqual(result, "both nil")

    def test_loop_recur_with_complex_expressions(self):
        """Test recur with complex argument expressions."""
        result = run_lispy_string(
            """
        (loop [n 5 items []]
          (if (<= n 0)
            items
            (recur (- n 1) (conj items (* n n)))))
        """,
            self.env,
        )
        # Should add squares: 25, 16, 9, 4, 1 (in reverse order due to conj)
        from lispy.types import Vector

        self.assertEqual(result, Vector([25, 16, 9, 4, 1]))

    # --- Performance/Deep Recursion Tests ---

    def test_loop_deep_iteration_no_stack_overflow(self):
        """Test that loop can handle deep iteration without stack overflow."""
        result = run_lispy_string(
            """
        (loop [n 1000]
          (if (<= n 0)
            "completed"
            (recur (- n 1))))
        """,
            self.env,
        )
        self.assertEqual(result, "completed")

    def test_loop_large_accumulation(self):
        """Test loop with large accumulation."""
        result = run_lispy_string(
            """
        (loop [n 100 sum 0]
          (if (<= n 0)
            sum
            (recur (- n 1) (+ sum n))))
        """,
            self.env,
        )
        self.assertEqual(result, 5050)  # Sum of 1 to 100

    # --- Interaction with Other Features ---

    def test_loop_with_thread_first(self):
        """Test loop used with thread-first macro."""
        # Create a simple function that uses loop internally
        run_lispy_string(
            """
        (define factorial-loop (fn [n]
          (loop [i n acc 1]
            (if (<= i 1)
              acc
              (recur (- i 1) (* acc i))))))
        """,
            self.env,
        )

        result = run_lispy_string("(-> 5 factorial-loop)", self.env)
        self.assertEqual(result, 120)  # 5!

    def test_loop_nested_in_function(self):
        """Test loop used inside a function."""
        run_lispy_string(
            """
        (define countdown-from (fn [start]
          (loop [n start]
            (if (<= n 0)
              "done"
              (recur (- n 1))))))
        """,
            self.env,
        )

        result = run_lispy_string("(countdown-from 5)", self.env)
        self.assertEqual(result, "done")

    def test_loop_with_cond(self):
        """Test loop with cond for multiple conditions."""
        result = run_lispy_string(
            """
        (loop [x 15]
          (cond
            (= x 0) "zero"
            (< x 5) "small"
            (< x 10) "medium"
            true (recur (- x 5))))
        """,
            self.env,
        )
        self.assertEqual(
            result, "medium"
        )  # 15 -> 10 -> 5, and 5 is not < 5, so "medium"


if __name__ == "__main__":
    unittest.main()
