#!/usr/bin/env python3
import argparse
import contextlib
import json
import logging
import sys
from pathlib import Path
from typing import Any, TypeVar
from collections.abc import Callable

try:
  from opendbc.car.docs import get_all_car_docs, get_params_for_docs
  from opendbc.car.docs_definitions import BaseCarHarness
  from opendbc.car.values import PLATFORMS
except ImportError:
  print("Error: Unable to import opendbc modules. Run 'source ./setup.sh' first.")
  sys.exit(1)

logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S", level=logging.INFO)
logger = logging.getLogger("car_metadata")

EXCLUDED_SUPPORT_TYPES = ["Not compatible", "Community"]

T = TypeVar('T')

def safe_get(obj: Any, attr: str, default: Any = None) -> Any:
  """Get attribute safely with a default value."""
  return getattr(obj, attr, default)

def to_json(value: Any) -> Any:
  """Convert any value to JSON-serializable format."""
  if value is None or isinstance(value, str | int | float | bool):
    return value
  if hasattr(value, "value"):
    return value.value
  if hasattr(value, "name"):
    return value.name
  return str(value)

def extract_list(obj: Any, attr: str, extractor: Callable = lambda x: x, check: Callable = None) -> list:
  """Extract a list from an object attribute using extractor function."""
  items = getattr(obj, attr, None)
  if not items:
    return []
  if check and not check(items):
    return []
  return [extractor(item) for item in items]

def has_all(obj: Any, *attrs: str) -> bool:
  """Check if object has all the specified attributes."""
  return all(hasattr(obj, attr) for attr in attrs)

def get_car_parts_info(car_doc: Any) -> dict:
  """Extract car parts information."""
  result = {"car_parts": [], "harness": None, "has_angled_mount": False}

  if not (hasattr(car_doc, "car_parts") and car_doc.car_parts and
          hasattr(car_doc.car_parts, "all_parts")):
    return result

  try:
    all_parts = car_doc.car_parts.all_parts()
    angled_mount_parts = ["angled_mount_8_degrees", "threex_angled_mount"]
    result["has_angled_mount"] = any(part.name in angled_mount_parts for part in all_parts)

    for part_enum in car_doc.car_parts.parts:
      base_part = part_enum.value
      result["car_parts"].append(base_part.name)
      if isinstance(base_part, BaseCarHarness):
        result["harness"] = part_enum.name.lower()
  except Exception:
    logger.debug(f"Error processing car parts for {car_doc.name}")

  return result

def get_car_params_attrs(cp: Any) -> dict:
  """Extract attributes from CarParams object."""
  # Calculate center to front ratio
  center_to_front_ratio = 0.5  # Default value
  if cp and has_all(cp, "centerToFront", "wheelbase") and cp.wheelbase > 0:
    with contextlib.suppress(AttributeError, ZeroDivisionError):
      center_to_front_ratio = cp.centerToFront / cp.wheelbase

  # Handle special case for max lateral accel
  max_lateral_accel = safe_get(cp, "maxLateralAccel")
  if isinstance(max_lateral_accel, float) and max_lateral_accel in [float("inf"), float("-inf")]:
    max_lateral_accel = None

  return {
    # Basic specs
    "mass": safe_get(cp, "mass"),
    "wheelbase": safe_get(cp, "wheelbase"),
    "steer_ratio": safe_get(cp, "steerRatio"),
    "center_to_front_ratio": center_to_front_ratio,
    "max_lateral_accel": max_lateral_accel,
    # Network and bus config
    "network_location": to_json(safe_get(cp, "networkLocation")),
    "radar_delay": safe_get(cp, "radarDelay"),
    "wheel_speed_factor": safe_get(cp, "wheelSpeedFactor"),
    # Speed settings
    "start_accel": safe_get(cp, "startAccel"),
    # Steering configuration
    "steer_control_type": to_json(safe_get(cp, "steerControlType")),
    "steer_actuator_delay": safe_get(cp, "steerActuatorDelay"),
    "steer_ratio_rear": safe_get(cp, "steerRatioRear"),
    "steer_limit_timer": safe_get(cp, "steerLimitTimer"),
    # Tire and inertia config
    "tire_stiffness_factor": safe_get(cp, "tireStiffnessFactor"),
    "tire_stiffness_front": safe_get(cp, "tireStiffnessFront"),
    "tire_stiffness_rear": safe_get(cp, "tireStiffnessRear"),
    "rotational_inertia": safe_get(cp, "rotationalInertia"),
    # Features and capabilities
    "experimental_longitudinal_available": safe_get(cp, "alphaLongitudinalAvailable"),
    "openpilot_longitudinal_control": safe_get(cp, "openpilotLongitudinalControl"),
    "dashcam_only": safe_get(cp, "dashcamOnly"),
    "enable_dsu": safe_get(cp, "enableDsu"),
    "enable_bsm": safe_get(cp, "enableBsm"),
    "pcm_cruise": safe_get(cp, "pcmCruise"),
    "flags": safe_get(cp, "flags"),
    "auto_resume_sng": safe_get(cp, "autoResumeSng"),
    "radarUnavailable": safe_get(cp, "radarUnavailable"),
    "passive": safe_get(cp, "passive"),
    # Longitudinal config
    "stopping_decel_rate": safe_get(cp, "stoppingDecelRate"),
    "vEgo_stopping": safe_get(cp, "vEgoStopping"),
    "vEgo_starting": safe_get(cp, "vEgoStarting"),
    "stop_accel": safe_get(cp, "stopAccel"),
    "longitudinal_actuator_delay": safe_get(cp, "longitudinalActuatorDelay"),
  }

def get_platform_attrs(platform: Any) -> dict:
  """Extract platform configuration attributes."""
  result = {}

  if has_all(platform, "config") and has_all(platform.config, "specs"):
    specs = platform.config.specs
    result.update({
      "mass_curb_weight": safe_get(specs, "mass"),
      "center_to_front_ratio_base": safe_get(specs, "centerToFrontRatio"),
      "min_steer_speed_base": safe_get(specs, "minSteerSpeed"),
      "min_enable_speed_base": safe_get(specs, "minEnableSpeed"),
      "tire_stiffness_factor_base": safe_get(specs, "tireStiffnessFactor"),
    })

  if hasattr(platform, "config"):
    result["bus_lookup"] = safe_get(platform.config, "dbc_dict")

  return result

def extract_metadata(car_doc: Any) -> dict | None:
  """Extract comprehensive metadata from a car document."""
  model = safe_get(car_doc, "car_fingerprint")
  if not model or model not in PLATFORMS:
    return None

  platform = PLATFORMS[model]
  cp = get_params_for_docs(platform)
  if not cp:
    return None

  # Basic car attributes
  basic_attrs = {
    field: safe_get(car_doc, field)
    for field in ["make", "model", "years", "year_list", "package", "requirements",
                 "video", "setup_video", "merged", "brand", "support_link", "detail_sentence"]
  }

  # Build initial metadata
  metadata = {
    "name": car_doc.name,
    "car_fingerprint": model,
    "support_type": to_json(safe_get(car_doc, "support_type")),
    "longitudinal": None,
    "fsr_longitudinal": "0 mph",
    "fsr_steering": "0 mph",
    "steering_torque": None,
    "auto_resume_star": "empty",
    "video_row": "",
    "detailed_parts": [],
    "tools_required": [],
    "hardware": "",
    "footnotes": extract_list(car_doc, "footnotes", lambda fn: fn.value.text),
    **basic_attrs,
    **get_car_parts_info(car_doc)
  }

  # Handle special case for min_steer_speed
  min_steer_speed = safe_get(car_doc, "min_steer_speed")
  is_comma_body_inf = (car_doc.name.lower() == "comma body" and
                      isinstance(min_steer_speed, float) and
                      min_steer_speed == float("-inf"))
  metadata["min_steer_speed"] = None if is_comma_body_inf else min_steer_speed
  metadata["min_enable_speed"] = safe_get(car_doc, "min_enable_speed")
  metadata["auto_resume"] = safe_get(car_doc, "auto_resume")

  # Handle row data
  if hasattr(car_doc, "row"):
    for key, value in car_doc.row.items():
      field_name = key.name.lower()
      metadata[field_name] = to_json(value)
      if field_name == "video" and value:
        metadata["video_row"] = str(value)

  # Add CarParams and platform attributes
  metadata.update(get_car_params_attrs(cp))
  metadata.update(get_platform_attrs(platform))

  return metadata

def main():
  """Generate car metadata files from car documentation."""
  parser = argparse.ArgumentParser(description="Generate car metadata files")
  parser.add_argument("--output", "-o", type=str, default="./output", help="Output directory")
  parser.add_argument("--everything", action="store_true", help="Include all cars")
  parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
  args = parser.parse_args()

  if args.verbose:
    logger.setLevel(logging.DEBUG)

  output_dir = Path(args.output)
  output_dir.mkdir(parents=True, exist_ok=True)

  # Get and filter car docs
  all_cars = get_all_car_docs()
  if not args.everything:
    all_cars = [car for car in all_cars if hasattr(car, "support_type") and car.support_type is not None
                and car.support_type.value not in EXCLUDED_SUPPORT_TYPES]

  logger.info(f"Processing {len(all_cars)} cars...")

  # Extract metadata
  cars_data, processed, errors = [], 0, 0
  for car_doc in all_cars:
    try:
      metadata = extract_metadata(car_doc)
      if metadata:
        cars_data.append(metadata)
        processed += 1
      else:
        errors += 1
    except Exception:
      logger.exception(f"Error processing {car_doc.name}")
      errors += 1

  # Sort and save
  cars_data.sort(key=lambda car: (car.get("make", ""), car.get("model", "")))
  json_file = output_dir / "cars.json"
  with json_file.open("w") as f:
    json.dump(cars_data, f, indent=2)

  logger.info(f"Generated {len(cars_data)} car entries in {json_file}")
  logger.info(f"Processed: {processed}, Errors: {errors}")

if __name__ == "__main__":
  main()
