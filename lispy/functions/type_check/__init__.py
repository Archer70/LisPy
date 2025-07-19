"""LisPy Type Checking Functions - Now using decorator-based registration"""

# The functions are now automatically registered via decorators
# Import them to trigger the decorator registration
from .is_boolean_q import is_boolean, is_boolean_documentation
from .is_function_q import is_function, is_function_documentation
from .is_list_q import is_list, is_list_documentation
from .is_map_q import is_map, is_map_documentation
from .is_nil_q import is_nil, is_nil_documentation
from .is_number_q import is_number, is_number_documentation
from .is_string_q import is_string, is_string_documentation
from .is_vector_q import is_vector, is_vector_documentation

__all__ = [
    # Functions (new names)
    "is_boolean",
    "is_function",
    "is_list",
    "is_map",
    "is_nil",
    "is_number",
    "is_string",
    "is_vector",
    # Documentation (new names)
    "is_boolean_documentation",
    "is_function_documentation",
    "is_list_documentation",
    "is_map_documentation",
    "is_nil_documentation",
    "is_number_documentation",
    "is_string_documentation",
    "is_vector_documentation",
]
