"""LisPy Promise Functions"""

from .promise import promise, promise_doc
from .resolve import resolve, resolve_doc
from .reject import reject, reject_doc
from .promise_all import promise_all, promise_all_doc
from .promise_race import promise_race, promise_race_doc

from .promise_any import promise_any, promise_any_doc
from .promise_all_settled import promise_all_settled, promise_all_settled_doc
from .then import then, then_doc
from .on_reject import on_reject, on_reject_doc
from .on_complete import on_complete, on_complete_doc
from .timeout import timeout, timeout_doc
from .with_timeout import with_timeout, with_timeout_doc
from .async_map import async_map, async_map_doc
from .async_filter import async_filter, async_filter_doc
from .async_reduce import async_reduce, async_reduce_doc
from .debounce import debounce, debounce_doc
from .retry import retry, retry_doc
from .throttle import throttle, throttle_doc

__all__ = [
    # Functions
    "promise",
    "resolve",
    "reject",
    "promise_all",
    "promise_race",
    "promise_any",
    "promise_all_settled",
    "then",
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
    "promise_doc",
    "resolve_doc",
    "reject_doc",
    "promise_all_doc",
    "promise_race_doc",
    "promise_any_doc",
    "promise_all_settled_doc",
    "then_doc",
    "on_reject_doc",
    "on_complete_doc",
    "timeout_doc",
    "with_timeout_doc",
    "async_map_doc",
    "async_filter_doc",
    "async_reduce_doc",
    "debounce_doc",
    "retry_doc",
    "throttle_doc",
]
