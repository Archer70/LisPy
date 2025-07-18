"""
HTTP GET function for LisPy.
"""

import urllib.request
import urllib.error
import threading
from lispy.types import LispyPromise, Symbol
from lispy.exceptions import ArityError, EvaluationError
from .utils import validate_url_with_message, normalize_headers, create_response_map, HTTPError


def builtin_http_get(args, env):
    """
    Make an HTTP GET request and return a promise.
    
    Args:
        args: List containing URL and optional headers map
        env: Environment (not used)
        
    Returns:
        LispyPromise that resolves to response map
    """
    # Only validate argument count immediately
    if not (1 <= len(args) <= 2):
        raise EvaluationError("http-get expects 1 or 2 arguments (url [headers])")
    
    # Create promise and execute request in background thread
    promise = LispyPromise()
    
    def http_request_handler():
        """Execute HTTP request in background thread."""
        try:
            url = args[0]
            headers = args[1] if len(args) > 1 else {}
            
            # Validate URL (inside promise so errors become rejections)
            if not isinstance(url, str):
                promise.reject(HTTPError(f"URL must be a string, got {type(url).__name__}"))
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
                promise.reject(HTTPError(f"Headers must be a map, got {type(headers).__name__}"))
                return
            
            normalized_headers = normalize_headers(headers)
            
            # Add default User-Agent if not provided
            if 'user-agent' not in [k.lower() for k in normalized_headers.keys()]:
                normalized_headers['User-agent'] = 'LisPy-HTTP/1.0'
            
            # Create request
            request = urllib.request.Request(url, headers=normalized_headers)
            
            # Make the request with timeout
            with urllib.request.urlopen(request, timeout=30) as response:
                status = response.getcode()
                response_headers = dict(response.headers)
                body = response.read().decode('utf-8')
                
                # Create standardized response
                result = create_response_map(status, response_headers, body, url)
                promise.resolve(result)
                
        except urllib.error.HTTPError as e:
            # HTTP errors (4xx, 5xx)
            try:
                error_body = e.read().decode('utf-8') if e.fp else ""
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


# Documentation
documentation_http_get = """
http-get: Make an HTTP GET request

Usage:
  (http-get url)
  (http-get url headers)

Arguments:
  url     - String URL to request (must be http:// or https://)
  headers - Optional map of headers to send

Returns:
  Promise that resolves to a response map with keys:
    :status  - HTTP status code (number)
    :headers - Response headers (map)
    :body    - Response body (string)
    :url     - Request URL (string)
    :ok      - True if status 2xx, false otherwise
    :json    - Parsed JSON (only if response is valid JSON)

Examples:
  ; Simple GET request
  (http-get "https://httpbin.org/get")
  
  ; GET with headers
  (http-get "https://api.example.com/data"
            {:authorization "Bearer token123"
             :accept "application/json"})
  
  ; Using with promises
  (-> (http-get "https://httpbin.org/json")
      (then (fn [response] 
              (if (:ok response)
                (println "Success:" (:json response))
                (println "Error:" (:status response))))))

Notes:
  - Requests timeout after 30 seconds
  - Both successful and error responses resolve the promise
  - Network errors reject the promise
  - JSON responses are automatically parsed to :json key
  - Headers support LisPy keyword syntax (:authorization)
""" 