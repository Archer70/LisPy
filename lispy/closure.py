from typing import List, Any
from .environment import Environment
from .types import Symbol # For parameter type hint

class Function:
    """
    Represents a user-defined function (a closure).
    It captures the parameters, body, and the defining environment.
    """
    def __init__(self, params: List[Symbol], body: List[Any], defining_env: Environment):
        self.params: List[Symbol] = params # List of Symbol objects for parameters
        self.body: List[Any] = body        # List of expressions forming the function body
        self.defining_env: Environment = defining_env # The environment captured at definition time

    def __repr__(self) -> str:
        param_names = [p.name for p in self.params]
        # To avoid overly long repr, maybe just show the number of body expressions
        # or a snippet of the first one if complex. For now, just param names.
        return f"<UserDefinedFunction params:({', '.join(param_names)})>"

    def __call__(self, *args: Any) -> Any:
        # This method is primarily to make Function instances satisfy Python's `callable()`.
        # The actual execution logic (creating new env, binding params, evaluating body)
        # will be handled by the `evaluate` function in `evaluator.py` when it
        # encounters a `Function` instance as the operator in a call.
        # This avoids circular dependencies between `closure.py` and `evaluator.py`.
        
        # If we were to make this directly executable from Python for some reason,
        # it would need access to the `evaluate` function.
        # For LisPy's evaluation loop, `evaluator.py` will drive the execution.
        raise NotImplementedError(
            "UserDefinedFunction instances are called by the LisPy evaluator, not directly in Python."
        ) 