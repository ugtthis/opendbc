"""
Parts and tools definitions for the metadata framework.

This module defines the data structures and types for vehicle parts and tools.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Part:
    """Represents a physical part needed for installation."""
    name: str
    description: str
    url: Optional[str] = None

@dataclass
class Tool:
    """Represents a tool needed for installation."""
    name: str
    description: str
    url: Optional[str] = None

@dataclass
class CarParts:
    """Collection of parts and tools needed for a specific car model."""
    parts: List[Part]
    tools: List[Tool]
    notes: Optional[str] = None

    @classmethod
    def create(cls, parts: List[Part], tools: List[Tool], notes: Optional[str] = None) -> 'CarParts':
        """Create a new CarParts instance with the specified parts and tools."""
        return cls(parts=parts, tools=tools, notes=notes)
