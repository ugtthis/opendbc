"""
Central parts definitions for the metadata framework.

This module provides a single source of truth for all parts used across
different vehicle brands, ensuring consistency and reducing redundancy.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Set, Dict, Any, Type

@dataclass
class BasePart:
    """Base class for parts with composition."""
    name: str
    description: str = ""
    url: Optional[str] = None
    category: str = "accessory"
    parts: List['EnumBase'] = field(default_factory=list)
    
    def all_parts(self) -> List['EnumBase']:
        """Get all parts including dependencies."""
        parts = []
        parts.extend(self.parts)
        for part in self.parts:
            parts.extend(part.value.all_parts())
        return parts

class EnumBase(Enum):
    """Base class for part enums."""
    @property
    def name(self) -> str:
        return self.value.name
        
    @property
    def description(self) -> str:
        return self.value.description
        
    @property
    def url(self) -> Optional[str]:
        return self.value.url
        
    @property
    def category(self) -> str:
        return self.value.category

# Define categories matching the existing PartCategory enum
class Category:
    HARNESS = "harness"
    TOOL = "tool"
    ACCESSORY = "accessory"

# Define actual part enums - EXACT MATCHES to docs_definitions.py
class Harness(EnumBase):
    """Harness connectors for different vehicle brands."""
    # Honda harnesses
    HONDA_NIDEC = BasePart("Honda Nidec connector", "For Honda vehicles with Nidec ADAS", category=Category.HARNESS)
    HONDA_BOSCH_A = BasePart("Honda Bosch A connector", "For Honda vehicles with Bosch ADAS (Type A)", category=Category.HARNESS)
    HONDA_BOSCH_B = BasePart("Honda Bosch B connector", "For Honda vehicles with Bosch ADAS (Type B)", category=Category.HARNESS)
    HONDA_BOSCH_C = BasePart("Honda Bosch C connector", "For Honda vehicles with Bosch ADAS (Type C)", category=Category.HARNESS)
    
    # Toyota harnesses
    TOYOTA_A = BasePart("Toyota A connector", "For Toyota vehicles (Type A)", category=Category.HARNESS)
    TOYOTA_B = BasePart("Toyota B connector", "For Toyota vehicles (Type B)", category=Category.HARNESS)
    
    # Subaru harnesses
    SUBARU_A = BasePart("Subaru A connector", "For pre-2020 models with torque-based LKAS", category=Category.HARNESS)
    SUBARU_B = BasePart("Subaru B connector", "For 2020-22 Outback/Legacy and 2020 Crosstrek Hybrid", category=Category.HARNESS)
    SUBARU_C = BasePart("Subaru C connector", "For 2022-24 Forester", category=Category.HARNESS)
    SUBARU_D = BasePart("Subaru D connector", "For 2023 Outback", category=Category.HARNESS)
    
    # Hyundai harnesses
    HYUNDAI_A = BasePart("Hyundai A connector", "For Hyundai/Kia vehicles (Type A)", category=Category.HARNESS)
    HYUNDAI_B = BasePart("Hyundai B connector", "For Hyundai/Kia vehicles (Type B)", category=Category.HARNESS)
    HYUNDAI_C = BasePart("Hyundai C connector", "For Hyundai/Kia vehicles (Type C)", category=Category.HARNESS)
    HYUNDAI_D = BasePart("Hyundai D connector", "For Hyundai/Kia vehicles (Type D)", category=Category.HARNESS)
    HYUNDAI_E = BasePart("Hyundai E connector", "For Hyundai/Kia vehicles (Type E)", category=Category.HARNESS)
    HYUNDAI_F = BasePart("Hyundai F connector", "For Hyundai/Kia vehicles (Type F)", category=Category.HARNESS)
    HYUNDAI_G = BasePart("Hyundai G connector", "For Hyundai/Kia vehicles (Type G)", category=Category.HARNESS)
    HYUNDAI_H = BasePart("Hyundai H connector", "For Hyundai/Kia vehicles (Type H)", category=Category.HARNESS)
    HYUNDAI_I = BasePart("Hyundai I connector", "For Hyundai/Kia vehicles (Type I)", category=Category.HARNESS)
    HYUNDAI_J = BasePart("Hyundai J connector", "For Hyundai/Kia vehicles (Type J)", category=Category.HARNESS)
    HYUNDAI_K = BasePart("Hyundai K connector", "For Hyundai/Kia vehicles (Type K)", category=Category.HARNESS)
    HYUNDAI_L = BasePart("Hyundai L connector", "For Hyundai/Kia vehicles (Type L)", category=Category.HARNESS)
    HYUNDAI_M = BasePart("Hyundai M connector", "For Hyundai/Kia vehicles (Type M)", category=Category.HARNESS)
    HYUNDAI_N = BasePart("Hyundai N connector", "For Hyundai/Kia vehicles (Type N)", category=Category.HARNESS)
    HYUNDAI_O = BasePart("Hyundai O connector", "For Hyundai/Kia vehicles (Type O)", category=Category.HARNESS)
    HYUNDAI_P = BasePart("Hyundai P connector", "For Hyundai/Kia vehicles (Type P)", category=Category.HARNESS)
    HYUNDAI_Q = BasePart("Hyundai Q connector", "For Hyundai/Kia vehicles (Type Q)", category=Category.HARNESS)
    HYUNDAI_R = BasePart("Hyundai R connector", "For Hyundai/Kia vehicles (Type R)", category=Category.HARNESS)

class Tool(EnumBase):
    """Tools needed for installation."""
    PRY_TOOL = BasePart("Pry Tool", "For removing interior trim pieces", category=Category.TOOL)
    SOCKET_8MM_DEEP = BasePart("Socket Wrench 8mm or 5/16\" (deep)", "For removing bolts during installation", category=Category.TOOL)

class Kit(EnumBase):
    """Kits for special installations."""
    CANFD_KIT = BasePart("CAN FD panda kit", "Required for vehicles with CAN FD", category=Category.ACCESSORY)

class Accessory(EnumBase):
    """Accessories for installation."""
    HARNESS_BOX = BasePart("Harness Box", "Protective box for the harness connection", category=Category.ACCESSORY)
    COMMA_POWER_V2 = BasePart("Comma Power V2", "Power management for comma devices", category=Category.ACCESSORY)

class Mount(EnumBase):
    """Mounts for devices."""
    REGULAR = BasePart("Regular Mount", "Standard mount for comma devices", category=Category.ACCESSORY)
    ANGLED_8_DEGREES = BasePart("Angled Mount (8 degrees)", "Angled mount for vehicles requiring a tilted device", category=Category.ACCESSORY)

class Device(EnumBase):
    """Devices for vehicle integration."""
    THREEX = BasePart("comma 3X", "Standard comma 3X device with regular mount", parts=[Mount.REGULAR], category=Category.ACCESSORY)
    THREEX_ANGLED_MOUNT = BasePart("comma 3X with angled mount", "comma 3X device with 8-degree angled mount", parts=[Mount.ANGLED_8_DEGREES], category=Category.ACCESSORY)
    RED_PANDA = BasePart("red panda", "CAN FD interface device", category=Category.ACCESSORY)

# Utility functions
def get_part_by_name(name: str) -> Optional[EnumBase]:
    """Find a part by its exact name."""
    for enum_class in [Harness, Tool, Kit, Accessory, Mount, Device]:
        for part in enum_class:
            if part.name == name:
                return part
    return None

def get_all_parts() -> List[EnumBase]:
    """Get a list of all defined parts."""
    all_parts = []
    for enum_class in [Harness, Tool, Kit, Accessory, Mount, Device]:
        all_parts.extend(list(enum_class))
    return all_parts 