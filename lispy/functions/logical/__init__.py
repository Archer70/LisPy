"""LisPy Logical Functions - Now using decorator-based registration"""

# The functions are now automatically registered via decorators
# Import them to trigger the decorator registration
from .equal_q import equal_q, equal_q_documentation
from .greater_than import greater_than, greater_than_documentation
from .greater_than_or_equal import greater_than_or_equal, greater_than_or_equal_documentation
from .less_than import less_than, less_than_documentation
from .less_than_or_equal import less_than_or_equal, less_than_or_equal_documentation
from .not_fn import not_fn, not_documentation

__all__ = [
    # Functions (new names)
    "equal_q",
    "greater_than",
    "greater_than_or_equal",
    "less_than",
    "less_than_or_equal",
    "not_fn",
    # Documentation (new names)
    "equal_q_documentation",
    "greater_than_documentation",
    "greater_than_or_equal_documentation", 
    "less_than_documentation",
    "less_than_or_equal_documentation",
    "not_documentation",
]
