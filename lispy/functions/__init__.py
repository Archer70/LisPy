# lispy_project/lispy/functions/__init__.py

from ..environment import Environment  # Import Environment from parent package

# Math functions
from .math import (
    builtin_abs,
    documentation_abs,
    builtin_add,
    documentation_add,
    builtin_divide,
    documentation_divide,
    builtin_equals,
    documentation_equals,
    builtin_max,
    documentation_max,
    builtin_min,
    documentation_min,
    builtin_modulo,
    documentation_modulo,
    builtin_multiply,
    documentation_multiply,
    builtin_subtract,
    documentation_subtract,
)

# Logical functions
from .logical import (
    builtin_equal_q,
    documentation_equal_q,
    builtin_greater_than,
    documentation_greater_than,
    builtin_greater_than_or_equal,
    documentation_greater_than_or_equal,
    builtin_less_than,
    documentation_less_than,
    builtin_less_than_or_equal,
    documentation_less_than_or_equal,
    builtin_not,
    documentation_not,
)

# Type checking functions
from .type_check import (
    builtin_is_boolean_q,
    documentation_is_boolean_q,
    builtin_is_function_q,
    documentation_is_function_q,
    builtin_is_list_q,
    documentation_is_list_q,
    builtin_is_map_q,
    documentation_is_map_q,
    builtin_is_nil_q,
    documentation_is_nil_q,
    builtin_is_number_q,
    documentation_is_number_q,
    builtin_is_string_q,
    documentation_is_string_q,
    builtin_is_vector_q,
    documentation_is_vector_q,
)

# Collection functions
from .collection import (
    append_fn,
    documentation_append,
    builtin_conj,
    documentation_conj,
    builtin_count,
    documentation_count,
    builtin_empty_q,
    documentation_empty_q,
    builtin_every_q,
    documentation_every_q,
    builtin_filter,
    documentation_filter,
    builtin_first,
    documentation_first,
    builtin_map,
    documentation_map,
    builtin_range,
    documentation_range,
    builtin_reduce,
    documentation_reduce,
    builtin_rest,
    documentation_rest,
    builtin_some,
    documentation_some,
    concat_fn,
    documentation_concat,
    nth_fn,
    documentation_nth,
    reverse_fn,
    documentation_reverse,
    sort_fn,
    documentation_sort,
)

# Map/Dictionary functions
from .map import (
    builtin_assoc,
    documentation_assoc,
    builtin_dissoc,
    documentation_dissoc,
    builtin_hash_map,
    documentation_hash_map,
    builtin_keys,
    documentation_keys,
    builtin_vals,
    documentation_vals,
    get_fn,
    documentation_get,
    merge_fn,
    documentation_merge,
)

# List/Sequence functions
from .list import (
    builtin_car,
    documentation_car,
    builtin_cdr,
    documentation_cdr,
    builtin_cons,
    documentation_cons,
    builtin_list,
    documentation_list,
    builtin_vector,
    documentation_vector,
)

# I/O functions
from .io import (
    builtin_print,
    documentation_print,
    builtin_println,
    documentation_println,
    builtin_read_line,
    documentation_read_line,
    builtin_slurp,
    documentation_slurp,
    builtin_spit,
    documentation_spit,
)

# String functions
from .string import (
    join_fn,
    documentation_join,
    split_fn,
    documentation_split,
)

# Type conversion functions
from .typing import (
    to_str_fn,
    documentation_str,
    to_int_fn,
    documentation_to_int,
    to_float_fn,
    documentation_to_float,
    to_bool_fn,
    documentation_to_bool,
)

# Promise functions
from .promises import (
    builtin_promise,
    documentation_promise,
    builtin_resolve,
    documentation_resolve,
    builtin_reject,
    documentation_reject,
    builtin_promise_all,
    documentation_promise_all,
    builtin_promise_race,
    documentation_promise_race,
    builtin_promise_any,
    documentation_promise_any,
    builtin_promise_all_settled,
    documentation_promise_all_settled,
    builtin_promise_then,
    documentation_promise_then,
    builtin_on_reject,
    documentation_on_reject,
    builtin_on_complete,
    documentation_on_complete,
    builtin_timeout,
    documentation_timeout,
    builtin_with_timeout,
    documentation_with_timeout,
    builtin_async_map,
    documentation_async_map,
    builtin_async_filter,
    documentation_async_filter,
    builtin_async_reduce,
    documentation_async_reduce,
    builtin_debounce,
    documentation_debounce,
    builtin_retry,
    documentation_retry,
    builtin_throttle,
    documentation_throttle,
)

# Other function imports (alphabetized)
from .bdd_assertions import (
    bdd_assertion_functions,
    documentation_assert_equal_q,
    documentation_assert_true_q,
    documentation_assert_false_q,
    documentation_assert_nil_q,
    documentation_assert_not_nil_q,
)
from .doc import builtin_doc, documentation_doc, register_documentation
from .print_doc import builtin_print_doc, documentation_print_doc

# Import documentation functions for special forms
from ..special_forms import (
    documentation_and,
    documentation_async,
    documentation_await,
    documentation_cond,
    documentation_define,
    documentation_defn_async,
    documentation_doseq,
    documentation_export,
    documentation_fn,
    documentation_if,
    documentation_import,
    documentation_let,
    documentation_loop,
    documentation_or,
    documentation_quote,
    documentation_recur,
    documentation_thread_first,
    documentation_thread_last,
    documentation_throw,
    documentation_try,
    documentation_when
)


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
    env.define("async-filter", builtin_async_filter)
    env.define("async-map", builtin_async_map)
    env.define("async-reduce", builtin_async_reduce)
    env.define("is_boolean?", builtin_is_boolean_q)
    env.define("car", builtin_car)
    env.define("cdr", builtin_cdr)
    env.define("concat", concat_fn)
    env.define("conj", builtin_conj)
    env.define("cons", builtin_cons)
    env.define("count", builtin_count)
    env.define("debounce", builtin_debounce)
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
    env.define("on-complete", builtin_on_complete)
    env.define("on-reject", builtin_on_reject)
    env.define("print", builtin_print)
    env.define("print-doc", builtin_print_doc)
    env.define("println", builtin_println)
    env.define("promise", builtin_promise)
    env.define("promise-all", builtin_promise_all)
    env.define("promise-race", builtin_promise_race)
    env.define("promise-any", builtin_promise_any)
    env.define("promise-all-settled", builtin_promise_all_settled)
    env.define("range", builtin_range)
    env.define("read-line", builtin_read_line)
    env.define("reduce", builtin_reduce)
    env.define("reject", builtin_reject)
    env.define("resolve", builtin_resolve)
    env.define("retry", builtin_retry)
    env.define("throttle", builtin_throttle)
    env.define("slurp", builtin_slurp)
    env.define("spit", builtin_spit)
    env.define("rest", builtin_rest)
    env.define("reverse", reverse_fn)
    env.define("some", builtin_some)
    env.define("sort", sort_fn)
    env.define("split", split_fn)
    env.define("str", to_str_fn)
    env.define("is_string?", builtin_is_string_q)
    env.define("timeout", builtin_timeout)
    env.define("promise-then", builtin_promise_then)
    env.define("vals", builtin_vals)
    env.define("with-timeout", builtin_with_timeout)
    env.define("vector", builtin_vector)
    env.define("is_vector?", builtin_is_vector_q)
    env.define("to-str", to_str_fn)
    env.define("to-int", to_int_fn)
    env.define("to-float", to_float_fn)
    env.define("to-bool", to_bool_fn)

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
    register_documentation("async-filter", documentation_async_filter)
    register_documentation("async-map", documentation_async_map)
    register_documentation("async-reduce", documentation_async_reduce)
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
    register_documentation("debounce", documentation_debounce)
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
    register_documentation("on-complete", documentation_on_complete)
    register_documentation("on-reject", documentation_on_reject)
    register_documentation("print", documentation_print)
    register_documentation("print-doc", documentation_print_doc)
    register_documentation("println", documentation_println)
    register_documentation("promise", documentation_promise)
    register_documentation("promise-all", documentation_promise_all)
    register_documentation("promise-race", documentation_promise_race)
    register_documentation("promise-any", documentation_promise_any)
    register_documentation("promise-all-settled", documentation_promise_all_settled)
    register_documentation("range", documentation_range)
    register_documentation("read-line", documentation_read_line)
    register_documentation("reduce", documentation_reduce)
    register_documentation("reject", documentation_reject)
    register_documentation("resolve", documentation_resolve)
    register_documentation("retry", documentation_retry)
    register_documentation("throttle", documentation_throttle)
    register_documentation("slurp", documentation_slurp)
    register_documentation("spit", documentation_spit)
    register_documentation("rest", documentation_rest)
    register_documentation("reverse", documentation_reverse)
    register_documentation("some", documentation_some)
    register_documentation("sort", documentation_sort)
    register_documentation("split", documentation_split)
    register_documentation("str", documentation_str)
    register_documentation("timeout", documentation_timeout)
    register_documentation("promise-then", documentation_promise_then)
    register_documentation("vals", documentation_vals)
    register_documentation("with-timeout", documentation_with_timeout)
    register_documentation("vector", documentation_vector)
    register_documentation("to-str", documentation_str)
    register_documentation("to-int", documentation_to_int)
    register_documentation("to-float", documentation_to_float)
    register_documentation("to-bool", documentation_to_bool)
    
    # Register special form documentation
    register_documentation("->", documentation_thread_first)
    register_documentation("->>", documentation_thread_last)
    register_documentation("and", documentation_and)
    register_documentation("async", documentation_async)
    register_documentation("await", documentation_await)
    register_documentation("cond", documentation_cond)
    register_documentation("define", documentation_define)
    register_documentation("defn-async", documentation_defn_async)
    register_documentation("doseq", documentation_doseq)
    register_documentation("export", documentation_export)
    register_documentation("fn", documentation_fn)
    register_documentation("if", documentation_if)
    register_documentation("import", documentation_import)
    register_documentation("let", documentation_let)
    register_documentation("loop", documentation_loop)
    register_documentation("or", documentation_or)
    register_documentation("quote", documentation_quote)
    register_documentation("recur", documentation_recur)
    register_documentation("throw", documentation_throw)
    register_documentation("try", documentation_try)
    register_documentation("when", documentation_when)


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
    "to_str_fn",
]
