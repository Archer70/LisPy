"""LisPy Collection Functions"""

from .append import append_fn, documentation_append
from .concat import concat_fn, documentation_concat
from .conj import builtin_conj, documentation_conj
from .count import builtin_count, documentation_count
from .empty import builtin_empty_q, documentation_empty_q
from .every_q import builtin_every_q, documentation_every_q
from .filter import builtin_filter, documentation_filter
from .first import builtin_first, documentation_first
from .map import builtin_map, documentation_map
from .nth import nth_fn, documentation_nth
from .reduce import builtin_reduce, documentation_reduce
from .rest import builtin_rest, documentation_rest
from .reverse import reverse_fn, documentation_reverse
from .some import builtin_some, documentation_some
from .sort import sort_fn, documentation_sort

__all__ = [
    # Functions
    "append_fn",
    "builtin_conj",
    "builtin_count",
    "builtin_empty_q",
    "builtin_every_q",
    "builtin_filter",
    "builtin_first",
    "builtin_map",
    "builtin_reduce",
    "builtin_rest",
    "builtin_some",
    "concat_fn",
    "nth_fn",
    "reverse_fn",
    "sort_fn",
    # Documentation
    "documentation_append",
    "documentation_concat",
    "documentation_conj",
    "documentation_count",
    "documentation_empty_q",
    "documentation_every_q",
    "documentation_filter",
    "documentation_first",
    "documentation_map",
    "documentation_nth",
    "documentation_reduce",
    "documentation_rest",
    "documentation_reverse",
    "documentation_some",
    "documentation_sort",
] 