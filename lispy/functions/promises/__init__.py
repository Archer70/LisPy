"""LisPy Promise Functions"""

from .promise import builtin_promise, documentation_promise
from .resolve import builtin_resolve, documentation_resolve
from .reject import builtin_reject, documentation_reject
from .promise_all import builtin_promise_all, documentation_promise_all
from .promise_race import builtin_promise_race, documentation_promise_race
from .delay import builtin_delay, documentation_delay
from .promise_any import builtin_promise_any, documentation_promise_any
from .promise_all_settled import builtin_promise_all_settled, documentation_promise_all_settled
from .then import builtin_promise_then, documentation_promise_then
from .on_reject import builtin_on_reject, documentation_on_reject
from .on_complete import builtin_on_complete, documentation_on_complete
from .timeout import builtin_timeout, documentation_timeout
from .with_timeout import builtin_with_timeout, documentation_with_timeout

__all__ = [
    # Functions
    "builtin_promise",
    "builtin_resolve", 
    "builtin_reject",
    "builtin_promise_all",
    "builtin_promise_race",
    "builtin_promise_any",
    "builtin_promise_all_settled",
    "builtin_delay",
    "builtin_promise_then",
    "builtin_on_reject",
    "builtin_on_complete",
    "builtin_timeout",
    "builtin_with_timeout",
    # Documentation
    "documentation_promise",
    "documentation_resolve",
    "documentation_reject",
    "documentation_promise_all",
    "documentation_promise_race",
    "documentation_promise_any",
    "documentation_promise_all_settled",
    "documentation_delay",
    "documentation_promise_then",
    "documentation_on_reject",
    "documentation_on_complete",
    "documentation_timeout",
    "documentation_with_timeout",
] 