# lispy_project/tests/special_forms/if_form_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class IfFormTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    # --- Tests for 'if' special form ---
    def test_if_true_condition(self):
        # (if true 10 20) -> 10
        result = run_lispy_string("(if true 10 20)", self.env)
        self.assertEqual(result, 10)

    def test_if_false_condition(self):
        # (if false 10 20) -> 20
        result = run_lispy_string("(if false 10 20)", self.env)
        self.assertEqual(result, 20)

    def test_if_nil_condition_is_falsey(self):
        # (if nil 10 20) -> 20 (nil is falsey)
        result = run_lispy_string("(if nil 10 20)", self.env)
        self.assertEqual(result, 20)

    def test_if_truthy_condition_number(self):
        # (if 0 10 20) -> 10 (0 is truthy)
        result = run_lispy_string("(if 0 10 20)", self.env)
        self.assertEqual(result, 10)

    def test_if_truthy_condition_string(self):
        # (if "hello" 10 20) -> 10 ("hello" is truthy)
        result = run_lispy_string('(if "hello" 10 20)', self.env)
        self.assertEqual(result, 10)

    def test_if_truthy_condition_empty_list(self):
        # (if '() 10 20) -> 10 (empty list is truthy in LisPy)
        # Empty lists are truthy, not an error
        result = run_lispy_string("(if '() 10 20)", self.env)
        self.assertEqual(result, 10)

    def test_if_false_condition_no_else(self):
        # (if false 10) -> nil (None)
        result = run_lispy_string("(if false 10)", self.env)
        self.assertIsNone(result)

    def test_if_true_condition_no_else(self):
        # (if true 10) -> 10
        result = run_lispy_string("(if true 10)", self.env)
        self.assertEqual(result, 10)

    def test_if_condition_is_expression(self):
        # (if (= 5 5) (+ 1 2) (+ 3 4)) -> 3
        result = run_lispy_string("(if (= 5 5) (+ 1 2) (+ 3 4))", self.env)
        self.assertEqual(result, 3)

    def test_if_only_correct_branch_is_evaluated(self):
        # Define x, then (if true (define x 100) (define x 200)), x should be 100
        run_lispy_string("(define x 1)", self.env)
        run_lispy_string("(if true (define x 100) (define x 200))", self.env)
        self.assertEqual(
            self.env.lookup("x"), 100, "True branch should have been evaluated"
        )

        # Reset x, then (if false (define x 300) (define x 400)), x should be 400
        run_lispy_string("(define x 1)", self.env)  # Reset x
        run_lispy_string("(if false (define x 300) (define x 400))", self.env)
        self.assertEqual(
            self.env.lookup("x"), 400, "False branch should have been evaluated"
        )

    def test_if_syntax_errors(self):
        # Too few arguments
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(if true)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'if' requires a condition, a then-expression, and an optional else-expression. Usage: (if cond then) or (if cond then else)",
        )
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(if)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'if' requires a condition, a then-expression, and an optional else-expression. Usage: (if cond then) or (if cond then else)",
        )
        # Too many arguments
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(if true 1 2 3)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'if' requires a condition, a then-expression, and an optional else-expression. Usage: (if cond then) or (if cond then else)",
        )


if __name__ == "__main__":
    unittest.main()
