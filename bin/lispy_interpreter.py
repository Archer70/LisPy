#!/usr/bin/env python3
"""
LisPy Interpreter - Command-line interface for running LisPy programs

Usage:
    python lispy_interpreter.py [file.lpy]           # Run a LisPy file
    python lispy_interpreter.py                      # Start REPL mode
    python lispy_interpreter.py --help               # Show help
"""

import sys
import os
import argparse
from pathlib import Path

# Add the project root to Python path so we can import lispy modules
project_root = Path(__file__).parent.parent  # Go up one level from bin/ to project root
sys.path.insert(0, str(project_root))

from lispy.lexer import tokenize
from lispy.parser import parse
from lispy.evaluator import evaluate
from lispy.functions import create_global_env
from lispy.module_system import get_module_loader, set_current_module, Module
from lispy.exceptions import EvaluationError, ParseError, LexerError
from lispy.utils import run_lispy_string


class LispyInterpreter:
    """Main LisPy interpreter class."""
    
    def __init__(self):
        self.env = create_global_env()
        self.module_loader = get_module_loader()
        
    def add_load_path(self, path: str):
        """Add a directory to the module load path."""
        abs_path = os.path.abspath(path)
        self.module_loader.add_load_path(abs_path)
        
    def run_file(self, file_path: str):
        """Execute a LisPy file as the main entry point."""
        file_path = os.path.abspath(file_path)
        
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.", file=sys.stderr)
            return 1
            
        if not file_path.endswith('.lpy'):
            print(f"Warning: File '{file_path}' doesn't have .lpy extension.")
            
        # Add the file's directory to the module load path
        file_dir = os.path.dirname(file_path)
        self.add_load_path(file_dir)
        
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
                
            # Parse and evaluate all expressions
            result = self._execute_source(source_code, file_path)
            
            # If the last expression returned a value, print it
            if result is not None:
                print(f"Program result: {result}")
            
            return 0
            
        except FileNotFoundError:
            print(f"Error: Could not read file '{file_path}'.", file=sys.stderr)
            return 1
        except (LexerError, ParseError, EvaluationError) as e:
            print(f"LisPy Error in '{file_path}': {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error in '{file_path}': {e}", file=sys.stderr)
            return 1
            
    def _execute_source(self, source_code: str, file_path: str = "<input>"):
        """Execute LisPy source code."""
        # Tokenize
        tokens = tokenize(source_code)
        
        # Parse all expressions
        expressions = self._parse_all_expressions(tokens)
        
        # Execute all expressions
        last_result = None
        for expr in expressions:
            last_result = evaluate(expr, self.env)
            
        return last_result
        
    def _parse_all_expressions(self, tokens):
        """Parse all expressions from a list of tokens."""
        expressions = []
        position = 0
        
        while position < len(tokens):
            # Find the end of the current expression
            expr_tokens, new_position = self._extract_next_expression_tokens(tokens, position)
            if expr_tokens:
                expr = parse(expr_tokens)
                expressions.append(expr)
            position = new_position
            
        return expressions
        
    def _extract_next_expression_tokens(self, tokens, start_pos):
        """Extract tokens for the next complete expression."""
        if start_pos >= len(tokens):
            return [], start_pos
            
        # Handle different token types
        token_type, token_value = tokens[start_pos]
        
        if token_type in ['NUMBER', 'STRING', 'BOOLEAN', 'NIL', 'SYMBOL']:
            # Atomic expression - just one token
            return [tokens[start_pos]], start_pos + 1
        elif token_type == 'QUOTE':
            # Quote expression - quote token + next expression
            quote_tokens = [tokens[start_pos]]
            next_expr_tokens, new_pos = self._extract_next_expression_tokens(tokens, start_pos + 1)
            return quote_tokens + next_expr_tokens, new_pos
        elif token_type in ['LPAREN', 'LBRACKET', 'LBRACE']:
            # Compound expression - find matching closing delimiter
            return self._extract_compound_expression(tokens, start_pos)
        else:
            raise EvaluationError(f"Unexpected token type: {token_type}")
            
    def _extract_compound_expression(self, tokens, start_pos):
        """Extract a compound expression (list, vector, or map)."""
        if start_pos >= len(tokens):
            return [], start_pos
            
        opening_token = tokens[start_pos][0]
        closing_token = {'LPAREN': 'RPAREN', 'LBRACKET': 'RBRACKET', 'LBRACE': 'RBRACE'}[opening_token]
        
        result_tokens = [tokens[start_pos]]  # Include opening token
        pos = start_pos + 1
        depth = 1
        
        while pos < len(tokens) and depth > 0:
            token_type, token_value = tokens[pos]
            result_tokens.append(tokens[pos])
            
            if token_type == opening_token:
                depth += 1
            elif token_type == closing_token:
                depth -= 1
                
            pos += 1
            
        if depth > 0:
            raise EvaluationError(f"Unclosed {opening_token}")
            
        return result_tokens, pos
        
    def start_repl(self):
        """Start an interactive Read-Eval-Print Loop."""
        print("LisPy Interactive Interpreter")
        print("Type expressions to evaluate them, or 'exit' to quit.")
        print("Use (import \"module-name\") to load modules.")
        print()
        
        while True:
            try:
                # Read input
                user_input = input("lispy> ").strip()
                
                # Check for exit
                if user_input.lower() in ['exit', 'quit', '(exit)', '(quit)']:
                    print("Goodbye!")
                    break
                    
                if not user_input:
                    continue
                    
                # Evaluate and print result
                result = run_lispy_string(user_input, self.env)
                if result is not None:
                    print(f"=> {result}")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
            except (LexerError, ParseError, EvaluationError) as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")


def main():
    """Main entry point for the LisPy interpreter."""
    parser = argparse.ArgumentParser(
        description="LisPy Interpreter - Run LisPy programs or start interactive mode",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bin/lispy_interpreter.py --repl              # Start REPL explicitly
  python bin/lispy_interpreter.py                     # Start REPL (default)
  python bin/lispy_interpreter.py main.lpy            # Run main.lpy
  python bin/lispy_interpreter.py examples/demo.lpy   # Run demo from examples/
        """
    )
    
    parser.add_argument(
        'file', 
        nargs='?', 
        help='LisPy file to execute'
    )
    
    parser.add_argument(
        '--repl',
        action='store_true',
        help='Start interactive REPL mode (default if no file specified)'
    )
    
    parser.add_argument(
        '-I', '--include-path',
        action='append',
        dest='include_paths',
        help='Add directory to module load path (can be used multiple times)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='LisPy 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.file and args.repl:
        print("Error: Cannot specify both a file and --repl option.", file=sys.stderr)
        return 1
    
    # Create interpreter
    interpreter = LispyInterpreter()
    
    # Add any additional include paths
    if args.include_paths:
        for path in args.include_paths:
            interpreter.add_load_path(path)
    
    # Determine mode: file execution or REPL
    if args.file:
        return interpreter.run_file(args.file)
    else:
        # Start REPL (either explicitly requested or default behavior)
        interpreter.start_repl()
        return 0


if __name__ == "__main__":
    sys.exit(main()) 