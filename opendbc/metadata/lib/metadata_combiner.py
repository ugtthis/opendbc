#!/usr/bin/env python3
from enum import Enum
from collections import defaultdict
from natsort import natsorted
from typing import get_args

from opendbc.car import gen_empty_fingerprint
from opendbc.car.structs import CarParams
from opendbc.car.car_helpers import interfaces, get_interface_attr
from opendbc.car.values import Platform, PLATFORMS
from opendbc.car.mock.values import CAR as MOCK
from opendbc.car.extra_cars import CAR as EXTRA
from opendbc.metadata.lib.definitions import (
    CarDocs, ExtraCarDocs, CommonFootnote
)

# Platform definitions for documentation
ExtraPlatform = Platform | EXTRA
EXTRA_BRANDS = get_args(ExtraPlatform)
EXTRA_PLATFORMS: dict[str, ExtraPlatform] = {str(platform): platform for brand in EXTRA_BRANDS for platform in brand}

def get_params_for_docs(model, platform) -> CarParams:
    """Get CarParams for documentation purposes."""
    cp_model, cp_platform = (model, platform) if model in interfaces else ("MOCK", MOCK.MOCK)
    CP: CarParams = interfaces[cp_model][0].get_params(
        cp_platform, 
        fingerprint=gen_empty_fingerprint(),
        car_fw=[CarParams.CarFw(ecu=CarParams.Ecu.unknown)],
        experimental_long=True, 
        docs=True
    )
    return CP

def get_all_footnotes() -> dict[Enum, int]:
    """Collect and number all footnotes from common and car-specific sources."""
    all_footnotes = list(CommonFootnote)
    for footnotes in get_interface_attr("Footnote", ignore_none=True).values():
        all_footnotes.extend(footnotes)
    return {fn: idx + 1 for idx, fn in enumerate(all_footnotes)}

def build_sorted_car_docs_list(platforms, footnotes=None, include_dashcam=False):
    """Build and sort a list of car documentation."""
    collected_car_docs: list[CarDocs | ExtraCarDocs] = []
    for model, platform in platforms.items():
        car_docs = platform.config.car_docs
        CP = get_params_for_docs(model, platform)

        if (CP.dashcamOnly and not include_dashcam) or not len(car_docs):
            continue

        # A platform can include multiple car models
        for _car_docs in car_docs:
            if not hasattr(_car_docs, "row"):
                _car_docs.init_make(CP)
                _car_docs.init(CP, footnotes)
            collected_car_docs.append(_car_docs)

    # Sort cars by make and model + year
    sorted_cars = natsorted(collected_car_docs, key=lambda car: car.name.lower())
    return sorted_cars

def get_all_car_docs() -> list[CarDocs]:
    """Get documentation for all supported cars."""
    collected_footnotes = get_all_footnotes()
    sorted_list: list[CarDocs] = build_sorted_car_docs_list(PLATFORMS, footnotes=collected_footnotes)
    return sorted_list

def get_car_docs_with_extras() -> list[CarDocs | ExtraCarDocs]:
    """Get documentation including extra cars."""
    sorted_list: list[CarDocs] = build_sorted_car_docs_list(EXTRA_PLATFORMS, include_dashcam=True)
    return sorted_list

def group_by_make(all_car_docs: list[CarDocs]) -> dict[str, list[CarDocs]]:
    """Group car documentation by make."""
    sorted_car_docs = defaultdict(list)
    for car_docs in all_car_docs:
        sorted_car_docs[car_docs.make].append(car_docs)
    return dict(sorted_car_docs)
