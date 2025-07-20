"""
Data models for the documentation generator.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class FunctionDoc:
    name: str
    symbol: str
    type: str  # 'function' or 'special-form'
    category: str
    arguments: str
    description: str
    examples: List[Dict[str, str]]
    notes: List[str]
    see_also: List[str]
    file_path: str
