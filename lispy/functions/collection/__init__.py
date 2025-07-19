"""LisPy Collection Functions - Partially using decorator-based registration"""

# The functions are now automatically registered via decorators
# Import converted functions to trigger the decorator registration
from .append import append_func, append_documentation
from .concat import concat_func, concat_documentation
from .conj import conj_func, conj_documentation
from .count import count_func, count_documentation
from .empty import empty_q, empty_q_documentation
from .first import first_func, first_documentation
from .filter import filter_func, filter_documentation
from .map import map_func, map_documentation
from .nth import nth_func, nth_documentation
from .reduce import reduce_func, reduce_documentation
from .rest import rest_func, rest_documentation
from .reverse import reverse_func, reverse_documentation

# Import remaining functions that haven't been converted yet (legacy)
from .every_q import every_q, every_q_doc
from .range import range_func, range_doc
from .some import some, some_doc
from .sort import sort_fn, documentation_sort

__all__ = [
    # Converted functions (new names)
    "append_func",
    "concat_func", 
    "conj_func",
    "count_func",
    "empty_q",
    "first_func",
    "filter_func",
    "map_func",
    "nth_func",
    "reduce_func",
    "rest_func",
    "reverse_func",
    # Converted documentation (new names)
    "append_documentation",
    "concat_documentation",
    "conj_documentation", 
    "count_documentation",
    "empty_q_documentation",
    "first_documentation",
    "filter_documentation",
    "map_documentation",
    "nth_documentation",
    "reduce_documentation",
    "rest_documentation",
    "reverse_documentation",
    
    # Recently converted functions
    "every_q",
    "range_func",
    "some", 
    "sort_fn",
    # Recently converted documentation
    "every_q_doc",
    "range_doc",
    "some_doc",
    "documentation_sort",
]
