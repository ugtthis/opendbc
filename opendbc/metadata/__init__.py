"""
Metadata Framework for OpenDBC

This package provides a structured framework for managing vehicle metadata,
including platform configurations, parts, footnotes, and documentation generation.

The framework is organized into:
1. Base components (constants, parts, footnotes, processors)
2. Brand-specific metadata (Subaru, Hyundai, etc.)
3. Utilities for documentation generation and data extraction
"""

# Import base components
from opendbc.metadata.base import (
    # Constants
    COLUMNS, EXTRA_CARS_COLUMNS, STARS, SUPPORT_TYPES, MS_TO_MPH, GOOD_TORQUE_THRESHOLD,
    
    # Parts
    Part, Tool, CarParts, PlatformParts, BrandPartProcessor, PartCategory,
    
    # Footnotes
    Footnote, FootnoteCollection,
    
    # Processors
    BaseProcessor, ModelData,
    
    # Parts Catalog
    PartsCatalog, HarnessId, ToolId, AccessoryId, CableId, MountId, DeviceId, KitId
)

# Import flag-based processor if available
try:
    from opendbc.metadata.base import FlagBasedProcessor, FlagConfig
except ImportError:
    pass

# Brand-specific processors
from opendbc.metadata.brand_metadata.subaru.processor import SubaruProcessor
from opendbc.metadata.brand_metadata.hyundai.processor import HyundaiProcessor

__all__ = [
    # Constants
    'COLUMNS', 'EXTRA_CARS_COLUMNS', 'STARS', 'SUPPORT_TYPES', 
    'MS_TO_MPH', 'GOOD_TORQUE_THRESHOLD',
    
    # Parts
    'Part', 'Tool', 'CarParts', 'PlatformParts', 'BrandPartProcessor', 'PartCategory',
    
    # Footnotes
    'Footnote', 'FootnoteCollection',
    
    # Processors
    'BaseProcessor', 'ModelData', 'SubaruProcessor', 'HyundaiProcessor',
    
    # Parts Catalog
    'PartsCatalog', 'HarnessId', 'ToolId', 'AccessoryId', 'CableId', 'MountId', 'DeviceId', 'KitId'
]
