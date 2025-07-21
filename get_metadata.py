#!/usr/bin/env python3
import json
from typing import Any
from opendbc.car.docs import get_all_car_docs, get_params_for_docs
from opendbc.car.docs_definitions import CarDocs, Tool, BaseCarHarness
from opendbc.car.values import PLATFORMS

def _convert_enum(value: Any) -> str | None:
  return getattr(value, "value", getattr(value, "name", str(value))) if value is not None else None


def _format_part_list(parts: list[Any], include_type: bool = False) -> list[dict[str, Any]]:
  from collections import Counter
  counts = Counter(parts)
  formatted = []
  for item, count in sorted(counts.items(), key=lambda x: str(x[0].value.name)):
    item_dict = {"count": count, "name": item.value.name, "enum_name": item.name}
    if include_type and hasattr(item, "part_type"):
      item_dict["type"] = item.part_type.name
    formatted.append(item_dict)
  return formatted


def _extract_basic_info(car_doc: CarDocs) -> dict[str, Any]:
  """Extracts basic, top-level information from the CarDocs object."""
  min_steer_speed = car_doc.min_steer_speed
  if car_doc.name.lower() == "comma body" and isinstance(min_steer_speed, float) and min_steer_speed == float("-inf"):
    min_steer_speed = None

  return {
    "name": car_doc.name,
    "make": getattr(car_doc, "make", None),
    "model": getattr(car_doc, "model", None),
    "years": getattr(car_doc, "years", None),
    "year_list": getattr(car_doc, "year_list", []),
    "package": car_doc.package,
    "video": car_doc.video,
    "setup_video": car_doc.setup_video,
    "footnotes": [fn.value.text for fn in car_doc.footnotes] if car_doc.footnotes else [],
    "min_steer_speed": min_steer_speed,
    "min_enable_speed": car_doc.min_enable_speed,
    "auto_resume": car_doc.auto_resume,
    "merged": car_doc.merged,
    "support_type": car_doc.support_type.value if car_doc.support_type else None,
    "support_link": car_doc.support_link,
    "detail_sentence": getattr(car_doc, "detail_sentence", None),
    "car_fingerprint": getattr(car_doc, "car_fingerprint", None),
    "brand": getattr(car_doc, "brand", None),
  }


def _extract_parts_info(car_doc: CarDocs) -> dict[str, Any]:
  """Extracts and formats hardware parts and tools information."""
  buy_link = f"https://comma.ai/shop/comma-3x?harness={car_doc.name.replace(' ', '%20')}"
  if not car_doc.car_parts or not car_doc.car_parts.parts:
    return {
      "car_parts": [], "harness": None, "has_angled_mount": False,
      "detailed_parts": [], "tools_required": [], "hardware": "", "buy_link": buy_link,
    }

  all_parts = car_doc.car_parts.all_parts()
  parts_list = [p for p in all_parts if not isinstance(p, Tool)]
  tools_list = [p for p in all_parts if isinstance(p, Tool)]
  harness_name = next((p.name.lower() for p in car_doc.car_parts.parts if isinstance(p.value, BaseCarHarness)), None)

  parts_display = "\n".join([f"- {parts_list.count(part)} {part.value.name}" for part in sorted(set(parts_list), key=lambda p: str(p.value.name))])
  hardware = f"Parts:\n{parts_display}"
  if tools_list:
    tools_display = "\n".join([f"- {tools_list.count(tool)} {tool.value.name}" for tool in sorted(set(tools_list), key=lambda t: str(t.value.name))])
    hardware += f"\n\nTools:\n{tools_display}"

  return {
    "car_parts": [p.value.name for p in car_doc.car_parts.parts],
    "harness": harness_name,
    "has_angled_mount": any(p.name in ["angled_mount_8_degrees", "threex_angled_mount"] for p in all_parts),
    "detailed_parts": _format_part_list(parts_list, True),
    "tools_required": _format_part_list(tools_list),
    "hardware": hardware,
    "buy_link": buy_link,
  }


def _extract_row_data(car_doc: CarDocs) -> dict[str, Any]:
  """Extracts data from the spreadsheet-style row attribute."""
  if not hasattr(car_doc, "row"):
    return {}

  row_data = {col.name.lower(): (col_val.value if hasattr(col_val, "value") else col_val) for col, col_val in car_doc.row.items()}
  return {
    "longitudinal": row_data.get("longitudinal"),
    "fsr_longitudinal": row_data.get("fsr_longitudinal", "0 mph"),
    "fsr_steering": row_data.get("fsr_steering", "0 mph"),
    "steering_torque": row_data.get("steering_torque"),
    "auto_resume_star": row_data.get("auto_resume"),
    "video_row": row_data.get("video", ""),
  }


def _extract_vehicle_configs(CP: Any, platform: Any) -> dict[str, Any]:
  """Extracts technical vehicle parameters from CarParams and platform configs."""
  center_to_front = 0.
  if hasattr(CP, 'centerToFront') and hasattr(CP, 'wheelbase') and CP.wheelbase > 0:
    center_to_front = CP.centerToFront / CP.wheelbase

  max_lateral_accel = getattr(CP, "maxLateralAccel", None)
  if isinstance(max_lateral_accel, float) and max_lateral_accel in [float("inf"), float("-inf")]:
    max_lateral_accel = None

  return {
    # CarParams
    "mass": CP.mass, "wheelbase": CP.wheelbase, "steer_ratio": CP.steerRatio,
    "radar_delay": CP.radarDelay, "wheel_speed_factor": CP.wheelSpeedFactor,
    "start_accel": CP.startAccel, "min_enable_speed": CP.minEnableSpeed,
    "steer_actuator_delay": CP.steerActuatorDelay, "steer_ratio_rear": CP.steerRatioRear,
    "steer_limit_timer": CP.steerLimitTimer, "tire_stiffness_factor": CP.tireStiffnessFactor,
    "tire_stiffness_front": CP.tireStiffnessFront, "tire_stiffness_rear": CP.tireStiffnessRear,
    "rotational_inertia": CP.rotationalInertia, "experimental_longitudinal_available": CP.alphaLongitudinalAvailable,
    "openpilot_longitudinal_control": CP.openpilotLongitudinalControl, "dashcam_only": CP.dashcamOnly,
    "enable_dsu": CP.enableDsu, "enable_bsm": CP.enableBsm, "pcm_cruise": CP.pcmCruise,
    "flags": CP.flags, "auto_resume_sng": CP.autoResumeSng, "radarUnavailable": CP.radarUnavailable,
    "passive": CP.passive, "stopping_decel_rate": CP.stoppingDecelRate, "vEgo_stopping": CP.vEgoStopping,
    "vEgo_starting": CP.vEgoStarting, "stop_accel": CP.stopAccel, "longitudinal_actuator_delay": CP.longitudinalActuatorDelay,

    # Platform Config
    "mass_curb_weight": platform.config.specs.mass,
    "center_to_front_ratio_base": platform.config.specs.centerToFrontRatio,
    "bus_lookup": platform.config.dbc_dict,
    "min_steer_speed_base": platform.config.specs.minSteerSpeed,
    "min_enable_speed_base": platform.config.specs.minEnableSpeed,
    "tire_stiffness_factor_base": platform.config.specs.tireStiffnessFactor,

    # Other
    "center_to_front_ratio": center_to_front,
    "max_lateral_accel": max_lateral_accel,
    "network_location": _convert_enum(getattr(CP, "networkLocation", None)),
    "steer_control_type": _convert_enum(getattr(CP, "steerControlType", None)),
  }


def extract_car_data(car_doc: CarDocs) -> dict[str, Any] | None:
  try:
    platform = PLATFORMS.get(car_doc.car_fingerprint)
    if not platform:
      return None
    CP = get_params_for_docs(platform)

    data = {}
    data.update(_extract_basic_info(car_doc))
    data.update(_extract_parts_info(car_doc))
    data.update(_extract_row_data(car_doc))
    data.update(_extract_vehicle_configs(CP, platform))
    return data

  except AttributeError as e:
    raise RuntimeError(f"Error processing {car_doc.name}: {e}")
  except Exception as e:
    print(f"Error processing {car_doc.name}: {e}")
    return None


def main() -> None:
  excluded_types = ["Not compatible", "Community"]
  all_cars: list[CarDocs] = [
    car_doc for car_doc in get_all_car_docs()
    if getattr(car_doc, "support_type", None) and car_doc.support_type.value not in excluded_types
  ]
  print(f"Processing {len(all_cars)} supported cars...")

  cars_data = [data for car_doc in all_cars if (data := extract_car_data(car_doc)) is not None]
  cars_data.sort(key=lambda car: (car.get("make") or "", car.get("model") or ""))

  output_file = "simplified_metadata.json"
  with open(output_file, "w") as f:
    json.dump(cars_data, f, indent=2, ensure_ascii=False)

  print(f"Generated {len(cars_data)} cars in {output_file}")


if __name__ == "__main__":
  main()