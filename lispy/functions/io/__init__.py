"""LisPy I/O Functions"""

from .print import print_func, print_documentation
from .println import println_func, println_documentation
from .read_line import read_line_func, read_line_documentation
from .slurp import slurp_func, slurp_documentation
from .spit import spit_func, spit_documentation

__all__ = [
    # Functions
    "print_func",
    "println_func",
    "read_line_func",
    "slurp_func",
    "spit_func",
    # Documentation
    "print_documentation",
    "println_documentation",
    "read_line_documentation",
    "slurp_documentation",
    "spit_documentation",
]
