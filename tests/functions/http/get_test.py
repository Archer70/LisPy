"""Tests for HTTP GET function"""

import unittest
import time
import json
from unittest.mock import patch, MagicMock, mock_open
from urllib.error import HTTPError, URLError
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, Symbol
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class MockHTTPResponse:
    """Mock HTTP response object for testing."""
    
    def __init__(self, body, status_code=200, headers=None):
        self.body = body.encode('utf-8') if isinstance(body, str) else body
        self.status_code = status_code
        self.headers = headers or {}
        
    def read(self):
        return self.body
        
    def getcode(self):
        return self.status_code
        
    def __enter__(self):
        return self
        
    def __exit__(self, *args):
        pass


class TestHttpGet(unittest.TestCase):
    """Test cases for HTTP GET function."""
    
    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()
    

    
    def test_http_get_requires_arguments(self):
        """Test that http-get requires at least one argument."""
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string("(http-get)", self.env)
        self.assertIn("expects 1 or 2 arguments", str(context.exception))
        
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(http-get "url" {} "extra")', self.env)
        self.assertIn("expects 1 or 2 arguments", str(context.exception))
    
    def test_http_get_url_must_be_string(self):
        """Test that URL must be a string."""
        # Integer URL should cause error
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-get 123))', self.env)
        self.assertIn("URL must be a string", str(context.exception))
        
        # None URL should cause error
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-get nil))', self.env)
        self.assertIn("URL must be a string", str(context.exception))
    
    def test_http_get_validates_url_format(self):
        """Test URL validation."""
        # Empty URL
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-get ""))', self.env)
        self.assertIn("URL cannot be empty", str(context.exception))
        
        # Invalid URL - no scheme
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-get "example.com"))', self.env)
        self.assertIn("missing scheme", str(context.exception))
        
        # Unsupported scheme
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-get "ftp://example.com"))', self.env)
        self.assertIn("Unsupported URL scheme", str(context.exception))
    
    @patch('urllib.request.urlopen')
    def test_http_get_successful_request(self, mock_urlopen):
        """Test successful HTTP GET request."""
        # Mock response
        response_body = '{"message": "Hello, World!"}'
        mock_response = MockHTTPResponse(response_body, 200, {
            'content-type': 'application/json',
            'server': 'test-server'
        })
        mock_urlopen.return_value = mock_response
        
        # Make request and await result
        response = run_lispy_string('(await (http-get "https://api.example.com/test"))', self.env)
        
        # Verify response format
        self.assertEqual(response[':status'], 200)
        self.assertEqual(response[':body'], response_body)
        self.assertEqual(response[':url'], "https://api.example.com/test")
        self.assertTrue(response[':ok'])
        
        # Check headers
        self.assertIn('content-type', response[':headers'])
        self.assertEqual(response[':headers']['content-type'], 'application/json')
        
        # Check JSON parsing
        self.assertIn(':json', response)
        self.assertEqual(response[':json']['message'], "Hello, World!")
    
    @patch('urllib.request.urlopen')
    def test_http_get_with_headers(self, mock_urlopen):
        """Test HTTP GET request with custom headers."""
        mock_response = MockHTTPResponse('OK', 200)
        mock_urlopen.return_value = mock_response
        
        # Request with headers
        lispy_code = '''
        (await (http-get "https://api.example.com/secure" 
                        {:authorization "Bearer token123" 
                         :accept "application/json"}))
        '''
        response = run_lispy_string(lispy_code, self.env)
        
        # Check that request was made
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        
        # Verify headers were added (case-insensitive)
        headers_dict = dict(request.headers)
        self.assertIn('Authorization', headers_dict)
        self.assertIn('Accept', headers_dict)
        self.assertEqual(headers_dict['Authorization'], 'Bearer token123')
        
        # Verify User-Agent was added
        self.assertIn('User-agent', headers_dict)
        self.assertEqual(headers_dict['User-agent'], 'LisPy-HTTP/1.0')
    
    @patch('urllib.request.urlopen')
    def test_http_get_http_error_response(self, mock_urlopen):
        """Test HTTP error responses (4xx, 5xx)."""
        # Mock 404 error
        error_body = '{"error": "Not Found"}'
        error = HTTPError(url="https://api.example.com/missing", code=404, msg="Not Found", 
                         hdrs={'content-type': 'application/json'}, fp=None)
        error.read = lambda: error_body.encode('utf-8')
        error.headers = {'content-type': 'application/json'}
        mock_urlopen.side_effect = error
        
        # Make request and await result
        response = run_lispy_string('(await (http-get "https://api.example.com/missing"))', self.env)
        
        # Check error response format
        self.assertEqual(response[':status'], 404)
        self.assertEqual(response[':body'], error_body)
        self.assertFalse(response[':ok'])  # Status not in 200-299 range
        
        # Check JSON parsing of error response
        self.assertIn(':json', response)
        self.assertEqual(response[':json']['error'], "Not Found")
    
    @patch('urllib.request.urlopen')
    def test_http_get_network_error(self, mock_urlopen):
        """Test network connection errors."""
        # Mock network error
        mock_urlopen.side_effect = URLError("Connection refused")
        
        # Make request - should cause error
        with self.assertRaises(EvaluationError) as context:
            run_lispy_string('(await (http-get "https://unreachable.example.com"))', self.env)
        
        # Should catch network error
        self.assertIn("NetworkError", str(context.exception))
        self.assertIn("Connection refused", str(context.exception))
    
    @patch('urllib.request.urlopen')
    def test_http_get_non_json_response(self, mock_urlopen):
        """Test handling of non-JSON responses."""
        response_body = "<html><body>Hello, World!</body></html>"
        mock_response = MockHTTPResponse(response_body, 200, {
            'content-type': 'text/html'
        })
        mock_urlopen.return_value = mock_response
        
        # Make request and await result
        response = run_lispy_string('(await (http-get "https://example.com"))', self.env)
        
        # Should have body but no JSON
        self.assertEqual(response[':body'], response_body)
        self.assertNotIn(':json', response)  # No JSON parsing for HTML
    
    @patch('urllib.request.urlopen')
    def test_http_get_invalid_json_response(self, mock_urlopen):
        """Test handling of invalid JSON with JSON content-type."""
        response_body = '{"invalid": json content}'  # Invalid JSON
        mock_response = MockHTTPResponse(response_body, 200, {
            'content-type': 'application/json'
        })
        mock_urlopen.return_value = mock_response
        
        # Make request and await result
        response = run_lispy_string('(await (http-get "https://api.example.com/invalid"))', self.env)
        
        # Should have body but no JSON (parsing failed gracefully)
        self.assertEqual(response[':body'], response_body)
        self.assertNotIn(':json', response)  # JSON parsing failed silently
    
    @patch('urllib.request.urlopen')
    def test_http_get_unicode_response(self, mock_urlopen):
        """Test handling of Unicode content."""
        response_body = '{"message": "Hello 世界! 🌍"}'
        mock_response = MockHTTPResponse(response_body, 200, {
            'content-type': 'application/json; charset=utf-8'
        })
        mock_urlopen.return_value = mock_response
        
        # Make request and await result
        response = run_lispy_string('(await (http-get "https://api.example.com/unicode"))', self.env)
        
        # Should handle Unicode correctly
        self.assertEqual(response[':body'], response_body)
        self.assertIn(':json', response)
        self.assertEqual(response[':json']['message'], "Hello 世界! 🌍")
    
    def test_http_get_function_available(self):
        """Test that http-get function is available in global environment."""
        # Verify the function is properly registered
        self.assertIn("http-get", self.env.store)
        
        # Verify it can be called (will error due to no args, but that's expected)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(http-get)", self.env)


if __name__ == '__main__':
    unittest.main() 