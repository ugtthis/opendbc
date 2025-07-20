#!/usr/bin/env python3
import json
import sys
import logging
import argparse
from pathlib import Path

try:
  from opendbc.car.docs import get_all_car_docs, get_params_for_docs
  from opendbc.car.docs_definitions import BaseCarHarness, Column
  from opendbc.car.values import PLATFORMS
except ImportError:
  print("Error: Unable to import opendbc modules. Run 'source ./setup.sh' first.")
  sys.exit(1)

logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S", level=logging.INFO)
logger = logging.getLogger("car_metadata")

EXCLUDED_SUPPORT_TYPES = ["Not compatible", "Community"]

def to_json_type(value):
  """Convert any value to a JSON-serializable type."""
  if value is None:
    return None
  if isinstance(value, (str, int, float, bool)):
    return value
  if hasattr(value, "value"):
    return value.value
  if hasattr(value, "name"):
    return value.name
  return str(value)

def format_items_to_dicts(items):
  """Format a list of enum items into structured dictionaries with counts."""
  if not items:
    return []
    
  # Count occurrences of each item
  item_counts = {}
  for item in items:
    item_counts[item] = item_counts.get(item, 0) + 1

  # Format items into dictionaries
  return [{
    "count": item_counts[item],
    "name": item.value.name if hasattr(item, "value") and hasattr(item.value, "name") else str(item),
    "enum_name": item.name if hasattr(item, "name") else "",
    "type": item.part_type.name if hasattr(item, "part_type") else None
  } for item in sorted(item_counts, key=lambda x: str(x.value.name) if hasattr(x, "value") else str(x))]

def extract_metadata(car_doc):
  """Extract metadata from a car document."""
  model = getattr(car_doc, "car_fingerprint", None)
  if not model or model not in PLATFORMS:
    return None

  platform = PLATFORMS[model]
  cp = get_params_for_docs(platform)
  if not cp:
    return None

  # Calculate special values
  min_steer_speed = getattr(car_doc, "min_steer_speed", None)
  min_steer_speed = None if (car_doc.name.lower() == "comma body" and 
                             isinstance(min_steer_speed, float) and 
                             min_steer_speed == float("-inf")) else min_steer_speed
  
  auto_resume = getattr(car_doc, "auto_resume", None)
  if auto_resume is None and cp:
    min_enable_speed = getattr(car_doc, "min_enable_speed", 0) or 0
    auto_resume = getattr(cp, "autoResumeSng", False) and min_enable_speed <= 0
  
  max_lateral_accel = getattr(cp, "maxLateralAccel", None)
  if isinstance(max_lateral_accel, float) and max_lateral_accel in [float("inf"), float("-inf")]:
    max_lateral_accel = None
    
  center_to_front_ratio = 0.5  # Default value
  if cp and hasattr(cp, "centerToFront") and hasattr(cp, "wheelbase") and cp.wheelbase > 0:
    try:
      center_to_front_ratio = cp.centerToFront / cp.wheelbase
    except (AttributeError, ZeroDivisionError):
      pass
  
  # Process car parts
  parts_list, tools_list = [], []
  car_parts, harness, has_angled_mount = [], None, False
  
  if hasattr(car_doc, "car_parts") and car_doc.car_parts and hasattr(car_doc.car_parts, "all_parts"):
    try:
      all_parts = car_doc.car_parts.all_parts()
      parts_list = [p for p in all_parts if not isinstance(p, Tool)]
      tools_list = [p for p in all_parts if isinstance(p, Tool)]
      
      # Check for angled mount
      angled_mount_parts = ["angled_mount_8_degrees", "threex_angled_mount"]
      has_angled_mount = any(part.name in angled_mount_parts for part in all_parts)
      
      # Extract basic part info
      for part_enum in car_doc.car_parts.parts:
        base_part = part_enum.value
        car_parts.append(base_part.name if hasattr(base_part, "name") else str(base_part))
        if isinstance(base_part, BaseCarHarness):
          harness = part_enum.name.lower()
    except Exception as e:
      logger.debug(f"Error processing car parts for {car_doc.name}: {e}")

  # Generate shop link
  model_years = getattr(car_doc, "model", "") + (" " + getattr(car_doc, "years", "") if hasattr(car_doc, "years") else "")
  shop_link = f"https://comma.ai/shop/comma-3x.html?make={getattr(car_doc, 'make', '')}&model={model_years}"
  
  # Extract footnotes
  footnotes = [fn.value.text for fn in getattr(car_doc, "footnotes", [])] if hasattr(car_doc, "footnotes") else []

  # Basic metadata
  metadata = {
    # Car info
    "name": car_doc.name,
    "make": getattr(car_doc, "make", None),
    "model": getattr(car_doc, "model", None),
    "years": getattr(car_doc, "years", None),
    "year_list": getattr(car_doc, "year_list", []),
    "package": getattr(car_doc, "package", None),
    "requirements": getattr(car_doc, "requirements", None),
    "car_fingerprint": model,
    "brand": getattr(car_doc, "brand", None),
    "merged": getattr(car_doc, "merged", None),
    
    # Support and documentation
    "support_link": getattr(car_doc, "support_link", None),
    "detail_sentence": getattr(car_doc, "detail_sentence", None),
    "support_type": to_json_type(getattr(car_doc, "support_type", None)),
    "video": getattr(car_doc, "video", None),
    "setup_video": getattr(car_doc, "setup_video", None),
    "footnotes": footnotes,
    "shop_link": shop_link,
    
    # Speed and control
    "longitudinal": getattr(car_doc, "longitudinal", None),
    "min_steer_speed": min_steer_speed,
    "min_enable_speed": getattr(car_doc, "min_enable_speed", None),
    "fsr_longitudinal": "0 mph",
    "fsr_steering": "0 mph",
    "steering_torque": getattr(car_doc, "steering_torque", None),
    "auto_resume": bool(auto_resume),
    "auto_resume_star": "full" if auto_resume else "empty",
    
    # Parts info
    "car_parts": car_parts,
    "harness": harness,
    "has_angled_mount": has_angled_mount,
    "detailed_parts": format_items_to_dicts(parts_list),
    "tools_required": format_items_to_dicts(tools_list),
    
    # CarParams attributes
    "mass": getattr(cp, "mass", None),
    "wheelbase": getattr(cp, "wheelbase", None),
    "steer_ratio": getattr(cp, "steerRatio", None),
    "center_to_front_ratio": center_to_front_ratio,
    "max_lateral_accel": max_lateral_accel,
    "network_location": to_json_type(getattr(cp, "networkLocation", None)),
    "radar_delay": getattr(cp, "radarDelay", None),
    "wheel_speed_factor": getattr(cp, "wheelSpeedFactor", None),
    "start_accel": getattr(cp, "startAccel", None),
    "steer_control_type": to_json_type(getattr(cp, "steerControlType", None)),
    "steer_actuator_delay": getattr(cp, "steerActuatorDelay", None),
    "steer_ratio_rear": getattr(cp, "steerRatioRear", None),
    "steer_limit_timer": getattr(cp, "steerLimitTimer", None),
    "tire_stiffness_factor": getattr(cp, "tireStiffnessFactor", None),
    "tire_stiffness_front": getattr(cp, "tireStiffnessFront", None),
    "tire_stiffness_rear": getattr(cp, "tireStiffnessRear", None),
    "rotational_inertia": getattr(cp, "rotationalInertia", None),
    "experimental_longitudinal_available": getattr(cp, "alphaLongitudinalAvailable", None),
    "openpilot_longitudinal_control": getattr(cp, "openpilotLongitudinalControl", None),
    "dashcam_only": getattr(cp, "dashcamOnly", None),
    "enable_dsu": getattr(cp, "enableDsu", None),
    "enable_bsm": getattr(cp, "enableBsm", None),
    "pcm_cruise": getattr(cp, "pcmCruise", None),
    "flags": getattr(cp, "flags", None),
    "auto_resume_sng": getattr(cp, "autoResumeSng", None),
    "radarUnavailable": getattr(cp, "radarUnavailable", None),
    "passive": getattr(cp, "passive", None),
    "stopping_decel_rate": getattr(cp, "stoppingDecelRate", None),
    "vEgo_stopping": getattr(cp, "vEgoStopping", None),
    "vEgo_starting": getattr(cp, "vEgoStarting", None),
    "stop_accel": getattr(cp, "stopAccel", None),
    "longitudinal_actuator_delay": getattr(cp, "longitudinalActuatorDelay", None),
  }    
  # Add platform config attributes
  if hasattr(platform, "config") and hasattr(platform.config, "specs"):
    specs = platform.config.specs
    metadata.update({
      "mass_curb_weight": getattr(specs, "mass", None),
      "center_to_front_ratio_base": getattr(specs, "centerToFrontRatio", None),
      "min_steer_speed_base": getattr(specs, "minSteerSpeed", None),
      "min_enable_speed_base": getattr(specs, "minEnableSpeed", None),
      "tire_stiffness_factor_base": getattr(specs, "tireStiffnessFactor", None),
    })

  # Add bus lookup if available
  if hasattr(platform, "config") and hasattr(platform.config, "dbc_dict"):
    metadata["bus_lookup"] = platform.config.dbc_dict
    
  # Handle row data (after setting defaults)
  if hasattr(car_doc, "row"):
    for key, value in car_doc.row.items():
      # Only process fields we want to include (skip auto_resume and setup_video)
      if key not in (Column.AUTO_RESUME, Column.SETUP_VIDEO):
        field_name = key.name.lower()
        metadata[field_name] = to_json_type(value)

  return metadata

def main():
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

  # Extract and sort metadata
  cars_data = []
  processed, errors = 0, 0
  for car_doc in all_cars:
    try:
      metadata = extract_metadata(car_doc)
      if metadata:
        cars_data.append(metadata)
        processed += 1
      else:
        errors += 1
    except Exception as e:
      logger.exception(f"Error processing {car_doc.name}: {e}")
      errors += 1

  # Sort by make and model
  cars_data.sort(key=lambda car: (car.get("make", ""), car.get("model", "")))
  
  # Save to file
  json_file = output_dir / "cars.json"
  with json_file.open("w") as f:
    json.dump(cars_data, f, indent=2)

  logger.info(f"Generated {processed} car entries in {json_file}")
  logger.info(f"Processed: {processed}, Errors: {errors}")

if __name__ == "__main__":
  main()
