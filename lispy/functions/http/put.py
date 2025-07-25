"""
HTTP PUT function for LisPy.
"""

import json
import threading
import urllib.error
import urllib.parse
import urllib.request

from lispy.exceptions import ArityError, EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import LispyPromise, Symbol

from .utils import (HTTPError, create_response_map, normalize_headers,
                    validate_url_with_message)


@lispy_function("http-put", web_safe=False, reason="Network access")
def http_put(args, env):
    """
    Make an HTTP PUT request and return a promise.

    Args:
        args: List containing URL, optional data, and optional headers
        env: Environment (not used)

    Returns:
        LispyPromise that resolves to response map
    """
    # Only validate argument count immediately
    if not (1 <= len(args) <= 3):
        raise EvaluationError("http-put expects 1-3 arguments (url [data] [headers])")

    # Create promise and execute request in background thread
    promise = LispyPromise()

    def http_request_handler():
        """Execute HTTP request in background thread."""
        try:
            url = args[0]
            data = args[1] if len(args) > 1 else None
            headers = args[2] if len(args) > 2 else {}

            # Validate URL (inside promise so errors become rejections)
            if not isinstance(url, str):
                promise.reject(
                    HTTPError(f"URL must be a string, got {type(url).__name__}")
                )
                return

            if not url.strip():
                promise.reject(HTTPError("URL cannot be empty"))
                return

            is_valid, error_message = validate_url_with_message(url)
            if not is_valid:
                promise.reject(HTTPError(error_message))
                return

            # Validate and normalize headers
            if not isinstance(headers, dict):
                promise.reject(
                    HTTPError(f"Headers must be a map, got {type(headers).__name__}")
                )
                return

            normalized_headers = normalize_headers(headers)

            # Prepare request body
            request_body = None
            if len(args) > 1 and not (data is None and len(args) > 2):
                # Include body if:
                # - Data argument is provided AND
                # - It's not None used as placeholder for headers (None + headers present)
                request_body, content_type = _encode_request_data(data)
                # Set Content-Type if not already specified
                if "content-type" not in [k.lower() for k in normalized_headers.keys()]:
                    normalized_headers["Content-Type"] = content_type

            # Add default User-Agent if not provided
            if "user-agent" not in [k.lower() for k in normalized_headers.keys()]:
                normalized_headers["User-agent"] = "LisPy-HTTP/1.0"

            # Create request
            request = urllib.request.Request(
                url, data=request_body, headers=normalized_headers, method="PUT"
            )

            # Make the request with timeout
            with urllib.request.urlopen(request, timeout=30) as response:
                status = response.getcode()
                response_headers = dict(response.headers)
                body = response.read().decode("utf-8")

                # Create standardized response
                result = create_response_map(status, response_headers, body, url)
                promise.resolve(result)

        except urllib.error.HTTPError as e:
            # HTTP errors (4xx, 5xx)
            try:
                error_body = e.read().decode("utf-8") if e.fp else ""
                error_headers = dict(e.headers) if e.headers else {}
                result = create_response_map(e.code, error_headers, error_body, url)
                promise.resolve(result)
            except Exception:
                promise.reject(HTTPError(f"HTTP {e.code}: {e.reason}"))
        except urllib.error.URLError as e:
            # Network errors
            promise.reject(HTTPError(f"NetworkError: {e.reason}"))
        except Exception as e:
            # Other errors
            promise.reject(HTTPError(f"Request failed: {str(e)}"))

    # Start request in background thread
    request_thread = threading.Thread(target=http_request_handler, daemon=True)
    request_thread.start()

    return promise


def _encode_request_data(data):
    """
    Encode data for HTTP request body.

    Args:
        data: Data to encode (dict, list, string, number, boolean, etc.)

    Returns:
        tuple: (encoded_bytes, content_type)
    """
    from lispy.types import LispyList, Vector

    if isinstance(data, str):
        # Raw string data
        return data.encode("utf-8"), "text/plain; charset=utf-8"

    elif isinstance(data, dict):
        # Encode maps as JSON with Symbol key conversion
        try:
            # Convert LisPy symbols to strings for JSON
            json_data = {}
            for key, value in data.items():
                str_key = key.name if isinstance(key, Symbol) else str(key)
                if str_key.startswith(":"):
                    str_key = str_key[1:]
                json_data[str_key] = _convert_for_json(value)

            json_string = json.dumps(json_data)
            return json_string.encode("utf-8"), "application/json; charset=utf-8"
        except (TypeError, ValueError):
            # Fall back to form encoding
            form_data = {}
            for key, value in data.items():
                str_key = key.name if isinstance(key, Symbol) else str(key)
                if str_key.startswith(":"):
                    str_key = str_key[1:]
                form_data[str_key] = str(value)

            encoded = urllib.parse.urlencode(form_data)
            return encoded.encode("utf-8"), "application/x-www-form-urlencoded"

    elif isinstance(data, (list, Vector, LispyList)):
        # Encode lists/vectors as JSON arrays
        try:
            json_array = [_convert_for_json(item) for item in data]
            json_string = json.dumps(json_array)
            return json_string.encode("utf-8"), "application/json; charset=utf-8"
        except (TypeError, ValueError):
            # Fall back to string representation
            return str(data).encode("utf-8"), "text/plain; charset=utf-8"

    elif isinstance(data, (int, float, bool)) or data is None:
        # Encode primitives as JSON
        try:
            json_string = json.dumps(data)
            return json_string.encode("utf-8"), "application/json; charset=utf-8"
        except (TypeError, ValueError):
            # Fall back to string representation
            return str(data).encode("utf-8"), "text/plain; charset=utf-8"

    else:
        # Convert other types to string
        return str(data).encode("utf-8"), "text/plain; charset=utf-8"


def _convert_for_json(value):
    """
    Convert LisPy values to JSON-compatible Python values.

    Args:
        value: Value to convert

    Returns:
        JSON-compatible value
    """
    from lispy.types import LispyList, Vector

    if isinstance(value, Symbol):
        # Convert symbols to strings (removing leading colon if present)
        symbol_name = value.name
        return symbol_name[1:] if symbol_name.startswith(":") else symbol_name
    elif isinstance(value, (list, Vector, LispyList)):
        # Recursively convert list elements
        return [_convert_for_json(item) for item in value]
    elif isinstance(value, dict):
        # Recursively convert dictionary values and normalize keys
        result = {}
        for k, v in value.items():
            str_key = k.name if isinstance(k, Symbol) else str(k)
            if str_key.startswith(":"):
                str_key = str_key[1:]
            result[str_key] = _convert_for_json(v)
        return result
    else:
        # Primitives (int, float, bool, None, str) are already JSON-compatible
        return value


# Documentation
@lispy_documentation("http-put")
def http_put_documentation():
    return """
Function: http-put
Arguments: (url [data] [headers])
Description: Make an HTTP PUT request and return a promise.

Arguments:
  url     - String URL to request (must be http:// or https://)
  data    - Optional data to send in request body (map, string, etc.)
  headers - Optional map of headers to send


Examples:
  ; Simple PUT request
  (http-put "https://httpbin.org/put")
  
  ; PUT with JSON data (resource update)
  (http-put "https://api.example.com/users/123"
            {:name "Alice Updated" :age 31})
  
  ; PUT with custom headers
  (http-put "https://api.example.com/resource/456"
            {:status "active" :priority "high"}
            {:authorization "Bearer token123"
             :content-type "application/json"})
  
  ; PUT with string data
  (http-put "https://api.example.com/content/789"
            "Updated content")

Notes:
  - Requests timeout after 30 seconds
  - Both successful and error responses resolve the promise
  - Network errors reject the promise
  - JSON responses are automatically parsed to :json key
  - Headers support LisPy keyword syntax (:authorization)
  - PUT is typically used for updating/replacing resources
"""
