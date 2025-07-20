"""LisPy Promise Functions"""

from .async_filter import async_filter, async_filter_documentation
from .async_map import async_map, async_map_documentation
from .async_reduce import async_reduce, async_reduce_documentation
from .debounce import debounce, debounce_documentation
from .on_complete import on_complete, on_complete_documentation
from .on_reject import on_reject, on_reject_documentation
from .promise import promise, promise_documentation
from .promise_all import promise_all, promise_all_documentation
from .promise_all_settled import (promise_all_settled,
                                  promise_all_settled_documentation)
from .promise_any import promise_any, promise_any_documentation
from .promise_race import promise_race, promise_race_documentation
from .reject import reject, reject_documentation
from .resolve import resolve, resolve_documentation
from .retry import retry, retry_documentation
from .then import promise_then, promise_then_documentation
from .throttle import throttle, throttle_documentation
from .timeout import timeout, timeout_documentation
from .with_timeout import with_timeout, with_timeout_documentation

__all__ = [
    # Functions
    "promise",
    "resolve",
    "reject",
    "promise_all",
    "promise_race",
    "promise_any",
    "promise_all_settled",
    "promise_then",
    "on_reject",
    "on_complete",
    "timeout",
    "with_timeout",
    "async_map",
    "async_filter",
    "async_reduce",
    "debounce",
    "retry",
    "throttle",
    # Documentation
    "promise_documentation",
    "resolve_documentation",
    "reject_documentation",
    "promise_all_documentation",
    "promise_race_documentation",
    "promise_any_documentation",
    "promise_all_settled_documentation",
    "promise_then_documentation",
    "on_reject_documentation",
    "on_complete_documentation",
    "timeout_documentation",
    "with_timeout_documentation",
    "async_map_documentation",
    "async_filter_documentation",
    "async_reduce_documentation",
    "debounce_documentation",
    "retry_documentation",
    "throttle_documentation",
]
