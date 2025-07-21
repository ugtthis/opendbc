#!/usr/bin/env python3
import json
from typing import Any
from opendbc.car.docs import get_all_car_docs, get_params_for_docs
from opendbc.car.docs_definitions import CarDocs, Tool, BaseCarHarness
from opendbc.car.values import PLATFORMS

def get_attr(obj: Any, path: str, default: Any = None) -> Any:
  for attr in path.split("."):
    try:
      obj = getattr(obj, attr)
    except (AttributeError, KeyError):
      return default
  return obj


def convert_enum(value: Any) -> str | None:
  return getattr(value, "value", getattr(value, "name", str(value))) if value is not None else None


def extract_basic_info(car_doc: CarDocs) -> dict[str, Any]:
  footnotes = []
  try:
    if car_doc.footnotes:
      footnotes = [fn.value.text for fn in car_doc.footnotes]
  except (AttributeError, TypeError):
    pass

  min_steer_speed = car_doc.min_steer_speed
  if car_doc.name.lower() == "comma body" and isinstance(min_steer_speed, float) and min_steer_speed == float("-inf"):
    min_steer_speed = None

  return {
    "name": car_doc.name,
    "make": get_attr(car_doc, "make"),
    "model": get_attr(car_doc, "model"),
    "years": get_attr(car_doc, "years"),
    "year_list": get_attr(car_doc, "year_list", []),
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
    "detail_sentence": get_attr(car_doc, "detail_sentence"),
    "car_fingerprint": get_attr(car_doc, "car_fingerprint"),
    "brand": get_attr(car_doc, "brand"),
  }


def extract_parts_info(car_doc: CarDocs) -> dict[str, Any]:
  buy_link = f"https://comma.ai/shop/comma-3x?harness={car_doc.name.replace(' ', '%20')}"
  
  if not car_doc.car_parts or not car_doc.car_parts.parts:
    return {
      "car_parts": [], 
      "harness": None, 
      "has_angled_mount": False, 
      "detailed_parts": [], 
      "tools_required": [], 
      "hardware": "", 
      "buy_link": buy_link
    }

  all_parts = car_doc.car_parts.all_parts()
  parts_list = [p for p in all_parts if not isinstance(p, Tool)]
  tools_list = [p for p in all_parts if isinstance(p, Tool)]

  car_parts = [part_enum.value.name for part_enum in car_doc.car_parts.parts]
  harness_name = None
  for part_enum in car_doc.car_parts.parts:
    if isinstance(part_enum.value, BaseCarHarness):
      harness_name = part_enum.name.lower()
      break

  angled_mount_parts = ["angled_mount_8_degrees", "threex_angled_mount"]
  has_angled_mount = any(part.name in angled_mount_parts for part in all_parts)

  def format_items(items, include_type=False):
    item_counts = {}
    for item in items:
      item_counts[item] = item_counts.get(item, 0) + 1

    formatted = []
    for item in sorted(item_counts, key=lambda x: str(x.value.name)):
      item_dict = {"count": item_counts[item], "name": item.value.name, "enum_name": item.name}
      if include_type and hasattr(item, "part_type"):
        item_dict["type"] = item.part_type.name
      formatted.append(item_dict)
    return formatted

  parts_display = "\n".join([f"- {parts_list.count(part)} {part.value.name}" for part in sorted(set(parts_list), key=lambda p: str(p.value.name))])

  hardware = f"Parts:\n{parts_display}"

  if tools_list:
    tools_display = "\n".join([f"- {tools_list.count(tool)} {tool.value.name}" for tool in sorted(set(tools_list), key=lambda t: str(t.value.name))])
    hardware += f"\n\nTools:\n{tools_display}"

  return {
    "car_parts": car_parts,
    "harness": harness_name,
    "has_angled_mount": has_angled_mount,
    "detailed_parts": format_items(parts_list, True),
    "tools_required": format_items(tools_list),
    "hardware": hardware,
    "buy_link": buy_link,
  }


def extract_row_data(car_doc: CarDocs) -> dict[str, Any]:
  row_data = {}
  if hasattr(car_doc, "row"):
    for col_enum, col_value in car_doc.row.items():
      key = col_enum.name.lower()
      value = col_value.value if hasattr(col_value, "value") else col_value
      row_data[key] = value

  return {
    "longitudinal": row_data.get("longitudinal"),
    "fsr_longitudinal": row_data.get("fsr_longitudinal", "0 mph"),
    "fsr_steering": row_data.get("fsr_steering", "0 mph"),
    "steering_torque": row_data.get("steering_torque"),
    "auto_resume_star": row_data.get("auto_resume"),
    "video_row": row_data.get("video", ""),
  }


def extract_vehicle_configs(CP: Any, platform: Any) -> dict[str, Any]:
  # Calculate center to front ratio
  center_to_front_ratio = 0.5
  if CP and hasattr(CP, "centerToFront") and hasattr(CP, "wheelbase") and CP.wheelbase > 0:
    try:
      center_to_front_ratio = CP.centerToFront / CP.wheelbase
    except (AttributeError, ZeroDivisionError):
      pass

  # Handle special case for max lateral accel
  max_lateral_accel = get_attr(CP, "maxLateralAccel")
  if isinstance(max_lateral_accel, float) and max_lateral_accel in [float("inf"), float("-inf")]:
    max_lateral_accel = None

  return {
    # Basic specs
    "mass": get_attr(CP, "mass"),
    "mass_curb_weight": get_attr(platform, "config.specs.mass"),
    "wheelbase": get_attr(CP, "wheelbase"),
    "steer_ratio": get_attr(CP, "steerRatio"),
    "center_to_front_ratio": center_to_front_ratio,
    "center_to_front_ratio_base": get_attr(platform, "config.specs.centerToFrontRatio"),
    "max_lateral_accel": max_lateral_accel,
    # Network and bus config
    "network_location": convert_enum(get_attr(CP, "networkLocation")),
    "bus_lookup": get_attr(platform, "config.dbc_dict"),
    "radar_delay": get_attr(CP, "radarDelay"),
    "wheel_speed_factor": get_attr(CP, "wheelSpeedFactor"),
    # Speed settings
    "start_accel": get_attr(CP, "startAccel"),
    "min_steer_speed_base": get_attr(platform, "config.specs.minSteerSpeed"),
    "min_enable_speed": get_attr(CP, "minEnableSpeed"),
    "min_enable_speed_base": get_attr(platform, "config.specs.minEnableSpeed"),
    # Steering configuration
    "steer_control_type": convert_enum(get_attr(CP, "steerControlType")),
    "steer_actuator_delay": get_attr(CP, "steerActuatorDelay"),
    "steer_ratio_rear": get_attr(CP, "steerRatioRear"),
    "steer_limit_timer": get_attr(CP, "steerLimitTimer"),
    # Tire and inertia config
    "tire_stiffness_factor": get_attr(CP, "tireStiffnessFactor"),
    "tire_stiffness_factor_base": get_attr(platform, "config.specs.tireStiffnessFactor"),
    "tire_stiffness_front": get_attr(CP, "tireStiffnessFront"),
    "tire_stiffness_rear": get_attr(CP, "tireStiffnessRear"),
    "rotational_inertia": get_attr(CP, "rotationalInertia"),
    # Features and capabilities  
    "experimental_longitudinal_available": get_attr(CP, "alphaLongitudinalAvailable"),
    "openpilot_longitudinal_control": get_attr(CP, "openpilotLongitudinalControl"),
    "dashcam_only": get_attr(CP, "dashcamOnly"),
    "enable_dsu": get_attr(CP, "enableDsu"),
    "enable_bsm": get_attr(CP, "enableBsm"),
    "pcm_cruise": get_attr(CP, "pcmCruise"),
    "flags": get_attr(CP, "flags"),
    "auto_resume_sng": get_attr(CP, "autoResumeSng"),
    "radarUnavailable": get_attr(CP, "radarUnavailable"),
    "passive": get_attr(CP, "passive"),
    # Longitudinal config
    "stopping_decel_rate": get_attr(CP, "stoppingDecelRate"),
    "vEgo_stopping": get_attr(CP, "vEgoStopping"),
    "vEgo_starting": get_attr(CP, "vEgoStarting"),
    "stop_accel": get_attr(CP, "stopAccel"),
    "longitudinal_actuator_delay": get_attr(CP, "longitudinalActuatorDelay"),
  }


def extract_car_data(car_doc: CarDocs) -> dict[str, Any] | None:
  try:
    platform = PLATFORMS.get(car_doc.car_fingerprint)
    if not platform:
      return None
    CP = get_params_for_docs(platform)

    # Combine all data extraction
    return {**extract_basic_info(car_doc), **extract_parts_info(car_doc), **extract_row_data(car_doc), **extract_vehicle_configs(CP, platform)}
  except Exception as e:
    print(f"Error processing {car_doc.name}: {e}")
    return None


def main() -> None:
  # Get all supported cars (exclude community/incompatible)
  excluded_types = ["Not compatible", "Community"]
  all_cars: list[CarDocs] = [
    car_doc for car_doc in get_all_car_docs()
    if getattr(car_doc, "support_type", None) and car_doc.support_type.value not in excluded_types
  ]

  print(f"Processing {len(all_cars)} supported cars...")

  # Extract data for all cars
  cars_data: list[dict[str, Any] | None] = [extract_car_data(car_doc) for car_doc in all_cars]
  cars_data: list[dict[str, Any]] = [car_data for car_data in cars_data if car_data is not None]

  # Sort by make then model
  cars_data.sort(key=lambda car_data: (car_data.get("make") or "", car_data.get("model") or ""))

  output_file = "simplified_metadata.json"
  with open(output_file, "w") as f:
    json.dump(cars_data, f, indent=2, ensure_ascii=False)

  print(f"Generated {len(cars_data)} cars in {output_file}")


if __name__ == "__main__":
  main()
