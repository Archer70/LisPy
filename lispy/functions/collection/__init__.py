"""LisPy Collection Functions - Partially using decorator-based registration"""

# The functions are now automatically registered via decorators
# Import converted functions to trigger the decorator registration
from .append import append, append_documentation
from .concat import concat, concat_documentation
from .conj import conj, conj_documentation
from .count import count, count_documentation
from .empty import empty_q, empty_q_documentation
from .every_q import every_q, every_q_documentation
from .filter import filter, filter_documentation
from .first import first, first_documentation
from .map import map, map_documentation
from .nth import nth, nth_documentation
from .range import range, range_documentation
from .reduce import reduce, reduce_documentation
from .rest import rest, rest_documentation
from .reverse import reverse, reverse_documentation
from .some import some, some_documentation
from .sort import sort, sort_documentation

__all__ = [
    # Converted functions (new names)
    "append",
    "concat",
    "conj",
    "count",
    "empty_q",
    "first",
    "filter",
    "map",
    "nth",
    "reduce",
    "rest",
    "reverse",
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
    "every_q",
    "range",
    "some",
    "sort",
    "every_q_documentation",
    "range_documentation",
    "some_documentation",
    "sort_documentation",
]
