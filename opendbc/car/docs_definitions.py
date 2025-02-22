import warnings
from opendbc.metadata.lib.definitions import (
    # Core enums
    Column, ExtraCarsColumn, SupportType, Star,
    # Parts-related
    BasePart, EnumBase, Mount, Cable, Accessory,
    BaseCarHarness, CarHarness, Device, Kit, Tool, PartType,
    # Car documentation
    CarDocs, ExtraCarDocs, CarParts, DEFAULT_CAR_PARTS,
    # Footnotes
    CarFootnote, CommonFootnote,
    # Helper functions
    get_footnotes, get_year_list, split_name,
    # Constants
    GOOD_TORQUE_THRESHOLD, MODEL_YEARS_RE,
)

# Re-export everything
__all__ = [
    'Column', 'ExtraCarsColumn', 'SupportType', 'Star',
    'BasePart', 'EnumBase', 'Mount', 'Cable', 'Accessory',
    'BaseCarHarness', 'CarHarness', 'Device', 'Kit', 'Tool', 'PartType',
    'CarDocs', 'ExtraCarDocs', 'CarParts', 'DEFAULT_CAR_PARTS',
    'CarFootnote', 'CommonFootnote',
    'get_footnotes', 'get_year_list', 'split_name',
    'GOOD_TORQUE_THRESHOLD', 'MODEL_YEARS_RE',
]

warnings.warn(
    "opendbc/car/docs_definitions.py is deprecated. Please import from metadata.lib.definitions directly.",
    DeprecationWarning,
    stacklevel=2
)
