"""
Base components for the metadata framework.

This module exports all base components used throughout the framework.
"""

from opendbc.metadata.base.constants import COLUMNS, EXTRA_CARS_COLUMNS, STARS, SUPPORT_TYPES, MS_TO_MPH, GOOD_TORQUE_THRESHOLD
from opendbc.metadata.base.parts import Part, PartCategory, Tool, CarParts, PlatformParts, BrandPartProcessor
from opendbc.metadata.base.footnotes import Footnote, FootnoteCollection
from opendbc.metadata.base.processor import ModelData, BaseProcessor
from opendbc.metadata.base.parts_definitions import (
    Harness, 
    Tool as ToolEnum, 
    Kit, 
    Accessory, 
    Category,
    BasePart,
    EnumBase,
    get_part_by_name,
    get_all_parts
)
from opendbc.metadata.base.model_helpers import (
    get_model_data,
    get_visible_models,
    get_model_by_platform,
    get_all_parts_for_model
)
