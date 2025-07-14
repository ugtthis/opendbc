#!/usr/bin/env python3
"""
Car Data JSON Generator

This script generates JSON files containing detailed information about cars supported by openpilot.
It extracts data from CarDocs and CarParams objects and formats it into a structured JSON format.

Usage:
  python3 create_cars_json.py                     # Generate regular cars JSON
  python3 create_cars_json.py --output custom.json # Custom output filename

The JSON output includes:
- Basic car information (make, model, years)
- Support status and requirements
- Hardware details (parts, harness, angled mount)
- Technical specifications
- Feature support details

Maintainer Notes:
- The car_docs_to_dict function maps CarDocs/CarParams attributes to JSON fields
- The has_angled_mount field is derived from parts that include angled mounts
- All data comes from opendbc/car/ modules, no external data sources needed
"""
import json
import os
import argparse
from opendbc.car.docs import get_all_car_docs, get_params_for_docs
from opendbc.car.docs_definitions import CarDocs, Star, BaseCarHarness, Tool
from opendbc.car.values import PLATFORMS
from opendbc.car.structs import CarParams

def car_docs_to_dict(car_doc: CarDocs, CP: CarParams = None, platform: str = None) -> dict:
    """
    Convert a CarDocs instance into a JSON-serializable dictionary.
    
    Args:
        car_doc: CarDocs instance containing car documentation
        CP: CarParams instance containing car parameters (optional)
        platform: Platform object containing car platform information (optional)
        
    Returns:
        Dictionary with car information ready for JSON serialization
    """
    # Helper function to convert enums to strings
    def enum_to_str(value):
        if value is None:
            return None
        if hasattr(value, 'value'):
            return value.value
        if hasattr(value, 'name'):
            return value.name
        if hasattr(value, '__str__'):
            return str(value)
        return value

    # Convert footnotes to a list of strings for JSON
    footnotes = [fn.value.text for fn in car_doc.footnotes] if car_doc.footnotes else []

    # Simplify car parts to a list of strings and extract harness
    car_parts = []
    harness_name = None
    if car_doc.car_parts and car_doc.car_parts.parts:
        for part_enum in car_doc.car_parts.parts:
            base_part = part_enum.value
            car_parts.append(base_part.name)
            # Extract harness name from BaseCarHarness instances
            if isinstance(base_part, BaseCarHarness):
                harness_name = part_enum.name.lower()

    # Convert row data for specific fields
    row_data = {}
    if hasattr(car_doc, "row"):
        for col_enum, col_value in car_doc.row.items():
            if isinstance(col_value, Star):
                row_data[col_enum.name.lower()] = col_value.value
            else:
                row_data[col_enum.name.lower()] = col_value

    # Get detailed parts information
    detailed_parts = []
    tools_required = []
    has_angled_mount = False
    
    if car_doc.car_parts and car_doc.car_parts.parts:
        # Get all parts including sub-parts
        all_parts = car_doc.car_parts.all_parts()
        
        # Check if any part is an angled mount
        for part in all_parts:
            if part.name == "angled_mount_8_degrees" or part.name == "threex_angled_mount":
                has_angled_mount = True
                break
        
        # Separate tools from regular parts
        parts_list = [part for part in all_parts if not isinstance(part, Tool)]
        tools_list = [part for part in all_parts if isinstance(part, Tool)]
        
        # Count occurrences of each part
        for part in sorted(set(parts_list), key=lambda p: str(p.value.name)):
            count = parts_list.count(part)
            part_type = part.part_type.name if hasattr(part, 'part_type') else None
            
            detailed_parts.append({
                "count": count,
                "name": part.value.name,
                "type": part_type,
                "enum_name": part.name
            })
        
        # Count occurrences of each tool
        for tool in sorted(set(tools_list), key=lambda t: str(t.value.name)):
            count = tools_list.count(tool)
            
            tools_required.append({
                "count": count,
                "name": tool.value.name,
                "enum_name": tool.name
            })
    
    # Format hardware details for HTML display (kept for backward compatibility)
    hardware_details = ""
    if car_doc.car_parts and car_doc.car_parts.parts:
        model_years = car_doc.model + (' ' + car_doc.years if car_doc.years else '')
        buy_link = f'<a href="https://comma.ai/shop/comma-3x.html?make={car_doc.make}&model={model_years}">Buy Here</a>'

        tools_docs = [part for part in car_doc.car_parts.all_parts() if isinstance(part, Tool)]
        parts_docs = [part for part in car_doc.car_parts.all_parts() if not isinstance(part, Tool)]

        def display_func(parts):
            return '<br>'.join([f"- {parts.count(part)} {part.value.name}" for part in sorted(set(parts), key=lambda part: str(part.value.name))])

        hardware_details = f'<details><summary>Parts</summary><sub>{display_func(parts_docs)}<br>{buy_link}</sub></details>'
        if len(tools_docs):
            hardware_details += f'<details><summary>Tools</summary><sub>{display_func(tools_docs)}</sub></details>'

    # Get car specifications from CarParams if available
    specs = {
        "mass": getattr(CP, "mass", None) if CP else None,  # kg, curb weight
        "wheelbase": getattr(CP, "wheelbase", None) if CP else None,  # meters
        "steer_ratio": getattr(CP, "steerRatio", None) if CP else None,
        "center_to_front_ratio": getattr(CP, "centerToFront", 0.5) / getattr(CP, "wheelbase", 1.0) if CP and getattr(CP, "wheelbase", 0) != 0 else 0.5,
        "start_accel": getattr(CP, "startAccel", None) if CP else None,
    }

    # Get network and bus information from CarParams and platform config
    network_info = {
        "network_location": enum_to_str(getattr(CP, "networkLocation", None)) if CP else None,
        "bus_lookup": platform.config.dbc_dict if platform else None,  # Get bus lookup from platform config
        "transmissionType": enum_to_str(getattr(CP, "transmissionType", None)) if CP else None,
        "radar_delay": getattr(CP, "radarDelay", None) if CP else None,
        "wheel_speed_factor": getattr(CP, "wheelSpeedFactor", None) if CP else None,
    }

    # Get feature support details from CarParams
    feature_support = {
        "experimental_longitudinal_available": getattr(CP, "experimentalLongitudinalAvailable", None) if CP else None,
        "openpilot_longitudinal_control": getattr(CP, "openpilotLongitudinalControl", None) if CP else None,
        "max_lateral_accel": getattr(CP, "maxLateralAccel", None) if CP else None,
        "dashcam_only": getattr(CP, "dashcamOnly", None) if CP else None,
        "enable_dsu": getattr(CP, "enableDsu", None) if CP else None,
        "enable_bsm": getattr(CP, "enableBsm", None) if CP else None,
        "pcm_cruise": getattr(CP, "pcmCruise", None) if CP else None,
        "flags": getattr(CP, "flags", None) if CP else None,
        "auto_resume_sng": getattr(CP, "autoResumeSng", None) if CP else None,
        "radarUnavailable": getattr(CP, "radarUnavailable", None) if CP else None,
        "passive": getattr(CP, "passive", None) if CP else None,
    }

    # Handle special cases for infinity values
    max_lateral_accel = feature_support["max_lateral_accel"]
    if isinstance(max_lateral_accel, float) and (max_lateral_accel == float('inf') or max_lateral_accel == float('-inf')):
        feature_support["max_lateral_accel"] = None

    # Get steering parameters from CarParams
    steering_params = {
        "steer_control_type": enum_to_str(getattr(CP, "steerControlType", None)) if CP else None,
        "steer_actuator_delay": getattr(CP, "steerActuatorDelay", None) if CP else None,
        "steer_ratio_rear": getattr(CP, "steerRatioRear", None) if CP else None,
        "steer_limit_timer": getattr(CP, "steerLimitTimer", None) if CP else None,
    }

    # Get longitudinal parameters from CarParams
    longitudinal_params = {
        "stopping_decel_rate": getattr(CP, "stoppingDecelRate", None) if CP else None,
        "vEgo_stopping": getattr(CP, "vEgoStopping", None) if CP else None,
        "vEgo_starting": getattr(CP, "vEgoStarting", None) if CP else None,
        "stop_accel": getattr(CP, "stopAccel", None) if CP else None,
        "longitudinal_actuator_delay": getattr(CP, "longitudinalActuatorDelay", None) if CP else None,
    }

    # Get tire parameters from CarParams
    tire_params = {
        "tire_stiffness_factor": getattr(CP, "tireStiffnessFactor", None) if CP else None,
        "tire_stiffness_front": getattr(CP, "tireStiffnessFront", None) if CP else None,
        "tire_stiffness_rear": getattr(CP, "tireStiffnessRear", None) if CP else None,
        "rotational_inertia": getattr(CP, "rotationalInertia", None) if CP else None,
    }

    min_steer_speed = car_doc.min_steer_speed
    if car_doc.name.lower() == "comma body" and isinstance(min_steer_speed, float) and min_steer_speed == float('-inf'):
        min_steer_speed = None

    return {
        # Basic car information
        "name": car_doc.name,
        "make": getattr(car_doc, "make", None),
        "model": getattr(car_doc, "model", None),
        "years": getattr(car_doc, "years", None),
        "year_list": getattr(car_doc, "year_list", []),
        "package": car_doc.package,
        "requirements": car_doc.requirements,
        "video": car_doc.video,
        "setup_video": car_doc.setup_video,
        "footnotes": footnotes,
        "min_steer_speed": min_steer_speed,
        "min_enable_speed": car_doc.min_enable_speed,
        "auto_resume": car_doc.auto_resume,
        "car_parts": car_parts,
        "harness": harness_name,
        "merged": car_doc.merged,
        "support_type": car_doc.support_type.value if car_doc.support_type else None,
        "support_link": car_doc.support_link,
        "detail_sentence": getattr(car_doc, "detail_sentence", None),
        "car_fingerprint": getattr(car_doc, "car_fingerprint", None),
        "has_angled_mount": has_angled_mount,
        "brand": getattr(car_doc, "brand", None),
        
        # Detailed parts information
        "detailed_parts": detailed_parts,
        "tools_required": tools_required,
        
        # Row data fields
        "longitudinal": row_data.get("longitudinal", None),
        "fsr_longitudinal": row_data.get("fsr_longitudinal", "0 mph"),
        "fsr_steering": row_data.get("fsr_steering", "0 mph"),
        "steering_torque": row_data.get("steering_torque", None),
        "auto_resume_star": row_data.get("auto_resume", None),
        "hardware": hardware_details,
        "video": row_data.get("video", ""),

        # Car specifications
        **specs,

        # Network and bus information
        **network_info,

        # Feature support details
        **feature_support,

        # Steering parameters
        **steering_params,

        # Longitudinal parameters
        **longitudinal_params,

        # Tire parameters
        **tire_params,
    }


def main():
    """
    Main function to parse arguments and generate the JSON file.
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Generate JSON files with car data')
    parser.add_argument('--output', type=str, default=None,
                        help='Output filename (defaults to all_cars.json)')
    args = parser.parse_args()
    
    # Get all cars
    all_cars = get_all_car_docs()
    default_filename = "all_cars.json"
    description = "all known cars"
    
    # Use provided output filename or default
    output_filename = args.output if args.output else default_filename

    # Build a JSON-serializable list of car information
    cars_data = []
    for car_doc in all_cars:
        # Get CarParams for this car
        model = car_doc.car_fingerprint
        platform = PLATFORMS[model]
        CP = get_params_for_docs(platform)
        
        # Pass platform to car_docs_to_dict
        cars_data.append(car_docs_to_dict(car_doc, CP, platform))

    # Write out to file
    with open(output_filename, 'w') as f:
        json.dump(cars_data, f, indent=2)
    print(f"Generated JSON with {description} in: {os.path.abspath(output_filename)}")


if __name__ == "__main__":
    main() 