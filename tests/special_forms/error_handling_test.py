import unittest

from lispy.environment import Environment
from lispy.exceptions import EvaluationError, UserThrownError
from lispy.special_forms.throw_form import handle_throw_form
from lispy.special_forms.try_form import handle_try_form
from lispy.types import Symbol


class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        self.env = Environment()

    def evaluate_fn(self, expr, env):
        """Simple evaluator for testing."""
        if isinstance(expr, (int, str, float)):
            return expr
        elif isinstance(expr, list) and len(expr) > 0:
            if expr[0] == Symbol("+"):
                return sum(self.evaluate_fn(arg, env) for arg in expr[1:])
            elif expr[0] == Symbol("*"):
                result = 1
                for arg in expr[1:]:
                    result *= self.evaluate_fn(arg, env)
                return result
            elif expr[0] == Symbol("str"):
                return str(self.evaluate_fn(expr[1], env))
            elif expr[0] == Symbol("throw"):
                return handle_throw_form(expr, env, self.evaluate_fn)
            elif expr[0] == Symbol("try"):
                return handle_try_form(expr, env, self.evaluate_fn)
        elif isinstance(expr, Symbol):
            return env.lookup(expr.name)
        return expr

    def test_throw_simple_value(self):
        """Test throwing a simple value."""
        with self.assertRaises(UserThrownError) as cm:
            handle_throw_form(
                [Symbol("throw"), "test error"], self.env, self.evaluate_fn
            )
        self.assertEqual(cm.exception.value, "test error")

    def test_throw_evaluated_expression(self):
        """Test throwing an evaluated expression."""
        with self.assertRaises(UserThrownError) as cm:
            handle_throw_form(
                [Symbol("throw"), [Symbol("+"), 1, 2]], self.env, self.evaluate_fn
            )
        self.assertEqual(cm.exception.value, 3)

    def test_throw_wrong_arg_count(self):
        """Test throw with wrong number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            handle_throw_form([Symbol("throw")], self.env, self.evaluate_fn)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'throw' expects exactly 1 argument (value), got 0.",
        )

        with self.assertRaises(EvaluationError) as cm:
            handle_throw_form([Symbol("throw"), 1, 2], self.env, self.evaluate_fn)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'throw' expects exactly 1 argument (value), got 2.",
        )

    def test_try_catch_user_thrown_error(self):
        """Test try/catch with user-thrown error."""
        result = handle_try_form(
            [
                Symbol("try"),
                [Symbol("throw"), "error message"],
                [Symbol("catch"), Symbol("e"), [Symbol("str"), Symbol("e")]],
            ],
            self.env,
            self.evaluate_fn,
        )
        self.assertEqual(result, "error message")

    def test_try_catch_system_error(self):
        """Test try/catch with system error."""

        # Create a simple error by dividing by zero (we'll simulate this)
        def error_eval(expr, env):
            if expr == Symbol("cause-error"):
                raise EvaluationError("Division by zero")
            return self.evaluate_fn(expr, env)

        result = handle_try_form(
            [
                Symbol("try"),
                Symbol("cause-error"),
                [Symbol("catch"), Symbol("e"), [Symbol("str"), Symbol("e")]],
            ],
            self.env,
            error_eval,
        )
        self.assertEqual(result, "Division by zero")

    def test_try_without_error(self):
        """Test try block that doesn't throw an error."""
        result = handle_try_form(
            [
                Symbol("try"),
                [Symbol("+"), 1, 2],
                [Symbol("catch"), Symbol("e"), "not executed"],
            ],
            self.env,
            self.evaluate_fn,
        )
        self.assertEqual(result, 3)

    def test_try_finally_without_error(self):
        """Test try/finally without error."""
        self.env.define("cleanup-called", False)

        def test_eval(expr, env):
            if expr == Symbol("do-cleanup"):
                env.define("cleanup-called", True)
                return None
            return self.evaluate_fn(expr, env)

        result = handle_try_form(
            [
                Symbol("try"),
                [Symbol("+"), 5, 5],
                [Symbol("finally"), Symbol("do-cleanup")],
            ],
            self.env,
            test_eval,
        )

        self.assertEqual(result, 10)
        self.assertTrue(self.env.lookup("cleanup-called"))

    def test_try_catch_finally(self):
        """Test try/catch/finally all together."""
        self.env.define("cleanup-called", False)

        def test_eval(expr, env):
            if expr == Symbol("do-cleanup"):
                env.define("cleanup-called", True)
                return None
            return self.evaluate_fn(expr, env)

        result = handle_try_form(
            [
                Symbol("try"),
                [Symbol("throw"), "error"],
                [Symbol("catch"), Symbol("e"), [Symbol("str"), Symbol("e")]],
                [Symbol("finally"), Symbol("do-cleanup")],
            ],
            self.env,
            test_eval,
        )

        self.assertEqual(result, "error")
        self.assertTrue(self.env.lookup("cleanup-called"))

    def test_try_finally_with_error_no_catch(self):
        """Test try/finally with error but no catch - error should propagate."""
        self.env.define("cleanup-called", False)

        def test_eval(expr, env):
            if expr == Symbol("do-cleanup"):
                env.define("cleanup-called", True)
                return None
            return self.evaluate_fn(expr, env)

        with self.assertRaises(UserThrownError):
            handle_try_form(
                [
                    Symbol("try"),
                    [Symbol("throw"), "error"],
                    [Symbol("finally"), Symbol("do-cleanup")],
                ],
                self.env,
                test_eval,
            )

        # Cleanup should still have been called
        self.assertTrue(self.env.lookup("cleanup-called"))

    def test_try_multiple_expressions_in_body(self):
        """Test try with multiple expressions in catch/finally bodies."""
        # Test that multiple expressions in catch body are executed in sequence
        # and that the last expression's value is returned
        result = handle_try_form(
            [
                Symbol("try"),
                [Symbol("throw"), "error"],
                [
                    Symbol("catch"),
                    Symbol("e"),
                    [Symbol("+"), 1, 2],  # First expression
                    [Symbol("*"), 3, 4],
                ],  # Second expression (should be returned)
            ],
            self.env,
            self.evaluate_fn,
        )

        # The result should be the value of the last expression in the catch block
        self.assertEqual(result, 12)

    def test_try_invalid_syntax(self):
        """Test try with invalid syntax."""
        # Missing body
        with self.assertRaises(EvaluationError) as cm:
            handle_try_form([Symbol("try")], self.env, self.evaluate_fn)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'try' expects at least 1 argument (body), got 0.",
        )

        # Invalid catch clause
        with self.assertRaises(EvaluationError) as cm:
            handle_try_form(
                [
                    Symbol("try"),
                    42,
                    [Symbol("catch")],  # Missing binding and body
                ],
                self.env,
                self.evaluate_fn,
            )
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'catch' expects at least 2 arguments (binding handler-body...), got 0.",
        )

        # Invalid catch binding
        with self.assertRaises(EvaluationError) as cm:
            handle_try_form(
                [
                    Symbol("try"),
                    42,
                    [Symbol("catch"), 42, "handler"],  # Binding must be symbol
                ],
                self.env,
                self.evaluate_fn,
            )
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'catch' binding must be a symbol, got int."
        )

        # Multiple catch clauses
        with self.assertRaises(EvaluationError) as cm:
            handle_try_form(
                [
                    Symbol("try"),
                    42,
                    [Symbol("catch"), Symbol("e1"), "handler1"],
                    [Symbol("catch"), Symbol("e2"), "handler2"],
                ],
                self.env,
                self.evaluate_fn,
            )
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'try' can only have one 'catch' clause."
        )

        # Multiple finally clauses
        with self.assertRaises(EvaluationError) as cm:
            handle_try_form(
                [
                    Symbol("try"),
                    42,
                    [Symbol("finally"), "cleanup1"],
                    [Symbol("finally"), "cleanup2"],
                ],
                self.env,
                self.evaluate_fn,
            )
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'try' can only have one 'finally' clause."
        )


if __name__ == "__main__":
    unittest.main()
