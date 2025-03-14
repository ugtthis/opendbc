"""
Script to extract car models from values.py and compare with attributes.py.

This script helps ensure that all models in values.py are properly represented
in attributes.py with the correct metadata.
"""

import re
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass
from opendbc.car.hyundai.values import CAR
from opendbc.car.docs_definitions import CarDocs

@dataclass
class CarModel:
    """Represents a car model with its metadata."""
    name: str
    years: List[int]
    package: str
    harness: str
    platform: str

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
            harness = None
            if doc.car_parts and doc.car_parts.parts:
                for part in doc.car_parts.parts:
                    if part.name.startswith('Hyundai'):
                        harness = part.name
                        break
            
            model = CarModel(
                name=name_without_years,
                years=years,
                package=doc.package,
                harness=harness,
                platform=str(platform)
            )
            
            make = name_without_years.split()[0]
            if make not in models:
                models[make] = []
            models[make].append(model)
    
    return models

def extract_models_from_attributes() -> Dict[str, Dict[str, Any]]:
    """Extract all car models from attributes.py."""
    # Updated import path to access attributes.py from the scripts directory
    from opendbc.metadata.brand_metadata.hyundai.attributes import MODEL_DATA
    return MODEL_DATA

def compare_models():
    """Compare models between values.py and attributes.py."""
    values_models = extract_models_from_values()
    attributes_models = extract_models_from_attributes()
    
    # Check for missing models in attributes.py
    missing_models = []
    mismatched_models = []
    
    for make, models in values_models.items():
        for model in models:
            # Create the expected model ID format (e.g., "Hyundai Elantra 2021-23")
            if len(model.years) > 1:
                model_id = f"{model.name} {model.years[0]}-{str(model.years[-1])[2:]}"
            else:
                model_id = f"{model.name} {model.years[0]}"
            
            if model_id not in attributes_models:
                missing_models.append((model_id, model))
            else:
                # Check for mismatches in metadata
                attr_model = attributes_models[model_id]
                mismatches = []
                
                # Check years
                if attr_model['years'] != model.years:
                    mismatches.append(f"years: expected {model.years}, got {attr_model['years']}")
                
                # Check package
                if attr_model['package'] != model.package:
                    mismatches.append(f"package: expected {model.package}, got {attr_model['package']}")
                
                # Check platform
                if attr_model['platform'] != model.platform:
                    mismatches.append(f"platform: expected {model.platform}, got {attr_model['platform']}")
                
                if mismatches:
                    mismatched_models.append((model_id, mismatches))
    
    # Print results
    print("\n=== Model Comparison Results ===\n")
    
    if missing_models:
        print("Missing models in attributes.py:")
        for model_id, model in missing_models:
            print(f"\n{model_id}:")
            print(f"  years: {model.years}")
            print(f"  package: {model.package}")
            print(f"  harness: {model.harness}")
            print(f"  platform: {model.platform}")
    else:
        print("No missing models in attributes.py")
    
    if mismatched_models:
        print("\nMismatched metadata:")
        for model_id, mismatches in mismatched_models:
            print(f"\n{model_id}:")
            for mismatch in mismatches:
                print(f"  - {mismatch}")
    else:
        print("\nNo metadata mismatches found")

if __name__ == "__main__":
    compare_models() 