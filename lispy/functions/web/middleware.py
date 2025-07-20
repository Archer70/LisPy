"""
Middleware registration function for LisPy Web Framework.
"""

from lispy.exceptions import EvaluationError
from lispy.web.app import WebApp
from lispy.closure import Function
from lispy.types import Symbol
from lispy.functions.decorators import lispy_function, lispy_documentation

@lispy_function("middleware", web_safe=False, reason="Network access")
def middleware(args, env):
    """
    Add middleware to a web application.
    
    Usage: (middleware app type handler)
    
    Args:
        app: WebApp instance created by (web-app)
        type: Middleware type - either :before or :after (or string equivalents)
        handler: Function that processes requests/responses
        
    Returns:
        The WebApp instance (for chaining)
        
    Examples:
        ; Before middleware (runs before route handler)
        (middleware app :before
          (fn [request]
            (println "Incoming request:" (:method request) (:path request))
            request))  ; Must return request object
        
        ; After middleware (runs after route handler)
        (middleware app :after
          (fn [request response]
            (println "Response status:" (:status response))
            response))  ; Must return response object
        
        ; Authentication middleware
        (middleware app :before
          (fn [request]
            (let [token (:authorization (:headers request))]
              (if (valid-token? token)
                request
                (assoc request :authenticated false)))))
    """
    if len(args) != 3:
        raise EvaluationError(
            f"SyntaxError: 'middleware' expects 3 arguments (app type handler), got {len(args)}."
        )
    
    app = args[0]
    middleware_type = args[1]
    handler = args[2]
    
    # Validate app argument
    if not isinstance(app, WebApp):
        raise EvaluationError(
            f"TypeError: 'middleware' first argument must be a web application (created by web-app), got {type(app).__name__}."
        )
    
    # Validate and normalize middleware type
    if isinstance(middleware_type, Symbol):
        type_str = middleware_type.name
        # Remove leading colon if present
        if type_str.startswith(':'):
            type_str = type_str[1:]
    elif isinstance(middleware_type, str):
        type_str = middleware_type.strip()
    else:
        raise EvaluationError(
            f"TypeError: 'middleware' type must be :before, :after, 'before', or 'after', got {type(middleware_type).__name__}."
        )
    
    if type_str not in ['before', 'after']:
        raise EvaluationError(
            f"ValueError: 'middleware' type must be 'before' or 'after', got '{type_str}'."
        )
    
    # Validate handler argument
    is_user_defined_fn = isinstance(handler, Function)
    is_builtin_fn = callable(handler) and not is_user_defined_fn
    
    if not (is_user_defined_fn or is_builtin_fn):
        raise EvaluationError(
            f"TypeError: 'middleware' handler must be a function, got {type(handler).__name__}."
        )
    
    # Validate handler arity for user-defined functions
    if is_user_defined_fn:
        expected_params = 1 if type_str == 'before' else 2
        if len(handler.params) != expected_params:
            param_desc = "1 argument (request)" if type_str == 'before' else "2 arguments (request response)"
            raise EvaluationError(
                f"TypeError: '{type_str}' middleware function must take {param_desc}, got {len(handler.params)}."
            )
    
    # Add middleware to the application
    try:
        app.add_middleware(type_str, handler)
    except Exception as e:
        raise EvaluationError(f"Failed to add {type_str} middleware: {str(e)}")
    
    # Return the app for chaining
    return app


@lispy_documentation("middleware")
def middleware_documentation():
    """Returns documentation for the middleware function."""
    return """Function: middleware
Arguments: (middleware app type handler)
Description: Adds middleware to a web application for request/response processing.

Middleware functions run before or after route handlers, allowing you to:
- Log requests and responses
- Authenticate users
- Add security headers
- Modify requests or responses
- Handle errors globally

Arguments:
  app     - Web application instance (created by web-app)
  type    - Middleware type: :before or :after (or "before"/"after" strings)
  handler - Function that processes requests and/or responses

Middleware Types:
  :before - Runs before the route handler
    - Receives: request object
    - Returns: modified request object (or original request)
    - Use for: authentication, logging, request modification
  
  :after  - Runs after the route handler  
    - Receives: request object, response object
    - Returns: modified response object (or original response)
    - Use for: response logging, adding headers, error handling

Execution Order:
  1. All :before middleware (in registration order)
  2. Route handler
  3. All :after middleware (in registration order)

Examples:
  ; Request logging middleware
  (middleware app :before
    (fn [request]
      (println "→" (:method request) (:path request) 
               "from" (:remote-addr request))
      request))
  
  ; Response logging middleware
  (middleware app :after
    (fn [request response]
      (println "←" (:status response) "for" (:path request))
      response))
  
  ; Authentication middleware
  (middleware app :before
    (fn [request]
      (let [auth-header (:authorization (:headers request))]
        (if (and auth-header (valid-token? auth-header))
          (assoc request :user (get-user-from-token auth-header))
          (assoc request :user nil)))))
  
  ; CORS headers middleware
  (middleware app :after
    (fn [request response]
      (let [cors-headers {:access-control-allow-origin "*"
                          :access-control-allow-methods "GET,POST,PUT,DELETE"
                          :access-control-allow-headers "Content-Type,Authorization"}]
        (assoc response :headers (merge (:headers response) cors-headers)))))
  
  ; Error handling middleware
  (middleware app :after
    (fn [request response]
      (if (>= (:status response) 400)
        (do
          (println "Error response:" (:status response) "for" (:path request))
          response)
        response)))
  
  ; Request timing middleware
  (middleware app :before
    (fn [request]
      (assoc request :start-time (current-time-millis))))
  
  (middleware app :after
    (fn [request response]
      (let [duration (- (current-time-millis) (:start-time request))]
        (println "Request took" duration "ms")
        response)))

Handler Function Signatures:
  Before middleware: (fn [request] ...)
    - Must return a request object (can be modified)
    - Return nil or the original request for no changes
  
  After middleware: (fn [request response] ...)
    - Must return a response object (can be modified)
    - Return nil or the original response for no changes

Error Handling:
  - Middleware errors are logged but don't crash the server
  - If middleware throws an error, the original request/response is used
  - Use try/catch within middleware for custom error handling

Notes:
  - Middleware runs in registration order
  - Before middleware can modify the request object
  - After middleware can modify the response object
  - Middleware is shared across all routes in the application
  - Use assoc/dissoc to modify request/response objects immutably
  - Returns the app instance for method chaining
  - Compatible with both keyword (:before) and string ("before") types
"""