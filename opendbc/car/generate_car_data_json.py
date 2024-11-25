import json
import os
from typing import Any
from enum import Enum

from opendbc.car.docs import get_car_docs_with_extras, get_all_footnotes, Column, CarDocs
from opendbc.car.docs_definitions import Star

def get_star_value(value: Star | str) -> Any:
    return value.value if isinstance(value, Star) else value

def convert_car_docs_to_json(car_docs: list[CarDocs], all_footnotes: dict[Enum, int]) -> list[dict[str, Any]]:
    car_data = []
    for car in car_docs:
        car_dict = {
            "name": car.name,
            "make": car.make,
            "model": car.model,
            "years": car.years,
            "year_list": car.year_list,
            "package": car.package,
            "requirements": car.requirements,
            "video_link": car.video_link,
            "footnotes": [str(all_footnotes[fn]) for fn in car.footnotes],
            "min_steer_speed": car.min_steer_speed,
            "min_enable_speed": car.min_enable_speed,
            "auto_resume": car.auto_resume,
            "car_parts": [part.value.name for part in car.car_parts.parts],
            "harness": car.car_parts.parts[0].name if car.car_parts.parts else None,
            "merged": car.merged,
            "support_type": car.support_type.value,
            "support_link": car.support_link,
            "detail_sentence": car.detail_sentence,
            "car_name": car.car_name,
            "car_fingerprint": car.car_fingerprint,
            "longitudinal": car.row[Column.LONGITUDINAL],
            "fsr_longitudinal": car.row[Column.FSR_LONGITUDINAL],
            "fsr_steering": car.row[Column.FSR_STEERING],
            "steering_torque": get_star_value(car.row[Column.STEERING_TORQUE]),
            "auto_resume_star": get_star_value(car.row[Column.AUTO_RESUME]),
            "hardware": car.row[Column.HARDWARE],
            "video": car.row[Column.VIDEO],
        }
        car_data.append(car_dict)
    return car_data

def generate_car_data_json(output_path: str) -> None:
    try:
        all_cars = get_car_docs_with_extras()
        all_footnotes = get_all_footnotes()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        car_data = convert_car_docs_to_json(all_cars, all_footnotes)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(car_data, f, indent=2)
    except Exception as e:
        raise RuntimeError(f"Failed to generate car documentation JSON: {str(e)}") from e

def main() -> None:
    output_path = os.path.join("car_data.json")
    generate_car_data_json(output_path)
    print(f"Car documentation JSON generated successfully: {output_path}")

if __name__ == "__main__":
    main()