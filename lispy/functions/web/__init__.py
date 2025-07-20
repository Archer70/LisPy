"""
Web functions for LisPy - Flask-like web framework functionality.
"""

from .web_app import web_app, web_app_documentation
from .route import route, route_documentation
from .middleware import middleware, middleware_documentation
from .start_server import start_server, start_server_documentation
from .stop_server import stop_server, stop_server_documentation

__all__ = [
    'web_app',
    'web_app_documentation',
    'route',
    'route_documentation',
    'middleware',
    'middleware_documentation',
    'start_server',
    'start_server_documentation',
    'stop_server',
    'stop_server_documentation',
]