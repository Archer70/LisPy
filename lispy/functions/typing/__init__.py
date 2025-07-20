"""LisPy Type Conversion Functions - Now using decorator-based registration"""

# The functions are now automatically registered via decorators
# Import them to trigger the decorator registration
from .to_bool import to_bool, to_bool_documentation
from .to_float import to_float, to_float_documentation
from .to_int import to_int, to_int_documentation
from .to_str import to_str, to_str_documentation

__all__ = [
    # Functions (new names)
    "to_bool",
    "to_float",
    "to_int",
    "to_str",
    # Documentation (new names)
    "to_bool_documentation",
    "to_float_documentation",
    "to_int_documentation",
    "to_str_documentation",
] 