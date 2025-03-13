"""Tests for consistency between values.py and attributes.py across all brands."""

import os
import importlib
import pytest
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from opendbc.car.docs_definitions import CarDocs

@dataclass
class CarModel:
    """Represents a car model with its metadata."""
    name: str
    years: List[int]
    package: str
    platform: str

def find_similar_models(needle: str, haystack: Set[str]) -> List[str]:
    """Find models in haystack that are similar to needle (ignoring years)."""
    needle_base = ' '.join(needle.split()[:-1])  # Remove year part
    return [model for model in haystack if ' '.join(model.split()[:-1]) == needle_base]

def format_model_differences(missing_models: Set[str], model_data_keys: Set[str]) -> str:
    """Format differences between values.py and attributes.py models with suggestions."""
    if not missing_models:
        return ""
    
    lines = ["Models found in values.py but missing from attributes.py:"]
    for model in sorted(missing_models):
        lines.append(f"  - {model}")
        
        # Find similar models that might be the same car with different years
        similar = find_similar_models(model, model_data_keys)
        if similar:
            lines.append("    Similar models found in attributes.py (possible year mismatch):")
            for similar_model in sorted(similar):
                lines.append(f"      * {similar_model}")
            lines.append("    Suggestion: Check if the years need to be updated in attributes.py")
        else:
            lines.append("    No similar models found - this model may need to be added to attributes.py")
    
    return "\n".join(lines)

def extract_models_from_values(brand: str) -> Dict[str, CarModel]:
    """Extract all car models from values.py for a specific brand."""
    try:
        # Import the brand's values module
        values_module = importlib.import_module(f"opendbc.car.{brand.lower()}.values")
        CAR = getattr(values_module, "CAR")
    except ImportError:
        pytest.skip(f"No values.py found for brand {brand}")
    except AttributeError:
        pytest.skip(f"No CAR enum found in values.py for brand {brand}")
    
    models = {}
    
    for platform in CAR:
        if not hasattr(platform.config, 'car_docs'):
            continue
            
        car_docs: List[CarDocs] = platform.config.car_docs
        for doc in car_docs:
            # Extract years from name
            years = []
            name_parts = doc.name.split()
            if not name_parts:
                continue
                
            year_str = name_parts[-1]
            if '-' in year_str:
                try:
                    year_parts = year_str.split('-')
                    if len(year_parts) != 2:
                        continue
                        
                    start_year = int(year_parts[0])
                    end_str = year_parts[1]
                    
                    # Handle both 4-digit and 2-digit end years
                    if len(end_str) == 4:
                        end_year = int(end_str)
                    elif len(end_str) == 2:
                        end_year = int(f"20{end_str}")
                    else:
                        continue
                        
                    years = list(range(start_year, end_year + 1))
                except (ValueError, IndexError):
                    continue
            else:
                try:
                    years = [int(year_str)]
                except ValueError:
                    continue
            
            if not years:
                continue
                
            # Create model ID in the same format as attributes.py
            name_without_years = ' '.join(name_parts[:-1])
            if len(years) > 1:
                model_id = f"{name_without_years} {years[0]}-{str(years[-1])[2:]}"
            else:
                model_id = f"{name_without_years} {years[0]}"
            
            models[model_id] = CarModel(
                name=name_without_years,
                years=years,
                package=doc.package,
                platform=str(platform)
            )
    
    return models

def get_model_data(brand: str) -> Optional[Dict[str, Dict]]:
    """Get MODEL_DATA from attributes.py for a specific brand."""
    try:
        # Import the brand's attributes module
        attributes_module = importlib.import_module(f"opendbc.metadata.brand_metadata.{brand.lower()}.attributes")
        return getattr(attributes_module, "MODEL_DATA")
    except ImportError:
        pytest.skip(f"No attributes.py found for brand {brand}")
    except AttributeError:
        pytest.skip(f"No MODEL_DATA found in attributes.py for brand {brand}")

def check_model_consistency_for_brand(brand: str):
    """Check model consistency for a specific brand."""
    values_models = extract_models_from_values(brand)
    model_data = get_model_data(brand)
    
    # Check that all models from values.py are in attributes.py
    missing_models = set(values_models.keys()) - set(model_data.keys())
    assert not missing_models, format_model_differences(missing_models, set(model_data.keys()))
    
    # Check that all models in attributes.py are in values.py
    extra_models = set(model_data.keys()) - set(values_models.keys())
    if extra_models:
        # Format message for extra models
        msg = ["Models found in attributes.py but missing from values.py:"]
        for model in sorted(extra_models):
            msg.append(f"  - {model}")
            similar = find_similar_models(model, set(values_models.keys()))
            if similar:
                msg.append("    Similar models found in values.py (possible year mismatch):")
                for similar_model in sorted(similar):
                    msg.append(f"      * {similar_model}")
                msg.append("    Suggestion: Check if the years need to be updated in values.py")
            else:
                msg.append("    No similar models found - this model may need to be removed from attributes.py")
        assert not extra_models, "\n".join(msg)
    
    # Check that metadata matches for each model
    for model_id, values_model in values_models.items():
        attrs_model = model_data[model_id]
        
        # Check basic metadata
        full_name = f"{attrs_model['make']} {attrs_model['model']}"
        assert full_name == values_model.name, \
            f"Model name mismatch for {brand} {model_id}:\n" \
            f"  values.py: {values_model.name}\n" \
            f"  attributes.py: {full_name}\n" \
            f"Suggestion: Update the make/model in attributes.py to match values.py"
        
        assert attrs_model["years"] == values_model.years, \
            f"Years mismatch for {brand} {model_id}:\n" \
            f"  values.py: {values_model.years}\n" \
            f"  attributes.py: {attrs_model['years']}\n" \
            f"Suggestion: Update the years list in attributes.py to match values.py"
        
        assert attrs_model["package"] == values_model.package, \
            f"Package mismatch for {brand} {model_id}:\n" \
            f"  values.py: {values_model.package}\n" \
            f"  attributes.py: {attrs_model['package']}\n" \
            f"Suggestion: Update the package in attributes.py to match values.py"
        
        assert attrs_model["platform"] == values_model.platform, \
            f"Platform mismatch for {brand} {model_id}:\n" \
            f"  values.py: {values_model.platform}\n" \
            f"  attributes.py: {attrs_model['platform']}\n" \
            f"Suggestion: Update the platform in attributes.py to match values.py"

def test_hyundai_model_consistency():
    """Test model consistency for Hyundai."""
    check_model_consistency_for_brand("hyundai")

def test_subaru_model_consistency():
    """Test model consistency for Subaru."""
    check_model_consistency_for_brand("subaru")

if __name__ == "__main__":
    # If a brand is specified as an argument, only test that brand
    import sys
    if len(sys.argv) > 1:
        brand = sys.argv[1].lower()
        check_model_consistency_for_brand(brand)
    else:
        # Otherwise test all brands
        pytest.main([__file__]) 