"""LisPy Map/Dictionary Functions"""

from .assoc import assoc, assoc_doc
from .dissoc import dissoc, dissoc_doc
from .get import get, get_doc
from .hash_map import hash_map, hash_map_doc
from .keys import keys, keys_doc
from .merge import merge, merge_doc
from .vals import vals, vals_doc

__all__ = [
    # Functions
    "assoc",
    "dissoc",
    "hash_map",
    "keys",
    "vals",
    "get",
    "merge",
    # Documentation
    "assoc_doc",
    "dissoc_doc",
    "get_doc",
    "hash_map_doc",
    "keys_doc",
    "merge_doc",
    "vals_doc",
]
