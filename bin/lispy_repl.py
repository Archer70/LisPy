#!/usr/bin/env python3
"""LisPy REPL Functionality"""

import sys
import os
import re # For improved word extraction
from pathlib import Path

# Add the project root to Python path if not already (e.g. when run directly)
# This allows importing lispy modules directly if this script is in bin/
if __name__ == '__main__' and os.path.basename(os.getcwd()) == 'bin':
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
elif __name__ == '__main__': # If run from project root
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root.parent))

from lispy.exceptions import EvaluationError, ParseError, LexerError
from lispy.utils import run_lispy_string
from lispy.environment import Environment # Corrected import
from lispy.lexer import tokenize as lispy_tokenize # For _check_buffer_completeness

# Import for dynamic loading of known symbols
from lispy.special_forms import special_form_handlers
# from lispy.functions import global_env_vars # This was incorrect, built-ins are in the env itself

# For prompt_toolkit integration
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.lexers import PygmentsLexer # For syntax highlighting
from pygments.lexers.lisp import SchemeLexer    # Using SchemeLexer as a base for LisPy
from prompt_toolkit.completion import Completer, Completion, WordCompleter # Added for completion

INDENT_UNIT = "  " # 2 spaces for indentation

# --- Custom Completer for LisPy ---
class LispyCompleter(Completer):
    """Custom completer for LisPy keywords, functions, and variables."""
    def __init__(self, environment: Environment):
        self.environment = environment # The REPL environment, pre-populated with built-ins
        self.known_constructs = set()

        # Dynamically load special forms names
        if special_form_handlers:
            self.known_constructs.update(special_form_handlers.keys())

        # Built-in functions are already in the self.environment.store by the time REPL starts,
        # so they will be picked up by the available_env_symbols logic in get_completions.
        # We just need to add core literals and any other keywords not part of special forms or built-ins.
        
        core_literals_and_keywords = {
            "true", "false", "nil",
            # BDD Keywords - kept here for now
            "describe", "feature", "it", "scenario", "given", "when", "then",
            "assert-equal?", "assert-true?", "assert-false?", "assert-nil?", "assert-not-nil?", "assert-raises?"
        }
        self.known_constructs.update(core_literals_and_keywords)

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        
        # Regex to find the word to complete. 
        # A LisPy symbol can contain many characters. This regex attempts to capture typical symbol characters.
        # It tries to find a sequence of valid symbol characters at the end of the string, OR
        # a sequence of valid symbol characters preceded by a delimiter ('(', '[', '{', or space).
        # Valid symbol chars: alphanumeric, and many common Lisp special chars.
        # Excludes: whitespace, (), [], {}, \"\'`,; (common delimiters or special meaning)
        # The character class for symbols: [a-zA-Z0-9_\-+*/=<>!?.:$%^&~]
        # Python raw strings r'...' are used. Backslashes for regex special chars (like \\s, \\[) are needed.
        # Literal backslashes in the character class must be escaped as \\\\.
        # The single quote \' is included as a valid symbol character here.
        match = re.search(r"([a-zA-Z0-9_\-+*/=<>!?.:$%^&~\'\"]+)\Z|(?<=[\s(\[{])([a-zA-Z0-9_\-+*/=<>!?.:$%^&~\'\"]*)\Z", text_before_cursor)
        word_to_complete = ""
        if match:
            # match.group(1) is for the first part of | (ending non-delimiter sequence)
            # match.group(2) is for the second part of | (sequence after a delimiter)
            word_to_complete = match.group(1) or match.group(2) or "" 

        provide_all_if_starts_new_symbol = False
        # If word_to_complete is empty and the character immediately before cursor is an opening delimiter or space.
        if not word_to_complete and text_before_cursor and text_before_cursor[-1] in ('(', '[', '{', ' '):
            provide_all_if_starts_new_symbol = True

        if word_to_complete or provide_all_if_starts_new_symbol:
            available_env_symbols = set()
            env = self.environment # This env includes built-ins and user-defined vars
            while env is not None:
                available_env_symbols.update(env.store.keys())
                env = env.outer
            
            # Suggestions will be a combination of known_constructs (special forms, core literals, BDD keywords)
            # and all symbols from the environment (which includes built-ins and user vars).
            current_suggestions = self.known_constructs.copy() 
            current_suggestions.update(available_env_symbols) 

            for suggestion in sorted(list(current_suggestions)):
                if provide_all_if_starts_new_symbol or suggestion.startswith(word_to_complete):
                    # start_position should be negative length of the part to be replaced
                    yield Completion(suggestion, start_position=-len(word_to_complete))

class LispyRepl:
    """Handles the LisPy Read-Eval-Print Loop (REPL) with history, multi-line input, syntax highlighting, and tab completion."""

    def __init__(self, env: Environment):
        """Initialize the REPL with a given environment, history, lexer, and completer."""
        self.env = env
        self.history = InMemoryHistory()
        self.lexer = PygmentsLexer(SchemeLexer) # Added for syntax highlighting
        self.completer = LispyCompleter(self.env) # Instantiate our custom completer
        self.session = PromptSession(
            history=self.history, 
            lexer=self.lexer, 
            completer=self.completer # Pass completer to session
        )

    def _check_buffer_completeness(self, buffer_string: str) -> tuple[bool, int]:
        """
        Checks if the input buffer string forms one or more complete LisPy expressions.
        Returns a tuple: (is_complete_or_definitely_malformed, open_delimiter_count).
        'is_complete_or_definitely_malformed' is True if parens are balanced or 
        there's a non-unterminated-string lexer error.
        'open_delimiter_count' is > 0 if incomplete, 0 if balanced or error.
        Can be negative if there are too many closing delimiters, handled by caller for indent.
        """
        stripped_buffer = buffer_string.strip()
        if not stripped_buffer:
            return True, 0

        try:
            tokens = lispy_tokenize(stripped_buffer)
        except LexerError as e:
            if str(e).startswith("Unterminated string"):
                return False, 1 # Heuristic for open item
            return True, 0 

        depth = 0
        for token_type, _ in tokens:
            if token_type in ['LPAREN', 'LBRACKET', 'LBRACE']:
                depth += 1
            elif token_type in ['RPAREN', 'RBRACKET', 'RBRACE']:
                depth -= 1
        return depth == 0, depth

    def start_repl(self):
        """Start an interactive Read-Eval-Print Loop with multi-line input, history, syntax highlighting, and tab completion."""
        print("LisPy Interactive Interpreter (Multi-line, History, Highlighting, Completion, Auto-Indent Guide enabled)")
        print("Type expressions to evaluate. Use Up/Down arrows for history. Press Tab for completions.")
        print("Enter an empty line to attempt completion if ambiguous.")
        print("Use (import \"module-name\") to load modules, 'exit' or '(exit)' to quit.")
        print()

        input_buffer = []
        # current_indent_level stores the number of INDENT_UNITs for the *next* line if continuing
        current_indent_level = 0 

        while True: # Outer loop for each full command
            # Reset buffer and indent for a new independent command
            if not input_buffer: # Only reset if buffer was cleared (new command or after processing)
                current_indent_level = 0

            prompt_prefix = ""
            if not input_buffer: # First line of a potential command
                prompt_message = "lispy> "
            else: # Continuation line
                # Indent based on the level determined from the *previous* line's incompleteness
                # Ensure indent_level is not negative for the string multiplication
                actual_indent_units = max(0, current_indent_level)
                prompt_prefix = INDENT_UNIT * actual_indent_units
                prompt_message = f"{prompt_prefix}  ...> "
            
            try:
                # Use prompt_toolkit session for input
                line_input = self.session.prompt(prompt_message)
            except KeyboardInterrupt: # Ctrl-C: clear current input or exit if buffer empty
                if not input_buffer: # If at fresh prompt, exit
                    print("Goodbye! (Ctrl-C at fresh prompt)")
                    return
                else: # If in middle of multi-line, clear buffer and restart line input
                    print(" (Input cleared)")
                    input_buffer = []
                    current_indent_level = 0
                    continue 
            except EOFError: # Ctrl-D
                if not input_buffer or not "".join(input_buffer).strip(): # exit if buffer is empty
                    print("\nGoodbye! (Ctrl-D)")
                    return
                else: # If buffer has content, try to execute it (like a final Enter)
                    print(" (Ctrl-D, attempting to execute buffer)")
                    # This makes Ctrl-D act like submitting the current buffer
                    # The loop will then process full_input_string
                    pass # Allow execution of current buffer

            if not input_buffer and line_input.strip().lower() in ['exit', 'quit', '(exit)', '(quit)']:
                print("Goodbye!")
                return
            
            input_buffer.append(line_input)
            full_input_string = " ".join(input_buffer)

            # Handle case where user just hits enter on a blank line at the main prompt
            if not full_input_string.strip() and len(input_buffer) == 1:
                input_buffer = [] # Reset for a fresh "lispy> " prompt
                current_indent_level = 0
                continue # Restart inner logic for prompt generation

            is_complete, open_delims = self._check_buffer_completeness(full_input_string)

            if is_complete:
                # Attempt to submit if: 
                # 1. The buffer is lexically complete (open_delims <= 0).
                # 2. Or, an empty line was entered, signifying user wants to try submitting.
                #    (But only if there's actual content in the buffer to submit).
                should_submit = (open_delims <= 0) or \
                                (line_input.strip() == "" and full_input_string.strip() != "") or \
                                (isinstance(line_input, str) and line_input == "")
                
                if should_submit:
                    final_code_to_run = full_input_string.strip()
                    input_buffer = [] # Clear buffer for next command
                    current_indent_level = 0 # Reset indent for next command

                    if not final_code_to_run: # If it ended up being empty (e.g. multiple blank lines)
                        continue # Get a fresh "lispy> " prompt

                    try:
                        # History is added automatically by prompt_toolkit if non-empty and not just whitespace
                        # We might want to add it explicitly if it was a multi-line that resolved via EOF/Ctrl-D
                        # However, session.prompt already adds to history upon successful read.
                        result = run_lispy_string(final_code_to_run, self.env)
                        if result is not None:
                            print(f"=> {result}")
                    except (LexerError, ParseError, EvaluationError) as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Unexpected REPL error: {type(e).__name__}: {e}")
                    continue # To the outer while True for a new command cycle
                else:
                    # is_complete is true, but open_delims > 0 (e.g. LexerError not unterminated string)
                    # or empty line was hit but buffer not considered submittable yet. 
                    # This path might be tricky. Let's simplify: if is_complete is true, we try to submit.
                    # The previous `should_submit` logic should cover it.
                    # If not submitting, it means we need more input, so set indent level.
                    current_indent_level = max(0, open_delims) # For the next line
            else: # Not complete
                current_indent_level = max(0, open_delims) # Set indent for the next line
                # Loop continues for more input

if __name__ == '__main__':
    # This allows running the REPL directly for testing
    print("(Running LisPy REPL directly for development testing)")
    from lispy.functions import create_global_env # Correct: create_global_env is in functions
    
    # Setup project root for module loading if run directly
    # This is a bit redundant with top-level path setup but ensures context for direct run.
    module_test_dir = Path(__file__).parent.parent.resolve()
    sys.path.insert(0, str(module_test_dir))
    # print(f"Sys.path for direct run: {sys.path}")

    global_env = create_global_env()
    
    # Example: Add current dir to load path for direct testing of (import "some_local_module")
    # from lispy.module_system import get_module_loader
    # get_module_loader().add_load_path(str(Path.cwd()))


    repl = LispyRepl(global_env)
    repl.start_repl() 