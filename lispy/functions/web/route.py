"""
Route registration function for LisPy Web Framework.
"""

from lispy.closure import Function
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.web.app import WebApp


@lispy_function("route", web_safe=False, reason="Network access")
def route(args, env):
    """
    Add a route to a web application.

    Usage: (route app method pattern handler)

    Args:
        app: WebApp instance created by (web-app)
        method: HTTP method as string (GET, POST, PUT, DELETE, etc.)
        pattern: URL pattern as string (e.g., "/users/:id")
        handler: Function that handles requests for this route

    Returns:
        The WebApp instance (for chaining)

    Examples:
        ; Simple GET route
        (route app "GET" "/"
          (fn [request]
            {:status 200
             :headers {:content-type "text/html"}
             :body "<h1>Home Page</h1>"}))

        ; Route with URL parameters
        (route app "GET" "/users/:id"
          (fn [request]
            (let [user-id (:id (:params request))]
              {:status 200
               :headers {:content-type "application/json"}
               :body (json-encode {:id user-id :name "User Name"})})))

        ; POST route with JSON body
        (route app "POST" "/api/users"
          (fn [request]
            (let [user-data (:json request)]
              {:status 201
               :headers {:content-type "application/json"}
               :body (json-encode {:message "User created" :data user-data})})))
    """
    if len(args) != 4:
        raise EvaluationError(
            f"SyntaxError: 'route' expects 4 arguments (app method pattern handler), got {len(args)}."
        )

    app = args[0]
    method = args[1]
    pattern = args[2]
    handler = args[3]

    # Validate app argument
    if not isinstance(app, WebApp):
        raise EvaluationError(
            f"TypeError: 'route' first argument must be a web application (created by web-app), got {type(app).__name__}."
        )

    # Validate method argument
    if not isinstance(method, str):
        raise EvaluationError(
            f"TypeError: 'route' method must be a string, got {type(method).__name__}."
        )

    method = method.upper().strip()
    if not method:
        raise EvaluationError("ValueError: 'route' method cannot be empty.")

    # Validate common HTTP methods
    valid_methods = {
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "HEAD",
        "OPTIONS",
        "PATCH",
        "TRACE",
        "CONNECT",
    }
    if method not in valid_methods:
        # Allow non-standard methods but warn
        print(
            f"Warning: Non-standard HTTP method '{method}' - this may not work with all clients."
        )

    # Validate pattern argument
    if not isinstance(pattern, str):
        raise EvaluationError(
            f"TypeError: 'route' pattern must be a string, got {type(pattern).__name__}."
        )

    if not pattern.strip():
        raise EvaluationError("ValueError: 'route' pattern cannot be empty.")

    # Ensure pattern starts with /
    if not pattern.startswith("/"):
        pattern = "/" + pattern

    # Validate handler argument
    is_user_defined_fn = isinstance(handler, Function)
    is_builtin_fn = callable(handler) and not is_user_defined_fn

    if not (is_user_defined_fn or is_builtin_fn):
        raise EvaluationError(
            f"TypeError: 'route' handler must be a function, got {type(handler).__name__}."
        )

    # Validate handler arity for user-defined functions
    if is_user_defined_fn and len(handler.params) != 1:
        raise EvaluationError(
            f"TypeError: 'route' handler function must take 1 argument (request), got {len(handler.params)}."
        )

    # Add route to the application
    try:
        app.add_route(method, pattern, handler)
    except Exception as e:
        raise EvaluationError(f"Failed to add route {method} {pattern}: {str(e)}")

    # Return the app for chaining
    return app


@lispy_documentation("route")
def route_documentation():
    """Returns documentation for the route function."""
    return """Function: route
Arguments: (route app method pattern handler)
Description: Adds an HTTP route to a web application.

Routes define how the application responds to specific HTTP requests. Each route
is identified by an HTTP method and URL pattern, and handled by a function.

Arguments:
  app     - Web application instance (created by web-app)
  method  - HTTP method as string (GET, POST, PUT, DELETE, etc.)
  pattern - URL pattern as string (supports parameters like /users/:id)
  handler - Function that processes requests for this route

URL Patterns:
  Static routes:    "/about", "/api/health"
  Parameter routes: "/users/:id", "/posts/:id/comments/:comment_id"
  
  Parameters are extracted from the URL and available in the request object
  under the :params key as keyword symbols (e.g., :id, :comment_id).

Handler Function:
  The handler function receives one argument: the request object.
  It must return a response object with :status, :headers, and :body keys.
  
  Request object structure:
    {:method "GET"
     :path "/users/123"
     :query-params {:page "1"}
     :headers {:content-type "application/json"}
     :body "{...}"
     :json {...}              ; Parsed JSON if applicable
     :params {:id "123"}      ; URL parameters
     :remote-addr "127.0.0.1"}
  
  Response object structure:
    {:status 200
     :headers {:content-type "text/html"}
     :body "<h1>Hello World</h1>"}

Examples:
  ; Simple home page
  (route app "GET" "/"
    (fn [request]
      {:status 200
       :headers {:content-type "text/html"}
       :body "<h1>Welcome to LisPy Web!</h1>"}))
  
  ; User profile with URL parameter
  (route app "GET" "/users/:id"
    (fn [request]
      (let [user-id (:id (:params request))]
        {:status 200
         :headers {:content-type "application/json"}
         :body (json-encode {:id user-id :name "User Name"})})))
  
  ; Create user with JSON body
  (route app "POST" "/api/users"
    (fn [request]
      (let [user-data (:json request)
            user-name (:name user-data)]
        {:status 201
         :headers {:content-type "application/json"}
         :body (json-encode {:message "User created" :name user-name})})))
  
  ; Health check endpoint
  (route app "GET" "/health"
    (fn [request]
      {:status 200
       :headers {:content-type "application/json"}
       :body (json-encode {:status "healthy" :timestamp (time)})}))
  
  ; Route with query parameters
  (route app "GET" "/search"
    (fn [request]
      (let [query (:q (:query-params request))
            page (:page (:query-params request))]
        {:status 200
         :headers {:content-type "application/json"}
         :body (json-encode {:query query :page page :results []})})))

HTTP Methods:
  Standard: GET, POST, PUT, DELETE, HEAD, OPTIONS, PATCH
  Less common: TRACE, CONNECT
  Custom methods are allowed but may not work with all clients

Notes:
  - Routes are matched in the order they were added
  - First matching route wins
  - URL parameters are automatically extracted and parsed
  - JSON request bodies are automatically parsed to :json key
  - Response headers are automatically formatted
  - Content-Type is auto-detected if not specified
  - Returns the app instance for method chaining
  - Route patterns must start with / (added automatically if missing)
"""
