"""
Response formatting for LisPy Web Framework.
Converts LisPy response data structures into HTTP responses.
"""

import json
from typing import Dict, Any, Tuple
from lispy.types import Symbol


DEFAULT_HEADERS = {
    'Server': 'LisPy-Web/1.0',
    'Content-Type': 'text/plain; charset=utf-8',
}


def normalize_response_headers(headers: Dict[Any, Any]) -> Dict[str, str]:
    """
    Convert LisPy response headers to HTTP headers.
    
    Args:
        headers: Response headers with possible Symbol keys
        
    Returns:
        Dict with string keys suitable for HTTP response
    """
    if not headers:
        return {}
    
    result = {}
    for key, value in headers.items():
        # Convert LisPy symbols (like :content-type) to strings
        str_key = key.name if isinstance(key, Symbol) else str(key)
        # Remove leading colon if present
        if str_key.startswith(':'):
            str_key = str_key[1:]
        
        # Convert to proper HTTP header format (Title-Case)
        header_name = '-'.join(word.capitalize() for word in str_key.split('-'))
        result[header_name] = str(value)
    
    return result


def get_content_type_from_body(body: Any) -> str:
    """
    Determine appropriate Content-Type based on response body.
    
    Args:
        body: Response body (string, dict, list, etc.)
        
    Returns:
        Appropriate Content-Type header value
    """
    if isinstance(body, str):
        # Check if it looks like HTML
        if body.strip().startswith('<') and '>' in body:
            return 'text/html; charset=utf-8'
        else:
            return 'text/plain; charset=utf-8'
    elif isinstance(body, (dict, list)):
        return 'application/json; charset=utf-8'
    else:
        return 'text/plain; charset=utf-8'


def serialize_response_body(body: Any, content_type: str) -> str:
    """
    Serialize response body to string based on content type.
    
    Args:
        body: Response body (any type)
        content_type: Content-Type header value
        
    Returns:
        Serialized body as string
    """
    if body is None:
        return ""
    
    if isinstance(body, str):
        return body
    
    if 'application/json' in content_type:
        try:
            return json.dumps(body, indent=2)
        except (TypeError, ValueError):
            # Fallback to string representation
            return str(body)
    
    return str(body)


def format_response(response_data: Dict[Symbol, Any]) -> Tuple[int, Dict[str, str], str]:
    """
    Format LisPy response into HTTP response components.
    
    Args:
        response_data: LisPy response dict with keys like:
        {:status 200
         :headers {:content-type "application/json"}
         :body {:message "Hello World"}}
         
    Returns:
        Tuple of (status_code, headers_dict, body_string)
    """
    # Extract response components with defaults
    status_code = response_data.get(Symbol(':status'), 200)
    response_headers = response_data.get(Symbol(':headers'), {})
    body = response_data.get(Symbol(':body'), "")
    
    # Validate status code
    if not isinstance(status_code, int) or not (100 <= status_code <= 599):
        status_code = 500
        body = f"Invalid status code: {status_code}"
        response_headers = {}
    
    # Normalize headers
    http_headers = normalize_response_headers(response_headers)
    
    # Merge with defaults, user headers take precedence
    final_headers = DEFAULT_HEADERS.copy()
    final_headers.update(http_headers)
    
    # Auto-detect content type if not specified
    if 'Content-Type' not in final_headers:
        final_headers['Content-Type'] = get_content_type_from_body(body)
    
    # Serialize body
    body_string = serialize_response_body(body, final_headers['Content-Type'])
    
    # Set content length
    final_headers['Content-Length'] = str(len(body_string.encode('utf-8')))
    
    return status_code, final_headers, body_string


def create_error_response(status_code: int, message: str) -> Tuple[int, Dict[str, str], str]:
    """
    Create a standard error response.
    
    Args:
        status_code: HTTP status code
        message: Error message
        
    Returns:
        Tuple of (status_code, headers_dict, body_string)
    """
    headers = DEFAULT_HEADERS.copy()
    headers['Content-Type'] = 'application/json; charset=utf-8'
    
    error_body = json.dumps({
        'error': message,
        'status': status_code
    }, indent=2)
    
    headers['Content-Length'] = str(len(error_body.encode('utf-8')))
    
    return status_code, headers, error_body


def create_method_not_allowed_response(allowed_methods: list) -> Tuple[int, Dict[str, str], str]:
    """
    Create a 405 Method Not Allowed response.
    
    Args:
        allowed_methods: List of allowed HTTP methods
        
    Returns:
        Tuple of (status_code, headers_dict, body_string)
    """
    headers = DEFAULT_HEADERS.copy()
    headers['Allow'] = ', '.join(allowed_methods)
    headers['Content-Type'] = 'application/json; charset=utf-8'
    
    error_body = json.dumps({
        'error': 'Method Not Allowed',
        'status': 405,
        'allowed_methods': allowed_methods
    }, indent=2)
    
    headers['Content-Length'] = str(len(error_body.encode('utf-8')))
    
    return 405, headers, error_body