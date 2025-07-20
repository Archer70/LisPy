"""LisPy Math Functions - Now using decorator-based registration"""

# The functions are now automatically registered via decorators
# Import them to trigger the decorator registration
from .abs import abs_documentation, abs_fn
from .add import add, add_documentation
from .divide import divide, divide_documentation
from .equals import equals, equals_documentation
from .max import max_documentation, max_fn
from .min import min_documentation, min_fn
from .modulo import modulo, modulo_documentation
from .multiply import multiply, multiply_documentation
from .subtract import subtract, subtract_documentation

__all__ = [
    # Functions (new names)
    "abs_fn",
    "add",
    "divide",
    "equals",
    "max_fn",
    "min_fn",
    "modulo",
    "multiply",
    "subtract",
    # Documentation (new names)
    "abs_documentation",
    "add_documentation",
    "divide_documentation",
    "equals_documentation",
    "max_documentation",
    "min_documentation",
    "modulo_documentation",
    "multiply_documentation",
    "subtract_documentation",
]
