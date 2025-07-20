"""
URL routing for LisPy Web Framework.
Handles route registration, pattern matching, and route resolution.
"""

import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class Route:
    """Represents a single route with method, pattern, and handler."""

    method: str
    pattern: str
    handler: Callable
    compiled_pattern: re.Pattern
    param_names: List[str]


class Router:
    """
    URL router that handles route registration and matching.
    Supports URL patterns like '/users/:id' and '/posts/:id/comments/:comment_id'.
    """

    def __init__(self):
        self.routes: List[Route] = []

    def add_route(self, method: str, pattern: str, handler: Callable) -> None:
        """
        Add a route to the router.

        Args:
            method: HTTP method (GET, POST, etc.)
            pattern: URL pattern (e.g., '/users/:id')
            handler: Handler function for this route
        """
        method = method.upper()

        # Compile pattern and extract parameter names
        compiled_pattern, param_names = self._compile_pattern(pattern)

        route = Route(
            method=method,
            pattern=pattern,
            handler=handler,
            compiled_pattern=compiled_pattern,
            param_names=param_names,
        )

        self.routes.append(route)

    def find_route(
        self, method: str, path: str
    ) -> Optional[Tuple[Route, Dict[str, str]]]:
        """
        Find a matching route for the given method and path.

        Args:
            method: HTTP method
            path: Request path

        Returns:
            Tuple of (Route, params_dict) if found, None otherwise
        """
        method = method.upper()

        for route in self.routes:
            if route.method != method:
                continue

            match = route.compiled_pattern.match(path)
            if match:
                # Extract path parameters
                params = {}
                for i, param_name in enumerate(route.param_names):
                    params[param_name] = match.group(i + 1)

                return route, params

        return None

    def get_allowed_methods(self, path: str) -> List[str]:
        """
        Get all allowed HTTP methods for a given path.

        Args:
            path: Request path

        Returns:
            List of allowed HTTP methods
        """
        allowed_methods = []

        for route in self.routes:
            if route.compiled_pattern.match(path):
                allowed_methods.append(route.method)

        return allowed_methods

    def _compile_pattern(self, pattern: str) -> Tuple[re.Pattern, List[str]]:
        """
        Compile a URL pattern into a regex and extract parameter names.

        Args:
            pattern: URL pattern like '/users/:id' or '/posts/:id/comments/:comment_id'

        Returns:
            Tuple of (compiled_regex, parameter_names_list)
        """
        # Find all parameter names (parts starting with :)
        param_names = []
        pattern_parts = pattern.split("/")

        # Build regex pattern
        regex_parts = []
        for part in pattern_parts:
            if part.startswith(":"):
                # Parameter part - extract name and replace with regex group
                param_name = part[1:]  # Remove the ':'
                param_names.append(param_name)
                regex_parts.append("([^/]+)")  # Match anything except /
            else:
                # Literal part - escape regex special characters
                escaped_part = re.escape(part)
                regex_parts.append(escaped_part)

        # Join parts and compile regex
        regex_pattern = "/".join(regex_parts)

        # Ensure pattern matches full path (anchored)
        if not regex_pattern.startswith("^"):
            regex_pattern = "^" + regex_pattern
        if not regex_pattern.endswith("$"):
            regex_pattern = regex_pattern + "$"

        compiled_pattern = re.compile(regex_pattern)

        return compiled_pattern, param_names

    def get_routes_summary(self) -> List[Dict[str, str]]:
        """
        Get a summary of all registered routes.

        Returns:
            List of dicts with route information
        """
        return [
            {
                "method": route.method,
                "pattern": route.pattern,
                "params": route.param_names,
            }
            for route in self.routes
        ]
