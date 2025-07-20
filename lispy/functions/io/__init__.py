"""LisPy I/O Functions"""

from .print import print_fn, print_documentation
from .println import println, println_documentation
from .read_line import read_line, read_line_documentation
from .slurp import slurp, slurp_documentation
from .spit import spit, spit_documentation

__all__ = [
    # Functions
    "print_fn",
    "println",
    "read_line",
    "slurp",
    "spit",
    # Documentation
    "print_documentation",
    "println_documentation",
    "read_line_documentation",
    "slurp_documentation",
    "spit_documentation",
]
