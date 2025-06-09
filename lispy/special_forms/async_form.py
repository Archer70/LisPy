import time
from typing import List, Any, Callable
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise


class AsyncContext:
    """Manages async execution state and simple event loop."""
    
    def __init__(self):
        self.pending_promises = set()
        self.running = False
    
    def register_promise(self, promise: LispyPromise):
        """Register a promise to be tracked by the event loop."""
        if promise.state == "pending":
            self.pending_promises.add(promise)
            # Remove when resolved/rejected
            def cleanup():
                self.pending_promises.discard(promise)
            promise.callbacks.append(cleanup)
    
    def run_until_complete(self, main_promise: LispyPromise):
        """Run event loop until main operation completes."""
        self.running = True
        
        # Register the main promise
        if isinstance(main_promise, LispyPromise):
            self.register_promise(main_promise)
        
        while self.running and (
            (isinstance(main_promise, LispyPromise) and main_promise.state == "pending") or 
            self.pending_promises
        ):
            # Simple event loop - just wait a bit
            time.sleep(0.001)
            
            # Check if main promise is complete
            if isinstance(main_promise, LispyPromise) and main_promise.state != "pending":
                break
        
        self.running = False
        
        if isinstance(main_promise, LispyPromise):
            if main_promise.state == "resolved":
                return main_promise.value
            elif main_promise.state == "rejected":
                raise EvaluationError(f"Async operation failed: {main_promise.error}")
            else:
                return None
        else:
            return main_promise


def handle_async_form(expression: List[Any], env: Environment, evaluate_fn: Callable) -> Any:
    """
    Handle the 'async' special form.
    
    Usage: (async <body>)
    
    Creates an async context and evaluates the body, handling any promises returned.
    """
    if len(expression) != 2:
        raise EvaluationError("SyntaxError: 'async' expects exactly 1 argument (body expression), got {}.".format(len(expression) - 1))
    
    body = expression[1]
    context = AsyncContext()
    
    # Store async context in environment for await to access
    old_context = env.store.get("__async_context__")
    env.define("__async_context__", context)
    
    try:
        # Evaluate body in async context
        result = evaluate_fn(body, env)
        
        # If result is a promise, wait for it
        if isinstance(result, LispyPromise):
            return context.run_until_complete(result)
        else:
            return result
    finally:
        # Clean up async context
        if old_context is not None:
            env.define("__async_context__", old_context)
        elif "__async_context__" in env.store:
            del env.store["__async_context__"] 