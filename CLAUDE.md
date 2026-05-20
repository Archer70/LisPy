# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
python -m unittest discover -s tests -p '*_test.py'

# Run a single test module
python -m unittest tests.lexer_test
python -m unittest tests.functions.collection.map_test

# Lint
flake8

# Format
black .

# Sort imports
isort .

# Start the REPL
python bin/lispy_interpreter.py --repl

# Run a .lpy file
python bin/lispy_interpreter.py program.lpy

# Run with additional module search paths
python bin/lispy_interpreter.py -I ./lib program.lpy

# Run BDD .lpy tests
python bin/lispy_interpreter.py --bdd "tests/features/**/*.lpy"
```

## Architecture

The interpreter pipeline is: **source text → Lexer → Parser → Evaluator**.

- `lispy/lexer.py` — tokenizes source text
- `lispy/parser.py` — converts tokens into nested Python lists (S-expressions)
- `lispy/evaluator.py` — walks the AST, dispatching to special form handlers or calling built-in/user functions
- `lispy/types.py` — core runtime types: `Symbol`, `Vector`, `LispyList`, `LispyMapLiteral`, `LispyPromise`
- `lispy/environment.py` — lexical scope chain; each `Environment` has an optional `outer` parent
- `lispy/closure.py` — `Function` object that captures params, body, and defining environment
- `lispy/tail_call.py` — `TailCall` sentinel used by the `recur` trampoline in the evaluator
- `lispy/module_system.py` — loads `.lpy` files, resolves search paths, caches modules, detects circular imports
- `lispy/exceptions.py` — `EvaluationError`, `AssertionFailure`, `UserThrownError`

### Special Forms

All special forms live in `lispy/special_forms/`. Each form is a module with a `handle_*` function and a `documentation_*` function. They are registered in the `special_form_handlers` dict in `lispy/special_forms/__init__.py`. A parallel `web_safe_special_form_handlers` dict excludes forms unsafe for server-side use (`import`, `export`, `throw`, `assert-raises?`).

### Built-in Functions

All built-in functions live in `lispy/functions/` organized by category (`math/`, `collection/`, `string/`, `http/`, etc.). Each function uses two decorators from `lispy/functions/decorators.py`:

```python
@lispy_function("map")                         # registers it; add web_safe=False, reason="..." if unsafe
def builtin_map(args, env): ...

@lispy_documentation("map")                    # registers inline docs shown by (doc `map)
def map_documentation() -> str: ...
```

All decorated functions are auto-discovered when the category `__init__.py` is imported. `lispy/functions/__init__.py` imports every category package, so adding a new function file only requires adding it to its category's `__init__.py`.

### Environments: global vs. web-safe

`create_global_env()` builds the full environment. `create_web_safe_env()` starts from the full env and strips unsafe built-ins and swaps in the web-safe special form handlers — use this for untrusted user input.

### BDD Framework

`lispy/bdd/` and `lispy/special_forms/bdd/` implement the `describe`/`it`/`given`/`action`/`then` forms. The runner in `bin/lispy_interpreter.py` handles the `--bdd` flag. BDD assertion functions live in `lispy/functions/bdd_assertions/`.

## Code Style

- Follow PEP 8; run `flake8` and `black` before committing (line-length limit is not enforced — E501 is ignored).
- No magic literals — define named constants.
- Prefer descriptive names over explanatory comments.
- Keep functions short; extract logical units into named helpers.
