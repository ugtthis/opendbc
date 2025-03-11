"""
Parts and tools definitions for the metadata framework.

This module defines the data structures and types for vehicle parts and tools.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Set

class PartCategory(Enum):
    """Categories of parts needed for installation."""
    HARNESS = "harness"
    TOOL = "tool"
    ACCESSORY = "accessory"

@dataclass(frozen=True)
class Part:
    """Represents a physical part needed for installation."""
    id: str  # e.g. "subaru_a"
    name: str  # e.g. "Subaru Harness Type A"
    category: PartCategory
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

@dataclass
class PlatformParts:
    """Parts required for a specific platform."""
    required_parts: Set[Part]
    optional_parts: Set[Part] = field(default_factory=set)
    tools: Set[Part] = field(default_factory=set)

class BrandPartProcessor:
    """Base class for determining parts based on platform flags."""
    
    def get_parts_for_platform(self, platform_config) -> PlatformParts:
        """Get required parts based on platform config from values.py."""
        raise NotImplementedError
