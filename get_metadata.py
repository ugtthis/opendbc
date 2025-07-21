#!/usr/bin/env python3
import json
from typing import Any
from opendbc.car.docs import get_all_car_docs, get_params_for_docs
from opendbc.car.docs_definitions import CarDocs, Tool, BaseCarHarness
from opendbc.car.values import PLATFORMS


def extract_car_data(car_doc: CarDocs) -> dict[str, Any] | None:
  try:
    platform = PLATFORMS.get(car_doc.car_fingerprint)
    if not platform:
      return None

    CP = get_params_for_docs(platform)

    # Handle special case from comma body
    min_steer_speed = None if car_doc.min_steer_speed == float("-inf") else car_doc.min_steer_speed
    max_lateral_accel = None if getattr(CP, "maxLateralAccel", None) == float("inf") else getattr(CP, "maxLateralAccel", None)

    # Build data dictionary
    data = {
      # Basic info
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

      # CarParams
      "mass": CP.mass,
      "wheelbase": CP.wheelbase,
      "steer_ratio": CP.steerRatio,
      "radar_delay": CP.radarDelay,
      "wheel_speed_factor": CP.wheelSpeedFactor,
      "start_accel": CP.startAccel,
      "steer_actuator_delay": CP.steerActuatorDelay,
      "steer_ratio_rear": CP.steerRatioRear,
      "steer_limit_timer": CP.steerLimitTimer,
      "tire_stiffness_factor": CP.tireStiffnessFactor,
      "tire_stiffness_front": CP.tireStiffnessFront,
      "tire_stiffness_rear": CP.tireStiffnessRear,
      "rotational_inertia": CP.rotationalInertia,
      "experimental_longitudinal_available": CP.alphaLongitudinalAvailable,
      "openpilot_longitudinal_control": CP.openpilotLongitudinalControl,
      "dashcam_only": CP.dashcamOnly,
      "enable_dsu": CP.enableDsu,
      "enable_bsm": CP.enableBsm,
      "pcm_cruise": CP.pcmCruise,
      "flags": CP.flags,
      "auto_resume_sng": CP.autoResumeSng,
      "radarUnavailable": CP.radarUnavailable,
      "passive": CP.passive,
      "stopping_decel_rate": CP.stoppingDecelRate,
      "vEgo_stopping": CP.vEgoStopping,
      "vEgo_starting": CP.vEgoStarting,
      "stop_accel": CP.stopAccel,
      "longitudinal_actuator_delay": CP.longitudinalActuatorDelay,

      # Platform Config
      "mass_curb_weight": platform.config.specs.mass,
      "center_to_front_ratio_base": platform.config.specs.centerToFrontRatio,
      "bus_lookup": platform.config.dbc_dict,
      "min_steer_speed_base": platform.config.specs.minSteerSpeed,
      "min_enable_speed_base": platform.config.specs.minEnableSpeed,
      "tire_stiffness_factor_base": platform.config.specs.tireStiffnessFactor,

      # Derived
      "center_to_front_ratio": platform.config.specs.centerToFrontRatio,
      "max_lateral_accel": max_lateral_accel,
      "network_location": str(getattr(CP, "networkLocation", None)),
      "steer_control_type": str(getattr(CP, "steerControlType", None)),
      "buy_link": f"https://comma.ai/shop/comma-3x?harness={car_doc.name.replace(' ', '%20')}",
    }

    # Parts info
    if not car_doc.car_parts or not car_doc.car_parts.parts:
      data.update({
        "car_parts": [],
        "harness": None,
        "has_angled_mount": False,
        "detailed_parts": [],
        "tools_required": [],
        "hardware": "",
      })
    else:
      all_parts = car_doc.car_parts.all_parts()
      parts = [p for p in all_parts if not isinstance(p, Tool)]
      tools = [p for p in all_parts if isinstance(p, Tool)]

      # Build formatted data using unique items
      unique_parts = sorted(set(parts), key=lambda p: str(p.value.name))
      unique_tools = sorted(set(tools), key=lambda t: str(t.value.name))

      detailed_parts = [{"count": parts.count(p), "name": p.value.name, "enum_name": p.name,
                        "type": p.part_type.name if hasattr(p, "part_type") else None}
                       for p in unique_parts]

      tools_required = [{"count": tools.count(t), "name": t.value.name, "enum_name": t.name}
                       for t in unique_tools]

      # Hardware display string
      parts_str = "\n".join([f"- {parts.count(p)} {p.value.name}" for p in unique_parts])
      tools_str = "\n".join([f"- {tools.count(t)} {t.value.name}" for t in unique_tools])
      hardware = f"Parts:\n{parts_str}" + (f"\n\nTools:\n{tools_str}" if tools else "")

      data.update({
        "car_parts": [p.value.name for p in car_doc.car_parts.parts],
        "harness": next((p.name.lower() for p in car_doc.car_parts.parts if isinstance(p.value, BaseCarHarness)), None),
        "has_angled_mount": any(p.name in ["angled_mount_8_degrees", "threex_angled_mount"] for p in all_parts),
        "detailed_parts": detailed_parts,
        "tools_required": tools_required,
        "hardware": hardware,
      })

    # Row data
    if hasattr(car_doc, "row"):
      row_data = {col.name.lower(): (col_val.value if hasattr(col_val, "value") else col_val)
                  for col, col_val in car_doc.row.items()}
      data.update({
        "longitudinal": row_data.get("longitudinal"),
        "fsr_longitudinal": row_data.get("fsr_longitudinal", "0 mph"),
        "fsr_steering": row_data.get("fsr_steering", "0 mph"),
        "steering_torque": row_data.get("steering_torque"),
        "auto_resume_star": row_data.get("auto_resume"),
      })

    return data
  except Exception as e:
    print(f"Error processing {car_doc.name}: {e}")
    return None


def main() -> None:
  excluded_types = ["Not compatible", "Community"]
  all_cars = [car_doc for car_doc in get_all_car_docs()
              if getattr(car_doc, "support_type", None) and car_doc.support_type.value not in excluded_types]
  print(f"Processing {len(all_cars)} supported cars...")

  cars_data = [data for car_doc in all_cars if (data := extract_car_data(car_doc)) is not None]
  cars_data.sort(key=lambda car: (car.get("make") or "", car.get("model") or ""))

  with open("simplified_metadata.json", "w") as f:
    json.dump(cars_data, f, indent=2, ensure_ascii=False)

  print(f"Generated {len(cars_data)} cars in simplified_metadata.json")


if __name__ == "__main__":
  main()