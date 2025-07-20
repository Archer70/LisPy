"""
Middleware chain execution for LisPy Web Framework.
Handles before/after middleware processing.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List

from lispy.exceptions import EvaluationError
from lispy.types import Symbol


@dataclass
class Middleware:
    """Represents a middleware function with its type."""

    middleware_type: str  # 'before' or 'after'
    handler: Callable


class MiddlewareChain:
    """
    Manages and executes middleware chain for web requests.
    Supports 'before' middleware (runs before route handler) and
    'after' middleware (runs after route handler).
    """

    def __init__(self):
        self.middleware: List[Middleware] = []

    def add_middleware(self, middleware_type: str, handler: Callable) -> None:
        """
        Add middleware to the chain.

        Args:
            middleware_type: Either 'before' or 'after'
            handler: Middleware function
        """
        if middleware_type not in ["before", "after"]:
            raise ValueError(
                f"Invalid middleware type: {middleware_type}. Must be 'before' or 'after'."
            )

        middleware = Middleware(middleware_type=middleware_type, handler=handler)

        self.middleware.append(middleware)

    def execute_before_middleware(
        self, request: Dict[Symbol, Any], env
    ) -> Dict[Symbol, Any]:
        """
        Execute all 'before' middleware in order.

        Args:
            request: Request object to process
            env: LisPy environment for function execution

        Returns:
            Modified request object
        """
        current_request = request

        for middleware in self.middleware:
            if middleware.middleware_type == "before":
                try:
                    # Execute middleware function with request
                    result = self._execute_middleware_function(
                        middleware.handler, current_request, env
                    )

                    # Middleware should return modified request or None (no change)
                    if result is not None:
                        if not isinstance(result, dict):
                            raise EvaluationError(
                                f"Before middleware must return a request object (dict), got {type(result).__name__}"
                            )
                        current_request = result

                except Exception as e:
                    # Middleware errors should not crash the server
                    print(f"Warning: Before middleware error: {e}")
                    # Continue with original request

        return current_request

    def execute_after_middleware(
        self, request: Dict[Symbol, Any], response: Dict[Symbol, Any], env
    ) -> Dict[Symbol, Any]:
        """
        Execute all 'after' middleware in order.

        Args:
            request: Original request object
            response: Response object to process
            env: LisPy environment for function execution

        Returns:
            Modified response object
        """
        current_response = response

        for middleware in self.middleware:
            if middleware.middleware_type == "after":
                try:
                    # Execute middleware function with request and response
                    result = self._execute_middleware_function(
                        middleware.handler, request, env, current_response
                    )

                    # Middleware should return modified response or None (no change)
                    if result is not None:
                        if not isinstance(result, dict):
                            raise EvaluationError(
                                f"After middleware must return a response object (dict), got {type(result).__name__}"
                            )
                        current_response = result

                except Exception as e:
                    # Middleware errors should not crash the server
                    print(f"Warning: After middleware error: {e}")
                    # Continue with original response

        return current_response

    def _execute_middleware_function(
        self,
        handler: Callable,
        request: Dict[Symbol, Any],
        env,
        response: Dict[Symbol, Any] = None,
    ) -> Any:
        """
        Execute a middleware function with proper argument handling.

        Args:
            handler: Middleware function to execute
            request: Request object
            env: LisPy environment
            response: Response object (for after middleware)

        Returns:
            Result from middleware function
        """
        # Check if it's a LisPy user-defined function
        from lispy.closure import Function
        from lispy.environment import Environment
        from lispy.evaluator import evaluate

        if isinstance(handler, Function):
            # User-defined LisPy function
            call_env = Environment(outer=handler.defining_env)

            # Bind parameters based on middleware type
            if response is not None:
                # After middleware: (fn [request response] ...)
                if len(handler.params) != 2:
                    raise EvaluationError(
                        f"After middleware function must take 2 arguments (request response), got {len(handler.params)}"
                    )

                call_env.define(handler.params[0].name, request)
                call_env.define(handler.params[1].name, response)
            else:
                # Before middleware: (fn [request] ...)
                if len(handler.params) != 1:
                    raise EvaluationError(
                        f"Before middleware function must take 1 argument (request), got {len(handler.params)}"
                    )

                call_env.define(handler.params[0].name, request)

            # Execute function body
            result = None
            for expr in handler.body:
                result = evaluate(expr, call_env)

            return result

        elif callable(handler):
            # Built-in function - call with args list
            if response is not None:
                # After middleware
                return handler([request, response], env)
            else:
                # Before middleware
                return handler([request], env)

        else:
            raise EvaluationError(
                f"Middleware handler must be a function, got {type(handler).__name__}"
            )

    def get_middleware_summary(self) -> List[Dict[str, str]]:
        """
        Get a summary of all registered middleware.

        Returns:
            List of dicts with middleware information
        """
        result = []
        for i, middleware in enumerate(self.middleware):
            result.append(
                {
                    "index": str(i),
                    "type": middleware.middleware_type,
                    "handler": str(middleware.handler),
                }
            )
        return result
