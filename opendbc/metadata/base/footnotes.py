"""
Footnotes definitions for the metadata framework.

This module defines the data structures and types for vehicle documentation footnotes.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from .constants import COLUMNS

@dataclass
class Footnote:
    """Represents a footnote in the vehicle documentation."""
    text: str
    columns: List[str]  # List of column names this footnote applies to
    
    def __post_init__(self):
        """Validate that all columns exist in COLUMNS."""
        for column in self.columns:
            if column not in COLUMNS:
                raise ValueError(f"Invalid column name: {column}")

@dataclass
class FootnoteCollection:
    """Collection of footnotes for a specific car model."""
    footnotes: Dict[str, Footnote]  # key is footnote ID
    
    @classmethod
    def create(cls, footnotes: Dict[str, Footnote]) -> 'FootnoteCollection':
        """Create a new FootnoteCollection instance."""
        return cls(footnotes=footnotes)
    
    def get_footnote(self, footnote_id: str) -> Optional[Footnote]:
        """Get a footnote by its ID."""
        return self.footnotes.get(footnote_id)
    
    def get_footnotes_for_column(self, column: str) -> List[Footnote]:
        """Get all footnotes that apply to a specific column."""
        return [f for f in self.footnotes.values() if column in f.columns]
