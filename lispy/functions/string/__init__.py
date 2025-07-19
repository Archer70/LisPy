"""LisPy String Functions - Now using decorator-based registration"""

# The functions are now automatically registered via decorators
# Import them to trigger the decorator registration
from .join import join_func, join_documentation
from .split import split_func, split_documentation

__all__ = [
    # Functions (new names)
    "join_func",
    "split_func",
    # Documentation (new names)
    "join_documentation",
    "split_documentation",
]
