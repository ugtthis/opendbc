#!/usr/bin/env python3
import json
import os
from opendbc.car.docs import get_all_car_docs
from opendbc.car.docs_definitions import CarDocs, ExtraCarDocs, Star, CarHarness, BaseCarHarness

def _part_to_dict(part_enum):
    """
    Extracts information from the Enum-based part (e.g. Cable, Harness, Accessory).
    """
    base_part = part_enum.value
    return {
        "enum_name": part_enum.name,
        "display_name": base_part.name,
        "sub_parts": [p.value.name for p in base_part.parts],  # one-level down
        "has_connector": getattr(base_part, "has_connector", None),
    }

def car_docs_to_dict(c: CarDocs) -> dict:
    """
    Turn a CarDocs (or ExtraCarDocs) instance into a JSON-serializable dictionary,
    matching the specified format with hardware details and simplified car parts.
    """
    # Convert footnotes to a list of strings for JSON
    footnotes = [fn.value.text for fn in c.footnotes] if c.footnotes else []

    # Simplify car parts to a list of strings and extract harness
    car_parts = []
    harness_name = None
    if c.car_parts and c.car_parts.parts:
        for part_enum in c.car_parts.parts:
            base_part = part_enum.value
            car_parts.append(base_part.name)
            # Extract harness name from BaseCarHarness instances
            if isinstance(base_part, BaseCarHarness):
                harness_name = part_enum.name.lower()

    # Convert row data for specific fields
    row_data = {}
    if hasattr(c, "row"):
        for col_enum, col_value in c.row.items():
            if isinstance(col_value, Star):
                row_data[col_enum.name.lower()] = col_value.value
            else:
                row_data[col_enum.name.lower()] = col_value

    # Format hardware details
    hardware_parts = []
    if c.car_parts and c.car_parts.parts:
        for part_enum in c.car_parts.parts:
            base_part = part_enum.value
            # Add main part
            hardware_parts.append(f"- 1 {base_part.name}")
            # Add sub parts if any
            for sub_part in base_part.parts:
                hardware_parts.append(f"- 1 {sub_part.value.name}")
    
    hardware_details = ""
    if hardware_parts:
        parts_list = "<br>".join(hardware_parts)
        shop_link = f'<a href="https://comma.ai/shop/comma-3x.html?make={c.make}&model={c.name}">Buy Here</a>'
        hardware_details = f'<details><summary>Parts</summary><sub>{parts_list}<br>{shop_link}</sub></details>'

    return {
        "name": c.name,
        "make": getattr(c, "make", None),
        "model": getattr(c, "model", None),
        "years": getattr(c, "years", None),
        "year_list": getattr(c, "year_list", []),
        "package": c.package,
        "requirements": c.requirements,
        "video_link": c.video_link,
        "footnotes": footnotes,
        "min_steer_speed": c.min_steer_speed,
        "min_enable_speed": c.min_enable_speed,
        "auto_resume": c.auto_resume,
        "car_parts": car_parts,
        "harness": harness_name,
        "merged": c.merged,
        "support_type": c.support_type.value if c.support_type else None,
        "support_link": c.support_link,
        "detail_sentence": getattr(c, "detail_sentence", None),
        "car_name": getattr(c, "car_name", None),
        "car_fingerprint": getattr(c, "car_fingerprint", None),
        "longitudinal": row_data.get("longitudinal", None),
        "fsr_longitudinal": row_data.get("fsr_longitudinal", None),
        "fsr_steering": row_data.get("fsr_steering", None),
        "steering_torque": row_data.get("steering_torque", None),
        "auto_resume_star": row_data.get("auto_resume", None),
        "hardware": hardware_details,
        "video": row_data.get("video", "")
    }

def main():
    # Retrieve a list of all known cars from docs.py
    all_cars = get_all_car_docs()

    # Build a JSON-serializable list of car information
    cars_data = [car_docs_to_dict(c) for c in all_cars]

    # Default output filename
    output_filename = "all_cars.json"
    # Write out to file
    with open(output_filename, 'w') as f:
        json.dump(cars_data, f, indent=2)
    print(f"Generated JSON with all known cars in: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    main()