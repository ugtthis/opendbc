#!/usr/bin/env python3
from typing import Dict, List, Any
from enum import Enum
from natsort import natsorted

from opendbc.car import gen_empty_fingerprint
from opendbc.car.structs import CarParams
from opendbc.car.car_helpers import interfaces, get_interface_attr
from opendbc.car.mock.values import CAR as MOCK
from opendbc.metadata.lib.definitions import CarDocs, ExtraCarDocs, CommonFootnote


def get_params_for_docs(model, platform) -> CarParams:
    """Gets CarParams for documentation"""
    cp_model, cp_platform = (model, platform) if model in interfaces else ("MOCK", MOCK.MOCK)
    CP: CarParams = interfaces[cp_model][0].get_params(cp_platform,
                                                     fingerprint=gen_empty_fingerprint(),
                                                     car_fw=[CarParams.CarFw(ecu=CarParams.Ecu.unknown)],
                                                     experimental_long=True,
                                                     docs=True)
    return CP


def get_all_footnotes() -> dict[Enum, int]:
    """Gets all footnotes including interface ones"""
    all_footnotes = list(CommonFootnote)
    for footnotes in get_interface_attr("Footnote", ignore_none=True).values():
        all_footnotes.extend(footnotes)
    return {fn: idx + 1 for idx, fn in enumerate(all_footnotes)}


def build_sorted_car_docs_list(platforms, footnotes=None, include_dashcam=False):
    """Builds and sorts car docs list"""
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