#!/usr/bin/env python3
"""
Core metadata functionality for OpenDBC.
This module serves as the main entry point for the metadata package.
"""

from opendbc.metadata.lib.definitions import (
    CarDocs, ExtraCarDocs,
    Column, ExtraCarsColumn,
    SupportType, Star
)

from opendbc.metadata.lib.metadata_combiner import (
    get_all_car_docs,
    get_car_docs_with_extras,
    ExtraPlatform,
    EXTRA_BRANDS,
    EXTRA_PLATFORMS
)

__all__ = [
    'CarDocs', 'ExtraCarDocs',
    'Column', 'ExtraCarsColumn',
    'SupportType', 'Star',
    'get_all_car_docs', 'get_car_docs_with_extras',
    'ExtraPlatform', 'EXTRA_BRANDS', 'EXTRA_PLATFORMS'
]
