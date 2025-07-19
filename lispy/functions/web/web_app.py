"""
Web app creation function for LisPy Web Framework.
"""

from lispy.exceptions import EvaluationError
from lispy.web.app import WebApp
from lispy.functions.decorators import lispy_function, lispy_documentation

@lispy_function("web-app", web_safe=False, reason="Network access")
def web_app(args, env):
    """
    Create a new web application instance.
    
    Usage: (web-app)
    
    Returns:
        A WebApp instance that can be configured with routes and middleware
        
    Examples:
        ; Create a new web application
        (define app (web-app))
        
        ; Add routes to the application
        (route app "GET" "/" home-handler)
        (route app "POST" "/api/users" create-user-handler)
        
        ; Start the server
        (start-server app {:port 8080})
    """
    if len(args) != 0:
        raise EvaluationError(
            f"SyntaxError: 'web-app' expects 0 arguments, got {len(args)}."
        )
    
    # Create and return a new WebApp instance
    return WebApp()


@lispy_documentation("web-app")
def web_app_documentation():
    """Returns documentation for the web-app function."""
    return """Function: web-app
Arguments: (web-app)
Description: Creates a new web application instance.

A web application is the main container for routes, middleware, and server configuration.
After creating a web application, you can add routes and middleware, then start a server.

Examples:
  ; Create a basic web application
  (define app (web-app))
  
  ; Add a simple route
  (route app "GET" "/"
    (fn [request]
      {:status 200
       :headers {:content-type "text/html"}
       :body "<h1>Hello, LisPy Web!</h1>"}))
  
  ; Add middleware for logging
  (middleware app :before
    (fn [request]
      (println "Request:" (:method request) (:path request))
      request))
  
  ; Start the server
  (define server-promise (start-server app {:port 8080}))
  (await server-promise)

Return Value:
  Returns a WebApp instance that can be used with other web functions.
  
  The WebApp instance supports:
  - Adding routes with the 'route' function
  - Adding middleware with the 'middleware' function  
  - Starting a server with the 'start-server' function
  - Getting application info with internal methods

Notes:
  - Takes no arguments - creates a fresh, empty web application
  - Each call creates a separate, independent application instance
  - Applications can run on different ports simultaneously
  - Routes and middleware are isolated between applications
  - Compatible with LisPy's functional programming style
  - Designed to be similar to Flask's app creation pattern
"""