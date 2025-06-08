"""LisPy Type Checking Functions"""

from .is_boolean_q import builtin_is_boolean_q, documentation_is_boolean_q
from .is_function_q import builtin_is_function_q, documentation_is_function_q
from .is_list_q import builtin_is_list_q, documentation_is_list_q
from .is_map_q import builtin_is_map_q, documentation_is_map_q
from .is_nil_q import builtin_is_nil_q, documentation_is_nil_q
from .is_number_q import builtin_is_number_q, documentation_is_number_q
from .is_string_q import builtin_is_string_q, documentation_is_string_q
from .is_vector_q import builtin_is_vector_q, documentation_is_vector_q

__all__ = [
    # Functions
    "builtin_is_boolean_q",
    "builtin_is_function_q",
    "builtin_is_list_q",
    "builtin_is_map_q",
    "builtin_is_nil_q",
    "builtin_is_number_q",
    "builtin_is_string_q",
    "builtin_is_vector_q",
    # Documentation
    "documentation_is_boolean_q",
    "documentation_is_function_q",
    "documentation_is_list_q",
    "documentation_is_map_q",
    "documentation_is_nil_q",
    "documentation_is_number_q",
    "documentation_is_string_q",
    "documentation_is_vector_q",
] 