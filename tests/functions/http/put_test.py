"""
Tests for HTTP PUT function.
"""

import unittest
from unittest.mock import patch, MagicMock
import time
from lispy.functions import create_global_env
from lispy.types import LispyPromise, Symbol
from lispy.exceptions import EvaluationError
from lispy.utils import run_lispy_string


class TestHttpPut(unittest.TestCase):
    """Test HTTP PUT function."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()



    def test_http_put_requires_arguments(self):
        """Test that http-put requires at least one argument."""
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(http-put)", self.env)
        self.assertIn("expects 1-3 arguments", str(context.exception))
        
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(http-put "url" {} {} "extra")', self.env)
        self.assertIn("expects 1-3 arguments", str(context.exception))

    def test_http_put_url_validation(self):
        """Test URL validation."""
        # Invalid URL
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-put 123))', self.env)
        self.assertIn("URL must be a string", str(context.exception))

    def test_http_put_function_available(self):
        """Test that http-put function is available in global environment."""
        # Verify the function is properly registered
        self.assertIn("http-put", self.env.store)
        
        # Verify it can be called (will error due to no args, but that's expected)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(http-put)", self.env)

    @patch('urllib.request.urlopen')
    def test_http_put_successful_request(self, mock_urlopen):
        """Test successful HTTP PUT request."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        response_body = '{"id": 123, "message": "Updated"}'
        mock_response.read.return_value = response_body.encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Make request and await result
        response = run_lispy_string('(await (http-put "https://httpbin.org/put"))', self.env)
        
        # Verify response structure
        self.assertEqual(response[':status'], 200)
        self.assertEqual(response[':body'], response_body)
        self.assertTrue(response[':ok'])
        
        # Verify it used PUT method
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, 'PUT')

    @patch('urllib.request.urlopen')
    def test_http_put_with_data(self, mock_urlopen):
        """Test HTTP PUT request with data."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        response_body = '{"success": true}'
        mock_response.read.return_value = response_body.encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Make request with JSON data
        response = run_lispy_string('(await (http-put "https://httpbin.org/put" {:id 123 :name "Updated User"}))', self.env)
        
        # Verify request method and content type
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.method, 'PUT')
        self.assertEqual(request.get_header('Content-type'), 'application/json; charset=utf-8')
        
        # Verify the request body contains JSON
        request_data = request.data.decode('utf-8')
        self.assertIn('"id": 123', request_data)
        self.assertIn('"name": "Updated User"', request_data)

    @patch('urllib.request.urlopen')
    def test_http_put_with_headers(self, mock_urlopen):
        """Test HTTP PUT request with headers."""
        # Mock response
        mock_response = MagicMock()
        mock_response.getcode.return_value = 200
        mock_response.headers = {}
        mock_response.read.return_value = b'OK'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Make request with headers
        response = run_lispy_string('(await (http-put "https://httpbin.org/put" nil {:authorization "Bearer token123"}))', self.env)
        
        # Verify headers were sent
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        headers_dict = dict(request.headers)
        self.assertIn('Authorization', headers_dict)
        self.assertEqual(headers_dict['Authorization'], 'Bearer token123')

    @patch('urllib.request.urlopen')
    def test_http_put_error_response(self, mock_urlopen):
        """Test HTTP error responses."""
        from urllib.error import HTTPError
        
        # Create mock error response
        error_body = '{"error": "Not Found"}'
        mock_error = HTTPError("https://httpbin.org/put", 404, "Not Found", {}, None)
        mock_error.read = MagicMock(return_value=error_body.encode('utf-8'))
        mock_error.headers = {}
        mock_urlopen.side_effect = mock_error
        
        # Make request and await result
        response = run_lispy_string('(await (http-put "https://httpbin.org/put"))', self.env)
        
        # Verify error response
        self.assertEqual(response[':status'], 404)
        self.assertFalse(response[':ok'])


if __name__ == '__main__':
    unittest.main() 