"""LisPy Type Checking Functions - Now using decorator-based registration"""

# The functions are now automatically registered via decorators
# Import them to trigger the decorator registration
from .is_boolean_q import is_boolean_q, is_boolean_q_documentation
from .is_function_q import is_function_q, is_function_q_documentation
from .is_list_q import is_list_q, is_list_q_documentation
from .is_map_q import is_map_q, is_map_q_documentation
from .is_nil_q import is_nil_q, is_nil_q_documentation
from .is_number_q import is_number_q, is_number_q_documentation
from .is_string_q import is_string_q, is_string_q_documentation
from .is_vector_q import is_vector_q, is_vector_q_documentation

__all__ = [
    # Functions (new names)
    "is_boolean_q",
    "is_function_q",
    "is_list_q",
    "is_map_q",
    "is_nil_q",
    "is_number_q",
    "is_string_q",
    "is_vector_q",
    # Documentation (new names)
    "is_boolean_q_documentation",
    "is_function_q_documentation",
    "is_list_q_documentation",
    "is_map_q_documentation",
    "is_nil_q_documentation",
    "is_number_q_documentation",
    "is_string_q_documentation",
    "is_vector_q_documentation",
]
