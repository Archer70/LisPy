# lispy_project/lispy/functions/__init__.py

from ..environment import Environment  # Import Environment from parent package

# Function imports (alphabetized)
from .abs import builtin_abs, documentation_abs
from .add import builtin_add, documentation_add
from .append import append_fn, documentation_append
from .assoc import builtin_assoc, documentation_assoc
from .bdd_assertions import (
    bdd_assertion_functions,
    documentation_assert_equal_q,
    documentation_assert_true_q,
    documentation_assert_false_q,
    documentation_assert_nil_q,
    documentation_assert_not_nil_q
)
from .is_boolean_q import builtin_is_boolean_q, documentation_is_boolean_q
from .car import builtin_car, documentation_car
from .cdr import builtin_cdr, documentation_cdr
from .concat import concat_fn, documentation_concat
from .conj import builtin_conj, documentation_conj
from .cons import builtin_cons, documentation_cons
from .count import builtin_count, documentation_count
from .dissoc import builtin_dissoc, documentation_dissoc
from .divide import builtin_divide, documentation_divide
from .doc import builtin_doc, documentation_doc, register_documentation
from .empty import builtin_empty_q, documentation_empty_q
from .equals import builtin_equals, documentation_equals
from .equal_q import builtin_equal_q, documentation_equal_q
from .every_q import builtin_every_q, documentation_every_q
from .filter import builtin_filter, documentation_filter
from .first import builtin_first, documentation_first
from .is_function_q import builtin_is_function_q, documentation_is_function_q
from .get import get_fn, documentation_get
from .greater_than import builtin_greater_than, documentation_greater_than
from .greater_than_or_equal import builtin_greater_than_or_equal, documentation_greater_than_or_equal
from .hash_map import builtin_hash_map, documentation_hash_map
from .join import join_fn, documentation_join
from .keys import builtin_keys, documentation_keys
from .less_than import builtin_less_than, documentation_less_than
from .less_than_or_equal import builtin_less_than_or_equal, documentation_less_than_or_equal
from .list import builtin_list, documentation_list
from .is_list_q import builtin_is_list_q, documentation_is_list_q
from .map import builtin_map, documentation_map
from .is_map_q import builtin_is_map_q, documentation_is_map_q
from .max import builtin_max, documentation_max
from .merge import merge_fn, documentation_merge
from .min import builtin_min, documentation_min
from .modulo import builtin_modulo, documentation_modulo
from .multiply import builtin_multiply, documentation_multiply
from .is_nil_q import builtin_is_nil_q, documentation_is_nil_q
from .not_fn import builtin_not, documentation_not
from .nth import nth_fn, documentation_nth
from .is_number_q import builtin_is_number_q, documentation_is_number_q
from .print import builtin_print, documentation_print
from .print_doc import builtin_print_doc, documentation_print_doc
from .println import builtin_println, documentation_println
from .reduce import builtin_reduce, documentation_reduce
from .rest import builtin_rest, documentation_rest
from .reverse import reverse_fn, documentation_reverse
from .some import builtin_some, documentation_some
from .sort import sort_fn, documentation_sort
from .split import split_fn, documentation_split
from .str import str_fn, documentation_str
from .is_string_q import builtin_is_string_q, documentation_is_string_q
from .subtract import builtin_subtract, documentation_subtract
from .vals import builtin_vals, documentation_vals
from .vector import builtin_vector, documentation_vector
from .is_vector_q import builtin_is_vector_q, documentation_is_vector_q


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
    env.define("equal?", builtin_equal_q)
    env.define(">", builtin_greater_than)
    env.define(">=", builtin_greater_than_or_equal)

    # Functions (alphabetized by name)
    env.define("abs", builtin_abs)
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
    env.define("doc", builtin_doc)
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
    env.define("max", builtin_max)
    env.define("merge", merge_fn)
    env.define("min", builtin_min)
    env.define("not", builtin_not)
    env.define("is_nil?", builtin_is_nil_q)
    env.define("nth", nth_fn)
    env.define("is_number?", builtin_is_number_q)
    env.define("print", builtin_print)
    env.define("print-doc", builtin_print_doc)
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

    # Set up documentation registry
    setup_documentation_registry()

    return env


def setup_documentation_registry():
    """Register all documentation functions with their corresponding function names."""
    # Register documentation functions
    register_documentation("*", documentation_multiply)
    register_documentation("+", documentation_add)
    register_documentation("-", documentation_subtract)
    register_documentation("/", documentation_divide)
    register_documentation("<", documentation_less_than)
    register_documentation("<=", documentation_less_than_or_equal)
    register_documentation("=", documentation_equals)
    register_documentation("equal?", documentation_equal_q)
    register_documentation(">", documentation_greater_than)
    register_documentation(">=", documentation_greater_than_or_equal)
    register_documentation("abs", documentation_abs)
    register_documentation("append", documentation_append)
    register_documentation("assoc", documentation_assoc)
    register_documentation("assert-equal?", documentation_assert_equal_q)
    register_documentation("assert-false?", documentation_assert_false_q)
    register_documentation("assert-nil?", documentation_assert_nil_q)
    register_documentation("assert-not-nil?", documentation_assert_not_nil_q)
    register_documentation("assert-true?", documentation_assert_true_q)
    register_documentation("car", documentation_car)
    register_documentation("cdr", documentation_cdr)
    register_documentation("concat", documentation_concat)
    register_documentation("conj", documentation_conj)
    register_documentation("cons", documentation_cons)
    register_documentation("count", documentation_count)
    register_documentation("dissoc", documentation_dissoc)
    register_documentation("doc", documentation_doc)
    register_documentation("empty?", documentation_empty_q)
    register_documentation("every?", documentation_every_q)
    register_documentation("filter", documentation_filter)
    register_documentation("first", documentation_first)
    register_documentation("get", documentation_get)
    register_documentation("hash-map", documentation_hash_map)
    register_documentation("is_boolean?", documentation_is_boolean_q)
    register_documentation("is_function?", documentation_is_function_q)
    register_documentation("is_list?", documentation_is_list_q)
    register_documentation("is_map?", documentation_is_map_q)
    register_documentation("is_nil?", documentation_is_nil_q)
    register_documentation("is_number?", documentation_is_number_q)
    register_documentation("is_string?", documentation_is_string_q)
    register_documentation("is_vector?", documentation_is_vector_q)
    register_documentation("join", documentation_join)
    register_documentation("keys", documentation_keys)
    register_documentation("list", documentation_list)
    register_documentation("map", documentation_map)
    register_documentation("max", documentation_max)
    register_documentation("merge", documentation_merge)
    register_documentation("min", documentation_min)
    register_documentation("%", documentation_modulo)
    register_documentation("not", documentation_not)
    register_documentation("nth", documentation_nth)
    register_documentation("print", documentation_print)
    register_documentation("print-doc", documentation_print_doc)
    register_documentation("println", documentation_println)
    register_documentation("reduce", documentation_reduce)
    register_documentation("rest", documentation_rest)
    register_documentation("reverse", documentation_reverse)
    register_documentation("some", documentation_some)
    register_documentation("sort", documentation_sort)
    register_documentation("split", documentation_split)
    register_documentation("str", documentation_str)
    register_documentation("vals", documentation_vals)
    register_documentation("vector", documentation_vector)


# Create a single global environment instance when the module is loaded.
global_env = create_global_env()

__all__ = [
    "append_fn",
    "builtin_abs",
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
    "builtin_doc",
    "builtin_empty_q",
    "builtin_equals",
    "builtin_equal_q", 
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
    "builtin_max",
    "builtin_min",
    "builtin_modulo",
    "builtin_multiply",
    "builtin_is_nil_q",
    "builtin_not",
    "builtin_is_number_q",
    "builtin_print",
    "builtin_print_doc",
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
