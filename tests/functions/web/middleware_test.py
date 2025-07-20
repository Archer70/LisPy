"""
Tests for middleware function.
"""

import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.web.app import WebApp


class TestMiddleware(unittest.TestCase):
    """Test middleware function."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_middleware_before_basic(self):
        """Test basic before middleware registration."""
        code = """
        (let [app (web-app)]
          (middleware app "before" (fn [request] request))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertIsInstance(result, WebApp)
        self.assertEqual(len(result.middleware_chain.middleware), 1)

        middleware = result.middleware_chain.middleware[0]
        self.assertEqual(middleware.middleware_type, "before")

    def test_middleware_after_basic(self):
        """Test basic after middleware registration."""
        code = """
        (let [app (web-app)]
          (middleware app "after" (fn [request response] response))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertEqual(len(result.middleware_chain.middleware), 1)
        middleware = result.middleware_chain.middleware[0]
        self.assertEqual(middleware.middleware_type, "after")

    def test_middleware_returns_app_for_chaining(self):
        """Test that middleware returns the app for method chaining."""
        code = """
        (let [app (web-app)
              result (middleware app "before" (fn [request] request))]
          (equal? app result))
        """
        result = run_lispy_string(code, self.env)

        self.assertTrue(result)

    def test_middleware_method_chaining(self):
        """Test that middleware supports method chaining."""
        code = """
        (let [app (web-app)]
          (middleware app "before" (fn [request] request))
          (middleware app "after" (fn [request response] response))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertIsInstance(result, WebApp)
        self.assertEqual(len(result.middleware_chain.middleware), 2)

    def test_middleware_string_types(self):
        """Test middleware with string types instead of keywords."""
        code = """
        (let [app (web-app)]
          (middleware app "before" (fn [request] request))
          (middleware app "after" (fn [request response] response))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertEqual(len(result.middleware_chain.middleware), 2)
        self.assertEqual(
            result.middleware_chain.middleware[0].middleware_type, "before"
        )
        self.assertEqual(result.middleware_chain.middleware[1].middleware_type, "after")

    def test_middleware_multiple_before(self):
        """Test multiple before middleware registration."""
        code = """
        (let [app (web-app)]
          (middleware app "before" (fn [req] req))
          (middleware app "before" (fn [req] req))
          (middleware app "before" (fn [req] req))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertEqual(len(result.middleware_chain.middleware), 3)
        for mw in result.middleware_chain.middleware:
            self.assertEqual(mw.middleware_type, "before")

    def test_middleware_multiple_after(self):
        """Test multiple after middleware registration."""
        code = """
        (let [app (web-app)]
          (middleware app "after" (fn [req res] res))
          (middleware app "after" (fn [req res] res))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertEqual(len(result.middleware_chain.middleware), 2)
        for mw in result.middleware_chain.middleware:
            self.assertEqual(mw.middleware_type, "after")

    def test_middleware_mixed_types(self):
        """Test mixing before and after middleware."""
        code = """
        (let [app (web-app)]
          (middleware app "before" (fn [req] req))
          (middleware app "after" (fn [req res] res))
          (middleware app "before" (fn [req] req))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertEqual(len(result.middleware_chain.middleware), 3)
        types = [mw.middleware_type for mw in result.middleware_chain.middleware]
        self.assertEqual(types, ["before", "after", "before"])

    def test_middleware_argument_validation(self):
        """Test middleware argument validation."""
        # Test wrong number of arguments
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(middleware)", self.env)
        self.assertIn("expects 3 arguments", str(context.exception))

        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(middleware (web-app))", self.env)
        self.assertIn("expects 3 arguments", str(context.exception))

        # Test invalid app argument
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(
                '(middleware "not-an-app" "before" (fn [req] req))', self.env
            )
        self.assertIn("must be a web application", str(context.exception))

        # Test invalid type argument
        code = """
        (let [app (web-app)]
          (middleware app 123 (fn [req] req)))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("must be :before, :after", str(context.exception))

        # Test invalid type value
        code = """
        (let [app (web-app)]
          (middleware app "invalid" (fn [req] req)))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("must be 'before' or 'after'", str(context.exception))

        # Test invalid handler argument
        code = """
        (let [app (web-app)]
          (middleware app "before" "not-a-function"))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("handler must be a function", str(context.exception))

    def test_middleware_before_arity_validation(self):
        """Test that before middleware must take exactly one argument."""
        code = """
        (let [app (web-app)]
          (middleware app "before" (fn [] nil)))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("must take 1 argument (request)", str(context.exception))

        code = """
        (let [app (web-app)]
          (middleware app "before" (fn [req res] req)))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn("must take 1 argument (request)", str(context.exception))

    def test_middleware_after_arity_validation(self):
        """Test that after middleware must take exactly two arguments."""
        code = """
        (let [app (web-app)]
          (middleware app "after" (fn [req] req)))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn(
            "must take 2 arguments (request response)", str(context.exception)
        )

        code = """
        (let [app (web-app)]
          (middleware app "after" (fn [req res extra] res)))
        """
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(code, self.env)
        self.assertIn(
            "must take 2 arguments (request response)", str(context.exception)
        )

    def test_middleware_with_routes(self):
        """Test middleware combined with routes."""
        code = """
        (let [app (web-app)]
          (middleware app "before" (fn [req] req))
          (route app "GET" "/" (fn [req] {:status 200 :body "Hello"}))
          (middleware app "after" (fn [req res] res))
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertEqual(len(result.middleware_chain.middleware), 2)
        self.assertEqual(len(result.router.routes), 1)

    def test_middleware_documentation(self):
        """Test that middleware has documentation."""
        result = run_lispy_string("(doc middleware)", self.env)

        self.assertIsInstance(result, str)
        self.assertIn("middleware", result)
        self.assertIn("Adds middleware", result)

    def test_middleware_complex_example(self):
        """Test a complex middleware example."""
        code = """
        (let [app (web-app)]
          ; Add authentication middleware
          (middleware app "before" 
                      (fn [request]
                        ; Simulate adding auth info
                        (assoc request :authenticated true)))
          
          ; Add logging middleware
          (middleware app "before"
                      (fn [request]
                        ; Just pass through the request
                        request))
          
          ; Add CORS headers middleware
          (middleware app "after"
                      (fn [request response]
                        ; Simulate adding CORS headers
                        (assoc response :cors-added true)))
          
          ; Add response logging middleware
          (middleware app "after"
                      (fn [request response]
                        ; Just pass through the response
                        response))
          
          app)
        """
        result = run_lispy_string(code, self.env)

        self.assertEqual(len(result.middleware_chain.middleware), 4)

        # Check middleware types in order
        types = [mw.middleware_type for mw in result.middleware_chain.middleware]
        expected_types = ["before", "before", "after", "after"]
        self.assertEqual(types, expected_types)


if __name__ == "__main__":
    unittest.main()
