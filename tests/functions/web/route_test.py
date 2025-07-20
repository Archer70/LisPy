"""
Tests for route function.
"""

import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.web.app import WebApp


class TestRoute(unittest.TestCase):
    """Test route function."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_route_basic_usage(self):
        """Test basic route registration."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/" (fn [request] {:status 200 :body "Hello"}))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertIsInstance(result, WebApp)
        self.assertEqual(len(result.router.routes), 1)

        route = result.router.routes[0]
        self.assertEqual(route.method, "GET")
        self.assertEqual(route.pattern, "/")

    def test_route_returns_app_for_chaining(self):
        """Test that route returns the app for method chaining."""
        code = """
        (let [app (web-app)
              result (route app "GET" "/" (fn [request] {:status 200 :body "Hello"}))]
          (equal? app result))
        """
        result = run_lispy_string(code, self.env)

        self.assertTrue(result)

    def test_route_method_chaining(self):
        """Test that route supports method chaining."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/" (fn [request] {:status 200 :body "Home"}))
          (route app "POST" "/users" (fn [request] {:status 201 :body "Created"}))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertIsInstance(result, WebApp)
        self.assertEqual(len(result.router.routes), 2)

    def test_route_with_parameters(self):
        """Test route with URL parameters."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/users/:id" (fn [request] {:status 200 :body "User"}))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertEqual(len(result.router.routes), 1)
        route = result.router.routes[0]
        self.assertEqual(route.pattern, "/users/:id")
        self.assertEqual(route.param_names, ["id"])

    def test_route_multiple_parameters(self):
        """Test route with multiple URL parameters."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/users/:id/posts/:post_id" 
                 (fn [request] {:status 200 :body "Post"}))
          app)
        """
        result = run_lispy_string(code, self.env)

        route = result.router.routes[0]
        self.assertEqual(route.pattern, "/users/:id/posts/:post_id")
        self.assertEqual(route.param_names, ["id", "post_id"])

    def test_route_method_case_insensitive(self):
        """Test that HTTP methods are normalized to uppercase."""
        code = """
        (let [app (web-app)]
          (route app "get" "/" (fn [request] {:status 200 :body "Hello"}))
          app)
        """
        result = run_lispy_string(code, self.env)

        route = result.router.routes[0]
        self.assertEqual(route.method, "GET")

    def test_route_auto_adds_leading_slash(self):
        """Test that leading slash is added to pattern if missing."""
        code = """
        (let [app (web-app)]
          (route app "GET" "home" (fn [request] {:status 200 :body "Hello"}))
          app)
        """
        result = run_lispy_string(code, self.env)

        route = result.router.routes[0]
        self.assertEqual(route.pattern, "/home")

    def test_route_various_http_methods(self):
        """Test various HTTP methods."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/get" (fn [request] {:status 200 :body "GET"}))
          (route app "POST" "/post" (fn [request] {:status 200 :body "POST"}))
          (route app "PUT" "/put" (fn [request] {:status 200 :body "PUT"}))
          (route app "DELETE" "/delete" (fn [request] {:status 200 :body "DELETE"}))
          (route app "PATCH" "/patch" (fn [request] {:status 200 :body "PATCH"}))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertEqual(len(result.router.routes), 5)
        methods = [route.method for route in result.router.routes]
        self.assertEqual(methods, ["GET", "POST", "PUT", "DELETE", "PATCH"])

    def test_route_argument_validation(self):
        """Test route argument validation."""
        # Test wrong number of arguments
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(route)", self.env)
        self.assertIn("expects 4 arguments", str(context.exception))

        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(route (web-app))", self.env)
        self.assertIn("expects 4 arguments", str(context.exception))

        # Test invalid app argument
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(route "not-an-app" "GET" "/" (fn [req] {}))', self.env)
        self.assertIn("must be a web application", str(context.exception))

        # Test invalid method argument
        code = """
        (let [app (web-app)]
          (route app 123 "/" (fn [req] {})))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("method must be a string", str(context.exception))

        # Test empty method
        code = """
        (let [app (web-app)]
          (route app "" "/" (fn [req] {})))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("method cannot be empty", str(context.exception))

        # Test invalid pattern argument
        code = """
        (let [app (web-app)]
          (route app "GET" 123 (fn [req] {})))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("pattern must be a string", str(context.exception))

        # Test empty pattern
        code = """
        (let [app (web-app)]
          (route app "GET" "" (fn [req] {})))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("pattern cannot be empty", str(context.exception))

        # Test invalid handler argument
        code = """
        (let [app (web-app)]
          (route app "GET" "/" "not-a-function"))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("handler must be a function", str(context.exception))

    def test_route_handler_arity_validation(self):
        """Test that route handlers must take exactly one argument."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/" (fn [] {})))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("must take 1 argument", str(context.exception))

        code = """
        (let [app (web-app)]
          (route app "GET" "/" (fn [req res] {})))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("must take 1 argument", str(context.exception))

    def test_route_documentation(self):
        """Test that route has documentation."""
        result = run_lispy_string("(doc route)", self.env)

        self.assertIsInstance(result, str)
        self.assertIn("route", result)
        self.assertIn("Adds an HTTP route", result)

    def test_route_complex_example(self):
        """Test a complex routing example."""
        code = """
        (let [app (web-app)]
          (route app "GET" "/" 
                 (fn [req] {:status 200 :body "Home Page"}))
          (route app "GET" "/users/:id" 
                 (fn [req] {:status 200 :body "User Profile"}))
          (route app "POST" "/api/users" 
                 (fn [req] {:status 201 :body "User Created"}))
          (route app "PUT" "/api/users/:id" 
                 (fn [req] {:status 200 :body "User Updated"}))
          (route app "DELETE" "/api/users/:id" 
                 (fn [req] {:status 204 :body ""}))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertEqual(len(result.router.routes), 5)

        # Check route patterns
        patterns = [route.pattern for route in result.router.routes]
        expected_patterns = [
            "/",
            "/users/:id",
            "/api/users",
            "/api/users/:id",
            "/api/users/:id",
        ]
        self.assertEqual(patterns, expected_patterns)

        # Check methods
        methods = [route.method for route in result.router.routes]
        expected_methods = ["GET", "GET", "POST", "PUT", "DELETE"]
        self.assertEqual(methods, expected_methods)


if __name__ == "__main__":
    unittest.main()
