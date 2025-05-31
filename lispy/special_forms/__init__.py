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
from .bdd.describe_form import describe_form_handler
from .bdd.it_form import it_form_handler
from .bdd.given_form import given_form_handler
from .bdd.when_form import when_form_handler
from .bdd.then_form import then_form_handler
from .bdd.assert_raises_q_form import assert_raises_q_form_handler

# A registry for special form handlers
# Maps the symbol (as a string) to the handler function
special_form_handlers = {
    "define": handle_define_form,
    "fn": handle_fn_form,
    "if": handle_if_form,
    "let": handle_let_form,
    "quote": handle_quote_form,
    "import": import_form,
    "export": export_form,
    "recur": handle_recur,
    "->": handle_thread_first,
    "describe": describe_form_handler,
    "it": it_form_handler,
    "given": given_form_handler,
    "when": when_form_handler,
    "then": then_form_handler,
    "assert-raises?": assert_raises_q_form_handler,
}

__all__ = ["special_form_handlers"] # Keep __all__ simple for now