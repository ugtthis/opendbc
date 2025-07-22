#!/usr/bin/env python3
import json
from typing import Any
from opendbc.car.docs import get_all_car_docs, get_params_for_docs
from opendbc.car.docs_definitions import CarDocs, Tool, BaseCarHarness, Column
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
      "brand": getattr(car_doc, "brand", None), # The parent company

      # Capability info
      "longitudinal": car_doc.row.get(Column.LONGITUDINAL),
      "fsr_longitudinal": car_doc.row.get(Column.FSR_LONGITUDINAL, "0 mph"),
      "fsr_steering": car_doc.row.get(Column.FSR_STEERING, "0 mph"),
      "steering_torque": car_doc.row[Column.STEERING_TORQUE].value,
      "auto_resume_star": "full" if car_doc.auto_resume else "empty",

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
    all_parts = car_doc.car_parts.all_parts() if car_doc.car_parts and car_doc.car_parts.parts else []
    parts = [p for p in all_parts if not isinstance(p, Tool)]
    tools = [p for p in all_parts if isinstance(p, Tool)]
    
    data.update({
      "has_angled_mount": any(p.name in ["angled_mount_8_degrees", "threex_angled_mount"] for p in all_parts),
      "harness": next((p.name for p in all_parts if isinstance(p.value, BaseCarHarness)), None),
      "tools_required": [{"name": t.value.name, "count": tools.count(t)} for t in dict.fromkeys(tools)],
      "parts": [{"name": p.value.name, "type": p.part_type.name, "count": parts.count(p)} for p in dict.fromkeys(parts)],
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

  with open("metadata.json", "w") as f:
    json.dump(cars_data, f, indent=2, ensure_ascii=False)

  print(f"Generated {len(cars_data)} cars in metadata.json")


if __name__ == "__main__":
  main()