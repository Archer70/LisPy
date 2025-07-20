import json
import threading
import time
import unittest
from unittest.mock import Mock, patch

from lispy.exceptions import LisPyError
from lispy.functions import create_global_env
from lispy.types import LispyList, LispyPromise, Symbol, Vector
from lispy.utils import run_lispy_string


class TestHTTPEnhancedDataTypes(unittest.TestCase):
    """Test enhanced data type support for HTTP functions."""

    def setUp(self):
        """Set up test environment."""
        self.env = create_global_env()
        self.test_url = "https://httpbin.dev/post"

    def create_mock_response(
        self, status=200, body='{"message": "success"}', headers=None
    ):
        """Create a mock HTTP response."""
        mock_response = Mock()
        mock_response.getcode.return_value = status
        mock_response.headers = headers or {"Content-Type": "application/json"}
        mock_response.read.return_value = body.encode("utf-8")
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        return mock_response

    @patch("urllib.request.urlopen")
    def test_post_vector_data(self, mock_urlopen):
        """Test POST request with Vector data sends JSON array."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" [1 2 3]))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"[1, 2, 3]")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_post_lispy_list_data(self, mock_urlopen):
        """Test POST request with LispyList data sends JSON array."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" (list 1 2 3)))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"[1, 2, 3]")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_post_python_list_data(self, mock_urlopen):
        """Test POST request with Python list data sends JSON array."""
        # Note: Python lists need to be converted to LisPy lists in the context
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" [1 2 3]))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"[1, 2, 3]")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_post_number_data(self, mock_urlopen):
        """Test POST request with number data sends JSON."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" 42))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"42")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_post_float_data(self, mock_urlopen):
        """Test POST request with float data sends JSON."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" 3.14159))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"3.14159")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_post_boolean_true_data(self, mock_urlopen):
        """Test POST request with boolean True data sends JSON."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" true))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"true")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_post_boolean_false_data(self, mock_urlopen):
        """Test POST request with boolean False data sends JSON."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" false))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"false")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_post_none_data(self, mock_urlopen):
        """Test POST request with None data sends JSON null."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" nil))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"null")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_post_nested_data_with_symbols(self, mock_urlopen):
        """Test POST request with nested data containing symbols."""
        mock_urlopen.return_value = self.create_mock_response()

        lispy_code = """(await (http-post "https://httpbin.dev/post" 
                          {:user {:name "Alice" 
                                  :tags [:admin :user]}
                           :scores [100 95 87]}))"""
        response = run_lispy_string(lispy_code, self.env)

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]

        # Parse the JSON to verify structure
        sent_json = json.loads(request.data.decode("utf-8"))
        expected = {
            "user": {"name": "Alice", "tags": ["admin", "user"]},
            "scores": [100, 95, 87],
        }
        self.assertEqual(sent_json, expected)
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_put_enhanced_data_types(self, mock_urlopen):
        """Test PUT request with enhanced data types."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-put "https://httpbin.dev/post" [1 2 3]))', self.env
        )

        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"[1, 2, 3]")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_delete_enhanced_data_types(self, mock_urlopen):
        """Test DELETE request with enhanced data types."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-delete "https://httpbin.dev/post" 42))', self.env
        )

        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"42")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_generic_request_enhanced_data_types(self, mock_urlopen):
        """Test generic http-request with enhanced data types."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-request "POST" "https://httpbin.dev/post" true))', self.env
        )

        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"true")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_empty_list_data(self, mock_urlopen):
        """Test POST request with empty list sends empty JSON array."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" []))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"[]")
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_mixed_type_list(self, mock_urlopen):
        """Test POST request with mixed-type list."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" [1 "hello" true nil :test]))',
            self.env,
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]

        # Parse the JSON to verify structure
        sent_json = json.loads(request.data.decode("utf-8"))
        expected = [1, "hello", True, None, "test"]
        self.assertEqual(sent_json, expected)
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )

    @patch("urllib.request.urlopen")
    def test_backward_compatibility_string_data(self, mock_urlopen):
        """Test that string data still works as text/plain (backward compatibility)."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" "Hello World"))', self.env
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.data, b"Hello World")
        self.assertEqual(request.headers["Content-type"], "text/plain; charset=utf-8")

    @patch("urllib.request.urlopen")
    def test_backward_compatibility_dict_data(self, mock_urlopen):
        """Test that dictionary data still works as JSON (backward compatibility)."""
        mock_urlopen.return_value = self.create_mock_response()

        response = run_lispy_string(
            '(await (http-post "https://httpbin.dev/post" {:name "Alice" :age 30}))',
            self.env,
        )

        # Verify request was made with correct data
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]

        # Parse the JSON to verify structure
        sent_json = json.loads(request.data.decode("utf-8"))
        expected = {"name": "Alice", "age": 30}
        self.assertEqual(sent_json, expected)
        self.assertEqual(
            request.headers["Content-type"], "application/json; charset=utf-8"
        )


if __name__ == "__main__":
    unittest.main()
