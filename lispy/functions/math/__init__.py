"""LisPy Math Functions"""

from .abs import builtin_abs, documentation_abs
from .add import builtin_add, documentation_add
from .divide import builtin_divide, documentation_divide
from .equals import builtin_equals, documentation_equals
from .max import builtin_max, documentation_max
from .min import builtin_min, documentation_min
from .modulo import builtin_modulo, documentation_modulo
from .multiply import builtin_multiply, documentation_multiply
from .subtract import builtin_subtract, documentation_subtract

__all__ = [
    # Functions
    "builtin_abs",
    "builtin_add", 
    "builtin_divide",
    "builtin_equals",
    "builtin_max",
    "builtin_min",
    "builtin_modulo",
    "builtin_multiply",
    "builtin_subtract",
    # Documentation
    "documentation_abs",
    "documentation_add",
    "documentation_divide", 
    "documentation_equals",
    "documentation_max",
    "documentation_min",
    "documentation_modulo",
    "documentation_multiply",
    "documentation_subtract",
]
