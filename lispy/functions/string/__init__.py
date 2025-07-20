"""LisPy String Functions - Now using decorator-based registration"""

# The functions are now automatically registered via decorators
# Import them to trigger the decorator registration
from .join import join_documentation, join_fn
from .split import split_documentation, split_fn

__all__ = [
    # Functions (new names)
    "join_fn",
    "split_fn",
    # Documentation (new names)
    "join_documentation",
    "split_documentation",
]
