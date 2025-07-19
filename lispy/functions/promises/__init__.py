"""LisPy Promise Functions"""

from .promise import promise, promise_doc
from .resolve import resolve, resolve_doc
from .reject import reject, reject_doc
from .promise_all import promise_all, promise_all_doc
from .promise_race import promise_race, promise_race_doc

from .promise_any import builtin_promise_any, documentation_promise_any
from .promise_all_settled import (
    builtin_promise_all_settled,
    documentation_promise_all_settled,
)
from .then import builtin_promise_then, documentation_promise_then
from .on_reject import builtin_on_reject, documentation_on_reject
from .on_complete import builtin_on_complete, documentation_on_complete
from .timeout import builtin_timeout, documentation_timeout
from .with_timeout import builtin_with_timeout, documentation_with_timeout
from .async_map import builtin_async_map, documentation_async_map
from .async_filter import builtin_async_filter, documentation_async_filter
from .async_reduce import builtin_async_reduce, documentation_async_reduce
from .debounce import builtin_debounce, documentation_debounce
from .retry import builtin_retry, documentation_retry
from .throttle import builtin_throttle, documentation_throttle

__all__ = [
    # Functions
    "promise",
    "resolve",
    "reject",
    "promise_all",
    "promise_race",
    "builtin_promise_any",
    "builtin_promise_all_settled",
    "builtin_promise_then",
    "builtin_on_reject",
    "builtin_on_complete",
    "builtin_timeout",
    "builtin_with_timeout",
    "builtin_async_map",
    "builtin_async_filter",
    "builtin_async_reduce",
    "builtin_debounce",
    "builtin_retry",
    "builtin_throttle",
    # Documentation
    "promise_doc",
    "resolve_doc",
    "reject_doc",
    "promise_all_doc",
    "promise_race_doc",
    "documentation_promise_any",
    "documentation_promise_all_settled",
    "documentation_promise_then",
    "documentation_on_reject",
    "documentation_on_complete",
    "documentation_timeout",
    "documentation_with_timeout",
    "documentation_async_map",
    "documentation_async_filter",
    "documentation_async_reduce",
    "documentation_debounce",
    "documentation_retry",
    "documentation_throttle",
]
