# LisPy Custom Types

import threading
from typing import Any, Callable, List, Optional


class Symbol:
    """Represents a Lisp symbol."""

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Symbol('{self.name}')"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.name == other.name
        return False

    def __hash__(self):
        # Symbols are hashable so they can be used as dict keys (e.g. in environments)
        return hash(self.name)


class Vector(list):
    """Represents a Lisp vector, which is self-evaluating.
    Inherits from list for convenience but can be distinctly identified.
    """

    def __repr__(self):
        # Provide a Lisp-like representation for vectors
        return f"[{' '.join(map(repr, self))}]"

    # No need to override __eq__ or __hash__ if list's behavior is fine
    # and vectors are mutable like lists. If they need to be hashable for some reason
    # (e.g., to be keys in LisPy maps, though not typical for vectors),
    # then __hash__ and __eq__ would need careful consideration, likely making them immutable.
    # For now, assume they are mutable sequences like Python lists.


class LispyMapLiteral(dict):
    """Represents a map literal from source code that needs evaluation.
    This is distinct from runtime dictionaries returned by functions.
    """

    pass


class LispyList(list):
    """Represents a Lisp list.
    Inherits from list for convenience and distinct identification.
    """

    def __repr__(self):
        # Provide a Lisp-like representation for lists
        return f"({' '.join(map(repr, self))})"

    # Similar to Vector, assuming mutable sequence behavior from Python lists.
    # If lists needed to be hashable, immutability would be a consideration.


class LispyPromise:
    """Represents an asynchronous operation in LisPy."""

    def __init__(self, executor_fn: Optional[Callable[[], Any]] = None):
        self.state = "pending"  # pending, resolved, rejected
        self.value = None
        self.error = None
        self.callbacks: List[Callable[[], None]] = []

        if executor_fn:
            try:
                # Execute immediately in background thread
                threading.Thread(
                    target=self._execute, args=[executor_fn], daemon=True
                ).start()
            except Exception as e:
                self.reject(e)

    def _execute(self, executor_fn: Callable[[], Any]) -> None:
        """Execute the promise function in a background thread."""
        try:
            result = executor_fn()
            self.resolve(result)
        except Exception as e:
            self.reject(e)

    def resolve(self, value: Any) -> None:
        """Resolve the promise with a value."""
        if self.state == "pending":
            self.state = "resolved"
            self.value = value
            self._notify_callbacks()

    def reject(self, error: Any) -> None:
        """Reject the promise with an error."""
        if self.state == "pending":
            self.state = "rejected"
            self.error = error
            self._notify_callbacks()

    def _notify_callbacks(self) -> None:
        """Notify all registered callbacks."""
        for callback in self.callbacks:
            try:
                callback()
            except Exception as e:
                # Log error but don't let callback failures break the promise
                print(f"Promise callback error: {e}")
        self.callbacks = []

    def then(self, callback: Callable[[Any], Any]) -> "LispyPromise":
        """Chain a callback to be executed when promise resolves."""
        if self.state == "resolved":
            try:
                result = callback(self.value)
                # If callback returns a promise, chain it
                if isinstance(result, LispyPromise):
                    new_promise = LispyPromise()
                    result.then(lambda v: new_promise.resolve(v))
                    result.catch(lambda e: new_promise.reject(e))
                    return new_promise
                else:
                    return self._create_resolved_promise(result)
            except Exception as e:
                return self._create_rejected_promise(e)
        elif self.state == "rejected":
            return self._create_rejected_promise(self.error)
        else:
            new_promise = LispyPromise()
            self.callbacks.append(lambda: self._handle_then(callback, new_promise))
            return new_promise

    def _handle_then(
        self, callback: Callable[[Any], Any], new_promise: "LispyPromise"
    ) -> None:
        """Handle then callback execution."""
        if self.state == "resolved":
            try:
                result = callback(self.value)
                # If callback returns a promise, chain it
                if isinstance(result, LispyPromise):
                    result.then(lambda v: new_promise.resolve(v))
                    result.catch(lambda e: new_promise.reject(e))
                else:
                    new_promise.resolve(result)
            except Exception as e:
                new_promise.reject(e)
        else:
            new_promise.reject(self.error)

    def catch(self, error_callback: Callable[[Any], Any]) -> "LispyPromise":
        """Handle promise rejection."""
        if self.state == "rejected":
            try:
                result = error_callback(self.error)
                return self._create_resolved_promise(result)
            except Exception as e:
                return self._create_rejected_promise(e)
        elif self.state == "resolved":
            return self._create_resolved_promise(self.value)
        else:
            new_promise = LispyPromise()
            self.callbacks.append(
                lambda: self._handle_catch(error_callback, new_promise)
            )
            return new_promise

    def _handle_catch(
        self, error_callback: Callable[[Any], Any], new_promise: "LispyPromise"
    ) -> None:
        """Handle catch callback execution."""
        if self.state == "rejected":
            try:
                result = error_callback(self.error)
                new_promise.resolve(result)
            except Exception as e:
                new_promise.reject(e)
        else:
            new_promise.resolve(self.value)

    def _create_resolved_promise(self, value: Any) -> "LispyPromise":
        """Create a promise that's already resolved."""
        promise = LispyPromise()
        promise.resolve(value)
        return promise

    def _create_rejected_promise(self, error: Any) -> "LispyPromise":
        """Create a promise that's already rejected."""
        promise = LispyPromise()
        promise.reject(error)
        return promise

    def __repr__(self):
        if self.state == "resolved":
            return f"Promise(resolved: {repr(self.value)})"
        elif self.state == "rejected":
            return f"Promise(rejected: {repr(self.error)})"
        else:
            return "Promise(pending)"

    def __str__(self):
        return self.__repr__()
