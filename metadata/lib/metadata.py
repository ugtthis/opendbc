#!/usr/bin/env python3
import os
from collections import defaultdict
from typing import Dict, List, get_args

from opendbc.car.values import Platform, PLATFORMS
from opendbc.car.extra_cars import CAR as EXTRA
from opendbc.metadata.lib.definitions import CarDocs, ExtraCarDocs
from opendbc.metadata.lib.metadata_combiner import build_sorted_car_docs_list, get_all_footnotes

# Constants from original docs.py
EXTRA_CARS_MD_OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "docs", "CARS.md")
EXTRA_CARS_MD_TEMPLATE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "CARS_template.md")

ExtraPlatform = Platform | EXTRA
EXTRA_BRANDS = get_args(ExtraPlatform)
EXTRA_PLATFORMS: dict[str, ExtraPlatform] = {str(platform): platform for brand in EXTRA_BRANDS for platform in brand}


def get_all_car_docs() -> list[CarDocs]:
    """Gets all car docs for supported platforms"""
    collected_footnotes = get_all_footnotes()
    sorted_list: list[CarDocs] = build_sorted_car_docs_list(PLATFORMS, footnotes=collected_footnotes)
    return sorted_list


def get_car_docs_with_extras() -> list[CarDocs | ExtraCarDocs]:
    """Gets car docs including extras"""
    sorted_list: list[CarDocs] = build_sorted_car_docs_list(EXTRA_PLATFORMS, include_dashcam=True)
    return sorted_list


def group_by_make(all_car_docs: list[CarDocs]) -> dict[str, list[CarDocs]]:
    """Groups car docs by manufacturer"""
    sorted_car_docs = defaultdict(list)
    for car_docs in all_car_docs:
        sorted_car_docs[car_docs.make].append(car_docs)
    return dict(sorted_car_docs)