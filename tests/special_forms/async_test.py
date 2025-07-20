import unittest
import time
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, Symbol, Vector
from lispy.special_forms.async_form import handle_async_form
from lispy.special_forms.await_form import handle_await_form
from lispy.special_forms.defn_async_form import handle_defn_async_form
from lispy.functions.promises.promise import promise
from lispy.functions.promises.resolve import resolve
from lispy.functions.promises.reject import reject


class TestAsyncSpecialForms(unittest.TestCase):
    def setUp(self):
        self.env = Environment()
        # Add promise functions to environment
        self.env.define("promise", promise)
        self.env.define("resolve", resolve)
        self.env.define("reject", reject)

    def evaluate_fn(self, expr, env):
        """Simple evaluator for testing."""
        if isinstance(expr, (int, str, float)):
            return expr
        elif isinstance(expr, list) and len(expr) > 0:
            if expr[0] == Symbol("promise"):
                return promise(expr[1:], env)
            elif expr[0] == Symbol("resolve"):
                return resolve(expr[1:], env)
            elif expr[0] == Symbol("reject"):
                return reject(expr[1:], env)
            elif expr[0] == Symbol("+"):
                return sum(self.evaluate_fn(arg, env) for arg in expr[1:])
            elif expr[0] == Symbol("*"):
                result = 1
                for arg in expr[1:]:
                    result *= self.evaluate_fn(arg, env)
                return result
        elif isinstance(expr, Symbol):
            return env.lookup(expr.name)
        return expr

    def test_async_with_simple_value(self):
        """Test async with a simple value."""
        result = handle_async_form([Symbol("async"), 42], self.env, self.evaluate_fn)
        self.assertEqual(result, 42)

    def test_async_with_resolved_promise(self):
        """Test async with a resolved promise."""
        promise_expr = [Symbol("resolve"), 100]
        result = handle_async_form(
            [Symbol("async"), promise_expr], self.env, self.evaluate_fn
        )
        self.assertEqual(result, 100)

    def test_async_with_pending_promise(self):
        """Test async with a pending promise."""

        def slow_fn(args, env):
            time.sleep(0.01)
            return "async result"

        promise_expr = [Symbol("promise"), slow_fn]
        result = handle_async_form(
            [Symbol("async"), promise_expr], self.env, self.evaluate_fn
        )
        self.assertEqual(result, "async result")

    def test_async_wrong_arg_count(self):
        """Test async with wrong number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            handle_async_form([Symbol("async")], self.env, self.evaluate_fn)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'async' expects exactly 1 argument (body expression), got 0.",
        )

        with self.assertRaises(EvaluationError) as cm:
            handle_async_form([Symbol("async"), 1, 2], self.env, self.evaluate_fn)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'async' expects exactly 1 argument (body expression), got 2.",
        )

    def test_await_with_resolved_promise(self):
        """Test await with a resolved promise."""
        promise = resolve([42], self.env)
        result = handle_await_form(
            [Symbol("await"), promise], self.env, self.evaluate_fn
        )
        self.assertEqual(result, 42)

    def test_await_with_pending_promise(self):
        """Test await with a pending promise."""

        def slow_fn(args, env):
            time.sleep(0.01)
            return "awaited result"

        promise_obj = promise([slow_fn], self.env)
        result = handle_await_form(
            [Symbol("await"), promise_obj], self.env, self.evaluate_fn
        )
        self.assertEqual(result, "awaited result")

    def test_await_with_rejected_promise(self):
        """Test await with a rejected promise."""
        promise = reject(["Test error"], self.env)
        with self.assertRaises(EvaluationError) as cm:
            handle_await_form([Symbol("await"), promise], self.env, self.evaluate_fn)
        self.assertEqual(str(cm.exception), "Promise rejected: Test error")

    def test_await_with_non_promise(self):
        """Test await with non-promise value."""
        with self.assertRaises(EvaluationError) as cm:
            handle_await_form([Symbol("await"), 42], self.env, self.evaluate_fn)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'await' can only be used with promises, got int.",
        )

    def test_await_wrong_arg_count(self):
        """Test await with wrong number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            handle_await_form([Symbol("await")], self.env, self.evaluate_fn)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'await' expects exactly 1 argument (promise expression), got 0.",
        )

        promise = resolve([1], self.env)
        with self.assertRaises(EvaluationError) as cm:
            handle_await_form(
                [Symbol("await"), promise, promise], self.env, self.evaluate_fn
            )
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'await' expects exactly 1 argument (promise expression), got 2.",
        )

    def test_defn_async_basic(self):
        """Test defn-async with basic function."""
        name = Symbol("test-fn")
        params = Vector([Symbol("x")])
        body = [[Symbol("+"), Symbol("x"), 10]]

        result = handle_defn_async_form(
            [Symbol("defn-async"), name, params] + body, self.env, self.evaluate_fn
        )
        self.assertIsNone(result)  # defn-async returns nil

        # Check that function was defined
        self.assertTrue("test-fn" in self.env.store)
        async_fn = self.env.lookup("test-fn")
        self.assertTrue(callable(async_fn))

        # Call the async function
        promise = async_fn([5], self.env)
        self.assertIsInstance(promise, LispyPromise)

        # Wait for result
        time.sleep(0.01)
        self.assertEqual(promise.state, "resolved")
        self.assertEqual(promise.value, 15)

    def test_defn_async_no_params(self):
        """Test defn-async with no parameters."""
        name = Symbol("no-param-fn")
        params = Vector([])
        body = [42]

        handle_defn_async_form(
            [Symbol("defn-async"), name, params] + body, self.env, self.evaluate_fn
        )

        async_fn = self.env.lookup("no-param-fn")
        promise = async_fn([], self.env)

        time.sleep(0.01)
        self.assertEqual(promise.state, "resolved")
        self.assertEqual(promise.value, 42)

    def test_defn_async_multiple_params(self):
        """Test defn-async with multiple parameters."""
        name = Symbol("multi-param-fn")
        params = Vector([Symbol("x"), Symbol("y"), Symbol("z")])
        body = [[Symbol("+"), Symbol("x"), [Symbol("*"), Symbol("y"), Symbol("z")]]]

        handle_defn_async_form(
            [Symbol("defn-async"), name, params] + body, self.env, self.evaluate_fn
        )

        async_fn = self.env.lookup("multi-param-fn")
        promise = async_fn([1, 2, 3], self.env)

        time.sleep(0.01)
        self.assertEqual(promise.state, "resolved")
        self.assertEqual(promise.value, 7)  # 1 + (2 * 3)

    def test_defn_async_wrong_arg_count(self):
        """Test defn-async with wrong number of arguments."""
        with self.assertRaises(EvaluationError) as cm:
            handle_defn_async_form(
                [Symbol("defn-async"), Symbol("fn")], self.env, self.evaluate_fn
            )
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'defn-async' expects at least 3 arguments (name, params, body...), got 1.",
        )

        with self.assertRaises(EvaluationError) as cm:
            handle_defn_async_form(
                [Symbol("defn-async"), Symbol("fn"), Vector([])],
                self.env,
                self.evaluate_fn,
            )
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'defn-async' expects at least 3 arguments (name, params, body...), got 2.",
        )

    def test_defn_async_invalid_name(self):
        """Test defn-async with invalid function name."""
        with self.assertRaises(EvaluationError) as cm:
            handle_defn_async_form(
                [Symbol("defn-async"), 42, Vector([]), 1], self.env, self.evaluate_fn
            )
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'defn-async' function name must be a symbol, got int.",
        )

    def test_defn_async_invalid_params(self):
        """Test defn-async with invalid parameters."""
        with self.assertRaises(EvaluationError) as cm:
            handle_defn_async_form(
                [Symbol("defn-async"), Symbol("fn"), 42, 1], self.env, self.evaluate_fn
            )
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'defn-async' parameters must be a list or vector, got int.",
        )

        with self.assertRaises(EvaluationError) as cm:
            handle_defn_async_form(
                [Symbol("defn-async"), Symbol("fn"), Vector([42]), 1],
                self.env,
                self.evaluate_fn,
            )
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'defn-async' parameter must be a symbol, got int.",
        )

    def test_defn_async_wrong_call_args(self):
        """Test calling async function with wrong number of arguments."""
        name = Symbol("test-fn")
        params = Vector([Symbol("x")])
        body = [Symbol("x")]

        handle_defn_async_form(
            [Symbol("defn-async"), name, params] + body, self.env, self.evaluate_fn
        )
        async_fn = self.env.lookup("test-fn")

        with self.assertRaises(EvaluationError) as cm:
            async_fn([], self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'test-fn' expects 1 arguments, got 0."
        )

        with self.assertRaises(EvaluationError) as cm:
            async_fn([1, 2], self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'test-fn' expects 1 arguments, got 2."
        )


if __name__ == "__main__":
    unittest.main()
