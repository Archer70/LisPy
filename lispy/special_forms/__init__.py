# lispy_project/lispy/special_forms/__init__.py
from typing import Dict, Callable, List, Any
from ..environment import Environment # For type hint in handler signature

# Import handler functions
from .define_form import handle_define_form
from .fn_form import handle_fn_form
from .if_form import handle_if_form
from .let_form import handle_let_form
from .quote_form import handle_quote_form
from .import_form import import_form
from .export_form import export_form
from .recur_form import handle_recur
from .thread_first import handle_thread_first
from .cond_form import handle_cond
from .when_form import handle_when_form
from .loop_form import handle_loop_form
from .bdd.describe_form import describe_form_handler
from .bdd.it_form import it_form_handler
from .bdd.given_form import given_form_handler
from .bdd.action_form import action_form_handler
from .bdd.then_form import then_form_handler
from .bdd.assert_raises_q_form import assert_raises_q_form_handler
from .and_form import handle_and_form
from .or_form import handle_or_form

# A registry for special form handlers
# Maps the symbol (as a string) to the handler function
special_form_handlers: Dict[str, Callable[[List[Any], Environment, Callable], Any]] = {
    "define": handle_define_form,
    "fn": handle_fn_form,
    "if": handle_if_form,
    "let": handle_let_form,
    "quote": handle_quote_form,
    "import": import_form,
    "export": export_form,
    "recur": handle_recur,
    "->": handle_thread_first,
    "cond": handle_cond,
    "when": handle_when_form,
    "loop": handle_loop_form,
    "action": action_form_handler,
    "describe": describe_form_handler,
    "it": it_form_handler,
    "given": given_form_handler,
    "then": then_form_handler,
    "assert-raises?": assert_raises_q_form_handler,
    "and": handle_and_form,
    "or": handle_or_form,
}

__all__ = ["special_form_handlers"]