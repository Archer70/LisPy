import time
import unittest

from lispy.functions import global_env
from lispy.utils import run_lispy_string


class TestAsyncIntegration(unittest.TestCase):
    def setUp(self):
        self.env = global_env

    def test_basic_promise_creation(self):
        """Test creating and using promises."""
        # Test promise creation
        result = run_lispy_string("(promise (fn [] (+ 1 2)))", self.env)
        self.assertEqual(str(type(result).__name__), "LispyPromise")

        # Wait for promise to resolve
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 3)

    def test_resolve_function(self):
        """Test resolve function."""
        result = run_lispy_string("(resolve 42)", self.env)
        self.assertEqual(str(type(result).__name__), "LispyPromise")
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 42)

    def test_reject_function(self):
        """Test reject function."""
        result = run_lispy_string('(reject "error")', self.env)
        self.assertEqual(str(type(result).__name__), "LispyPromise")
        self.assertEqual(result.state, "rejected")
        self.assertEqual(result.error, "error")

    def test_async_with_await(self):
        """Test async block with await."""
        result = run_lispy_string("(async (await (resolve 100)))", self.env)
        self.assertEqual(result, 100)

    def test_async_with_promise_await(self):
        """Test async block with promise and await."""
        result = run_lispy_string("(async (await (promise (fn [] (* 5 5)))))", self.env)
        self.assertEqual(result, 25)

    def test_defn_async_basic(self):
        """Test defining and calling async functions."""
        # Define an async function
        run_lispy_string("(defn-async add-async [x y] (+ x y))", self.env)

        # Call the async function
        result = run_lispy_string("(add-async 3 4)", self.env)
        self.assertEqual(str(type(result).__name__), "LispyPromise")

        # Wait for result
        time.sleep(0.01)
        self.assertEqual(result.state, "resolved")
        self.assertEqual(result.value, 7)

    def test_async_with_defn_async(self):
        """Test using async function within async block."""
        # Define async function
        run_lispy_string("(defn-async multiply-async [x y] (* x y))", self.env)

        # Use in async block
        result = run_lispy_string("(async (await (multiply-async 6 7)))", self.env)
        self.assertEqual(result, 42)

    def test_async_with_io_operations(self):
        """Test async with I/O operations wrapped in promises."""
        # Test with simple string operation wrapped in promise
        result = run_lispy_string(
            '(async (await (promise (fn [] (to-str "hello world")))))', self.env
        )
        self.assertEqual(result, "hello world")

    def test_nested_async_operations(self):
        """Test nested async operations."""
        # Define nested async functions
        run_lispy_string("(defn-async inner-async [x] (+ x 10))", self.env)
        run_lispy_string(
            "(defn-async outer-async [x] (await (inner-async x)))", self.env
        )

        # Use nested async
        result = run_lispy_string("(async (await (outer-async 5)))", self.env)
        self.assertEqual(result, 15)

    def test_promise_with_complex_computation(self):
        """Test promise with more complex computation."""
        result = run_lispy_string(
            """
            (async 
              (await 
                (promise 
                  (fn [] (reduce [1 2 3 4 5] + 0)))))
        """,
            self.env,
        )
        self.assertEqual(result, 15)

    def test_async_error_handling(self):
        """Test async error handling."""
        # This should raise an error when awaited
        with self.assertRaises(Exception):
            run_lispy_string('(async (await (reject "test error")))', self.env)

    def test_documentation_available(self):
        """Test that documentation is available for async functions."""
        # Test promise documentation
        result = run_lispy_string("(doc promise)", self.env)
        self.assertIn("Creates a promise", result)

        # Test resolve documentation
        result = run_lispy_string("(doc resolve)", self.env)
        self.assertIn("already resolved", result)

        # Test reject documentation
        result = run_lispy_string("(doc reject)", self.env)
        self.assertIn("already rejected", result)


if __name__ == "__main__":
    unittest.main()
