"""
HTTP utility functions for LisPy HTTP client.
"""

import json
from urllib.parse import urlparse
from lispy.exceptions import LisPyError
from lispy.types import Symbol


class HTTPError(LisPyError):
    """Exception raised for HTTP-related errors."""
    pass


def validate_url_with_message(url):
    """
    Validate URL and return (is_valid, error_message).
    
    Args:
        url (str): URL to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        parsed = urlparse(url)
        
        if not parsed.scheme:
            return False, f"Invalid URL '{url}' - missing scheme (http/https)"
        
        if parsed.scheme not in ('http', 'https'):
            return False, f"Unsupported URL scheme '{parsed.scheme}'"
        
        if not parsed.netloc:
            return False, f"Invalid URL '{url}' - missing host"
        
        return True, ""
        
    except Exception as e:
        return False, f"Invalid URL '{url}': {str(e)}"


def is_valid_url(url):
    """
    Validate if a string is a valid HTTP/HTTPS URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    valid, _ = validate_url_with_message(url)
    return valid


def normalize_headers(headers_dict):
    """
    Convert LisPy keyword headers to string headers for urllib.
    
    Args:
        headers_dict (dict): Headers with possible LisPy Symbol keys
        
    Returns:
        dict: Headers with string keys
    """
    if not headers_dict:
        return {}
    
    normalized = {}
    for key, value in headers_dict.items():
        # Convert LisPy symbols (like :authorization) to strings
        str_key = key.name if isinstance(key, Symbol) else str(key)
        # Remove leading colon if present
        if str_key.startswith(':'):
            str_key = str_key[1:]
        normalized[str_key] = str(value)
    
    return normalized


def parse_json_safely(text):
    """
    Parse JSON text, returning None if parsing fails.
    
    Args:
        text (str): JSON text to parse
        
    Returns:
        object or None: Parsed JSON or None if invalid
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None


def create_response_map(status, headers, body, url):
    """
    Create standardized response map for HTTP responses.
    
    Args:
        status (int): HTTP status code
        headers (dict): Response headers
        body (str): Response body text
        url (str): Request URL
        
    Returns:
        dict: Standardized response with LisPy keyword keys
    """
    response = {
        ':status': status,
        ':headers': headers,
        ':body': body,
        ':url': url,
        ':ok': 200 <= status < 300,
    }
    
    # Add parsed JSON if content is JSON
    parsed_json = parse_json_safely(body)
    if parsed_json is not None:
        response[':json'] = parsed_json
    
    return response 