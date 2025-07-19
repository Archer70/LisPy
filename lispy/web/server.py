"""
HTTP Server implementation for LisPy Web Framework.
Uses Python's standard library http.server for HTTP handling.
"""

import http.server
import socketserver
import threading
import time
from typing import Dict, Any, Optional
from urllib.parse import unquote
from .app import WebApp


class LispyHTTPHandler(http.server.BaseHTTPRequestHandler):
    """
    HTTP request handler that integrates with LisPy WebApp.
    Handles all HTTP methods and routes requests through the WebApp.
    """
    
    def __init__(self, request, client_address, server):
        # Store reference to the WebApp and LisPy environment
        self.web_app: WebApp = server.web_app
        self.lispy_env = server.lispy_env
        super().__init__(request, client_address, server)
    
    def do_GET(self):
        """Handle HTTP GET requests."""
        self._handle_request('GET')
    
    def do_POST(self):
        """Handle HTTP POST requests."""
        self._handle_request('POST')
    
    def do_PUT(self):
        """Handle HTTP PUT requests."""
        self._handle_request('PUT')
    
    def do_DELETE(self):
        """Handle HTTP DELETE requests."""
        self._handle_request('DELETE')
    
    def do_HEAD(self):
        """Handle HTTP HEAD requests."""
        self._handle_request('HEAD')
    
    def do_OPTIONS(self):
        """Handle HTTP OPTIONS requests."""
        self._handle_request('OPTIONS')
    
    def do_PATCH(self):
        """Handle HTTP PATCH requests."""
        self._handle_request('PATCH')
    
    def _handle_request(self, method: str):
        """
        Handle HTTP request of any method.
        
        Args:
            method: HTTP method name
        """
        try:
            # Parse request components
            path = unquote(self.path)  # URL decode the path
            headers = dict(self.headers)
            
            # Read request body
            body = ""
            if method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                content_length = int(headers.get('Content-Length', '0'))
                if content_length > 0:
                    body = self.rfile.read(content_length).decode('utf-8')
            
            # Process request through WebApp
            status_code, response_headers, response_body = self.web_app.handle_request(
                method=method,
                path=path,
                headers=headers,
                body=body,
                client_address=self.client_address,
                env=self.lispy_env
            )
            
            # Send HTTP response
            self.send_response(status_code)
            
            # Send headers
            for header_name, header_value in response_headers.items():
                self.send_header(header_name, header_value)
            self.end_headers()
            
            # Send body (except for HEAD requests)
            if method != 'HEAD':
                self.wfile.write(response_body.encode('utf-8'))
                
        except Exception as e:
            # Handle any unexpected errors
            try:
                self.send_error(500, f"Internal Server Error: {str(e)}")
            except:
                # If we can't even send an error response, just pass
                pass
    
    def log_message(self, format, *args):
        """
        Override to customize logging format.
        """
        print(f"[{self.log_date_time_string()}] {format % args}")


class LispyHTTPServer:
    """
    HTTP server that hosts a LisPy WebApp.
    Manages server lifecycle and provides promise-based control.
    """
    
    def __init__(self, web_app: WebApp, lispy_env, host: str = 'localhost', port: int = 8080):
        self.web_app = web_app
        self.lispy_env = lispy_env
        self.host = host
        self.port = port
        self.httpd: Optional[socketserver.TCPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.is_running = False
        
    def start(self) -> Dict[str, Any]:
        """
        Start the HTTP server in a background thread.
        
        Returns:
            Dict with server information
        """
        if self.is_running:
            raise RuntimeError("Server is already running")
        
        try:
            # Create the HTTP server
            self.httpd = socketserver.TCPServer((self.host, self.port), LispyHTTPHandler)
            
            # Store references for the handler
            self.httpd.web_app = self.web_app
            self.httpd.lispy_env = self.lispy_env
            
            # Mark WebApp as running
            self.web_app.is_running = True
            
            # Start server in background thread
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()
            
            # Wait a moment to ensure server starts
            time.sleep(0.1)
            
            self.is_running = True
            
            return {
                'host': self.host,
                'port': self.port,
                'url': f"http://{self.host}:{self.port}",
                'status': 'running'
            }
            
        except Exception as e:
            self.web_app.is_running = False
            raise RuntimeError(f"Failed to start server: {str(e)}")
    
    def stop(self):
        """
        Stop the HTTP server gracefully.
        """
        if not self.is_running:
            return
        
        try:
            if self.httpd:
                self.httpd.shutdown()
                self.httpd.server_close()
            
            if self.server_thread:
                self.server_thread.join(timeout=5.0)
            
            self.web_app.is_running = False
            self.is_running = False
            
        except Exception as e:
            print(f"Warning: Error during server shutdown: {e}")
    
    def _run_server(self):
        """
        Run the HTTP server (called in background thread).
        """
        try:
            self.httpd.serve_forever()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.is_running = False
            self.web_app.is_running = False
    
    def get_server_info(self) -> Dict[str, Any]:
        """
        Get information about the server.
        
        Returns:
            Dict with server status and configuration
        """
        return {
            'host': self.host,
            'port': self.port,
            'url': f"http://{self.host}:{self.port}" if self.is_running else None,
            'is_running': self.is_running,
            'app_summary': self.web_app.get_app_summary()
        }