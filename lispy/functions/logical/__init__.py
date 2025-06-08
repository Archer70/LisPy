"""LisPy Logical Functions"""

from .equal_q import builtin_equal_q, documentation_equal_q
from .greater_than import builtin_greater_than, documentation_greater_than
from .greater_than_or_equal import builtin_greater_than_or_equal, documentation_greater_than_or_equal
from .less_than import builtin_less_than, documentation_less_than
from .less_than_or_equal import builtin_less_than_or_equal, documentation_less_than_or_equal
from .not_fn import builtin_not, documentation_not

__all__ = [
    # Functions
    "builtin_equal_q",
    "builtin_greater_than",
    "builtin_greater_than_or_equal", 
    "builtin_less_than",
    "builtin_less_than_or_equal",
    "builtin_not",
    # Documentation
    "documentation_equal_q",
    "documentation_greater_than",
    "documentation_greater_than_or_equal",
    "documentation_less_than", 
    "documentation_less_than_or_equal",
    "documentation_not",
] 