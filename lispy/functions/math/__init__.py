"""LisPy Math Functions - Now using decorator-based registration"""

# The functions are now automatically registered via decorators
# Import them to trigger the decorator registration
from .abs import abs_func, abs_documentation
from .add import add, add_documentation
from .divide import divide, divide_documentation
from .equals import equals, equals_documentation
from .max import max_func, max_documentation
from .min import min_func, min_documentation
from .modulo import modulo, modulo_documentation
from .multiply import multiply, multiply_documentation
from .subtract import subtract, subtract_documentation

__all__ = [
    # Functions (new names)
    "abs_func",
    "add",
    "divide", 
    "equals",
    "max_func",
    "min_func",
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
