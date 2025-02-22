#!/usr/bin/env python3
import argparse
import os
import jinja2
from typing import get_args
from collections import defaultdict
from natsort import natsorted

from opendbc.car.common.basedir import BASEDIR
from opendbc.metadata.lib.definitions import (
    CarDocs, Device, ExtraCarDocs, Column, 
    ExtraCarsColumn, PartType
)
from opendbc.metadata.lib.metadata_combiner import (
    get_car_docs_with_extras,
    get_all_footnotes,
    group_by_make
)

# Update paths to use metadata templates
METADATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
EXTRA_CARS_MD_OUT = os.path.join(BASEDIR, "../", "../", "docs", "CARS_TEST.md")
EXTRA_CARS_MD_TEMPLATE = os.path.join(METADATA_DIR, "templates", "CARS_template.md")

def generate_cars_md(all_car_docs: list[CarDocs], template_fn: str) -> str:
    """Generate markdown documentation for supported cars."""
    with open(template_fn) as f:
        template = jinja2.Template(f.read(), trim_blocks=True, lstrip_blocks=True)

    footnotes = [fn.value.text for fn in get_all_footnotes()]
    cars_md: str = template.render(
        all_car_docs=all_car_docs,
        PartType=PartType,
        group_by_make=group_by_make,
        footnotes=footnotes,
        Device=Device,
        Column=Column
    )
    return cars_md

def generate_cars_md_with_extras(car_docs_with_extras: list[CarDocs | ExtraCarDocs], template_fn: str) -> str:
    """Generate markdown documentation including extra cars."""
    with open(template_fn) as f:
        template = jinja2.Template(f.read(), trim_blocks=True, lstrip_blocks=True)

    cars_md: str = template.render(
        car_docs_with_extras=car_docs_with_extras,
        PartType=PartType,
        group_by_make=group_by_make,
        ExtraCarsColumn=ExtraCarsColumn
    )
    return cars_md

def main():
    parser = argparse.ArgumentParser(
        description="Auto generates supportability info docs for all known cars",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--template", default=EXTRA_CARS_MD_TEMPLATE, help="Override default template filename")
    parser.add_argument("--out", default=EXTRA_CARS_MD_OUT, help="Override default generated filename")
    args = parser.parse_args()

    with open(args.out, 'w') as f:
        f.write(generate_cars_md_with_extras(get_car_docs_with_extras(), args.template))
    print(f"Generated and written to {args.out}")

if __name__ == "__main__":
    main()
