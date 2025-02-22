#!/usr/bin/env python3
import jinja2
from typing import List

from opendbc.metadata.lib.definitions import CarDocs, ExtraCarDocs, Column, ExtraCarsColumn, PartType, Device
from opendbc.metadata.lib.metadata import group_by_make
from opendbc.metadata.lib.metadata_combiner import get_all_footnotes


def generate_cars_md(all_car_docs: list[CarDocs], template_fn: str) -> str:
    """Generates markdown for supported cars"""
    with open(template_fn) as f:
        template = jinja2.Template(f.read(), trim_blocks=True, lstrip_blocks=True)

    footnotes = [fn.value.text for fn in get_all_footnotes()]
    cars_md: str = template.render(all_car_docs=all_car_docs, PartType=PartType,
                                 group_by_make=group_by_make, footnotes=footnotes,
                                 Device=Device, Column=Column)
    return cars_md


def generate_cars_md_with_extras(car_docs_with_extras: list[CarDocs | ExtraCarDocs], template_fn: str) -> str:
    """Generates markdown including extra cars"""
    with open(template_fn) as f:
        template = jinja2.Template(f.read(), trim_blocks=True, lstrip_blocks=True)

    cars_md: str = template.render(car_docs_with_extras=car_docs_with_extras, PartType=PartType,
                                 group_by_make=group_by_make, ExtraCarsColumn=ExtraCarsColumn)
    return cars_md


if __name__ == "__main__":
    import argparse
    from opendbc.metadata.lib.metadata import EXTRA_CARS_MD_TEMPLATE, EXTRA_CARS_MD_OUT, get_car_docs_with_extras

    parser = argparse.ArgumentParser(description="Auto generates supportability info docs for all known cars",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--template", default=EXTRA_CARS_MD_TEMPLATE, help="Override default template filename")
    parser.add_argument("--out", default=EXTRA_CARS_MD_OUT, help="Override default generated filename")
    args = parser.parse_args()

    with open(args.out, 'w') as f:
        f.write(generate_cars_md_with_extras(get_car_docs_with_extras(), args.template))
    print(f"Generated and written to {args.out}")