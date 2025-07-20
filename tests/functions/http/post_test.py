"""
Tests for HTTP POST function.
"""

import time
import unittest
from unittest.mock import MagicMock, patch

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.types import LispyPromise, Symbol
from lispy.utils import run_lispy_string


class TestHttpPost(unittest.TestCase):
    """Test HTTP POST function."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()

    def test_http_post_requires_arguments(self):
        """Test that http-post requires at least one argument."""
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(http-post)", self.env)
        self.assertIn("expects 1-3 arguments", str(context.exception))

        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(http-post "url" {} {} "extra")', self.env)
        self.assertIn("expects 1-3 arguments", str(context.exception))

    def test_http_post_url_must_be_string(self):
        """Test that URL must be a string."""
        # Integer URL should cause error
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(await (http-post 123))", self.env)
        self.assertIn("URL must be a string", str(context.exception))

        # None URL should cause error
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(await (http-post nil))", self.env)
        self.assertIn("URL must be a string", str(context.exception))

    def test_http_post_validates_url_format(self):
        """Test URL validation."""
        # Empty URL
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-post ""))', self.env)
        self.assertIn("URL cannot be empty", str(context.exception))

        # Invalid URL - no scheme
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-post "example.com"))', self.env)
        self.assertIn("missing scheme", str(context.exception))

        # Unsupported scheme
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-post "ftp://example.com"))', self.env)
        self.assertIn("Unsupported URL scheme", str(context.exception))

    def test_http_post_function_available(self):
        """Test that http-post function is available in global environment."""
        # Verify the function is properly registered
        self.assertIn("http-post", self.env.store)

        # Verify it can be called (will error due to no args, but that's expected)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(http-post)", self.env)

    @patch("urllib.request.urlopen")
    def test_http_post_successful_request(self, mock_urlopen):
        """Test successful HTTP POST request."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 201
        mock_response.headers = {"Content-Type": "application/json", "Server": "test"}
        response_body = '{"id": 123, "message": "Created"}'
        mock_response.read.return_value = response_body.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make request and await result
        response = run_lispy_string(
            '(await (http-post "https://httpbin.org/post"))', self.env
        )

        # Verify response structure
        self.assertEqual(response[":status"], 201)
        self.assertEqual(response[":body"], response_body)
        self.assertEqual(response[":url"], "https://httpbin.org/post")
        self.assertTrue(response[":ok"])
        self.assertEqual(response[":json"]["message"], "Created")

    @patch("urllib.request.urlopen")
    def test_http_post_with_json_data(self, mock_urlopen):
        """Test HTTP POST request with JSON data."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {"Content-Type": "application/json"}
        response_body = '{"success": true}'
        mock_response.read.return_value = response_body.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make request with JSON data
        data = {Symbol("name"): "Alice", Symbol("age"): 30}
        response = run_lispy_string(
            '(await (http-post "https://httpbin.org/post" {:name "Alice" :age 30}))',
            self.env,
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            request.get_header("Content-type"), "application/json; charset=utf-8"
        )

        # Verify the request body contains JSON
        request_data = request.data.decode("utf-8")
        self.assertIn('"name": "Alice"', request_data)
        self.assertIn('"age": 30', request_data)

    @patch("urllib.request.urlopen")
    def test_http_post_with_string_data(self, mock_urlopen):
        """Test HTTP POST request with string data."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {"Content-Type": "text/plain"}
        response_body = "Data received"
        mock_response.read.return_value = response_body.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make request with string data
        response = run_lispy_string(
            '(await (http-post "https://httpbin.org/post" "Hello World"))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            request.get_header("Content-type"), "text/plain; charset=utf-8"
        )
        self.assertEqual(request.data, b"Hello World")

    @patch("urllib.request.urlopen")
    def test_http_post_with_headers(self, mock_urlopen):
        """Test HTTP POST request with custom headers."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {"Content-Type": "application/json"}
        response_body = '{"success": true}'
        mock_response.read.return_value = response_body.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Make request with headers
        lispy_code = """
        (await (http-post "https://httpbin.org/post" nil 
                         {:authorization "Bearer token123" 
                          :accept "application/json"}))
        """
        response = run_lispy_string(lispy_code, self.env)

        # Verify headers were sent
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        headers_dict = dict(request.headers)
        self.assertIn("Authorization", headers_dict)
        self.assertEqual(headers_dict["Authorization"], "Bearer token123")
        self.assertIn("Accept", headers_dict)
        self.assertEqual(headers_dict["Accept"], "application/json")
        self.assertIn("User-agent", headers_dict)

    @patch("urllib.request.urlopen")
    def test_http_post_http_error_response(self, mock_urlopen):
        """Test HTTP error responses (4xx, 5xx)."""
        from urllib.error import HTTPError

        # Create mock error response
        error_body = '{"error": "Bad Request"}'
        error_headers = {"Content-Type": "application/json"}
        mock_error = HTTPError(
            "https://httpbin.org/post", 400, "Bad Request", error_headers, None
        )
        mock_error.read = MagicMock(return_value=error_body.encode("utf-8"))
        mock_error.headers = error_headers
        mock_urlopen.side_effect = mock_error

        # Make request and await result
        response = run_lispy_string(
            '(await (http-post "https://httpbin.org/post"))', self.env
        )

        # Verify error response
        self.assertEqual(response[":status"], 400)
        self.assertEqual(response[":body"], error_body)
        self.assertFalse(response[":ok"])

    @patch("urllib.request.urlopen")
    def test_http_post_network_error(self, mock_urlopen):
        """Test network connection errors."""
        from urllib.error import URLError

        # Mock network error
        mock_urlopen.side_effect = URLError("Connection refused")

        # Make request - should cause error
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string(
                '(await (http-post "https://unreachable.example.com"))', self.env
            )

        # Should catch network error
        self.assertIn("NetworkError", str(context.exception))


if __name__ == "__main__":
    unittest.main()
