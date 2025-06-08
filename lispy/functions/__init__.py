# lispy_project/lispy/functions/__init__.py

from ..environment import Environment  # Import Environment from parent package

# Function imports (alphabetized)
from .add import builtin_add
from .append import append_fn
from .assoc import builtin_assoc
from .bdd_assertions import bdd_assertion_functions
from .is_boolean_q import builtin_is_boolean_q
from .car import builtin_car
from .cdr import builtin_cdr
from .concat import concat_fn
from .conj import builtin_conj
from .cons import builtin_cons
from .count import builtin_count
from .dissoc import builtin_dissoc
from .divide import builtin_divide
from .empty import builtin_empty_q
from .equals import builtin_equals
from .every_q import builtin_every_q
from .filter import builtin_filter
from .first import builtin_first
from .is_function_q import builtin_is_function_q
from .get import get_fn
from .greater_than import builtin_greater_than
from .greater_than_or_equal import builtin_greater_than_or_equal
from .hash_map import builtin_hash_map
from .join import join_fn
from .keys import builtin_keys
from .less_than import builtin_less_than
from .less_than_or_equal import builtin_less_than_or_equal
from .list import builtin_list
from .is_list_q import builtin_is_list_q
from .map import builtin_map
from .is_map_q import builtin_is_map_q
from .merge import merge_fn
from .modulo import builtin_modulo
from .multiply import builtin_multiply
from .is_nil_q import builtin_is_nil_q
from .not_fn import builtin_not
from .nth import nth_fn
from .is_number_q import builtin_is_number_q
from .print import builtin_print
from .println import builtin_println
from .reduce import builtin_reduce
from .rest import builtin_rest
from .reverse import reverse_fn
from .some import builtin_some
from .sort import sort_fn
from .split import split_fn
from .str import str_fn
from .is_string_q import builtin_is_string_q
from .subtract import builtin_subtract
from .vals import builtin_vals
from .vector import builtin_vector
from .is_vector_q import builtin_is_vector_q


def create_global_env() -> Environment:
    """Creates and returns the global environment with built-in functions."""
    env = Environment()

    # Mathematical operations (alphabetized by symbol)
    env.define("*", builtin_multiply)
    env.define("+", builtin_add)
    env.define("-", builtin_subtract)
    env.define("/", builtin_divide)
    env.define("%", builtin_modulo)

    # Comparison operations (alphabetized by symbol)
    env.define("<", builtin_less_than)
    env.define("<=", builtin_less_than_or_equal)
    env.define("=", builtin_equals)
    env.define(">", builtin_greater_than)
    env.define(">=", builtin_greater_than_or_equal)

    # Functions (alphabetized by name)
    env.define("append", append_fn)
    env.define("assoc", builtin_assoc)
    env.define("is_boolean?", builtin_is_boolean_q)
    env.define("car", builtin_car)
    env.define("cdr", builtin_cdr)
    env.define("concat", concat_fn)
    env.define("conj", builtin_conj)
    env.define("cons", builtin_cons)
    env.define("count", builtin_count)
    env.define("dissoc", builtin_dissoc)
    env.define("empty?", builtin_empty_q)
    env.define("every?", builtin_every_q)
    env.define("filter", builtin_filter)
    env.define("first", builtin_first)
    env.define("get", get_fn)
    env.define("is_function?", builtin_is_function_q)
    env.define("hash-map", builtin_hash_map)
    env.define("join", join_fn)
    env.define("keys", builtin_keys)
    env.define("list", builtin_list)
    env.define("is_list?", builtin_is_list_q)
    env.define("map", builtin_map)
    env.define("is_map?", builtin_is_map_q)
    env.define("merge", merge_fn)
    env.define("not", builtin_not)
    env.define("is_nil?", builtin_is_nil_q)
    env.define("nth", nth_fn)
    env.define("is_number?", builtin_is_number_q)
    env.define("print", builtin_print)
    env.define("println", builtin_println)
    env.define("reduce", builtin_reduce)
    env.define("rest", builtin_rest)
    env.define("reverse", reverse_fn)
    env.define("some", builtin_some)
    env.define("sort", sort_fn)
    env.define("split", split_fn)
    env.define("str", str_fn)
    env.define("is_string?", builtin_is_string_q)
    env.define("vals", builtin_vals)
    env.define("vector", builtin_vector)
    env.define("is_vector?", builtin_is_vector_q)

    # Add BDD assertion functions
    for name, func in bdd_assertion_functions.items():
        env.define(name, func)

    return env


# Create a single global environment instance when the module is loaded.
global_env = create_global_env()

__all__ = [
    "append_fn",
    "builtin_add",
    "builtin_assoc",
    "builtin_is_boolean_q",
    "builtin_car",
    "builtin_cdr",
    "builtin_conj",
    "builtin_cons",
    "builtin_count",
    "builtin_dissoc",
    "builtin_divide",
    "builtin_empty_q",
    "builtin_equals",
    "builtin_every_q",
    "builtin_filter",
    "builtin_first",
    "builtin_is_function_q",
    "builtin_greater_than",
    "builtin_greater_than_or_equal",
    "builtin_hash_map",
    "builtin_keys",
    "builtin_less_than",
    "builtin_less_than_or_equal",
    "builtin_list",
    "builtin_is_list_q",
    "builtin_map",
    "builtin_is_map_q",
    "builtin_modulo",
    "builtin_multiply",
    "builtin_is_nil_q",
    "builtin_not",
    "builtin_is_number_q",
    "builtin_print",
    "builtin_println",
    "builtin_reduce",
    "builtin_rest",
    "builtin_some",
    "builtin_is_string_q",
    "builtin_subtract",
    "builtin_vals",
    "builtin_vector",
    "builtin_is_vector_q",
    "concat_fn",
    "create_global_env",
    "get_fn",
    "global_env",
    "join_fn",
    "merge_fn",
    "nth_fn",
    "reverse_fn",
    "sort_fn",
    "split_fn",
    "str_fn",
]
