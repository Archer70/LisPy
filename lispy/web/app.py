"""
Web application container for LisPy Web Framework.
Combines routing, middleware, and request handling.
"""

from typing import Any, Callable, Dict

from lispy.exceptions import EvaluationError
from lispy.types import Symbol

from .middleware import MiddlewareChain
from .request import parse_request
from .response import (create_error_response,
                       create_method_not_allowed_response, format_response)
from .router import Router


class WebApp:
    """
    Web application that combines routing and middleware.
    This is the main container for a LisPy web application.
    """

    def __init__(self):
        self.router = Router()
        self.middleware_chain = MiddlewareChain()
        self.is_running = False

    def add_route(self, method: str, pattern: str, handler: Callable) -> None:
        """
        Add a route to the application.

        Args:
            method: HTTP method (GET, POST, etc.)
            pattern: URL pattern (e.g., '/users/:id')
            handler: Handler function for this route
        """
        self.router.add_route(method, pattern, handler)

    def add_middleware(self, middleware_type: str, handler: Callable) -> None:
        """
        Add middleware to the application.

        Args:
            middleware_type: Either 'before' or 'after'
            handler: Middleware function
        """
        self.middleware_chain.add_middleware(middleware_type, handler)

    def handle_request(
        self,
        method: str,
        path: str,
        headers,
        body: str = "",
        client_address=None,
        env=None,
    ):
        """
        Handle an incoming HTTP request through the full application pipeline.

        Args:
            method: HTTP method
            path: Request path
            headers: HTTP headers
            body: Request body
            client_address: Client IP address
            env: LisPy environment for function execution

        Returns:
            Tuple of (status_code, headers_dict, body_string)
        """
        try:
            # Find matching route
            route_match = self.router.find_route(method, path)

            if not route_match:
                # Check if path exists with different method
                allowed_methods = self.router.get_allowed_methods(path)
                if allowed_methods:
                    return create_method_not_allowed_response(allowed_methods)
                else:
                    return create_error_response(404, f"Not Found: {method} {path}")

            route, route_params = route_match

            # Parse request with route pattern for parameter extraction
            parsed_url = __import__("urllib.parse").parse.urlparse(path)
            clean_path = parsed_url.path

            request = parse_request(
                method=method,
                path=path,
                headers=headers,
                body=body,
                route_pattern=route.pattern,
                client_address=client_address,
            )

            # Execute before middleware
            if env:
                request = self.middleware_chain.execute_before_middleware(request, env)

            # Execute route handler
            response = self._execute_route_handler(route.handler, request, env)

            # Validate response format
            if not isinstance(response, dict):
                return create_error_response(
                    500,
                    f"Route handler must return a response object (dict), got {type(response).__name__}",
                )

            # Execute after middleware
            if env:
                response = self.middleware_chain.execute_after_middleware(
                    request, response, env
                )

            # Format response for HTTP (with JSON enhancement)
            return format_response(response, enhance_json=True)

        except Exception as e:
            # Catch-all error handler
            error_msg = f"Internal Server Error: {str(e)}"
            return create_error_response(500, error_msg)

    def _execute_route_handler(
        self, handler: Callable, request: Dict[Symbol, Any], env
    ) -> Dict[Symbol, Any]:
        """
        Execute a route handler function with proper argument handling.

        Args:
            handler: Route handler function
            request: Request object
            env: LisPy environment

        Returns:
            Response object from handler
        """
        # Check if it's a LisPy user-defined function
        from lispy.closure import Function
        from lispy.environment import Environment
        from lispy.evaluator import evaluate

        if isinstance(handler, Function):
            # User-defined LisPy function
            if len(handler.params) != 1:
                raise EvaluationError(
                    f"Route handler function must take 1 argument (request), got {len(handler.params)}"
                )

            # Create execution environment with access to global functions through env parameter
            if env and hasattr(env, "store"):
                # Use the provided environment (which has global functions) as the outer scope
                call_env = Environment(outer=env)
            else:
                # Fallback to the original defining environment
                call_env = Environment(outer=handler.defining_env)

            call_env.define(handler.params[0].name, request)

            # Execute function body
            result = None
            for expr in handler.body:
                result = evaluate(expr, call_env)

            return result

        elif callable(handler):
            # Built-in function - call with args list
            return handler([request], env)

        else:
            raise EvaluationError(
                f"Route handler must be a function, got {type(handler).__name__}"
            )

    def get_app_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the application configuration.

        Returns:
            Dict with routes and middleware information
        """
        return {
            "routes": self.router.get_routes_summary(),
            "middleware": self.middleware_chain.get_middleware_summary(),
            "is_running": self.is_running,
        }
