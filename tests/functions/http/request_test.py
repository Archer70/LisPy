"""
Tests for generic HTTP request function.
"""

import time
import unittest
from unittest.mock import MagicMock, patch

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.types import LispyPromise, Symbol
from lispy.utils import run_lispy_string


class TestHttpRequest(unittest.TestCase):
    """Test generic HTTP request function."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_http_request_requires_arguments(self):
        """Test that http-request requires at least two arguments."""
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(http-request)", self.env)
        self.assertIn("expects 2-4 arguments", str(context.exception))

        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(http-request "GET")', self.env)
        self.assertIn("expects 2-4 arguments", str(context.exception))

        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(http-request "GET" "url" {} {} "extra")', self.env)
        self.assertIn("expects 2-4 arguments", str(context.exception))

    def test_http_request_method_validation(self):
        """Test HTTP method validation."""
        # Method must be string
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(
                '(await (http-request 123 "https://httpbin.org/get"))', self.env
            )
        self.assertIn("Method must be a string", str(context.exception))

        # Method cannot be empty
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(
                '(await (http-request "" "https://httpbin.org/get"))', self.env
            )
        self.assertIn("Method cannot be empty", str(context.exception))

    def test_http_request_url_validation(self):
        """Test URL validation."""
        # URL must be string
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-request "GET" 123))', self.env)
        self.assertIn("URL must be a string", str(context.exception))

        # Invalid URL format
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-request "GET" "invalid-url"))', self.env)
        self.assertIn("missing scheme", str(context.exception))

    def test_http_request_function_available(self):
        """Test that http-request function is available in global environment."""
        # Verify the function is properly registered
        self.assertIn("http-request", self.env.store)

        # Verify it can be called (will error due to insufficient args, but that's expected)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(http-request)", self.env)

    @patch("urllib.request.urlopen")
    def test_http_request_get_method(self, mock_urlopen):
        """Test GET method via generic request."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {"Content-Type": "application/json"}
        response_body = '{"method": "GET"}'
        mock_response.read.return_value = response_body.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make GET request and await result
        response = run_lispy_string(
            '(await (http-request "GET" "https://httpbin.org/get"))', self.env
        )

        # Verify response structure
        self.assertEqual(response[":status"], 200)
        self.assertTrue(response[":ok"])

        # Verify correct method was used
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, "GET")

    @patch("urllib.request.urlopen")
    def test_http_request_post_with_data(self, mock_urlopen):
        """Test POST method with JSON data."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 201
        mock_response.headers = {"Content-Type": "application/json"}
        response_body = '{"created": true}'
        mock_response.read.return_value = response_body.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make POST request with data
        response = run_lispy_string(
            '(await (http-request "POST" "https://httpbin.org/post" {:name "Alice" :email "alice@example.com"}))',
            self.env,
        )

        # Verify request details
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            request.get_header("Content-type"), "application/json; charset=utf-8"
        )

        # Verify data was encoded as JSON
        request_data = request.data.decode("utf-8")
        self.assertIn('"name": "Alice"', request_data)
        self.assertIn('"email": "alice@example.com"', request_data)

    @patch("urllib.request.urlopen")
    def test_http_request_case_insensitive_method(self, mock_urlopen):
        """Test that HTTP methods are case-insensitive."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {}
        mock_response.read.return_value = b"OK"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make request with lowercase method
        response = run_lispy_string(
            '(await (http-request "get" "https://httpbin.org/get"))', self.env
        )

        # Verify method was converted to uppercase
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, "GET")

    @patch("urllib.request.urlopen")
    def test_http_request_head_method(self, mock_urlopen):
        """Test HEAD method (no body expected)."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {"Content-Length": "1234"}
        mock_response.read.return_value = b""  # HEAD typically returns no body
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make HEAD request
        response = run_lispy_string(
            '(await (http-request "HEAD" "https://httpbin.org/get"))', self.env
        )
        self.assertEqual(response[":status"], 200)
        self.assertEqual(response[":body"], "")

        # Verify HEAD method was used
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, "HEAD")

    @patch("urllib.request.urlopen")
    def test_http_request_options_method(self, mock_urlopen):
        """Test OPTIONS method."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {"Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS"}
        mock_response.read.return_value = b""
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make OPTIONS request
        response = run_lispy_string(
            '(await (http-request "OPTIONS" "https://api.example.com/users"))', self.env
        )
        self.assertEqual(response[":status"], 200)
        self.assertIn("Allow", response[":headers"])

        # Verify OPTIONS method was used
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, "OPTIONS")

    @patch("urllib.request.urlopen")
    def test_http_request_patch_method(self, mock_urlopen):
        """Test PATCH method for partial updates."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {"Content-Type": "application/json"}
        response_body = '{"updated": true}'
        mock_response.read.return_value = response_body.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make PATCH request with partial data
        data = {Symbol("status"): "active"}
        response = run_lispy_string(
            '(await (http-request "PATCH" "https://api.example.com/users/123" {:status "active"}))',
            self.env,
        )

        # Verify PATCH method and data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, "PATCH")
        self.assertIsNotNone(request.data)  # PATCH should include body

        request_data = request.data.decode("utf-8")
        self.assertIn('"status": "active"', request_data)

    @patch("urllib.request.urlopen")
    def test_http_request_custom_method(self, mock_urlopen):
        """Test custom/non-standard HTTP method."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {}
        mock_response.read.return_value = b"Custom method handled"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make request with custom method
        response = run_lispy_string(
            '(await (http-request "PURGE" "https://api.example.com/cache"))', self.env
        )

        # Verify custom method was used
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, "PURGE")

    @patch("urllib.request.urlopen")
    def test_http_request_get_with_data_ignored(self, mock_urlopen):
        """Test that data is ignored for GET requests."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {}
        mock_response.read.return_value = b"OK"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make GET request with data (should be ignored)
        response = run_lispy_string(
            '(await (http-request "GET" "https://httpbin.org/get" {:should "be ignored"}))',
            self.env,
        )

        # Verify no body was sent (data ignored for GET)
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, "GET")
        self.assertIsNone(request.data)

    @patch("urllib.request.urlopen")
    def test_http_request_with_headers(self, mock_urlopen):
        """Test request with custom headers."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {}
        mock_response.read.return_value = b"OK"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make request with headers
        response = run_lispy_string(
            '(await (http-request "GET" "https://api.example.com/data" nil {:authorization "Bearer token123" :x-custom-header "custom-value"}))',
            self.env,
        )

        # Verify headers were sent
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        headers_dict = dict(request.headers)
        self.assertIn("Authorization", headers_dict)
        self.assertEqual(headers_dict["Authorization"], "Bearer token123")
        self.assertIn("X-custom-header", headers_dict)
        self.assertEqual(headers_dict["X-custom-header"], "custom-value")

    @patch("urllib.request.urlopen")
    def test_http_request_error_response(self, mock_urlopen):
        """Test HTTP error responses."""
        from urllib.error import HTTPError

        # Create mock error response
        error_body = '{"error": "Not Found"}'
        mock_error = HTTPError(
            "https://api.example.com/missing", 404, "Not Found", {}, None
        )
        mock_error.read = MagicMock(return_value=error_body.encode("utf-8"))
        mock_error.headers = {}
        mock_urlopen.side_effect = mock_error

        # Make request and await result
        response = run_lispy_string(
            '(await (http-request "GET" "https://api.example.com/missing"))', self.env
        )

        # Verify error response
        self.assertEqual(response[":status"], 404)
        self.assertFalse(response[":ok"])
        self.assertEqual(response[":body"], error_body)

    @patch("urllib.request.urlopen")
    def test_http_request_network_error(self, mock_urlopen):
        """Test network connection errors."""
        from urllib.error import URLError

        # Mock network error
        mock_urlopen.side_effect = URLError("Connection refused")

        # Make request - should cause error
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(
                '(await (http-request "GET" "https://unreachable.example.com"))',
                self.env,
            )

        # Should catch network error
        self.assertIn("NetworkError", str(context.exception))


if __name__ == "__main__":
    unittest.main()
