#!/usr/bin/env python3
import warnings

# Re-export everything from new locations
from opendbc.metadata.lib.metadata import (
    EXTRA_CARS_MD_OUT,
    EXTRA_CARS_MD_TEMPLATE,
    ExtraPlatform,
    EXTRA_BRANDS,
    EXTRA_PLATFORMS,
)

from opendbc.metadata.lib.metadata_combiner import (
    get_params_for_docs,
    get_all_footnotes,
    build_sorted_car_docs_list,
    get_all_car_docs,
    get_car_docs_with_extras,
    group_by_make,
)

from opendbc.metadata.scripts.generator.md import (
    generate_cars_md,
    generate_cars_md_with_extras,
)

# Export everything
__all__ = [
    'EXTRA_CARS_MD_OUT', 'EXTRA_CARS_MD_TEMPLATE',
    'ExtraPlatform', 'EXTRA_BRANDS', 'EXTRA_PLATFORMS',
    'get_params_for_docs', 'get_all_footnotes',
    'build_sorted_car_docs_list', 'get_all_car_docs',
    'get_car_docs_with_extras', 'group_by_make',
    'generate_cars_md', 'generate_cars_md_with_extras',
]

warnings.warn(
    "Importing from opendbc.car.docs is deprecated. Please import from opendbc.metadata.lib.{metadata,metadata_combiner} "
    "or opendbc.metadata.scripts.generator.md",
    DeprecationWarning,
    stacklevel=2
)
