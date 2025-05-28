# lispy_project/lispy/functions/__init__.py

from ..environment import Environment # Import Environment from parent package
from ..types import LispyList, Vector, Symbol # Changed List to LispyList

from .add import builtin_add
from .subtract import builtin_subtract
from .multiply import builtin_multiply
from .divide import builtin_divide
from .modulo import builtin_modulo
from .equals import builtin_equals
from .greater_than import builtin_greater_than
from .less_than import builtin_less_than
from .greater_than_or_equal import builtin_greater_than_or_equal
from .less_than_or_equal import builtin_less_than_or_equal
from .not_fn import builtin_not
from .list import builtin_list
from .cons import builtin_cons
from .car import builtin_car
from .cdr import builtin_cdr
from .empty import builtin_empty_q
from .count import builtin_count
from .get import get_fn # Import the new get function
from .vector import builtin_vector # Changed from vector_fn and renamed function
from .hash_map import builtin_hash_map # Changed from hash_map_fn and renamed function
from .first import builtin_first
from .rest import builtin_rest
from .conj import builtin_conj
from .assoc import builtin_assoc
from .dissoc import builtin_dissoc
from .keys import builtin_keys
from .vals import builtin_vals # Added vals
from .print import builtin_print
from .println import builtin_println

def create_global_env() -> Environment:
    """Creates and returns the global environment with built-in functions."""
    env = Environment()
    env.define("+", builtin_add)
    env.define("-", builtin_subtract)
    env.define("*", builtin_multiply)
    env.define("/", builtin_divide)
    env.define("%", builtin_modulo)
    env.define("=", builtin_equals)
    env.define(">", builtin_greater_than)
    env.define("<", builtin_less_than)
    env.define(">=", builtin_greater_than_or_equal)
    env.define("<=", builtin_less_than_or_equal)
    env.define("not", builtin_not)
    env.define("list", builtin_list)
    env.define("cons", builtin_cons)
    env.define("car", builtin_car)
    env.define("cdr", builtin_cdr)
    env.define("empty?", builtin_empty_q)
    env.define("count", builtin_count)
    env.define("get", get_fn) # Add get to the environment
    env.define("vector", builtin_vector) # Renamed from builtin_vector_fn
    env.define("hash-map", builtin_hash_map) # Renamed from builtin_hash_map_fn
    env.define("first", builtin_first)
    env.define("rest", builtin_rest)
    env.define("conj", builtin_conj)
    env.define("assoc", builtin_assoc)
    env.define("dissoc", builtin_dissoc)
    env.define("keys", builtin_keys)
    env.define("vals", builtin_vals) # Added vals
    env.define("print", builtin_print)
    env.define("println", builtin_println)
    return env

# Create a single global environment instance when the module is loaded.
global_env = create_global_env()

__all__ = [
    "builtin_add",
    "builtin_subtract",
    "builtin_multiply",
    "builtin_divide",
    "builtin_modulo",
    "builtin_equals",
    "builtin_greater_than",
    "builtin_less_than",
    "builtin_greater_than_or_equal",
    "builtin_less_than_or_equal",
    "builtin_not",
    "builtin_list",
    "builtin_cons",
    "builtin_car",
    "builtin_cdr",
    "builtin_empty_q",
    "builtin_count",
    "get_fn", # Add get_fn to __all__
    "builtin_vector", # Renamed from builtin_vector_fn
    "builtin_hash_map", # Renamed from builtin_hash_map_fn
    "builtin_first",
    "builtin_rest",
    "builtin_conj",
    "builtin_assoc",
    "builtin_dissoc",
    "builtin_keys",
    "builtin_vals", # Added vals
    "builtin_print",
    "builtin_println",
    "create_global_env",
    "global_env",
] 