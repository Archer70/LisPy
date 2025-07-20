"""
Tests for web-app function.
"""

import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.web.app import WebApp


class TestWebApp(unittest.TestCase):
    """Test web-app function."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_web_app_creation(self):
        """Test that web-app creates a WebApp instance."""
        result = run_lispy_string("(web-app)", self.env)

        self.assertIsInstance(result, WebApp)
        self.assertFalse(result.is_running)
        self.assertEqual(len(result.router.routes), 0)
        self.assertEqual(len(result.middleware_chain.middleware), 0)

    def test_web_app_no_arguments(self):
        """Test that web-app requires no arguments."""
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(web-app 123)", self.env)
        self.assertIn("expects 0 arguments", str(context.exception))

    def test_web_app_multiple_instances(self):
        """Test that multiple web-app calls create separate instances."""
        code = """
        (let [app1 (web-app)
              app2 (web-app)]
          (equal? app1 app2))
        """
        result = run_lispy_string(code, self.env)

        # Should be different instances
        self.assertFalse(result)

    def test_web_app_with_variable(self):
        """Test that web-app can be stored in a variable."""
        code = """
        (let [my-app (web-app)]
          my-app)
        """
        result = run_lispy_string(code, self.env)

        self.assertIsInstance(result, WebApp)

    def test_web_app_function_documentation(self):
        """Test that web-app has documentation."""
        # Access documentation through the doc function
        result = run_lispy_string("(doc web-app)", self.env)

        self.assertIsInstance(result, str)
        self.assertIn("web-app", result)
        self.assertIn("Creates a new web application", result)

    def test_web_app_in_thread_first(self):
        """Test that web-app can be used in thread-first expressions."""
        # This will be useful when we add more functions
        code = """
        (-> (web-app))
        """
        result = run_lispy_string(code, self.env)

        self.assertIsInstance(result, WebApp)


if __name__ == "__main__":
    unittest.main()
