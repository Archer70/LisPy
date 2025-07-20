"""
Server shutdown function for LisPy Web Framework.
"""

from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import Symbol
from lispy.web.app import WebApp

from .start_server import _running_servers


@lispy_function("stop-server", web_safe=False, reason="Network access")
def stop_server(args, env):
    """
    Stop a running HTTP server gracefully.

    Usage: (stop-server app)
           (stop-server server-info)

    Args:
        app: WebApp instance that is currently running, OR
        server-info: Server information dict returned by start-server

    Returns:
        True if server was stopped, False if server was not running

    Examples:
        ; Stop by app instance
        (define app (web-app))
        (start-server app {:port 8080})
        (stop-server app)

        ; Stop by server info
        (define server-info (await (start-server app {:port 8080})))
        (stop-server server-info)
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'stop-server' expects 1 argument (app or server-info), got {len(args)}."
        )

    target = args[0]

    # Determine if argument is WebApp or server info dict
    if isinstance(target, WebApp):
        # Stop by WebApp instance
        return _stop_server_by_app(target)
    elif isinstance(target, dict):
        # Stop by server info dict
        return _stop_server_by_info(target)
    else:
        raise EvaluationError(
            f"TypeError: 'stop-server' argument must be a web application or server info dict, got {type(target).__name__}."
        )


def _stop_server_by_app(app: WebApp) -> bool:
    """Stop server by WebApp instance."""
    if not app.is_running:
        return False

    # Find the server running this app
    for server_id, server in list(_running_servers.items()):
        if server.web_app is app:
            try:
                server.stop()
                del _running_servers[server_id]
                return True
            except Exception as e:
                print(f"Warning: Error stopping server {server_id}: {e}")
                return False

    # App says it's running but we can't find the server
    app.is_running = False
    return False


def _stop_server_by_info(server_info: dict) -> bool:
    """Stop server by server info dict."""
    # Extract server ID from info
    server_id = server_info.get(Symbol(":server_id"), server_info.get("server_id"))

    if not server_id:
        raise EvaluationError(
            "Server info dict must contain :server_id or 'server_id' key."
        )

    if server_id not in _running_servers:
        return False  # Server not running

    try:
        server = _running_servers[server_id]
        server.stop()
        del _running_servers[server_id]
        return True
    except Exception as e:
        print(f"Warning: Error stopping server {server_id}: {e}")
        return False


@lispy_documentation("stop-server")
def stop_server_documentation():
    """Returns documentation for the stop-server function."""
    return """Function: stop-server
Arguments: (stop-server app-or-server-info)
Description: Gracefully stops a running HTTP server.

The function can stop a server using either the web application instance
or the server information returned by start-server.

Arguments:
  app-or-server-info - Either:
    - WebApp instance (returned by web-app)
    - Server info dict (returned by start-server promise)

Examples:
  ; Stop server using app instance
  (define app (web-app))
  (route app "GET" "/" (fn [req] {:status 200 :body "Hello"}))
  (start-server app {:port 8080})
  ; ... later ...
  (stop-server app)
  
  ; Stop server using server info
  (define app (web-app))
  (route app "GET" "/" (fn [req] {:status 200 :body "Hello"}))
  (define server-promise (start-server app {:port 8080}))
  (define server-info (await server-promise))
  ; ... later ...
  (stop-server server-info)
  
  ; Conditional stopping
  (define app (web-app))
  (start-server app {:port 8080})
  ; ... later ...
  (if (stop-server app)
    (println "Server stopped successfully")
    (println "Server was not running"))
  
  ; Stop in error handler
  (try
    (define app (web-app))
    (define server-promise (start-server app {:port 8080}))
    (await server-promise)
  (catch [error]
    (stop-server app)
    (println "Server stopped due to error:" error)))

Return Value:
  Returns a boolean:
  - true: Server was running and has been stopped
  - false: Server was not running (no action taken)

Server Shutdown Process:
  1. Server stops accepting new connections
  2. Existing connections are allowed to complete
  3. Server resources are cleaned up
  4. WebApp is marked as not running
  5. Server thread terminates gracefully

Use Cases:
  ; Graceful shutdown on signal
  (define app (web-app))
  (start-server app {:port 8080})
  ; ... on SIGTERM or SIGINT ...
  (stop-server app)
  
  ; Conditional restart
  (if (stop-server app)
    (start-server app {:port 8081})  ; Restart on different port
    (println "Server was not running"))
  
  ; Stop all servers (using server info tracking)
  (define servers [])
  (define server1 (await (start-server app1 {:port 8080})))
  (define server2 (await (start-server app2 {:port 8081})))
  (conj! servers server1 server2)
  ; ... later ...
  (map stop-server servers)

Error Handling:
  - Function does not throw errors for normal stop operations
  - Returns false if server is already stopped or not found
  - Prints warnings for internal stop errors but continues
  - Safe to call multiple times on the same server

Notes:
  - Server shutdown is asynchronous but function returns immediately
  - Stopped servers cannot be restarted (create new server instance)
  - WebApp can be reused with start-server after stopping
  - Graceful shutdown waits for active requests to complete
  - Uses server registry for tracking multiple servers
  - Compatible with both app instances and server info objects
  - Does not affect other servers running on different ports
"""
