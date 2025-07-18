"""
Tests for HTTP DELETE function.
"""

import unittest
from unittest.mock import patch, MagicMock
import time
from lispy.functions import create_global_env
from lispy.types import LispyPromise, Symbol
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class TestHttpDelete(unittest.TestCase):
    """Test HTTP DELETE function."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()



    def test_http_delete_requires_arguments(self):
        """Test that http-delete requires at least one argument."""
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(http-delete)", self.env)
        self.assertIn("expects 1-3 arguments", str(context.exception))
        
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(http-delete "url" {} {} "extra")', self.env)
        self.assertIn("expects 1-3 arguments", str(context.exception))

    def test_http_delete_url_validation(self):
        """Test URL validation."""
        # Invalid URL
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-delete 123))', self.env)
        self.assertIn("URL must be a string", str(context.exception))

    def test_http_delete_function_available(self):
        """Test that http-delete function is available in global environment."""
        # Verify the function is properly registered
        self.assertIn("http-delete", self.env.store)
        
        # Verify it can be called (will error due to no args, but that's expected)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(http-delete)", self.env)

    @patch('urllib.request.urlopen')
    def test_http_delete_successful_request(self, mock_urlopen):
        """Test successful HTTP DELETE request."""
        # Mock response (common for DELETE to return 204 No Content)
        mock_response = MagicMock()
        mock_response.getcode.return_value = 204
        mock_response.headers = {}
        mock_response.read.return_value = b''
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Make request and await result
        response = run_lispy_string('(await (http-delete "https://httpbin.org/delete"))', self.env)
        
        # Verify response structure
        self.assertEqual(response[':status'], 204)
        self.assertEqual(response[':body'], '')
        self.assertTrue(response[':ok'])
        
        # Verify it used DELETE method
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, 'DELETE')

    @patch('urllib.request.urlopen')
    def test_http_delete_without_body(self, mock_urlopen):
        """Test HTTP DELETE request without body (typical use case)."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        response_body = '{"deleted": true, "id": 123}'
        mock_response.read.return_value = response_body.encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Make request without data
        response = run_lispy_string('(await (http-delete "https://api.example.com/users/123"))', self.env)
        
        # Verify request method and no body
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, 'DELETE')
        self.assertIsNone(request.data)  # No body for typical DELETE

    @patch('urllib.request.urlopen')
    def test_http_delete_with_data(self, mock_urlopen):
        """Test HTTP DELETE request with data (less common but supported)."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        response_body = '{"deleted_count": 3}'
        mock_response.read.return_value = response_body.encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Make request with data (bulk delete scenario)
        response = run_lispy_string('(await (http-delete "https://api.example.com/bulk-delete" {:ids [1 2 3]}))', self.env)
        
        # Verify request method and content type
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, 'DELETE')
        self.assertEqual(request.get_header('Content-type'), 'application/json; charset=utf-8')
        
        # Verify the request body contains JSON
        request_data = request.data.decode('utf-8')
        self.assertIn('"ids": [1, 2, 3]', request_data)

    @patch('urllib.request.urlopen')
    def test_http_delete_with_headers(self, mock_urlopen):
        """Test HTTP DELETE request with headers."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {}
        mock_response.read.return_value = b'OK'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Make request with headers (no body)
        response = run_lispy_string('(await (http-delete "https://api.example.com/resource/456" nil {:authorization "Bearer token123"}))', self.env)
        
        # Verify headers were sent
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        headers_dict = dict(request.headers)
        self.assertIn('Authorization', headers_dict)
        self.assertEqual(headers_dict['Authorization'], 'Bearer token123')
        self.assertIsNone(request.data)  # Explicitly no body

    @patch('urllib.request.urlopen')
    def test_http_delete_error_responses(self, mock_urlopen):
        """Test HTTP error responses for DELETE."""
        from urllib.error import HTTPError
        
        # Test 404 Not Found
        error_body = '{"error": "Resource not found"}'
        mock_error = HTTPError("https://api.example.com/users/999", 404, "Not Found", {}, None)
        mock_error.read = MagicMock(return_value=error_body.encode('utf-8'))
        mock_error.headers = {}
        mock_urlopen.side_effect = mock_error
        
        # Make request and await result
        response = run_lispy_string('(await (http-delete "https://api.example.com/users/999"))', self.env)
        
        # Verify error response
        self.assertEqual(response[':status'], 404)
        self.assertFalse(response[':ok'])
        self.assertEqual(response[':body'], error_body)

    @patch('urllib.request.urlopen')
    def test_http_delete_network_error(self, mock_urlopen):
        """Test network connection errors."""
        from urllib.error import URLError
        
        # Mock network error
        mock_urlopen.side_effect = URLError("Connection refused")
        
        # Make request - should cause error
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-delete "https://unreachable.example.com/resource"))', self.env)
        
        # Should catch network error
        self.assertIn("NetworkError", str(context.exception))


if __name__ == '__main__':
    unittest.main() 