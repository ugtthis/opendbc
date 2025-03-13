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
    
    # Parts Definitions
    Harness, ToolEnum, Kit, Accessory, Category, BasePart, EnumBase, get_part_by_name, get_all_parts,
    
    # Model Helpers
    get_model_data, get_visible_models, get_model_by_platform, get_all_parts_for_model
)

# Import flag-based processor if available
try:
    from opendbc.metadata.base.flag_processor import FlagBasedProcessor, FlagConfig
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
    
    # Parts Definitions
    'Harness', 'ToolEnum', 'Kit', 'Accessory', 'Category', 'BasePart', 'EnumBase',
    'get_part_by_name', 'get_all_parts',
    
    # Model Helpers
    'get_model_data', 'get_visible_models', 'get_model_by_platform', 'get_all_parts_for_model'
]

# Add flag-based processor to __all__ if available
try:
    __all__.extend(['FlagBasedProcessor', 'FlagConfig'])
except NameError:
    pass
