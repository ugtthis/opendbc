"""
Script to generate model data for attributes.py.

This script extracts model data from values.py and generates the corresponding
entries for attributes.py.
"""

import re
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from opendbc.car.hyundai.values import CAR, HyundaiCanFDPlatformConfig, HyundaiFlags
from opendbc.car.docs_definitions import CarDocs, CarHarness
from opendbc.metadata.base.parts_definitions import Harness, Tool, Kit

@dataclass
class CarModel:
    """Represents a car model with its metadata."""
    name: str
    years: List[int]
    package: str
    harness: str
    platform: str
    video_link: str = None
    make: str = None

def extract_models_from_values() -> Dict[str, List[CarModel]]:
    """Extract all car models from values.py."""
    models: Dict[str, List[CarModel]] = {}
    
    for platform in CAR:
        if not hasattr(platform.config, 'car_docs'):
            continue
            
        car_docs: List[CarDocs] = platform.config.car_docs
        for doc in car_docs:
            # Extract years from name using regex
            year_pattern = r'(\d{4})(?:-(\d{2,4}))?'
            name_without_years = re.sub(year_pattern, '', doc.name).strip()
            years = []
            match = re.search(year_pattern, doc.name)
            if match:
                start_year = int(match.group(1))
                end_year = int(match.group(2)) if match.group(2) else start_year
                if len(str(end_year)) == 2:
                    end_year = int(str(start_year)[:2] + str(end_year))
                years = list(range(start_year, end_year + 1))
            
            # Extract harness from car_parts
            harnesses = []
            if doc.car_parts and doc.car_parts.parts:
                for part in doc.car_parts.parts:
                    if isinstance(part, CarHarness):
                        # Extract the harness letter from the enum name and make it uppercase
                        harness_letter = part.name.split("_")[-1].upper()
                        harnesses.append(harness_letter)
            
            # If multiple harnesses are found, use both
            harness = ' and '.join(harnesses) if harnesses else None
            
            make = name_without_years.split()[0]
            model = CarModel(
                name=name_without_years,
                years=years,
                package=doc.package,
                harness=harness,
                platform=str(platform),
                video_link=doc.video_link,
                make=make
            )
            
            if make not in models:
                models[make] = []
            models[make].append(model)
    
    return models

def generate_model_data() -> Dict[str, Dict[str, Any]]:
    """Generate model data for attributes.py."""
    models = extract_models_from_values()
    model_data = {}
    
    # Process models in the order they appear in values.py: Hyundai, Kia, Genesis
    make_order = ["Hyundai", "Kia", "Genesis"]
    
    for make in make_order:
        if make not in models:
            continue
            
        make_models = models[make]
        for model in make_models:
            # Create the model ID (e.g., "Hyundai Elantra 2021-23")
            if len(model.years) > 1:
                model_id = f"{model.name} {model.years[0]}-{str(model.years[-1])[2:]}"
            else:
                model_id = f"{model.name} {model.years[0]}"
            
            # Initialize model data with all required fields
            model_data[model_id] = {
                "make": make,
                "model": model.name.split(" ", 1)[1],  # Remove make from model name
                "years": model.years,
                "platform": model.platform,
                "package": model.package,
                "explicit_parts": [],  # Initialize empty list for parts
                "explicit_footnotes": [],  # Initialize empty list for footnotes
                "support_type": "upstream",
                "video_link": f'"{model.video_link}"' if model.video_link else None,
                "min_steer_speed": 0.0,  # Will be updated if MIN_STEER_32_MPH flag is present
                "min_enable_speed": 0.0,
                "auto_resume": True,
                "visible_in_docs": True
            }
            
            # Add parts from car_parts first
            if model.harness:
                # Handle multiple harnesses (e.g., "A and K")
                for harness_letter in model.harness.split(" and "):
                    model_data[model_id]["explicit_parts"].append(f"Harness.HYUNDAI_{harness_letter}")
            
            # Add CAN FD kit for CAN FD platforms
            if hasattr(CAR, model.platform):
                car_config = getattr(CAR, model.platform)
                if hasattr(car_config.config, 'flags') and car_config.config.flags & HyundaiFlags.CANFD:
                    model_data[model_id]["explicit_parts"].append("Kit.CANFD_KIT")
            
            # Add footnotes
            # Add SCC footnote for platforms with SCC
            if "Smart Cruise Control" in model.package or "Highway Driving Assist" in model.package:
                model_data[model_id]["explicit_footnotes"].append("scc")
            
            # Add radar SCC footnote for platforms with radar SCC
            if hasattr(CAR, model.platform):
                car_config = getattr(CAR, model.platform)
                if hasattr(car_config.config, 'flags') and car_config.config.flags & HyundaiFlags.RADAR_SCC:
                    model_data[model_id]["explicit_footnotes"].append("radar_scc")
            
            # Add min speed footnote for platforms with min speed requirement
            # Check if the platform has the MIN_STEER_32_MPH flag set
            if hasattr(CAR, model.platform):
                car_config = getattr(CAR, model.platform)
                if hasattr(car_config.config, 'flags') and car_config.config.flags & HyundaiFlags.MIN_STEER_32_MPH:
                    model_data[model_id]["explicit_footnotes"].append("min_speed")
                    model_data[model_id]["min_steer_speed"] = 32 * 0.44704  # 32 mph in m/s
    
    return model_data

def generate_attributes_file():
    """Generate the complete attributes.py file."""
    model_data = generate_model_data()
    
    # Sort models by the order they appear in values.py
    def sort_key(item):
        make = item[1]["make"]
        model = item[1]["model"]
        make_order = {"Hyundai": 0, "Kia": 1, "Genesis": 2}
        return (make_order[make], model)
    
    sorted_models = sorted(model_data.items(), key=sort_key)
    
    # Generate file content
    content = [
        '"""',
        "Static metadata attributes for Hyundai vehicles.",
        "",
        "This module contains all the non-functional metadata for Hyundai vehicles,",
        "including model information, parts, and other documentation-related information.",
        "Footnotes have been moved to footnotes.py and helper functions to base/model_helpers.py.",
        '"""',
        "",
        "from typing import Dict, Any",
        "from opendbc.metadata.base.parts_definitions import Harness, Tool, Kit",
        "",
        "# ===== MODEL DATA =====",
        "",
        "MODEL_DATA = {",
    ]
    
    # Add each model entry
    for model_id, data in sorted_models:
        content.append(f'    "{model_id}": {{')
        content.append(f'        "make": "{data["make"]}",')
        content.append(f'        "model": "{data["model"]}",')
        content.append(f'        "years": {data["years"]},')
        content.append(f'        "platform": "{data["platform"]}",')
        content.append(f'        "package": "{data["package"]}",')
        content.append(f'        "explicit_parts": [{", ".join(data["explicit_parts"])}],')
        content.append(f'        "explicit_footnotes": {data["explicit_footnotes"]},')
        content.append(f'        "support_type": "{data["support_type"]}",')
        content.append(f'        "video_link": {data["video_link"]},')
        content.append(f'        "min_steer_speed": {data["min_steer_speed"]},')
        content.append(f'        "min_enable_speed": {data["min_enable_speed"]},')
        content.append(f'        "auto_resume": {data["auto_resume"]},')
        content.append(f'        "visible_in_docs": {data["visible_in_docs"]}')
        content.append('    },')
    
    content.append("}")
    
    # Write to file
    # Update the file path to use the parent directory
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "attributes.py")
    with open(file_path, "w") as f:
        f.write("\n".join(content))

if __name__ == "__main__":
    generate_attributes_file() 