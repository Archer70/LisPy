import unittest

from lispy.environment import Environment
from lispy.evaluator import evaluate
from lispy.exceptions import EvaluationError
from lispy.functions import global_env
from lispy.types import Symbol

# We might need to parse some simple expressions to feed the evaluator
# from lispy.parser import parse # If needed for more complex test cases later


class EvaluatorTest(unittest.TestCase):
    def setUp(self):
        """Set up a new environment for each test.
        For tests involving global_env, we'll pass it directly."""
        self.env = Environment(outer=global_env)
        self.empty_env = Environment()

    def test_evaluate_numbers(self):
        self.assertEqual(evaluate(123, self.env), 123)
        self.assertEqual(evaluate(-10, self.env), -10)
        self.assertEqual(evaluate(3.14, self.env), 3.14)
        self.assertEqual(evaluate(0.0, self.env), 0.0)

    def test_evaluate_string(self):
        self.assertEqual(evaluate("hello", self.env), "hello")
        self.assertEqual(evaluate("", self.env), "")

    def test_evaluate_booleans(self):
        self.assertEqual(evaluate(True, self.env), True)
        self.assertEqual(evaluate(False, self.env), False)

    def test_evaluate_nil(self):
        self.assertEqual(evaluate(None, self.env), None)

    def test_evaluate_unbound_symbol(self):
        test_symbol = Symbol("my_var_really_unbound")
        with self.assertRaisesRegex(
            EvaluationError, "Unbound symbol: my_var_really_unbound"
        ):
            evaluate(test_symbol, self.empty_env)

    def test_evaluate_bound_symbol(self):
        self.env.define("my_var", 42)
        test_symbol = Symbol("my_var")
        self.assertEqual(evaluate(test_symbol, self.env), 42)

        self.env.define("another_var", "hello_lispy")
        test_symbol_2 = Symbol("another_var")
        self.assertEqual(evaluate(test_symbol_2, self.env), "hello_lispy")

    def test_evaluate_unhandled_list(self):
        pass

    def test_evaluate_other_unhandled_type(self):
        # Example of another unhandled type
        class UnhandledType:
            pass

        test_obj = UnhandledType()
        with self.assertRaisesRegex(
            EvaluationError, "Cannot evaluate type: UnhandledType"
        ):
            evaluate(test_obj, self.env)

    # --- New tests for function calls ---
    def test_evaluate_simple_addition(self):
        expr = [Symbol("+"), 1, 2]
        self.assertEqual(evaluate(expr, self.env), 3)

    def test_evaluate_addition_multiple_args(self):
        expr = [Symbol("+"), 1, 2, 3.0, 4]
        self.assertEqual(evaluate(expr, self.env), 10.0)

    def test_evaluate_addition_no_args(self):
        expr = [Symbol("+")]
        self.assertEqual(evaluate(expr, self.env), 0)

    def test_evaluate_addition_type_error(self):
        expr = [Symbol("+"), 1, "foo"]
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 2 to '\+' must be a number, got str: 'foo'",
        ):
            evaluate(expr, self.env)

    def test_evaluate_call_non_function_symbol(self):
        # Trying to call a symbol that is bound to a non-function (e.g. a number)
        self.env.define("not_a_function", 123)
        with self.assertRaisesRegex(
            EvaluationError,
            r"Object '.*' is not a function or a recognized callable procedure. \(Called with operator: 'not_a_function'\)",
        ):
            evaluate([Symbol("not_a_function"), "arg"], self.env)

    def test_evaluate_call_non_function_literal(self):
        expr = [1, 2, 3]
        with self.assertRaisesRegex(EvaluationError, "Object '1' is not a function."):
            evaluate(expr, self.env)

    def test_evaluate_empty_list_call(self):
        # An empty list itself, when evaluated as a form, should be an error.
        with self.assertRaisesRegex(
            EvaluationError,
            "Cannot evaluate an empty list as a function call or special form",
        ):
            evaluate([], self.env)

    def test_evaluate_call_empty_list_as_operator(self):
        # Evaluating (()) which parses to [[]]
        # This means trying to call [] as a function.
        # Now, the inner [] evaluation causes the error directly.
        expr = [[]]
        with self.assertRaisesRegex(
            EvaluationError,
            r"Cannot evaluate an empty list as a function call or special form",
        ):
            evaluate(expr, self.env)

    def test_evaluate_nested_call(self):
        expr = [Symbol("+"), 1, [Symbol("+"), 2, 3]]
        self.assertEqual(evaluate(expr, self.env), 6)

    def test_evaluate_lookup_from_global_env(self):
        local_env = Environment(outer=global_env)
        expr = [Symbol("+"), 5, 5]
        self.assertEqual(evaluate(expr, local_env), 10)


if __name__ == "__main__":
    unittest.main()
