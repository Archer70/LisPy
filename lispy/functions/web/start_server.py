"""
Server startup function for LisPy Web Framework.
"""

import threading
from lispy.exceptions import EvaluationError
from lispy.web.app import WebApp
from lispy.web.server import LispyHTTPServer
from lispy.types import LispyPromise, Symbol
from lispy.functions.decorators import lispy_function, lispy_documentation

# Global registry of running servers for management
_running_servers = {}
_server_counter = 0
_server_counter_lock = threading.Lock()


@lispy_function("start-server", web_safe=False, reason="Network access")
def start_server(args, env):
    """
    Start an HTTP server for a web application.
    
    Usage: (start-server app)
           (start-server app config)
    
    Args:
        app: WebApp instance created by (web-app)
        config: Optional configuration map with keys:
                :port (default: 8080)
                :host (default: "localhost")
                
    Returns:
        A promise that resolves with server information and keeps the script alive
        
    Examples:
        ; Start server with default settings (localhost:8080)
        (define server-promise (start-server app))
        (await server-promise)  ; Keeps script alive
        
        ; Start server with custom port and host
        (define server-promise (start-server app {:port 3000 :host "0.0.0.0"}))
        (await server-promise)
        
        ; Get server info when it starts
        (-> (start-server app {:port 8080})
            (then (fn [info] 
                    (println "Server running at" (:url info)))))
    """
    if not (1 <= len(args) <= 2):
        raise EvaluationError(
            f"SyntaxError: 'start-server' expects 1 or 2 arguments (app [config]), got {len(args)}."
        )
    
    app = args[0]
    config = args[1] if len(args) > 1 else {}
    
    # Validate app argument
    if not isinstance(app, WebApp):
        raise EvaluationError(
            f"TypeError: 'start-server' first argument must be a web application (created by web-app), got {type(app).__name__}."
        )
    
    # Validate config argument
    if not isinstance(config, dict):
        raise EvaluationError(
            f"TypeError: 'start-server' config must be a map, got {type(config).__name__}."
        )
    
    # Extract configuration with defaults
    port = config.get(Symbol(':port'), config.get('port', 8080))
    host = config.get(Symbol(':host'), config.get('host', 'localhost'))
    
    # Validate port
    if not isinstance(port, int):
        raise EvaluationError(
            f"TypeError: 'start-server' port must be an integer, got {type(port).__name__}."
        )
    
    if not (1 <= port <= 65535):
        raise EvaluationError(
            f"ValueError: 'start-server' port must be between 1 and 65535, got {port}."
        )
    
    # Validate host
    if not isinstance(host, str):
        raise EvaluationError(
            f"TypeError: 'start-server' host must be a string, got {type(host).__name__}."
        )
    
    if not host.strip():
        raise EvaluationError("ValueError: 'start-server' host cannot be empty.")
    
    # Check if app is already running
    if app.is_running:
        raise EvaluationError("ValueError: This web application is already running on a server.")
    
    # Create the server promise that keeps the script alive
    server_promise = LispyPromise()
    
    def start_server_async():
        """Start the server in a background thread."""
        global _server_counter
        
        try:
            # Create and start the HTTP server
            server = LispyHTTPServer(app, env, host, port)
            server_info = server.start()
            
            # Register the server for management (thread-safe)
            with _server_counter_lock:
                _server_counter += 1
                server_id = f"server_{_server_counter}"
                _running_servers[server_id] = server
            
            # Add server ID to info
            server_info['server_id'] = server_id
            server_info['routes'] = app.router.get_routes_summary()
            server_info['middleware'] = app.middleware_chain.get_middleware_summary()
            
            # Resolve promise with server info
            server_promise.resolve(server_info)
            
            # Keep the server running (this keeps the promise and script alive)
            while server.is_running:
                threading.Event().wait(1)  # Sleep for 1 second intervals
            
            # Server stopped - clean up
            if server_id in _running_servers:
                del _running_servers[server_id]
                
        except Exception as e:
            # Server failed to start
            server_promise.reject(f"Failed to start server: {str(e)}")
    
    # Start server in background thread
    server_thread = threading.Thread(target=start_server_async, daemon=True)
    server_thread.start()
    
    return server_promise


def stop_all_servers():
    """
    Stop all running servers (internal utility function).
    """
    global _running_servers
    
    for server_id, server in list(_running_servers.items()):
        try:
            server.stop()
        except Exception as e:
            print(f"Warning: Error stopping server {server_id}: {e}")
    
    _running_servers.clear()


def get_running_servers():
    """
    Get information about all running servers (internal utility function).
    """
    return {
        server_id: server.get_server_info() 
        for server_id, server in _running_servers.items()
    }


@lispy_documentation("start-server")
def start_server_documentation():
    """Returns documentation for the start-server function."""
    return """Function: start-server
Arguments: (start-server app [config])
Description: Starts an HTTP server for a web application and returns a promise.

The server runs in a background thread and the returned promise keeps the
LisPy script alive. The promise resolves with server information when the
server successfully starts, but continues running until explicitly stopped.

Arguments:
  app    - Web application instance (created by web-app)
  config - Optional configuration map with server settings

Configuration Options:
  :port - Port number to listen on (default: 8080)
  :host - Host address to bind to (default: "localhost")
  
  Common host values:
    "localhost" or "127.0.0.1" - Local access only
    "0.0.0.0" - Accept connections from any IP address

Examples:
  ; Start server with default settings (localhost:8080)
  (define app (web-app))
  (route app "GET" "/" (fn [req] {:status 200 :body "Hello!"}))
  (define server-promise (start-server app))
  (await server-promise)  ; Script stays alive, server runs
  
  ; Start server on custom port
  (define server-promise (start-server app {:port 3000}))
  (await server-promise)
  
  ; Start server accessible from external IPs
  (define server-promise (start-server app {:port 8080 :host "0.0.0.0"}))
  (await server-promise)
  
  ; Get server info when it starts
  (-> (start-server app {:port 8080})
      (then (fn [info] 
              (println "Server started!")
              (println "URL:" (:url info))
              (println "Routes:" (:routes info)))))
  
  ; Complete example with routes and middleware
  (define app (web-app))
  
  ; Add routes
  (route app "GET" "/" 
    (fn [req] {:status 200 :body "Welcome!"}))
  (route app "GET" "/health"
    (fn [req] {:status 200 :body "OK"}))
  
  ; Add logging middleware
  (middleware app :before
    (fn [req] 
      (println (:method req) (:path req))
      req))
  
  ; Start server
  (await (start-server app {:port 8080}))

Return Value:
  Returns a Promise that:
  - Resolves with server information when server starts
  - Keeps the script alive while server is running
  - Server information includes:
    {:host "localhost"
     :port 8080
     :url "http://localhost:8080"
     :status "running"
     :server_id "server_1"
     :routes [...route info...]
     :middleware [...middleware info...]}

Server Lifecycle:
  1. Promise is created immediately (server starts in background)
  2. Promise resolves with server info when server is ready
  3. Server continues running (keeping script alive)
  4. Server runs until explicitly stopped or script exits
  5. Background thread handles all HTTP requests

Error Handling:
  - Promise rejects if server fails to start
  - Common failures: port already in use, permission denied
  - Server errors during operation are logged but don't crash the script
  - Route handler errors return 500 responses but don't stop the server

Notes:
  - Server starts immediately when function is called
  - Promise resolution indicates server is ready to accept requests
  - Multiple applications can run on different ports simultaneously
  - Server runs in daemon thread (doesn't prevent script exit)
  - Use await to keep script alive and wait for server
  - Compatible with LisPy's promise system and async/await
  - Similar to Flask's app.run() but with promise-based lifecycle
  - Automatically handles request parsing and response formatting
"""