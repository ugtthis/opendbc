#!/usr/bin/env python3
import argparse
import contextlib
import json
import logging
import sys
from pathlib import Path

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

def serialize_value(value):
  """Convert enum types and other special values to JSON-serializable formats."""
  if value is None or isinstance(value, str | int | float | bool):
    return value
  # Handle enum types with .value attribute (most common case)
  if hasattr(value, "value"):
    return value.value
  # Handle enum types with .name attribute
  if hasattr(value, "name"):
    return value.name
  # Convert anything else to string
  return str(value)

def extract_metadata(car_doc):
  """Extract comprehensive metadata from a car document."""
  model = getattr(car_doc, "car_fingerprint", None)
  if not model or model not in PLATFORMS:
    return None

  platform = PLATFORMS[model]
  CP = get_params_for_docs(platform)
  if not CP:
    return None

  metadata = {
    "name": car_doc.name,
    "make": getattr(car_doc, "make", None),
    "model": getattr(car_doc, "model", None),
    "years": getattr(car_doc, "years", None),
    "year_list": getattr(car_doc, "year_list", []),
    "package": getattr(car_doc, "package", None),
    "requirements": getattr(car_doc, "requirements", None),
    "video": getattr(car_doc, "video", None),
    "setup_video": getattr(car_doc, "setup_video", None),
    "merged": getattr(car_doc, "merged", None),
    "car_fingerprint": model,
    "brand": getattr(car_doc, "brand", None),
    "support_link": getattr(car_doc, "support_link", None),
    "detail_sentence": getattr(car_doc, "detail_sentence", None),
    "support_type": serialize_value(getattr(car_doc, "support_type", None)),
    "longitudinal": None, "fsr_longitudinal": "0 mph", "fsr_steering": "0 mph",
    "steering_torque": None, "auto_resume_star": "empty", "video_row": "",
    "car_parts": [], "harness": None, "has_angled_mount": False,
    "detailed_parts": [], "tools_required": [], "hardware": "",
    "footnotes": [fn.value.text for fn in car_doc.footnotes] if hasattr(car_doc, "footnotes") and car_doc.footnotes else [],
  }

  # Handle special case for min_steer_speed
  min_steer_speed = getattr(car_doc, "min_steer_speed", None)
  is_comma_body_inf = (car_doc.name.lower() == "comma body" and
                      isinstance(min_steer_speed, float) and
                      min_steer_speed == float("-inf"))
  metadata["min_steer_speed"] = None if is_comma_body_inf else min_steer_speed
  metadata["min_enable_speed"] = getattr(car_doc, "min_enable_speed", None)
  metadata["auto_resume"] = getattr(car_doc, "auto_resume", None)

  # Handle row data
  if hasattr(car_doc, "row"):
    for key, value in car_doc.row.items():
      field_name = key.name.lower()
      metadata[field_name] = serialize_value(value)
      if field_name == "video" and value:
        metadata["video_row"] = str(value)

  # Extract parts information
  if hasattr(car_doc, "car_parts") and car_doc.car_parts and hasattr(car_doc.car_parts, "all_parts"):
    try:
      all_parts = car_doc.car_parts.all_parts()
      # Check for angled mount
      angled_mount_parts = ["angled_mount_8_degrees", "threex_angled_mount"]
      metadata["has_angled_mount"] = any(part.name in angled_mount_parts for part in all_parts)
      # Extract harness info
      for part_enum in car_doc.car_parts.parts:
        base_part = part_enum.value
        metadata["car_parts"].append(base_part.name)
        if isinstance(base_part, BaseCarHarness):
          metadata["harness"] = part_enum.name.lower()
    except Exception:
      logger.debug(f"Error processing car parts for {car_doc.name}")

  # Calculate center to front ratio
  center_to_front_ratio = 0.5  # Default value
  if CP and hasattr(CP, "centerToFront") and hasattr(CP, "wheelbase") and CP.wheelbase > 0:
    with contextlib.suppress(AttributeError, ZeroDivisionError):
      center_to_front_ratio = CP.centerToFront / CP.wheelbase

  # Handle special case for max lateral accel
  max_lateral_accel = getattr(CP, "maxLateralAccel", None)
  if isinstance(max_lateral_accel, float) and max_lateral_accel in [float("inf"), float("-inf")]:
    max_lateral_accel = None

  # Add CarParams attributes
  cp_attrs = {
    # Basic specs
    "mass": getattr(CP, "mass", None),
    "wheelbase": getattr(CP, "wheelbase", None),
    "steer_ratio": getattr(CP, "steerRatio", None),
    "center_to_front_ratio": center_to_front_ratio,
    "max_lateral_accel": max_lateral_accel,
    # Network and bus config
    "network_location": serialize_value(getattr(CP, "networkLocation", None)),
    "radar_delay": getattr(CP, "radarDelay", None),
    "wheel_speed_factor": getattr(CP, "wheelSpeedFactor", None),
    # Speed settings
    "start_accel": getattr(CP, "startAccel", None),
    # Steering configuration
    "steer_control_type": serialize_value(getattr(CP, "steerControlType", None)),
    "steer_actuator_delay": getattr(CP, "steerActuatorDelay", None),
    "steer_ratio_rear": getattr(CP, "steerRatioRear", None),
    "steer_limit_timer": getattr(CP, "steerLimitTimer", None),
    # Tire and inertia config
    "tire_stiffness_factor": getattr(CP, "tireStiffnessFactor", None),
    "tire_stiffness_front": getattr(CP, "tireStiffnessFront", None),
    "tire_stiffness_rear": getattr(CP, "tireStiffnessRear", None),
    "rotational_inertia": getattr(CP, "rotationalInertia", None),
    # Features and capabilities
    "experimental_longitudinal_available": getattr(CP, "alphaLongitudinalAvailable", None),
    "openpilot_longitudinal_control": getattr(CP, "openpilotLongitudinalControl", None),
    "dashcam_only": getattr(CP, "dashcamOnly", None),
    "enable_dsu": getattr(CP, "enableDsu", None),
    "enable_bsm": getattr(CP, "enableBsm", None),
    "pcm_cruise": getattr(CP, "pcmCruise", None),
    "flags": getattr(CP, "flags", None),
    "auto_resume_sng": getattr(CP, "autoResumeSng", None),
    "radarUnavailable": getattr(CP, "radarUnavailable", None),
    "passive": getattr(CP, "passive", None),
    # Longitudinal config
    "stopping_decel_rate": getattr(CP, "stoppingDecelRate", None),
    "vEgo_stopping": getattr(CP, "vEgoStopping", None),
    "vEgo_starting": getattr(CP, "vEgoStarting", None),
    "stop_accel": getattr(CP, "stopAccel", None),
    "longitudinal_actuator_delay": getattr(CP, "longitudinalActuatorDelay", None),
  }

  # Add platform config attributes
  if hasattr(platform, "config") and hasattr(platform.config, "specs"):
    specs = platform.config.specs
    cp_attrs.update({
      "mass_curb_weight": getattr(specs, "mass", None),
      "center_to_front_ratio_base": getattr(specs, "centerToFrontRatio", None),
      "min_steer_speed_base": getattr(specs, "minSteerSpeed", None),
      "min_enable_speed_base": getattr(specs, "minEnableSpeed", None),
      "tire_stiffness_factor_base": getattr(specs, "tireStiffnessFactor", None),
    })

  if hasattr(platform, "config"):
    cp_attrs["bus_lookup"] = getattr(platform.config, "dbc_dict", None)

  metadata.update(cp_attrs)
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
