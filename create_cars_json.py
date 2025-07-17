#!/usr/bin/env python3
"""
Metadata JSON Generator

It extracts data from CarDocs and CarParams objects into a structured JSON format.

Usage:
source ./setup.sh                               # First time setup
python3 create_cars_json.py                     # Generate regular cars JSON
python3 create_cars_json.py --output custom.json # Custom output filename
python3 create_cars_json.py --everything        # Include community/incompatible cars
python3 create_cars_json.py --verbose           # Detailed progress output
python3 create_cars_json.py --validate          # Validate output after generation
"""

import json
import os
import sys
import logging
import argparse
from typing import Any, Optional
from dataclasses import dataclass


EXCLUDED_SUPPORT_TYPES = ["Not compatible", "Community"]


try:
  from opendbc.car.docs import get_all_car_docs, get_params_for_docs
  from opendbc.car.docs_definitions import CarDocs, Star, BaseCarHarness, Tool
  from opendbc.car.values import PLATFORMS
  from opendbc.car.structs import CarParams
except ImportError as e:
  print("Error: Unable to import opendbc modules.")
  print(f"Import error: {e}")
  print("\nTo fix this:")
  print("1. Ensure you're in the opendbc repository")
  print("2. Run `source ./setup.sh` to set up the environment")
  sys.exit(1)


@dataclass
class ScriptStats:
  total_cars: int = 0
  processed_cars: int = 0
  errors: int = 0
  warnings: int = 0


class MetadataExtractor:
  def __init__(self, verbose: bool = False, everything: bool = False):
    self.everything = everything
    self.stats = ScriptStats()

    # Configure logging
    self.logger = logging.getLogger("car_metadata")
    self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Create console handler with formatter
    console = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S")
    console.setFormatter(formatter)
    self.logger.addHandler(console)

  def _validate_car_doc(self, car_doc: CarDocs) -> bool:
    if not car_doc.name:
      self.logger.warning("Car missing name field")
      self.stats.warnings += 1
      return False

    if not hasattr(car_doc, "car_fingerprint") or not car_doc.car_fingerprint:
      self.logger.warning(f"Car {car_doc.name} missing fingerprint")
      self.stats.warnings += 1
      return False

    return True

  def _convert_enum(self, value: Any) -> str | None:
    if value is None:
      return None
    return value.value if hasattr(value, "value") else (
           value.name if hasattr(value, "name") else str(value))

  def deep_get(self, obj: Any, path: str, default: Any = None) -> Any:
    if obj is None:
      return default

    # Optimize for the common case
    if '.' not in path:
      return getattr(obj, path, default)

    nested_value = obj
    for attr in path.split('.'):
      try:
        nested_value = getattr(nested_value, attr)
      except (AttributeError, KeyError):
        return default
    return nested_value

  def extract_car_data(self, car_doc: CarDocs) -> dict[str, Any] | None:
    if not self._validate_car_doc(car_doc):
      return None

    try:
      # Get platform for this car
      model = car_doc.car_fingerprint
      platform = PLATFORMS.get(model)
      if not platform:
        self.logger.error(f"Platform not found for {car_doc.name}")
        self.stats.errors += 1
        return None

      # Get car parameters
      CP = get_params_for_docs(platform)

      # Build the car data dictionary
      car_data = {}
      car_data.update(self._extract_basic_info(car_doc))
      car_data.update(self._extract_parts_info(car_doc))
      car_data.update(self._extract_row_data(car_doc))
      car_data.update(self._extract_vehicle_configs(car_doc, CP, platform))

      return car_data

    except Exception:
      self.logger.exception(f"Error processing {car_doc.name}")
      self.stats.errors += 1
      return None

  def _extract_basic_info(self, car_doc: CarDocs) -> dict[str, Any]:
    # Extract footnotes safely
    footnotes = []
    try:
      if car_doc.footnotes:
        footnotes = [fn.value.text for fn in car_doc.footnotes]
    except Exception:
      pass

    # Handle special case for min_steer_speed
    min_steer_speed = car_doc.min_steer_speed
    if car_doc.name.lower() == "comma body" and isinstance(min_steer_speed, float) and min_steer_speed == float("-inf"):
      min_steer_speed = None

    return {
      "name": car_doc.name,
      "make": self.deep_get(car_doc, "make"),
      "model": self.deep_get(car_doc, "model"),
      "years": self.deep_get(car_doc, "years"),
      "year_list": self.deep_get(car_doc, "year_list", []),
      "package": car_doc.package,
      "requirements": car_doc.requirements,
      "video": car_doc.video,
      "setup_video": car_doc.setup_video,
      "footnotes": footnotes,
      "min_steer_speed": min_steer_speed,
      "min_enable_speed": car_doc.min_enable_speed,
      "auto_resume": car_doc.auto_resume,
      "merged": car_doc.merged,
      "support_type": car_doc.support_type.value if car_doc.support_type else None,
      "support_link": car_doc.support_link,
      "detail_sentence": self.deep_get(car_doc, "detail_sentence"),
      "car_fingerprint": self.deep_get(car_doc, "car_fingerprint"),
      "brand": self.deep_get(car_doc, "brand"),
    }

  def _extract_parts_info(self, car_doc: CarDocs) -> dict[str, Any]:
    # Default values for when no parts are available
    if not car_doc.car_parts or not car_doc.car_parts.parts:
      return {
        "car_parts": [],
        "harness": None,
        "has_angled_mount": False,
        "detailed_parts": [],
        "tools_required": [],
        "hardware": "",
      }

    # Get all parts including sub-parts
    all_parts = car_doc.car_parts.all_parts()
    parts_list = [part for part in all_parts if not isinstance(part, Tool)]
    tools_list = [part for part in all_parts if isinstance(part, Tool)]

    # Extract basic info
    angled_mount_parts = ["angled_mount_8_degrees", "threex_angled_mount"]
    car_parts = []
    harness_name = None
    has_angled_mount = any(part.name in angled_mount_parts for part in all_parts)

    # Get basic parts and harness
    for part_enum in car_doc.car_parts.parts:
      base_part = part_enum.value
      car_parts.append(base_part.name)
      if isinstance(base_part, BaseCarHarness):
        harness_name = part_enum.name.lower()

    # Format hardware HTML
    hardware_details = self._format_hardware_html(car_doc, parts_list, tools_list)

    return {
      "car_parts": car_parts,
      "harness": harness_name,
      "has_angled_mount": has_angled_mount,
      "detailed_parts": self._format_detailed_parts(parts_list),
      "tools_required": self._format_tools_required(tools_list),
      "hardware": hardware_details,
    }

  def _format_detailed_parts(self, parts_list: list[Any]) -> list[dict[str, Any]]:
    detailed_parts = []
    for part in sorted(set(parts_list), key=lambda p: str(p.value.name)):
      count = parts_list.count(part)
      part_type = part.part_type.name if hasattr(part, "part_type") else None
      detailed_parts.append({
        "count": count,
        "name": part.value.name,
        "type": part_type,
        "enum_name": part.name
      })
    return detailed_parts

  def _format_tools_required(self, tools_list: list[Any]) -> list[dict[str, Any]]:
    tools_required = []
    for tool in sorted(set(tools_list), key=lambda t: str(t.value.name)):
      count = tools_list.count(tool)
      tools_required.append({
        "count": count,
        "name": tool.value.name,
        "enum_name": tool.name
      })
    return tools_required

  def _format_hardware_html(self, car_doc: CarDocs, parts_list: list[Any], tools_list: list[Any]) -> str:
    model_years = car_doc.model + (" " + car_doc.years if car_doc.years else "")
    buy_link = f'<a href="https://comma.ai/shop/comma-3x.html?make={car_doc.make}&model={model_years}">Buy Here</a>'

    # Format parts list
    display_parts = "<br>".join([
      f"- {parts_list.count(part)} {part.value.name}"
      for part in sorted(set(parts_list), key=lambda part: str(part.value.name))
    ])

    hardware_details = f"<details><summary>Parts</summary><sub>{display_parts}<br>{buy_link}</sub></details>"

    # Add tools if any exist
    if tools_list:
      display_tools = "<br>".join([
        f"- {tools_list.count(tool)} {tool.value.name}"
        for tool in sorted(set(tools_list), key=lambda tool: str(tool.value.name))
      ])
      hardware_details += f"<details><summary>Tools</summary><sub>{display_tools}</sub></details>"

    return hardware_details

  def _extract_row_data(self, car_doc: CarDocs) -> dict[str, Any]:
    row_data = {}
    default_fsr_speed = "0 mph"

    if hasattr(car_doc, "row"):
      for col_enum, col_value in car_doc.row.items():
        key = col_enum.name.lower()
        value = col_value.value if isinstance(col_value, Star) else col_value
        row_data[key] = value

    return {
      "longitudinal": row_data.get("longitudinal"),
      "fsr_longitudinal": row_data.get("fsr_longitudinal", default_fsr_speed),
      "fsr_steering": row_data.get("fsr_steering", default_fsr_speed),
      "steering_torque": row_data.get("steering_torque"),
      "auto_resume_star": row_data.get("auto_resume"),
      "video_row": row_data.get("video", ""),
    }

  # Not using pipe syntax (CarParams | None) because capnp types don't support it at runtime
  def _extract_vehicle_configs(self, car_doc: CarDocs, CP: Optional[CarParams], platform: Any) -> dict[str, Any]:  # noqa: UP007
    # Calculate center to front ratio
    center_to_front_ratio = 0.5  # Default value
    if CP and hasattr(CP, "centerToFront") and hasattr(CP, "wheelbase") and CP.wheelbase > 0:
      try:
        center_to_front_ratio = CP.centerToFront / CP.wheelbase
      except (AttributeError, ZeroDivisionError) as e:
        self.logger.warning(f"Error calculating center_to_front_ratio for {car_doc.name}: {e}")

    # Handle special case for max lateral accel
    max_lateral_accel = self.deep_get(CP, "maxLateralAccel")
    if isinstance(max_lateral_accel, float) and (max_lateral_accel in [float("inf"), float("-inf")]):
      max_lateral_accel = None

    # Extract configurations
    return {
      # Basic specs
      "mass": self.deep_get(CP, "mass"),
      "mass_curb_weight": self.deep_get(platform, "config.specs.mass"),
      "wheelbase": self.deep_get(CP, "wheelbase"),
      "steer_ratio": self.deep_get(CP, "steerRatio"),
      "center_to_front_ratio": center_to_front_ratio,
      "center_to_front_ratio_base": self.deep_get(platform, "config.specs.centerToFrontRatio"),
      "max_lateral_accel": max_lateral_accel,

      # Network and bus config
      "network_location": self._convert_enum(self.deep_get(CP, "networkLocation")),
      "bus_lookup": self.deep_get(platform, "config.dbc_dict"),
      "radar_delay": self.deep_get(CP, "radarDelay"),
      "wheel_speed_factor": self.deep_get(CP, "wheelSpeedFactor"),

      # Speed settings
      "start_accel": self.deep_get(CP, "startAccel"),
      "min_steer_speed_base": self.deep_get(platform, "config.specs.minSteerSpeed"),
      "min_enable_speed": self.deep_get(CP, "minEnableSpeed"),
      "min_enable_speed_base": self.deep_get(platform, "config.specs.minEnableSpeed"),

      # Steering configuration
      "steer_control_type": self._convert_enum(self.deep_get(CP, "steerControlType")),
      "steer_actuator_delay": self.deep_get(CP, "steerActuatorDelay"),
      "steer_ratio_rear": self.deep_get(CP, "steerRatioRear"),
      "steer_limit_timer": self.deep_get(CP, "steerLimitTimer"),

      # Tire and inertia config
      "tire_stiffness_factor": self.deep_get(CP, "tireStiffnessFactor"),
      "tire_stiffness_factor_base": self.deep_get(platform, "config.specs.tireStiffnessFactor"),
      "tire_stiffness_front": self.deep_get(CP, "tireStiffnessFront"),
      "tire_stiffness_rear": self.deep_get(CP, "tireStiffnessRear"),
      "rotational_inertia": self.deep_get(CP, "rotationalInertia"),

      # Features and capabilities
      "experimental_longitudinal_available": self.deep_get(CP, "experimentalLongitudinalAvailable"),
      "openpilot_longitudinal_control": self.deep_get(CP, "openpilotLongitudinalControl"),
      "dashcam_only": self.deep_get(CP, "dashcamOnly"),
      "enable_dsu": self.deep_get(CP, "enableDsu"),
      "enable_bsm": self.deep_get(CP, "enableBsm"),
      "pcm_cruise": self.deep_get(CP, "pcmCruise"),
      "flags": self.deep_get(CP, "flags"),
      "auto_resume_sng": self.deep_get(CP, "autoResumeSng"),
      "radarUnavailable": self.deep_get(CP, "radarUnavailable"),
      "passive": self.deep_get(CP, "passive"),

      # Longitudinal config
      "stopping_decel_rate": self.deep_get(CP, "stoppingDecelRate"),
      "vEgo_stopping": self.deep_get(CP, "vEgoStopping"),
      "vEgo_starting": self.deep_get(CP, "vEgoStarting"),
      "stop_accel": self.deep_get(CP, "stopAccel"),
      "longitudinal_actuator_delay": self.deep_get(CP, "longitudinalActuatorDelay"),
    }

  def validate_output(self, cars_data: list[dict[str, Any]]) -> bool:
    self.logger.info("Validating generated data...")

    validation_errors = 0
    required_fields = ["name", "make", "model", "car_fingerprint"]
    valid_mass_range = (500, 5000)  # kg
    valid_wheelbase_range = (1.0, 5.0)  # meters

    for i, car in enumerate(cars_data):
      # Check required fields
      for field in required_fields:
        if not car.get(field):
          self.logger.error(f"Car {i} missing required field: {field}")
          validation_errors += 1

      # Check for reasonable data ranges
      mass = car.get("mass")
      if mass is not None:
        min_mass, max_mass = valid_mass_range
        if mass < min_mass or mass > max_mass:
          self.logger.warning(f"Car {car.get('name', i)} has suspicious mass: {mass} kg")
          self.stats.warnings += 1

      wheelbase = car.get("wheelbase")
      if wheelbase is not None:
        min_wb, max_wb = valid_wheelbase_range
        if wheelbase < min_wb or wheelbase > max_wb:
          self.logger.warning(f"Car {car.get('name', i)} has suspicious wheelbase: {wheelbase} m")
          self.stats.warnings += 1

    if validation_errors > 0:
      self.logger.error(f"Validation failed with {validation_errors} errors")
      return False

    self.logger.info("Validation passed!")
    return True

  def get_all_cars(self) -> list[CarDocs]:
    try:
      all_cars = get_all_car_docs()

      if not self.everything:
        return [
          car for car in all_cars
          if getattr(car, "support_type", None) is not None
          and car.support_type.value not in EXCLUDED_SUPPORT_TYPES
        ]

      return all_cars
    except Exception:
      self.logger.exception("Error retrieving car docs")
      self.stats.errors += 1
      return []

  def generate_json(self, output_filename: str, validate: bool = False) -> bool:
    self.logger.info("Starting car data extraction...")

    # Get all cars
    all_cars = self.get_all_cars()
    self.stats.total_cars = len(all_cars)

    if self.stats.total_cars == 0:
      self.logger.error("Error: No cars found. Check your opendbc installation.")
      return False

    car_type = "all known cars" if self.everything else "supported cars"
    self.logger.info(f"Processing {self.stats.total_cars} {car_type}...")

    # Process all cars
    cars_data = []
    for car_doc in all_cars:
      car_dict = self.extract_car_data(car_doc)
      if car_dict:
        cars_data.append(car_dict)
        self.stats.processed_cars += 1

    # Check if we processed any cars
    if not cars_data:
      self.logger.error("Error: No car data was processed successfully.")
      return False

    def sort_by_make_then_model(car):
      return (car.get('make') or '', car.get('model') or '')

    cars_data = sorted(cars_data, key=sort_by_make_then_model)

    # Write out to file
    self.logger.info(f"Writing {len(cars_data)} cars to {output_filename}...")

    try:
      with open(output_filename, "w") as f:
        json.dump(cars_data, f, indent=2, ensure_ascii=False)
    except OSError:
      self.logger.exception(f"Error writing to file {output_filename}")
      return False

    # Validate output if requested
    if validate and not self.validate_output(cars_data):
      return False

    # Success summary
    self.logger.info("=" * 30)
    self.logger.info("GENERATION COMPLETE")
    self.logger.info("=" * 30)
    self.logger.info(f"Total cars processed: {self.stats.processed_cars}/{self.stats.total_cars}")
    if self.stats.errors > 0 or self.stats.warnings > 0:
      self.logger.info(f"Errors: {self.stats.errors}, Warnings: {self.stats.warnings}")
    self.logger.info(f"Output file: {os.path.abspath(output_filename)}")

    return True


def main():
  # Set up command-line argument parsing
  parser = argparse.ArgumentParser(
    description="Generate JSON files with car data from opendbc",
    epilog="""
Examples:
  %(prog)s                          # Generate supported cars only
  %(prog)s --everything             # Include community/incompatible cars
  %(prog)s --output custom.json     # Custom output filename
  %(prog)s --verbose --validate     # Detailed output with validation
        """,
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )

  parser.add_argument("--output", type=str, default=None, help="Output filename (defaults to all_cars.json or supported_cars.json)")
  parser.add_argument("--everything", action="store_true", help="Include community and incompatible cars (default: supported cars only)")
  parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output with progress reporting")
  parser.add_argument("--validate", action="store_true", help="Validate output data after generation")

  args = parser.parse_args()

  # Determine output filename
  output_filename = args.output or ("all_cars.json" if args.everything else "supported_cars.json")

  # Create extractor and generate JSON
  extractor = MetadataExtractor(verbose=args.verbose, everything=args.everything)

  try:
    success = extractor.generate_json(output_filename, validate=args.validate)
    sys.exit(0 if success else 1)
  except KeyboardInterrupt:
    print("\nGeneration interrupted by user")
    sys.exit(130)
  except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)


if __name__ == "__main__":
  main()