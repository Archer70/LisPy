"""
Web functions for LisPy - Flask-like web framework functionality.
"""

from .web_app import builtin_web_app, documentation_web_app
from .route import builtin_route, documentation_route
from .middleware import builtin_middleware, documentation_middleware
from .start_server import builtin_start_server, documentation_start_server
from .stop_server import builtin_stop_server, documentation_stop_server

__all__ = [
    'builtin_web_app',
    'documentation_web_app',
    'builtin_route',
    'documentation_route',
    'builtin_middleware',
    'documentation_middleware',
    'builtin_start_server',
    'documentation_start_server',
    'builtin_stop_server',
    'documentation_stop_server',
]