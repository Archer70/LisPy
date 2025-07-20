"""
Request parsing for LisPy Web Framework.
Converts HTTP requests into LisPy data structures with keyword keys.
"""

import json
import urllib.parse
from typing import Any, Dict, Optional

from lispy.types import Symbol


def parse_query_string(query_string: str) -> Dict[Symbol, str]:
    """
    Parse URL query string into LisPy map with keyword keys.

    Args:
        query_string: Raw query string (e.g. "name=Alice&age=30")

    Returns:
        Dict with Symbol keys for LisPy compatibility
    """
    if not query_string:
        return {}

    parsed = urllib.parse.parse_qs(query_string)
    result = {}

    for key, values in parsed.items():
        # Convert to LisPy keyword symbol and take first value
        symbol_key = Symbol(f":{key}")
        result[symbol_key] = values[0] if values else ""

    return result


def parse_headers(headers) -> Dict[Symbol, str]:
    """
    Parse HTTP headers into LisPy map with keyword keys.

    Args:
        headers: HTTP headers object

    Returns:
        Dict with Symbol keys for LisPy compatibility
    """
    result = {}

    for key, value in headers.items():
        # Convert header names to lowercase keywords
        symbol_key = Symbol(f":{key.lower()}")
        result[symbol_key] = value

    return result


def parse_json_body(body: str, content_type: str) -> Optional[Any]:
    """
    Parse JSON body if content type indicates JSON.

    Args:
        body: Request body as string
        content_type: Content-Type header value

    Returns:
        Parsed JSON data or None if not JSON/invalid
    """
    if not body or not content_type:
        return None

    if "application/json" in content_type.lower():
        try:
            return json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return None

    return None


def extract_path_params(path: str, route_pattern: str) -> Dict[Symbol, str]:
    """
    Extract path parameters from URL using route pattern.

    Args:
        path: Actual request path (e.g. "/users/123")
        route_pattern: Route pattern (e.g. "/users/:id")

    Returns:
        Dict with extracted parameters as Symbol keys
    """
    path_parts = [p for p in path.split("/") if p]
    pattern_parts = [p for p in route_pattern.split("/") if p]

    if len(path_parts) != len(pattern_parts):
        return {}

    params = {}
    for path_part, pattern_part in zip(path_parts, pattern_parts):
        if pattern_part.startswith(":"):
            param_name = pattern_part[1:]  # Remove the ':'
            symbol_key = Symbol(f":{param_name}")
            params[symbol_key] = path_part

    return params


def parse_request(
    method: str,
    path: str,
    headers,
    body: str = "",
    route_pattern: str = "",
    client_address=None,
) -> Dict[Symbol, Any]:
    """
    Parse HTTP request into LisPy data structure.

    Args:
        method: HTTP method (GET, POST, etc.)
        path: Request path including query string
        headers: HTTP headers
        body: Request body
        route_pattern: Matched route pattern for parameter extraction
        client_address: Client IP address tuple

    Returns:
        Dict representing request with LisPy keyword keys:
        {:method "GET"
         :path "/users/123"
         :query-params {:page "1"}
         :headers {:content-type "application/json"}
         :body "{\"name\": \"Alice\"}"
         :json {:name "Alice"}
         :params {:id "123"}
         :remote-addr "127.0.0.1"}
    """
    # Split path and query string
    parsed_url = urllib.parse.urlparse(path)
    clean_path = parsed_url.path
    query_string = parsed_url.query

    # Parse components
    query_params = parse_query_string(query_string)
    parsed_headers = parse_headers(headers)
    content_type = headers.get("Content-Type", "")
    json_data = parse_json_body(body, content_type)
    path_params = (
        extract_path_params(clean_path, route_pattern) if route_pattern else {}
    )

    # Get client IP
    remote_addr = client_address[0] if client_address else "unknown"

    # Build request object with LisPy keyword keys
    request = {
        Symbol(":method"): method.upper(),
        Symbol(":path"): clean_path,
        Symbol(":query-params"): query_params,
        Symbol(":headers"): parsed_headers,
        Symbol(":body"): body,
        Symbol(":params"): path_params,
        Symbol(":remote-addr"): remote_addr,
    }

    # Add JSON data if available
    if json_data is not None:
        request[Symbol(":json")] = json_data

    return request
